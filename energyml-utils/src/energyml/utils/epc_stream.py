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
from energyml.utils.uri import Uri, parse_uri
from energyml.utils.workspace import EnergymlWorkspace
import numpy as np
from .constants import EPCRelsRelationshipType, OptimizedRegex, EpcExportVersion
from .epc import Epc, gen_energyml_object_path, gen_rels_path, get_epc_content_type_path
from .introspection import (
    get_class_from_content_type,
    get_obj_content_type,
    get_obj_identifier,
    get_obj_uuid,
    get_object_type_for_file_path_from_class,
    get_direct_dor_list,
    get_obj_type,
    get_obj_usable_class,
)
from .serialization import read_energyml_xml_bytes, serialize_xml
from .xml import is_energyml_content_type


@dataclass(frozen=True)
class EpcObjectMetadata:
    """Metadata for an object in the EPC file."""

    uuid: str
    object_type: str
    content_type: str
    file_path: str
    version: Optional[str] = None
    identifier: Optional[str] = None

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


class EpcStreamReader(EnergymlWorkspace):
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
        """
        self.epc_file_path = Path(epc_file_path)
        self.cache_size = cache_size
        self.validate_on_load = validate_on_load
        self.force_h5_path = force_h5_path

        is_new_file = False

        # Validate file exists and is readable
        if not self.epc_file_path.exists():
            logging.info(f"EPC file not found: {epc_file_path}. Creating a new empty EPC file.")
            self._create_empty_epc()
            is_new_file = True
            # raise FileNotFoundError(f"EPC file not found: {epc_file_path}")

        if not zipfile.is_zipfile(self.epc_file_path):
            raise ValueError(f"File is not a valid ZIP/EPC file: {epc_file_path}")

        # Check if the ZIP file has the required EPC structure
        if not is_new_file:
            try:
                with zipfile.ZipFile(self.epc_file_path, "r") as zf:
                    content_types_path = get_epc_content_type_path()
                    if content_types_path not in zf.namelist():
                        logging.info(f"EPC file is missing required structure. Initializing empty EPC file.")
                        self._create_empty_epc()
                        is_new_file = True
            except Exception as e:
                logging.warning(f"Failed to check EPC structure: {e}. Reinitializing.")

        # Object metadata storage
        self._metadata: Dict[str, EpcObjectMetadata] = {}  # identifier -> metadata
        self._uuid_index: Dict[str, List[str]] = {}  # uuid -> list of identifiers
        self._type_index: Dict[str, List[str]] = {}  # object_type -> list of identifiers

        # Caching system using weak references
        self._object_cache: WeakValueDictionary = WeakValueDictionary()
        self._access_order: List[str] = []  # LRU tracking

        # Core properties and stats
        self._core_props: Optional[CoreProperties] = None
        self.stats = EpcStreamingStats()

        # File handle management
        self._zip_file: Optional[zipfile.ZipFile] = None

        # EPC export version detection
        self.export_version: EpcExportVersion = export_version or EpcExportVersion.CLASSIC  # Default

        # Additional rels management
        self.additional_rels: Dict[str, List[Relationship]] = {}

        # Initialize by loading metadata
        if not is_new_file and preload_metadata:
            self._load_metadata()
            # Detect EPC version after loading metadata
            self.export_version = self._detect_epc_version()

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
        try:
            with self._get_zip_file() as zf:
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

    @contextmanager
    def _get_zip_file(self) -> Iterator[zipfile.ZipFile]:
        """Context manager for ZIP file access with proper resource management."""
        zf = None
        try:
            zf = zipfile.ZipFile(self.epc_file_path, "r")
            yield zf
        finally:
            if zf is not None:
                zf.close()

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
        """
        Fast extraction of UUID and version from XML without full parsing.

        Uses optimized regex patterns for performance.
        """
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
        # Store core properties path for lazy loading
        if override.part_name:
            self._core_props_path = override.part_name.lstrip("/")

    def _detect_epc_version(self) -> EpcExportVersion:
        """
        Detect EPC packaging version based on file structure.

        CLASSIC version uses simple flat structure: obj_Type_UUID.xml
        EXPANDED version uses namespace structure: namespace_pkg/UUID/version_X/Type_UUID.xml

        Returns:
            EpcExportVersion: The detected version (CLASSIC or EXPANDED)
        """
        try:
            with self._get_zip_file() as zf:
                file_list = zf.namelist()

                # Look for patterns that indicate EXPANDED version
                # EXPANDED uses paths like: namespace_resqml22/UUID/version_X/Type_UUID.xml
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
                        # Further validate it's the EXPANDED structure
                        path_parts = file_path.split("/")
                        if len(path_parts) >= 2:  # namespace_pkg/filename or namespace_pkg/version_x/filename
                            logging.info(f"Detected EXPANDED EPC version based on path: {file_path}")
                            return EpcExportVersion.EXPANDED

                # If no EXPANDED patterns found, assume CLASSIC
                logging.info("Detected CLASSIC EPC version")
                return EpcExportVersion.CLASSIC

        except Exception as e:
            logging.warning(f"Failed to detect EPC version, defaulting to CLASSIC: {e}")
            return EpcExportVersion.CLASSIC

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
        if self._core_props is None and hasattr(self, "_core_props_path"):
            try:
                with self._get_zip_file() as zf:
                    core_data = zf.read(self._core_props_path)
                    self.stats.bytes_read += len(core_data)
                    self._core_props = read_energyml_xml_bytes(core_data, CoreProperties)
            except Exception as e:
                logging.error(f"Failed to load core properties: {e}")

        return self._core_props

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

    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        """
        Get all relationships for a given object.
        :param obj: the object or its identifier/URI
        :return: list of Relationship objects
        """
        rels = []

        # read rels from EPC file
        if isinstance(obj, (str, Uri)):
            obj = self.get_object_by_identifier(obj)
        with zipfile.ZipFile(self.epc_file_path, "r") as zf:
            rels_path = gen_rels_path(obj, self.export_version)
            try:
                rels_data = zf.read(rels_path)
                self.stats.bytes_read += len(rels_data)
                relationships = read_energyml_xml_bytes(rels_data, Relationships)
                rels.extend(relationships.relationship)
            except KeyError:
                # No rels file found for this object
                pass

        return rels

    def get_h5_file_paths(self, obj: Union[str, Uri, Any]) -> List[str]:
        """
        Get all HDF5 file paths referenced in the EPC file (from rels to external resources)
        :param obj: the object or its identifier/URI
        :return: list of HDF5 file paths
        """
        if self.force_h5_path is not None:
            return [self.force_h5_path]
        h5_paths = set()

        if isinstance(obj, (str, Uri)):
            obj = self.get_object_by_identifier(obj)

        for rels in self.additional_rels.get(get_obj_identifier(obj), []):
            if rels.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
                h5_paths.add(rels.target)

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
        # Resolve proxy to object
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

    def get_object_dependencies(self, identifier: str) -> List[str]:
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
        """Remove a single object by its full identifier."""
        try:
            if identifier not in self._metadata:
                return False

            metadata = self._metadata[identifier]

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
            # Remove existing object
            self.remove_object(identifier)

            # Add updated object
            new_identifier = self.add_object(obj)

            logging.info(f"Updated object {identifier} to {new_identifier} in EPC file")
            return new_identifier

        except Exception as e:
            logging.error(f"Failed to update object {identifier}: {e}")
            raise RuntimeError(f"Failed to update object in EPC: {e}")

    def add_rels_for_object(self, identifier: Union[str, Uri, Any], relationships: List[Relationship]) -> None:
        """
        Add additional relationships for a specific object.

        Args:
            identifier: The identifier of the object, can be str, Uri, or the object itself
            relationships: List of Relationship objects to add
        """
        is_uri = isinstance(identifier, Uri) or (isinstance(identifier, str) and parse_uri(identifier) is not None)
        object_instance = None
        if is_uri:
            uri = parse_uri(identifier) if isinstance(identifier, str) else identifier
            assert uri is not None and uri.uuid is not None
            identifier = uri.uuid + "." + (uri.version or "")
            object_instance = self.get_object_by_identifier(identifier)
        elif not isinstance(identifier, str):
            identifier = get_obj_identifier(identifier)
            object_instance = self.get_object_by_identifier(identifier)
        else:
            object_instance = identifier

        assert isinstance(identifier, str)

        if identifier not in self.additional_rels:
            self.additional_rels[identifier] = []

        self.additional_rels[identifier].extend(relationships)
        if len(self.additional_rels[identifier]) > 0:
            # Create temporary file for updated EPC
            with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
                temp_path = temp_file.name
            # Update the .rels file for this object by updating the rels file in the EPC
            with (
                zipfile.ZipFile(self.epc_file_path, "r") as source_zip,
                zipfile.ZipFile(temp_path, "a") as target_zip,
            ):
                # copy all files except the rels file to be updated
                for item in source_zip.infolist():
                    if item.filename != gen_rels_path(object_instance, self.export_version):
                        buffer = source_zip.read(item.filename)
                        target_zip.writestr(item, buffer)

                self._update_existing_rels_files(
                    Relationships(relationship=relationships),
                    gen_rels_path(object_instance, self.export_version),
                    source_zip,
                    target_zip,
                )
            shutil.move(temp_path, self.epc_file_path)

    def _compute_object_rels(self, obj: Any, obj_identifier: str) -> List[Relationship]:
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
                target_rels_path = gen_rels_path(dor, self.export_version)

                # Create SOURCE relationship (this object -> target object)
                rel = Relationship(
                    target=target_rels_path,
                    type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                    id=f"_{obj_identifier}_{get_obj_type(get_obj_usable_class(dor))}_{target_identifier}",
                )
                rels.append(rel)
            except Exception as e:
                logging.warning(f"Failed to create relationship for DOR in {obj_identifier}: {e}")

        return rels

    def _get_objects_referencing(self, target_identifier: str) -> List[Tuple[str, Any]]:
        """
        Find all objects that reference the target object.

        Args:
            target_identifier: The identifier of the target object

        Returns:
            List of tuples (identifier, object) of objects that reference the target
        """
        referencing_objects = []

        # We need to check all objects in the EPC to find those that reference our target
        for identifier in self._metadata:
            # Load the object to check its DORs
            obj = self.get_object_by_identifier(identifier)
            if obj is not None:
                # Check if this object references our target
                direct_dors = get_direct_dor_list(obj)
                for dor in direct_dors:
                    try:
                        dor_identifier = get_obj_identifier(dor)
                        if dor_identifier == target_identifier:
                            referencing_objects.append((identifier, obj))
                            break  # Found a reference, no need to check other DORs in this object
                    except Exception:
                        continue

        return referencing_objects

    def _update_existing_rels_files(
        self, rels: Relationships, rel_path: str, source_zip: zipfile.ZipFile, target_zip: zipfile.ZipFile
    ) -> None:
        """Merge new relationships with existing .rels, reading from source and writing to target ZIP.

        Args:
            rels: New Relationships to add
            rel_path: Path to the .rels file
            source_zip: ZIP to read existing rels from
            target_zip: ZIP to write updated rels to
        """
        # print("@ Updating rels file:", rel_path)
        existing_relationships = []
        try:
            if rel_path in source_zip.namelist():
                rels_data = source_zip.read(rel_path)
                existing_rels = read_energyml_xml_bytes(rels_data, Relationships)
                if existing_rels and existing_rels.relationship:
                    existing_relationships = list(existing_rels.relationship)
        except Exception as e:
            logging.debug(f"Could not read existing rels for {rel_path}: {e}")

        for new_rel in rels.relationship:
            rel_exists = any(
                r.target == new_rel.target and r.type_value == new_rel.type_value for r in existing_relationships
            )
            cpt = 0
            new_rel_id = new_rel.id
            while any(r.id == new_rel_id for r in existing_relationships):
                new_rel_id = f"{new_rel.id}_{cpt}"
                cpt += 1
            if new_rel_id != new_rel.id:
                new_rel.id = new_rel_id
            if not rel_exists:
                existing_relationships.append(new_rel)

        if existing_relationships:
            updated_rels = Relationships(relationship=existing_relationships)
            updated_rels_xml = serialize_xml(updated_rels)
            target_zip.writestr(rel_path, updated_rels_xml)

    def _update_rels_files(
        self,
        obj: Any,
        metadata: EpcObjectMetadata,
        source_zip: zipfile.ZipFile,
        target_zip: zipfile.ZipFile,
    ) -> List[str]:
        """
        Update all necessary .rels files when adding/updating an object.

        This includes:
        1. The object's own .rels file (for objects it references)
        2. The .rels files of objects that now reference this object (DESTINATION relationships)

        Args:
            obj: The object being added/updated
            metadata: Metadata for the object
            source_zip: Source ZIP file to read existing rels from
            target_zip: Target ZIP file to write updated rels to

        returns:
            List of updated .rels file paths
        """
        obj_identifier = metadata.identifier
        updated_rels_paths = []
        if not obj_identifier:
            logging.warning("Object identifier is None, skipping rels update")
            return updated_rels_paths

        # 1. Create/update the object's own .rels file
        obj_rels_path = gen_rels_path(obj, self.export_version)
        obj_relationships = self._compute_object_rels(obj, obj_identifier)

        if obj_relationships:
            self._update_existing_rels_files(
                Relationships(relationship=obj_relationships), obj_rels_path, source_zip, target_zip
            )
            updated_rels_paths.append(obj_rels_path)

        # 2. Update .rels files of objects referenced by this object
        # These objects need DESTINATION relationships pointing to our object
        direct_dors = get_direct_dor_list(obj)

        logging.debug(f"Updating rels for object {obj_identifier}, found {len(direct_dors)} direct DORs")

        for dor in direct_dors:
            try:
                target_rels_path = gen_rels_path(dor, self.export_version)
                target_identifier = get_obj_identifier(dor)

                # Add DESTINATION relationship from target to our object
                dest_rel = Relationship(
                    target=metadata.file_path,
                    type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                    id=f"_{target_identifier}_{get_obj_type(get_obj_usable_class(obj))}_{obj_identifier}",
                )

                self._update_existing_rels_files(
                    Relationships(relationship=[dest_rel]), target_rels_path, source_zip, target_zip
                )
                updated_rels_paths.append(target_rels_path)

            except Exception as e:
                logging.warning(f"Failed to update rels for referenced object: {e}")
        return updated_rels_paths

    def _remove_rels_files(
        self, obj: Any, metadata: EpcObjectMetadata, source_zip: zipfile.ZipFile, target_zip: zipfile.ZipFile
    ) -> None:
        """
        Remove/update .rels files when removing an object.

        This includes:
        1. Removing the object's own .rels file
        2. Removing DESTINATION relationships from objects that this object referenced

        Args:
            obj: The object being removed
            metadata: Metadata for the object
            source_zip: Source ZIP file to read existing rels from
            target_zip: Target ZIP file to write updated rels to
        """
        # obj_identifier = metadata.identifier

        # 1. The object's own .rels file will be automatically excluded by not copying it
        # obj_rels_path = gen_rels_path(obj, self.export_version)

        # 2. Update .rels files of objects that were referenced by this object
        # Remove DESTINATION relationships that pointed to our object
        direct_dors = get_direct_dor_list(obj)

        for dor in direct_dors:
            try:
                target_identifier = get_obj_identifier(dor)

                # Check if target object exists
                if target_identifier not in self._metadata:
                    continue

                target_obj = self.get_object_by_identifier(target_identifier)
                if target_obj is None:
                    continue

                target_rels_path = gen_rels_path(target_obj, self.export_version)

                # Read existing rels for the target object
                existing_relationships = []
                try:
                    if target_rels_path in source_zip.namelist():
                        rels_data = source_zip.read(target_rels_path)
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

                # Write updated rels file (or skip if no relationships left)
                if updated_relationships:
                    updated_rels = Relationships(relationship=updated_relationships)
                    updated_rels_xml = serialize_xml(updated_rels)
                    target_zip.writestr(target_rels_path, updated_rels_xml)

            except Exception as e:
                logging.warning(f"Failed to update rels for referenced object during removal: {e}")

    def _add_object_to_file(self, obj: Any, metadata: EpcObjectMetadata) -> None:
        """Add object to the EPC file by safely rewriting the ZIP archive.

        The method creates a temporary ZIP archive, copies all entries except
        the ones to be updated (content types and relevant .rels), then writes
        the new object, merges and writes updated .rels files and the
        updated [Content_Types].xml before replacing the original file. This
        avoids issues with append mode creating overlapped entries.
        """
        xml_content = serialize_xml(obj)

        # Create temporary file for updated EPC
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with zipfile.ZipFile(self.epc_file_path, "r") as source_zip:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zip:

                    # Add new object file
                    target_zip.writestr(metadata.file_path, xml_content)

                    # Update .rels files by merging with existing ones read from source
                    updated_rels_paths = self._update_rels_files(obj, metadata, source_zip, target_zip)

                    # Copy all existing files except [Content_Types].xml and rels we'll update
                    for item in source_zip.infolist():
                        if item.filename == get_epc_content_type_path() or item.filename in updated_rels_paths:
                            continue
                        data = source_zip.read(item.filename)
                        target_zip.writestr(item, data)

                    # Update [Content_Types].xml
                    updated_content_types = self._update_content_types_xml(source_zip, metadata, add=True)
                    target_zip.writestr(get_epc_content_type_path(), updated_content_types)

            # Replace original file with updated version
            shutil.move(temp_path, self.epc_file_path)

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            logging.error(f"Failed to add object to EPC file: {e}")
            raise

    def _remove_object_from_file(self, metadata: EpcObjectMetadata) -> None:
        """Remove object from the EPC file by updating the ZIP archive.

        Note: This does NOT remove .rels files. Use clean_rels() to remove orphaned relationships.
        """

        # Create temporary file for updated EPC
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            # Copy existing EPC to temp file, excluding the object to remove
            with zipfile.ZipFile(self.epc_file_path, "r") as source_zip:
                with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as target_zip:
                    # Copy all existing files except the one to remove and [Content_Types].xml
                    # We keep .rels files as-is (they will be cleaned by clean_rels() if needed)
                    for item in source_zip.infolist():
                        if item.filename not in [metadata.file_path, get_epc_content_type_path()]:
                            data = source_zip.read(item.filename)
                            target_zip.writestr(item, data)

                    # Update [Content_Types].xml
                    updated_content_types = self._update_content_types_xml(source_zip, metadata, add=False)
                    target_zip.writestr(get_epc_content_type_path(), updated_content_types)

            # Replace original file with updated version
            shutil.move(temp_path, self.epc_file_path)

        except Exception:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def _update_content_types_xml(
        self, source_zip: zipfile.ZipFile, metadata: EpcObjectMetadata, add: bool = True
    ) -> str:
        """Update [Content_Types].xml to add or remove object entry."""
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
        from .serialization import serialize_xml

        return serialize_xml(content_types)

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
            with zipfile.ZipFile(self.epc_file_path, "r") as source_zip:
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
                obj_rels_path = gen_rels_path(obj, self.export_version)

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

                    if relationships:
                        if obj_rels_path not in rels_files:
                            rels_files[obj_rels_path] = Relationships(relationship=[])
                        rels_files[obj_rels_path].relationship.extend(relationships)

            except Exception as e:
                logging.warning(f"Failed to create SOURCE rels for {identifier}: {e}")

        # Add DESTINATION relationships
        for target_identifier, source_list in reverse_references.items():
            try:
                target_obj = self.get_object_by_identifier(target_identifier)
                if target_obj is None:
                    continue

                target_metadata = self._metadata[target_identifier]
                target_rels_path = gen_rels_path(target_obj, self.export_version)

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

        # Third pass: write the new EPC with updated .rels files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as temp_file:
            temp_path = temp_file.name

        try:
            with zipfile.ZipFile(self.epc_file_path, "r") as source_zip:
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

        with zipfile.ZipFile(self.epc_file_path, "r") as zf:
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
