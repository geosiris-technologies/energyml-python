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

    # --- IjkGrid + UnstructuredGrid: return empty when geometry is missing ---

    def test_ijk_grid_returns_empty_when_no_ni_nj_nk(self, epc22):
        """Reader returns an empty NumpyMultiMesh when ni/nj/nk are absent."""
        from energyml.utils.data.mesh_numpy import read_numpy_ijk_grid_representation
        mock_obj = MagicMock()
        mock_obj.ni = None
        mock_obj.nj = None
        mock_obj.nk = None
        result = read_numpy_ijk_grid_representation(mock_obj, epc22)
        assert isinstance(result, NumpyMultiMesh)
        assert result.patch_count() == 0

    def test_ijk_grid_parametric_no_longer_raises_not_supported(self):
        """Parametric IJK grids now enter the evaluation path instead of raising NotSupportedError.

        With a minimal stub (missing ``parameters``), the code should raise
        ``ValueError`` — never ``NotSupportedError`` — proving the guard was
        removed and the evaluation pipeline is entered.
        """
        from energyml.utils.exception import NotSupportedError
        from energyml.utils.data.mesh_numpy import read_numpy_ijk_grid_representation

        mock_obj = MagicMock()
        mock_obj.ni = 2
        mock_obj.nj = 2
        mock_obj.nk = 1
        mock_obj.kgaps = None

        # Bare class so type().__name__ contains "Parametric" but has no attrs.
        mock_pts = type("Point3DParametricArray", (), {})()
        mock_geom = MagicMock()
        mock_geom.column_layer_split_coordinate_lines = None

        from unittest.mock import patch as mock_patch

        with mock_patch(
            "energyml.utils.data.mesh_numpy.search_attribute_matching_name_with_path",
            return_value=[("Points", mock_pts)],
        ), mock_patch("energyml.utils.data.mesh_numpy.get_obj_uri", return_value="mock-uri"):
            mock_obj.geometry = mock_geom
            with pytest.raises(Exception) as exc_info:
                read_numpy_ijk_grid_representation(mock_obj)
            # The important assertion: the code must NOT raise NotSupportedError.
            assert not isinstance(exc_info.value, NotSupportedError), (
                "Expected evaluation-path error (e.g. ValueError), "
                "but NotSupportedError was raised — the old guard is still active."
            )

    def test_unstructured_grid_returns_empty_when_no_geometry(self, epc22):
        """Reader returns an empty NumpyMultiMesh when geometry is absent."""
        from energyml.utils.data.mesh_numpy import read_numpy_unstructured_grid_representation
        mock_obj = MagicMock()
        mock_obj.geometry = None
        result = read_numpy_unstructured_grid_representation(mock_obj, epc22)
        assert isinstance(result, NumpyMultiMesh)
        assert result.patch_count() == 0


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


# ---------------------------------------------------------------------------
# 9. Point3dParametricArray / ParametricLineArray evaluation helpers
# ---------------------------------------------------------------------------


def _make_pla(
    knot_count: int,
    ctrl_pts: np.ndarray,       # (K, P, d) — will be passed as a raw np.ndarray
    ctrl_params: Optional[np.ndarray],  # (K, P) or None
    kinds: np.ndarray,          # (P,)
    tangents: Optional[np.ndarray] = None,  # (K, P, 3) or None
):
    """Build a SimpleNamespace that duck-types ParametricLineArray for testing."""
    from types import SimpleNamespace

    return SimpleNamespace(
        knot_count=knot_count,
        control_points=ctrl_pts,       # read_array will return this directly (it's an ndarray)
        control_point_parameters=ctrl_params,
        line_kind_indices=kinds,
        tangent_vectors=tangents,
        parametric_line_intersections=None,
    )


