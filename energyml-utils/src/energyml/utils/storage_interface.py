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
- ResourceMetadata: Dataclass for object metadata (similar to ETP Resource)
- DataArrayMetadata: Dataclass for array metadata

Example Usage:
    ```python
    from energyml.utils.storage_interface import create_storage

    # Use with EPC file
    storage = create_storage("my_data.epc")

    # Same API for all implementations!
    obj = storage.get_object("uuid.version") or storage.get_object("eml:///dataspace('default')/resqml22.TriangulatedSetRepresentation('uuid')")
    metadata_list = storage.list_objects()
    array = storage.read_array(obj, "values/0")
    storage.put_object(new_obj)
    storage.close()
    ```
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Tuple

from energyml.utils.uri import Uri
from energyml.opc.opc import Relationship
import numpy as np


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

    def __str__(self):
        return f"{'[' + self.title + '] ' if self.title else ''}{self.uri}"


def create_resource_metadata_from_uri(
    uri: Uri,
    title: Optional[str] = None,
    last_changed: Optional[datetime] = None,
    custom_data: Optional[Dict[str, Any]] = None,
    source_count: Optional[int] = None,
    target_count: Optional[int] = None,
) -> ResourceMetadata:
    """
    Create ResourceMetadata from an ETP URI.

    Args:
        uri: ETP URI (e.g., 'eml:///dataspace('default')/resqml22.TriangulatedSetRepresentation('uuid.version')')
    Returns:
        ResourceMetadata instance with fields extracted from the URI
    """
    if not uri.is_object_uri():
        raise ValueError("URI must be an object URI to create ResourceMetadata")
    return ResourceMetadata(
        uri=str(uri),
        uuid=uri.uuid or "",
        title=title or "",
        object_type=uri.object_type or "",
        content_type=uri.get_content_type(),
        version=uri.version,
        dataspace=uri.dataspace,
        custom_data=custom_data or {},
        source_count=source_count,
        target_count=target_count,
        last_changed=last_changed,
    )


@dataclass
class DataArrayMetadata:
    """
    Metadata for a data array in an energyml object.

    This provides information about arrays stored in HDF5 or other external storage,
    similar to ETP DataArrayMetadata. Supports RESQML v2.2 ExternalDataArrayPart attributes.

    The dimensions field represents the shape of the array that would be returned:
    - For full arrays: the complete array dimensions from the external file
    - For sub-selections: the size of the selected portion (determined by start_indices + counts)
    """

    path_in_resource: Optional[str]
    """Path to the array within the HDF5 file (PathInExternalFile)"""

    array_type: str
    """Data type of the array (e.g., 'double', 'int', 'string')"""

    dimensions: List[int]
    """Array dimensions/shape. For sub-selections, this reflects the selected portion size."""

    start_indices: Optional[List[int]] = None
    """Start index for each dimension (RESQML v2.2 StartIndex). If None, starts at 0."""

    external_uri: Optional[str] = None
    """URI where the DataArrayPart is stored (RESQML v2.2 URI). Can override default file path."""

    mime_type: Optional[str] = None
    """MIME type of the external file (RESQML v2.2 MimeType)"""

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

    @classmethod
    def from_numpy_array(cls, path_in_resource: Optional[str], array: np.ndarray) -> "DataArrayMetadata":
        """
        Create DataArrayMetadata from a numpy array.

        Args:
            path_in_resource: Path to the array within the HDF5 file
            array: Numpy array
        Returns:
            DataArrayMetadata instance
        """
        return cls(
            path_in_resource=path_in_resource,
            array_type=str(array.dtype),
            dimensions=list(array.shape),
        )

    @classmethod
    def from_list(cls, path_in_resource: Optional[str], data: List[Any]) -> "DataArrayMetadata":
        """
        Create DataArrayMetadata from a list.

        Args:
            path_in_resource: Path to the array within the HDF5 file
            data: List of data
        Returns:
            DataArrayMetadata instance
        """
        array = np.array(data)
        return cls.from_numpy_array(path_in_resource, array)


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
    def read_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        """
        Read a data array from external storage (HDF5) with optional sub-selection.

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Path within the HDF5 file (e.g., 'values/0')
            start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
            counts: Optional count of elements for each dimension (RESQML v2.2 Count)
            external_uri: Optional URI to override default file path (RESQML v2.2 URI)

        Returns:
            The data array as a numpy array, or None if not found.
            If start_indices and counts are provided, returns the sub-selected portion.
        """
        pass

    def read_array_view(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        """
        Read a data array as a zero-copy view when possible.

        For HDF5 datasets that are contiguous and uncompressed, returns a numpy array
        backed directly by the memory-mapped file buffer (no copy). For chunked or
        compressed datasets it transparently falls back to a copy, identical to
        :meth:`read_array`.

        The caller **must not mutate** the returned array; use ``arr.copy()`` first if
        in-place modification is required.

        Default implementation delegates to :meth:`read_array` so that any third-party
        subclass that does not override this method retains correct behaviour.

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Path within the HDF5 file (e.g., 'values/0')
            start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
            counts: Optional count of elements for each dimension (RESQML v2.2 Count)
            external_uri: Optional URI to override default file path (RESQML v2.2 URI)

        Returns:
            The data array as a numpy array (view if possible, copy otherwise), or None if not found.
        """
        return self.read_array(proxy, path_in_external, start_indices, counts, external_uri)

    @abstractmethod
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
        Write a data array to external storage (HDF5) with optional offset.

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Path within the HDF5 file (e.g., 'values/0')
            array: The numpy array to write
            start_indices: Optional start index for each dimension for partial writes
            external_uri: Optional URI to override default file path (RESQML v2.2 URI)
            **kwargs: Additional format-specific parameters

        Returns:
            True if successfully written, False otherwise
        """
        pass

    @abstractmethod
    def get_array_metadata(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """
        Get metadata for data array(s) with optional sub-selection.

        Args:
            proxy: The object identifier/URI or the object itself that references the array
            path_in_external: Optional specific path. If None, returns all array metadata for the object
            start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
            counts: Optional count of elements for each dimension (RESQML v2.2 Count).
                    When provided, the returned dimensions will reflect the sub-selected size.

        Returns:
            DataArrayMetadata if path specified, List[DataArrayMetadata] if no path,
            or None if not found. The dimensions field reflects sub-selection when counts provided.
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
    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        """Get relationships for an object.

        Args:
            obj: The object identifier/URI or the object itself

        Returns:
            List of Relationship objects
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


__all__ = [
    "EnergymlStorageInterface",
    "ResourceMetadata",
    "DataArrayMetadata",
]
