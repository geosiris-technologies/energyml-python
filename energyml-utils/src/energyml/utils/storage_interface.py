# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Unified Storage Interface Module

This module provides a unified interface for reading and writing energyml objects and arrays,
abstracting away whether the data comes from an ETP server, a local EPC file, or an EPC stream reader.

The storage interface enables applications to work with energyml data without knowing the
underlying storage mechanism, making it easy to switch between server-based and file-based
workflows.

Key Components:
- EnergymlStorageInterface: Abstract base class defining the storage interface
- ETPStorage: Implementation for ETP server-based storage (requires py-etp-client)
- EPCStorage: Implementation for local EPC file-based storage
- EPCStreamStorage: Implementation for streaming EPC file-based storage
- ResourceMetadata: Dataclass for object metadata (similar to ETP Resource)
- DataArrayMetadata: Dataclass for array metadata
- create_storage: Factory function for creating storage instances

Example Usage:
    ```python
    from energyml.utils.storage_interface import create_storage

    # Use with EPC file
    storage = create_storage("my_data.epc")

    # Same API for all implementations!
    obj = storage.get_object("uuid.version")
    metadata_list = storage.list_objects()
    array = storage.read_array(obj, "values/0")
    storage.put_object(new_obj)
    storage.close()
    ```
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
import logging

import numpy as np

from energyml.utils.uri import Uri, parse_uri
from energyml.utils.introspection import (
    get_obj_identifier,
    get_obj_uuid,
    get_obj_version,
    get_obj_type,
    get_content_type_from_class,
    epoch_to_date,
    epoch,
)
from energyml.utils.constants import content_type_to_qualified_type


@dataclass
class ResourceMetadata:
    """
    Metadata for an energyml object, similar to ETP Resource.

    This class provides a unified representation of object metadata across
    different storage backends (EPC, EPC Stream, ETP).
    """

    uri: str
    """URI of the resource (ETP-style uri or identifier)"""

    uuid: str
    """Object UUID"""

    title: str
    """Object title/name from citation"""

    object_type: str
    """Qualified type (e.g., 'resqml20.obj_TriangulatedSetRepresentation')"""

    content_type: str
    """Content type (e.g., 'application/x-resqml+xml;version=2.0;type=obj_TriangulatedSetRepresentation')"""

    version: Optional[str] = None
    """Object version (optional)"""

    dataspace: Optional[str] = None
    """Dataspace name (primarily for ETP)"""

    created: Optional[datetime] = None
    """Creation timestamp"""

    last_changed: Optional[datetime] = None
    """Last modification timestamp"""

    source_count: Optional[int] = None
    """Number of source relationships (objects this references)"""

    target_count: Optional[int] = None
    """Number of target relationships (objects referencing this)"""

    custom_data: Dict[str, Any] = field(default_factory=dict)
    """Additional custom metadata"""

    @property
    def identifier(self) -> str:
        """Get object identifier (uuid.version or uuid if no version)"""
        if self.version:
            return f"{self.uuid}.{self.version}"
        return self.uuid


@dataclass
class DataArrayMetadata:
    """
    Metadata for a data array in an energyml object.

    This provides information about arrays stored in HDF5 or other external storage,
    similar to ETP DataArrayMetadata.
    """

    path_in_resource: str
    """Path to the array within the HDF5 file"""

    array_type: str
    """Data type of the array (e.g., 'double', 'int', 'string')"""

    dimensions: List[int]
    """Array dimensions/shape"""

    custom_data: Dict[str, Any] = field(default_factory=dict)
    """Additional custom metadata"""

    @property
    def size(self) -> int:
        """Total number of elements in the array"""
        result = 1
        for dim in self.dimensions:
            result *= dim
        return result

    @property
    def ndim(self) -> int:
        """Number of dimensions"""
        return len(self.dimensions)


