# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Memory-efficient EPC file handler for large files.

This module provides EpcStreamReader - a lazy-loading, memory-efficient alternative
to the standard Epc class for handling very large EPC files without loading all
content into memory at once.
"""

import atexit
from datetime import datetime
import tempfile
import traceback
import numpy as np
import shutil
import logging
import os
import re
import zipfile
from enum import Enum
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterator, Set, Union, Tuple, TypedDict
from weakref import WeakValueDictionary

from energyml.opc.opc import (
    Types,
    Override,
    CoreProperties,
    Relationships,
    Relationship,
)
from energyml.utils.data.datasets_io import (
    FileCacheManager,
    get_handler_registry,
)
from energyml.utils.epc_utils import (
    EXPANDED_EXPORT_FOLDER_PREFIX,
    create_default_core_properties,
    create_default_types,
    create_mandatory_structure_epc,
    extract_uuid_and_version_from_obj_path,
    gen_rels_path_from_obj_path,
    repair_epc_structure_if_not_valid,
)
from energyml.utils.storage_interface import (
    DataArrayMetadata,
    EnergymlStorageInterface,
    ResourceMetadata,
    create_resource_metadata_from_uri,
)
from energyml.utils.uri import Uri, create_uri_from_content_type_or_qualified_type
from energyml.utils.constants import (
    EPCRelsRelationshipType,
    EpcExportVersion,
    MimeType,
    OptimizedRegex,
    file_extension_to_mime_type,
    date_to_datetime,
)
from energyml.utils.epc import (
    gen_energyml_object_path,
    get_epc_content_type_path,
    gen_core_props_path,
)

from energyml.utils.introspection import (
    get_class_from_content_type,
    get_content_type_from_class,
    get_obj_identifier,
    get_obj_title,
    get_obj_uri,
    get_object_attribute_advanced,
    get_direct_dor_list,
    get_obj_type,
    get_obj_usable_class,
    gen_uuid,
)
from energyml.utils.serialization import read_energyml_xml_bytes, serialize_xml

from energyml.utils.xml import is_energyml_content_type


def get_dor_identifiers_from_obj(obj: Any) -> Set[str]:
    """Get identifiers of all Data Object References (DORs) directly referenced by the given object."""
    identifiers = set()
    try:
        dor_list = get_direct_dor_list(obj)
        for dor in dor_list:
            try:
                identifier = get_obj_identifier(dor)
                if identifier:
                    identifiers.add(identifier)
            except Exception as e:
                logging.warning(f"Failed to extract identifier from DOR: {e}")
    except Exception as e:
        logging.warning(f"Failed to get DOR list from object: {e}")
    return identifiers


def get_dor_uris_from_obj(obj: Any) -> Set[Uri]:
    """Get uri of all Data Object References (DORs) directly referenced by the given object."""
    uri_set = set()
    try:
        dor_list = get_direct_dor_list(obj)
        for dor in dor_list:
            try:
                uri = get_obj_uri(dor)
                if uri:
                    uri_set.add(uri)
            except Exception as e:
                logging.warning(f"Failed to extract uri from DOR: {e}")
    except Exception as e:
        logging.warning(f"Failed to get DOR list from object: {e}")
    return uri_set


class RelsUpdateMode(Enum):
    """
    Relationship update modes for EPC file management.

    UPDATE_AT_MODIFICATION: Maintain relationships in real-time as objects are added/removed/modified.
                           This provides the best consistency but may be slower for bulk operations.

    UPDATE_ON_CLOSE: Rebuild all relationships when closing the EPC file.
                    This is more efficient for bulk operations but relationships are only
                    consistent after closing.

    MANUAL: No automatic relationship updates. User must manually call rebuild_all_rels().
           This provides maximum control and performance for advanced use cases.
    """

    UPDATE_AT_MODIFICATION = "update_at_modification"
    UPDATE_ON_CLOSE = "update_on_close"
    MANUAL = "manual"


@dataclass(frozen=True)
class EpcObjectMetadata:
    """Metadata for an object in the EPC file."""

    uri: Uri

    title: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None
    last_changed: Optional[datetime] = None

    def __post_init__(self):
        if not self.uri.is_object_uri():
            raise ValueError(f"URI must be an object URI: {self.uri}")

    @property
    def uuid(self) -> str:
        return self.uri.uuid  # type: ignore Guaranteed to be non-None for object URIs due to __post_init__ validation

    @property
    def object_type(self) -> str:
        return self.uri.object_type  # type: ignore Guaranteed to be non-None for object URIs due to __post_init__ validation

    @property
    def content_type(self) -> str:
        return self.uri.get_content_type()

    @property
    def qualified_type(self) -> str:
        return self.uri.get_qualified_type()

    @property
    def version(self) -> Optional[str]:
        return self.uri.version

    @property
    def identifier(self) -> str:
        return self.uri.as_identifier()

    def file_path(self, export_version: EpcExportVersion) -> str:
        return gen_energyml_object_path(self.uri, export_version=export_version)

    def rels_path(self, export_version: EpcExportVersion) -> str:
        return gen_rels_path_from_obj_path(self.file_path(export_version=export_version))

    def __str__(self):
        return str(self.uri)

    def to_resource_metadata(self) -> ResourceMetadata:
        return create_resource_metadata_from_uri(
            self.uri, title=self.title, custom_data=self.custom_data, last_changed=self.last_changed
        )


@dataclass
class EpcStreamingStats:
    """Statistics for EPC streaming operations."""

    total_objects: int = 0
    loaded_objects: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    bytes_read: int = 0

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate percentage."""
        total_requests = self.cache_hits + self.cache_misses
        return (self.cache_hits / total_requests * 100) if total_requests > 0 else 0.0

    @property
    def memory_efficiency(self) -> float:
        """Calculate memory efficiency percentage."""
        return (1 - (self.loaded_objects / self.total_objects)) * 100 if self.total_objects > 0 else 100.0


# ===========================================================================================
# PARALLEL PROCESSING WORKER FUNCTIONS
# ===========================================================================================

# Configuration constants for parallel processing
_MIN_OBJECTS_PER_WORKER = 10  # Minimum objects to justify spawning a worker
_WORKER_POOL_SIZE_RATIO = 10  # Number of objects per worker process


class _WorkerResult(TypedDict):
    """Type definition for parallel worker function return value."""

    identifier: str
    file_path: str
    object_type: str
    referenced_objects: List[Tuple[str, str]]  # List of (target_identifier, target_type)


def process_object_for_rels_worker(
    args: Tuple[str, str, Dict[str, EpcObjectMetadata]], export_version: EpcExportVersion
) -> Optional[_WorkerResult]:
    """
    Worker function for parallel relationship processing (runs in separate process).

    This function is executed in a separate process to compute DESTINATION relationships
    for a single object. It bypasses Python's GIL for CPU-intensive XML parsing.

    Performance characteristics:
    - Each worker process opens its own ZIP file handle
    - XML parsing happens independently on separate CPU cores
    - Results are serialized back to the main process via pickle

    Args:
        args: Tuple containing:
            - identifier: Object UUID/identifier to process
            - epc_file_path: Absolute path to the EPC file
            - metadata_dict: Dictionary of all object metadata (for validation)
        export_version: Version of EPC export format to use

    Returns:
        Dictionary conforming to _WorkerResult TypedDict with the following keys:
            - 'identifier': The identifier of the processed object
            - 'file_path': The file path of the object within the EPC archive
            - 'object_type': The type of the object (e.g., 'BoundaryFeature', 'TriangulatedSetRepresentation')
            - 'referenced_objects': List of tuples (target_identifier, target_type) for all
              Data Object References (DORs) found in this object that exist in the EPC
        Returns None if processing fails (e.g., object not found, parsing error).
    """
    identifier, epc_file_path, metadata_dict = args

    try:
        # Open ZIP file in this worker process
        metadata = metadata_dict.get(identifier)
        if not metadata:
            return None

        # Load object from ZIP
        with zipfile.ZipFile(epc_file_path, "r") as zf:
            obj_data = zf.read(metadata.file_path(export_version=export_version))
            obj_class = get_class_from_content_type(metadata.content_type)
            obj = read_energyml_xml_bytes(obj_data, obj_class)

        # Extract this object's type from metadata (no need to parse object)
        obj_type = metadata.object_type

        # Get all DOR URIs - URIs contain all necessary info (type, uuid, version)
        dor_uris = get_dor_uris_from_obj(obj)

        # Build list of (target_identifier, target_type) tuples from URIs
        referenced_objects = []
        for uri in dor_uris:
            try:
                target_identifier = uri.as_identifier()
                # Only include if target exists in metadata
                if target_identifier and target_identifier in metadata_dict:
                    # Extract type directly from URI (no need to load target object)
                    target_type = uri.object_type
                    if target_type:
                        referenced_objects.append((target_identifier, target_type))
            except Exception as e:
                # Don't fail entire object for one bad DOR
                logging.debug(f"Skipping invalid DOR URI in {identifier}: {e}")

        return {
            "identifier": identifier,
            "file_path": metadata.file_path(export_version=export_version),
            "object_type": obj_type,
            "referenced_objects": referenced_objects,
        }

    except Exception as e:
        logging.warning(f"Worker failed to process {identifier}: {e}")
        return None


# ===========================================================================================
# HELPER CLASSES FOR REFACTORED ARCHITECTURE
# ===========================================================================================


