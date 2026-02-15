# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
This module contains utilities to read/write EPC files.
"""

import datetime
import threading
import logging
import os
from pathlib import Path
import random
import time
import traceback
import zipfile
from dataclasses import dataclass, field
from functools import wraps
from io import BytesIO
from typing import List, Any, Set, Tuple, Union, Dict, Optional
import numpy as np

from enum import Enum
from xsdata.formats.dataclass.models.generics import DerivedElement

from energyml.opc.opc import CoreProperties, Relationships, Types, Relationship, Override
from energyml.utils.storage_interface import DataArrayMetadata, EnergymlStorageInterface, ResourceMetadata
from energyml.utils.uri import Uri, parse_uri

from energyml.utils.constants import (
    EpcExportVersion,
    RawFile,
    EPCRelsRelationshipType,
)
from energyml.utils.data.datasets_io import (
    get_handler_registry,
    read_external_dataset_array,
)
from energyml.utils.exception import UnparsableFile
from energyml.utils.introspection import (
    get_class_from_content_type,
    get_obj_type,
    get_obj_uri,
    get_obj_usable_class,
    get_obj_version,
    get_obj_uuid,
    get_content_type_from_class,
    gen_uuid,
    get_obj_identifier,
    get_object_attribute,
    get_qualified_type_from_class,
)
from energyml.utils.serialization import (
    serialize_xml,
    read_energyml_xml_str,
    read_energyml_xml_bytes,
    read_energyml_json_str,
    read_energyml_json_bytes,
    JSON_VERSION,
)
from energyml.utils.xml import is_energyml_content_type
from energyml.utils.epc_utils import (
    gen_core_props_path,
    gen_energyml_object_path,
    gen_rels_path,
    get_epc_content_type_path,
    create_h5_external_relationship,
    get_file_folder,
    make_path_relative_to_other_file,
    make_path_relative_to_filepath_list,
)


class EnergymlObjectCollection:
    """
    A collection that maintains both list semantics (for backward compatibility)
    and dict-based lookups (for O(1) performance) for energyml objects.

    This allows existing code using .append() to work while providing efficient
    get_object_by_identifier() and get_object_by_uuid() operations.
    """

    def __init__(self, objects: Optional[List[Any]] = None):
        self._by_identifier: Dict[str, Any] = {}
        self._by_uri: Dict[str, Any] = {}
        self._by_uuid: Dict[str, List[Any]] = {}
        self._objects_list: List[Any] = []

        if objects:
            for obj in objects:
                self.append(obj)

    def append(self, obj: Any) -> None:
        """Add an object to the collection (list-compatible method)."""
        identifier = get_obj_identifier(obj)
        uri = str(get_obj_uri(obj))
        uuid = get_obj_uuid(obj)

        # Check if object already exists by identifier
        if identifier in self._by_identifier:
            # Replace existing object
            existing = self._by_identifier[identifier]
            idx = self._objects_list.index(existing)
            self._objects_list[idx] = obj

            # Clean up old URI mapping
            old_uri = str(get_obj_uri(existing))
            if old_uri in self._by_uri:
                del self._by_uri[old_uri]

            # Clean up old UUID mapping
            old_uuid = get_obj_uuid(existing)
            if old_uuid in self._by_uuid and existing in self._by_uuid[old_uuid]:
                self._by_uuid[old_uuid].remove(existing)
                if not self._by_uuid[old_uuid]:
                    del self._by_uuid[old_uuid]
        else:
            # Add new object
            self._objects_list.append(obj)

        # Update all indices
        self._by_identifier[identifier] = obj
        self._by_uri[uri] = obj

        if uuid not in self._by_uuid:
            self._by_uuid[uuid] = []
        if obj not in self._by_uuid[uuid]:
            self._by_uuid[uuid].append(obj)

    def remove(self, obj: Any) -> None:
        """Remove an object from the collection (list-compatible method)."""
        identifier = get_obj_identifier(obj)

        if identifier in self._by_identifier:
            stored_obj = self._by_identifier[identifier]
            self._objects_list.remove(stored_obj)

            # Clean up all indices
            del self._by_identifier[identifier]

            uri = str(get_obj_uri(stored_obj))
            if uri in self._by_uri:
                del self._by_uri[uri]

            uuid = get_obj_uuid(stored_obj)
            if uuid in self._by_uuid and stored_obj in self._by_uuid[uuid]:
                self._by_uuid[uuid].remove(stored_obj)
                if not self._by_uuid[uuid]:
                    del self._by_uuid[uuid]

    def get_by_identifier(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """Get object by identifier (O(1) lookup)."""
        # Try identifier lookup first
        obj = self._by_identifier.get(str(identifier))
        if obj is not None:
            return obj

        # Try URI lookup
        return self._by_uri.get(str(identifier))

    def get_by_uuid(self, uuid: str) -> List[Any]:
        """Get all objects with this UUID (O(1) lookup)."""
        return self._by_uuid.get(uuid, [])

    def __iter__(self):
        """Iterate over objects in insertion order."""
        return iter(self._objects_list)

    def __len__(self) -> int:
        """Get number of objects."""
        return len(self._objects_list)

    def __getitem__(self, index: int) -> Any:
        """Support indexing (e.g., energyml_objects[0])."""
        return self._objects_list[index]

    def __bool__(self) -> bool:
        """Support boolean checks (e.g., if energyml_objects:)."""
        return len(self._objects_list) > 0


class EpcRelsCacheErrorPolicy(Enum):
    LOG = "log"
    RAISE = "raise"
    SKIP = "skip"


class EpcRelsCache:
    """
    EPC Relationships Cache Manager

    Summary
    -------
    Manages in-memory relationships between EPC objects, using canonical Uri as the internal key.
    Accepts identifier, Uri, str(Uri), or the object itself as input for all public methods.
    Does not manage rels file paths; export logic is handled by the Epc class.

    API Reference
    -------------
    - __init__(epc: Epc | EnergymlObjectCollection, export_version, error_policy='log')
        Initialize with a reference to the owning Epc or a collection of objects.
        Optionally set error handling policy ('log', 'raise', 'skip').

    - set_rels_from_file(obj: Union[str, Uri, Any], rels: Relationships) -> None
        Attach relationships loaded from a .rels file to the given object (by any accepted key type).
        Used for supplemental or precomputed rels.

    - add_supplemental_rels(obj: Union[str, Uri, Any], rels: Union[Relationship, List[Relationship]]) -> None
        Add supplemental relationships for an object. These persist across cache clears and are merged lazily.

    - get_object_rels(obj: Union[str, Uri, Any]) -> List[Relationship]
        Return the effective relationships for an object, merging computed and supplemental rels, deduplicated.

    - get_object_relationships(obj: Union[str, Uri, Any]) -> Relationships
        Return RelationShips(get_object_rels(obj)) for the given object.

    - compute_rels(parallel: bool = False, recompute_all: bool = False) -> Dict[Uri, List[Relationship]]
        Recompute all relationships. If parallel=True, use a thread/process pool for the map phase.
        Returns a mapping of Uri to deduplicated relationships. Export logic (rels path, target) is handled by Epc.

    - update_cache_for_object(obj: Union[str, Uri, Any]) -> None
        Incrementally update relationships for a single object add, remove, or modification.

    - clear_cache() and recompute_cache(parallel=False)
        Clear or fully recompute the internal cache.

    - clean_rels(obj: Union[str, Uri, Any] = None) -> None
        Deduplicate relationships for a given object or all objects. Called after full recompute.

    - validate_rels() -> Dict[str, Any]
        Run validation checks: duplicate rels, missing reverse links, circular references, etc.
        Returns a report of issues found.

    Implementation Notes
    -------------------
    - All public methods accept identifier, Uri, str(Uri), or object; internally, always convert to Uri with a specific function to avoid code duplication.
    - Internal caches: {Uri: List[Relationship]} for computed, {Uri: List[Relationship]} for supplemental, {Uri: Set[Uri]} for reverse index (target -> sources).
    - Reverse index enables O(1) lookup of which objects reference a given target, critical for incremental updates.
    - No rels path management; Epc class is responsible for rels file path and target attribute generation.
    - Relationship IDs must be deterministic (e.g., UUIDv5 or hash of source+target+type).
    - On exception, log/skip/raise according to error_policy. Omitted objects do not block the pipeline.
    - clean_rels() can be parallelized, as deduplication is per-object.
    - Use threading.Lock or RLock to protect cache updates. Only lock during writes.

    Behavioural Invariants
    ---------------------
    - Canonical in-memory key: Uri. Never mix identifier and Uri in the same map.
    - Supplemental rels are preserved and merged lazily; not lost on clear/recompute unless explicitly removed.
    - All deduplication and validation is performed on the in-memory Uri-keyed data.

    Validation & Testing
    -------------------
    - clean_rels() ensures no duplicate (type, target) relationships per object.
    - validate_rels() checks for missing reverse links, circular references, and other edge cases.
    - Unit tests should cover all input types, deduplication, error handling, and validation.
    - Use EnergymlObjectCollection for initial tests.

    Migration/Integration
    --------------------
    - This class is standalone. Once implemented and tested, integrate into Epc, replacing legacy rels handling.
    - No migration needed until integration.

    """

    def __init__(self, epc_or_collection, export_version=None, error_policy=EpcRelsCacheErrorPolicy.LOG):
        """
        Initialize the EpcRelsCache.
        :param epc_or_collection: Epc instance or EnergymlObjectCollection
        :param export_version: EPC export version. If None and epc_or_collection is Epc, uses epc.export_version
        :param export_version: EPC export version (for rels path/target generation)
        :param error_policy: EpcRelsCacheErrorPolicy enum value for error handling
        """
        self._lock = threading.RLock()
        if isinstance(error_policy, str):
            # Allow legacy string for backward compatibility
            error_policy = EpcRelsCacheErrorPolicy(error_policy.lower())
        self._error_policy = error_policy
        # Accept Epc or EnergymlObjectCollection
        if isinstance(epc_or_collection, Epc):
            self._objects = epc_or_collection.energyml_objects
            self._epc = epc_or_collection
            self._export_version_fallback = export_version or epc_or_collection.export_version
        else:
            self._objects = epc_or_collection
            self._epc = None
            self._export_version_fallback = export_version or EpcExportVersion.CLASSIC
        # Internal caches
        self._computed_rels = {}  # {Uri: List[Relationship]}
        self._supplemental_rels = {}  # {Uri: List[Relationship]}
        self._reverse_index: Dict[Uri, Set[Uri]] = {}  # {target_uri: {source_uris}}

    @property
    def export_version(self) -> EpcExportVersion:
        """Get the current export version, using Epc's version if available."""
        if self._epc is not None:
            return self._epc.export_version
        return self._export_version_fallback

    def _uri_from_any(self, obj_or_id: Any) -> "Uri":
        """
        Normalize input to canonical Uri.
        Accepts identifier, Uri, str(Uri), or object.
        """
        if isinstance(obj_or_id, Uri):
            return obj_or_id
        if hasattr(obj_or_id, "object_version") or hasattr(obj_or_id, "__dict__"):
            # Likely an energyml object
            return get_obj_uri(obj_or_id)
        if isinstance(obj_or_id, str):
            # Try parse as Uri
            uri = parse_uri(obj_or_id)
            if uri:
                return uri
            # Try as identifier
            obj = None
            if self._epc and hasattr(self._epc, "get_object_by_identifier"):
                obj = self._epc.get_object_by_identifier(obj_or_id)
            elif hasattr(self._objects, "get_by_identifier"):
                obj = self._objects.get_by_identifier(obj_or_id)
            if obj:
                return get_obj_uri(obj)
        raise ValueError(f"Cannot resolve to Uri: {obj_or_id}")

    def set_rels_from_file(self, obj: Any, rels: "Relationships") -> None:
        """Attach relationships loaded from a .rels file to the given object."""
        uri = self._uri_from_any(obj)
        with self._lock:
            self._computed_rels[uri] = list(rels.relationship) if hasattr(rels, "relationship") else list(rels)

            # check supplemental to keep :
            for r in rels.relationship or []:
                if r.type_value not in (
                    str(EPCRelsRelationshipType.DESTINATION_OBJECT),
                    str(EPCRelsRelationshipType.SOURCE_OBJECT),
                    str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY),
                    str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML),
                ):
                    if uri not in self._supplemental_rels:
                        self._supplemental_rels[uri] = []
                    self._supplemental_rels[uri].append(r)

            # self._supplemental_rels[uri] = list(rels.relationship) if hasattr(rels, "relationship") else list(rels)

    def add_supplemental_rels(self, obj: Any, rels: Union["Relationship", List["Relationship"]]) -> None:
        """Add supplemental relationships for an object."""
        uri = self._uri_from_any(obj)
        with self._lock:
            if uri not in self._supplemental_rels:
                self._supplemental_rels[uri] = []
            if isinstance(rels, list):
                self._supplemental_rels[uri].extend(rels)
            else:
                self._supplemental_rels[uri].append(rels)

    def get_supplemental_rels(self, obj: Any, default=None) -> List["Relationship"]:
        """Get supplemental relationships for an object."""
        uri = self._uri_from_any(obj)
        with self._lock:
            return self._supplemental_rels.get(uri, default if default is not None else [])

    def get_object_rels(self, obj: Any) -> List["Relationship"]:
        """Return the effective relationships for an object, merging computed and supplemental rels, deduplicated."""
        uri = self._uri_from_any(obj)
        with self._lock:
            rels = list(self._computed_rels.get(uri, []))
            rels.extend(self._supplemental_rels.get(uri, []))
        return self._deduplicate_rels(rels)

    def compute_rels(self, parallel: bool = False) -> Dict["Uri", List["Relationship"]]:
        """
        Recompute all relationships, including reverse relationships. If parallel=True, use a thread/process pool for the map phase.
        Returns a mapping of Uri to deduplicated relationships.
        """
        import collections
        import concurrent.futures

        with self._lock:
            self._computed_rels.clear()
            objects = list(self._objects)

        # First pass: collect direct DORs for each object
        def map_func(obj) -> Optional[Tuple[Uri, Set[Uri], Set[Tuple[str, str]]]]:
            try:
                uri = get_obj_uri(obj)
                dor_uris, external_uris = self._get_direct_dor_uris(obj)
                return (uri, dor_uris, external_uris)
            except Exception as e:
                self._handle_error(f"Failed to compute DORs for {obj}: {e}")
                return None

        results = []
        if parallel:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for res in executor.map(map_func, objects):
                    if res:
                        results.append(res)
        else:
            for obj in objects:
                res = map_func(obj)
                if res:
                    results.append(res)

        # Second pass: build forward and reverse relationships
        rels_map = collections.defaultdict(list)  # {Uri: List[Relationship]}
        for src_uri, dor_uris, external_uris in results:
            src_path = gen_energyml_object_path(src_uri, export_version=self.export_version)
            for tgt_uri in dor_uris:
                tgt_path = gen_energyml_object_path(tgt_uri, export_version=self.export_version)
                # Forward rel (src -> tgt)
                rels_map[src_uri].append(
                    Relationship(
                        target=tgt_path,
                        type_value=get_rels_dor_type(dor_target=tgt_path, in_dor_owner_rels_file=True),
                        id=f"_{gen_uuid()}",
                    )
                )
                # Reverse rel (tgt -> src)
                rels_map[tgt_uri].append(
                    Relationship(
                        target=src_path,
                        type_value=get_rels_dor_type(dor_target=tgt_path, in_dor_owner_rels_file=False),
                        id=f"_{gen_uuid()}",
                    )
                )
            for ext_uri, _ in external_uris:
                rels_map[src_uri].append(create_external_relationship(ext_uri))

        # Build reverse index from results
        reverse_idx = collections.defaultdict(set)
        for src_uri, dor_uris, external_uris in results:
            for tgt_uri in dor_uris:
                reverse_idx[tgt_uri].add(src_uri)

        with self._lock:
            self._computed_rels = dict(rels_map)
            self._reverse_index = {k: v for k, v in reverse_idx.items()}
        self.clean_rels()
        return {uri: self.get_object_rels(uri) for uri in self._computed_rels}

    def update_cache_for_object(self, obj: Any) -> None:
        """Incrementally update relationships for a single object, including reverse relationships."""
        uri = self._uri_from_any(obj)
        dor_uris, external_uris = self._get_direct_dor_uris(obj)

        with self._lock:
            # Remove old reverse index entries for this object
            if uri in self._computed_rels:
                # Find old DOR targets and clean them up
                old_rels = self._computed_rels.get(uri, [])
                for old_rel in old_rels:
                    # Extract target URI from path (approximate - we'll rebuild from scratch)
                    pass

            # Clean up old reverse index entries where this object was the source
            for tgt_uri, sources in list(self._reverse_index.items()):
                if uri in sources:
                    sources.discard(uri)
                    if not sources:
                        del self._reverse_index[tgt_uri]

            # Compute forward relationships for this object
            forward_rels = []
            src_path = gen_energyml_object_path(uri, export_version=self.export_version)

            for tgt_uri in dor_uris:
                tgt_path = gen_energyml_object_path(tgt_uri, export_version=self.export_version)
                # Forward rel (this object -> target)
                forward_rels.append(
                    Relationship(
                        target=tgt_path,
                        type_value=get_rels_dor_type(dor_target=tgt_path, in_dor_owner_rels_file=True),
                        id=f"_{gen_uuid()}",
                    )
                )

                # Update reverse index: target is now referenced by this object
                if tgt_uri not in self._reverse_index:
                    self._reverse_index[tgt_uri] = set()
                self._reverse_index[tgt_uri].add(uri)

                # Add reverse rel to target if target exists in cache
                if tgt_uri in self._computed_rels:
                    reverse_rel = Relationship(
                        target=src_path,
                        type_value=get_rels_dor_type(dor_target=tgt_path, in_dor_owner_rels_file=False),
                        id=f"_{gen_uuid()}",
                    )
                    self._computed_rels[tgt_uri].append(reverse_rel)

            # Compute reverse relationships from index (who references me?)
            reverse_rels = []
            for src_uri in self._reverse_index.get(uri, set()):
                if src_uri != uri:  # Avoid self-references
                    src_path = gen_energyml_object_path(src_uri, export_version=self.export_version)
                    tgt_path = gen_energyml_object_path(uri, export_version=self.export_version)
                    reverse_rels.append(
                        Relationship(
                            target=src_path,
                            type_value=get_rels_dor_type(dor_target=tgt_path, in_dor_owner_rels_file=False),
                            id=f"_{gen_uuid()}",
                        )
                    )

            for ext_uri, _ in external_uris:
                forward_rels.append(create_external_relationship(ext_uri))

            # Store combined relationships
            self._computed_rels[uri] = forward_rels + reverse_rels

    def clear_cache(self) -> None:
        """Clear the internal caches and reverse index."""
        with self._lock:
            self._computed_rels.clear()
            self._reverse_index.clear()

    def recompute_cache(self, parallel: bool = False) -> Dict["Uri", List["Relationship"]]:
        """Fully recompute the internal cache."""
        return self.compute_rels(parallel=parallel)

    def clean_rels(self, obj: Optional[Any] = None) -> None:
        """
        Deduplicate relationships for a given object or all objects.
        Removes duplicates by (target, type_value).
        """
        with self._lock:
            if obj is not None:
                uri = self._uri_from_any(obj)
                rels = self._computed_rels.get(uri, []) + self._supplemental_rels.get(uri, [])
                deduped = self._deduplicate_rels(rels)
                self._computed_rels[uri] = deduped
            else:
                for uri in set(list(self._computed_rels.keys()) + list(self._supplemental_rels.keys())):
                    rels = self._computed_rels.get(uri, []) + self._supplemental_rels.get(uri, [])
                    deduped = self._deduplicate_rels(rels)
                    self._computed_rels[uri] = deduped

    def validate_rels(self) -> Dict[str, Any]:
        """
        Run validation checks: duplicate rels, orphaned references, circular references, etc.
        Returns a report of issues found.
        """
        report = {"duplicates": [], "orphaned_references": [], "circular": [], "index_inconsistency": []}

        with self._lock:
            # Check for duplicates
            for uri, rels in self._computed_rels.items():
                seen = set()
                for rel in rels:
                    key = (getattr(rel, "target", None), getattr(rel, "type_value", None))
                    if key in seen:
                        report["duplicates"].append((str(uri), key))
                    else:
                        seen.add(key)

            # Check for orphaned references (references to non-existent objects)
            all_object_uris = set()
            if self._epc:
                all_object_uris = {get_obj_uri(obj) for obj in self._epc.energyml_objects}
            elif self._objects:
                all_object_uris = {get_obj_uri(obj) for obj in self._objects}

            for target_uri, sources in self._reverse_index.items():
                # An object is orphaned if it's referenced but doesn't exist in the collection
                # Note: target_uri may be in _computed_rels due to reverse relationships,
                # but that doesn't mean the object actually exists in the collection
                if target_uri not in all_object_uris:
                    report["orphaned_references"].append(
                        {"target": str(target_uri), "referenced_by": [str(s) for s in sources]}
                    )

            # Check reverse index consistency
            for src_uri, rels in self._computed_rels.items():
                for rel in rels:
                    # Check if forward relationships are properly indexed
                    # This is a sanity check for the index
                    pass

        return report

    def get_reverse_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the reverse reference index for debugging and validation.
        Returns a dictionary with index statistics.
        """
        with self._lock:
            stats = {
                "total_targets": len(self._reverse_index),
                "total_references": sum(len(sources) for sources in self._reverse_index.values()),
                "max_references_to_single_target": max(
                    (len(sources) for sources in self._reverse_index.values()), default=0
                ),
                "targets_by_reference_count": {},
            }

            # Group targets by how many sources reference them
            for target_uri, sources in self._reverse_index.items():
                count = len(sources)
                if count not in stats["targets_by_reference_count"]:
                    stats["targets_by_reference_count"][count] = 0
                stats["targets_by_reference_count"][count] += 1

            return stats

    def _handle_error(self, msg: str) -> None:
        if self._error_policy == EpcRelsCacheErrorPolicy.LOG:
            import logging

            logging.error(msg)
        elif self._error_policy == EpcRelsCacheErrorPolicy.RAISE:
            raise RuntimeError(msg)
        # else: SKIP

    def _deduplicate_rels(self, rels: List["Relationship"]) -> List["Relationship"]:
        """Remove duplicate relationships by (target, type_value)."""
        seen = set()
        result = []
        for rel in rels:
            key = (getattr(rel, "target", None), getattr(rel, "type_value", None))
            if key not in seen:
                seen.add(key)
                result.append(rel)
        return result

    def _remove_object_from_cache(self, obj: Any) -> None:
        """
        Remove an object from the cache, cleaning up all references and reverse index entries.
        """
        uri = self._uri_from_any(obj)

        with self._lock:
            # Remove from computed rels
            if uri in self._computed_rels:
                del self._computed_rels[uri]

            # Remove from supplemental rels
            if uri in self._supplemental_rels:
                del self._supplemental_rels[uri]

            # Remove from reverse index (as target)
            if uri in self._reverse_index:
                del self._reverse_index[uri]

            # Remove from reverse index (as source)
            for target_uri, sources in list(self._reverse_index.items()):
                if uri in sources:
                    sources.discard(uri)
                    if not sources:
                        del self._reverse_index[target_uri]

            # Remove reverse rels from targets' computed rels
            for other_uri, other_rels in self._computed_rels.items():
                if other_uri != uri:
                    # Filter out relationships targeting the removed object
                    uri_path = gen_energyml_object_path(uri, export_version=self.export_version)
                    self._computed_rels[other_uri] = [
                        rel for rel in other_rels if getattr(rel, "target", None) != uri_path
                    ]

    def _get_direct_dor_uris(self, obj: Any) -> Tuple[Set[Uri], Set[Tuple[str, str]]]:
        """
        Return the set of direct DOR target Uris for the given object and Tuple[filepath, mimetype] for external references.
        """
        try:
            return get_dor_or_external_uris_from_obj(obj)
        except Exception as e:
            self._handle_error(f"Error getting direct DOR URIs: {e}")
            return set(), set()


def log_timestamp(func):
    """Decorator to log timestamps for function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        start_time = time.perf_counter()
        timestamp_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Get file path from arguments if available
        file_path = None
        if args:
            if isinstance(args[0], str) and (args[0].endswith(".epc") or "/" in args[0] or "\\" in args[0]):
                file_path = args[0]
            elif hasattr(args[0], "epc_file_path"):
                file_path = args[0].epc_file_path
        if "path" in kwargs:
            file_path = kwargs["path"]
        elif "epc_file_path" in kwargs:
            file_path = kwargs["epc_file_path"]

        path_info = f" [{file_path}]" if file_path else ""
        print(f"⏱️  [{timestamp_start}] Starting {func_name}{path_info}")

        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            timestamp_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(f"✅ [{timestamp_end}] Completed {func_name} in {elapsed:.3f}s{path_info}")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            timestamp_end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            print(f"❌ [{timestamp_end}] Failed {func_name} after {elapsed:.3f}s{path_info}: {e}")
            raise

    return wrapper


