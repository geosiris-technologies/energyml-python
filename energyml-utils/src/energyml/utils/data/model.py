# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import OrderedDict
from io import BytesIO
from typing import Dict, Optional, List, Union, Any

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class DatasetReader:
    def read_array(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[np.ndarray]:
        return None

    def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[int]]:
        return None


class FileCacheManager:
    """
    Manages a cache of open file handles to avoid reopening overhead.

    Keeps up to `max_open_files` (default 3) files open using an LRU strategy.
    When a file is accessed, it moves to the front of the cache. When the cache
    is full, the least recently used file is closed and removed.

    Features:
    - Thread-safe access to file handles
    - Automatic cleanup of least-recently-used files
    - Support for any file type with proper handlers
    - Explicit close() method for cleanup
    """

    def __init__(self, max_open_files: int = 3):
        """
        Initialize file cache manager.

        Args:
            max_open_files: Maximum number of files to keep open simultaneously
        """
        self.max_open_files = max_open_files
        # file_path -> (file handle, mode)
        self._cache: OrderedDict[str, tuple[Any, str]] = OrderedDict()
        self._handlers: Dict[str, "ExternalArrayHandler"] = {}  # file_path -> handler instance

    def get_or_open(self, file_path: str, handler: "ExternalArrayHandler", mode: str = "r") -> Optional[Any]:
        """
        Get an open file handle from cache, or open it if not cached.

        Args:
            file_path: Path to the file
            handler: Handler instance that knows how to open this file type
            mode: File open mode ('r', 'a', etc.)

        Returns:
            Open file handle, or None if opening failed
        """
        # Normalize path
        file_path = os.path.abspath(file_path) if os.path.exists(file_path) else file_path

        # Check cache first, and validate mode compatibility
        if file_path in self._cache:
            cached_handle, cached_mode = self._cache[file_path]
            # If requested mode is compatible with cached mode, reuse
            if self._is_mode_compatible(cached_mode, mode):
                self._cache.move_to_end(file_path)
                return cached_handle
            # Otherwise, close and reopen with new mode
            # logger.debug(f"Mode change for cached file {file_path}: {cached_mode} -> {mode}. Reopening.")
            try:
                if hasattr(cached_handle, "close"):
                    cached_handle.close()
            except Exception as e:
                logger.debug(f"Error closing cached file {file_path}: {e}")
            del self._cache[file_path]
            if file_path in self._handlers:
                del self._handlers[file_path]

        # Not in cache - try to open it
        try:
            file_handle = handler.open_file_no_cache(file_path, mode)
            if file_handle is None:
                return None

            # Add to cache with mode
            self._cache[file_path] = (file_handle, mode)
            self._handlers[file_path] = handler
            self._cache.move_to_end(file_path)

            # Evict oldest if cache is full
            if len(self._cache) > self.max_open_files:
                self._evict_oldest()

            return file_handle

        except Exception as e:
            logger.debug(f"Failed to open file {file_path}: {e}")
            return None

    def _evict_oldest(self) -> None:
        """Remove the least recently used file from cache."""
        if not self._cache:
            return

        # Get oldest (first) item
        oldest_path, (oldest_handle, _) = self._cache.popitem(last=False)

        # Close the file handle
        try:
            if hasattr(oldest_handle, "close"):
                oldest_handle.close()
        except Exception as e:
            logger.debug(f"Error closing cached file {oldest_path}: {e}")

        # Remove handler reference
        if oldest_path in self._handlers:
            del self._handlers[oldest_path]

    def close_all(self) -> None:
        """Close all cached file handles."""
        for file_path, (file_handle, _) in list(self._cache.items()):
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except Exception as e:
                logger.debug(f"Error closing file {file_path}: {e}")

        self._cache.clear()
        self._handlers.clear()

    def remove(self, file_path: str) -> None:
        """
        Remove a specific file from cache and close it.

        Args:
            file_path: Path to the file to remove
        """
        file_path = os.path.abspath(file_path) if os.path.exists(file_path) else file_path

        if file_path in self._cache:
            file_handle, _ = self._cache.pop(file_path)
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except Exception as e:
                logger.debug(f"Error closing file {file_path}: {e}")

        if file_path in self._handlers:
            del self._handlers[file_path]

    def __len__(self) -> int:
        """Return number of cached files."""
        return len(self._cache)

    def __contains__(self, file_path: str) -> bool:
        """Check if a file is in cache."""
        file_path = os.path.abspath(file_path) if os.path.exists(file_path) else file_path
        return file_path in self._cache

    @staticmethod
    def _is_mode_compatible(cached_mode: str, requested_mode: str) -> bool:
        """
        Determine if the cached file mode is compatible with the requested mode.
        'r' is only compatible with 'r'. 'r+' and 'a' are compatible with each other and with 'r+'.
        'w' is never compatible (always destructive).
        """
        # Simplified: treat 'r' as readonly, 'r+', 'a' as read/write, 'w' as destructive
        readonly_modes = {"r"}
        rw_modes = {"r+", "a"}
        destructive_modes = {"w", "w+", "x"}

        # logger.debug(f"Checking mode compatibility: cached_mode={cached_mode}, requested_mode={requested_mode}")

        result = False

        if cached_mode in destructive_modes or requested_mode in destructive_modes:
            result = False
        if cached_mode in readonly_modes and requested_mode in readonly_modes:
            result = True
        if cached_mode in rw_modes and (requested_mode in rw_modes or requested_mode in readonly_modes):
            result = True

        # logger.debug(f"\tMode compatibility result: {result}")

        return result


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

    def __init__(self, max_open_files: int = 3):
        self.file_cache = FileCacheManager(max_open_files=max_open_files)

    def close(self) -> None:
        """Close every file handle this handler still holds open."""
        cache = getattr(self, "file_cache", None)
        if cache is not None:
            cache.close_all()

    def __del__(self):
        # The cache is per-handler and owns its handles, so releasing the handler must release
        # them. Nothing used to do it: the read methods wrapped the *cached* handle in `with`,
        # which closed a handle the cache went on serving — the next read on the same file then
        # failed with "invalid identifier type to function". Closing here instead keeps the
        # handles valid for as long as the handler lives, and still frees them afterwards
        # (on Windows an open HDF5 handle keeps the file locked).
        try:
            self.close()
        except Exception:  # interpreter shutdown can pull the rug from under us
            pass

    def __enter__(self) -> "ExternalArrayHandler":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

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

    #: Human-readable name of the format, used in the diagnostics of :meth:`open_file_no_cache`.
    format_name: str = "file"

    def _open_file(self, file_path: str, mode: str = "r") -> Optional[Any]:
        """
        Open *file_path* with the underlying library, letting any failure propagate.

        This is the **only** thing a concrete handler has to provide: the error handling and the
        diagnostic message are shared, in :meth:`open_file_no_cache`. Each of the five real
        handlers used to carry its own copy of the same four-line try / log / return-None block,
        two of which were byte-for-byte identical, and one of which had had its log commented out
        — so an unreadable HDF5 file failed with no message at all.

        Args:
            file_path: Path to the file
            mode: File open mode
        Returns:
            Open file handle, or None when this handler cannot open files at all
        """
        raise NotImplementedError

    def open_file_no_cache(self, file_path: str, mode: str = "r") -> Optional[Any]:
        """
        Open a file without using the cache. This is for handlers that manage their own file handles.

        Args:
            file_path: Path to the file
            mode: File open mode
        Returns:
            Open file handle, or None if opening failed
        """
        try:
            return self._open_file(file_path, mode)
        except Exception as e:
            logger.error("Failed to open %s file %s: %s", self.format_name, file_path, e)
            return None


# @dataclass
# class ETPReader(DatasetReader):
#     def read_array(self, obj_uri: str, path_in_external_file: str) -> Optional[np.ndarray]:
#         return None

#     def get_array_dimension(self, source: str, path_in_external_file: str) -> Optional[np.ndarray]:
#         return None


#: Public API of this module. Declared explicitly so that renaming or removing anything
#: else is not a breaking change, and so `from ... import *` does not leak the imports.
__all__ = [
    "DatasetReader",
    "FileCacheManager",
    "ExternalArrayHandler",
]
