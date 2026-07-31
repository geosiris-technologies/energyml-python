"""Tests for the unified CRS pipeline: PointFrame / to_frame / compute_origin_shift.

The pipeline replaces two mechanisms that used to coexist:

* ``apply_from_crs_info`` — the full local -> projected transform, and
* ``crs_displacement_np`` — offsets and Z flip only,

selected by a list of type-name substrings in each dispatcher. A reader missing from the list
had its points transformed twice; a reader wrongly listed kept raw coordinates. ``Grid2d`` was in
neither list, so the same object came out rotated from :mod:`mesh` and un-rotated from
:mod:`mesh_numpy`.

Note: every Grid2d fixture in ``rc/epc/`` has a zero areal rotation and an easting-first axis
order, so that divergence is invisible on real files — hence the synthetic rotation in
:class:`TestGrid2dGetsTheFullTransform`.
"""
import math
import os

import numpy as np
import pytest

from energyml.utils.data.crs import (
    CrsInfo,
    FramedPoints,
    PointFrame,
    apply_from_crs_info,
    compute_origin_shift,
    is_pyproj_available,
    reproject_to_wgs84,
    to_frame,
)
from energyml.utils.data.mesh_numpy import _ensure_float64_points, read_numpy_mesh_object
from energyml.utils.epc_file import EpcAccessMode, EpcFile
from energyml.utils.exception import NotSupportedError

_WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EPC22 = os.path.join(_WORKSPACE_ROOT, "rc", "epc", "testingPackageCpp22.epc")

requires_epc22 = pytest.mark.skipif(not os.path.isfile(_EPC22), reason="testingPackageCpp22.epc fixture is missing")
requires_pyproj = pytest.mark.skipif(not is_pyproj_available(), reason="requires the 'crs' extra (pyproj)")


@pytest.fixture
def epc22():
    yield EpcFile(epc_file_path=_EPC22, mode=EpcAccessMode.READ_ONLY)


def _first_object_of_type(epc, type_fragment: str):
    for meta in epc.list_objects(resolve_titles=False):
        if type_fragment in (getattr(meta, "object_type", "") or ""):
            return epc.get_object_by_uuid(meta.uuid)[0]
    return None


def _rotated_crs_info(angle_rad: float) -> CrsInfo:
    """A CrsInfo whose *only* effect is an areal rotation."""
    return CrsInfo(
        x_offset=0.0,
        y_offset=0.0,
        z_offset=0.0,
        areal_rotation_value=angle_rad,
        areal_rotation_uom="rad",
        z_increasing_downward=False,
        projected_axis_order="easting northing",
    )


# ---------------------------------------------------------------------------
# Frame ordering
# ---------------------------------------------------------------------------


class TestFrameOrdering:
    def test_stages_are_ordered(self):
        assert PointFrame.LOCAL.stage < PointFrame.PROJECTED.stage < PointFrame.WGS84.stage

    def test_going_backwards_is_refused(self):
        pts = np.zeros((2, 3))
        with pytest.raises(NotSupportedError):
            to_frame(pts, CrsInfo(), PointFrame.LOCAL, PointFrame.PROJECTED)
        with pytest.raises(NotSupportedError):
            to_frame(pts, CrsInfo(), PointFrame.PROJECTED, PointFrame.WGS84)

    def test_same_frame_is_a_no_op(self):
        pts = np.array([[1.0, 2.0, 3.0]])
        result = to_frame(pts, _rotated_crs_info(math.pi / 3), PointFrame.LOCAL, PointFrame.LOCAL)
        assert isinstance(result, FramedPoints)
        assert result.frame is PointFrame.LOCAL
        np.testing.assert_array_equal(result.points, [[1.0, 2.0, 3.0]])

    def test_projected_target_on_already_projected_points_changes_nothing(self):
        # This is what makes the double transform impossible: the frame is carried, so a second
        # pass through the dispatcher cannot re-apply the offsets.
        pts = np.array([[420000.0, 6470000.0, -100.0]])
        crs_info = CrsInfo(x_offset=420000.0, y_offset=6470000.0)
        result = to_frame(pts, crs_info, PointFrame.PROJECTED, PointFrame.PROJECTED)
        np.testing.assert_array_equal(result.points, [[420000.0, 6470000.0, -100.0]])


