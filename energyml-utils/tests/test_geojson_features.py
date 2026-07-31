"""GeoJSON feature granularity, and the CRS fallback for packages that name none.

A RESQML patch is one GeoJSON feature. Exploding a patch into one feature per triangle or per
line segment repeats the whole metadata block — uuid, citation, EPSG codes — on every element:
a 882-triangle surface produced 882 features, and a 15-station wellbore 14 two-point LineStrings.

These tests use synthetic meshes so they need no EPC fixture; the CRS-fallback tests use a
minimal fake workspace.
"""

import io
import json
from types import SimpleNamespace

import numpy as np

from energyml.utils.data.export._base import GeoJSONExportOptions
from energyml.utils.data.export.geojson import export_geojson
from energyml.utils.data.mesh_numpy import (
    NumpyMultiMesh,
    NumpyPointSetMesh,
    NumpyPolylineMesh,
    NumpySurfaceMesh,
)
from energyml.utils.data.crs import PointFrame


def _export(mesh, **opt_kwargs) -> dict:
    """Run the registry writer on a single patch and parse the result."""
    multi = NumpyMultiMesh(identifier="test", patches=[mesh])
    buffer = io.StringIO()
    options = GeoJSONExportOptions(to_wgs84=False, include_metadata=False, **opt_kwargs)
    export_geojson(multi, buffer, options)
    return json.loads(buffer.getvalue())


def _square_grid_surface(n_tri: int) -> NumpySurfaceMesh:
    """A fan of *n_tri* triangles sharing point 0."""
    pts = np.array([[float(i), float(i % 3), 0.0] for i in range(n_tri + 2)], dtype=np.float64)
    faces = []
    for t in range(n_tri):
        faces.extend([3, 0, t + 1, t + 2])
    return NumpySurfaceMesh(
        identifier="surface",
        points=pts,
        faces=np.array(faces, dtype=np.int64),
        frame=PointFrame.PROJECTED,
    )


def _polyline(n_points: int, n_lines: int = 1) -> NumpyPolylineMesh:
    pts = np.array([[float(i), 0.0, float(i)] for i in range(n_points * n_lines)], dtype=np.float64)
    lines = []
    for line in range(n_lines):
        base = line * n_points
        lines.append(n_points)
        lines.extend(range(base, base + n_points))
    return NumpyPolylineMesh(
        identifier="polyline",
        points=pts,
        lines=np.array(lines, dtype=np.int64),
        frame=PointFrame.PROJECTED,
    )


class TestOneFeaturePerPatch:
    def test_triangulated_patch_is_a_single_multipolygon(self):
        doc = _export(_square_grid_surface(10))
        assert len(doc["features"]) == 1
        geometry = doc["features"][0]["geometry"]
        assert geometry["type"] == "MultiPolygon"
        assert len(geometry["coordinates"]) == 10, "one polygon per triangle, inside one feature"
        for polygon in geometry["coordinates"]:
            ring = polygon[0]
            assert ring[0] == ring[-1], "a GeoJSON ring must be closed"

    def test_single_triangle_is_a_polygon_not_a_multipolygon(self):
        doc = _export(_square_grid_surface(1))
        assert doc["features"][0]["geometry"]["type"] == "Polygon"

    def test_wellbore_polyline_is_a_single_linestring(self):
        doc = _export(_polyline(15))
        assert len(doc["features"]) == 1
        geometry = doc["features"][0]["geometry"]
        assert geometry["type"] == "LineString"
        assert len(geometry["coordinates"]) == 15, "every station in one line"

    def test_several_lines_become_one_multilinestring(self):
        doc = _export(_polyline(4, n_lines=3))
        assert len(doc["features"]) == 1
        geometry = doc["features"][0]["geometry"]
        assert geometry["type"] == "MultiLineString"
        assert [len(line) for line in geometry["coordinates"]] == [4, 4, 4]

    def test_point_set_is_a_single_multipoint(self):
        mesh = NumpyPointSetMesh(
            identifier="points",
            points=np.arange(30, dtype=np.float64).reshape(10, 3),
            frame=PointFrame.PROJECTED,
        )
        doc = _export(mesh)
        assert len(doc["features"]) == 1
        assert doc["features"][0]["geometry"]["type"] == "MultiPoint"
        assert len(doc["features"][0]["geometry"]["coordinates"]) == 10

    def test_metadata_is_written_once_per_patch(self):
        """The point of the change: 10 triangles must not carry 10 copies of the citation."""
        multi = NumpyMultiMesh(identifier="test", patches=[_square_grid_surface(10)])
        buffer = io.StringIO()
        export_geojson(multi, buffer, GeoJSONExportOptions(to_wgs84=False, properties={"marker": "x"}))
        doc = json.loads(buffer.getvalue())
        assert sum(1 for f in doc["features"] if f["properties"].get("marker") == "x") == 1


class TestExplodeElementsOption:
    def test_explode_restores_one_feature_per_element(self):
        doc = _export(_square_grid_surface(10), explode_elements=True)
        assert len(doc["features"]) == 10
        assert {f["geometry"]["type"] for f in doc["features"]} == {"Polygon"}
        assert [f["properties"]["element_index"] for f in doc["features"]] == list(range(10))

    def test_explode_splits_a_polyline_per_line(self):
        doc = _export(_polyline(4, n_lines=3), explode_elements=True)
        assert len(doc["features"]) == 3
        assert {f["geometry"]["type"] for f in doc["features"]} == {"LineString"}


class TestPackageDefaultCrs:
    """`PointGeometry.LocalCrs` is optional; a package may declare its CRS once for all."""

    @staticmethod
    def _workspace(objects):
        """Minimal duck-typed workspace: list_objects() + get_object()."""
        metadata = [
            SimpleNamespace(uuid=f"uuid-{i}", uri=f"eml:///{type(o).__name__}(uuid-{i})", object_type=type(o).__name__)
            for i, o in enumerate(objects)
        ]
        by_uri = {m.uri: o for m, o in zip(metadata, objects)}
        return SimpleNamespace(
            list_objects=lambda resolve_titles=True: metadata,
            get_object=lambda uri: by_uri.get(uri),
        )

    def test_the_only_projected_crs_is_used(self):
        from energyml.utils.data.helper import get_package_default_crs

        class ProjectedCrs:
            pass

        crs = ProjectedCrs()
        assert get_package_default_crs(self._workspace([crs])) is crs

    def test_a_full_local_crs_wins_over_a_projected_one(self):
        from energyml.utils.data.helper import get_package_default_crs

        class ProjectedCrs:
            pass

        class LocalEngineeringCompoundCrs:
            pass

        local = LocalEngineeringCompoundCrs()
        found = get_package_default_crs(self._workspace([ProjectedCrs(), local]))
        assert found is local, "the local frame describes offsets and rotation, the projected one does not"

    def test_an_ambiguous_package_returns_nothing(self):
        from energyml.utils.data.helper import get_package_default_crs

        class ProjectedCrs:
            pass

        # Two candidates of the same kind: choosing one would silently place the geometry
        # in the wrong frame.
        assert get_package_default_crs(self._workspace([ProjectedCrs(), ProjectedCrs()])) is None

    def test_a_lone_vertical_crs_is_never_chosen(self):
        from energyml.utils.data.helper import get_package_default_crs

        class VerticalCrs:
            pass

        assert get_package_default_crs(self._workspace([VerticalCrs()])) is None

    def test_no_workspace_is_not_an_error(self):
        from energyml.utils.data.helper import get_package_default_crs

        assert get_package_default_crs(None) is None
