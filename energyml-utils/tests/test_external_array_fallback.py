"""External-array reading must never fail silently, and an empty export must not be written.

A representation whose external arrays cannot be read still produces patches — with zero points.
Nothing said so: the failure was logged at DEBUG, the patches came back empty, and the exporter
wrote a valid but useless ``{"type": "FeatureCollection", "features": []}``.

That is what an ``h5py`` + ``numpy>=2`` pair did to *every* HDF5 array, because
``np.array(dataset, copy=False)`` changed meaning in NumPy 2.0: it used to mean "avoid a copy if
possible" and now means "never copy — raise if you would have to". An HDF5 dataset lives on disk,
so the read always has to allocate.
"""

import os
import tempfile

import numpy as np
import pytest

from energyml.utils.data.export import ExportFormat, EmptyMeshError, drop_empty_patches, export_mesh
from energyml.utils.data.mesh_numpy import NumpyMultiMesh, NumpyPointSetMesh, NumpySurfaceMesh
from energyml.utils.data.crs import PointFrame
from energyml.utils.epc_file import _read_array_from_handler


class _Handler:
    """Duck-typed array handler recording which of its two entry points were used."""

    def __init__(self, view_result=None, view_raises=False, read_result=None, read_raises=False):
        self.view_result, self.view_raises = view_result, view_raises
        self.read_result, self.read_raises = read_result, read_raises
        self.calls = []

    def read_array_view(self, file_path, path, start_indices=None, counts=None):
        self.calls.append("view")
        if self.view_raises:
            raise ValueError("Dataset.__array__ received copy=False but memory allocation cannot be avoided")
        return self.view_result

    def read_array(self, file_path, path, start_indices=None, counts=None):
        self.calls.append("read")
        if self.read_raises:
            raise OSError("unreadable")
        return self.read_result


class TestViewFailureFallsBackToAPlainRead:
    def test_a_raising_view_falls_back_to_read_array(self):
        """The zero-copy view is an optimisation — losing it must not lose the data.

        This is the exact numpy>=2 failure: the view raises for every candidate file, and the
        array used to come back as None.
        """
        data = np.arange(6.0).reshape(2, 3)
        handler = _Handler(view_raises=True, read_result=data)
        result = _read_array_from_handler(handler, "f.h5", "/points")
        np.testing.assert_array_equal(result, data)
        assert handler.calls == ["view", "read"], "the same file must be retried, not skipped"

    def test_a_view_returning_none_falls_back_too(self):
        data = np.arange(3.0)
        handler = _Handler(view_result=None, read_result=data)
        np.testing.assert_array_equal(_read_array_from_handler(handler, "f.h5", "/p"), data)
        assert handler.calls == ["view", "read"]

    def test_a_working_view_is_used_as_is(self):
        data = np.arange(3.0)
        handler = _Handler(view_result=data, read_result=np.zeros(3))
        np.testing.assert_array_equal(_read_array_from_handler(handler, "f.h5", "/p"), data)
        assert handler.calls == ["view"], "no need to read twice when the view worked"

    def test_both_failing_returns_none_without_raising(self):
        handler = _Handler(view_raises=True, read_raises=True)
        assert _read_array_from_handler(handler, "f.h5", "/p") is None


def _hdf5_sample(tmp_name: str = "sample.h5"):
    """Write a small HDF5 file and return ``(path, handler, expected_array)``."""
    h5py = pytest.importorskip("h5py")
    from energyml.utils.data.datasets_io import get_handler_registry

    expected = np.arange(12.0).reshape(4, 3)
    path = os.path.join(tempfile.mkdtemp(), tmp_name)
    with h5py.File(path, "w") as f:
        f.create_dataset("/grp/points", data=expected)
    return path, get_handler_registry().get_handler_for_file(path), expected


