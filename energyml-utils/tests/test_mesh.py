"""Regression tests for the fixes applied to mesh.py / mesh_numpy.py.

Each test here pins down a defect that was previously silent:

* ``read_mesh_object`` handed back the energyml objects themselves when given a list.
* ``read_property_interpreted_with_cbt`` raised ``NameError`` on its own error path.
* the numpy readers advanced their ``sub_indices`` window by the *filtered* count, which
  misaligned every patch after the first one.
* the Grid2d axis-count reconciliation could emit indices past the end of the points array.
* the reader dispatchers scanned every module member on each call.
"""
import os

import numpy as np
import pytest

from energyml.utils.data.mesh import (
    AbstractMesh,
    _list_exportable_uuids,
    _mesh_name_mapping,
    get_object_reader_function,
    read_mesh_object,
)
from energyml.utils.data.properties import read_property_interpreted_with_cbt
from energyml.utils.data.mesh_numpy import (
    _fit_grid_dimensions,
    get_numpy_reader_function,
    read_numpy_mesh_object,
)
from energyml.utils.epc_file import EpcAccessMode, EpcFile
from energyml.utils.exception import NotSupportedError

_WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EPC_DIR = os.path.join(_WORKSPACE_ROOT, "rc", "epc")
_EPC22 = os.path.join(_EPC_DIR, "testingPackageCpp22.epc")
_EPC201 = os.path.join(_EPC_DIR, "testingPackageCpp.epc")

#: TriangulatedSetRepresentation of ``testingPackageCpp22.epc``: 5 patches x 4 triangles.
_MULTI_PATCH_UUID = "1a4112fa-c4ef-4c8d-aed0-47d9273bebc5"


requires_epc22 = pytest.mark.skipif(not os.path.isfile(_EPC22), reason="testingPackageCpp22.epc fixture is missing")
requires_epc201 = pytest.mark.skipif(not os.path.isfile(_EPC201), reason="testingPackageCpp.epc fixture is missing")


@pytest.fixture
def epc22():
    epc = EpcFile(epc_file_path=_EPC22, mode=EpcAccessMode.READ_ONLY)
    yield epc


def _vtk_flat_to_triangles(faces: np.ndarray) -> np.ndarray:
    """``[3, a, b, c, 3, a, b, c, …]`` → ``(M, 3)``."""
    if len(faces) == 0:
        return np.empty((0, 3), dtype=np.int64)
    return np.asarray(faces, dtype=np.int64).reshape(-1, 4)[:, 1:]


def _first_of_type(epc, type_fragment: str):
    for meta in epc.list_objects(resolve_titles=False):
        if type_fragment in (getattr(meta, "object_type", "") or ""):
            return epc.get_object_by_uuid(meta.uuid)[0]
    return None


def _all_triangles(multi) -> np.ndarray:
    parts = [_vtk_flat_to_triangles(getattr(p, "faces", np.empty(0))) for p in multi.flat_patches()]
    parts = [p for p in parts if len(p) > 0]
    return np.concatenate(parts, axis=0) if parts else np.empty((0, 3), dtype=np.int64)


# ---------------------------------------------------------------------------
# Grid2d axis-count reconciliation
# ---------------------------------------------------------------------------


class TestFitGridDimensions:
    def test_exact_match_is_untouched(self):
        assert _fit_grid_dimensions(5, 4, 20) == (5, 4)

    def test_mismatch_keeps_the_fastest_axis(self):
        # The fastest axis defines the row stride of the connectivity, so it is the one kept.
        assert _fit_grid_dimensions(5, 4, 17) == (4, 4)

    def test_degenerate_dimensions_generate_no_face(self):
        assert _fit_grid_dimensions(0, 4, 20) == (0, 0)
        assert _fit_grid_dimensions(5, 0, 20) == (0, 0)
        assert _fit_grid_dimensions(5, 4, 0) == (0, 0)

    @pytest.mark.parametrize("nb_points", [1, 2, 3, 7, 12, 19, 20, 21, 100])
    @pytest.mark.parametrize("declared", [(5, 4), (4, 5), (1, 1), (10, 10)])
    def test_product_never_exceeds_the_points_read(self, declared, nb_points):
        # This is the invariant that keeps the generated indices in range: the previous
        # decrement-both loop could leave sa * fa > nb_points (and even fa == 0).
        sa, fa = _fit_grid_dimensions(declared[0], declared[1], nb_points)
        assert sa >= 0 and fa >= 0
        assert sa * fa <= nb_points


# ---------------------------------------------------------------------------
# Dispatchers
# ---------------------------------------------------------------------------


