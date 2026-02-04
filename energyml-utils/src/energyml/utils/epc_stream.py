# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Memory-efficient EPC file handler for large files.

This module provides EpcStreamReader - a lazy-loading, memory-efficient alternative
to the standard Epc class for handling very large EPC files without loading all
content into memory at once.
"""

import tempfile
import shutil
import logging
import os
import zipfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterator, Union, Tuple
from weakref import WeakValueDictionary

from energyml.opc.opc import Types, Override, CoreProperties, Relationships, Relationship
from energyml.utils.data.datasets_io import HDF5FileReader, HDF5FileWriter
from energyml.utils.storage_interface import DataArrayMetadata, EnergymlStorageInterface, ResourceMetadata
from energyml.utils.uri import Uri, parse_uri
import h5py
import numpy as np
from energyml.utils.constants import (
    EPCRelsRelationshipType,
    OptimizedRegex,
    EpcExportVersion,
    content_type_to_qualified_type,
)
from energyml.utils.epc import Epc, gen_energyml_object_path, gen_rels_path, get_epc_content_type_path

from energyml.utils.introspection import (
    get_class_from_content_type,
    get_obj_content_type,
    get_obj_identifier,
    get_obj_uuid,
    get_object_type_for_file_path_from_class,
    get_direct_dor_list,
    get_obj_type,
    get_obj_usable_class,
)
from energyml.utils.serialization import read_energyml_xml_bytes, serialize_xml
from .xml import is_energyml_content_type
from enum import Enum


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

    uuid: str
    object_type: str
    content_type: str
    file_path: str
    identifier: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self):
        if self.identifier is None:
            # Generate identifier if not provided
            object.__setattr__(self, "identifier", f"{self.uuid}.{self.version or ''}")


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
        self._type_index: Dict[str, List[str]] = {}  # object_type -> list of identifiers
        self._core_props: Optional[CoreProperties] = None
        self._core_props_path: Optional[str] = None

    def load_metadata(self) -> None:
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

                self.stats.total_objects = len(self._metadata)

        except Exception as e:
            logging.error(f"Failed to load metadata from EPC file: {e}")
            raise

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
            raise FileNotFoundError("No [Content_Types].xml found in EPC file")

    def _process_energyml_object_metadata(self, zf: zipfile.ZipFile, override: Override) -> None:
        """Process metadata for an EnergyML object without loading it."""
        if not override.part_name or not override.content_type:
            return

        file_path = override.part_name.lstrip("/")
        content_type = override.content_type

        try:
            # Quick peek to extract UUID and version without full parsing
            uuid, version, obj_type = self._extract_object_info_fast(zf, file_path, content_type)

            if uuid:  # Only process if we successfully extracted UUID
                metadata = EpcObjectMetadata(
                    uuid=uuid, object_type=obj_type, content_type=content_type, file_path=file_path, version=version
                )

                # Store in indexes
                identifier = metadata.identifier
                if identifier:
                    self._metadata[identifier] = metadata

                    # Update UUID index
                    if uuid not in self._uuid_index:
                        self._uuid_index[uuid] = []
                    self._uuid_index[uuid].append(identifier)

                    # Update type index
                    if obj_type not in self._type_index:
                        self._type_index[obj_type] = []
                    self._type_index[obj_type].append(identifier)

        except Exception as e:
            logging.warning(f"Failed to process metadata for {file_path}: {e}")

    def _extract_object_info_fast(
        self, zf: zipfile.ZipFile, file_path: str, content_type: str
    ) -> Tuple[Optional[str], Optional[str], str]:
        """Fast extraction of UUID and version from XML without full parsing."""
        try:
            # Read only the beginning of the file for UUID extraction
            with zf.open(file_path) as f:
                # Read first chunk (usually sufficient for root element)
                chunk = f.read(2048)  # 2KB should be enough for root element
                self.stats.bytes_read += len(chunk)

                chunk_str = chunk.decode("utf-8", errors="ignore")

                # Extract UUID using optimized regex
                uuid_match = OptimizedRegex.UUID_NO_GRP.search(chunk_str)
                uuid = uuid_match.group(0) if uuid_match else None

                # Extract version if present
                version = None
                version_patterns = [
                    r'object[Vv]ersion["\']?\s*[:=]\s*["\']([^"\']+)',
                ]

                for pattern in version_patterns:
                    import re

                    version_match = re.search(pattern, chunk_str)
                    if version_match:
                        version = version_match.group(1)
                        # Ensure version is a string
                        if not isinstance(version, str):
                            version = str(version)
                        break

                # Extract object type from content type
                obj_type = self._extract_object_type_from_content_type(content_type)

                return uuid, version, obj_type

        except Exception as e:
            logging.debug(f"Fast extraction failed for {file_path}: {e}")
            return None, None, "Unknown"

    def _extract_object_type_from_content_type(self, content_type: str) -> str:
        """Extract object type from content type string."""
        try:
            match = OptimizedRegex.CONTENT_TYPE.search(content_type)
            if match:
                return match.group("type")
        except (AttributeError, KeyError):
            pass
        return "Unknown"

    def _is_core_properties(self, content_type: str) -> bool:
        """Check if content type is CoreProperties."""
        return content_type == "application/vnd.openxmlformats-package.core-properties+xml"

    def _process_core_properties_metadata(self, override: Override) -> None:
        """Process core properties metadata."""
        if override.part_name:
            self._core_props_path = override.part_name.lstrip("/")

    def get_metadata(self, identifier: str) -> Optional[EpcObjectMetadata]:
        """Get metadata for an object by identifier."""
        return self._metadata.get(identifier)

    def get_by_uuid(self, uuid: str) -> List[str]:
        """Get all identifiers for objects with the given UUID."""
        return self._uuid_index.get(uuid, [])

    def get_by_type(self, object_type: str) -> List[str]:
        """Get all identifiers for objects of the given type."""
        return self._type_index.get(object_type, [])

    def list_metadata(self, object_type: Optional[str] = None) -> List[EpcObjectMetadata]:
        """List metadata for all objects, optionally filtered by type."""
        if object_type is None:
            return list(self._metadata.values())
        return [self._metadata[identifier] for identifier in self._type_index.get(object_type, [])]

    def add_metadata(self, metadata: EpcObjectMetadata) -> None:
        """Add metadata for a new object."""
        identifier = metadata.identifier
        if identifier:
            self._metadata[identifier] = metadata

            # Update UUID index
            if metadata.uuid not in self._uuid_index:
                self._uuid_index[metadata.uuid] = []
            self._uuid_index[metadata.uuid].append(identifier)

            # Update type index
            if metadata.object_type not in self._type_index:
                self._type_index[metadata.object_type] = []
            self._type_index[metadata.object_type].append(identifier)

            self.stats.total_objects += 1

    def remove_metadata(self, identifier: str) -> Optional[EpcObjectMetadata]:
        """Remove metadata for an object. Returns the removed metadata."""
        metadata = self._metadata.pop(identifier, None)
        if metadata:
            # Update UUID index
            if metadata.uuid in self._uuid_index:
                self._uuid_index[metadata.uuid].remove(identifier)
                if not self._uuid_index[metadata.uuid]:
                    del self._uuid_index[metadata.uuid]

            # Update type index
            if metadata.object_type in self._type_index:
                self._type_index[metadata.object_type].remove(identifier)
                if not self._type_index[metadata.object_type]:
                    del self._type_index[metadata.object_type]

            self.stats.total_objects -= 1

        return metadata

    def contains(self, identifier: str) -> bool:
        """Check if an object with the given identifier exists."""
        return identifier in self._metadata

    def __len__(self) -> int:
        """Return total number of objects."""
        return len(self._metadata)

    def __iter__(self) -> Iterator[str]:
        """Iterate over object identifiers."""
        return iter(self._metadata.keys())

    def gen_rels_path_from_metadata(self, metadata: EpcObjectMetadata) -> str:
        """Generate rels path from object metadata without loading the object."""
        obj_path = metadata.file_path
        # Extract folder and filename from the object path
        if "/" in obj_path:
            obj_folder = obj_path[: obj_path.rindex("/") + 1]
            obj_file_name = obj_path[obj_path.rindex("/") + 1 :]
        else:
            obj_folder = ""
            obj_file_name = obj_path

        return f"{obj_folder}_rels/{obj_file_name}.rels"

    def gen_rels_path_from_identifier(self, identifier: str) -> Optional[str]:
        """Generate rels path from object identifier without loading the object."""
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
                logging.error(f"Failed to load core properties: {e}")

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

    def update_content_types_xml(
        self, source_zip: zipfile.ZipFile, metadata: EpcObjectMetadata, add: bool = True
    ) -> str:
        """Update [Content_Types].xml to add or remove object entry.
        
        Args:
            source_zip: Open ZIP file to read from
            metadata: Object metadata
            add: If True, add entry; if False, remove entry
            
        Returns:
            Updated [Content_Types].xml as string
        """
        # Read existing content types
        content_types = self._read_content_types(source_zip)

        if add:
            # Add new override entry
            new_override = Override()
            new_override.part_name = f"/{metadata.file_path}"
            new_override.content_type = metadata.content_type
            content_types.override.append(new_override)
        else:
            # Remove override entry
            content_types.override = [
                override for override in content_types.override if override.part_name != f"/{metadata.file_path}"
            ]

        # Serialize back to XML
        return serialize_xml(content_types)


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
        export_version: EpcExportVersion,
        rels_update_mode: RelsUpdateMode,
    ):
        """
        Initialize the relationship manager.

        Args:
            zip_accessor: ZIP file accessor for reading/writing
            metadata_manager: Metadata manager for object lookups
            stats: Statistics tracker
            export_version: EPC export version
            rels_update_mode: Relationship update mode
        """
        self.zip_accessor = zip_accessor
        self.metadata_manager = metadata_manager
        self.stats = stats
        self.export_version = export_version
        self.rels_update_mode = rels_update_mode

        # Additional rels management (for user-added relationships)
        self.additional_rels: Dict[str, List[Relationship]] = {}

    def get_obj_rels(self, obj_identifier: str, rels_path: Optional[str] = None) -> List[Relationship]:
        """
        Get all relationships for a given object.
        Merges relationships from the EPC file with in-memory additional relationships.
        """
        rels = []

        # Read rels from EPC file
        if rels_path is None:
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
        if obj_identifier in self.additional_rels:
            rels.extend(self.additional_rels[obj_identifier])

        return rels

    def update_rels_for_new_object(self, obj: Any, obj_identifier: str) -> None:
        """Update relationships when a new object is added (UPDATE_AT_MODIFICATION mode)."""
        metadata = self.metadata_manager.get_metadata(obj_identifier)
        if not metadata:
            logging.warning(f"Metadata not found for {obj_identifier}")
            return

        # Get all objects this new object references
        direct_dors = get_direct_dor_list(obj)

        # Build SOURCE relationships for this object
        source_relationships = []
        dest_updates: Dict[str, Relationship] = {}

        for dor in direct_dors:
            try:
                target_identifier = get_obj_identifier(dor)
                if not self.metadata_manager.contains(target_identifier):
                    continue

                target_metadata = self.metadata_manager.get_metadata(target_identifier)
                if not target_metadata:
                    continue

                # Create SOURCE relationship
                source_rel = Relationship(
                    target=target_metadata.file_path,
                    type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                    id=f"_{obj_identifier}_{get_obj_type(get_obj_usable_class(dor))}_{target_identifier}",
                )
                source_relationships.append(source_rel)

                # Create DESTINATION relationship
                dest_rel = Relationship(
                    target=metadata.file_path,
                    type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                    id=f"_{target_identifier}_{get_obj_type(get_obj_usable_class(obj))}_{obj_identifier}",
                )
                dest_updates[target_identifier] = dest_rel

            except Exception as e:
                logging.warning(f"Failed to create relationship for DOR: {e}")

        # Write updates
        self.write_rels_updates(obj_identifier, source_relationships, dest_updates)

    def update_rels_for_modified_object(self, obj: Any, obj_identifier: str, old_dors: List[Any]) -> None:
        """Update relationships when an object is modified (UPDATE_AT_MODIFICATION mode)."""
        metadata = self.metadata_manager.get_metadata(obj_identifier)
        if not metadata:
            logging.warning(f"Metadata not found for {obj_identifier}")
            return

        # Get new DORs
        new_dors = get_direct_dor_list(obj)

        # Convert to sets of identifiers for comparison
        old_dor_ids = {
            get_obj_identifier(dor) for dor in old_dors if self.metadata_manager.contains(get_obj_identifier(dor))
        }
        new_dor_ids = {
            get_obj_identifier(dor) for dor in new_dors if self.metadata_manager.contains(get_obj_identifier(dor))
        }

        # Find added and removed references
        added_dor_ids = new_dor_ids - old_dor_ids
        removed_dor_ids = old_dor_ids - new_dor_ids

        # Build new SOURCE relationships
        source_relationships = []
        dest_updates: Dict[str, Relationship] = {}

        # Create relationships for all new DORs
        for dor in new_dors:
            target_identifier = get_obj_identifier(dor)
            if not self.metadata_manager.contains(target_identifier):
                continue

            target_metadata = self.metadata_manager.get_metadata(target_identifier)
            if not target_metadata:
                continue

            # SOURCE relationship
            source_rel = Relationship(
                target=target_metadata.file_path,
                type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                id=f"_{obj_identifier}_{get_obj_type(get_obj_usable_class(dor))}_{target_identifier}",
            )
            source_relationships.append(source_rel)

            # DESTINATION relationship (for added DORs only)
            if target_identifier in added_dor_ids:
                dest_rel = Relationship(
                    target=metadata.file_path,
                    type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                    id=f"_{target_identifier}_{get_obj_type(get_obj_usable_class(obj))}_{obj_identifier}",
                )
                dest_updates[target_identifier] = dest_rel

        # For removed DORs, remove DESTINATION relationships
        removals: Dict[str, str] = {}
        for removed_id in removed_dor_ids:
            removals[removed_id] = f"_{removed_id}_.*_{obj_identifier}"

        # Write updates
        self.write_rels_updates(obj_identifier, source_relationships, dest_updates, removals)

    def update_rels_for_removed_object(self, obj_identifier: str, obj: Optional[Any] = None) -> None:
        """Update relationships when an object is removed (UPDATE_AT_MODIFICATION mode)."""
        if obj is None:
            # Object must be provided for removal
            logging.warning(f"Cannot update rels for removed object {obj_identifier}: object not provided")
            return

        # Get all objects this object references
        direct_dors = get_direct_dor_list(obj)

        # Build removal patterns for DESTINATION relationships
        removals: Dict[str, str] = {}
        for dor in direct_dors:
            try:
                target_identifier = get_obj_identifier(dor)
                if not self.metadata_manager.contains(target_identifier):
                    continue

                removals[target_identifier] = f"_{target_identifier}_.*_{obj_identifier}"

            except Exception as e:
                logging.warning(f"Failed to process DOR for removal: {e}")

        # Write updates
        self.write_rels_updates(obj_identifier, [], {}, removals, delete_source_rels=True)

    def write_rels_updates(
        self,
        source_identifier: str,
        source_relationships: List[Relationship],
        dest_updates: Dict[str, Relationship],
        removals: Optional[Dict[str, str]] = None,
        delete_source_rels: bool = False,
    ) -> None:
        """Write relationship updates to the EPC file efficiently."""
        import re

        removals = removals or {}
        rels_updates: Dict[str, str] = {}
        files_to_delete: List[str] = []

        with self.zip_accessor.get_zip_file() as zf:
            # 1. Handle source object's rels file
            if not delete_source_rels:
                source_rels_path = self.metadata_manager.gen_rels_path_from_identifier(source_identifier)
                if source_rels_path:
                    # Read existing rels (excluding SOURCE_OBJECT type)
                    existing_rels = []
                    try:
                        if source_rels_path in zf.namelist():
                            rels_data = zf.read(source_rels_path)
                            existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                            if existing_rels_obj and existing_rels_obj.relationship:
                                # Keep only non-SOURCE relationships
                                existing_rels = [
                                    r
                                    for r in existing_rels_obj.relationship
                                    if r.type_value != EPCRelsRelationshipType.SOURCE_OBJECT.get_type()
                                ]
                    except Exception:
                        pass

                    # Combine with new SOURCE relationships
                    all_rels = existing_rels + source_relationships
                    if all_rels:
                        rels_updates[source_rels_path] = serialize_xml(Relationships(relationship=all_rels))
                    elif source_rels_path in zf.namelist() and not all_rels:
                        files_to_delete.append(source_rels_path)
            else:
                # Mark source rels file for deletion
                source_rels_path = self.metadata_manager.gen_rels_path_from_identifier(source_identifier)
                if source_rels_path:
                    files_to_delete.append(source_rels_path)

            # 2. Handle destination updates
            for target_identifier, dest_rel in dest_updates.items():
                target_rels_path = self.metadata_manager.gen_rels_path_from_identifier(target_identifier)
                if not target_rels_path:
                    continue

                # Read existing rels
                existing_rels = []
                try:
                    if target_rels_path in zf.namelist():
                        rels_data = zf.read(target_rels_path)
                        existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                        if existing_rels_obj and existing_rels_obj.relationship:
                            existing_rels = list(existing_rels_obj.relationship)
                except Exception:
                    pass

                # Add new DESTINATION relationship if not already present
                rel_exists = any(
                    r.target == dest_rel.target and r.type_value == dest_rel.type_value for r in existing_rels
                )

                if not rel_exists:
                    existing_rels.append(dest_rel)
                    rels_updates[target_rels_path] = serialize_xml(Relationships(relationship=existing_rels))

            # 3. Handle removals
            for target_identifier, pattern in removals.items():
                target_rels_path = self.metadata_manager.gen_rels_path_from_identifier(target_identifier)
                if not target_rels_path:
                    continue

                # Read existing rels
                existing_rels = []
                try:
                    if target_rels_path in zf.namelist():
                        rels_data = zf.read(target_rels_path)
                        existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                        if existing_rels_obj and existing_rels_obj.relationship:
                            existing_rels = list(existing_rels_obj.relationship)
                except Exception:
                    pass

                # Filter out relationships matching the pattern
                regex = re.compile(pattern)
                filtered_rels = [r for r in existing_rels if not (r.id and regex.match(r.id))]

                if len(filtered_rels) != len(existing_rels):
                    if filtered_rels:
                        rels_updates[target_rels_path] = serialize_xml(Relationships(relationship=filtered_rels))
                    else:
                        files_to_delete.append(target_rels_path)

        # Write updates to EPC file
        if rels_updates or files_to_delete:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
                temp_path = temp_file.name

            try:
                with self.zip_accessor.get_zip_file() as source_zf:
                    with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zf:
                        # Copy all files except those to delete or update
                        files_to_skip = set(files_to_delete)
                        for item in source_zf.infolist():
                            if item.filename not in files_to_skip and item.filename not in rels_updates:
                                data = source_zf.read(item.filename)
                                target_zf.writestr(item, data)

                        # Write updated rels files
                        for rels_path, rels_xml in rels_updates.items():
                            target_zf.writestr(rels_path, rels_xml)

                # Replace original
                shutil.move(temp_path, self.zip_accessor.epc_file_path)
                self.zip_accessor.reopen_persistent_zip()

            except Exception as e:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                logging.error(f"Failed to write rels updates: {e}")
                raise

    def compute_object_rels(self, obj: Any, obj_identifier: str) -> List[Relationship]:
        """
        Compute relationships for a given object (SOURCE relationships).
        This object references other objects through DORs.

        Args:
            obj: The EnergyML object
            obj_identifier: The identifier of the object

        Returns:
            List of Relationship objects for this object's .rels file
        """
        rels = []

        # Get all DORs (Data Object References) in this object
        direct_dors = get_direct_dor_list(obj)

        for dor in direct_dors:
            try:
                target_identifier = get_obj_identifier(dor)

                # Get target file path from metadata without processing DOR
                # The relationship target should be the object's file path, not its rels path
                if self.metadata_manager.contains(target_identifier):
                    target_metadata = self.metadata_manager.get_metadata(target_identifier)
                    if target_metadata:
                        target_path = target_metadata.file_path
                    else:
                        target_path = gen_energyml_object_path(dor, self.export_version)
                else:
                    # Fall back to generating path from DOR if metadata not found
                    target_path = gen_energyml_object_path(dor, self.export_version)

                # Create SOURCE relationship (this object -> target object)
                rel = Relationship(
                    target=target_path,
                    type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                    id=f"_{obj_identifier}_{get_obj_type(get_obj_usable_class(dor))}_{target_identifier}",
                )
                rels.append(rel)
            except Exception as e:
                logging.warning(f"Failed to create relationship for DOR in {obj_identifier}: {e}")

        return rels

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


# ===========================================================================================
# MAIN CLASS (REFACTORED TO USE HELPER CLASSES)
# ===========================================================================================


class EpcStreamReader(EnergymlStorageInterface):
    """
    Memory-efficient EPC file reader with lazy loading and smart caching.

    This class provides the same interface as the standard Epc class but loads
    objects on-demand rather than keeping everything in memory. Perfect for
    handling very large EPC files with thousands of objects.

    Features:
    - Lazy loading: Objects loaded only when accessed
    - Smart caching: LRU cache with configurable size
    - Memory monitoring: Track memory usage and cache efficiency
    - Streaming validation: Validate objects without full loading
    - Batch operations: Efficient bulk operations
    - Context management: Automatic resource cleanup
    - Flexible relationship management: Three modes for updating object relationships

    Relationship Update Modes:
    - UPDATE_AT_MODIFICATION: Maintains relationships in real-time as objects are added/removed/modified.
                             Best for maintaining consistency but may be slower for bulk operations.
    - UPDATE_ON_CLOSE: Rebuilds all relationships when closing the EPC file (default).
                      More efficient for bulk operations but relationships only consistent after closing.
    - MANUAL: No automatic relationship updates. User must manually call rebuild_all_rels().
             Maximum control and performance for advanced use cases.

    Performance optimizations:
    - Pre-compiled regex patterns for 15-75% faster parsing
    - Weak references to prevent memory leaks
    - Compressed metadata storage
    - Efficient ZIP file handling
    """

    def __init__(
        self,
        epc_file_path: Union[str, Path],
        cache_size: int = 100,
        validate_on_load: bool = True,
        preload_metadata: bool = True,
        export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
        force_h5_path: Optional[str] = None,
        keep_open: bool = False,
        force_title_load: bool = False,
        rels_update_mode: RelsUpdateMode = RelsUpdateMode.UPDATE_ON_CLOSE,
    ):
        """
        Initialize the EPC stream reader.

        Args:
            epc_file_path: Path to the EPC file
            cache_size: Maximum number of objects to keep in memory cache
            validate_on_load: Whether to validate objects when loading
            preload_metadata: Whether to preload all object metadata
            export_version: EPC packaging version (CLASSIC or EXPANDED)
            force_h5_path: Optional forced HDF5 file path for external resources. If set, all arrays will be read/written from/to this path.
            keep_open: If True, keeps the ZIP file open for better performance with multiple operations. File is closed only when instance is deleted or close() is called.
            force_title_load: If True, forces loading object titles when listing objects (may impact performance)
            rels_update_mode: Mode for updating relationships (UPDATE_AT_MODIFICATION, UPDATE_ON_CLOSE, or MANUAL)
        """
        # Public attributes
        self.epc_file_path = Path(epc_file_path)
        self.cache_size = cache_size
        self.validate_on_load = validate_on_load
        self.force_h5_path = force_h5_path
        self.cache_opened_h5 = None
        self.keep_open = keep_open
        self.force_title_load = force_title_load
        self.rels_update_mode = rels_update_mode
        self.export_version: EpcExportVersion = export_version or EpcExportVersion.CLASSIC
        self.stats = EpcStreamingStats()

        # Caching system using weak references
        self._object_cache: WeakValueDictionary = WeakValueDictionary()
        self._access_order: List[str] = []  # LRU tracking

        is_new_file = False

        # Validate file exists and is readable
        if not self.epc_file_path.exists():
            logging.info(f"EPC file not found: {epc_file_path}. Creating a new empty EPC file.")
            self._create_empty_epc()
            is_new_file = True

        if not zipfile.is_zipfile(self.epc_file_path):
            raise ValueError(f"File is not a valid ZIP/EPC file: {epc_file_path}")

        # Check if the ZIP file has the required EPC structure
        if not is_new_file:
            try:
                with zipfile.ZipFile(self.epc_file_path, "r") as zf:
                    content_types_path = get_epc_content_type_path()
                    if content_types_path not in zf.namelist():
                        logging.info("EPC file is missing required structure. Initializing empty EPC file.")
                        self._create_empty_epc()
                        is_new_file = True
            except Exception as e:
                logging.warning(f"Failed to check EPC structure: {e}. Reinitializing.")

        # Initialize helper classes (internal architecture)
        self._zip_accessor = _ZipFileAccessor(self.epc_file_path, keep_open=keep_open)
        self._metadata_mgr = _MetadataManager(self._zip_accessor, self.stats)
        self._rels_mgr = _RelationshipManager(
            self._zip_accessor, self._metadata_mgr, self.stats, self.export_version, rels_update_mode
        )

        # Initialize by loading metadata
        if not is_new_file and preload_metadata:
            self._metadata_mgr.load_metadata()
            # Detect EPC version after loading metadata
            self.export_version = self._metadata_mgr.detect_epc_version()
            # Update relationship manager's export version
            self._rels_mgr.export_version = self.export_version

        # Open persistent ZIP connection if keep_open is enabled
        if keep_open and not is_new_file:
            self._zip_accessor.open_persistent_connection()

        # Backward compatibility: expose internal structures as properties
        # This allows existing code to access _metadata, _uuid_index, etc.
        self._metadata = self._metadata_mgr._metadata
        self._uuid_index = self._metadata_mgr._uuid_index
        self._type_index = self._metadata_mgr._type_index
        self.additional_rels = self._rels_mgr.additional_rels

    def _create_empty_epc(self) -> None:
        """Create an empty EPC file structure."""
        # Ensure directory exists
        self.epc_file_path.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(self.epc_file_path, "w") as zf:
            # Create [Content_Types].xml
            content_types = Types()
            content_types_xml = serialize_xml(content_types)
            zf.writestr(get_epc_content_type_path(), content_types_xml)

            # Create _rels/.rels
            rels = Relationships()
            rels_xml = serialize_xml(rels)
            zf.writestr("_rels/.rels", rels_xml)

    def _load_metadata(self) -> None:
        """Load object metadata from [Content_Types].xml without loading actual objects."""
        # Delegate to metadata manager
        self._metadata_mgr.load_metadata()

    def _read_content_types(self, zf: zipfile.ZipFile) -> Types:
        """Read and parse [Content_Types].xml file."""
        # Delegate to metadata manager
        return self._metadata_mgr._read_content_types(zf)

    def _process_energyml_object_metadata(self, zf: zipfile.ZipFile, override: Override) -> None:
        """Process metadata for an EnergyML object without loading it."""
        # Delegate to metadata manager
        self._metadata_mgr._process_energyml_object_metadata(zf, override)

    def _extract_object_info_fast(
        self, zf: zipfile.ZipFile, file_path: str, content_type: str
    ) -> Tuple[Optional[str], Optional[str], str]:
        """Fast extraction of UUID and version from XML without full parsing."""
        # Delegate to metadata manager
        return self._metadata_mgr._extract_object_info_fast(zf, file_path, content_type)

    def _extract_object_type_from_content_type(self, content_type: str) -> str:
        """Extract object type from content type string."""
        # Delegate to metadata manager
        return self._metadata_mgr._extract_object_type_from_content_type(content_type)

    def _is_core_properties(self, content_type: str) -> bool:
        """Check if content type is CoreProperties."""
        # Delegate to metadata manager
        return self._metadata_mgr._is_core_properties(content_type)

    def _process_core_properties_metadata(self, override: Override) -> None:
        """Process core properties metadata."""
        # Delegate to metadata manager
        self._metadata_mgr._process_core_properties_metadata(override)

    def _detect_epc_version(self) -> EpcExportVersion:
        """Detect EPC packaging version based on file structure."""
        # Delegate to metadata manager
        return self._metadata_mgr.detect_epc_version()

    def _gen_rels_path_from_metadata(self, metadata: EpcObjectMetadata) -> str:
        """Generate rels path from object metadata without loading the object."""
        # Delegate to metadata manager
        return self._metadata_mgr.gen_rels_path_from_metadata(metadata)

    def _gen_rels_path_from_identifier(self, identifier: str) -> Optional[str]:
        """Generate rels path from object identifier without loading the object."""
        # Delegate to metadata manager
        return self._metadata_mgr.gen_rels_path_from_identifier(identifier)

    @contextmanager
    def _get_zip_file(self) -> Iterator[zipfile.ZipFile]:
        """Context manager for ZIP file access with proper resource management.

        If keep_open is True, uses the persistent connection. Otherwise opens a new one.
        """
        # Delegate to the ZIP accessor helper class
        with self._zip_accessor.get_zip_file() as zf:
            yield zf

    def get_object_by_identifier(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """
        Get object by its identifier with smart caching.

        Args:
            identifier: Object identifier (uuid.version)

        Returns:
            The requested object or None if not found
        """
        is_uri = isinstance(identifier, Uri) or parse_uri(identifier) is not None
        if is_uri:
            uri = parse_uri(identifier) if isinstance(identifier, str) else identifier
            assert uri is not None and uri.uuid is not None
            identifier = uri.uuid + "." + (uri.version or "")

        # Check cache first
        if identifier in self._object_cache:
            self._update_access_order(identifier)  # type: ignore
            self.stats.cache_hits += 1
            return self._object_cache[identifier]

        self.stats.cache_misses += 1

        # Check if metadata exists
        if identifier not in self._metadata:
            return None

        # Load object from file
        obj = self._load_object(identifier)

        if obj is not None:
            # Add to cache with LRU management
            self._add_to_cache(identifier, obj)
            self.stats.loaded_objects += 1

        return obj

    def _load_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """Load object from EPC file."""
        is_uri = isinstance(identifier, Uri) or parse_uri(identifier) is not None
        if is_uri:
            uri = parse_uri(identifier) if isinstance(identifier, str) else identifier
            assert uri is not None and uri.uuid is not None
            identifier = uri.uuid + "." + (uri.version or "")
        assert isinstance(identifier, str)
        metadata = self._metadata.get(identifier)
        if not metadata:
            return None

        try:
            with self._get_zip_file() as zf:
                obj_data = zf.read(metadata.file_path)
                self.stats.bytes_read += len(obj_data)

                obj_class = get_class_from_content_type(metadata.content_type)
                obj = read_energyml_xml_bytes(obj_data, obj_class)

                if self.validate_on_load:
                    self._validate_object(obj, metadata)

                return obj

        except Exception as e:
            logging.error(f"Failed to load object {identifier}: {e}")
            return None

    def _validate_object(self, obj: Any, metadata: EpcObjectMetadata) -> None:
        """Validate loaded object against metadata."""
        try:
            obj_uuid = get_obj_uuid(obj)
            if obj_uuid != metadata.uuid:
                logging.warning(f"UUID mismatch for {metadata.identifier}: expected {metadata.uuid}, got {obj_uuid}")
        except Exception as e:
            logging.debug(f"Validation failed for {metadata.identifier}: {e}")

    def _add_to_cache(self, identifier: Union[str, Uri], obj: Any) -> None:
        """Add object to cache with LRU eviction."""
        is_uri = isinstance(identifier, Uri) or parse_uri(identifier) is not None
        if is_uri:
            uri = parse_uri(identifier) if isinstance(identifier, str) else identifier
            assert uri is not None and uri.uuid is not None
            identifier = uri.uuid + "." + (uri.version or "")

        assert isinstance(identifier, str)

        # Remove from access order if already present
        if identifier in self._access_order:
            self._access_order.remove(identifier)

        # Add to front (most recently used)
        self._access_order.insert(0, identifier)

        # Add to cache
        self._object_cache[identifier] = obj

        # Evict if cache is full
        while len(self._access_order) > self.cache_size:
            oldest = self._access_order.pop()
            self._object_cache.pop(oldest, None)

    def _update_access_order(self, identifier: str) -> None:
        """Update access order for LRU cache."""
        if identifier in self._access_order:
            self._access_order.remove(identifier)
            self._access_order.insert(0, identifier)

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """Get all objects with the specified UUID."""
        if uuid not in self._uuid_index:
            return []

        objects = []
        for identifier in self._uuid_index[uuid]:
            obj = self.get_object_by_identifier(identifier)
            if obj is not None:
                objects.append(obj)

        return objects

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        return self.get_object_by_identifier(identifier)

    def get_objects_by_type(self, object_type: str) -> List[Any]:
        """Get all objects of the specified type."""
        if object_type not in self._type_index:
            return []

        objects = []
        for identifier in self._type_index[object_type]:
            obj = self.get_object_by_identifier(identifier)
            if obj is not None:
                objects.append(obj)

        return objects

    def list_object_metadata(self, object_type: Optional[str] = None) -> List[EpcObjectMetadata]:
        """
        List metadata for objects without loading them.

        Args:
            object_type: Optional filter by object type

        Returns:
            List of object metadata
        """
        if object_type is None:
            return list(self._metadata.values())

        return [self._metadata[identifier] for identifier in self._type_index.get(object_type, [])]

    def get_statistics(self) -> EpcStreamingStats:
        """Get current streaming statistics."""
        return self.stats

    def list_objects(
        self, dataspace: Optional[str] = None, object_type: Optional[str] = None
    ) -> List[ResourceMetadata]:
        """
        List all objects with metadata (EnergymlStorageInterface method).

        Args:
            dataspace: Optional dataspace filter (ignored for EPC files)
            object_type: Optional type filter (qualified type)

        Returns:
            List of ResourceMetadata for all matching objects
        """

        results = []
        metadata_list = self.list_object_metadata(object_type)

        for meta in metadata_list:
            try:
                # Load object to get title
                title = ""
                if self.force_title_load and meta.identifier:
                    obj = self.get_object_by_identifier(meta.identifier)
                    if obj and hasattr(obj, "citation") and obj.citation:
                        if hasattr(obj.citation, "title"):
                            title = obj.citation.title

                # Build URI
                qualified_type = content_type_to_qualified_type(meta.content_type)
                if meta.version:
                    uri = f"eml:///{qualified_type}(uuid={meta.uuid},version='{meta.version}')"
                else:
                    uri = f"eml:///{qualified_type}({meta.uuid})"

                resource = ResourceMetadata(
                    uri=uri,
                    uuid=meta.uuid,
                    version=meta.version,
                    title=title,
                    object_type=meta.object_type,
                    content_type=meta.content_type,
                )

                results.append(resource)
            except Exception:
                continue

        return results

    def get_array_metadata(
        self, proxy: Union[str, Uri, Any], path_in_external: Optional[str] = None
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """
        Get metadata for data array(s) (EnergymlStorageInterface method).

        Args:
            proxy: The object identifier/URI or the object itself
            path_in_external: Optional specific path

        Returns:
            DataArrayMetadata if path specified, List[DataArrayMetadata] if no path,
            or None if not found
        """
        from energyml.utils.storage_interface import DataArrayMetadata

        try:
            if path_in_external:
                array = self.read_array(proxy, path_in_external)
                if array is not None:
                    return DataArrayMetadata(
                        path_in_resource=path_in_external,
                        array_type=str(array.dtype),
                        dimensions=list(array.shape),
                    )
            else:
                # Would need to scan all possible paths - not practical
                return []
        except Exception:
            pass

        return None

    def preload_objects(self, identifiers: List[str]) -> int:
        """
        Preload specific objects into cache.

        Args:
            identifiers: List of object identifiers to preload

        Returns:
            Number of objects successfully loaded
        """
        loaded_count = 0
        for identifier in identifiers:
            if self.get_object_by_identifier(identifier) is not None:
                loaded_count += 1
        return loaded_count

    def clear_cache(self) -> None:
        """Clear the object cache to free memory."""
        self._object_cache.clear()
        self._access_order.clear()
        self.stats.loaded_objects = 0

    def get_core_properties(self) -> Optional[CoreProperties]:
        """Get core properties (loaded lazily)."""
        # Delegate to metadata manager
        return self._metadata_mgr.get_core_properties()

    def _gen_rels_path_from_metadata(self, metadata: EpcObjectMetadata) -> str:
        """
        Generate rels path from object metadata without loading the object.

        Args:
            metadata: Object metadata containing file path information

        Returns:
            Path to the rels file for this object
        """
        obj_path = metadata.file_path
        # Extract folder and filename from the object path
        if "/" in obj_path:
            obj_folder = obj_path[: obj_path.rindex("/") + 1]
            obj_file_name = obj_path[obj_path.rindex("/") + 1 :]
        else:
            obj_folder = ""
            obj_file_name = obj_path

        return f"{obj_folder}_rels/{obj_file_name}.rels"

    def _gen_rels_path_from_identifier(self, identifier: str) -> Optional[str]:
        """
        Generate rels path from object identifier without loading the object.

        Args:
            identifier: Object identifier (uuid.version)

        Returns:
            Path to the rels file, or None if metadata not found
        """
        metadata = self._metadata.get(identifier)
        if metadata is None:
            return None
        return self._gen_rels_path_from_metadata(metadata)

    def _update_rels_for_new_object(self, obj: Any, obj_identifier: str) -> None:
        """Update relationships when a new object is added (UPDATE_AT_MODIFICATION mode)."""
        # Delegate to relationship manager
        self._rels_mgr.update_rels_for_new_object(obj, obj_identifier)

    def _update_rels_for_modified_object(self, obj: Any, obj_identifier: str, old_dors: List[Any]) -> None:
        """Update relationships when an object is modified (UPDATE_AT_MODIFICATION mode)."""
        # Delegate to relationship manager
        self._rels_mgr.update_rels_for_modified_object(obj, obj_identifier, old_dors)

    def _update_rels_for_removed_object(self, obj_identifier: str, obj: Optional[Any] = None) -> None:
        """Update relationships when an object is removed (UPDATE_AT_MODIFICATION mode)."""
        # Delegate to relationship manager
        self._rels_mgr.update_rels_for_removed_object(obj_identifier, obj)

    def _write_rels_updates(
        self,
        source_identifier: str,
        source_relationships: List[Relationship],
        dest_updates: Dict[str, Relationship],
        removals: Optional[Dict[str, str]] = None,
        delete_source_rels: bool = False,
    ) -> None:
        """Write relationship updates to the EPC file efficiently."""
        # Delegate to relationship manager
        self._rels_mgr.write_rels_updates(
            source_identifier, source_relationships, dest_updates, removals, delete_source_rels
        )

    def _reopen_persistent_zip(self) -> None:
        """Reopen persistent ZIP file after modifications to reflect changes."""
        # Delegate to ZIP accessor
        self._zip_accessor.reopen_persistent_zip()

    def to_epc(self, load_all: bool = False) -> Epc:
        """
        Convert to standard Epc instance.

        Args:
            load_all: Whether to load all objects into memory

        Returns:
            Standard Epc instance
        """
        epc = Epc()
        epc.epc_file_path = str(self.epc_file_path)
        core_props = self.get_core_properties()
        if core_props is not None:
            epc.core_props = core_props

        if load_all:
            # Load all objects
            for identifier in self._metadata:
                obj = self.get_object_by_identifier(identifier)
                if obj is not None:
                    epc.energyml_objects.append(obj)

        return epc

    def set_rels_update_mode(self, mode: RelsUpdateMode) -> None:
        """
        Change the relationship update mode.

        Args:
            mode: The new RelsUpdateMode to use

        Note:
            Changing from MANUAL or UPDATE_ON_CLOSE to UPDATE_AT_MODIFICATION
            may require calling rebuild_all_rels() first to ensure consistency.
        """

    def set_rels_update_mode(self, mode: RelsUpdateMode) -> None:
        """
        Change the relationship update mode.

        Args:
            mode: The new RelsUpdateMode to use

        Note:
            Changing from MANUAL or UPDATE_ON_CLOSE to UPDATE_AT_MODIFICATION
            may require calling rebuild_all_rels() first to ensure consistency.
        """
        if not isinstance(mode, RelsUpdateMode):
            raise ValueError(f"mode must be a RelsUpdateMode enum value, got {type(mode)}")

        old_mode = self.rels_update_mode
        self.rels_update_mode = mode
        # Also update the relationship manager
        self._rels_mgr.rels_update_mode = mode

        logging.info(f"Changed relationship update mode from {old_mode.value} to {mode.value}")

    def get_rels_update_mode(self) -> RelsUpdateMode:
        """
        Get the current relationship update mode.

        Returns:
            The current RelsUpdateMode
        """
        return self.rels_update_mode

    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        """
        Get all relationships for a given object.
        Merges relationships from the EPC file with in-memory additional relationships.

        Optimized to avoid loading the object when identifier/URI is provided.

        :param obj: the object or its identifier/URI
        :return: list of Relationship objects
        """
        # Get identifier without loading the object
        obj_identifier = None
        rels_path = None

        if isinstance(obj, (str, Uri)):
            # Convert URI to identifier if needed
            if isinstance(obj, Uri) or parse_uri(obj) is not None:
                uri = parse_uri(obj) if isinstance(obj, str) else obj
                assert uri is not None and uri.uuid is not None
                obj_identifier = uri.uuid + "." + (uri.version or "")
            else:
                obj_identifier = obj

            # Generate rels path from metadata without loading the object
            rels_path = self._gen_rels_path_from_identifier(obj_identifier)
        else:
            # We have the actual object
            obj_identifier = get_obj_identifier(obj)
            rels_path = gen_rels_path(obj, self.export_version)

        # Delegate to relationship manager
        return self._rels_mgr.get_obj_rels(obj_identifier, rels_path)

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

        obj_identifier = None
        rels_path = None

        # Get identifier and rels path without loading the object
        if isinstance(obj, (str, Uri)):
            # Convert URI to identifier if needed
            if isinstance(obj, Uri) or parse_uri(obj) is not None:
                uri = parse_uri(obj) if isinstance(obj, str) else obj
                assert uri is not None and uri.uuid is not None
                obj_identifier = uri.uuid + "." + (uri.version or "")
            else:
                obj_identifier = obj

            # Generate rels path from metadata without loading the object
            rels_path = self._gen_rels_path_from_identifier(obj_identifier)
        else:
            # We have the actual object
            obj_identifier = get_obj_identifier(obj)
            rels_path = gen_rels_path(obj, self.export_version)

        # Check in-memory additional rels first
        for rels in self.additional_rels.get(obj_identifier, []):
            if rels.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
                h5_paths.add(rels.target)

        # Also check rels from the EPC file
        if rels_path is not None:
            with self._get_zip_file() as zf:
                try:
                    rels_data = zf.read(rels_path)
                    self.stats.bytes_read += len(rels_data)
                    relationships = read_energyml_xml_bytes(rels_data, Relationships)
                    for rel in relationships.relationship:
                        if rel.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
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

    def read_array(self, proxy: Union[str, Uri, Any], path_in_external: str) -> Optional[np.ndarray]:
        """
        Read a dataset from the HDF5 file linked to the proxy object.
        :param proxy: the object or its identifier
        :param path_in_external: the path in the external HDF5 file
        :return: the dataset as a numpy array
        """
        # Resolve proxy to object

        h5_path = []
        if self.force_h5_path is not None:
            if self.cache_opened_h5 is None:
                self.cache_opened_h5 = h5py.File(self.force_h5_path, "a")
            h5_path = [self.cache_opened_h5]
        else:
            if isinstance(proxy, (str, Uri)):
                obj = self.get_object_by_identifier(proxy)
            else:
                obj = proxy

            h5_path = self.get_h5_file_paths(obj)

        h5_reader = HDF5FileReader()

        if h5_path is None or len(h5_path) == 0:
            raise ValueError("No HDF5 file paths found for the given proxy object.")
        else:
            for h5p in h5_path:
                # TODO: handle different type of files
                try:
                    return h5_reader.read_array(source=h5p, path_in_external_file=path_in_external)
                except Exception:
                    pass
                    # logging.error(f"Failed to read HDF5 dataset from {h5p}: {e}")

    def write_array(self, proxy: Union[str, Uri, Any], path_in_external: str, array: np.ndarray) -> bool:
        """
        Write a dataset to the HDF5 file linked to the proxy object.
        :param proxy: the object or its identifier
        :param path_in_external: the path in the external HDF5 file
        :param array: the numpy array to write

        return: True if successful
        """
        h5_path = []
        if self.force_h5_path is not None:
            if self.cache_opened_h5 is None:
                self.cache_opened_h5 = h5py.File(self.force_h5_path, "a")
            h5_path = [self.cache_opened_h5]
        else:
            if isinstance(proxy, (str, Uri)):
                obj = self.get_object_by_identifier(proxy)
            else:
                obj = proxy

            h5_path = self.get_h5_file_paths(obj)

        h5_writer = HDF5FileWriter()

        if h5_path is None or len(h5_path) == 0:
            raise ValueError("No HDF5 file paths found for the given proxy object.")
        else:
            for h5p in h5_path:
                try:
                    h5_writer.write_array(target=h5p, path_in_external_file=path_in_external, array=array)
                    return True
                except Exception as e:
                    logging.error(f"Failed to write HDF5 dataset to {h5p}: {e}")
        return False

    def validate_all_objects(self, fast_mode: bool = True) -> Dict[str, List[str]]:
        """
        Validate all objects in the EPC file.

        Args:
            fast_mode: If True, only validate metadata without loading full objects

        Returns:
            Dictionary with 'errors' and 'warnings' keys containing lists of issues
        """
        results = {"errors": [], "warnings": []}

        for identifier, metadata in self._metadata.items():
            try:
                if fast_mode:
                    # Quick validation - just check file exists and is readable
                    with self._get_zip_file() as zf:
                        try:
                            zf.getinfo(metadata.file_path)
                        except KeyError:
                            results["errors"].append(f"Missing file for object {identifier}: {metadata.file_path}")
                else:
                    # Full validation - load and validate object
                    obj = self.get_object_by_identifier(identifier)
                    if obj is None:
                        results["errors"].append(f"Failed to load object {identifier}")
                    else:
                        self._validate_object(obj, metadata)

            except Exception as e:
                results["errors"].append(f"Validation error for {identifier}: {e}")

        return results

    def get_object_dependencies(self, identifier: Union[str, Uri]) -> List[str]:
        """
        Get list of object identifiers that this object depends on.

        This would need to be implemented based on DOR analysis.
        """
        # Placeholder for dependency analysis
        # Would need to parse DORs in the object
        return []

    def __len__(self) -> int:
        """Return total number of objects in EPC."""
        return len(self._metadata)

    def __contains__(self, identifier: str) -> bool:
        """Check if object with identifier exists."""
        return identifier in self._metadata

    def __iter__(self) -> Iterator[str]:
        """Iterate over object identifiers."""
        return iter(self._metadata.keys())

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.clear_cache()
        self.close()
        if self.cache_opened_h5 is not None:
            try:
                self.cache_opened_h5.close()
            except Exception:
                pass
            self.cache_opened_h5 = None

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

    def close(self) -> None:
        """Close the persistent ZIP file if it's open, recomputing rels first if mode is UPDATE_ON_CLOSE."""
        # Recompute all relationships before closing if in UPDATE_ON_CLOSE mode
        if self.rels_update_mode == RelsUpdateMode.UPDATE_ON_CLOSE:
            try:
                self.rebuild_all_rels(clean_first=True)
                logging.info("Rebuilt all relationships on close (UPDATE_ON_CLOSE mode)")
            except Exception as e:
                logging.warning(f"Error rebuilding rels on close: {e}")

        # Delegate to ZIP accessor
        self._zip_accessor.close()

    def put_object(self, obj: Any, dataspace: Optional[str] = None) -> Optional[str]:
        """
        Store an energyml object (EnergymlStorageInterface method).

        Args:
            obj: The energyml object to store
            dataspace: Optional dataspace name (ignored for EPC files)

        Returns:
            The identifier of the stored object (UUID.version or UUID), or None on error
        """
        try:
            return self.add_object(obj, replace_if_exists=True)
        except Exception:
            return None

    def add_object(self, obj: Any, file_path: Optional[str] = None, replace_if_exists: bool = True) -> str:
        """
        Add a new object to the EPC file and update caches.

        Args:
            obj: The EnergyML object to add
            file_path: Optional custom file path, auto-generated if not provided
            replace_if_exists: If True, replace the object if it already exists. If False, raise ValueError.

        Returns:
            The identifier of the added object

        Raises:
            ValueError: If object is invalid or already exists (when replace_if_exists=False)
            RuntimeError: If file operations fail
        """
        identifier = None
        metadata = None

        try:
            # Extract object information
            identifier = get_obj_identifier(obj)
            uuid = identifier.split(".")[0] if identifier else None

            if not uuid:
                raise ValueError("Object must have a valid UUID")

            version = identifier[len(uuid) + 1 :] if identifier and "." in identifier else None
            # Ensure version is treated as a string, not an integer
            if version is not None and not isinstance(version, str):
                version = str(version)

            object_type = get_object_type_for_file_path_from_class(obj)

            if identifier in self._metadata:
                if replace_if_exists:
                    # Remove the existing object first
                    logging.info(f"Replacing existing object {identifier}")
                    self.remove_object(identifier)
                else:
                    raise ValueError(
                        f"Object with identifier {identifier} already exists. Use update_object() or set replace_if_exists=True."
                    )

            # Generate file path if not provided
            file_path = gen_energyml_object_path(obj, self.export_version)

            print(f"Generated file path: {file_path} for export version: {self.export_version}")

            # Determine content type based on object type
            content_type = get_obj_content_type(obj)

            # Create metadata
            metadata = EpcObjectMetadata(
                uuid=uuid,
                object_type=object_type,
                content_type=content_type,
                file_path=file_path,
                version=version,
                identifier=identifier,
            )

            # Update internal structures
            self._metadata[identifier] = metadata

            # Update UUID index
            if uuid not in self._uuid_index:
                self._uuid_index[uuid] = []
            self._uuid_index[uuid].append(identifier)

            # Update type index
            if object_type not in self._type_index:
                self._type_index[object_type] = []
            self._type_index[object_type].append(identifier)

            # Add to cache
            self._add_to_cache(identifier, obj)

            # Save changes to file
            self._add_object_to_file(obj, metadata)

            # Update relationships if in UPDATE_AT_MODIFICATION mode
            if self.rels_update_mode == RelsUpdateMode.UPDATE_AT_MODIFICATION:
                self._update_rels_for_new_object(obj, identifier)

            # Update stats
            self.stats.total_objects += 1

            logging.info(f"Added object {identifier} to EPC file")
            return identifier

        except Exception as e:
            logging.error(f"Failed to add object: {e}")
            # Rollback changes if we created metadata
            if identifier and metadata:
                self._rollback_add_object(identifier)
            raise RuntimeError(f"Failed to add object to EPC: {e}")

    def delete_object(self, identifier: Union[str, Uri]) -> bool:
        """
        Delete an object by its identifier (EnergymlStorageInterface method).

        Args:
            identifier: Object identifier (UUID or UUID.version) or ETP URI

        Returns:
            True if successfully deleted, False otherwise
        """
        return self.remove_object(identifier)

    def remove_object(self, identifier: Union[str, Uri]) -> bool:
        """
        Remove an object (or all versions of an object) from the EPC file and update caches.

        Args:
            identifier: The identifier of the object to remove. Can be either:
                       - Full identifier (uuid.version) to remove a specific version
                       - UUID only to remove ALL versions of that object

        Returns:
            True if object(s) were successfully removed, False if not found

        Raises:
            RuntimeError: If file operations fail
        """
        try:
            is_uri = isinstance(identifier, Uri) or parse_uri(identifier) is not None
            if is_uri:
                uri = parse_uri(identifier) if isinstance(identifier, str) else identifier
                assert uri is not None and uri.uuid is not None
                identifier = uri.uuid + "." + (uri.version or "")
            assert isinstance(identifier, str)

            if identifier not in self._metadata:
                # Check if identifier is a UUID only (should remove all versions)
                if identifier in self._uuid_index:
                    # Remove all versions for this UUID
                    identifiers_to_remove = self._uuid_index[identifier].copy()
                    removed_count = 0

                    for id_to_remove in identifiers_to_remove:
                        if self._remove_single_object(id_to_remove):
                            removed_count += 1

                    return removed_count > 0
                else:
                    return False

            # Single identifier removal
            return self._remove_single_object(identifier)

        except Exception as e:
            logging.error(f"Failed to remove object {identifier}: {e}")
            raise RuntimeError(f"Failed to remove object from EPC: {e}")

    def _remove_single_object(self, identifier: str) -> bool:
        """
        Remove a single object by its full identifier.

        Args:
            identifier: The full identifier (uuid.version) of the object to remove
        Returns:
            True if the object was successfully removed, False otherwise
        """
        try:
            if identifier not in self._metadata:
                return False

            metadata = self._metadata[identifier]

            # If in UPDATE_AT_MODIFICATION mode, update rels before removing
            obj = None
            if self.rels_update_mode == RelsUpdateMode.UPDATE_AT_MODIFICATION:
                obj = self.get_object_by_identifier(identifier)
                if obj:
                    self._update_rels_for_removed_object(identifier, obj)

            # IMPORTANT: Remove from file FIRST (before clearing cache/metadata)
            # because _remove_object_from_file needs to load the object to access its DORs
            self._remove_object_from_file(metadata)

            # Now remove from cache
            if identifier in self._object_cache:
                del self._object_cache[identifier]

            if identifier in self._access_order:
                self._access_order.remove(identifier)

            # Remove from indexes
            uuid = metadata.uuid
            object_type = metadata.object_type

            if uuid in self._uuid_index:
                if identifier in self._uuid_index[uuid]:
                    self._uuid_index[uuid].remove(identifier)
                if not self._uuid_index[uuid]:
                    del self._uuid_index[uuid]

            if object_type in self._type_index:
                if identifier in self._type_index[object_type]:
                    self._type_index[object_type].remove(identifier)
                if not self._type_index[object_type]:
                    del self._type_index[object_type]

            # Remove from metadata (do this last)
            del self._metadata[identifier]

            # Update stats
            self.stats.total_objects -= 1
            if self.stats.loaded_objects > 0:
                self.stats.loaded_objects -= 1

            logging.info(f"Removed object {identifier} from EPC file")
            return True

        except Exception as e:
            logging.error(f"Failed to remove single object {identifier}: {e}")
            return False

    def update_object(self, obj: Any) -> str:
        """
        Update an existing object in the EPC file.

        Args:
            obj: The EnergyML object to update
        Returns:
            The identifier of the updated object
        """
        identifier = get_obj_identifier(obj)
        if not identifier or identifier not in self._metadata:
            raise ValueError("Object must have a valid identifier and exist in the EPC file")

        try:
            # If in UPDATE_AT_MODIFICATION mode, get old DORs and handle update differently
            if self.rels_update_mode == RelsUpdateMode.UPDATE_AT_MODIFICATION:
                old_obj = self.get_object_by_identifier(identifier)
                old_dors = get_direct_dor_list(old_obj) if old_obj else []

                # Preserve non-SOURCE/DESTINATION relationships (like EXTERNAL_RESOURCE) before removal
                preserved_rels = []
                try:
                    obj_rels = self.get_obj_rels(identifier)
                    preserved_rels = [
                        r
                        for r in obj_rels
                        if r.type_value
                        not in (
                            EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                            EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                        )
                    ]
                except Exception:
                    pass

                # Remove existing object (without rels update since we're replacing it)
                # Temporarily switch to MANUAL mode to avoid double updates
                original_mode = self.rels_update_mode
                self.rels_update_mode = RelsUpdateMode.MANUAL
                self.remove_object(identifier)
                self.rels_update_mode = original_mode

                # Add updated object (without rels update since we'll do custom update)
                self.rels_update_mode = RelsUpdateMode.MANUAL
                new_identifier = self.add_object(obj)
                self.rels_update_mode = original_mode

                # Now do the specialized update that handles both adds and removes
                self._update_rels_for_modified_object(obj, new_identifier, old_dors)

                # Restore preserved relationships (like EXTERNAL_RESOURCE)
                if preserved_rels:
                    # These need to be written directly to the rels file
                    # since _update_rels_for_modified_object already wrote it
                    rels_path = self._gen_rels_path_from_identifier(new_identifier)
                    if rels_path:
                        with self._get_zip_file() as zf:
                            # Read current rels
                            current_rels = []
                            try:
                                if rels_path in zf.namelist():
                                    rels_data = zf.read(rels_path)
                                    rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                                    if rels_obj and rels_obj.relationship:
                                        current_rels = list(rels_obj.relationship)
                            except Exception:
                                pass

                            # Add preserved rels
                            all_rels = current_rels + preserved_rels

                            # Write back
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
                                temp_path = temp_file.name

                            try:
                                with self._get_zip_file() as source_zf:
                                    with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zf:
                                        # Copy all files except the rels file we're updating
                                        for item in source_zf.infolist():
                                            if item.filename != rels_path:
                                                buffer = source_zf.read(item.filename)
                                                target_zf.writestr(item, buffer)

                                        # Write updated rels file
                                        target_zf.writestr(
                                            rels_path, serialize_xml(Relationships(relationship=all_rels))
                                        )

                                # Replace original
                                shutil.move(temp_path, self.epc_file_path)
                                self._reopen_persistent_zip()

                            except Exception:
                                if os.path.exists(temp_path):
                                    os.unlink(temp_path)
                                raise

            else:
                # For other modes (UPDATE_ON_CLOSE, MANUAL), preserve non-SOURCE/DESTINATION relationships
                preserved_rels = []
                try:
                    obj_rels = self.get_obj_rels(identifier)
                    preserved_rels = [
                        r
                        for r in obj_rels
                        if r.type_value
                        not in (
                            EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                            EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                        )
                    ]
                except Exception:
                    pass

                # Simple remove + add
                self.remove_object(identifier)
                new_identifier = self.add_object(obj)

                # Restore preserved relationships if any
                if preserved_rels:
                    self.add_rels_for_object(new_identifier, preserved_rels, write_immediately=True)

            logging.info(f"Updated object {identifier} to {new_identifier} in EPC file")
            return new_identifier

        except Exception as e:
            logging.error(f"Failed to update object {identifier}: {e}")
            raise RuntimeError(f"Failed to update object in EPC: {e}")

    def add_rels_for_object(
        self, identifier: Union[str, Uri, Any], relationships: List[Relationship], write_immediately: bool = False
    ) -> None:
        """
        Add additional relationships for a specific object.

        Relationships are stored in memory and can be written immediately or deferred
        until write_pending_rels() is called, or when the EPC is closed.

        Args:
            identifier: The identifier of the object, can be str, Uri, or the object itself
            relationships: List of Relationship objects to add
            write_immediately: If True, writes pending rels to disk immediately after adding.
                             If False (default), rels are kept in memory for batching.
        """
        is_uri = isinstance(identifier, Uri) or (isinstance(identifier, str) and parse_uri(identifier) is not None)
        if is_uri:
            uri = parse_uri(identifier) if isinstance(identifier, str) else identifier
            assert uri is not None and uri.uuid is not None
            identifier = uri.uuid + "." + (uri.version or "")
        elif not isinstance(identifier, str):
            identifier = get_obj_identifier(identifier)

        assert isinstance(identifier, str)

        if identifier not in self.additional_rels:
            self.additional_rels[identifier] = []

        self.additional_rels[identifier].extend(relationships)
        logging.debug(f"Added {len(relationships)} relationships for object {identifier} (in-memory)")

        if write_immediately:
            self.write_pending_rels()

    def write_pending_rels(self) -> int:
        """
        Write all pending in-memory relationships to the EPC file efficiently.

        This method reads existing rels, merges them in memory with pending rels,
        then rewrites only the affected rels files in a single ZIP update.

        Returns:
            Number of rels files updated
        """
        if not self.additional_rels:
            logging.debug("No pending relationships to write")
            return 0

        updated_count = 0

        # Step 1: Read existing rels and merge with pending rels in memory
        merged_rels: Dict[str, Relationships] = {}  # rels_path -> merged Relationships

        with self._get_zip_file() as zf:
            for obj_identifier, new_relationships in self.additional_rels.items():
                # Generate rels path from metadata without loading the object
                rels_path = self._gen_rels_path_from_identifier(obj_identifier)
                if rels_path is None:
                    logging.warning(f"Could not generate rels path for {obj_identifier}")
                    continue

                # Read existing rels from ZIP
                existing_relationships = []
                try:
                    if rels_path in zf.namelist():
                        rels_data = zf.read(rels_path)
                        existing_rels = read_energyml_xml_bytes(rels_data, Relationships)
                        if existing_rels and existing_rels.relationship:
                            existing_relationships = list(existing_rels.relationship)
                except Exception as e:
                    logging.debug(f"Could not read existing rels for {rels_path}: {e}")

                # Merge new relationships, avoiding duplicates
                for new_rel in new_relationships:
                    # Check if relationship already exists
                    rel_exists = any(
                        r.target == new_rel.target and r.type_value == new_rel.type_value
                        for r in existing_relationships
                    )

                    if not rel_exists:
                        # Ensure unique ID
                        cpt = 0
                        new_rel_id = new_rel.id
                        while any(r.id == new_rel_id for r in existing_relationships):
                            new_rel_id = f"{new_rel.id}_{cpt}"
                            cpt += 1
                        if new_rel_id != new_rel.id:
                            new_rel.id = new_rel_id

                        existing_relationships.append(new_rel)

                # Store merged result
                if existing_relationships:
                    merged_rels[rels_path] = Relationships(relationship=existing_relationships)

        # Step 2: Write updated rels back to ZIP (create temp, copy all, replace)
        if not merged_rels:
            return 0

        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            # Copy entire ZIP, replacing only the updated rels files
            with self._get_zip_file() as source_zf:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zf:
                    # Copy all files except the rels we're updating
                    for item in source_zf.infolist():
                        if item.filename not in merged_rels:
                            buffer = source_zf.read(item.filename)
                            target_zf.writestr(item, buffer)

                    # Write updated rels files
                    for rels_path, relationships in merged_rels.items():
                        rels_xml = serialize_xml(relationships)
                        target_zf.writestr(rels_path, rels_xml)
                        updated_count += 1

            # Replace original with updated ZIP
            shutil.move(temp_path, self.epc_file_path)
            self._reopen_persistent_zip()

            # Clear pending rels after successful write
            self.additional_rels.clear()

            logging.info(f"Wrote {updated_count} rels files to EPC")
            return updated_count

        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            logging.error(f"Failed to write pending rels: {e}")
            raise

    def _compute_object_rels(self, obj: Any, obj_identifier: str) -> List[Relationship]:
        """Compute relationships for a given object (SOURCE relationships).
        
        Delegates to _rels_mgr.compute_object_rels()
        """
        return self._rels_mgr.compute_object_rels(obj, obj_identifier)

    def _merge_rels(self, new_rels: List[Relationship], existing_rels: List[Relationship]) -> List[Relationship]:
        """Merge new relationships with existing ones, avoiding duplicates and ensuring unique IDs.

        Delegates to _rels_mgr.merge_rels()
        """
        return self._rels_mgr.merge_rels(new_rels, existing_rels)

    def _add_object_to_file(self, obj: Any, metadata: EpcObjectMetadata) -> None:
        """Add object to the EPC file efficiently.

        Reads existing rels, computes updates in memory, then writes everything
        in a single ZIP operation.
        """
        xml_content = serialize_xml(obj)
        obj_identifier = metadata.identifier
        assert obj_identifier is not None, "Object identifier must not be None"

        # Step 1: Compute which rels files need to be updated and prepare their content
        rels_updates: Dict[str, str] = {}  # rels_path -> XML content

        with self._get_zip_file() as zf:
            # 1a. Object's own .rels file
            obj_rels_path = gen_rels_path(obj, self.export_version)
            obj_relationships = self._compute_object_rels(obj, obj_identifier)

            if obj_relationships:
                # Read existing rels
                existing_rels = []
                try:
                    if obj_rels_path in zf.namelist():
                        rels_data = zf.read(obj_rels_path)
                        existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                        if existing_rels_obj and existing_rels_obj.relationship:
                            existing_rels = list(existing_rels_obj.relationship)
                except Exception:
                    pass

                # Merge and serialize
                merged_rels = self._merge_rels(obj_relationships, existing_rels)
                if merged_rels:
                    rels_updates[obj_rels_path] = serialize_xml(Relationships(relationship=merged_rels))

            # 1b. Update rels of referenced objects (DESTINATION relationships)
            direct_dors = get_direct_dor_list(obj)
            for dor in direct_dors:
                try:
                    target_identifier = get_obj_identifier(dor)

                    # Generate rels path from metadata without processing DOR
                    target_rels_path = self._gen_rels_path_from_identifier(target_identifier)
                    if target_rels_path is None:
                        # Fall back to generating from DOR if metadata not found
                        target_rels_path = gen_rels_path(dor, self.export_version)

                    # Create DESTINATION relationship
                    dest_rel = Relationship(
                        target=metadata.file_path,
                        type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                        id=f"_{target_identifier}_{get_obj_type(get_obj_usable_class(obj))}_{obj_identifier}",
                    )

                    # Read existing rels
                    existing_rels = []
                    try:
                        if target_rels_path in zf.namelist():
                            rels_data = zf.read(target_rels_path)
                            existing_rels_obj = read_energyml_xml_bytes(rels_data, Relationships)
                            if existing_rels_obj and existing_rels_obj.relationship:
                                existing_rels = list(existing_rels_obj.relationship)
                    except Exception:
                        pass

                    # Merge and serialize
                    merged_rels = self._merge_rels([dest_rel], existing_rels)
                    if merged_rels:
                        rels_updates[target_rels_path] = serialize_xml(Relationships(relationship=merged_rels))

                except Exception as e:
                    logging.warning(f"Failed to prepare rels update for referenced object: {e}")

            # 1c. Update [Content_Types].xml
            content_types_xml = self._update_content_types_xml(zf, metadata, add=True)

        # Step 2: Write everything to new ZIP
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with self._get_zip_file() as source_zf:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zf:
                    # Write new object
                    target_zf.writestr(metadata.file_path, xml_content)

                    # Write updated [Content_Types].xml
                    target_zf.writestr(get_epc_content_type_path(), content_types_xml)

                    # Write updated rels files
                    for rels_path, rels_xml in rels_updates.items():
                        target_zf.writestr(rels_path, rels_xml)

                    # Copy all other files
                    files_to_skip = {get_epc_content_type_path(), metadata.file_path}
                    files_to_skip.update(rels_updates.keys())

                    for item in source_zf.infolist():
                        if item.filename not in files_to_skip:
                            buffer = source_zf.read(item.filename)
                            target_zf.writestr(item, buffer)

            # Replace original
            shutil.move(temp_path, self.epc_file_path)
            self._reopen_persistent_zip()

        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            logging.error(f"Failed to add object to EPC file: {e}")
            raise

    def _remove_object_from_file(self, metadata: EpcObjectMetadata) -> None:
        """Remove object from the EPC file efficiently.

        Reads existing rels, computes updates in memory, then writes everything
        in a single ZIP operation. Note: This does NOT remove .rels files.
        Use clean_rels() to remove orphaned relationships.
        """
        # Load object first (needed to process its DORs)
        if metadata.identifier is None:
            logging.error("Cannot remove object with None identifier")
            raise ValueError("Object identifier must not be None")

        obj = self.get_object_by_identifier(metadata.identifier)
        if obj is None:
            logging.warning(f"Object {metadata.identifier} not found, cannot remove rels")
            # Still proceed with removal even if object can't be loaded

        # Step 1: Compute rels updates (remove DESTINATION relationships from referenced objects)
        rels_updates: Dict[str, str] = {}  # rels_path -> XML content

        if obj is not None:
            with self._get_zip_file() as zf:
                direct_dors = get_direct_dor_list(obj)

                for dor in direct_dors:
                    try:
                        target_identifier = get_obj_identifier(dor)
                        if target_identifier not in self._metadata:
                            continue

                        # Use metadata to generate rels path without loading the object
                        target_rels_path = self._gen_rels_path_from_identifier(target_identifier)
                        if target_rels_path is None:
                            continue

                        # Read existing rels
                        existing_relationships = []
                        try:
                            if target_rels_path in zf.namelist():
                                rels_data = zf.read(target_rels_path)
                                existing_rels = read_energyml_xml_bytes(rels_data, Relationships)
                                if existing_rels and existing_rels.relationship:
                                    existing_relationships = list(existing_rels.relationship)
                        except Exception as e:
                            logging.debug(f"Could not read existing rels for {target_identifier}: {e}")

                        # Remove DESTINATION relationship that pointed to our object
                        updated_relationships = [
                            r
                            for r in existing_relationships
                            if not (
                                r.target == metadata.file_path
                                and r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()
                            )
                        ]

                        # Only update if relationships remain
                        if updated_relationships:
                            rels_updates[target_rels_path] = serialize_xml(
                                Relationships(relationship=updated_relationships)
                            )

                    except Exception as e:
                        logging.warning(f"Failed to update rels for referenced object during removal: {e}")

                # Update [Content_Types].xml
                content_types_xml = self._update_content_types_xml(zf, metadata, add=False)
        else:
            # If we couldn't load the object, still update content types
            with self._get_zip_file() as zf:
                content_types_xml = self._update_content_types_xml(zf, metadata, add=False)

        # Step 2: Write everything to new ZIP
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with self._get_zip_file() as source_zf:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zf:
                    # Write updated [Content_Types].xml
                    target_zf.writestr(get_epc_content_type_path(), content_types_xml)

                    # Write updated rels files
                    for rels_path, rels_xml in rels_updates.items():
                        target_zf.writestr(rels_path, rels_xml)

                    # Copy all files except removed object, its rels, and files we're updating
                    obj_rels_path = self._gen_rels_path_from_metadata(metadata)
                    files_to_skip = {get_epc_content_type_path(), metadata.file_path}
                    if obj_rels_path:
                        files_to_skip.add(obj_rels_path)
                    files_to_skip.update(rels_updates.keys())

                    for item in source_zf.infolist():
                        if item.filename not in files_to_skip:
                            buffer = source_zf.read(item.filename)
                            target_zf.writestr(item, buffer)

            # Replace original
            shutil.move(temp_path, self.epc_file_path)
            self._reopen_persistent_zip()

        except Exception as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            logging.error(f"Failed to remove object from EPC file: {e}")
            raise

    def _update_content_types_xml(
        self, source_zip: zipfile.ZipFile, metadata: EpcObjectMetadata, add: bool = True
    ) -> str:
        """Update [Content_Types].xml to add or remove object entry.
        
        Delegates to _metadata_mgr.update_content_types_xml()
        """
        return self._metadata_mgr.update_content_types_xml(source_zip, metadata, add)

    def _rollback_add_object(self, identifier: Optional[str]) -> None:
        """Rollback changes made during failed add_object operation."""
        if identifier and identifier in self._metadata:
            metadata = self._metadata[identifier]

            # Remove from metadata
            del self._metadata[identifier]

            # Remove from indexes
            uuid = metadata.uuid
            object_type = metadata.object_type

            if uuid in self._uuid_index and identifier in self._uuid_index[uuid]:
                self._uuid_index[uuid].remove(identifier)
                if not self._uuid_index[uuid]:
                    del self._uuid_index[uuid]

            if object_type in self._type_index and identifier in self._type_index[object_type]:
                self._type_index[object_type].remove(identifier)
                if not self._type_index[object_type]:
                    del self._type_index[object_type]

            # Remove from cache
            if identifier in self._object_cache:
                del self._object_cache[identifier]
            if identifier in self._access_order:
                self._access_order.remove(identifier)

    def clean_rels(self) -> Dict[str, int]:
        """
        Clean all .rels files by removing relationships to objects that no longer exist.

        This method:
        1. Scans all .rels files in the EPC
        2. For each relationship, checks if the target object exists
        3. Removes relationships pointing to non-existent objects
        4. Removes empty .rels files

        Returns:
            Dictionary with statistics:
            - 'rels_files_scanned': Number of .rels files examined
            - 'relationships_removed': Number of orphaned relationships removed
            - 'rels_files_removed': Number of empty .rels files removed
        """
        import tempfile
        import shutil

        stats = {
            "rels_files_scanned": 0,
            "relationships_removed": 0,
            "rels_files_removed": 0,
        }

        # Create temporary file for updated EPC
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with self._get_zip_file() as source_zip:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zip:
                    # Get all existing object file paths for validation
                    existing_object_files = {metadata.file_path for metadata in self._metadata.values()}

                    # Process each file
                    for item in source_zip.infolist():
                        if item.filename.endswith(".rels"):
                            # Process .rels file
                            stats["rels_files_scanned"] += 1

                            try:
                                rels_data = source_zip.read(item.filename)
                                rels_obj = read_energyml_xml_bytes(rels_data, Relationships)

                                if rels_obj and rels_obj.relationship:
                                    # Filter out relationships to non-existent objects
                                    original_count = len(rels_obj.relationship)

                                    # Keep only relationships where the target exists
                                    # or where the target is external (starts with ../ or http)
                                    valid_relationships = []
                                    for rel in rels_obj.relationship:
                                        target = rel.target
                                        # Keep external references (HDF5, etc.) and existing objects
                                        if (
                                            target.startswith("../")
                                            or target.startswith("http")
                                            or target in existing_object_files
                                            or target.lstrip("/")
                                            in existing_object_files  # Also check without leading slash
                                        ):
                                            valid_relationships.append(rel)

                                    removed_count = original_count - len(valid_relationships)
                                    stats["relationships_removed"] += removed_count

                                    if removed_count > 0:
                                        logging.info(
                                            f"Removed {removed_count} orphaned relationships from {item.filename}"
                                        )

                                    # Only write the .rels file if it has remaining relationships
                                    if valid_relationships:
                                        rels_obj.relationship = valid_relationships
                                        updated_rels = serialize_xml(rels_obj)
                                        target_zip.writestr(item.filename, updated_rels)
                                    else:
                                        # Empty .rels file, don't write it
                                        stats["rels_files_removed"] += 1
                                        logging.info(f"Removed empty .rels file: {item.filename}")
                                else:
                                    # Empty or invalid .rels, don't copy it
                                    stats["rels_files_removed"] += 1

                            except Exception as e:
                                logging.warning(f"Failed to process .rels file {item.filename}: {e}")
                                # Copy as-is on error
                                data = source_zip.read(item.filename)
                                target_zip.writestr(item, data)

                        else:
                            # Copy non-.rels files as-is
                            data = source_zip.read(item.filename)
                            target_zip.writestr(item, data)

            # Replace original file
            shutil.move(temp_path, self.epc_file_path)

            logging.info(
                f"Cleaned .rels files: scanned {stats['rels_files_scanned']}, "
                f"removed {stats['relationships_removed']} orphaned relationships, "
                f"removed {stats['rels_files_removed']} empty .rels files"
            )

            return stats

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise RuntimeError(f"Failed to clean .rels files: {e}")

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
                obj = self.get_object_by_identifier(identifier)
                if obj is None:
                    continue

                stats["objects_processed"] += 1

                # Get all DORs in this object
                dors = get_direct_dor_list(obj)

                for dor in dors:
                    try:
                        target_identifier = get_obj_identifier(dor)
                        if target_identifier in self._metadata:
                            # Record this reference
                            if target_identifier not in reverse_references:
                                reverse_references[target_identifier] = []
                            reverse_references[target_identifier].append((identifier, obj))
                    except Exception:
                        pass

            except Exception as e:
                logging.warning(f"Failed to analyze object {identifier}: {e}")

        # Second pass: create the .rels files
        # Map of rels_file_path -> Relationships object
        rels_files: Dict[str, Relationships] = {}

        # Process each object to create SOURCE relationships
        for identifier in self._metadata:
            try:
                obj = self.get_object_by_identifier(identifier)
                if obj is None:
                    continue

                # metadata = self._metadata[identifier]
                obj_rels_path = self._gen_rels_path_from_identifier(identifier)

                # Get all DORs (objects this object references)
                dors = get_direct_dor_list(obj)

                if dors:
                    # Create SOURCE relationships
                    relationships = []

                    for dor in dors:
                        try:
                            target_identifier = get_obj_identifier(dor)
                            if target_identifier in self._metadata:
                                target_metadata = self._metadata[target_identifier]

                                rel = Relationship(
                                    target=target_metadata.file_path,
                                    type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                                    id=f"_{identifier}_{get_obj_type(get_obj_usable_class(dor))}_{target_identifier}",
                                )
                                relationships.append(rel)
                                stats["source_relationships"] += 1

                        except Exception as e:
                            logging.debug(f"Failed to create SOURCE relationship: {e}")

                    if relationships and obj_rels_path:
                        if obj_rels_path not in rels_files:
                            rels_files[obj_rels_path] = Relationships(relationship=[])
                        rels_files[obj_rels_path].relationship.extend(relationships)

            except Exception as e:
                logging.warning(f"Failed to create SOURCE rels for {identifier}: {e}")

        # Add DESTINATION relationships
        for target_identifier, source_list in reverse_references.items():
            try:
                if target_identifier not in self._metadata:
                    continue

                target_metadata = self._metadata[target_identifier]
                target_rels_path = self._gen_rels_path_from_identifier(target_identifier)

                if not target_rels_path:
                    continue

                # Create DESTINATION relationships for each object that references this one
                for source_identifier, source_obj in source_list:
                    try:
                        source_metadata = self._metadata[source_identifier]

                        rel = Relationship(
                            target=source_metadata.file_path,
                            type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                            id=f"_{target_identifier}_{get_obj_type(get_obj_usable_class(source_obj))}_{source_identifier}",
                        )

                        if target_rels_path not in rels_files:
                            rels_files[target_rels_path] = Relationships(relationship=[])
                        rels_files[target_rels_path].relationship.append(rel)
                        stats["destination_relationships"] += 1

                    except Exception as e:
                        logging.debug(f"Failed to create DESTINATION relationship: {e}")

            except Exception as e:
                logging.warning(f"Failed to create DESTINATION rels for {target_identifier}: {e}")

        stats["rels_files_created"] = len(rels_files)

        # Before writing, preserve EXTERNAL_RESOURCE and other non-SOURCE/DESTINATION relationships
        # This includes rels files that may not be in rels_files yet
        with self._get_zip_file() as zf:
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
            with self._get_zip_file() as source_zip:
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
            self._reopen_persistent_zip()

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

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"EpcStreamReader(path='{self.epc_file_path}', "
            f"objects={len(self._metadata)}, "
            f"cached={len(self._object_cache)}, "
            f"cache_hit_rate={self.stats.cache_hit_rate:.1f}%)"
        )

    def dumps_epc_content_and_files_lists(self):
        """Dump EPC content and files lists for debugging."""
        content_list = []
        file_list = []

        with self._get_zip_file() as zf:
            file_list = zf.namelist()

            for item in zf.infolist():
                content_list.append(f"{item.filename} - {item.file_size} bytes")

        return {
            "content_list": sorted(content_list),
            "file_list": sorted(file_list),
        }


# Utility functions for backward compatibility


def read_epc_stream(epc_file_path: Union[str, Path], **kwargs) -> EpcStreamReader:
    """
    Factory function to create EpcStreamReader instance.

    Args:
        epc_file_path: Path to EPC file
        **kwargs: Additional arguments for EpcStreamReader

    Returns:
        EpcStreamReader instance
    """
    return EpcStreamReader(epc_file_path, **kwargs)


def convert_to_streaming_epc(epc: Epc, output_path: Optional[Union[str, Path]] = None) -> EpcStreamReader:
    """
    Convert standard Epc to streaming version.

    Args:
        epc: Standard Epc instance
        output_path: Optional path to save EPC file

    Returns:
        EpcStreamReader instance
    """
    if output_path is None and epc.epc_file_path:
        output_path = epc.epc_file_path
    elif output_path is None:
        raise ValueError("Output path must be provided if EPC doesn't have a file path")

    # Export EPC to file if needed
    if not Path(output_path).exists():
        epc.export_file(str(output_path))

    return EpcStreamReader(output_path)


__all__ = ["EpcStreamReader", "EpcObjectMetadata", "EpcStreamingStats", "read_epc_stream", "convert_to_streaming_epc"]