class TestReadArrayViewIsNumpy2Safe:
    def test_the_view_does_not_ask_numpy_never_to_copy(self, monkeypatch):
        """Reproduce the NumPy 2 contract on any NumPy: ``copy=False`` must never be used.

        Under NumPy 2, ``np.array(x, copy=False)`` raises instead of copying when a copy is
        unavoidable — which it always is for an HDF5 dataset. Making the stub raise pins the
        behaviour without needing a NumPy 2 interpreter.
        """
        path, handler, expected = _hdf5_sample("nocopy.h5")
        real_array = np.array

        def strict_array(obj, *args, **kwargs):
            if kwargs.get("copy", True) is False:
                raise ValueError(
                    "Dataset.__array__ received copy=False but memory allocation cannot be avoided on read"
                )
            return real_array(obj, *args, **kwargs)

        monkeypatch.setattr(np, "array", strict_array)
        np.testing.assert_array_equal(handler.read_array_view(path, "/grp/points"), expected)

    def test_reading_a_real_hdf5_array_returns_the_values(self):
        path, handler, expected = _hdf5_sample()
        np.testing.assert_array_equal(handler.read_array_view(path, "/grp/points"), expected)
        np.testing.assert_array_equal(handler.read_array(path, "/grp/points"), expected)


class TestTheFileCacheKeepsItsHandlesUsable:
    """The cache owns the handle; a consumer must not be able to close it."""

    def test_reading_twice_works_in_either_order(self):
        path, handler, expected = _hdf5_sample("twice.h5")
        # read_array first used to close the cached handle, so the following view raised
        # "invalid identifier type to function".
        np.testing.assert_array_equal(handler.read_array(path, "/grp/points"), expected)
        np.testing.assert_array_equal(handler.read_array_view(path, "/grp/points"), expected)

        path2, handler2, expected2 = _hdf5_sample("twice2.h5")
        np.testing.assert_array_equal(handler2.read_array_view(path2, "/grp/points"), expected2)
        np.testing.assert_array_equal(handler2.read_array(path2, "/grp/points"), expected2)


class TestEmptyExportsAreRefused:
    @staticmethod
    def _empty_surface():
        return NumpySurfaceMesh(
            identifier="empty",
            points=np.empty((0, 3), dtype=np.float64),
            faces=np.empty(0, dtype=np.int64),
            frame=PointFrame.PROJECTED,
        )

    @staticmethod
    def _filled_points():
        return NumpyPointSetMesh(
            identifier="filled",
            points=np.arange(9.0).reshape(3, 3),
            frame=PointFrame.PROJECTED,
        )

    def test_empty_patches_are_dropped(self):
        kept = drop_empty_patches(NumpyMultiMesh(patches=[self._empty_surface(), self._filled_points()]))
        assert [m.identifier for m in kept] == ["filled"]

    def test_all_empty_raises_instead_of_returning_nothing(self):
        with pytest.raises(EmptyMeshError, match="Nothing to export"):
            drop_empty_patches(NumpyMultiMesh(patches=[self._empty_surface()]), raise_when_empty=True)

    def test_export_mesh_refuses_to_write_an_empty_file(self):
        """The reported symptom: a 54-byte GeoJSON with an empty feature list."""
        path = os.path.join(tempfile.mkdtemp(), "out.geojson")
        with pytest.raises(EmptyMeshError):
            export_mesh(NumpyMultiMesh(patches=[self._empty_surface()]), path, format=ExportFormat.GEOJSON)
        assert not os.path.exists(path), "no file must be left behind when there is nothing to write"

    def test_export_mesh_keeps_the_readable_patches(self):
        """A partially readable object must export what it has, without the empty patches."""
        import json

        path = os.path.join(tempfile.mkdtemp(), "out.geojson")
        export_mesh(
            NumpyMultiMesh(patches=[self._empty_surface(), self._filled_points()]),
            path,
            format=ExportFormat.GEOJSON,
        )
        doc = json.load(open(path, encoding="utf-8"))
        assert len(doc["features"]) == 1
        assert doc["features"][0]["geometry"]["type"] == "MultiPoint"