class TestReaderDispatch:
    def test_known_type_resolves_to_its_reader(self):
        assert get_object_reader_function("TriangulatedSetRepresentation").__name__ == (
            "read_triangulated_set_representation"
        )
        assert get_numpy_reader_function("TriangulatedSetRepresentation").__name__ == (
            "read_numpy_triangulated_set_representation"
        )

    def test_unknown_type_resolves_to_none(self):
        assert get_object_reader_function("NoSuchRepresentation") is None
        assert get_numpy_reader_function("NoSuchRepresentation") is None

    def test_lookup_is_stable_across_calls(self):
        # The lookup is memoised; repeated calls must keep returning the same object.
        first = get_object_reader_function("PointRepresentation")
        assert first is get_object_reader_function("PointRepresentation")
        assert get_numpy_reader_function("PointRepresentation") is get_numpy_reader_function("PointRepresentation")

    def test_property_dispatch_cannot_reach_a_geometry_reader(self):
        # read_property resolves in its own module namespace; while it lived in mesh.py that
        # namespace also held the geometry readers, so a PointRepresentation silently returned
        # meshes instead of raising NotSupportedError.
        from energyml.utils.data.properties import get_property_reader_function

        assert get_property_reader_function("TriangulatedSetRepresentation") is None
        assert get_property_reader_function("PointRepresentation") is None
        assert get_property_reader_function("ContinuousProperty").__name__ == "read_continuous_property"

    def test_schema_type_names_resolve_like_class_names(self):
        # RESQML 2.0.1 keeps the `obj_` prefix in its schema type, which is what a content type
        # and ResourceMetadata.object_type carry — the python class name drops the underscore.
        # Only the latter used to be normalised, so _list_exportable_uuids found nothing at all
        # in a 2.0.1 EPC and `extract_3d` exported no file.
        for spelling in (
            "TriangulatedSetRepresentation",
            "ObjTriangulatedSetRepresentation",
            "obj_TriangulatedSetRepresentation",
            "resqml20.obj_TriangulatedSetRepresentation",
        ):
            assert _mesh_name_mapping(spelling) == "TriangulatedSetRepresentation", spelling
            assert get_object_reader_function(_mesh_name_mapping(spelling)) is not None, spelling
            assert get_numpy_reader_function(_mesh_name_mapping(spelling)) is not None, spelling

        assert _mesh_name_mapping("obj_PolylineSetRepresentation") == "PolylineRepresentation"
        assert _mesh_name_mapping("obj_Grid2dRepresentation") == "Grid2dRepresentation"
        assert _mesh_name_mapping("obj_LocalDepth3dCrs") == "LocalDepth3dCrs"

    def test_imported_helper_is_not_mistaken_for_a_reader(self):
        # mesh.py imports read_array / read_grid2d_patch / read_parametric_geometry from helper.py,
        # which the `read_<snake_case(type)>` convention would otherwise match on a type named
        # Array or Grid2dPatch — and then call with a reader signature.
        assert get_object_reader_function("Array") is None
        assert get_object_reader_function("Grid2dPatch") is None
        assert get_object_reader_function("ParametricGeometry") is None


@requires_epc201
class TestExportableUuidListing:
    """``_list_exportable_uuids`` drives ``extract_3d`` when no ``--uuid`` is given."""

    def test_v2_0_1_representations_are_listed(self):
        epc = EpcFile(epc_file_path=_EPC201, mode=EpcAccessMode.READ_ONLY)
        listed = _list_exportable_uuids(epc)

        assert listed, "no exportable representation found in a v2.0.1 EPC"

        # every listed object must actually be readable as a mesh, and every representation
        # that has a reader must be listed
        by_uuid = {meta.uuid: meta.object_type for meta in epc.list_objects(resolve_titles=False) if meta.object_type}
        expected = {
            uuid
            for uuid, object_type in by_uuid.items()
            if get_object_reader_function(_mesh_name_mapping(object_type)) is not None
        }
        assert set(listed) == expected
        assert any("Triangulated" in by_uuid[uuid] for uuid in listed)


# ---------------------------------------------------------------------------
# read_mesh_object on a list of objects
# ---------------------------------------------------------------------------


@requires_epc22
class TestReadMeshObjectList:
    def test_list_input_returns_meshes_not_the_input_objects(self, epc22):
        obj = epc22.get_object_by_uuid(_MULTI_PATCH_UUID)[0]

        single = read_mesh_object(energyml_object=obj, workspace=epc22)
        from_list = read_mesh_object(energyml_object=[obj, obj], workspace=epc22)

        assert all(
            isinstance(m, AbstractMesh) for m in from_list
        ), "a list input used to be returned unchanged, i.e. the energyml objects themselves"
        assert len(from_list) == 2 * len(single)