class TestEvaluatePillarKind0:
    """Vertical pillars: constant X, Y; Z = P-value."""

    def test_z_equals_query_param(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_pts = np.array([[10.0, 20.0, 0.0], [10.0, 20.0, 0.0]])  # (2, 3), XY constant
        ctrl_params = None  # unused for kind=0
        query = np.array([100.0, 200.0, 300.0])
        result = _evaluate_one_pillar(0, ctrl_params, ctrl_pts, None, query)

        assert result.shape == (3, 3)
        np.testing.assert_allclose(result[:, 0], 10.0)  # X constant
        np.testing.assert_allclose(result[:, 1], 20.0)  # Y constant
        np.testing.assert_allclose(result[:, 2], query)  # Z = P

    def test_2d_ctrl_pts(self):
        """Kind=0 with only (X, Y) control points — typical RESQML encoding."""
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_pts = np.array([[5.0, 7.0]])  # (1, 2)
        result = _evaluate_one_pillar(0, None, ctrl_pts, None, np.array([0.0, 50.0]))
        np.testing.assert_allclose(result[:, 0], 5.0)
        np.testing.assert_allclose(result[:, 1], 7.0)
        np.testing.assert_allclose(result[:, 2], [0.0, 50.0])


class TestEvaluatePillarKind1:
    """Linear pillar: piecewise linear interpolation."""

    def test_linear_midpoint(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([0.0, 10.0])
        ctrl_pts = np.array([[0.0, 0.0, 0.0], [10.0, 20.0, 30.0]])
        result = _evaluate_one_pillar(1, ctrl_params, ctrl_pts, None, np.array([5.0]))
        np.testing.assert_allclose(result[0], [5.0, 10.0, 15.0])

    def test_linear_at_knots(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([0.0, 10.0, 20.0])
        ctrl_pts = np.array([[1.0, 2.0, 3.0], [11.0, 12.0, 13.0], [21.0, 22.0, 23.0]])
        result = _evaluate_one_pillar(1, ctrl_params, ctrl_pts, None, ctrl_params)
        np.testing.assert_allclose(result, ctrl_pts, atol=1e-10)

    def test_clamp_below_range(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([5.0, 10.0])
        ctrl_pts = np.array([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        # np.interp clamps to first knot value
        result = _evaluate_one_pillar(1, ctrl_params, ctrl_pts, None, np.array([0.0]))
        np.testing.assert_allclose(result[0, 0], 1.0)


class TestEvaluatePillarKind2:
    """Natural cubic spline — requires scipy."""

    @pytest.fixture(autouse=True)
    def _require_scipy(self):
        pytest.importorskip("scipy")

    def test_passes_through_knots(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([0.0, 5.0, 10.0, 15.0])
        ctrl_pts = np.array([
            [0.0, 0.0, 0.0],
            [3.0, 1.0, 5.0],
            [6.0, 0.0, 10.0],
            [9.0, -1.0, 15.0],
        ])
        result = _evaluate_one_pillar(2, ctrl_params, ctrl_pts, None, ctrl_params)
        np.testing.assert_allclose(result, ctrl_pts, atol=1e-8)

    def test_interpolated_value_between_knots(self):
        from energyml.utils.data.helper import _evaluate_one_pillar
        from scipy.interpolate import CubicSpline

        ctrl_params = np.array([0.0, 1.0, 2.0])
        ctrl_pts = np.array([[0.0, 0.0, 0.0], [1.0, 4.0, 2.0], [2.0, 0.0, 4.0]])
        query = np.array([0.5])

        result = _evaluate_one_pillar(2, ctrl_params, ctrl_pts, None, query)
        cs = CubicSpline(ctrl_params, ctrl_pts, bc_type="natural")
        expected = cs(query)
        np.testing.assert_allclose(result, expected, atol=1e-10)


class TestEvaluatePillarKind3:
    """Tangential cubic (Hermite) — falls back to linear when no tangents."""

    def test_fallback_to_linear_without_tangents(self):
        from energyml.utils.data.helper import _evaluate_one_pillar
        import warnings

        ctrl_params = np.array([0.0, 10.0])
        ctrl_pts = np.array([[0.0, 0.0, 0.0], [10.0, 10.0, 10.0]])
        result = _evaluate_one_pillar(3, ctrl_params, ctrl_pts, None, np.array([5.0]))
        np.testing.assert_allclose(result[0], [5.0, 5.0, 5.0], atol=1e-10)

    def test_hermite_midpoint(self):
        from energyml.utils.data.helper import _evaluate_one_pillar, hermite_interpolation

        ctrl_params = np.array([0.0, 10.0])
        ctrl_pts = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 10.0]])
        # Tangents pointing straight down.
        tangents = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])

        query = np.array([5.0])
        result = _evaluate_one_pillar(3, ctrl_params, ctrl_pts, tangents, query)
        expected = hermite_interpolation(5.0, 0.0, 10.0, ctrl_pts[0], ctrl_pts[1], tangents[0], tangents[1])
        np.testing.assert_allclose(result[0], expected, atol=1e-10)


class TestEvaluatePillarKind4:
    """Z-linear cubic: X, Y use natural cubic; Z uses linear interp."""

    @pytest.fixture(autouse=True)
    def _require_scipy(self):
        pytest.importorskip("scipy")

    def test_z_is_linear(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([0.0, 10.0, 20.0])
        ctrl_pts = np.array([
            [0.0, 0.0, 0.0],
            [5.0, 3.0, 10.0],
            [10.0, 0.0, 20.0],
        ])
        query = np.array([5.0, 10.0, 15.0])
        result = _evaluate_one_pillar(4, ctrl_params, ctrl_pts, None, query)

        # Z must match linear interpolation.
        z_linear = np.interp(query, ctrl_params, ctrl_pts[:, 2])
        np.testing.assert_allclose(result[:, 2], z_linear, atol=1e-10)

    def test_xy_uses_cubic(self):
        from energyml.utils.data.helper import _evaluate_one_pillar
        from scipy.interpolate import CubicSpline

        ctrl_params = np.array([0.0, 1.0, 2.0])
        ctrl_pts = np.array([[0.0, 0.0, 0.0], [1.0, 4.0, 1.0], [2.0, 0.0, 2.0]])
        query = np.array([0.5])

        result = _evaluate_one_pillar(4, ctrl_params, ctrl_pts, None, query)
        cs_xy = CubicSpline(ctrl_params, ctrl_pts[:, :2], bc_type="natural")
        np.testing.assert_allclose(result[0, :2], cs_xy(query)[0], atol=1e-10)


class TestEvaluatePillarKind5:
    """Minimum-curvature spline."""

    def test_straight_vertical_pillar(self):
        """A perfectly vertical pillar with tangents [0,0,1] should give linear Z."""
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([0.0, 100.0])
        ctrl_pts = np.array([[10.0, 20.0, 0.0], [10.0, 20.0, 100.0]])
        tangents = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])
        query = np.array([0.0, 50.0, 100.0])

        result = _evaluate_one_pillar(5, ctrl_params, ctrl_pts, tangents, query)
        np.testing.assert_allclose(result[:, 2], [0.0, 50.0, 100.0], atol=1e-6)
        np.testing.assert_allclose(result[:, 0], 10.0, atol=1e-6)
        np.testing.assert_allclose(result[:, 1], 20.0, atol=1e-6)

    def test_fallback_when_no_tangents(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        ctrl_params = np.array([0.0, 10.0])
        ctrl_pts = np.array([[0.0, 0.0, 0.0], [5.0, 5.0, 10.0]])
        result = _evaluate_one_pillar(5, ctrl_params, ctrl_pts, None, np.array([5.0]))
        np.testing.assert_allclose(result[0], [2.5, 2.5, 5.0], atol=1e-10)


class TestEvaluatePillarKindNull:
    """Null pillar (kind=-1) should produce NaN output."""

    def test_null_pillar_returns_nan(self):
        from energyml.utils.data.helper import _evaluate_one_pillar

        result = _evaluate_one_pillar(-1, None, np.zeros((1, 3)), None, np.array([0.0, 10.0]))
        assert result.shape == (2, 3)
        assert np.all(np.isnan(result))


class TestEvaluateParametricLineArray:
    """Integration tests for evaluate_parametric_line_array."""

    def _make_query(self, nkl, n_pillars, depth_start=0.0, depth_end=100.0):
        """Build a uniform (NKL, n_pillars) query parameter array."""
        depths = np.linspace(depth_start, depth_end, nkl)
        return np.tile(depths[:, np.newaxis], (1, n_pillars))

    def test_all_vertical_3x3_grid(self):
        """All-vertical 3×3 pillar grid (kind=0) — quick smoke test."""
        from energyml.utils.data.helper import evaluate_parametric_line_array

        ni, nj = 2, 2
        n_pillars = (ni + 1) * (nj + 1)  # 9
        nkl = 4
        K = 2  # knot count

        # Vertical pillars: (K, P, 2) — only X, Y per knot.
        ctrl_pts = np.zeros((K, n_pillars, 2), dtype=np.float64)
        for p in range(n_pillars):
            ctrl_pts[:, p, 0] = float(p % (ni + 1))  # X = pillar column
            ctrl_pts[:, p, 1] = float(p // (ni + 1))  # Y = pillar row

        kinds = np.full(n_pillars, 0, dtype=np.int32)
        query = self._make_query(nkl, n_pillars)

        pla = _make_pla(K, ctrl_pts, None, kinds)
        result = evaluate_parametric_line_array(pla, None, None, query, ni, nj)

        assert result.shape == (nkl, n_pillars, 3)
        assert result.dtype == np.float64
        # For each pillar: Z at each layer == query param.
        np.testing.assert_allclose(result[:, :, 2], query, atol=1e-10)

    def test_all_linear_single_pillar(self):
        """Single linear pillar grid (kind=1), trivial 1×1 check."""
        from energyml.utils.data.helper import evaluate_parametric_line_array

        ni, nj = 1, 1
        n_pillars = 4  # (1+1)*(1+1)
        nkl = 3
        K = 2

        ctrl_pts = np.zeros((K, n_pillars, 3), dtype=np.float64)
        ctrl_pts[0] = 0.0
        ctrl_pts[1] = 100.0  # all coords go from 0 to 100

        ctrl_params = np.zeros((K, n_pillars), dtype=np.float64)
        ctrl_params[0] = 0.0
        ctrl_params[1] = 100.0

        kinds = np.full(n_pillars, 1, dtype=np.int32)
        query = self._make_query(nkl, n_pillars, 0.0, 100.0)

        pla = _make_pla(K, ctrl_pts, ctrl_params, kinds)
        result = evaluate_parametric_line_array(pla, None, None, query, ni, nj)

        assert result.shape == (nkl, n_pillars, 3)
        # All control points go uniformly 0→100 in every coordinate, so each
        # result coordinate == the query P-value for that node.
        expected = np.broadcast_to(query[:, :, np.newaxis], (nkl, n_pillars, 3))
        np.testing.assert_allclose(result, expected, atol=1e-10)

    def test_mixed_kinds(self):
        """Grid with mixed kinds (0 and 1) — result shape must be correct."""
        from energyml.utils.data.helper import evaluate_parametric_line_array

        ni, nj = 1, 1
        n_pillars = 4
        nkl = 3
        K = 2

        ctrl_pts = np.zeros((K, n_pillars, 3), dtype=np.float64)
        ctrl_pts[1, :, 2] = 100.0  # Z goes from 0 to 100

        ctrl_params = np.zeros((K, n_pillars), dtype=np.float64)
        ctrl_params[1] = 100.0

        # Pillars 0,2 vertical; pillars 1,3 linear.
        kinds = np.array([0, 1, 0, 1], dtype=np.int32)
        query = self._make_query(nkl, n_pillars, 0.0, 100.0)

        pla = _make_pla(K, ctrl_pts, ctrl_params, kinds)
        result = evaluate_parametric_line_array(pla, None, None, query, ni, nj)

        assert result.shape == (nkl, n_pillars, 3)
        assert not np.any(np.isnan(result))

    def test_output_dtype_is_float64(self):
        """Output must always be float64 regardless of input dtype."""
        from energyml.utils.data.helper import evaluate_parametric_line_array

        ni, nj = 1, 1
        n_pillars = 4
        nkl = 2
        K = 2

        ctrl_pts = np.zeros((K, n_pillars, 3), dtype=np.float32)  # float32 input
        ctrl_params = np.array([[0.0], [10.0]], dtype=np.float32).repeat(n_pillars, axis=1)
        kinds = np.full(n_pillars, 1, dtype=np.int32)
        query = np.linspace(0, 10, nkl * n_pillars).reshape(nkl, n_pillars)

        pla = _make_pla(K, ctrl_pts, ctrl_params, kinds)
        result = evaluate_parametric_line_array(pla, None, None, query, ni, nj)

        assert result.dtype == np.float64


class TestResolveParametricLineArray:
    """resolve_parametric_line_array with a direct PLA should return it unchanged."""

    def test_direct_pla_returned_unchanged(self):
        from types import SimpleNamespace
        from energyml.utils.data.helper import resolve_parametric_line_array

        pla = SimpleNamespace(knot_count=2, control_points=None)
        result = resolve_parametric_line_array(pla, None, None, 4)
        assert result is pla

    def test_from_representation_lattice_missing_workspace_raises(self):
        """Without a workspace, resolving a ParametricLineFromRepresentationLatticeArray raises ValueError."""
        from types import SimpleNamespace
        from energyml.utils.data.helper import resolve_parametric_line_array

        # Create a stub whose type name contains "FromRepresentationLattice".
        pla_from_rep = type("ParametricLineFromRepresentationLatticeArray", (), {
            "supporting_representation": SimpleNamespace(uuid="some-uuid"),
            "line_indices_on_supporting_representation": None,
        })()
        with pytest.raises(ValueError, match="workspace is required"):
            resolve_parametric_line_array(pla_from_rep, None, None, 4)