# ---------------------------------------------------------------------------
# Stage 1: LOCAL -> PROJECTED
# ---------------------------------------------------------------------------


class TestLocalToProjected:
    def test_matches_apply_from_crs_info(self):
        crs_info = CrsInfo(
            x_offset=1000.0,
            y_offset=2000.0,
            z_offset=15.0,
            areal_rotation_value=0.3,
            areal_rotation_uom="rad",
            z_increasing_downward=True,
            projected_axis_order="easting northing",
        )
        pts = np.array([[10.0, 20.0, 30.0], [-5.0, 7.5, 0.0]])

        expected = apply_from_crs_info(pts.copy(), crs_info, inplace=False)
        result = to_frame(pts.copy(), crs_info, PointFrame.PROJECTED, PointFrame.LOCAL)

        assert result.frame is PointFrame.PROJECTED
        np.testing.assert_allclose(result.points, expected)

    def test_rotation_is_applied(self):
        angle = math.pi / 2
        result = to_frame(
            np.array([[1.0, 0.0, 0.0]]),
            _rotated_crs_info(angle),
            PointFrame.PROJECTED,
            PointFrame.LOCAL,
        )
        # RESQML rotation is clockwise: x' = x·cos + y·sin, y' = -x·sin + y·cos
        np.testing.assert_allclose(result.points[0], [0.0, -1.0, 0.0], atol=1e-12)

    def test_without_crs_info_the_frame_stays_local(self):
        pts = np.array([[1.0, 2.0, 3.0]])
        result = to_frame(pts, None, PointFrame.PROJECTED, PointFrame.LOCAL)
        assert result.frame is PointFrame.LOCAL
        assert result.degraded_reason is not None
        np.testing.assert_array_equal(result.points, [[1.0, 2.0, 3.0]])

    def test_inplace_false_leaves_the_source_untouched(self):
        pts = np.array([[10.0, 20.0, 30.0]])
        original = pts.copy()
        result = to_frame(pts, CrsInfo(x_offset=5.0), PointFrame.PROJECTED, PointFrame.LOCAL, inplace=False)
        np.testing.assert_array_equal(pts, original)
        assert result.points[0, 0] == 15.0


# ---------------------------------------------------------------------------
# Stage 2: PROJECTED -> WGS84 degradation
# ---------------------------------------------------------------------------


class TestWgs84Degradation:
    def test_missing_epsg_degrades_to_projected(self):
        # No projected_epsg_code -> reproject_to_wgs84 cannot run. The points must stay usable
        # and the caller must be able to tell that WGS84 was not reached.
        pts = np.array([[420000.0, 6470000.0, -100.0]])
        result = to_frame(pts.copy(), CrsInfo(), PointFrame.WGS84, PointFrame.PROJECTED)

        assert result.frame is PointFrame.PROJECTED
        assert result.degraded_reason is not None
        np.testing.assert_allclose(result.points, pts)

    def test_empty_array_reports_the_requested_frame(self):
        # An empty patch must not make a whole FeatureCollection look degraded.
        result = to_frame(np.empty((0, 3)), CrsInfo(), PointFrame.WGS84, PointFrame.LOCAL)
        assert result.frame is PointFrame.WGS84
        assert result.degraded_reason is None


# ---------------------------------------------------------------------------
# Origin shift
# ---------------------------------------------------------------------------