# ---------------------------------------------------------------------------
# read_property_interpreted_with_cbt error path
# ---------------------------------------------------------------------------


class TestCategoryLookupErrorPath:
    def test_unsupported_lookup_type_raises_not_supported(self, monkeypatch):
        # The property readers live in properties.py now; mesh.py only re-exports them.
        import energyml.utils.data.properties as mesh_module

        class _Dor:
            pass

        class _Prop:
            category_lookup = _Dor()

        class _Workspace:
            def get_object(self, _uri):
                return object()

        monkeypatch.setattr(mesh_module, "get_obj_uri", lambda _o: "uri")
        # Anything that is neither a list/ndarray nor a dict reaches the error branch, which
        # used to reference a variable bound only in the dict branch -> NameError.
        monkeypatch.setattr(mesh_module, "read_column_based_table", lambda *_a, **_k: 42)

        with pytest.raises(NotSupportedError) as exc_info:
            read_property_interpreted_with_cbt(
                _Prop(),
                _Workspace(),
                _cache_property_arrays=np.array([0, 1]),
            )
        assert "int" in str(exc_info.value)


# ---------------------------------------------------------------------------
# sub_indices window alignment across patches
# ---------------------------------------------------------------------------


class TestGrid2dQuadConnectivity:
    """The quad connectivity is built by broadcasting instead of a Python double loop.

    The expected arrays below are written out explicitly rather than derived from a second
    implementation, so the test stays a specification of the connectivity.
    """

    @staticmethod
    def _read_grid(monkeypatch, points, sa, fa, keep_holes):
        import energyml.utils.data.mesh_numpy as mesh_numpy

        class _Grid:
            # A plain class, not a MagicMock: `hasattr(obj, "geometry")` selects the RESQML 2.2
            # branch, and a mock would answer True to everything and produce a second patch.
            geometry = object()

        monkeypatch.setattr(mesh_numpy, "read_grid2d_patch", lambda **_k: points)
        monkeypatch.setattr(
            mesh_numpy,
            "search_attribute_matching_name",
            lambda _obj, name: [fa] if "Fastest" in name else [sa],
        )
        monkeypatch.setattr(mesh_numpy, "search_attribute_matching_name_with_path", lambda *_a, **_k: [])
        monkeypatch.setattr(mesh_numpy, "get_crs_obj", lambda **_k: None)
        monkeypatch.setattr(mesh_numpy, "get_obj_uuid", lambda _o: "uuid")
        monkeypatch.setattr(mesh_numpy, "get_obj_uri", lambda _o: "uri")

        result = mesh_numpy.read_numpy_grid2d_representation(_Grid(), workspace=None, keep_holes=keep_holes)
        return result.flat_patches()

    def test_full_2x3_grid(self, monkeypatch):
        # 2 rows x 3 columns of nodes -> 1 x 2 = 2 quads.
        points = [[float(i), float(j), 0.0] for j in range(2) for i in range(3)]
        patches = self._read_grid(monkeypatch, points, sa=2, fa=3, keep_holes=True)

        assert len(patches) == 1
        # VTK flat format: [4, a, b, c, d, 4, a, b, c, d]
        np.testing.assert_array_equal(
            patches[0].faces,
            [4, 0, 1, 4, 3, 4, 1, 2, 5, 4],
        )

    def test_hole_drops_only_the_cells_that_touch_it(self, monkeypatch):
        # 3x3 nodes -> 2x2 = 4 quads. Node 4 (the centre) is a hole, and it is a corner of all
        # four cells, so every cell disappears while the 8 remaining nodes are kept.
        points = [[float(i), float(j), 0.0] for j in range(3) for i in range(3)]
        points[4][2] = float("nan")
        patches = self._read_grid(monkeypatch, points, sa=3, fa=3, keep_holes=False)
        assert patches == [] or len(patches[0].faces) == 0

    def test_hole_in_a_corner_keeps_the_other_cells(self, monkeypatch):
        # 3x3 nodes, node 0 is a hole: it belongs to the first cell only.
        points = [[float(i), float(j), 0.0] for j in range(3) for i in range(3)]
        points[0][2] = float("nan")
        patches = self._read_grid(monkeypatch, points, sa=3, fa=3, keep_holes=False)

        assert len(patches) == 1
        assert len(patches[0].points) == 8, "only the NaN node is dropped"
        # 3 of the 4 cells survive; indices are renumbered over the 8 surviving nodes.
        faces = patches[0].faces
        assert len(faces) == 3 * 5
        quads = faces.reshape(-1, 5)
        assert (quads[:, 0] == 4).all()
        np.testing.assert_array_equal(
            quads[:, 1:],
            [[0, 1, 4, 3], [2, 3, 6, 5], [3, 4, 7, 6]],
        )

    def test_degenerate_dimensions_produce_no_patch(self, monkeypatch):
        points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        assert self._read_grid(monkeypatch, points, sa=1, fa=2, keep_holes=True) == []


@requires_epc22
class TestLegacyAdapter:
    """``mesh.py``'s geometry readers delegate to ``mesh_numpy`` and convert the result back.

    The full before/after comparison was done over every representation of every fixture in
    ``rc/epc/`` (1155 objects, 942 meshes): identifiers, coordinates, index structures and
    edge/face counts all matched. These tests pin the properties that comparison relied on.
    """

    def test_point_list_is_a_numpy_array(self, epc22):
        # Documented change: the legacy containers now hold the (N, 3) float64 array produced by
        # the numpy reader instead of a list of lists. The field was already annotated
        # Union[List[Point], np.ndarray].
        obj = epc22.get_object_by_uuid(_MULTI_PATCH_UUID)[0]
        meshes = read_mesh_object(obj, workspace=epc22)

        assert meshes
        for m in meshes:
            assert isinstance(m.point_list, np.ndarray)
            assert m.point_list.dtype == np.float64
            assert m.point_list.ndim == 2 and m.point_list.shape[1] == 3

    def test_indices_are_plain_lists_of_int(self, epc22):
        # get_indices() feeds the OBJ / OFF / GeoJSON writers, which index and len() it.
        obj = epc22.get_object_by_uuid(_MULTI_PATCH_UUID)[0]
        mesh = read_mesh_object(obj, workspace=epc22)[0]

        indices = mesh.get_indices()
        assert isinstance(indices, list)
        assert all(isinstance(face, list) for face in indices)
        assert all(isinstance(i, int) for i in indices[0])

    def test_legacy_identifiers_are_preserved(self, epc22):
        obj = epc22.get_object_by_uuid(_MULTI_PATCH_UUID)[0]
        meshes = read_mesh_object(obj, workspace=epc22)

        from energyml.utils.introspection import get_obj_uri

        uri = get_obj_uri(obj)
        for index, mesh in enumerate(meshes):
            assert mesh.identifier == f"{uri}_patch{index}"

    def test_point_sets_keep_their_own_naming(self, epc22):
        obj = _first_of_type(epc22, "PointSet")
        if obj is None:
            pytest.skip("no PointSetRepresentation in the fixture")
        meshes = read_mesh_object(obj, workspace=epc22)
        assert meshes[0].identifier == "Patch num 0"

    def test_volumetric_types_are_refused_with_a_pointer_to_the_numpy_stack(self, epc22):
        # AbstractMesh models points, polylines and surfaces only.
        from energyml.utils.data.mesh import read_ijk_grid_representation

        with pytest.raises(NotSupportedError) as exc_info:
            read_ijk_grid_representation(object(), workspace=epc22)
        assert "mesh_numpy" in str(exc_info.value)


@requires_epc22
class TestSubIndicesPatchAlignment:
    def test_partial_selection_spanning_two_patches(self, epc22):
        obj = epc22.get_object_by_uuid(_MULTI_PATCH_UUID)[0]

        every_triangle = _all_triangles(read_numpy_mesh_object(obj, workspace=epc22))
        assert len(every_triangle) == 20, "fixture changed: expected 5 patches x 4 triangles"

        # 0 and 1 live in patch 0, 5 and 6 in patch 1. Because the first patch drops half of
        # its faces, an offset advanced by the filtered count desynchronises every later patch.
        selection = [0, 1, 5, 6]
        selected = _all_triangles(read_numpy_mesh_object(obj, workspace=epc22, sub_indices=selection))

        assert len(selected) == len(selection)
        np.testing.assert_array_equal(selected, every_triangle[selection])

    def test_full_selection_is_identity(self, epc22):
        obj = epc22.get_object_by_uuid(_MULTI_PATCH_UUID)[0]

        every_triangle = _all_triangles(read_numpy_mesh_object(obj, workspace=epc22))
        selected = _all_triangles(
            read_numpy_mesh_object(obj, workspace=epc22, sub_indices=list(range(len(every_triangle))))
        )

        np.testing.assert_array_equal(selected, every_triangle)