class _ZipFileAccessor:
    """
    Internal helper class for managing ZIP file access with proper resource management.

    This class handles:
    - Persistent ZIP connections when keep_open=True
    - On-demand connections when keep_open=False
    - Proper cleanup and resource management
    - Connection pooling for better performance
    """

    def __init__(self, epc_file_path: Path, keep_open: bool = False):
        """
        Initialize the ZIP file accessor.

        Args:
            epc_file_path: Path to the EPC file
            keep_open: If True, maintains a persistent connection
        """
        self.epc_file_path = epc_file_path
        self.keep_open = keep_open
        self._persistent_zip: Optional[zipfile.ZipFile] = None

    def open_persistent_connection(self) -> None:
        """Open a persistent ZIP connection if keep_open is enabled."""
        if self.keep_open and self._persistent_zip is None:
            self._persistent_zip = zipfile.ZipFile(self.epc_file_path, "r")

    @contextmanager
    def get_zip_file(self) -> Iterator[zipfile.ZipFile]:
        """
        Context manager for ZIP file access with proper resource management.

        If keep_open is True, uses the persistent connection. Otherwise opens a new one.
        """
        if self.keep_open and self._persistent_zip is not None:
            # Use persistent connection, don't close it
            yield self._persistent_zip
        else:
            # Open and close per request
            zf = None
            try:
                zf = zipfile.ZipFile(self.epc_file_path, "r")
                yield zf
            finally:
                if zf is not None:
                    zf.close()

    def reopen_persistent_zip(self) -> None:
        """Reopen persistent ZIP file after modifications to reflect changes."""
        if self.keep_open and self._persistent_zip is not None:
            try:
                self._persistent_zip.close()
            except Exception:
                pass
            self._persistent_zip = zipfile.ZipFile(self.epc_file_path, "r")

    def close(self) -> None:
        """Close the persistent ZIP file if it's open."""
        if self._persistent_zip is not None:
            try:
                self._persistent_zip.close()
            except Exception as e:
                logging.debug(f"Error closing persistent ZIP file: {e}")
            finally:
                self._persistent_zip = None

    def __del__(self):
        """Ensure the persistent ZIP file is closed when the accessor is garbage collected."""
        try:
            self.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class _MetadataManager:
    """
    Internal helper class for managing object metadata, indexing, and queries.

    This class handles:
    - Loading metadata from [Content_Types].xml
    - Maintaining UUID and type indexes
    - Fast metadata queries without loading objects
    - Version detection
    """

    def __init__(self, zip_accessor: _ZipFileAccessor, stats: EpcStreamingStats):
        """
        Initialize the metadata manager.

        Args:
            zip_accessor: ZIP file accessor for reading from EPC
            stats: Statistics tracker
        """
        self.zip_accessor = zip_accessor
        self.stats = stats

        # Object metadata storage
        self._metadata: Dict[str, EpcObjectMetadata] = {}  # identifier -> metadata
        self._uuid_index: Dict[str, List[str]] = {}  # uuid -> list of identifiers
        self._core_props: Optional[CoreProperties] = None
        self._export_version = EpcExportVersion.CLASSIC  # Store export version, default set to CLASSIC

    def set_export_version(self, version: EpcExportVersion) -> None:
        """Set the export version."""
        self._export_version = version

    def load_metadata(self, detect_export_version: bool = True) -> None:
        """Load object metadata from [Content_Types].xml without loading actual objects."""
        try:
            with self.zip_accessor.get_zip_file() as zf:
                # Read content types
                content_types = self._read_content_types(zf)

                # Process each override entry
                for override in content_types.override:
                    if override.content_type and override.part_name:
                        if is_energyml_content_type(override.content_type):
                            self._process_energyml_object_metadata(zf, override)
                        elif self._is_core_properties(override.content_type):
                            self._process_core_properties_metadata(override)
                        else:
                            logging.debug(
                                f"Epc_StreamReader @load_metadata Skipping non-EnergyML content type: {override.content_type}"
                            )

                        # checking export version
                        if (
                            detect_export_version
                            and self._export_version == EpcExportVersion.CLASSIC
                            and override.part_name.startswith(
                                (EXPANDED_EXPORT_FOLDER_PREFIX, f"/{EXPANDED_EXPORT_FOLDER_PREFIX}")
                            )
                        ):
                            logging.debug(f"Detected EXPANDED EPC version based on path: {override.part_name}")
                            self._export_version = EpcExportVersion.EXPANDED

                self.stats.total_objects = len(self._metadata)

        except Exception as e:
            logging.error(f"Failed to load metadata from EPC file: {e}")
            raise

    def get_metadata(self, identifier: str) -> Optional[EpcObjectMetadata]:
        """Get metadata for an object by identifier."""
        return self._metadata.get(identifier)

    def get_uuid_identifiers(self, uuid: str) -> List[str]:
        """Get all identifiers for objects with the given UUID.
        Note: Multiple objects can share the same UUID if there are multiple versions of the same object in the EPC file.
        """
        return self._uuid_index.get(uuid, [])

    def get_by_qualified_type(self, qualified_type: str) -> List[str]:
        """Get all identifiers for objects of the given qualified type."""
        return [m.identifier for m in self._metadata.values() if m.qualified_type == qualified_type]

    def list_metadata(self, qualified_type_filter: Optional[str] = None) -> List[EpcObjectMetadata]:
        """List metadata for all objects, optionally filtered by type."""
        if qualified_type_filter is None:
            return list(self._metadata.values())
        return [
            self._metadata[identifier]
            for identifier in self._metadata
            if self._metadata[identifier].qualified_type == qualified_type_filter
        ]

    def add_metadata(self, metadata: EpcObjectMetadata) -> None:
        """Add metadata for a new object."""
        identifier = metadata.identifier
        if identifier:
            self._metadata[identifier] = metadata

            # Update UUID index
            if metadata.uuid not in self._uuid_index:
                self._uuid_index[metadata.uuid] = []
            if identifier not in self._uuid_index[metadata.uuid]:
                self._uuid_index[metadata.uuid].append(identifier)

            self.stats.total_objects += 1

    def remove_metadata(self, identifier: Union[str, EpcObjectMetadata]) -> Optional[EpcObjectMetadata]:
        """Remove metadata for an object. Returns the removed metadata."""
        if isinstance(identifier, EpcObjectMetadata):
            identifier = identifier.identifier
        metadata = self._metadata.pop(identifier, None)
        if metadata:
            # Update UUID index
            if metadata.uuid in self._uuid_index:
                self._uuid_index[metadata.uuid].remove(identifier)
                if not self._uuid_index[metadata.uuid]:
                    del self._uuid_index[metadata.uuid]

            self.stats.total_objects -= 1

        return metadata

    def contains(self, identifier: str) -> bool:
        """Check if an object with the given identifier exists."""
        return identifier in self._metadata

    def gen_rels_path_from_metadata(self, metadata: EpcObjectMetadata) -> str:
        """Generate rels path from object metadata without loading the object."""
        if not isinstance(metadata, EpcObjectMetadata):
            raise ValueError("Metadata must be an instance of EpcObjectMetadata")
        return metadata.rels_path(export_version=self._export_version)

    def gen_rels_path_from_identifier(self, identifier: str) -> Optional[str]:
        """Generate rels path from object identifier without loading the object."""
        if not isinstance(identifier, str):
            raise ValueError("Identifier must be a string")
        metadata = self._metadata.get(identifier)
        if metadata is None:
            return None
        return self.gen_rels_path_from_metadata(metadata)

    def get_core_properties(self) -> Optional[CoreProperties]:
        """Get core properties (loaded lazily)."""
        if self._core_props is None and self._core_props_path:
            try:
                with self.zip_accessor.get_zip_file() as zf:
                    core_data = zf.read(self._core_props_path)
                    self.stats.bytes_read += len(core_data)
                    self._core_props = read_energyml_xml_bytes(core_data, CoreProperties)
            except Exception as e:
                logging.error(f"Failed to load core properties, creating a default one: {e}")
                self._core_props = create_default_core_properties()

        return self._core_props

    def detect_epc_version(self) -> EpcExportVersion:
        """Detect EPC packaging version based on file structure."""
        try:
            with self.zip_accessor.get_zip_file() as zf:
                file_list = zf.namelist()

                # Look for patterns that indicate EXPANDED version
                for file_path in file_list:
                    # Skip metadata files
                    if (
                        file_path.startswith("[Content_Types]")
                        or file_path.startswith("_rels/")
                        or file_path.endswith(".rels")
                    ):
                        continue

                    # Check for namespace_ prefix pattern
                    if file_path.startswith("namespace_"):
                        path_parts = file_path.split("/")
                        if len(path_parts) >= 2:
                            logging.info(f"Detected EXPANDED EPC version based on path: {file_path}")
                            return EpcExportVersion.EXPANDED

                # If no EXPANDED patterns found, assume CLASSIC
                logging.info("Detected CLASSIC EPC version")
                return EpcExportVersion.CLASSIC

        except Exception as e:
            logging.warning(f"Failed to detect EPC version, defaulting to CLASSIC: {e}")
            return EpcExportVersion.CLASSIC

    # def update_content_types_xml(
    #     self, source_zip: zipfile.ZipFile, metadata: EpcObjectMetadata, add: bool = True
    # ) -> str:
    #     """Update [Content_Types].xml to add or remove object entry.

    #     Args:
    #         source_zip: Open ZIP file to read from
    #         metadata: Object metadata
    #         add: If True, add entry; if False, remove entry

    #     Returns:
    #         Updated [Content_Types].xml as string
    #     """
    #     # Read existing content types
    #     content_types = self._read_content_types(source_zip)

    #     if add:
    #         # Add new override entry
    #         new_override = Override()
    #         new_override.part_name = f"/{metadata.file_path}"
    #         new_override.content_type = metadata.content_type
    #         content_types.override.append(new_override)
    #     else:
    #         # Remove existing override entry
    #         content_types.override = [
    #             o for o in content_types.override if o.part_name and o.part_name.lstrip("/") != metadata.file_path
    #         ]

    #     # Serialize back to XML
    #     return serialize_xml(content_types)

    def get_content_type(self, zf: zipfile.ZipFile) -> Types:

        meta_dict_key_path = {
            m.file_path(export_version=self._export_version): m.content_type for m in self._metadata.values()
        }
        other_files_in_epc = set()
        for name in zf.namelist():
            if (
                name not in meta_dict_key_path
                and not name.endswith("rels")
                and not name == get_epc_content_type_path()
                and not name == gen_core_props_path()
            ):
                other_files_in_epc.add(name)

        content_types = create_default_types()

        # creating overrides
        for file_path, content_type in meta_dict_key_path.items():
            override = Override(content_type=content_type, part_name=f"/{file_path}")
            content_types.override.append(override)

        # Add overrides for other files in EPC that are not in metadata (to preserve them)
        for file_path in other_files_in_epc:
            file_extension = os.path.splitext(file_path)[1].lstrip(".").lower()
            mime_type = file_extension_to_mime_type(file_extension)
            if mime_type:
                override = Override(content_type=mime_type, part_name=f"/{file_path}")
                content_types.override.append(override)

        return content_types

    #     ____  ____  _____    _____  ____________   __  _________________  ______  ____  _____
    #    / __ \/ __ \/  _/ |  / /   |/_  __/ ____/  /  |/  / ____/_  __/ / / / __ \/ __ \/ ___/
    #   / /_/ / /_/ // / | | / / /| | / / / __/    / /|_/ / __/   / / / /_/ / / / / / / /\__ \
    #  / ____/ _, _// /  | |/ / ___ |/ / / /___   / /  / / /___  / / / __  / /_/ / /_/ /___/ /
    # /_/   /_/ |_/___/  |___/_/  |_/_/ /_____/  /_/  /_/_____/ /_/ /_/ /_/\____/_____//____/

    def _read_content_types(self, zf: zipfile.ZipFile) -> Types:
        """Read and parse [Content_Types].xml file."""
        content_types_path = get_epc_content_type_path()

        try:
            content_data = zf.read(content_types_path)
            self.stats.bytes_read += len(content_data)
            return read_energyml_xml_bytes(content_data, Types)
        except KeyError:
            # Try case-insensitive search
            for name in zf.namelist():
                if name.lower() == content_types_path.lower():
                    content_data = zf.read(name)
                    self.stats.bytes_read += len(content_data)
                    return read_energyml_xml_bytes(content_data, Types)
            raise FileNotFoundError(f"No {content_types_path} found in EPC file")

    def _process_energyml_object_metadata(self, zf: zipfile.ZipFile, override: Override) -> None:
        """Process metadata for an EnergyML object without loading it."""
        if not override.part_name or not override.content_type:
            return

        file_path = override.part_name.lstrip("/")
        content_type = override.content_type

        try:
            # First try to extract UUID and version from file path (works for EXPANDED mode)
            uuid, version = extract_uuid_and_version_from_obj_path(file_path)

            # For CLASSIC mode, version is not in the path, so we need to extract it from XML content
            if uuid and version is None:
                try:
                    # Read first chunk of XML to extract version without full parsing
                    with zf.open(file_path) as f:
                        chunk = f.read(2048)  # 2KB should be enough for root element
                        self.stats.bytes_read += len(chunk)
                        chunk_str = chunk.decode("utf-8", errors="ignore")

                        # Extract version if present
                        version_patterns = [
                            r'object[Vv]ersion["\']?\s*[:=]\s*["\']([^"\']+)',
                        ]

                        for pattern in version_patterns:
                            version_match = re.search(pattern, chunk_str)
                            if version_match:
                                version = version_match.group(1)
                                if not isinstance(version, str):
                                    version = str(version)
                                break
                except Exception as e:
                    logging.debug(f"Failed to extract version from XML content for {file_path}: {e}")

            if uuid:  # Only process if we successfully extracted UUID
                uri = create_uri_from_content_type_or_qualified_type(ct_or_qt=content_type, uuid=uuid, version=version)
                metadata = EpcObjectMetadata(uri=uri)

                # Store in indexes
                identifier = metadata.identifier
                if identifier:
                    self._metadata[identifier] = metadata

                    # Update UUID index
                    if uuid not in self._uuid_index:
                        self._uuid_index[uuid] = []
                    self._uuid_index[uuid].append(identifier)

        except Exception as e:
            traceback.print_exc()
            logging.warning(f"Failed to process metadata for {file_path}: {e}")

    def _is_core_properties(self, content_type: str) -> bool:
        """Check if content type is CoreProperties."""
        return content_type == MimeType.CORE_PROPERTIES.value

    def _process_core_properties_metadata(self, override: Override) -> None:
        """Process core properties metadata."""
        if override.part_name:
            self._core_props_path = override.part_name.lstrip("/")

    def __len__(self) -> int:
        """Return total number of objects."""
        return len(self._metadata)

    def __iter__(self) -> Iterator[str]:
        """Iterate over object identifiers."""
        return iter(self._metadata.keys())