class TestOriginShift:
    def test_shift_is_shared_across_arrays(self):
        # The whole point: one vector for every patch, so patches do not move relative to
        # each other. A per-patch centroid would give each array a different shift.
        a = np.array([[0.0, 0.0, 0.0], [100.0, 100.0, 10.0]])
        b = np.array([[900.0, 500.0, 0.0], [1000.0, 600.0, 20.0]])

        shift = compute_origin_shift([a, b])
        assert shift == (500.0, 300.0, 10.0)

        moved_a = to_frame(a.copy(), None, PointFrame.LOCAL, PointFrame.LOCAL, origin_shift=shift).points
        moved_b = to_frame(b.copy(), None, PointFrame.LOCAL, PointFrame.LOCAL, origin_shift=shift).points

        # Relative geometry preserved
        np.testing.assert_allclose(moved_b - moved_a, b - a)
        # And the coordinates are now small
        assert np.max(np.abs(np.concatenate([moved_a, moved_b]))) < np.max(np.abs(np.concatenate([a, b])))

    def test_applied_shift_is_reported(self):
        result = to_frame(
            np.array([[10.0, 10.0, 10.0]]),
            None,
            PointFrame.LOCAL,
            PointFrame.LOCAL,
            origin_shift=(1.0, 2.0, 3.0),
        )
        assert result.origin_shift == (1.0, 2.0, 3.0)
        np.testing.assert_allclose(result.points, [[9.0, 8.0, 7.0]])

    def test_no_points_gives_a_zero_shift(self):
        assert compute_origin_shift([]) == (0.0, 0.0, 0.0)
        assert compute_origin_shift([np.empty((0, 3))]) == (0.0, 0.0, 0.0)

    def test_nan_only_input_does_not_produce_a_nan_shift(self):
        # Grid2d holes are stored as NaN; a NaN shift would wipe out every coordinate.
        shift = compute_origin_shift([np.full((3, 3), np.nan)])
        assert shift == (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Chunked reprojection
# ---------------------------------------------------------------------------


@requires_pyproj
class TestReprojectionChunking:
    """The reprojection copies each axis into a reusable scratch buffer, block by block, so its
    scratch memory is constant instead of proportional to the point count. These tests pin the
    behaviour that the blocking must not change."""

    CRS = CrsInfo(projected_epsg_code=32631)

    def _points(self, n):
        pts = np.empty((n, 3), dtype=np.float64)
        pts[:, 0] = np.linspace(400000.0, 440000.0, n)
        pts[:, 1] = np.linspace(6470000.0, 6510000.0, n)
        pts[:, 2] = np.linspace(-3000.0, 0.0, n)
        return pts

    def test_result_is_independent_of_the_chunk_size(self, monkeypatch):
        import energyml.utils.data.crs as crs_module

        pts = self._points(1000)
        single_block = reproject_to_wgs84(pts.copy(), self.CRS, inplace=False)

        # A chunk size that does not divide the point count exercises the ragged last block.
        monkeypatch.setattr(crs_module, "_REPROJECT_CHUNK", 137)
        many_blocks = reproject_to_wgs84(pts.copy(), self.CRS, inplace=False)

        np.testing.assert_allclose(many_blocks, single_block, rtol=0, atol=0)

    def test_inplace_and_copy_agree(self):
        pts = self._points(500)
        copied = reproject_to_wgs84(pts.copy(), self.CRS, inplace=False)
        target = pts.copy()
        returned = reproject_to_wgs84(target, self.CRS, inplace=True)

        assert returned is target, "inplace=True must write into the array it was given"
        np.testing.assert_allclose(target, copied)

    def test_inplace_false_leaves_the_source_untouched(self):
        pts = self._points(300)
        original = pts.copy()
        reproject_to_wgs84(pts, self.CRS, inplace=False)
        np.testing.assert_array_equal(pts, original)

    def test_single_point_takes_the_scalar_path(self):
        one = self._points(1)
        result = reproject_to_wgs84(one.copy(), self.CRS, inplace=False)
        assert result.shape == (1, 3)
        # Same answer as when that point is part of a longer array.
        pair = np.vstack([one, one])
        np.testing.assert_allclose(result[0], reproject_to_wgs84(pair, self.CRS, inplace=False)[0])


@requires_pyproj
class TestUnusableVerticalCrs:
    """A file may declare a vertical EPSG code PROJ cannot resolve — typically a *datum* code
    where a CRS code was expected (``EPSG:6230``, the ED50 datum, in the Volve export). The
    compound ``EPSG:h+EPSG:v`` then fails to build; refusing the whole reprojection would leave
    the coordinates in their projected CRS although the horizontal part is perfectly usable."""

    #: ED50 / UTM zone 31N, and the ED50 *datum* code the file declares as its vertical CRS.
    BROKEN = CrsInfo(projected_epsg_code=23031, vertical_epsg_code=6230)
    HORIZONTAL_ONLY = CrsInfo(projected_epsg_code=23031)

    def _points(self, n=64):
        pts = np.empty((n, 3), dtype=np.float64)
        pts[:, 0] = np.linspace(435000.0, 436000.0, n)
        pts[:, 1] = np.linspace(6477000.0, 6478000.0, n)
        pts[:, 2] = np.linspace(-3000.0, -2500.0, n)
        return pts

    def test_horizontal_reprojection_still_happens(self):
        pts = self._points()
        result = reproject_to_wgs84(pts.copy(), self.BROKEN, inplace=False)

        # Volve, North Sea: ~1.9 E, ~58.4 N.
        assert 1.0 < result[0, 0] < 3.0
        assert 57.0 < result[0, 1] < 60.0

        # Same answer as a CRS that never declared a vertical code, up to the ellipsoidal height
        # the ED50 -> WGS84 datum shift is fed: that path hands Z to PROJ, this one does not
        # (Z is not a height here), which moves the result by well under a metre.
        horizontal = reproject_to_wgs84(pts.copy(), self.HORIZONTAL_ONLY, inplace=False)
        np.testing.assert_allclose(result[:, :2], horizontal[:, :2], rtol=0, atol=1e-5)

    def test_z_is_passed_through_untouched(self):
        pts = self._points()
        result = reproject_to_wgs84(pts.copy(), self.BROKEN, inplace=False)
        # The vertical CRS was dropped, so Z is still in its source frame — not silently
        # datum-shifted, and not sign-flipped either.
        np.testing.assert_array_equal(result[:, 2], pts[:, 2])

    def test_single_point_path_agrees(self):
        pts = self._points()
        full = reproject_to_wgs84(pts.copy(), self.BROKEN, inplace=False)
        one = reproject_to_wgs84(pts[:1].copy(), self.BROKEN, inplace=False)
        np.testing.assert_allclose(one[0], full[0])

    def test_frame_reaches_wgs84(self):
        framed = to_frame(self._points(), self.BROKEN, PointFrame.WGS84, PointFrame.PROJECTED)
        assert framed.frame is PointFrame.WGS84
        assert framed.degraded_reason is None

    def test_a_missing_horizontal_code_still_raises(self):
        from energyml.utils.exception import NotEnoughInformationError

        with pytest.raises(NotEnoughInformationError):
            reproject_to_wgs84(self._points(), CrsInfo(vertical_epsg_code=6230), inplace=False)

    def test_depth_vertical_crs_flips_z_without_touching_the_source(self):
        # EPSG:5715 (MSL depth) is a *depth* CRS. Two negations are in play and they must not be confused:
        #   - ours, because the Z column holds heights (z_is_up) while the CRS expects depths;
        #   - PROJ's own, when it converts that depth axis to the ellipsoidal height of EPSG:4979.
        # With z_is_up=True the two cancel out, so the height comes back roughly unchanged; with
        # z_is_up=False only PROJ's negation applies. Comparing the two isolates our flip, which
        # is now folded into the per-block scratch fill instead of a full-size copy.
        crs = CrsInfo(projected_epsg_code=32631, vertical_epsg_code=5715)
        pts = self._points(64)
        original = pts.copy()

        as_height = reproject_to_wgs84(pts, crs, inplace=False, z_is_up=True)
        np.testing.assert_array_equal(pts, original, err_msg="inplace=False must not touch the source")
        as_depth = reproject_to_wgs84(original.copy(), crs, inplace=False, z_is_up=False)

        np.testing.assert_allclose(as_height[:, 2], -as_depth[:, 2], atol=1e-6)
        # And the flip is only about Z: longitude / latitude are untouched by it.
        np.testing.assert_allclose(as_height[:, :2], as_depth[:, :2])

    def test_chunking_holds_with_a_depth_crs_too(self, monkeypatch):
        # The Z flip happens per block now, so a ragged last block must not skip it.
        import energyml.utils.data.crs as crs_module

        crs = CrsInfo(projected_epsg_code=32631, vertical_epsg_code=5715)
        pts = self._points(1000)
        single_block = reproject_to_wgs84(pts.copy(), crs, inplace=False)

        monkeypatch.setattr(crs_module, "_REPROJECT_CHUNK", 137)
        many_blocks = reproject_to_wgs84(pts.copy(), crs, inplace=False)

        np.testing.assert_allclose(many_blocks, single_block, rtol=0, atol=0)


# ---------------------------------------------------------------------------
# Buffer ownership (read_array_view must not be mutated)
# ---------------------------------------------------------------------------


class TestPointBufferOwnership:
    def test_view_input_is_copied(self):
        source = np.arange(12, dtype=np.float64).reshape(4, 3)
        view = source[:]  # a view: base is not None
        assert view.base is not None

        points = _ensure_float64_points(view)
        points[0, 0] = -999.0
        assert source[0, 0] == 0.0, "the workspace array must not be mutated through the mesh"

    def test_read_only_input_is_copied(self):
        source = np.arange(12, dtype=np.float64).reshape(4, 3)
        source.setflags(write=False)

        points = _ensure_float64_points(source)
        assert points.flags.writeable
        points[0, 0] = -999.0
        assert source[0, 0] == 0.0

    def test_own_false_keeps_the_borrowed_buffer(self):
        # Used where the caller immediately concatenates, which allocates anyway.
        source = np.arange(12, dtype=np.float64).reshape(4, 3)
        borrowed = _ensure_float64_points(source, own=False)
        assert borrowed is source

    def test_list_input_needs_no_extra_copy(self):
        points = _ensure_float64_points([[1.0, 2.0, 3.0]])
        assert points.flags.writeable
        np.testing.assert_array_equal(points, [[1.0, 2.0, 3.0]])


# ---------------------------------------------------------------------------
# Grid2d: the divergence the frame field fixes
# ---------------------------------------------------------------------------


@requires_epc22
class TestGrid2dGetsTheFullTransform:
    def test_rotation_reaches_grid2d_points(self, epc22, monkeypatch):
        import energyml.utils.data.mesh_numpy as mesh_numpy

        obj = _first_object_of_type(epc22, "Grid2d")
        assert obj is not None, "fixture changed: no Grid2dRepresentation found"

        local = read_numpy_mesh_object(obj, workspace=epc22, frame=PointFrame.LOCAL)
        local_pts = local.flat_patches()[0].points.copy()

        angle = math.pi / 2
        monkeypatch.setattr(mesh_numpy, "extract_crs_info", lambda *_a, **_k: _rotated_crs_info(angle))

        projected = read_numpy_mesh_object(obj, workspace=epc22, frame=PointFrame.PROJECTED)
        patch = projected.flat_patches()[0]
        assert patch.frame is PointFrame.PROJECTED

        # Clockwise rotation of 90 deg: (x, y) -> (y, -x). crs_displacement_np, the previous
        # fallback for Grid2d in the numpy stack, applied no rotation at all.
        expected_x = local_pts[:, 1]
        expected_y = -local_pts[:, 0]
        np.testing.assert_allclose(patch.points[:, 0], expected_x, atol=1e-9)
        np.testing.assert_allclose(patch.points[:, 1], expected_y, atol=1e-9)

    def test_reading_twice_gives_the_same_coordinates(self, epc22):
        # The blocklist was there to avoid transforming twice; the frame field must give the
        # same guarantee for every type, Grid2d included.
        obj = _first_object_of_type(epc22, "Grid2d")
        first = read_numpy_mesh_object(obj, workspace=epc22).flat_patches()[0].points.copy()
        second = read_numpy_mesh_object(obj, workspace=epc22).flat_patches()[0].points
        np.testing.assert_allclose(first, second)


# ---------------------------------------------------------------------------
# frame= on the reader
# ---------------------------------------------------------------------------


@requires_epc22
class TestReaderFrameParameter:
    def test_local_differs_from_projected_when_the_crs_has_an_offset(self, epc22):
        obj = _first_object_of_type(epc22, "Grid2d")
        local = read_numpy_mesh_object(obj, workspace=epc22, frame=PointFrame.LOCAL)
        projected = read_numpy_mesh_object(obj, workspace=epc22, frame=PointFrame.PROJECTED)

        assert local.flat_patches()[0].frame is PointFrame.LOCAL
        assert projected.flat_patches()[0].frame is PointFrame.PROJECTED

    def test_use_crs_displacement_false_maps_to_local(self, epc22):
        obj = _first_object_of_type(epc22, "Grid2d")
        result = read_numpy_mesh_object(obj, workspace=epc22, use_crs_displacement=False)
        assert result.flat_patches()[0].frame is PointFrame.LOCAL