class EnergymlStorageInterface(ABC):
    """
    Abstract base class for energyml data storage operations.

    This interface defines a common API for interacting with energyml objects and arrays,
    regardless of whether they are stored on an ETP server, in a local EPC file, or in
    a streaming EPC reader.

    All implementations must provide methods for:
    - Getting, putting, and deleting energyml objects
    - Reading and writing data arrays
    - Getting array metadata
    - Listing available objects with metadata
    - Transaction support (where applicable)
    - Closing the storage connection
    """

    @abstractmethod
    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """
        Retrieve an object by its identifier (UUID or UUID.version).

        Args:
            identifier: Object identifier (UUID or UUID.version) or ETP URI

        Returns:
            The deserialized energyml object, or None if not found
        """
        pass

    @abstractmethod
    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """
        Retrieve all objects with the given UUID (all versions).

        Args:
            uuid: Object UUID

        Returns:
            List of objects with this UUID (may be empty)
        """
        pass

    @abstractmethod
    def put_object(self, obj: Any, dataspace: Optional[str] = None) -> Optional[str]:
        """
        Store an energyml object.

        Args:
            obj: The energyml object to store
            dataspace: Optional dataspace name (primarily for ETP)

        Returns:
            The identifier of the stored object (UUID.version or UUID), or None on error
        """
        pass

    @abstractmethod
    def delete_object(self, identifier: Union[str, Uri]) -> bool:
        """
        Delete an object by its identifier.

        Args:
            identifier: Object identifier (UUID or UUID.version) or ETP URI

        Returns:
            True if successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    def read_array(self, proxy: Union[str, Uri, Any], path_in_external: str) -> Optional[np.ndarray]:
        """
        Read a data array from external storage (HDF5).

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Path within the HDF5 file (e.g., 'values/0')

        Returns:
            The data array as a numpy array, or None if not found
        """
        pass

    @abstractmethod
    def write_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        array: np.ndarray,
    ) -> bool:
        """
        Write a data array to external storage (HDF5).

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Path within the HDF5 file (e.g., 'values/0')
            array: The numpy array to write

        Returns:
            True if successfully written, False otherwise
        """
        pass

    @abstractmethod
    def get_array_metadata(
        self, proxy: Union[str, Uri, Any], path_in_external: Optional[str] = None
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """
        Get metadata for data array(s).

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Optional specific path. If None, returns all array metadata for the object

        Returns:
            DataArrayMetadata if path specified, List[DataArrayMetadata] if no path,
            or None if not found
        """
        pass

    @abstractmethod
    def list_objects(
        self, dataspace: Optional[str] = None, object_type: Optional[str] = None
    ) -> List[ResourceMetadata]:
        """
        List all objects with their metadata.

        Args:
            dataspace: Optional dataspace filter (primarily for ETP)
            object_type: Optional type filter (qualified type, e.g., 'resqml20.obj_Grid2dRepresentation')

        Returns:
            List of ResourceMetadata for all matching objects
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the storage connection and release resources.
        """
        pass

    # Transaction support (optional, may raise NotImplementedError)

    def start_transaction(self) -> bool:
        """
        Start a transaction (if supported).

        Returns:
            True if transaction started, False if not supported
        """
        raise NotImplementedError("Transactions not supported by this storage backend")

    def commit_transaction(self) -> Tuple[bool, Optional[str]]:
        """
        Commit the current transaction (if supported).

        Returns:
            Tuple of (success, transaction_uuid)
        """
        raise NotImplementedError("Transactions not supported by this storage backend")

    def rollback_transaction(self) -> bool:
        """
        Rollback the current transaction (if supported).

        Returns:
            True if rolled back successfully
        """
        raise NotImplementedError("Transactions not supported by this storage backend")

    # Additional utility methods

    def get_object_dependencies(self, identifier: Union[str, Uri]) -> List[str]:
        """
        Get list of object identifiers that this object depends on (references).

        Args:
            identifier: Object identifier

        Returns:
            List of identifiers of objects this object references
        """
        raise NotImplementedError("Dependency tracking not implemented by this storage backend")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class EPCStorage(EnergymlStorageInterface):
    """
    EPC file-based storage implementation.

    This implementation uses an Epc object to interact with energyml data stored in
    a local EPC file. Arrays are stored in associated HDF5 external files.

    Args:
        epc: An initialized Epc instance
    """

    def __init__(self, epc: "Epc"):  # noqa: F821
        """
        Initialize EPC storage with an Epc instance.

        Args:
            epc: An Epc instance
        """
        from energyml.utils.epc import Epc

        if not isinstance(epc, Epc):
            raise TypeError(f"Expected Epc instance, got {type(epc)}")

        self.epc = epc
        self._closed = False

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """Retrieve an object by identifier from EPC."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        # Convert URI to identifier if needed
        if isinstance(identifier, Uri):
            identifier = f"{identifier.uuid}.{identifier.version}" if identifier.version else identifier.uuid
        elif isinstance(identifier, str) and identifier.startswith("eml://"):
            parsed = parse_uri(identifier)
            identifier = f"{parsed.uuid}.{parsed.version}" if parsed.version else ""

        return self.epc.get_object_by_identifier(identifier)

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """Retrieve all objects with the given UUID."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        result = self.epc.get_object_by_uuid(uuid)
        return result if isinstance(result, list) else [result] if result else []

    def put_object(self, obj: Any, dataspace: Optional[str] = None) -> Optional[str]:
        """Store an object in EPC."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        try:
            # Check if object already exists
            identifier = get_obj_identifier(obj)
            existing = self.epc.get_object_by_identifier(identifier)

            if existing:
                # Update existing object
                self.epc.energyml_objects.remove(existing)

            # Add new object
            self.epc.energyml_objects.append(obj)
            return identifier
        except Exception as e:
            logging.error(f"Failed to put object: {e}")
            return None

    def delete_object(self, identifier: Union[str, Uri]) -> bool:
        """Delete an object from EPC."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        try:
            obj = self.get_object(identifier)
            if obj and obj in self.epc.energyml_objects:
                self.epc.energyml_objects.remove(obj)
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to delete object: {e}")
            return False

    def read_array(self, proxy: Union[str, Uri, Any], path_in_external: str) -> Optional[np.ndarray]:
        """Read array from HDF5 file associated with EPC."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        # Get object if proxy is identifier
        if isinstance(proxy, (str, Uri)):
            proxy = self.get_object(proxy)
            if proxy is None:
                return None

        return self.epc.read_array(proxy, path_in_external)

    def write_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        array: np.ndarray,
    ) -> bool:
        """Write array to HDF5 file associated with EPC."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        # Get object if proxy is identifier
        if isinstance(proxy, (str, Uri)):
            proxy = self.get_object(proxy)
            if proxy is None:
                return False

        return self.epc.write_array(proxy, path_in_external, array)

    def get_array_metadata(
        self, proxy: Union[str, Uri, Any], path_in_external: Optional[str] = None
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """Get array metadata (limited support for EPC)."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        # EPC doesn't have native array metadata support
        # We can try to read the array and infer metadata
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
                logging.warning("EPC does not support listing all arrays without specific path")
                return []
        except Exception as e:
            logging.error(f"Failed to get array metadata: {e}")

        return None

    def list_objects(
        self, dataspace: Optional[str] = None, object_type: Optional[str] = None
    ) -> List[ResourceMetadata]:
        """List all objects with metadata."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        results = []
        for obj in self.epc.energyml_objects:
            try:
                uuid = get_obj_uuid(obj)
                version = get_obj_version(obj)
                obj_type = get_obj_type(obj)
                content_type = get_content_type_from_class(obj.__class__)

                # Apply type filter
                if object_type and obj_type != object_type:
                    continue

                # Get title from citation
                title = "Unknown"
                if hasattr(obj, "citation") and obj.citation:
                    if hasattr(obj.citation, "title"):
                        title = obj.citation.title

                # Build URI
                qualified_type = content_type_to_qualified_type(content_type)
                if version:
                    uri = f"eml:///{qualified_type}(uuid={uuid},version='{version}')"
                else:
                    uri = f"eml:///{qualified_type}({uuid})"

                metadata = ResourceMetadata(
                    uri=uri,
                    uuid=uuid,
                    version=version,
                    title=title,
                    object_type=obj_type,
                    content_type=content_type,
                )

                results.append(metadata)
            except Exception as e:
                logging.warning(f"Failed to get metadata for object: {e}")
                continue

        return results

    def close(self) -> None:
        """Close the EPC storage."""
        self._closed = True

    def save(self, file_path: Optional[str] = None) -> None:
        """
        Save the EPC to disk.

        Args:
            file_path: Optional path to save to. If None, uses epc.epc_file_path
        """
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        self.epc.export_file(file_path)


class EPCStreamStorage(EnergymlStorageInterface):
    """
    Memory-efficient EPC stream-based storage implementation.

    This implementation uses EpcStreamReader for lazy loading and caching,
    making it ideal for handling very large EPC files with thousands of objects.

    Features:
    - Lazy loading: Objects loaded only when accessed
    - Smart caching: LRU cache with configurable size
    - Memory monitoring: Track memory usage and cache efficiency
    - Same interface as EPCStorage for seamless switching

    Args:
        stream_reader: An EpcStreamReader instance
    """

    def __init__(self, stream_reader: "EpcStreamReader"):  # noqa: F821
        """
        Initialize EPC stream storage with an EpcStreamReader instance.

        Args:
            stream_reader: An EpcStreamReader instance
        """
        from energyml.utils.epc_stream import EpcStreamReader

        if not isinstance(stream_reader, EpcStreamReader):
            raise TypeError(f"Expected EpcStreamReader instance, got {type(stream_reader)}")

        self.stream_reader = stream_reader
        self._closed = False

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """Retrieve an object by identifier from EPC stream."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        # Convert URI to identifier if needed
        if isinstance(identifier, Uri):
            identifier = f"{identifier.uuid}.{identifier.version or ''}"
        elif isinstance(identifier, str) and identifier.startswith("eml://"):
            parsed = parse_uri(identifier)
            identifier = f"{parsed.uuid}.{parsed.version or ''}"

        return self.stream_reader.get_object_by_identifier(identifier)

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """Retrieve all objects with the given UUID."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        return self.stream_reader.get_object_by_uuid(uuid)

    def put_object(self, obj: Any, dataspace: Optional[str] = None) -> Optional[str]:
        """Store an object in EPC stream."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        try:
            return self.stream_reader.add_object(obj, replace_if_exists=True)
        except Exception as e:
            logging.error(f"Failed to put object: {e}")
            return None

    def delete_object(self, identifier: Union[str, Uri]) -> bool:
        """Delete an object from EPC stream."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        try:
            return self.stream_reader.remove_object(identifier)
        except Exception as e:
            logging.error(f"Failed to delete object: {e}")
            return False

    def read_array(self, proxy: Union[str, Uri, Any], path_in_external: str) -> Optional[np.ndarray]:
        """Read array from HDF5 file associated with EPC stream."""
        if self._closed:
            raise RuntimeError("Storage is closed")

        return self.stream_reader.read_array(proxy, path_in_external)

    def write_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        array: np.ndarray,
    ) -> bool:
        """Write array to HDF5 file associated with EPC stream."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        return self.stream_reader.write_array(proxy, path_in_external, array)

    def get_array_metadata(
        self, proxy: Union[str, Uri, Any], path_in_external: Optional[str] = None
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """Get array metadata (limited support for EPC Stream)."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        # EPC Stream doesn't have native array metadata support
        # We can try to read the array and infer metadata
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
                logging.warning("EPC Stream does not support listing all arrays without specific path")
                return []
        except Exception as e:
            logging.error(f"Failed to get array metadata: {e}")

        return None

    def list_objects(
        self, dataspace: Optional[str] = None, object_type: Optional[str] = None
    ) -> List[ResourceMetadata]:
        """List all objects with metadata."""
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        results = []
        metadata_list = self.stream_reader.list_object_metadata(object_type)

        for meta in metadata_list:
            try:
                # Load object to get title
                # obj = self.stream_reader.get_object_by_identifier(meta.identifier)
                # title = "Unknown"
                # if obj and hasattr(obj, "citation") and obj.citation:
                #     if hasattr(obj.citation, "title"):
                #         title = obj.citation.title

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
                    title="",  # we do not fill the title to avoid loading the object
                    object_type=meta.object_type,
                    content_type=meta.content_type,
                )

                results.append(resource)
            except Exception as e:
                logging.warning(f"Failed to get metadata for {meta.identifier}: {e}")
                continue

        return results

    def close(self) -> None:
        """Close the EPC stream storage."""
        self._closed = True

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get streaming statistics.

        Returns:
            Dictionary with cache statistics and performance metrics
        """
        # if self._closed:
        # raise RuntimeError("Storage is closed")

        stats = self.stream_reader.get_statistics()
        return {
            "total_objects": stats.total_objects,
            "loaded_objects": stats.loaded_objects,
            "cache_hits": stats.cache_hits,
            "cache_misses": stats.cache_misses,
            "cache_hit_ratio": stats.cache_hit_ratio,
            "bytes_read": stats.bytes_read,
        }


def create_storage(
    source: Union[str, Path, "Epc", "EpcStreamReader"],  # noqa: F821
    stream_mode: bool = False,
    cache_size: int = 100,
    **kwargs,
) -> EnergymlStorageInterface:
    """
    Factory function to create an appropriate storage interface from various sources.

    This convenience function automatically determines the correct storage implementation
    based on the type of source provided.

    Args:
        source: Can be:
            - Epc instance: Creates EPCStorage
            - EpcStreamReader instance: Creates EPCStreamStorage
            - str/Path (file path): Loads EPC file and creates EPCStorage or EPCStreamStorage
        stream_mode: If True and source is a file path, creates EPCStreamStorage for memory efficiency
        cache_size: Cache size for stream mode (default: 100)
        **kwargs: Additional arguments passed to EpcStreamReader if in stream mode

    Returns:
        An EnergymlStorageInterface implementation (EPCStorage or EPCStreamStorage)

    Raises:
        ValueError: If the source type is not supported
        FileNotFoundError: If file path does not exist

    Example:
        ```python
        # From EPC instance
        from energyml.utils.epc import Epc
        epc = Epc()
        storage = create_storage(epc)

        # From EPC stream reader
        from energyml.utils.epc_stream import EpcStreamReader
        stream_reader = EpcStreamReader("large_file.epc", cache_size=50)
        storage = create_storage(stream_reader)

        # From file path (regular mode)
        storage = create_storage("path/to/file.epc")

        # From file path (streaming mode for large files)
        storage = create_storage("path/to/large_file.epc", stream_mode=True, cache_size=50)
        ```
    """
    from energyml.utils.epc import Epc
    from energyml.utils.epc_stream import EpcStreamReader

    if isinstance(source, Epc):
        return EPCStorage(source)

    elif isinstance(source, EpcStreamReader):
        return EPCStreamStorage(source)

    elif isinstance(source, (str, Path)):
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"EPC file not found: {file_path}")

        if stream_mode:
            # Create streaming reader for memory efficiency
            stream_reader = EpcStreamReader(file_path, cache_size=cache_size, **kwargs)
            return EPCStreamStorage(stream_reader)
        else:
            # Load full EPC into memory
            from energyml.utils.epc import read_energyml_epc_file

            epc = read_energyml_epc_file(str(file_path))
            return EPCStorage(epc)

    else:
        raise ValueError(
            f"Unsupported source type: {type(source)}. " "Expected Epc, EpcStreamReader, or file path (str/Path)"
        )


__all__ = [
    "EnergymlStorageInterface",
    "EPCStorage",
    "EPCStreamStorage",
    "ResourceMetadata",
    "DataArrayMetadata",
    "create_storage",
]
