# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, List, Union, Any

import numpy as np


@dataclass
class DatasetReader:
    def read_array(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[np.ndarray]:
        return None

    def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[int]]:
        return None


class ExternalArrayHandler(ABC):
    """
    Base class for handling external array storage (HDF5, Parquet, CSV, etc.).

    This abstract interface defines the contract for reading, writing, and querying
    metadata from external array files. Implementations for specific formats extend
    this class and handle format-specific details.

    Key features:
    - Format-agnostic interface
    - Support for file paths, BytesIO, or already-opened file handles
    - Metadata queries without loading full arrays
    - Support for sub-array selection via start_indices and counts (RESQML v2.2)
    """

    @abstractmethod
    def read_array(
        self,
        source: Union[BytesIO, str, Any],
        path_in_external_file: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
    ) -> Optional[np.ndarray]:
        """
        Read array data from external storage with optional sub-selection.

        Args:
            source: File path, BytesIO, or already-opened file handle
            path_in_external_file: Path/dataset name within the file (format-specific)
            start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
            counts: Optional count of elements for each dimension (RESQML v2.2 Count)

        Returns:
            Numpy array if successful, None otherwise. If start_indices and counts are
            provided, returns the sub-selected portion of the array.
        """
        pass

    @abstractmethod
    def write_array(
        self,
        target: Union[str, BytesIO, Any],
        array: Union[list, np.ndarray],
        path_in_external_file: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        **kwargs,
    ) -> bool:
        """
        Write array data to external storage with optional offset.

        Args:
            target: File path, BytesIO, or already-opened file handle
            array: Data to write
            path_in_external_file: Path/dataset name within the file (format-specific)
            start_indices: Optional start index for each dimension for partial writes
            **kwargs: Additional format-specific parameters

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_array_metadata(
        self,
        source: Union[BytesIO, str, Any],
        path_in_external_file: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
    ) -> Optional[Union[dict, List[dict]]]:
        """
        Get metadata about arrays in external storage without loading the data.

        Args:
            source: File path, BytesIO, or already-opened file handle
            path_in_external_file: Specific array path, or None to get all arrays
            start_indices: Optional start index for each dimension
            counts: Optional count of elements for each dimension

        Returns:
            Dict with keys: 'path', 'dtype', 'shape', 'size' for single array.
            If start_indices and counts provided, 'shape' reflects the sub-selection.
            List of such dicts if path_in_external_file is None.
            None if not found or error.
        """
        pass

    @abstractmethod
    def list_arrays(self, source: Union[BytesIO, str, Any]) -> List[str]:
        """
        List all array paths/dataset names in the external file.

        Args:
            source: File path, BytesIO, or already-opened file handle

        Returns:
            List of array path strings
        """
        pass

    @abstractmethod
    def can_handle_file(self, file_path: str) -> bool:
        """
        Check if this handler can process the given file based on extension.

        Args:
            file_path: Path to the file

        Returns:
            True if this handler supports the file format
        """
        pass


# @dataclass
# class ETPReader(DatasetReader):
#     def read_array(self, obj_uri: str, path_in_external_file: str) -> Optional[np.ndarray]:
#         return None

#     def get_array_dimension(self, source: str, path_in_external_file: str) -> Optional[np.ndarray]:
#         return None