class _RelationshipManager:
    """
    Internal helper class for managing relationships between objects.

    This class handles:
    - Reading relationships from .rels files
    - Writing relationship updates
    - Supporting 3 update modes (UPDATE_AT_MODIFICATION, UPDATE_ON_CLOSE, MANUAL)
    - Preserving EXTERNAL_RESOURCE relationships
    - Rebuilding all relationships
    """

    def __init__(
        self,
        zip_accessor: _ZipFileAccessor,
        metadata_manager: _MetadataManager,
        stats: EpcStreamingStats,
        rels_update_mode: RelsUpdateMode,
    ):
        """
        Initialize the relationship manager.

        Args:
            zip_accessor: ZIP file accessor for reading/writing
            metadata_manager: Metadata manager for object lookups
            stats: Statistics tracker
            rels_update_mode: Relationship update mode
        """
        self.zip_accessor = zip_accessor
        self.metadata_manager = metadata_manager
        self.stats = stats
        self.rels_update_mode = rels_update_mode

        # Additional rels management (for user-added relationships)
        self.additional_rels: Dict[str, List[Relationship]] = {}

    def get_obj_rels(self, obj_identifier: Optional[str] = None, rels_path: Optional[str] = None) -> List[Relationship]:
        """
        Get all relationships for a given object.
        Merges relationships from the EPC file with in-memory additional relationships.
        """
        rels = []

        # Read rels from EPC file
        if rels_path is None and obj_identifier is not None:
            rels_path = self.metadata_manager.gen_rels_path_from_identifier(obj_identifier)

        if rels_path is not None:
            with self.zip_accessor.get_zip_file() as zf:
                try:
                    rels_data = zf.read(rels_path)
                    self.stats.bytes_read += len(rels_data)
                    relationships = read_energyml_xml_bytes(rels_data, Relationships)
                    rels.extend(relationships.relationship)
                except KeyError:
                    # No rels file found for this object
                    pass

        # Merge with in-memory additional relationships
        if obj_identifier is not None and obj_identifier in self.additional_rels:
            rels = self.merge_rels(rels, self.additional_rels[obj_identifier])

        return rels

    def update_rels_for_new_object(self, obj: Any, obj_identifier: str) -> None:
        """Update relationships when a new object is added (UPDATE_AT_MODIFICATION mode)."""
        metadata = self.metadata_manager.get_metadata(obj_identifier)
        if not metadata:
            logging.warning(f"Metadata not found for {obj_identifier}")
            return

        # Get all objects this new object references
        dest_target_uris = get_dor_uris_from_obj(obj)
        # logging.debug(f"Updating relationships for new object {obj_identifier}, found DOR targets: {dest_target_uris}")

        obj_file_path = metadata.file_path(export_version=self.metadata_manager._export_version)

        dest_rels = []
        source_relationships = {}
        for target_uri in dest_target_uris:
            target_path = gen_energyml_object_path(target_uri, export_version=self.metadata_manager._export_version)

            dest_rel = Relationship(
                target=target_path,
                type_value=str(EPCRelsRelationshipType.DESTINATION_OBJECT),
                id=f"_{gen_uuid()}",
            )
            dest_rels.append(dest_rel)

            source_relationships[target_path] = Relationship(
                target=obj_file_path,
                type_value=str(EPCRelsRelationshipType.SOURCE_OBJECT),
                id=f"_{gen_uuid()}",
            )

        # Write updates
        self._write_rels_updates(
            current_object_id=obj_identifier,
            current_rels_additions=dest_rels,
            target_path_rels_additions=source_relationships,
        )

    def update_rels_for_modified_object(self, obj: Any, obj_identifier: str) -> None:
        """Update relationships when an object is modified (UPDATE_AT_MODIFICATION mode)."""
        metadata = self.metadata_manager.get_metadata(obj_identifier)
        if not metadata:
            logging.warning(f"Metadata not found for {obj_identifier}")
            return

        obj_path = metadata.file_path(export_version=self.metadata_manager._export_version)

        previous_dest_rels_target_path = {
            r.target
            for r in self.get_obj_rels(obj_identifier)
            if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT) and r.target is not None
        }
        # Latest DORs from the modified object
        dest_target_uris = get_dor_uris_from_obj(obj)
        # logging.debug(f"Updating relationships for new object {obj_identifier}, found DOR targets: {dest_target_uris}")

        # Build new SOURCE relationships
        current_rels_additions: List[Relationship] = []
        reversed_source_relationships: Dict[str, Relationship] = {}

        # Create relationships for all new DORs
        for target_uri in dest_target_uris:
            target_path = gen_energyml_object_path(target_uri, export_version=self.metadata_manager._export_version)

            # DESTINATION relationship : current is referenced by
            dest_rel = Relationship(
                target=target_path,
                type_value=str(EPCRelsRelationshipType.DESTINATION_OBJECT),
                id=f"_{gen_uuid()}",
            )
            current_rels_additions.append(dest_rel)

            if target_path not in previous_dest_rels_target_path:
                # REVERSED SOURCE relationship : target references current, if not already existing (to avoid duplicates if DORs are not changed for this target)
                source_rel = Relationship(
                    target=obj_path,
                    type_value=str(EPCRelsRelationshipType.SOURCE_OBJECT),
                    id=f"_{gen_uuid()}",
                )
                reversed_source_relationships[target_path] = source_rel

        # list previous dest that does not exist anymore in the modified object, to remove the corresponding reversed source relationship on target side
        outdated_dors_targets_paths = previous_dest_rels_target_path - reversed_source_relationships.keys()

        # Write updates
        self._write_rels_updates(
            current_object_id=obj_identifier,
            current_rels_additions=list(current_rels_additions),
            target_path_rels_additions=reversed_source_relationships,
            target_path_rels_removals=outdated_dors_targets_paths,
        )

    def update_rels_for_removed_object(self, obj_identifier: str) -> None:
        """Update relationships when an object is removed (UPDATE_AT_MODIFICATION mode)."""
        current_rels = self.get_obj_rels(obj_identifier)  # Ensure we have the latest relationships loaded

        dest_rels = [r for r in current_rels if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()]

        # Write updates
        self._write_rels_updates(
            current_object_id=obj_identifier,
            target_path_rels_removals=[
                r.target
                for r in current_rels
                if r.target is not None and r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()
            ],
            delete_current_obj_rels_file_and_file=len(dest_rels)
            == len(
                current_rels
            ),  # If all relationships are DESTINATION_OBJECT, we can delete the .rels file entirely. If some source rels exists, we keep it to ease potential add of this element later, to avoid parsing all reals to find its sources rels from other object DEST rels
        )

    # def compute_object_rels(self, obj: Any, obj_identifier: str) -> List[Relationship]:
    #     """
    #     Compute relationships for a given object (SOURCE relationships).
    #     This object references other objects through DORs.

    #     Args:
    #         obj: The EnergyML object
    #         obj_identifier: The identifier of the object

    #     Returns:
    #         List of Relationship objects for this object's .rels file
    #     """
    #     rels = []

    #     # Get all DORs (Data Object References) in this object
    #     direct_dors = get_direct_dor_list(obj)

    #     for dor in direct_dors:
    #         try:
    #             target_identifier = get_obj_identifier(dor)

    #             # Get target file path from metadata without processing DOR
    #             # The relationship target should be the object's file path, not its rels path
    #             if self.metadata_manager.contains(target_identifier):
    #                 target_metadata = self.metadata_manager.get_metadata(target_identifier)
    #                 if target_metadata:
    #                     target_path = target_metadata.file_path
    #                 else:
    #                     target_path = gen_energyml_object_path(dor, self._metadata_mgr._export_version)
    #             else:
    #                 # Fall back to generating path from DOR if metadata not found
    #                 target_path = gen_energyml_object_path(dor, self._metadata_mgr._export_version)

    #             # Create SOURCE relationship (this object -> target object)
    #             rel = Relationship(
    #                 target=target_path,
    #                 type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
    #                 id=f"_{obj_identifier}_{get_obj_type(get_obj_usable_class(dor))}_{target_identifier}",
    #             )
    #             rels.append(rel)
    #         except Exception as e:
    #             logging.warning(f"Failed to create relationship for DOR in {obj_identifier}: {e}")

    #     return rels

    def merge_rels(self, new_rels: List[Relationship], existing_rels: List[Relationship]) -> List[Relationship]:
        """Merge new relationships with existing ones, avoiding duplicates and ensuring unique IDs.

        Args:
            new_rels: New relationships to add
            existing_rels: Existing relationships

        Returns:
            Merged list of relationships
        """
        merged = list(existing_rels)

        for new_rel in new_rels:
            # Check if relationship already exists
            rel_exists = any(r.target == new_rel.target and r.type_value == new_rel.type_value for r in merged)

            if not rel_exists:
                # Ensure unique ID
                cpt = 0
                new_rel_id = new_rel.id
                while any(r.id == new_rel_id for r in merged):
                    new_rel_id = f"{new_rel.id}_{cpt}"
                    cpt += 1
                if new_rel_id != new_rel.id:
                    new_rel.id = new_rel_id

                merged.append(new_rel)

        return merged

    def _write_rels_updates(
        self,
        current_object_id: str,
        current_rels_additions: Optional[List[Relationship]] = None,
        current_rels_removals: Optional[Union[List[str], Set[str]]] = None,
        target_path_rels_additions: Optional[Dict[str, Relationship]] = None,
        target_path_rels_removals: Optional[Union[List[str], Set[str]]] = None,
        delete_current_obj_rels_file_and_file: bool = False,
    ) -> None:
        """Write relationship updates to the EPC file efficiently.

        Args:
            current_object_id: Identifier of the object being modified/added/removed
            current_rels_additions: List of Relationship objects to add to the current object's .rels file
            current_rels_removals: List or set of relationship ID patterns to remove from the current object's .rels file
            target_path_rels_additions: Dict mapping target object file paths (not the .rels path) to Relationship objects to add to their .rels files (for SOURCE relationships)
            target_path_rels_removals: List or set of relationship ID patterns to remove from target objects' .rels files (for SOURCE relationships)
            delete_current_obj_rels_file_and_file: If True, deletes the current object's .rels file entirely (if contains only DEST relations) and the object file iteself


        """
        # Implementation of this method would involve:
        # - Reading existing .rels files for current and target objects
        # - Merging additions and removals while preserving EXTERNAL_RESOURCE relationships
        # - Writing back updated .rels files to the ZIP (either by modifying in place or rebuilding)
        # - Handling different update modes (immediate vs on close)

        # 1st : debug log the inputs
        # logging.debug(
        #     f"Writing rels updates for current_object_id={current_object_id}, current_rels_additions={current_rels_additions}, current_rels_removals={current_rels_removals}, target_path_rels_additions={target_path_rels_additions}, target_path_rels_removals={target_path_rels_removals}, delete_current_obj_rels_file_and_file={delete_current_obj_rels_file_and_file}\n\n"
        # )

        current_obj_meta = self.metadata_manager.get_metadata(current_object_id)
        if not current_obj_meta:
            logging.warning(f"Metadata not found for {current_object_id}, cannot write rels updates")
            return
        current_object_path = current_obj_meta.file_path(export_version=self.metadata_manager._export_version)
        current_rels_path = self.metadata_manager.gen_rels_path_from_metadata(current_obj_meta)

        current_obj_actual_rels = self.get_obj_rels(current_object_id, rels_path=current_rels_path)

        current_updated_rels = (
            self.merge_rels(current_rels_additions, current_obj_actual_rels)
            if current_rels_additions
            else current_obj_actual_rels
        )
        if current_rels_removals:
            for removal_obj_id in current_rels_removals:
                target_metadata = self.metadata_manager.get_metadata(removal_obj_id)
                target_path = (
                    target_metadata.file_path(export_version=self.metadata_manager._export_version)
                    if target_metadata
                    else None
                )
                if target_path:
                    current_updated_rels = [
                        r for r in current_updated_rels if r.target is not None and (target_path not in r.target)
                    ]

        # Now handle target objects' .rels updates
        targets_new_rels_to_path: Dict[str, List[Relationship]] = {}
        # First, get existing rels for all target objects
        if target_path_rels_additions or target_path_rels_removals:
            target_ids = set()
            if target_path_rels_additions:
                target_ids.update(target_path_rels_additions.keys())
            if target_path_rels_removals:
                target_ids.update(target_path_rels_removals)

            for target_id in target_ids:
                # we authorize to pass a rels path directly as target_id in target_rels_additions for more flexibility, but if it's not the case we try to find target metadata and generate rels path from it
                target_rels_path = None
                if target_id.endswith(".xml"):
                    target_rels_path = gen_rels_path_from_obj_path(target_id)
                elif target_id.endswith(".rels"):
                    target_rels_path = target_id
                else:
                    target_meta = self.metadata_manager.get_metadata(target_id)
                    if not target_meta:
                        logging.warning(
                            f"Metadata not found for target {target_id}, skipping rels updates for this target"
                        )
                        continue
                    target_rels_path = self.metadata_manager.gen_rels_path_from_metadata(target_meta)
                existing_target_rels = self.get_obj_rels(rels_path=target_rels_path)

                # Merge additions and removals for this target
                updated_target_rels = existing_target_rels
                if target_path_rels_additions and target_id in target_path_rels_additions:
                    updated_target_rels = self.merge_rels([target_path_rels_additions[target_id]], updated_target_rels)
                if target_path_rels_removals and target_id in target_path_rels_removals:
                    # TODO: maybe we should be able to support non energyml objects and take target path to remove in a tuple in target_rels_removals instead of target_id only ?
                    updated_target_rels = [r for r in updated_target_rels if r.target != current_object_path]

                targets_new_rels_to_path[target_rels_path] = updated_target_rels

        files_to_delete = []
        if delete_current_obj_rels_file_and_file:
            files_to_delete.append(current_object_path)
            if (
                len(
                    [r for r in current_updated_rels if r.type_value != str(EPCRelsRelationshipType.DESTINATION_OBJECT)]
                )
                == 0
            ):
                # if current object must be removed and its rels file had only dest relationship. We can delete the rels file as well.
                files_to_delete.append(current_rels_path)

        rels_updates = {}
        if current_rels_additions is not None or current_rels_removals is not None:
            rels_updates = {current_rels_path: serialize_xml(Relationships(relationship=current_updated_rels))}
        for target_rels_path, updated_rels in targets_new_rels_to_path.items():
            rels_updates[target_rels_path] = serialize_xml(Relationships(relationship=updated_rels))

        files_to_skip = set(files_to_delete).union(set(rels_updates.keys()))

        # logging.debug(
        #     f"====\nFiles to delete: {files_to_delete}, rels updates to write: {list(rels_updates.keys())}, files to skip in copy: {files_to_skip}\n\n"
        # )

        # Write in tmp file and then replace original to minimize I/O and handle multiple updates in one operation
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name
        try:
            with self.zip_accessor.get_zip_file() as source_zf:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zf:
                    # Copy all files except those to delete or update
                    ct_xml = None

                    for item in source_zf.infolist():
                        if get_epc_content_type_path() in item.filename:
                            ct_xml = source_zf.read(item.filename)
                        elif item.filename not in files_to_skip and item.filename not in rels_updates:
                            data = source_zf.read(item.filename)
                            target_zf.writestr(item, data)

                    # Write updated rels files
                    for rels_path, rels_xml in rels_updates.items():
                        target_zf.writestr(rels_path, rels_xml)
                        # logging.debug(f"Wrote updated rels file: {rels_path} -> {rels_xml}")

                    if delete_current_obj_rels_file_and_file:
                        ct_object: Optional[Types] = None
                        if ct_xml is not None:
                            # remove the object entry from [Content_Types].xml if the object file is deleted
                            ct_object = read_energyml_xml_bytes(ct_xml, Types)
                            if ct_object is not None:
                                ct_object.override = [
                                    o for o in ct_object.override if current_object_path not in (o.part_name or "")
                                ]

                        if ct_object is None:
                            ct_object = self.metadata_manager.get_content_type(target_zf)
                        ct_xml = serialize_xml(ct_object)

                    if ct_xml is None:
                        ct_xml = serialize_xml(self.metadata_manager.get_content_type(target_zf))

                    target_zf.writestr(get_epc_content_type_path(), ct_xml)

            # Replace original
            shutil.move(temp_path, self.zip_accessor.epc_file_path)
            self.zip_accessor.reopen_persistent_zip()

        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            logging.error(f"Failed to write rels updates: {e}")
            raise