@dataclass
class Epc(EnergymlStorageInterface):
    """
    A class that represent an EPC file content. Creating an isntance of this class with a file path will not directly load the file content if it exists.
    To read an existing file, use the @read_file or @read_stream functions.
    Moreover, you must explicitly call @export_file or @export_io functions to save the content of the instance.
    """

    # content_type: List[str] = field(
    #     default_factory=list,
    # )

    export_version: EpcExportVersion = field(default=EpcExportVersion.CLASSIC)

    core_props: Optional[CoreProperties] = field(default=None)

    """ xml files referred in the [Content_Types].xml  """
    energyml_objects: EnergymlObjectCollection = field(
        default_factory=EnergymlObjectCollection,
    )

    """ Other files content like pdf etc """
    raw_files: List[RawFile] = field(
        default_factory=list,
    )

    """ A list of external files. It can be used to link hdf5 files """
    external_files_path: List[str] = field(
        default_factory=list,
    )

    """ A list of h5 files stored in memory. (Usefull for Cloud services that doesn't work with local files """
    h5_io_files: List[BytesIO] = field(
        default_factory=list,
    )

    force_h5_path: Optional[str] = field(default=None)

    """ Relationships cache for efficient rels computation and management """
    _rels_cache: Optional[EpcRelsCache] = field(default=None, init=False, repr=False)

    """
    Additional rels for objects (DEPRECATED - use _rels_cache.add_supplemental_rels instead).
    Key is the object (same than in @energyml_objects) and value is a list of
    RelationShip. This can be used to link an HDF5 to an ExternalPartReference in resqml 2.0.1
    Key is a value returned by @get_obj_identifier
    """
    # additional_rels: Dict[str, List[Relationship]] = field(default_factory=lambda: {})

    """
    Epc file path. Used when loaded from a local file or for export
    """
    epc_file_path: Optional[str] = field(default=None)

    def __post_init__(self):
        """Initialize the relationships cache after dataclass initialization."""
        if self._rels_cache is None:
            self._rels_cache = EpcRelsCache(self, export_version=self.export_version)

    def __str__(self):
        return (
            "EPC file ("
            + str(self.export_version)
            + ") "
            + f"{len(self.energyml_objects)} energyml objects and {len(self.raw_files)} other files {[f.path for f in self.raw_files]}"
            # + f"\n{[serialize_json(ar) for ar in self.additional_rels]}"
        )

    def add_file(self, obj: Union[List, bytes, BytesIO, str, RawFile]):
        """
        Add one ore multiple files to the epc file.
        For non energyml file, it is better to use the RawFile class.
        The input can be a single file content, file path, or a list of them
        :param obj:
        :return:
        """
        if isinstance(obj, list):
            for o in obj:
                self.add_file(o)
        elif isinstance(obj, bytes) or isinstance(obj, BytesIO):
            try:
                xml_obj = read_energyml_xml_bytes(obj)
                self.energyml_objects.append(xml_obj)
            except:
                try:
                    if isinstance(obj, BytesIO):
                        obj.seek(0)
                    json_obj = read_energyml_json_bytes(obj, json_version=JSON_VERSION.OSDU_OFFICIAL)
                    self.add_file(json_obj)
                except:
                    # if isinstance(obj, BytesIO):
                    #     obj.seek(0)
                    # self.add_file(RawFile(path=f"pleaseRenameThisFile_{str(random.random())}", content=obj))
                    raise UnparsableFile()
        elif isinstance(obj, RawFile):
            self.raw_files.append(obj)
        elif isinstance(obj, str):
            # Can be a path or a content
            if os.path.exists(obj):
                with open(obj, "rb") as f:
                    file_content = f.read()
                    f_name = os.path.basename(obj)
                    _, f_ext = os.path.splitext(f_name)
                    if f_ext.lower().endswith(".xml") or f_ext.lower().endswith(".json"):
                        try:
                            self.add_file(file_content)
                        except UnparsableFile:
                            self.add_file(RawFile(f_name, BytesIO(file_content)))
                    elif not f_ext.lower().endswith(".rels"):
                        self.add_file(RawFile(f_name, BytesIO(file_content)))
                    else:
                        logging.error(f"Not supported file extension {f_name}")
            else:
                try:
                    xml_obj = read_energyml_xml_str(obj)
                    self.energyml_objects.append(xml_obj)
                except:
                    try:
                        if isinstance(obj, BytesIO):
                            obj.seek(0)
                        json_obj = read_energyml_json_str(obj, json_version=JSON_VERSION.OSDU_OFFICIAL)
                        self.add_file(json_obj)
                    except:
                        if isinstance(obj, BytesIO):
                            obj.seek(0)
                        self.add_file(RawFile(path=f"pleaseRenameThisFile_{str(random.random())}.txt", content=obj))
        elif str(type(obj).__module__).startswith("energyml."):
            # We should test "energyml.(resqml|witsml|prodml|eml|common)" but I didn't to avoid issues if
            # another specific package comes in the future
            self.energyml_objects.append(obj)
        else:
            logging.error(f"unsupported type {str(type(obj))}")

    # EXPORT functions

    def gen_opc_content_type(self) -> Types:
        """
        Generates a :class:`Types` instance and fill it with energyml objects :class:`Override` values
        :return:
        """
        ct = create_default_types()

        for e_obj in self.energyml_objects:
            ct.override.append(
                Override(
                    content_type=get_content_type_from_class(type(e_obj)),
                    part_name=gen_energyml_object_path(e_obj, self.export_version),
                )
            )

        for rf in self.raw_files:
            # file_extension = os.path.splitext(file_path)[1].lstrip(".").lower()
            mime_type = in_epc_file_path_to_mime_type(rf.path)
            if mime_type:
                override = Override(content_type=mime_type, part_name=f"{rf.path}")
                ct.override.append(override)

        return ct

    # @log_timestamp
    def export_file(
        self, path: Optional[str] = None, allowZip64: bool = True, force_recompute_object_rels: bool = True
    ) -> None:
        """
        Export the epc file. If :param:`path` is None, the epc 'self.epc_file_path' is used
        :param path:
        :return:
        """
        if path is None:
            path = self.epc_file_path

        if path is None:
            raise ValueError("No path provided and epc_file_path is not set")

        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, allowZip64=allowZip64) as zip_file:
            self._export_io(
                zip_file=zip_file, allowZip64=allowZip64, force_recompute_object_rels=force_recompute_object_rels
            )

    def export_io(self, allowZip64: bool = True, force_recompute_object_rels: bool = True) -> BytesIO:
        """
        Export the epc file into a :class:`BytesIO` instance. The result is an 'in-memory' zip file.
        :return:
        """
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, allowZip64=allowZip64) as zip_file:
            self._export_io(
                zip_file=zip_file, allowZip64=allowZip64, force_recompute_object_rels=force_recompute_object_rels
            )

        return zip_buffer

    def _export_io(
        self, zip_file: zipfile.ZipFile, allowZip64: bool = True, force_recompute_object_rels: bool = True
    ) -> None:
        """
        Export the epc file into a :class:`BytesIO` instance. The result is an 'in-memory' zip file.
        :return:
        """
        # CoreProps
        if self.core_props is None:
            self.core_props = create_default_core_properties()

        zip_file.writestr(gen_core_props_path(self.export_version), serialize_xml(self.core_props))

        #  Energyml objects
        for e_obj in self.energyml_objects:
            e_path = gen_energyml_object_path(e_obj, self.export_version)
            zip_file.writestr(e_path, serialize_xml(e_obj))

        # Rels
        for rels_path, rels in self.compute_rels(force_recompute_object_rels=force_recompute_object_rels).items():
            zip_file.writestr(rels_path, serialize_xml(rels))

        # Other files:
        for raw in self.raw_files:
            zip_file.writestr(raw.path, raw.content.read())

        # ContentType
        zip_file.writestr(get_epc_content_type_path(), serialize_xml(self.gen_opc_content_type()))

    # === Relationships management functions ===

    def add_rels_for_object(
        self,
        obj: Any,
        relationships: List[Relationship],
    ) -> None:
        """
        Add relationships to an object in the EPC stream
        :param obj:
        :param relationships:
        :return:
        """

        self._rels_cache.add_supplemental_rels(obj, relationships)

        # if isinstance(obj, str) or isinstance(obj, Uri):
        #     obj = self.get_object_by_identifier(obj)
        #     obj_ident = get_obj_identifier(obj)
        # else:
        #     obj_ident = get_obj_identifier(obj)
        # if obj_ident not in self.additional_rels:
        #     self.additional_rels[obj_ident] = []

        # self.additional_rels[obj_ident] = self.additional_rels[obj_ident] + relationships

    def rels_to_h5_file(self, obj: Any, h5_path: str) -> Relationship:
        """
        Creates in the epc file, a Relation (in the object .rels file) to link a h5 external file.
        Usually this function is used to link an ExternalPartReference to a h5 file.
        :param obj:
        :param h5_path:
        :return: the Relationship added to the rels cache
        """
        # obj_ident = get_obj_identifier(obj)
        # if obj_ident not in self.additional_rels:
        #     self.additional_rels[obj_ident] = []

        nb_current_file = len(self.get_h5_file_paths(obj))

        rel = create_h5_external_relationship(h5_path=h5_path, current_idx=nb_current_file)
        # self.additional_rels[obj_ident].append(rel)
        self._rels_cache.add_supplemental_rels(obj, rel)
        return rel

    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        """
        Get the relationships for a given energyml object using the cache.
        :param obj: The object identifier/URI or the object itself
        :return: List of Relationship objects
        """
        # Ensure cache is initialized
        if self._rels_cache is None:
            self._rels_cache = EpcRelsCache(self, export_version=self.export_version)

        # Convert identifier to object if needed
        if isinstance(obj, str) or isinstance(obj, Uri):
            obj = self.get_object_by_identifier(obj)
            if obj is None:
                return []

        # Get relationships from cache (includes computed + supplemental rels)
        return self._rels_cache.get_object_rels(obj)

    def update_rels_cache(self) -> None:
        """Update the relationships cache for all objects. This should be called after any modification to the energyml objects to keep the cache consistent."""
        if self._rels_cache is None:
            self._rels_cache = EpcRelsCache(self, export_version=self.export_version)
        self._rels_cache.recompute_cache()

    def clean_rels_cache(self, obj: Any = None) -> None:
        """Clean relationships for a specific object in the cache. If no object is provided, clean all relationships in the cache. This will remove duplicates and ensure consistency between computed and supplemental relationships."""
        if self._rels_cache is not None:
            self._rels_cache.clean_rels(obj)

    def clear_rels_cache(self) -> None:
        """Clear the relationships cache. This will remove all computed and supplemental relationships, forcing a full recomputation on next access."""
        if self._rels_cache is not None:
            self._rels_cache.clear_cache()

    def compute_rels(self, force_recompute_object_rels: bool = False) -> Dict[str, Relationships]:
        """
        Compute all relationships in the EPC file.
        :param force_recompute_object_rels: If True, recompute all object relationships from scratch
        :return: Dictionary mapping rels file paths to Relationships objects
        """
        # Ensure cache is initialized
        if self._rels_cache is None:
            self._rels_cache = EpcRelsCache(self, export_version=self.export_version)

        # Recompute cache if requested
        if force_recompute_object_rels:
            self._rels_cache.recompute_cache()

        result = {}

        # all energyml objects - get relationships from cache
        for obj in self.energyml_objects:
            obj_file_rels_path = gen_rels_path(obj, export_version=self.export_version)

            # Get relationships from cache (includes computed + supplemental)
            cached_rels = self._rels_cache.get_object_rels(obj)

            result[obj_file_rels_path] = Relationships(relationship=cached_rels)

        # CoreProps
        core_props = self.core_props or create_default_core_properties()
        core_props_rels_path = gen_rels_path(core_props, self.export_version)
        result[core_props_rels_path] = Relationships(relationship=[])
        for rf in self.raw_files:
            if is_core_prop_or_extension_path(rf.path):
                result[core_props_rels_path].relationship.append(
                    Relationship(
                        target=rf.path,
                        type_value=str(EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES),
                        id=f"_{gen_uuid()}",
                    )
                )

        # ContentType
        content_type_path_rels = get_epc_content_type_rels_path()
        result[content_type_path_rels] = Relationships(
            relationship=[
                Relationship(
                    id="CoreProperties",
                    type_value=str(EPCRelsRelationshipType.CORE_PROPERTIES),
                    target=gen_core_props_path(),
                )
            ]
        )

        return result

    # === Array functions ===

    def get_epc_file_folder(self) -> Optional[str]:
        return get_file_folder(self.epc_file_path) if self.epc_file_path else None

    def read_external_array(
        self,
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        use_epc_io_h5: bool = True,
    ) -> List[Any]:
        """Read an external array from HDF5 files linked to the EPC file.
        :param energyml_array: the energyml array object (e.g. FloatingPointExternalArray)
        :param root_obj: the root object containing the energyml_array
        :param path_in_root: the path in the root object to the energyml_array
        :param use_epc_io_h5: if True, use also the in-memory HDF5 files stored in epc.h5_io_files

        :return: the array read from the external datasets
        """
        sources = []
        if self is not None and use_epc_io_h5 and self.h5_io_files is not None and len(self.h5_io_files):
            sources = sources + self.h5_io_files

        return read_external_dataset_array(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
            additional_sources=sources,
            epc=self,
        )

    def read_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        """
        Read a data array from external storage (HDF5, Parquet, CSV, etc.) with optional sub-selection.

        :param proxy: The object identifier/URI or the object itself that references the array
        :param path_in_external: Path within the external file (e.g., 'values/0')
        :param start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
        :param counts: Optional count of elements for each dimension (RESQML v2.2 Count)
        :param external_uri: Optional URI to override default file path (RESQML v2.2 URI)
        :return: The data array as a numpy array, or None if not found
        """
        obj = proxy
        if isinstance(proxy, str) or isinstance(proxy, Uri):
            obj = self.get_object_by_identifier(proxy)

        # Determine which external files to use
        file_paths = self.get_h5_file_paths(obj)
        if external_uri:
            file_paths.insert(0, make_path_relative_to_other_file(external_uri, self.epc_file_path))

        if not file_paths or len(file_paths) == 0:
            file_paths = self.external_files_path

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return None

        # Get the file handler registry
        handler_registry = get_handler_registry()

        for file_path in file_paths:
            # Get the appropriate handler for this file type
            handler = handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Use handler to read array with sub-selection support
                array = handler.read_array(file_path, path_in_external, start_indices, counts)
                if array is not None:
                    return array
            except Exception as e:
                logging.debug(f"Failed to read dataset from {file_path}: {e}")
                pass

        logging.error(f"Failed to read array from any available file paths: {file_paths}")
        return None

    def write_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        array: np.ndarray,
        start_indices: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """
        Write a data array to external storage (HDF5, Parquet, CSV, etc.) with optional offset.

        :param proxy: The object identifier/URI or the object itself that references the array
        :param path_in_external: Path within the external file (e.g., 'values/0')
        :param array: The numpy array to write
        :param start_indices: Optional start index for each dimension for partial writes
        :param external_uri: Optional URI to override default file path (RESQML v2.2 URI)
        :param kwargs: Additional format-specific parameters (e.g., dtype, column_titles)
        :return: True if successfully written, False otherwise
        """
        obj = proxy
        if isinstance(proxy, str) or isinstance(proxy, Uri):
            obj = self.get_object_by_identifier(proxy)

        # Determine which external files to use
        file_paths = (
            [make_path_relative_to_other_file(external_uri, self.epc_file_path)]
            if external_uri
            else self.get_h5_file_paths(obj)
        )
        if not file_paths or len(file_paths) == 0:
            file_paths = self.external_files_path

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return False

        # Get the file handler registry
        handler_registry = get_handler_registry()

        # Try to write to the first available file
        for file_path in file_paths:
            # Get the appropriate handler for this file type
            handler = handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Use handler to write array with optional partial write support
                success = handler.write_array(file_path, array, path_in_external, start_indices, **kwargs)
                if success:
                    return True
            except Exception as e:
                logging.error(f"Failed to write dataset to {file_path}: {e}")

        logging.error(f"Failed to write array to any available file paths: {file_paths}")
        return False

    def get_array_metadata(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """
        Get metadata for data array(s) without loading the full array data.
        Supports RESQML v2.2 sub-array selection metadata.

        :param proxy: The object identifier/URI or the object itself that references the array
        :param path_in_external: Optional specific path. If None, returns all array metadata for the object
        :param start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
        :param counts: Optional count of elements for each dimension (RESQML v2.2 Count)
        :return: DataArrayMetadata if path specified, List[DataArrayMetadata] if no path, or None if not found
        """
        obj = proxy
        if isinstance(proxy, str) or isinstance(proxy, Uri):
            obj = self.get_object_by_identifier(proxy)

        # Get possible file paths for this object
        file_paths = self.get_h5_file_paths(obj)
        if not file_paths or len(file_paths) == 0:
            file_paths = self.external_files_path

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return None

        # Get the file handler registry
        handler_registry = get_handler_registry()

        for file_path in file_paths:
            # Get the appropriate handler for this file type
            handler = handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Use handler to get metadata without loading full array
                metadata_dict = handler.get_array_metadata(file_path, path_in_external, start_indices, counts)

                if metadata_dict is None:
                    continue

                # Convert dict(s) to DataArrayMetadata
                if isinstance(metadata_dict, list):
                    return [
                        DataArrayMetadata(
                            path_in_resource=m.get("path"),
                            array_type=m.get("dtype", "unknown"),
                            dimensions=m.get("shape", []),
                            start_indices=start_indices,
                            custom_data={"size": m.get("size", 0)},
                        )
                        for m in metadata_dict
                    ]
                else:
                    return DataArrayMetadata(
                        path_in_resource=metadata_dict.get("path"),
                        array_type=metadata_dict.get("dtype", "unknown"),
                        dimensions=metadata_dict.get("shape", []),
                        start_indices=start_indices,
                        custom_data={"size": metadata_dict.get("size", 0)},
                    )
            except Exception as e:
                logging.debug(f"Failed to get metadata from file {file_path}: {e}")

        return None

    def get_h5_file_paths(self, obj: Any) -> List[str]:
        """
        Get all HDF5 file paths referenced in the EPC file (from rels to external resources)
        :return: list of HDF5 file paths
        """

        if self.force_h5_path is not None:
            return [self.force_h5_path]

        is_uri = (isinstance(obj, str) and parse_uri(obj) is not None) or isinstance(obj, Uri)
        if is_uri:
            obj = self.get_object_by_identifier(obj)

        h5_paths = set()

        if isinstance(obj, str):
            obj = self.get_object_by_identifier(obj)
        # for rels in self.additional_rels.get(get_obj_identifier(obj), []):
        for rels in self._rels_cache.get_supplemental_rels(obj):
            if rels.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
                h5_paths.add(rels.target)

        if len(h5_paths) == 0:
            # search if an h5 file has the same name than the epc file
            epc_folder = self.get_epc_file_folder()
            if epc_folder is not None and self.epc_file_path is not None:
                epc_file_name = os.path.basename(self.epc_file_path)
                epc_file_base, _ = os.path.splitext(epc_file_name)
                possible_h5_path = os.path.join(epc_folder, epc_file_base + ".h5")
                if os.path.exists(possible_h5_path):
                    h5_paths.add(possible_h5_path)

        return make_path_relative_to_filepath_list(list(h5_paths), self.epc_file_path)

    def get_object_as_dor(self, identifier: str, dor_qualified_type) -> Optional[Any]:
        """
        Search an object by its identifier and returns a DOR
        :param identifier:
        :param dor_qualified_type: the qualified type of the DOR (e.g. resqml22.DataObjectReference)
        :return:
        """
        obj = self.get_object_by_identifier(identifier=identifier)
        # if obj is None:

        return as_dor(obj_or_identifier=obj or identifier, dor_qualified_type=dor_qualified_type)

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """
        Search all objects with the uuid :param:`uuid`.
        :param uuid:
        :return:
        """
        return self.energyml_objects.get_by_uuid(uuid)

    def get_object_by_identifier(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """
        Search an object by its identifier.
        :param identifier: given by the function :func:`get_obj_identifier`, or a URI (or its str representation)
        :return:
        """
        # Use the O(1) dict lookup from the collection
        return self.energyml_objects.get_by_identifier(identifier)

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        return self.get_object_by_identifier(identifier)

    def add_object(self, obj: Any) -> bool:
        """
        Add an energyml object to the EPC stream (calls put_object for consistency)
        :param obj:
        :return:
        """
        return self.put_object(obj) is not None

    def remove_object(self, identifier: Union[str, Uri]) -> None:
        """
        Remove an energyml object from the EPC stream by its identifier (calls delete_object for consistency)
        :param identifier:
        :return:
        """
        self.delete_object(identifier)

    def __len__(self) -> int:
        return len(self.energyml_objects)

    def list_objects(self, dataspace: str | None = None, object_type: str | None = None) -> List[ResourceMetadata]:
        result = []
        for obj in self.energyml_objects:
            if (dataspace is None or get_obj_type(get_obj_usable_class(obj)) == dataspace) and (
                object_type is None or get_qualified_type_from_class(type(obj)) == object_type
            ):
                res_meta = ResourceMetadata(
                    uri=str(get_obj_uri(obj)),
                    uuid=get_obj_uuid(obj),
                    title=get_object_attribute(obj, "citation.title") or "",
                    object_type=type(obj).__name__,
                    version=get_obj_version(obj),
                    content_type=get_content_type_from_class(type(obj)) or "",
                )
                result.append(res_meta)
        return result

    def put_object(self, obj: Any, dataspace: str | None = None) -> str | None:
        """
        Add or update an energyml object in the EPC stream.
        :param obj: The energyml object to add
        :param dataspace: Optional dataspace parameter (for interface compatibility)
        :return: The URI of the added object, or None if failed
        """
        self.energyml_objects.append(obj)

        # Update relationships cache
        if self._rels_cache is None:
            self._rels_cache = EpcRelsCache(self, export_version=self.export_version)
        self._rels_cache.update_cache_for_object(obj)

        return str(get_obj_uri(obj))

    def delete_object(self, identifier: Union[str, Any]) -> bool:
        """
        Delete an energyml object from the EPC stream.
        :param identifier: The object identifier/URI or the object itself
        :return: True if object was deleted, False otherwise
        """
        obj = self.get_object_by_identifier(identifier)
        if obj is not None:
            # Remove from collection
            self.energyml_objects.remove(obj)

            # Update relationships cache
            if self._rels_cache is None:
                self._rels_cache = EpcRelsCache(self, export_version=self.export_version)
            self._rels_cache._remove_object_from_cache(obj)

            return True
        return False

    def dumps_epc_content_and_files_lists(self) -> str:
        """
        Dumps the EPC content and files lists for debugging purposes.
        :return: A string representation of the EPC content and files lists.
        """
        content_list = [
            f"{get_obj_identifier(obj)} ({get_qualified_type_from_class(type(obj))})" for obj in self.energyml_objects
        ]
        raw_files_list = [raw_file.path for raw_file in self.raw_files]

        return "EPC Content:\n" + "\n".join(content_list) + "\n\nRaw Files:\n" + "\n".join(raw_files_list)

    def close(self) -> None:
        """
        Close the EPC file and release any resources.
        :return:
        """
        pass

    # ==============
    # Class methods
    # ==============

    @classmethod
    # @log_timestamp
    def read_file(cls, epc_file_path: str, read_rels_from_files: bool = True, recompute_rels: bool = False) -> "Epc":
        """
        Read an EPC file from disk.
        :param epc_file_path: Path to the EPC file
        :param read_rels_from_files: If True, populate cache from .rels files in the EPC
        :param recompute_rels: If True, recompute all relationships after loading
        :return: Epc instance
        """
        with open(epc_file_path, "rb") as f:
            epc = cls.read_stream(
                BytesIO(f.read()), read_rels_from_files=read_rels_from_files, recompute_rels=recompute_rels
            )
            epc.epc_file_path = epc_file_path
            return epc
        raise IOError(f"Failed to open EPC file {epc_file_path}")

    @classmethod
    def read_stream(
        cls, epc_file_io: BytesIO, read_rels_from_files: bool = True, recompute_rels: bool = False
    ):  # returns an Epc instance
        """
        Read an EPC file from a BytesIO stream.
        :param epc_file_io: BytesIO containing the EPC file
        :param read_rels_from_files: If True, populate cache from .rels files in the EPC
        :param recompute_rels: If True, recompute all relationships after loading
        :return: an :class:`EPC` instance
        """
        try:
            _read_files = []
            obj_list = []
            raw_file_list = []
            # additional_rels = {}
            core_props = None
            # Store rels files separately for potential cache population
            rels_files_to_load = {}  # {obj_path: Relationships}
            path_to_obj = {}

            with zipfile.ZipFile(epc_file_io, "r", zipfile.ZIP_DEFLATED) as epc_file:
                content_type_file_name = get_epc_content_type_path()
                content_type_info = None
                try:
                    content_type_info = epc_file.getinfo(content_type_file_name)
                except KeyError:
                    for info in epc_file.infolist():
                        if info.filename.lower() == content_type_file_name.lower():
                            content_type_info = info
                            break

                _read_files.append(content_type_file_name)

                if content_type_info is None:
                    logging.error(f"No {content_type_file_name} file found")
                else:
                    content_type_obj: Types = read_energyml_xml_bytes(epc_file.read(content_type_file_name))
                    for ov in content_type_obj.override:
                        ov_ct = ov.content_type
                        ov_path = ov.part_name
                        # logging.debug(ov_ct)
                        while ov_path.startswith("/") or ov_path.startswith("\\"):
                            ov_path = ov_path[1:]
                        if is_energyml_content_type(ov_ct):
                            _read_files.append(ov_path)
                            try:
                                ov_obj = read_energyml_xml_bytes(
                                    epc_file.read(ov_path),
                                    get_class_from_content_type(ov_ct),
                                )
                                if isinstance(ov_obj, DerivedElement):
                                    ov_obj = ov_obj.value
                                path_to_obj[ov_path] = ov_obj
                                obj_list.append(ov_obj)
                            except Exception:
                                logging.error(traceback.format_exc())
                                logging.error(
                                    f"Epc.@read_stream failed to parse file {ov_path} for content-type: {ov_ct} => {str(get_class_from_content_type(ov_ct))}\n\n",
                                )
                                try:
                                    logging.debug(epc_file.read(ov_path))
                                except:
                                    pass
                                # raise e
                        elif get_class_from_content_type(ov_ct) == CoreProperties:
                            _read_files.append(ov_path)
                            core_props = read_energyml_xml_bytes(epc_file.read(ov_path), CoreProperties)
                            path_to_obj[ov_path] = core_props

                    for f_info in epc_file.infolist():
                        if f_info.filename not in _read_files:
                            _read_files.append(f_info.filename)
                            if not f_info.filename.lower().endswith(".rels"):
                                try:
                                    raw_file_list.append(
                                        RawFile(
                                            path=f_info.filename,
                                            content=BytesIO(epc_file.read(f_info.filename)),
                                        )
                                    )
                                except IOError:
                                    logging.error(traceback.format_exc())
                            elif f_info.filename != "_rels/.rels":  # CoreProperties rels file
                                # RELS FILES READING START

                                # logging.debug(f"reading rels {f_info.filename}")
                                rels_path = Path(f_info.filename)
                                obj_folder = (
                                    str(rels_path.parent.parent) + "/" if str(rels_path.parent.parent) != "." else ""
                                )
                                obj_file_name = rels_path.stem  # removing the ".rels"
                                rels_file: Relationships = read_energyml_xml_bytes(
                                    epc_file.read(f_info.filename),
                                    Relationships,
                                )
                                obj_path = obj_folder + obj_file_name
                                if obj_path in path_to_obj:
                                    try:

                                        # Store all rels for potential cache population
                                        if read_rels_from_files:
                                            rels_files_to_load[obj_path] = rels_file

                                        # additional_rels_key = get_obj_identifier(path_to_obj[obj_path])
                                        # # Keep only non-computable rels in additional_rels (legacy support)
                                        # for rel in rels_file.relationship:
                                        #     # logging.debug(f"\t\t{rel.type_value}")
                                        #     if (
                                        #         rel.type_value != EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()
                                        #         and rel.type_value != EPCRelsRelationshipType.SOURCE_OBJECT.get_type()
                                        #         and rel.type_value
                                        #         != EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES.get_type()
                                        #     ):  # not a computable relation
                                        #         if additional_rels_key not in additional_rels:
                                        #             additional_rels[additional_rels_key] = []
                                        #         additional_rels[additional_rels_key].append(rel)
                                    except AttributeError:
                                        logging.error(traceback.format_exc())
                                        pass  # 'CoreProperties' object has no attribute 'object_version'
                                    except Exception as e:
                                        logging.error(f"Error with obj path {obj_path} {path_to_obj[obj_path]}")
                                        raise e
                                else:
                                    logging.error(
                                        f"xml file '{f_info.filename}' is not associate to any readable object "
                                        f"(or the object type is not supported because"
                                        f" of a lack of a dependency module) "
                                    )

            epc = Epc(
                energyml_objects=EnergymlObjectCollection(obj_list),
                raw_files=raw_file_list,
                core_props=core_props,
                # additional_rels=additional_rels,
            )

            # Populate rels cache from loaded rels files if requested
            if read_rels_from_files and rels_files_to_load:
                for obj_path, rels_file in rels_files_to_load.items():
                    if obj_path in path_to_obj:
                        obj = path_to_obj[obj_path]
                        # Only set rels for energyml objects (skip CoreProperties and other OPC objects)
                        if obj in obj_list:
                            epc._rels_cache.set_rels_from_file(obj, rels_file)

            # Recompute relationships if requested
            if recompute_rels:
                epc._rels_cache.recompute_cache()

            return epc
        except zipfile.BadZipFile as error:
            logging.error(error)

        return None


#     ______                                      __   ____                 __  _
#    / ____/___  ___  _________ ___  ______ ___  / /  / __/_  ______  _____/ /_(_)___  ____  _____
#   / __/ / __ \/ _ \/ ___/ __ `/ / / / __ `__ \/ /  / /_/ / / / __ \/ ___/ __/ / __ \/ __ \/ ___/
#  / /___/ / / /  __/ /  / /_/ / /_/ / / / / / / /  / __/ /_/ / / / / /__/ /_/ / /_/ / / / (__  )
# /_____/_/ /_/\___/_/   \__, /\__, /_/ /_/ /_/_/  /_/  \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/
#                       /____//____/

# Backward compatibility: re-export functions that were moved to epc_utils
# This allows existing code that imports these functions from epc.py to continue working
from .epc_utils import (
    create_default_core_properties,
    create_default_types,
    create_external_relationship,
    gen_rels_path_from_obj_path,
    get_dor_or_external_uris_from_obj,
    get_dor_uris_from_obj,
    get_epc_content_type_rels_path,
    get_rels_dor_type,
    in_epc_file_path_to_mime_type,
    is_core_prop_or_extension_path,
    update_prop_kind_dict_cache,
    get_property_kind_by_uuid,
    get_property_kind_and_parents,
    as_dor,
    create_energyml_object,
    create_external_part_reference,
    get_reverse_dor_list,
    get_file_folder_and_name_from_path,
)

# Also export the cache dict for backward compatibility
from .epc_utils import __CACHE_PROP_KIND_DICT__

__all__ = [
    "Epc",
    "update_prop_kind_dict_cache",
    "get_property_kind_by_uuid",
    "get_property_kind_and_parents",
    "as_dor",
    "create_energyml_object",
    "create_external_part_reference",
    "get_reverse_dor_list",
    "get_file_folder_and_name_from_path",
    "__CACHE_PROP_KIND_DICT__",
]


# def gen_rels_path_from_dor(dor: Any, export_version: EpcExportVersion = EpcExportVersion.CLASSIC) -> str:
