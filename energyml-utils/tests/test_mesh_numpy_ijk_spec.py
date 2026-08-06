"""Conformance of the IJK / connection-set readers to the RESQML specification.

Everything here runs against ``rc/epc/testingPackageCpp22.epc`` — the FESAPI example package,
which is the only fixture family cleared for publication, and which happens to be exactly what
these tests need: the same grid shipped left- *and* right-handed, explicit *and* parametric
geometry, faulted and unfaulted, K-gaps, undefined cells, an LGR, and three grid connection
sets. Expected values are read out of ``testingPackageCpp22.h5``, not produced by the reader.

Run from the workspace root:
    poetry run pytest tests/test_mesh_numpy_ijk_spec.py -v
"""

import os

import numpy as np
import pytest

from energyml.utils.data.mesh_numpy import (
    NumpySurfaceMesh,
    read_numpy_mesh_object,
)

_WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EPC22 = os.path.join(_WORKSPACE_ROOT, "rc", "epc", "testingPackageCpp22.epc")

pytestmark = pytest.mark.skipif(
    not os.path.isfile(_EPC22),
    reason="testingPackageCpp22.epc not found in rc/epc/",
)


@pytest.fixture(scope="module")
def ws():
    from energyml.utils.epc_file import EpcFile

    return EpcFile(_EPC22)


def _unpack_vtk_cells(mesh) -> list:
    """Split a VTK flat cell array into one node array per cell."""
    out, off = [], 0
    for _ in mesh.cell_types:
        n = int(mesh.cells[off])
        out.append(np.asarray(mesh.cells[off + 1 : off + 1 + n], dtype=np.int64))
        off += 1 + n
    assert off == len(mesh.cells), "cell array length does not match cell_types"
    return out


def _hex_signed_volume(p: np.ndarray) -> float:
    """Signed volume of a VTK hexahedron given its 8 corner points, shape (8, 3)."""
    tets = [(0, 1, 3, 4), (1, 2, 3, 6), (1, 4, 5, 6), (3, 4, 6, 7), (1, 3, 4, 6)]
    return float(sum(np.dot(np.cross(p[b] - p[a], p[c] - p[a]), p[d] - p[a]) / 6.0 for a, b, c, d in tets))


def _grid(ws, uuid):
    obj = ws.get_object(f"eml:///resqml22.IjkGridRepresentation({uuid})")
    if obj is None:
        pytest.skip(f"IjkGridRepresentation {uuid} not in fixture")
    return obj


def _mesh_of(ws, uuid, local: bool = False):
    """Read a grid, by default in the PROJECTED frame — the one a viewer renders.

    Handedness is only meaningful there: the local CRS of these fixtures measures Z as a depth,
    which makes (X, Y, Z) left-handed on its own, so the sign of a cell's Jacobian in the local
    frame says nothing about ``GridIsRighthanded``.
    """
    multi = read_numpy_mesh_object(_grid(ws, uuid), workspace=ws, use_crs_displacement=not local)
    return multi.flat_patches()[0]


def _points_of(ws, uuid):
    multi = read_numpy_mesh_object(_grid(ws, uuid), workspace=ws, use_crs_displacement=False)
    return np.concatenate([p.points for p in multi.flat_patches()])


class TestParametricGeometry:
    def test_split_coordinate_line_reuses_its_parent_pillar_line(self, ws):
        """A split coordinate line takes the parametric line of ``PillarIndices``.

        "Four faulted sugar cubes (parametric geometry)": 6 pillars, 2 split lines, every line
        vertical, so a node is (X, Y of the line, P). ``PillarIndices`` = [1, 4] and the split
        columns are parameterised 50 m below their parent — the fault throw.
        """
        xy = np.array([(0, 0), (375, 0), (700, 0), (0, 150), (375, 150), (700, 150)], dtype=float)
        params = np.array(
            [
                [300, 300, 350, 300, 300, 350, 350, 350],
                [400, 400, 450, 400, 400, 450, 450, 450],
                [500, 500, 550, 500, 500, 550, 550, 550],
            ],
            dtype=float,
        )
        line_of_col = [0, 1, 2, 3, 4, 5, 1, 4]
        expected = np.array(
            [[xy[line_of_col[c]][0], xy[line_of_col[c]][1], params[k, c]] for k in range(3) for c in range(8)]
        )
        np.testing.assert_allclose(_points_of(ws, "37c45c00-fa3e-11e5-a21e-0002a5d5c51b"), expected, atol=1e-9)

    def test_vertical_lines_place_z_at_the_parameter(self, ws):
        """RESQML vertical line: "Control points are (X,Y,-) [...] parameter values are depth"."""
        xy = np.array([(0, 0), (700, 0), (0, 150), (700, 150)], dtype=float)
        expected = np.array([[xy[c][0], xy[c][1], z] for z in (300.0, 500.0) for c in range(4)])
        np.testing.assert_allclose(_points_of(ws, "53bb70fe-2eef-4691-b4fe-14541e3a57eb"), expected, atol=1e-9)

    def test_nan_padded_knots_do_not_poison_the_lines(self, ws):
        """``KnotCount`` pads the shorter lines with NaN — those knots must be trimmed.

        "Four faulted sugar cubes with one cubic pillar" declares KnotCount=3, yet four of its
        six pillars are vertical with one real knot and pillar 0 is a 2-knot linear spline.
        """
        pts = _points_of(ws, "3ce91933-4f6f-4f35-b0ac-4ba4672f0a87")
        assert not np.isnan(pts).any(), "NaN padding leaked into the evaluated geometry"

        # Pillar 0 is linear between (0,0,300)@P=300 and (50,30,1000)@P=1000.
        for k, p in enumerate([300.0, 400.0, 500.0]):
            t = (p - 300.0) / 700.0
            np.testing.assert_allclose(pts[k * 8], [t * 50.0, t * 30.0, 300.0 + t * 700.0], atol=1e-9)


class TestCellConstruction:
    @pytest.mark.parametrize(
        "uuid",
        [
            "e96c2bde-e3ae-4d51-b078-a8e57fb1e667",  # Four by Three by Two Left Handed
            "4fc004e1-0f7d-46a8-935e-588f790a6f84",  # Four by Three by Two Right Handed
        ],
    )
    def test_hexahedra_are_positively_oriented(self, ws, uuid):
        """``GridIsRighthanded`` sets the winding; VTK always wants a positive Jacobian.

        The fixture ships the same grid twice, left- and right-handed, for exactly this case:
        before the flag was honoured, every cell of the left-handed one came out inside-out.
        Measured in the projected frame — see :func:`_mesh_of`.
        """
        mesh = _mesh_of(ws, uuid)
        for nodes in _unpack_vtk_cells(mesh):
            if len(nodes) != 8:
                continue  # a cell without geometry
            assert _hex_signed_volume(mesh.points[nodes]) > 0, f"inverted hexahedron in {uuid}"

    def test_cells_follow_the_resqml_ordering(self, ws):
        """Cells come out I fastest, then J, then K — the order the grid's properties use."""
        uuid = "4fc004e1-0f7d-46a8-935e-588f790a6f84"  # 4 x 3 x 2
        grid = _grid(ws, uuid)
        ni, nj, nk = int(grid.ni), int(grid.nj), int(grid.nk)
        mesh = _mesh_of(ws, uuid)
        cells = _unpack_vtk_cells(mesh)
        assert len(cells) == ni * nj * nk

        def pillar_xy(j, i):
            return mesh.points[j * (ni + 1) + i][:2]

        for c, nodes in enumerate(cells):
            if len(nodes) != 8:
                continue
            k, j, i = c // (ni * nj), (c // ni) % nj, c % ni
            centroid = mesh.points[nodes].mean(axis=0)
            xs = sorted([pillar_xy(j, i)[0], pillar_xy(j, i + 1)[0]])
            ys = sorted([pillar_xy(j, i)[1], pillar_xy(j + 1, i)[1]])
            assert xs[0] - 1e-6 <= centroid[0] <= xs[1] + 1e-6, f"cell {c} is not at I={i} (k={k}, j={j})"
            assert ys[0] - 1e-6 <= centroid[1] <= ys[1] + 1e-6, f"cell {c} is not at J={j} (k={k}, i={i})"

    def test_undefined_cells_stay_in_place_as_empty_cells(self, ws):
        """``CellGeometryIsDefined``=false keeps its slot so cell-indexed properties still align.

        The HDF5 of "Four by Three by Two Right Handed" stores the flag as (NK, NJ, NI) with
        zeros at flat indices 0, 11 and 23.
        """
        mesh = _mesh_of(ws, "4fc004e1-0f7d-46a8-935e-588f790a6f84")
        empty = [c for c, t in enumerate(mesh.cell_types) if int(t) == 0]
        assert empty == [0, 11, 23]
        cells = _unpack_vtk_cells(mesh)
        assert all(len(cells[c]) == 0 for c in empty), "an empty cell must list no node"

    def test_k_gaps_do_not_change_the_cell_count(self, ws):
        """A K-gap adds a node layer, not a cell: NKL = NK + gapCount + 1."""
        grid = _grid(ws, "c14755a5-e3b3-4272-99e5-fc20993b79a0")  # ... with gap layer
        mesh = _mesh_of(ws, "c14755a5-e3b3-4272-99e5-fc20993b79a0")
        assert len(mesh.cell_types) == int(grid.ni) * int(grid.nj) * int(grid.nk)

    def test_lgr_without_geometry_returns_empty_rather_than_raising(self, ws):
        """A grid whose geometry is inherited through ``ParentWindow`` is reported, not crashed on."""
        grid = _grid(ws, "2aec1720-fa3e-11e5-a116-0002a5d5c51b")
        assert getattr(grid, "geometry", None) is None
        multi = read_numpy_mesh_object(grid, workspace=ws, use_crs_displacement=False)
        assert multi.flat_patches() == []


class TestGridConnectionSet:
    @pytest.mark.parametrize(
        "uuid",
        [
            "03bb6fc0-fa3e-11e5-8c09-0002a5d5c51b",
            "20b480a8-5e3b-4336-8f6e-1b3099c2c60f",
            "a3d1462a-04e3-4374-921b-a4a1e9ba3ea3",
        ],
    )
    def test_faces_land_on_the_fault_plane(self, ws, uuid):
        """Every connection set of the fixture faults its grid at X=375.

        This is what pins the local face-per-cell indices the files use (3 = I+, 5 = I-): a wrong
        mapping would return the J or K faces, which are not planar in X.
        """
        obj = ws.get_object(f"eml:///resqml22.GridConnectionSetRepresentation({uuid})")
        if obj is None:
            pytest.skip(f"GridConnectionSet {uuid} not in fixture")
        patches = read_numpy_mesh_object(obj, workspace=ws, use_crs_displacement=False).flat_patches()
        assert patches, "expected the connection faces"
        mesh = patches[0]
        assert isinstance(mesh, NumpySurfaceMesh)

        off, n_faces = 0, 0
        while off < len(mesh.faces):
            n = int(mesh.faces[off])
            assert n == 4, "the face of an IJK cell is a quad"
            nodes = mesh.faces[off + 1 : off + 1 + n]
            np.testing.assert_allclose(mesh.points[nodes][:, 0], 375.0, atol=1e-9)
            off += 1 + n
            n_faces += 1
        assert n_faces > 0
        assert len(mesh.extra_arrays["connection_index"]) == n_faces

    def test_interpretation_index_is_exposed(self, ws):
        """``ConnectionInterpretations`` is what lets a viewer colour the set by fault."""
        obj = ws.get_object("eml:///resqml22.GridConnectionSetRepresentation(03bb6fc0-fa3e-11e5-8c09-0002a5d5c51b)")
        if obj is None:
            pytest.skip("GridConnectionSet not in fixture")
        mesh = read_numpy_mesh_object(obj, workspace=ws, use_crs_displacement=False).flat_patches()[0]
        interp = mesh.extra_arrays["interpretation_index"]
        assert set(np.unique(interp)) <= {-1, 0}
        assert (interp == 0).any(), "the interpreted connection should be flagged"


class TestNewlySupportedRepresentations:
    def test_wellbore_marker_frame_gives_one_point_per_marker(self, ws):
        obj = ws.get_object(
            "eml:///resqml20.obj_WellboreMarkerFrameRepresentation(657d5e6b-1752-425d-b3e7-237037fa11eb)"
        )
        if obj is None:
            pytest.skip("WellboreMarkerFrame not in fixture")
        patches = read_numpy_mesh_object(obj, workspace=ws).flat_patches()
        assert patches, "expected the marker positions"
        assert patches[0].points.shape[1] == 3
        assert len(patches[0].points) == int(obj.node_count)
        # The patch reports the marker frame, not the trajectory it took the geometry from.
        assert patches[0].source_type == type(obj).__name__

    def test_no_representation_of_the_fixture_fails(self, ws):
        """Regression net for the dispatcher: the file must read end to end."""
        failures = []
        for ref in ws.list_objects(resolve_titles=False):
            uri = str(ref.uri)
            obj = ws.get_object(uri)
            if "Representation" not in type(obj).__name__:
                continue
            try:
                read_numpy_mesh_object(obj, workspace=ws)
            except Exception as exc:  # noqa: BLE001 — the point is to report, not to classify
                failures.append(f"{uri}: {type(exc).__name__}: {exc}")
        assert not failures, "\n".join(failures)
