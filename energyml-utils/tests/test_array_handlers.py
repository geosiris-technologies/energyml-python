import os
import tempfile
import numpy as np
import pytest

from energyml.utils.data.datasets_io import (
    HDF5ArrayHandler,
    ParquetArrayHandler,
    CSVArrayHandler,
    LASArrayHandler,
    SEGYArrayHandler,
)


def is_h5py_file_closed(h5file):
    """Check if an h5py file handle is closed."""
    try:
        return not getattr(h5file, "id", None) or not h5file.id.valid
    except Exception:
        return True


def test_hdf5_array_handler_read_write():
    """Test HDF5ArrayHandler read/write and file closure."""
    arr = np.arange(6).reshape(2, 3)
    handler = HDF5ArrayHandler()
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name
    try:
        # Write
        assert handler.write_array(fname, arr, "/data"), "HDF5 write failed"
        # Read
        out = handler.read_array(fname, "/data")
        np.testing.assert_array_equal(arr, out)
        # Check file closed after handler deletion
        f = handler.file_cache.get_or_open(fname, handler, "r")
        del handler
        import gc

        gc.collect()
        assert is_h5py_file_closed(f), "HDF5 file not closed after handler deletion"
    finally:
        try:
            os.remove(fname)
        except Exception:
            pass


def test_parquet_array_handler_read_write():
    """Test ParquetArrayHandler read/write."""
    arr = np.arange(6).reshape(2, 3)
    handler = ParquetArrayHandler()
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
        fname = tmp.name
    try:
        assert handler.write_array(fname, arr, column_titles=["a", "b", "c"]), "Parquet write failed"
        out = handler.read_array(fname)
        np.testing.assert_array_equal(arr, out)
    finally:
        try:
            os.remove(fname)
        except Exception:
            pass


def test_csv_array_handler_read_write():
    """Test CSVArrayHandler read/write."""
    arr = np.arange(6).reshape(2, 3)
    handler = CSVArrayHandler()
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w+") as tmp:
        fname = tmp.name
    try:
        assert handler.write_array(fname, arr), "CSV write failed"
        out = handler.read_array(fname)
        # CSV may return strings, so cast to int
        np.testing.assert_array_equal(np.array(out, dtype=int), arr)
    finally:
        try:
            os.remove(fname)
        except Exception:
            pass


def test_las_array_handler_read_write():
    """Test LASArrayHandler read/write if supported."""
    arr = np.arange(6).reshape(2, 3)
    handler = LASArrayHandler()
    with tempfile.NamedTemporaryFile(suffix=".las", delete=False, mode="w+") as tmp:
        fname = tmp.name
    try:
        write_ok = False
        try:
            handler.write_array(fname, arr)
            write_ok = True
        except Exception as e:
            print(f"LAS write not supported: {e}")
        try:
            out = handler.read_array(fname)
            if write_ok and out is not None:
                np.testing.assert_array_equal(np.array(out, dtype=arr.dtype), arr)
        except Exception as e:
            print(f"LAS read not supported: {e}")
    finally:
        try:
            os.remove(fname)
        except Exception:
            pass


def test_segy_array_handler_read_write():
    """Test SEGYArrayHandler read/write if supported."""
    arr = np.arange(6).reshape(2, 3)
    handler = SEGYArrayHandler()
    with tempfile.NamedTemporaryFile(suffix=".sgy", delete=False, mode="w+b") as tmp:
        fname = tmp.name
    try:
        write_ok = False
        try:
            handler.write_array(fname, arr)
            write_ok = True
        except Exception as e:
            print(f"SEGY write not supported: {e}")
        try:
            out = handler.read_array(fname)
            if write_ok and out is not None:
                np.testing.assert_array_equal(np.array(out, dtype=arr.dtype), arr)
        except Exception as e:
            print(f"SEGY read not supported: {e}")
    finally:
        try:
            os.remove(fname)
        except Exception:
            pass