# ===========================================================================================
# MAIN CLASS (REFACTORED TO USE HELPER CLASSES)
# ===========================================================================================


class EpcStreamReader(EnergymlStorageInterface):

    def __init__(
        self,
        epc_file_path: Union[str, Path],
        rels_update_mode: RelsUpdateMode = RelsUpdateMode.UPDATE_ON_CLOSE,
        force_h5_path: Optional[str] = None,
        export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
        enable_parallel_rels: bool = False,
        parallel_worker_ratio: int = 10,
        cache_size: int = 100,
        # preload_metadata: bool = True,
        keep_open: bool = True,
        force_title_load: bool = False,
    ):
        # Public attributes
        self.epc_file_path = Path(epc_file_path)
        self.enable_parallel_rels = enable_parallel_rels
        self.parallel_worker_ratio = parallel_worker_ratio
        self.cache_size = cache_size
        self.force_h5_path = force_h5_path
        self.cache_opened_h5 = None
        self.keep_open = keep_open
        self.force_title_load = force_title_load
        # Note: rels_update_mode will be set on _rels_mgr when it's created below
        # self.export_version: EpcExportVersion = export_version or EpcExportVersion.CLASSIC
        self.stats = EpcStreamingStats()

        # Caching system using weak references
        self._object_cache: WeakValueDictionary = WeakValueDictionary()
        self._access_order: List[str] = []  # LRU tracking

        is_new_file = False
        # =====================================
        # Validate file exists and is readable
        # =====================================
        if not self.epc_file_path.exists():
            logging.info(f"EPC file not found: {self.epc_file_path}. Creating a new empty EPC file.")
            create_mandatory_structure_epc(self.epc_file_path)
            is_new_file = True

        if not zipfile.is_zipfile(self.epc_file_path):
            raise ValueError(f"File is not a valid ZIP/EPC file: {self.epc_file_path}")

        # validate mandatory files and structure, and auto-repair if enabled

        repair_epc_structure_if_not_valid(self.epc_file_path)

        self._zip_accessor = _ZipFileAccessor(self.epc_file_path, keep_open=keep_open)
        if keep_open and not is_new_file:
            self._zip_accessor.open_persistent_connection()

        # =====================================

        self._metadata_mgr = _MetadataManager(self._zip_accessor, self.stats)
        self._metadata_mgr.load_metadata()  # Load metadata at initialization (can be optimized to lazy load if needed) => export version may be auto-detected
        if is_new_file:
            self._metadata_mgr.set_export_version(export_version)
        self._rels_mgr = _RelationshipManager(self._zip_accessor, self._metadata_mgr, self.stats, rels_update_mode)

        # Initialize file cache manager for external array files (HDF5, Parquet, CSV, etc.)
        self._file_cache = FileCacheManager(max_open_files=3)
        self._handler_registry = get_handler_registry()

        # Register atexit handler to ensure cleanup on program shutdown
        self._atexit_registered = True
        atexit.register(self._atexit_close)

    # ================================
    # Properties
    # ================================

    @property
    def _metadata(self) -> Dict[str, EpcObjectMetadata]:
        """Backward compatibility property for accessing metadata."""
        return self._metadata_mgr._metadata

    @property
    def export_version(self) -> EpcExportVersion:
        """Get the detected or set export version."""
        return self._metadata_mgr._export_version

    @property
    def rels_update_mode(self) -> RelsUpdateMode:
        """Get the relationship update mode."""
        return self._rels_mgr.rels_update_mode

    @rels_update_mode.setter
    def rels_update_mode(self, mode: RelsUpdateMode) -> None:
        """Set the relationship update mode."""
        if not isinstance(mode, RelsUpdateMode):
            raise ValueError(f"Invalid rels_update_mode: {mode}. Must be an instance of RelsUpdateMode Enum.")
        self._rels_mgr.rels_update_mode = mode

    # ================================
    # Public API Methods
    # ================================

    def add_object(self, obj: Any, replace_if_exists: bool = True) -> Optional[str]:
        """Add an object to the EPC file. Returns the identifier of the added object."""
        # 1. Test if object already exists (by UUID) and handle according to replace_if_exists
        # 2. Call put_object to write the object data and metadata to the EPC file
        # 3. Update relationships if needed (depending on rels_update_mode)
        # 4. Return the identifier of the added object
        if not replace_if_exists:
            obj_uri: Uri = get_obj_uri(obj=obj, dataspace=None)
            if obj_uri is None:
                logging.error("Failed to get URI for the object, cannot add to EPC")
                return None
            obj_identifier = obj_uri.as_identifier()
            if self._metadata_mgr.get_metadata(obj_identifier) is not None:
                logging.warning(
                    f"Object with identifier {obj_identifier} already exists and replace_if_exists is False, skipping add"
                )
                raise ValueError(
                    f"Object with identifier {obj_identifier} already exists and replace_if_exists is False"
                )

        return self.put_object(obj=obj)

    def clear_cache(self) -> None:
        """Clear the object cache to free memory."""
        self._object_cache.clear()
        self._access_order.clear()
        self.stats.loaded_objects = 0

    def rebuild_all_rels(self, clean_first: bool = True) -> Dict[str, int]:
        """
        Rebuild all .rels files from scratch by analyzing all objects and their references.

        This method:
        1. Optionally cleans existing .rels files first
        2. Loads each object temporarily
        3. Analyzes its Data Object References (DORs)
        4. Creates/updates .rels files with proper SOURCE and DESTINATION relationships

        Args:
            clean_first: If True, remove all existing .rels files before rebuilding

        Returns:
            Dictionary with statistics:
            - 'objects_processed': Number of objects analyzed
            - 'rels_files_created': Number of .rels files created
            - 'source_relationships': Number of SOURCE relationships created
            - 'destination_relationships': Number of DESTINATION relationships created
            - 'parallel_mode': True if parallel processing was used (optional key)
            - 'execution_time': Execution time in seconds (optional key)
        """
        if self.enable_parallel_rels:
            return self._rebuild_all_rels_parallel(clean_first)
        else:
            return self._rebuild_all_rels_sequential(clean_first)

    def add_rels_for_object(
        self, identifier: Union[str, Uri, Any], relationships: Union[Relationship, List[Relationship]]
    ) -> None:
        """
        Add additional relationships for a specific object.

        Args:
            identifier: The identifier of the object, can be str, Uri, or the object itself
            relationships: List of Relationship objects to add
        """
        _id = self._id_from_uri_or_identifier(identifier=identifier, get_first_if_simple_uuid=True)

        if _id is None:
            logging.warning(f"Invalid identifier provided for adding relationships: {identifier}")
            return

        if not isinstance(relationships, list):
            relationships = [relationships]

        if _id not in self._rels_mgr.additional_rels:
            self._rels_mgr.additional_rels[_id] = []
        self._rels_mgr.additional_rels[_id].extend(relationships)
        self._rels_mgr._write_rels_updates(
            current_object_id=_id,
            current_rels_additions=relationships,
        )

    def get_statistics(self) -> EpcStreamingStats:
        """Get current statistics about the EPC streaming operations."""
        return self.stats

    def get_h5_file_paths(self, obj: Union[str, Uri, Any]) -> List[str]:
        """
        Get all HDF5 file paths referenced in the EPC file (from rels to external resources).
        Optimized to avoid loading the object when identifier/URI is provided.

        :param obj: the object or its identifier/URI
        :return: list of HDF5 file paths
        """
        if self.force_h5_path is not None:
            return [self.force_h5_path]
        h5_paths = set()

        rels_path = None

        _id = self._id_from_uri_or_identifier(identifier=obj, get_first_if_simple_uuid=True)
        if _id is not None:
            rels_path = self._metadata_mgr.gen_rels_path_from_identifier(_id)

            # Check in-memory additional rels first
            for rels in self._rels_mgr.additional_rels.get(_id, []):
                if rels.type_value == str(EPCRelsRelationshipType.EXTERNAL_RESOURCE):
                    h5_paths.add(rels.target)

        # Also check rels from the EPC file
        if rels_path is not None:
            with self._zip_accessor.get_zip_file() as zf:
                try:
                    rels_data = zf.read(rels_path)
                    self.stats.bytes_read += len(rels_data)
                    relationships = read_energyml_xml_bytes(rels_data, Relationships)
                    for rel in relationships.relationship:
                        if rel.type_value == str(EPCRelsRelationshipType.EXTERNAL_RESOURCE):
                            h5_paths.add(rel.target)
                except KeyError:
                    pass

        if len(h5_paths) == 0:
            # search if an h5 file has the same name than the epc file
            epc_folder = os.path.dirname(self.epc_file_path)
            if epc_folder is not None and self.epc_file_path is not None:
                epc_file_name = os.path.basename(self.epc_file_path)
                epc_file_base, _ = os.path.splitext(epc_file_name)
                possible_h5_path = os.path.join(epc_folder, epc_file_base + ".h5")
                if os.path.exists(possible_h5_path):
                    h5_paths.add(possible_h5_path)
        return list(h5_paths)

    #    ________    ___   __________    __  _________________  ______  ____  _____
    #   / ____/ /   /   | / ___/ ___/   /  |/  / ____/_  __/ / / / __ \/ __ \/ ___/
    #  / /   / /   / /| | \__ \\__ \   / /|_/ / __/   / / / /_/ / / / / / / /\__ \
    # / /___/ /___/ ___ |___/ /__/ /  / /  / / /___  / / / __  / /_/ / /_/ /___/ /
    # \____/_____/_/  |_/____/____/  /_/  /_/_____/ /_/ /_/ /_/\____/_____//____/

    #     ______                                      _______ __                              ____      __            ____
    #    / ____/___  ___  _________ ___  ______ ___  / / ___// /_____  _________ _____ ____  /  _/___  / /____  _____/ __/___ _________
    #   / __/ / __ \/ _ \/ ___/ __ `/ / / / __ `__ \/ /\__ \/ __/ __ \/ ___/ __ `/ __ `/ _ \ / // __ \/ __/ _ \/ ___/ /_/ __ `/ ___/ _ \
    #  / /___/ / / /  __/ /  / /_/ / /_/ / / / / / / /___/ / /_/ /_/ / /  / /_/ / /_/ /  __// // / / / /_/  __/ /  / __/ /_/ / /__/  __/
    # /_____/_/ /_/\___/_/   \__, /\__, /_/ /_/ /_/_//____/\__/\____/_/   \__,_/\__, /\___/___/_/ /_/\__/\___/_/  /_/  \__,_/\___/\___/
    #                       /____//____/                                       /____/

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """
        Retrieve an EnergyML object from the EPC file by its identifier or UUID.

        This method implements lazy loading with caching for memory efficiency.
        If a simple UUID is provided and multiple versions exist, returns the first one.

        Args:
            identifier: Object identifier (full identifier string or URI) or simple UUID.
                       Can be:
                       - A full identifier string (e.g., "eml:///resqml20.obj_TriangulatedSetRepresentation(uuid=abc-123, version='1.0')")
                       - A Uri object
                       - A simple UUID string (e.g., "abc-123")

        Returns:
            The deserialized EnergyML object, or None if not found or an error occurred.

        Behavior:
            - Checks the in-memory cache first (fast path)
            - If not cached, loads from ZIP file and deserializes XML
            - Updates cache and LRU access order
            - Updates statistics (cache hits/misses, bytes read)

        Notes:
            - For simple UUID lookups with multiple versions, returns the first match
            - Use get_object_by_uuid() to retrieve all versions of an object
        """
        _id = self._id_from_uri_or_identifier(identifier=identifier, get_first_if_simple_uuid=True)
        if _id is None:
            logging.warning(f"Invalid identifier provided: {identifier}")
            return None
        metadata = self._metadata_mgr.get_metadata(_id)

        if metadata is None:
            logging.warning(f"Object with identifier {_id} not found in metadata")
            return None

        # Check cache first
        if _id in self._object_cache:
            self._update_access_order(_id)  # type: ignore
            self.stats.cache_hits += 1
            return self._object_cache[_id]

        self.stats.cache_misses += 1

        file_path = metadata.file_path(export_version=self._metadata_mgr._export_version)

        try:
            with self._zip_accessor.get_zip_file() as zf:
                obj_data = zf.read(file_path)
                self.stats.bytes_read += len(obj_data)

                obj_class = get_class_from_content_type(metadata.content_type)
                obj = read_energyml_xml_bytes(obj_data, obj_class)
                # add to cache
                self._object_cache[_id] = obj
                self._update_access_order(_id)  # type: ignore
                return obj

        except Exception as e:
            logging.error(f"Failed to load object {identifier}: {e}")
        return None

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """
        Retrieve all EnergyML objects with the given UUID from the EPC file.

        This method returns all versions/instances of objects sharing the same UUID.
        In well-formed EPC files, typically only one object per UUID exists, but this
        method handles cases where multiple versions are present.

        Args:
            uuid: The UUID string to search for (e.g., "abc-123-def-456")

        Returns:
            List of deserialized EnergyML objects with the given UUID.
            Returns empty list if:
            - UUID is invalid or None
            - No objects with this UUID exist
            - All objects failed to load

        Behavior:
            - Validates UUID format and type
            - Retrieves all identifiers for the UUID from metadata manager
            - First collects all cached objects (fast path)
            - Then opens ZIP file once to load all non-cached objects in batch (efficient)
            - Maintains cache consistency across all loaded objects
            - Updates statistics for each object loaded

        Notes:
            - Objects are loaded lazily with caching for efficiency
            - Cache is updated for each successfully loaded object
            - Failed loads are logged but don't prevent other objects from loading
            - ZIP file is opened only once for all non-cached objects (performance optimization)
        """
        # Type guard: ensure uuid is a string
        if not isinstance(uuid, str):
            logging.warning(f"get_object_by_uuid called with non-string uuid: {type(uuid)}")
            return []

        # Type guard: ensure uuid is not empty
        if not uuid or not uuid.strip():
            logging.warning("get_object_by_uuid called with empty UUID")
            return []

        # Type guard: validate UUID format
        if OptimizedRegex.UUID.fullmatch(uuid) is None:
            logging.warning(f"get_object_by_uuid called with invalid UUID format: {uuid}")
            return []

        # Get all identifiers for this UUID
        identifiers = self._metadata_mgr.get_uuid_identifiers(uuid)

        # Guard: check if identifiers list is valid
        if identifiers is None or not isinstance(identifiers, list):
            logging.debug(f"No identifiers found for UUID: {uuid}")
            return []

        if len(identifiers) == 0:
            logging.debug(f"No objects found with UUID: {uuid}")
            return []

        # Phase 1: Collect cached objects and prepare list of non-cached identifiers
        objects = []
        non_cached_metadata = []  # List of (identifier, metadata) tuples to load from ZIP

        for identifier in identifiers:
            # Type guard: ensure identifier is valid
            if not identifier or not isinstance(identifier, str):
                logging.warning(f"Skipping invalid identifier in UUID lookup: {identifier}")
                continue

            # Get metadata first to validate object exists
            metadata = self._metadata_mgr.get_metadata(identifier)
            if metadata is None:
                logging.warning(f"Metadata not found for identifier {identifier}, skipping")
                continue

            # Check cache first for consistency
            if identifier in self._object_cache:
                obj = self._object_cache[identifier]
                if obj is not None:  # Guard: ensure cached object is valid
                    self._update_access_order(identifier)
                    self.stats.cache_hits += 1
                    objects.append(obj)
                else:
                    # Remove invalid cached entry and mark for re-loading
                    logging.warning(f"Removing invalid cached object for {identifier}")
                    del self._object_cache[identifier]
                    non_cached_metadata.append((identifier, metadata))
                    self.stats.cache_misses += 1
            else:
                # Not in cache, need to load from ZIP
                non_cached_metadata.append((identifier, metadata))
                self.stats.cache_misses += 1

        # Phase 2: Load all non-cached objects in a single ZIP file access
        if non_cached_metadata:
            try:
                with self._zip_accessor.get_zip_file() as zf:
                    for identifier, metadata in non_cached_metadata:
                        file_path = metadata.file_path(export_version=self._metadata_mgr._export_version)

                        try:
                            obj_data = zf.read(file_path)
                            self.stats.bytes_read += len(obj_data)

                            obj_class = get_class_from_content_type(metadata.content_type)
                            obj = read_energyml_xml_bytes(obj_data, obj_class)

                            # Guard: validate deserialized object
                            if obj is None:
                                logging.warning(f"Deserialization returned None for {identifier}")
                                continue

                            # Add to cache with consistency check
                            self._object_cache[identifier] = obj
                            self._update_access_order(identifier)
                            objects.append(obj)

                        except KeyError:
                            logging.error(f"File not found in ZIP for identifier {identifier}: {file_path}")
                        except Exception as e:
                            logging.error(f"Failed to deserialize object {identifier}: {e}")

            except Exception as e:
                logging.error(f"Failed to open ZIP file for batch loading: {e}")

        return objects

    def put_object(self, obj: Any, dataspace: Optional[str] = None) -> Optional[str]:
        # 1. Generate identifier and metadata for the object
        # 2. Write object data and metadata to the EPC file in a temporary file and then replace original to minimize I/O
        # 3. Update relationships if needed (depending on rels_update_mode)
        # 4. Return the identifier of the added/updated object

        uri = get_obj_uri(obj=obj, dataspace=None)
        if uri is None:
            raise ValueError("Failed to generate URI for the object, cannot put into EPC")

        identifier = uri.as_identifier()
        existing_metadata = self._metadata_mgr.get_metadata(identifier)
        file_path = gen_energyml_object_path(obj, self._metadata_mgr._export_version)
        is_update = existing_metadata is not None

        # Write object data and metadata to EPC
        try:
            file_allready_exists = False

            with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
                temp_path = temp_file.name
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zf:
                epc_content_type = None
                # Copy all existing files except the one being updated (if update) and its .rels file
                with self._zip_accessor.get_zip_file() as source_zf:
                    for item in source_zf.infolist():
                        # logging.debug(
                        #     f"Test {get_epc_content_type_path() in item.filename} with {item.filename} and {get_epc_content_type_path()} "
                        # )
                        if get_epc_content_type_path() in item.filename:
                            epc_content_type = source_zf.read(item.filename)
                        elif item.filename != file_path:
                            data = source_zf.read(item.filename)
                            zf.writestr(item, data)
                        else:
                            file_allready_exists = True

                    # Write new/updated object data
                    obj_xml_bytes = serialize_xml(obj)
                    zf.writestr(file_path, obj_xml_bytes)

                if not file_allready_exists:
                    ct_object = None
                    if epc_content_type is not None:
                        # logging.debug("Existing content type found, adding new object to it")
                        # add the new object to the existing content type and write it
                        ct_object = read_energyml_xml_bytes(epc_content_type, Types)
                        # logging.debug("Existing content type before adding object: " + str(ct_object))
                        ct_object.override.append(
                            Override(part_name=file_path, content_type=get_content_type_from_class(obj))
                        )
                    if ct_object is None:
                        # logging.debug("No existing content type found, generating new one from metadata manager")
                        ct_object = self._metadata_mgr.get_content_type(zf)
                    # logging.debug("New content type after adding object: " + str(ct_object))
                    zf.writestr(get_epc_content_type_path(), serialize_xml(ct_object))
                    # logging.debug("Written content type to EPC with new object : " + serialize_xml(ct_object))
                elif epc_content_type is not None:
                    zf.writestr(get_epc_content_type_path(), epc_content_type)
            # Replace original
            shutil.move(temp_path, self.epc_file_path)
            self._zip_accessor.reopen_persistent_zip()
        except Exception as e:
            raise IOError(f"Failed to write object to EPC: {e}")

        # adding the metadata to the metadata manager (after writing the file to ensure we have the correct export version for path generation)
        last_update = get_object_attribute_advanced(obj, "citation.lastUpdate")
        if last_update is None and isinstance(last_update, str):
            last_update = date_to_datetime(last_update)
        self._metadata_mgr.add_metadata(EpcObjectMetadata(uri=uri, title=get_obj_title(obj), last_changed=last_update))

        # update relationships if needed
        if self.rels_update_mode == RelsUpdateMode.UPDATE_AT_MODIFICATION:
            if file_allready_exists:
                self._rels_mgr.update_rels_for_modified_object(obj, identifier)
            else:
                self._rels_mgr.update_rels_for_new_object(obj, identifier)

        return identifier

    def delete_object(self, identifier: Union[str, Uri, Any]) -> bool:
        # 1. Validate identifier and check if object exists
        # 2. Update rels by removing from current object rels the "Destination" relationships to the deleted object and from other objects rels the "Source" relationships to the deleted object (depending on rels_update_mode)
        # 3. Remove object data and metadata from the EPC file in a temporary file and then replace original to minimize I/O
        # 4. Return True if deletion was successful, False otherwise
        _id = self._id_from_uri_or_identifier(identifier=identifier)
        if _id is None:
            logging.warning(f"Invalid identifier provided for deletion: {identifier}")
            return False
        metadata = self._metadata_mgr.get_metadata(_id)
        if metadata is None:
            logging.warning(f"Object with identifier {_id} not found in metadata, cannot delete")
            return False

        if self.rels_update_mode == RelsUpdateMode.UPDATE_AT_MODIFICATION:
            self._rels_mgr.update_rels_for_removed_object(
                _id
            )  # will update content_type when removing the object if needed

        # update metadata manager to remove the metadata of the deleted object
        self._metadata_mgr.remove_metadata(_id)
        return True

    def read_array(self, proxy: Union[str, Uri, Any], path_in_external: str) -> Optional[np.ndarray]:
        """
        Read a dataset from an external file (HDF5, Parquet, CSV, etc.) linked to the proxy object.

        Uses an intelligent caching mechanism that:
        1. Checks cached open files first (up to 3 files kept open)
        2. Tries all possible file paths
        3. Automatically selects the correct reader based on file extension
        4. Adds successfully opened files to cache

        Args:
            proxy: The object, its identifier, or URI
            path_in_external: Path/dataset name within the external file

        Returns:
            Numpy array if successful, None otherwise
        """
        # Get possible file paths for this object
        file_paths = []

        if self.force_h5_path is not None:
            # Use forced path if specified
            file_paths = [self.force_h5_path]
        else:
            # Get file paths from relationships
            file_paths = self.get_h5_file_paths(proxy)

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return None

        # Keep track of which paths we've tried from cache vs from scratch
        cached_paths = [p for p in file_paths if p in self._file_cache]
        non_cached_paths = [p for p in file_paths if p not in self._file_cache]

        # Try cached files first (most recently used first)
        for file_path in cached_paths:
            handler = self._handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Get cached file handle
                file_handle = self._file_cache.get_or_open(file_path, handler, mode="r")
                if file_handle is not None:
                    # Try to read from cached handle
                    result = handler.read_array(file_handle, path_in_external)
                    if result is not None:
                        return result
            except Exception as e:
                logging.debug(f"Failed to read from cached file {file_path}: {e}")
                # Remove from cache if it's causing issues
                self._file_cache.remove(file_path)

        # Try non-cached files
        for file_path in non_cached_paths:
            handler = self._handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Try to open and read, which will add to cache if successful
                file_handle = self._file_cache.get_or_open(file_path, handler, mode="r")
                if file_handle is not None:
                    result = handler.read_array(file_handle, path_in_external)
                    if result is not None:
                        return result
                else:
                    # Cache failed, try direct read without caching
                    result = handler.read_array(file_path, path_in_external)
                    if result is not None:
                        return result
            except Exception as e:
                logging.debug(f"Failed to read from file {file_path}: {e}")

        logging.error(f"Failed to read array from any available file paths: {file_paths}")
        return None

    def write_array(self, proxy: Union[str, Uri, Any], path_in_external: str, array: np.ndarray, **kwargs) -> bool:
        """
        Write a dataset to an external file (HDF5, Parquet, CSV, etc.) linked to the proxy object.

        Uses the same caching mechanism as read_array for efficiency.

        Args:
            proxy: The object, its identifier, or URI
            path_in_external: Path/dataset name within the external file
            array: Numpy array to write
            **kwargs: Additional format-specific parameters (e.g., dtype for HDF5, column_titles for Parquet)

        Returns:
            True if successful, False otherwise
        """
        # Get possible file paths for this object
        file_paths = []

        if self.force_h5_path is not None:
            # Use forced path if specified
            file_paths = [self.force_h5_path]
        else:
            # Get file paths from relationships
            file_paths = self.get_h5_file_paths(proxy)

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return False

        # Try to write to the first available file
        # For writes, we prefer cached files first, then non-cached
        cached_paths = [p for p in file_paths if p in self._file_cache]
        non_cached_paths = [p for p in file_paths if p not in self._file_cache]

        # Try cached files first
        for file_path in cached_paths:
            handler = self._handler_registry.get_handler_for_file(file_path)
            if handler is None:
                continue

            try:
                file_handle = self._file_cache.get_or_open(file_path, handler, mode="a")
                if file_handle is not None:
                    success = handler.write_array(file_handle, array, path_in_external, **kwargs)
                    if success:
                        return True
            except Exception as e:
                logging.debug(f"Failed to write to cached file {file_path}: {e}")
                self._file_cache.remove(file_path)

        # Try non-cached files
        for file_path in non_cached_paths:
            handler = self._handler_registry.get_handler_for_file(file_path)
            if handler is None:
                continue

            try:
                # Open in append mode and add to cache
                file_handle = self._file_cache.get_or_open(file_path, handler, mode="a")
                if file_handle is not None:
                    success = handler.write_array(file_handle, array, path_in_external, **kwargs)
                    if success:
                        return True
                else:
                    # Cache failed, try direct write
                    success = handler.write_array(file_path, array, path_in_external, **kwargs)
                    if success:
                        return True
            except Exception as e:
                logging.error(f"Failed to write to file {file_path}: {e}")

        return False

    def get_array_metadata(
        self, proxy: Union[str, Uri, Any], path_in_external: Optional[str] = None
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """
        Get metadata for data array(s) without loading the full array data.

        Args:
            proxy: The object, its identifier, or URI
            path_in_external: Optional specific array path. If None, returns metadata for all arrays.

        Returns:
            DataArrayMetadata if path specified, List[DataArrayMetadata] if no path,
            or None if not found
        """
        # Get possible file paths for this object
        file_paths = []

        if self.force_h5_path is not None:
            file_paths = [self.force_h5_path]
        else:
            file_paths = self.get_h5_file_paths(proxy)

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return None

        # Try cached files first
        cached_paths = [p for p in file_paths if p in self._file_cache]
        non_cached_paths = [p for p in file_paths if p not in self._file_cache]

        for file_path in cached_paths + non_cached_paths:
            handler = self._handler_registry.get_handler_for_file(file_path)
            if handler is None:
                continue

            try:
                file_handle = self._file_cache.get_or_open(file_path, handler, mode="r")
                source = file_handle if file_handle is not None else file_path

                metadata_dict = handler.get_array_metadata(source, path_in_external)

                if metadata_dict is None:
                    continue

                # Convert dict(s) to DataArrayMetadata
                if isinstance(metadata_dict, list):
                    return [
                        DataArrayMetadata(
                            path_in_resource=m.get("path"),
                            array_type=m.get("dtype", "unknown"),
                            dimensions=m.get("shape", []),
                            custom_data={"size": m.get("size", 0)},
                        )
                        for m in metadata_dict
                    ]
                else:
                    return DataArrayMetadata(
                        path_in_resource=metadata_dict.get("path"),
                        array_type=metadata_dict.get("dtype", "unknown"),
                        dimensions=metadata_dict.get("shape", []),
                        custom_data={"size": metadata_dict.get("size", 0)},
                    )
            except Exception as e:
                logging.debug(f"Failed to get metadata from file {file_path}: {e}")

        return None

    def list_objects(
        self, dataspace: Optional[str] = None, object_type: Optional[str] = None
    ) -> List[ResourceMetadata]:
        return [m.to_resource_metadata() for m in self._metadata_mgr.list_metadata(qualified_type_filter=object_type)]

    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        _id = self._id_from_uri_or_identifier(obj)

        if _id is None:
            logging.warning(f"Could not resolve identifier for object {obj}, cannot get relationships")
            return []

        metadata = self._metadata_mgr.get_metadata(_id)
        if metadata is None:
            logging.warning(f"Object with identifier {_id} not found in metadata, cannot get relationships")
            return []

        return self._rels_mgr.get_obj_rels(_id)

    def close(self) -> None:
        """Close the persistent ZIP file if it's open, recomputing rels first if mode is UPDATE_ON_CLOSE."""
        # Unregister atexit handler to avoid double-close
        if getattr(self, "_atexit_registered", False):
            atexit.unregister(self._atexit_close)
            self._atexit_registered = False

        # Recompute all relationships before closing if in UPDATE_ON_CLOSE mode
        if self.rels_update_mode == RelsUpdateMode.UPDATE_ON_CLOSE:
            try:
                self.rebuild_all_rels(clean_first=True)
                logging.info("Rebuilt all relationships on close (UPDATE_ON_CLOSE mode)")
            except Exception as e:
                logging.warning(f"Error rebuilding rels on close: {e}")

        # Close file cache
        if hasattr(self, "_file_cache"):
            self._file_cache.close_all()

        # Close cached h5 if using force_h5_path
        if self.cache_opened_h5 is not None:
            try:
                self.cache_opened_h5.close()
            except Exception as e:
                logging.debug(f"Error closing cache_opened_h5: {e}")
            self.cache_opened_h5 = None

        # Delegate to ZIP accessor
        self._zip_accessor.close()

    def get_object_dependencies(self, identifier: Union[str, Uri]) -> List[str]:
        return list(get_dor_identifiers_from_obj(self.get_object(identifier)))

    def start_transaction(self) -> bool:
        raise NotImplementedError("Transactions are not implemented in this version of EpcStreamReader")

    def commit_transaction(self) -> Tuple[bool, Optional[str]]:
        raise NotImplementedError("Transactions are not implemented in this version of EpcStreamReader")

    def rollback_transaction(self) -> bool:
        raise NotImplementedError("Transactions are not implemented in this version of EpcStreamReader")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.clear_cache()
        self.close()
        # Note: close() now handles cache_opened_h5

    def __len__(self) -> int:
        """Return total number of objects."""
        return len(self._metadata)

    def __iter__(self) -> Iterator[str]:
        """Iterate over object identifiers."""
        return iter(self._metadata.keys())

    #     ____  ____  _____    _____  ____________
    #    / __ \/ __ \/  _/ |  / /   |/_  __/ ____/
    #   / /_/ / /_/ // / | | / / /| | / / / __/
    #  / ____/ _, _// /  | |/ / ___ |/ / / /___
    # /_/   /_/ |_/___/  |___/_/  |_/_/ /_____/

    def __del__(self):
        """Destructor to ensure persistent ZIP file is closed."""
        try:
            self.close()
            if self.cache_opened_h5 is not None:
                try:
                    self.cache_opened_h5.close()
                except Exception:
                    pass
                self.cache_opened_h5 = None
        except Exception:
            pass  # Ignore errors during cleanup

    def _atexit_close(self) -> None:
        """Atexit callback — performs minimal cleanup without rebuilding rels."""
        try:
            self._zip_accessor.close()
        except Exception:
            pass

    def _update_access_order(self, identifier: str) -> None:
        """Update access order for LRU cache."""
        if identifier in self._access_order:
            self._access_order.remove(identifier)
            self._access_order.insert(0, identifier)

    def _id_from_uri_or_identifier(
        self, identifier: Union[str, Uri, Any], get_first_if_simple_uuid: bool = True
    ) -> Optional[str]:
        if identifier is None:
            return None
        elif isinstance(identifier, str):
            if OptimizedRegex.UUID.fullmatch(identifier) is not None:
                if not get_first_if_simple_uuid:
                    logging.warning(
                        f"Identifier {identifier} is a simple UUID, but get_first_if_simple_uuid is False, cannot resolve to full identifier"
                    )
                    return None
                # If it's a simple UUID, we need to find the corresponding identifier from metadata
                t_metadata_identifiers = self._metadata_mgr.get_uuid_identifiers(identifier)
                if t_metadata_identifiers is not None and len(t_metadata_identifiers) > 0:
                    return t_metadata_identifiers[
                        0
                    ]  # If multiple metadata entries for the same UUID, we take the first one (this should not happen in a well-formed EPC file)
                else:
                    logging.warning(f"No metadata found for UUID {identifier}, cannot get relationships")
                    return None
            else:
                return identifier
        elif isinstance(identifier, Uri):
            return identifier.as_identifier()
        elif isinstance(identifier, ResourceMetadata):
            return self._id_from_uri_or_identifier(identifier.identifier)
        elif isinstance(identifier, EpcObjectMetadata):
            return self._id_from_uri_or_identifier(identifier.uri)
        else:
            # Try to get URI from object
            obj_uri = get_obj_uri(obj=identifier, dataspace=None)
            if obj_uri is not None:
                return obj_uri.as_identifier()
            return str(identifier)

    def _rebuild_all_rels_sequential(self, clean_first: bool = True) -> Dict[str, int]:
        """
        Rebuild all .rels files from scratch by analyzing all objects and their references.

        This method:
        1. Optionally cleans existing .rels files first
        2. Loads each object temporarily
        3. Analyzes its Data Object References (DORs)
        4. Creates/updates .rels files with proper SOURCE and DESTINATION relationships

        Args:
            clean_first: If True, remove all existing .rels files before rebuilding

        Returns:
            Dictionary with statistics:
            - 'objects_processed': Number of objects analyzed
            - 'rels_files_created': Number of .rels files created
            - 'source_relationships': Number of SOURCE relationships created
            - 'destination_relationships': Number of DESTINATION relationships created
        """
        import tempfile
        import shutil

        stats = {
            "objects_processed": 0,
            "rels_files_created": 0,
            "source_relationships": 0,
            "destination_relationships": 0,
        }

        logging.info(f"Starting rebuild of all .rels files for {len(self._metadata)} objects...")

        # Build a map of which objects are referenced by which objects
        # Key: target identifier, Value: list of (source_identifier, source_obj)
        reverse_references: Dict[str, List[Tuple[str, Any]]] = {}

        # First pass: analyze all objects and build the reference map
        for identifier in self._metadata:
            try:
                obj = self.get_object(identifier)
                if obj is None:
                    continue

                stats["objects_processed"] += 1

                # Extract this object's type
                obj_type = get_obj_type(get_obj_usable_class(obj))

                # Get all DORs in this object
                dors = get_direct_dor_list(obj)

                for dor in dors:
                    try:
                        target_identifier = get_obj_identifier(dor)
                        if target_identifier in self._metadata:
                            # Record this reference (for building SOURCE rels in target's file)
                            if target_identifier not in reverse_references:
                                reverse_references[target_identifier] = []
                            reverse_references[target_identifier].append((identifier, obj_type))
                    except Exception:
                        pass

            except Exception as e:
                logging.warning(f"Failed to analyze object {identifier}: {e}")

        # Second pass: create the .rels files
        # Map of rels_file_path -> Relationships object
        rels_files: Dict[str, Relationships] = {}

        # Process each object to create DESTINATION relationships
        for identifier in self._metadata:
            try:
                obj = self.get_object(identifier)
                if obj is None:
                    continue

                obj_rels_path = self._metadata_mgr.gen_rels_path_from_identifier(identifier)

                # Get all DORs (objects this object references)
                dors = get_direct_dor_list(obj)

                if dors:
                    # Create DESTINATION relationships (this object -> targets it references)
                    relationships = []

                    for dor in dors:
                        try:
                            target_identifier = get_obj_identifier(dor)
                            if target_identifier in self._metadata:
                                target_metadata = self._metadata[target_identifier]
                                target_type = get_obj_type(get_obj_usable_class(dor))

                                rel = Relationship(
                                    target=target_metadata.file_path(export_version=self._metadata_mgr._export_version),
                                    type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                                    id=f"_{identifier}_{target_type}_{target_identifier}",
                                )
                                relationships.append(rel)
                                stats["destination_relationships"] += 1

                        except Exception as e:
                            logging.debug(f"Failed to create DESTINATION relationship: {e}")

                    if relationships and obj_rels_path:
                        if obj_rels_path not in rels_files:
                            rels_files[obj_rels_path] = Relationships(relationship=[])
                        rels_files[obj_rels_path].relationship.extend(relationships)

            except Exception as e:
                logging.warning(f"Failed to create DESTINATION rels for {identifier}: {e}")

        # Add SOURCE relationships (in target's .rels file, pointing back to sources)
        for target_identifier, source_list in reverse_references.items():
            try:
                if target_identifier not in self._metadata:
                    continue

                target_metadata = self._metadata[target_identifier]
                target_rels_path = self._metadata_mgr.gen_rels_path_from_identifier(target_identifier)

                if not target_rels_path:
                    continue

                # Create SOURCE relationships for each object that references this one
                for source_identifier, source_type in source_list:
                    try:
                        source_metadata = self._metadata[source_identifier]

                        rel = Relationship(
                            target=source_metadata.file_path(export_version=self._metadata_mgr._export_version),
                            type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                            id=f"_{target_identifier}_{source_type}_{source_identifier}",
                        )

                        if target_rels_path not in rels_files:
                            rels_files[target_rels_path] = Relationships(relationship=[])
                        rels_files[target_rels_path].relationship.append(rel)
                        stats["source_relationships"] += 1

                    except Exception as e:
                        logging.debug(f"Failed to create SOURCE relationship: {e}")

            except Exception as e:
                logging.warning(f"Failed to create SOURCE rels for {target_identifier}: {e}")

        stats["rels_files_created"] = len(rels_files)

        # Before writing, preserve EXTERNAL_RESOURCE and other non-SOURCE/DESTINATION relationships
        # This includes rels files that may not be in rels_files yet
        with self._zip_accessor.get_zip_file() as zf:
            # Check all existing .rels files
            for filename in zf.namelist():
                if not filename.endswith(".rels"):
                    continue

                try:
                    rels_data = zf.read(filename)
                    existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                    if existing_rels_obj and existing_rels_obj.relationship:
                        # Preserve non-SOURCE/DESTINATION relationships (e.g., EXTERNAL_RESOURCE)
                        preserved_rels = [
                            r
                            for r in existing_rels_obj.relationship
                            if r.type_value
                            not in (
                                EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                                EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                            )
                        ]
                        if preserved_rels:
                            if filename in rels_files:
                                # Add preserved relationships to existing entry
                                rels_files[filename].relationship = preserved_rels + rels_files[filename].relationship
                            else:
                                # Create new entry with only preserved relationships
                                rels_files[filename] = Relationships(relationship=preserved_rels)
                except Exception as e:
                    logging.debug(f"Could not preserve existing rels from {filename}: {e}")

        # Third pass: write the new EPC with updated .rels files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with self._zip_accessor.get_zip_file() as source_zip:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zip:
                    # Copy all non-.rels files
                    for item in source_zip.infolist():
                        if not (item.filename.endswith(".rels") and clean_first):
                            data = source_zip.read(item.filename)
                            target_zip.writestr(item, data)

                    # Write new .rels files
                    for rels_path, rels_obj in rels_files.items():
                        rels_xml = serialize_xml(rels_obj)
                        target_zip.writestr(rels_path, rels_xml)

            # Replace original file
            shutil.move(temp_path, self.epc_file_path)
            self._zip_accessor.reopen_persistent_zip()

            logging.info(
                f"Rebuilt .rels files: processed {stats['objects_processed']} objects, "
                f"created {stats['rels_files_created']} .rels files, "
                f"added {stats['source_relationships']} SOURCE and "
                f"{stats['destination_relationships']} DESTINATION relationships"
            )

            return stats

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise RuntimeError(f"Failed to rebuild .rels files: {e}")

    def _rebuild_all_rels_parallel(self, clean_first: bool = True) -> Dict[str, int]:
        """
        Parallel implementation of rebuild_all_rels using multiprocessing.

        Strategy:
        1. Use multiprocessing.Pool to process objects in parallel
        2. Each worker loads an object and computes its SOURCE relationships
        3. Main process aggregates results and builds DESTINATION relationships
        4. Sequential write phase (ZIP writing must be sequential)

        This bypasses Python's GIL for CPU-intensive XML parsing and provides
        significant speedup for large EPCs (tested with 80+ objects).
        """
        import time
        from multiprocessing import Pool, cpu_count

        start_time = time.time()

        stats = {
            "objects_processed": 0,
            "rels_files_created": 0,
            "source_relationships": 0,
            "destination_relationships": 0,
            "parallel_mode": True,
        }

        num_objects = len(self._metadata)
        logging.info(f"Starting PARALLEL rebuild of all .rels files for {num_objects} objects...")

        # Prepare work items for parallel processing
        # Pass metadata as dict (serializable) instead of keeping references
        metadata_dict = {k: v for k, v in self._metadata.items()}
        export_version = self._metadata_mgr._export_version
        work_items = [
            ((identifier, str(self.epc_file_path), metadata_dict), export_version) for identifier in self._metadata
        ]

        # Determine optimal number of workers based on available CPUs and workload
        # Don't spawn more workers than CPUs; use user-configurable ratio for workload per worker
        worker_ratio = self.parallel_worker_ratio if hasattr(self, "parallel_worker_ratio") else _WORKER_POOL_SIZE_RATIO
        num_workers = min(cpu_count(), max(1, num_objects // worker_ratio))
        logging.info(f"Using {num_workers} worker processes for {num_objects} objects (ratio: {worker_ratio})")

        # ============================================================================
        # PHASE 1: PARALLEL - Compute SOURCE relationships across worker processes
        # ============================================================================
        results = []
        with Pool(processes=num_workers) as pool:
            results = pool.starmap(process_object_for_rels_worker, work_items)

        # ============================================================================
        # PHASE 2: SEQUENTIAL - Aggregate worker results and build DESTINATION relationships
        # ============================================================================
        # Build data structures for subsequent phases:
        # - reverse_references: Map target objects to their sources (for SOURCE rels in target)
        # - rels_files: Accumulate all relationships by file path
        reverse_references: Dict[str, List[Tuple[str, str]]] = {}  # target_id -> [(source_id, source_type)]
        rels_files: Dict[str, Relationships] = {}

        for result in results:
            if result is None:
                continue

            identifier = result["identifier"]
            object_type = result["object_type"]
            referenced_objects = result["referenced_objects"]

            stats["objects_processed"] += 1

            # Create DESTINATION relationships for this object (objects this one references)
            obj_rels_path = self._metadata_mgr.gen_rels_path_from_identifier(identifier)
            if obj_rels_path and referenced_objects:
                if obj_rels_path not in rels_files:
                    rels_files[obj_rels_path] = Relationships(relationship=[])

                for target_identifier, target_type in referenced_objects:
                    # Verify target exists in metadata
                    if target_identifier not in self._metadata:
                        continue

                    target_metadata = self._metadata[target_identifier]

                    # Create DESTINATION relationship (this object -> target)
                    rel = Relationship(
                        target=target_metadata.file_path(export_version=export_version),
                        type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                        id=f"_{identifier}_{target_type}_{target_identifier}",
                    )
                    rels_files[obj_rels_path].relationship.append(rel)
                    stats["destination_relationships"] += 1

                    # Build reverse reference map for SOURCE relationships
                    if target_identifier not in reverse_references:
                        reverse_references[target_identifier] = []
                    reverse_references[target_identifier].append((identifier, object_type))

        # ============================================================================
        # PHASE 3: SEQUENTIAL - Create SOURCE relationships
        # ============================================================================
        for target_identifier, source_list in reverse_references.items():
            try:
                if target_identifier not in self._metadata:
                    continue

                target_rels_path = self._metadata_mgr.gen_rels_path_from_identifier(target_identifier)

                if not target_rels_path:
                    continue

                for source_identifier, source_type in source_list:
                    try:
                        source_metadata = self._metadata[source_identifier]

                        # Create SOURCE relationship (source object -> this target object)
                        rel = Relationship(
                            target=source_metadata.file_path(export_version=export_version),
                            type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                            id=f"_{target_identifier}_{source_type}_{source_identifier}",
                        )

                        if target_rels_path not in rels_files:
                            rels_files[target_rels_path] = Relationships(relationship=[])
                        rels_files[target_rels_path].relationship.append(rel)
                        stats["source_relationships"] += 1

                    except Exception as e:
                        logging.debug(f"Failed to create SOURCE relationship: {e}")

            except Exception as e:
                logging.warning(f"Failed to create SOURCE rels for {target_identifier}: {e}")

        stats["rels_files_created"] = len(rels_files)

        # ============================================================================
        # PHASE 4: SEQUENTIAL - Preserve non-object relationships
        # ============================================================================
        # Preserve EXTERNAL_RESOURCE and other non-standard relationship types
        with self._zip_accessor.get_zip_file() as zf:
            for filename in zf.namelist():
                if not filename.endswith(".rels"):
                    continue

                try:
                    rels_data = zf.read(filename)
                    existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                    if existing_rels_obj and existing_rels_obj.relationship:
                        preserved_rels = [
                            r
                            for r in existing_rels_obj.relationship
                            if r.type_value
                            not in (
                                EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                                EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                            )
                        ]
                        if preserved_rels:
                            if filename in rels_files:
                                rels_files[filename].relationship = preserved_rels + rels_files[filename].relationship
                            else:
                                rels_files[filename] = Relationships(relationship=preserved_rels)
                except Exception as e:
                    logging.debug(f"Could not preserve existing rels from {filename}: {e}")

        # ============================================================================
        # PHASE 5: SEQUENTIAL - Write all relationships to ZIP file
        # ============================================================================
        # ZIP file writing must be sequential (file format limitation)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with self._zip_accessor.get_zip_file() as source_zip:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zip:
                    # Copy all non-.rels files
                    for item in source_zip.infolist():
                        if not (item.filename.endswith(".rels") and clean_first):
                            data = source_zip.read(item.filename)
                            target_zip.writestr(item, data)

                    # Write new .rels files
                    for rels_path, rels_obj in rels_files.items():
                        rels_xml = serialize_xml(rels_obj)
                        target_zip.writestr(rels_path, rels_xml)

            # Replace original file
            shutil.move(temp_path, self.epc_file_path)
            self._zip_accessor.reopen_persistent_zip()

            execution_time = time.time() - start_time
            stats["execution_time"] = execution_time

            logging.info(
                f"Rebuilt .rels files (PARALLEL): processed {stats['objects_processed']} objects, "
                f"created {stats['rels_files_created']} .rels files, "
                f"added {stats['source_relationships']} SOURCE and "
                f"{stats['destination_relationships']} DESTINATION relationships "
                f"in {execution_time:.2f}s using {num_workers} workers"
            )

            return stats

        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise RuntimeError(f"Failed to rebuild .rels files (parallel): {e}")

    # =================================================================================
    # Retro compatibility aliases (to avoid breaking changes in tests and example code)
    # =================================================================================
    def remove_object(self, identifier: Union[str, Uri, Any]) -> bool:
        """Alias for delete_object for backward compatibility."""
        return self.delete_object(identifier)

    def update_object(self, obj: Any) -> Optional[str]:
        """Alias for put_object for backward compatibility."""
        return self.put_object(obj)

    def get_object_by_identifier(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """Alias for get_object for backward compatibility."""
        return self.get_object(identifier)
