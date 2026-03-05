"""Tests for the zero-copy numpy mesh reader (mesh_numpy.py).

Covers:
* NumpyMesh dataclass field shapes/dtypes.
* crs_displacement_np — vectorised CRS offset + Z-flip.
* _ViewWorkspace — routing of read_array to read_array_view.
* HDF5ArrayHandler.read_array_view — best-effort zero-copy.
* End-to-end read_numpy_mesh_object for all supported representation types,
  using the EPC/HDF5 fixtures already present in ``rc/epc/``.
* numpy_mesh_to_pyvista round-trip (requires pyvista; skipped otherwise).

Run from the workspace root:
    poetry run pytest tests/test_mesh_numpy.py -v
"""
import os
import tempfile
from typing import Optional
from unittest.mock import MagicMock

import numpy as np
import pytest

from energyml.utils.data.mesh_numpy import (
    NumpyMesh,
    NumpyMultiMesh,
    NumpyPointSetMesh,
    NumpyPolylineMesh,
    NumpySurfaceMesh,
    NumpyVolumeMesh,
    _ViewWorkspace,
    _build_vtk_faces_from_triangles,
    _build_vtk_faces_from_quads,
    _build_vtk_lines_from_segments,
    _ensure_float64_points,
    crs_displacement_np,
    read_numpy_mesh_object,
    numpy_mesh_to_pyvista,
    numpy_multi_mesh_to_pyvista,
)

# ---------------------------------------------------------------------------
# Paths helpers
# ---------------------------------------------------------------------------

_WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EPC_DIR = os.path.join(_WORKSPACE_ROOT, "rc", "epc")
_EPC22 = os.path.join(_EPC_DIR, "testingPackageCpp22.epc")
_EPC20 = os.path.join(_EPC_DIR, "testingPackageCpp.epc")


def _epc22_available() -> bool:
    return os.path.isfile(_EPC22)


def _epc20_available() -> bool:
    return os.path.isfile(_EPC20)


# ---------------------------------------------------------------------------
# 1. Dataclass shape / dtype invariants
# ---------------------------------------------------------------------------

class TestNumpyMeshDataclasses:
    def test_point_set_defaults(self):
        m = NumpyPointSetMesh()
        assert m.points.shape == (0, 3)
        assert m.points.dtype == np.float64

    def test_surface_mesh_defaults(self):
        m = NumpySurfaceMesh()
        assert m.faces.dtype == np.int64
        assert m.faces.ndim == 1

    def test_polyline_mesh_defaults(self):
        m = NumpyPolylineMesh()
        assert m.lines.dtype == np.int64

    def test_volume_mesh_defaults(self):
        m = NumpyVolumeMesh()
        assert m.cells.dtype == np.int64
        assert m.cell_types.dtype == np.uint8

    def test_surface_mesh_populated(self):
        pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
        faces = np.array([3, 0, 1, 2], dtype=np.int64)
        m = NumpySurfaceMesh(points=pts, faces=faces)
        assert m.points.shape == (3, 3)
        assert m.faces[0] == 3  # VTK triangle count prefix


# ---------------------------------------------------------------------------
# 2. _ensure_float64_points
# ---------------------------------------------------------------------------

class TestEnsureFloat64Points:
    def test_flat_list(self):
        a = _ensure_float64_points([1, 2, 3, 4, 5, 6])
        assert a.shape == (2, 3)
        assert a.dtype == np.float64

    def test_nested_list(self):
        a = _ensure_float64_points([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        assert a.shape == (2, 3)
        assert a.dtype == np.float64

    def test_already_correct_array(self):
        arr = np.zeros((5, 3), dtype=np.float64)
        result = _ensure_float64_points(arr)
        # Should return a view (same data, no copy)
        assert result.shape == (5, 3)
        assert result.dtype == np.float64

    def test_wrong_col_count_raises(self):
        with pytest.raises(ValueError):
            _ensure_float64_points(np.zeros((4, 5)))  # 5 cols is never valid

    def test_2d_points_padded_with_zeros(self):
        a = _ensure_float64_points(np.array([[1.0, 2.0], [3.0, 4.0]]))
        assert a.shape == (2, 3)
        np.testing.assert_array_equal(a[:, 2], [0.0, 0.0])


# ---------------------------------------------------------------------------
# 3. VTK connectivity builders
# ---------------------------------------------------------------------------

class TestVTKBuilders:
    def test_faces_from_triangles(self):
        tri = np.array([[0, 1, 2], [1, 2, 3]], dtype=np.int64)
        faces = _build_vtk_faces_from_triangles(tri)
        expected = np.array([3, 0, 1, 2, 3, 1, 2, 3], dtype=np.int64)
        np.testing.assert_array_equal(faces, expected)

    def test_faces_from_quads(self):
        quad = np.array([[0, 1, 2, 3]], dtype=np.int64)
        faces = _build_vtk_faces_from_quads(quad)
        expected = np.array([4, 0, 1, 2, 3], dtype=np.int64)
        np.testing.assert_array_equal(faces, expected)

    def test_lines_from_segments_3pts(self):
        lines = _build_vtk_lines_from_segments(3)
        # [2, 0, 1,  2, 1, 2]
        expected = np.array([2, 0, 1, 2, 1, 2], dtype=np.int64)
        np.testing.assert_array_equal(lines, expected)

    def test_lines_from_segments_1pt(self):
        lines = _build_vtk_lines_from_segments(1)
        assert len(lines) == 0

    def test_lines_from_segments_0pts(self):
        lines = _build_vtk_lines_from_segments(0)
        assert len(lines) == 0


# ---------------------------------------------------------------------------
# 4. crs_displacement_np
# ---------------------------------------------------------------------------

class TestCrsDisplacementNp:
    def _make_crs(self, x=0.0, y=0.0, z=0.0, z_reversed=False):
        """Build a minimal mock CRS object."""
        from unittest.mock import patch

        crs = MagicMock()

        # Patch the helper functions used by crs_displacement_np
        return crs, [x, y, z], z_reversed

    def test_offset_only(self):
        """Test pure XYZ offset without Z reversal."""
        pts = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float64)
        crs = MagicMock()

        # Patch helper functions at the module level
        import energyml.utils.data.mesh_numpy as mn
        orig_offset = mn.get_crs_origin_offset
        orig_zrev = mn.is_z_reversed
        try:
            mn.get_crs_origin_offset = lambda crs_obj: [10.0, 20.0, 30.0]
            mn.is_z_reversed = lambda crs_obj: False
            result = crs_displacement_np(pts.copy(), crs)
        finally:
            mn.get_crs_origin_offset = orig_offset
            mn.is_z_reversed = orig_zrev

        np.testing.assert_allclose(result, [[11.0, 22.0, 33.0], [14.0, 25.0, 36.0]])

    def test_z_reversal(self):
        """Test Z-axis inversion."""
        pts = np.array([[0.0, 0.0, 100.0]], dtype=np.float64)
        crs = MagicMock()

        import energyml.utils.data.mesh_numpy as mn
        orig_offset = mn.get_crs_origin_offset
        orig_zrev = mn.is_z_reversed
        try:
            mn.get_crs_origin_offset = lambda crs_obj: [0.0, 0.0, 0.0]
            mn.is_z_reversed = lambda crs_obj: True
            result = crs_displacement_np(pts.copy(), crs)
        finally:
            mn.get_crs_origin_offset = orig_offset
            mn.is_z_reversed = orig_zrev

        assert result[0, 2] == pytest.approx(-100.0)

    def test_inplace_false_no_mutation(self):
        """inplace=False must not mutate the original array."""
        pts = np.array([[1.0, 2.0, 3.0]], dtype=np.float64)
        original = pts.copy()
        crs = MagicMock()

        import energyml.utils.data.mesh_numpy as mn
        orig_offset = mn.get_crs_origin_offset
        orig_zrev = mn.is_z_reversed
        try:
            mn.get_crs_origin_offset = lambda crs_obj: [1.0, 1.0, 1.0]
            mn.is_z_reversed = lambda crs_obj: False
            result = crs_displacement_np(pts, crs, inplace=False)
        finally:
            mn.get_crs_origin_offset = orig_offset
            mn.is_z_reversed = orig_zrev

        np.testing.assert_array_equal(pts, original, err_msg="Source array was mutated despite inplace=False")
        np.testing.assert_allclose(result, [[2.0, 3.0, 4.0]])

    def test_none_crs_returns_unchanged(self):
        pts = np.array([[1.0, 2.0, 3.0]], dtype=np.float64)
        result = crs_displacement_np(pts, None)
        np.testing.assert_array_equal(result, pts)


# ---------------------------------------------------------------------------
# 5. _ViewWorkspace
# ---------------------------------------------------------------------------

class TestViewWorkspace:
    def test_read_array_redirects_to_view(self):
        """read_array on _ViewWorkspace should call read_array_view on the wrapped ws."""
        ws = MagicMock()
        ws.read_array_view.return_value = np.array([1, 2, 3])
        ws.some_other_attr = "hello"

        view_ws = _ViewWorkspace(ws)
        # read_array calls must be redirected
        result = view_ws.read_array("proxy", "path/in/h5", None, None, None)
        ws.read_array_view.assert_called_once_with("proxy", "path/in/h5", None, None, None)
        np.testing.assert_array_equal(result, [1, 2, 3])

    def test_other_attrs_forwarded(self):
        ws = MagicMock()
        ws.some_method.return_value = 42
        view_ws = _ViewWorkspace(ws)
        assert view_ws.some_method() == 42


# ---------------------------------------------------------------------------
# 6. HDF5ArrayHandler.read_array_view
# ---------------------------------------------------------------------------

class TestHDF5ArrayHandlerReadArrayView:
    """Verify zero-copy semantics of read_array_view vs read_array."""

    @pytest.fixture
    def h5_with_contiguous_dataset(self, tmp_path):
        """Create a small HDF5 file with a contiguous (non-chunked) dataset."""
        h5py = pytest.importorskip("h5py")
        fpath = str(tmp_path / "test_view.h5")
        arr = np.arange(12, dtype=np.float64).reshape(4, 3)
        with h5py.File(fpath, "w") as f:
            # contiguous layout — default when no chunks specified
            f.create_dataset("/pts", data=arr, chunks=None)
        return fpath, arr

    def test_read_array_view_returns_correct_data(self, h5_with_contiguous_dataset):
        from energyml.utils.data.datasets_io import HDF5ArrayHandler
        fpath, expected = h5_with_contiguous_dataset
        handler = HDF5ArrayHandler()
        result = handler.read_array_view(fpath, "/pts")
        handler.file_cache.close_all()
        assert result is not None
        np.testing.assert_allclose(result, expected)

    def test_read_array_view_is_ndarray(self, h5_with_contiguous_dataset):
        from energyml.utils.data.datasets_io import HDF5ArrayHandler
        fpath, _ = h5_with_contiguous_dataset
        handler = HDF5ArrayHandler()
        result = handler.read_array_view(fpath, "/pts")
        handler.file_cache.close_all()
        assert isinstance(result, np.ndarray)

    def test_subselection_correct(self, h5_with_contiguous_dataset):
        from energyml.utils.data.datasets_io import HDF5ArrayHandler
        fpath, expected = h5_with_contiguous_dataset
        handler = HDF5ArrayHandler()
        # Select rows 1 and 2 (start=1, count=2 along axis-0)
        result = handler.read_array_view(fpath, "/pts", start_indices=[1, 0], counts=[2, 3])
        handler.file_cache.close_all()
        np.testing.assert_allclose(result, expected[1:3])

    def test_storage_interface_default_fallback(self):
        """EnergymlStorageInterface.read_array_view must call read_array by default."""
        from energyml.utils.storage_interface import EnergymlStorageInterface

        class _Concrete(EnergymlStorageInterface):
            """Minimal concrete subclass that does NOT override read_array_view."""
            def get_object(self, identifier): return None
            def get_object_by_uuid(self, uuid): return []
            def put_object(self, obj, dataspace=None): return None
            def delete_object(self, identifier): return False
            def read_array(self, proxy, path, start=None, counts=None, uri=None):
                return np.array([99.0])
            def write_array(self, *a, **kw): return False
            def get_array_metadata(self, *a, **kw): return None
            def list_objects(self, *a, **kw): return []
            def get_obj_rels(self, obj): return []
            def close(self): pass

        ws = _Concrete()
        result = ws.read_array_view("p", "path")
        np.testing.assert_array_equal(result, [99.0])


# ---------------------------------------------------------------------------
# 7. End-to-end representation readers (require EPC fixtures)
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _epc22_available(), reason="testingPackageCpp22.epc not found in rc/epc/")
class TestReadNumpyMeshObjectEPC22:
    """Integration tests against testingPackageCpp22.epc."""

    @pytest.fixture(scope="class")
    def epc22(self):
        from energyml.utils.epc import Epc
        return Epc.read_file(_EPC22, read_rels_from_files=False, recompute_rels=False)

    # --- TriangulatedSetRepresentation ---
    def test_triangulated_set_returns_surface_mesh(self, epc22):
        obj = epc22.get_object_by_uuid("6e678338-3b53-49b6-8801-faee493e0c42")
        if not obj:
            pytest.skip("TriangulatedSet UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        assert isinstance(multi, NumpyMultiMesh)
        patches = multi.flat_patches()
        assert patches, "Expected at least one patch"
        for m in patches:
            assert isinstance(m, NumpySurfaceMesh)

    def test_triangulated_set_points_shape_dtype(self, epc22):
        obj = epc22.get_object_by_uuid("6e678338-3b53-49b6-8801-faee493e0c42")
        if not obj:
            pytest.skip("TriangulatedSet UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        for m in multi.flat_patches():
            assert m.points.ndim == 2
            assert m.points.shape[1] == 3
            assert m.points.dtype == np.float64

    def test_triangulated_set_faces_dtype_and_format(self, epc22):
        obj = epc22.get_object_by_uuid("6e678338-3b53-49b6-8801-faee493e0c42")
        if not obj:
            pytest.skip("TriangulatedSet UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        for m in multi.flat_patches():
            assert isinstance(m, NumpySurfaceMesh)
            assert m.faces.dtype == np.int64
            assert m.faces.ndim == 1
            # First element must be 3 (triangle)
            assert m.faces[0] == 3, "VTK face array must start with face vertex count (3 for triangles)"

    def test_triangulated_set_no_lists(self, epc22):
        """Guarantee no Python lists survive into the mesh dataclass."""
        obj = epc22.get_object_by_uuid("6e678338-3b53-49b6-8801-faee493e0c42")
        if not obj:
            pytest.skip("TriangulatedSet UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        for m in multi.flat_patches():
            assert isinstance(m.points, np.ndarray), "points must be ndarray"
            assert isinstance(m.faces, np.ndarray), "faces must be ndarray"

    # --- PointSetRepresentation ---
    def test_pointset_returns_pointset_mesh(self, epc22):
        obj = epc22.get_object_by_uuid("fbc5466c-94cd-46ab-8b48-2ae2162b372f")
        if not obj:
            pytest.skip("PointSet UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        assert isinstance(multi, NumpyMultiMesh)
        patches = multi.flat_patches()
        assert patches
        for m in patches:
            assert isinstance(m, NumpyPointSetMesh)
            assert m.points.ndim == 2
            assert m.points.shape[1] == 3
            assert m.points.dtype == np.float64

    # --- PolylineRepresentation ---
    def test_polyline_returns_polyline_mesh(self, epc22):
        obj = epc22.get_object_by_uuid("a54b8399-d3ba-4d4b-b215-8d4f8f537e66")
        if not obj:
            pytest.skip("Polyline UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        assert isinstance(multi, NumpyMultiMesh)
        patches = multi.flat_patches()
        assert patches
        for m in patches:
            assert isinstance(m, NumpyPolylineMesh)
            assert m.points.dtype == np.float64
            assert m.lines.dtype == np.int64

    # --- WellboreFrameRepresentation ---
    def test_wellbore_frame_returns_polyline(self, epc22):
        obj = epc22.get_object_by_uuid("d873e243-d893-41ab-9a3e-d20b851c099f")
        if not obj:
            pytest.skip("WellboreFrame UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        assert isinstance(multi, NumpyMultiMesh)
        patches = multi.flat_patches()
        assert patches
        for m in patches:
            assert isinstance(m, NumpyPolylineMesh)
            assert m.points.ndim == 2
            assert m.points.shape[1] == 3

    def test_wellbore_frame_lines_vtk_format(self, epc22):
        obj = epc22.get_object_by_uuid("d873e243-d893-41ab-9a3e-d20b851c099f")
        if not obj:
            pytest.skip("WellboreFrame UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        for m in multi.flat_patches():
            assert isinstance(m, NumpyPolylineMesh)
            if len(m.lines) > 0:
                # First element is count (number of points in first line segment)
                assert m.lines[0] == 2, "VTK segment should start with count=2"

    # --- Grid2dRepresentation ---
    def test_grid2d_returns_surface_mesh(self, epc22):
        # Try to find a Grid2dRepresentation in the EPC
        all_objs = epc22.list_objects()
        grid2d_uuids = [
            r.uuid for r in all_objs
            if "Grid2d" in (r.object_type or "")
        ]
        if not grid2d_uuids:
            pytest.skip("No Grid2dRepresentation found in testingPackageCpp22.epc")
        obj = epc22.get_object_by_uuid(grid2d_uuids[0])
        if not obj:
            pytest.skip("Grid2d object not found")
        meshes = read_numpy_mesh_object(obj[0], workspace=epc22)
        for m in meshes:
            assert isinstance(m, NumpySurfaceMesh)
            assert m.points.dtype == np.float64
            if len(m.faces) > 0:
                assert m.faces[0] == 4, "Grid2d quads: first VTK face entry must be 4"

    # --- RepresentationSet ---
    def test_representation_set_returns_mixed_mesh_list(self, epc22):
        obj = epc22.get_object_by_uuid("6b992199-5b47-4624-a62c-b70857133cda")
        if not obj:
            pytest.skip("RepresentationSet UUID not found in fixture EPC")
        multi = read_numpy_mesh_object(obj[0], workspace=epc22)
        assert isinstance(multi, NumpyMultiMesh)
        for m in multi.flat_patches():
            assert isinstance(m, NumpyMesh)

    # --- Stubs raise NotSupportedError ---
    def test_ijk_grid_raises_not_supported(self, epc22):
        from energyml.utils.exception import NotSupportedError
        from energyml.utils.data.mesh_numpy import read_numpy_ijk_grid_representation
        with pytest.raises(NotSupportedError):
            read_numpy_ijk_grid_representation(MagicMock(), epc22)

    def test_unstructured_grid_raises_not_supported(self, epc22):
        from energyml.utils.exception import NotSupportedError
        from energyml.utils.data.mesh_numpy import read_numpy_unstructured_grid_representation
        with pytest.raises(NotSupportedError):
            read_numpy_unstructured_grid_representation(MagicMock(), epc22)


# ---------------------------------------------------------------------------
# 8. numpy_mesh_to_pyvista round-trip
# ---------------------------------------------------------------------------

try:
    import pyvista as _pyvista
    _PYVISTA_AVAILABLE = True
except ImportError:
    _PYVISTA_AVAILABLE = False


@pytest.mark.skipif(not _PYVISTA_AVAILABLE, reason="pyvista not installed")
class TestNumpyMeshToPyvista:
    def test_surface_mesh(self):
        pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
        faces = np.array([3, 0, 1, 2], dtype=np.int64)
        m = NumpySurfaceMesh(points=pts, faces=faces)
        pv_mesh = numpy_mesh_to_pyvista(m)
        import pyvista
        assert isinstance(pv_mesh, pyvista.PolyData)
        assert pv_mesh.n_points == 3
        assert pv_mesh.n_cells == 1

    def test_polyline_mesh(self):
        pts = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]], dtype=np.float64)
        lines = _build_vtk_lines_from_segments(3)
        m = NumpyPolylineMesh(points=pts, lines=lines)
        pv_mesh = numpy_mesh_to_pyvista(m)
        import pyvista
        assert isinstance(pv_mesh, pyvista.PolyData)
        assert pv_mesh.n_points == 3

    def test_point_set_mesh(self):
        pts = np.random.rand(10, 3).astype(np.float64)
        m = NumpyPointSetMesh(points=pts)
        pv_mesh = numpy_mesh_to_pyvista(m)
        import pyvista
        assert isinstance(pv_mesh, pyvista.PolyData)
        assert pv_mesh.n_points == 10

    def test_pyvista_missing_raises_import_error(self, monkeypatch):
        """When pyvista is not importable, numpy_mesh_to_pyvista raises ImportError."""
        import builtins
        real_import = builtins.__import__

        def _mock_import(name, *args, **kwargs):
            if name == "pyvista":
                raise ImportError("mocked missing pyvista")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", _mock_import)
        m = NumpyPointSetMesh()
        with pytest.raises(ImportError, match="pyvista"):
            numpy_mesh_to_pyvista(m)

    def test_to_pyvista_method(self):
        """NumpyMesh.to_pyvista() convenience method."""
        pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
        faces = np.array([3, 0, 1, 2], dtype=np.int64)
        m = NumpySurfaceMesh(points=pts, faces=faces)
        pv_mesh = m.to_pyvista()
        import pyvista
        assert isinstance(pv_mesh, pyvista.PolyData)
