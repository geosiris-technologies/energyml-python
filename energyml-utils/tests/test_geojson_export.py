# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the GeoJSON export : energyml metadata, CRS declaration and WGS84 reprojection.

The tests run against the real EPC fixture ``rc/epc/80wells_surf.epc`` (RESQML v2.2, whose
representations reference a standalone ``ProjectedCrs`` with EPSG:3949 — Lambert-93 CC49).

The reprojection tests are skipped when the ``crs`` extra (pyproj) is not installed.
"""
from __future__ import annotations

import io
import json
from pathlib import Path

import numpy as np
import pytest

from energyml.utils.data import crs as crs_module
from energyml.utils.data.crs import (
    build_source_crs_id,
    crs_ogc_uri,
    crs_urn,
    extract_crs_info,
    is_pyproj_available,
)
from energyml.utils.data.export import GeoJSONExportOptions, _geojson_crs_members, _feature_id, export_geojson
from energyml.utils.epc import Epc
from energyml.utils.introspection import get_object_metadata

_EPC_PATH = Path(__file__).parent.parent / "rc" / "epc" / "80wells_surf.epc"

requires_pyproj = pytest.mark.skipif(not is_pyproj_available(), reason="requires the 'crs' extra (pyproj)")


@pytest.fixture(scope="module")
def epc() -> Epc:
    # rc/**/*.epc is git-ignored and only the needed fixtures are force-added, so a working copy
    # may legitimately lack this one — skip instead of erroring out of the fixture setup.
    if not _EPC_PATH.is_file():
        pytest.skip(f"fixture {_EPC_PATH.name} not present in rc/epc/")
    return Epc.read_file(str(_EPC_PATH))


@pytest.fixture(scope="module")
def point_set_object(epc: Epc):
    obj = next((o for o in epc.energyml_objects if "PointSet" in type(o).__name__), None)
    if obj is None:
        pytest.skip("no PointSetRepresentation in the fixture")
    return obj


def _read_multi_mesh(obj, epc):
    from energyml.utils.data.mesh_numpy import read_numpy_mesh_object

    return read_numpy_mesh_object(obj, workspace=epc, use_crs_displacement=True)


def _export(obj, epc, options: GeoJSONExportOptions) -> dict:
    out = io.StringIO()
    export_geojson(_read_multi_mesh(obj, epc), out, options)
    return json.loads(out.getvalue())


# ---------------------------------------------------------------------------
# CRS identifiers
# ---------------------------------------------------------------------------


class TestCrsIdentifiers:
    def test_ogc_uri_and_urn(self):
        assert crs_ogc_uri(32631) == "http://www.opengis.net/def/crs/EPSG/0/32631"
        assert crs_urn(32631) == "urn:ogc:def:crs:EPSG::32631"

    def test_build_source_crs_id(self):
        assert build_source_crs_id(32631) == "EPSG:32631"
        assert build_source_crs_id(32631, 5773) == "EPSG:32631+EPSG:5773"
        assert build_source_crs_id(None) is None
        assert build_source_crs_id(None, 5773) is None

    def test_crs_members_horizontal_only(self):
        members = _geojson_crs_members(3949, None)
        assert members["crs"] == {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3949"}}
        assert members["coordRefSys"] == crs_ogc_uri(3949)

    def test_crs_members_compound(self):
        members = _geojson_crs_members(32631, 5773)
        assert members["coordRefSys"] == [crs_ogc_uri(32631), crs_ogc_uri(5773)]

    def test_no_crs_member_without_epsg(self):
        assert _geojson_crs_members(None, 5773) == {}


class TestFeatureId:
    def test_uuid_only(self):
        assert _feature_id("abc") == "abc"

    def test_with_patch_and_element(self):
        assert _feature_id("abc", 1) == "abc_1"
        assert _feature_id("abc", 1, 7) == "abc_1_7"

    def test_without_uuid(self):
        assert _feature_id(None, 1) is None


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


class TestObjectMetadata:
    def test_metadata_of_a_real_object(self, point_set_object):
        metadata = get_object_metadata(point_set_object)
        assert metadata["uuid"] == point_set_object.uuid
        assert metadata["qualified_type"].endswith(".PointSetRepresentation")
        assert metadata["title"]
        # dates are exported as ISO 8601 strings
        assert "T" in metadata["creation"]

    def test_metadata_of_none(self):
        assert get_object_metadata(None) == {}


# ---------------------------------------------------------------------------
# GeoJSON output
# ---------------------------------------------------------------------------


class TestGeoJsonExport:
    def test_features_carry_id_and_metadata(self, point_set_object, epc):
        doc = _export(point_set_object, epc, GeoJSONExportOptions(indent=None))
        assert doc["type"] == "FeatureCollection"
        feature = doc["features"][0]
        assert feature["type"] == "Feature"
        assert feature["id"].startswith(point_set_object.uuid)
        properties = feature["properties"]
        assert properties["uuid"] == point_set_object.uuid
        assert properties["qualified_type"].endswith(".PointSetRepresentation")
        assert properties["title"]
        assert properties["projected_epsg_code"] == 3949

    def test_collection_bbox(self, point_set_object, epc):
        doc = _export(point_set_object, epc, GeoJSONExportOptions(indent=None))
        assert len(doc["bbox"]) == 6
        assert doc["bbox"][0] <= doc["bbox"][3]
        assert doc["bbox"][1] <= doc["bbox"][4]

    def test_metadata_can_be_disabled(self, point_set_object, epc):
        doc = _export(point_set_object, epc, GeoJSONExportOptions(indent=None, include_metadata=False))
        assert "title" not in doc["features"][0]["properties"]

    def test_source_crs_is_declared_when_not_reprojected(self, point_set_object, epc):
        doc = _export(point_set_object, epc, GeoJSONExportOptions(indent=None, to_wgs84=False))
        assert doc["crs"]["properties"]["name"] == crs_urn(3949)
        assert doc["coordRefSys"] == crs_ogc_uri(3949)
        # coordinates stay in the projected CRS (metric values, far outside the lon/lat range)
        assert abs(doc["features"][0]["geometry"]["coordinates"][0][0]) > 180

    def test_fallback_when_pyproj_is_missing(self, point_set_object, epc, monkeypatch):
        monkeypatch.setattr(crs_module, "is_pyproj_available", lambda: False)
        doc = _export(point_set_object, epc, GeoJSONExportOptions(indent=None, to_wgs84=True))
        # no reprojection, but the source CRS must be advertised
        assert doc["crs"]["properties"]["name"] == crs_urn(3949)
        assert abs(doc["features"][0]["geometry"]["coordinates"][0][0]) > 180

    @requires_pyproj
    def test_wgs84_is_the_default(self, point_set_object, epc):
        doc = _export(point_set_object, epc, GeoJSONExportOptions(indent=None))
        # an RFC 7946 document is implicitly CRS84 and must NOT carry a 'crs' member
        assert "crs" not in doc
        lon, lat = doc["features"][0]["geometry"]["coordinates"][0][:2]
        assert -180.0 <= lon <= 180.0
        assert -90.0 <= lat <= 90.0
        properties = doc["features"][0]["properties"]
        assert properties["source_crs"] == "EPSG:3949"
        assert properties["coordinates_crs"] == "OGC:CRS84"


# ---------------------------------------------------------------------------
# Reprojection
# ---------------------------------------------------------------------------


@requires_pyproj
class TestReprojection:
    def test_utm31n_to_wgs84(self):
        from energyml.utils.data.crs import reproject_to_wgs84

        points = np.array([[463000.0, 6570000.0, -1500.0]])
        result = reproject_to_wgs84(points, projected_epsg_code=32631)
        assert result.shape == (1, 3)
        assert result[0][0] == pytest.approx(2.350943, abs=1e-5)
        assert result[0][1] == pytest.approx(59.267329, abs=1e-5)
        # without a vertical CRS the Z column is left untouched
        assert result[0][2] == pytest.approx(-1500.0)

    def test_input_is_not_modified(self):
        from energyml.utils.data.crs import reproject_to_wgs84

        points = np.array([[463000.0, 6570000.0, -1500.0]])
        original = points.copy()
        reproject_to_wgs84(points, projected_epsg_code=32631)
        assert np.array_equal(points, original)

    def test_missing_epsg_raises(self):
        from energyml.utils.data.crs import reproject_to_wgs84
        from energyml.utils.exception import NotEnoughInformationError

        with pytest.raises(NotEnoughInformationError):
            reproject_to_wgs84(np.zeros((1, 3)))

    def test_crs_info_codes_are_used(self, point_set_object, epc):
        from energyml.utils.data.crs import reproject_to_wgs84
        from energyml.utils.data.helper import get_crs_obj

        crs_obj = get_crs_obj(context_obj=point_set_object, root_obj=point_set_object, workspace=epc)
        crs_info = extract_crs_info(crs_obj, epc)
        assert crs_info.projected_epsg_code == 3949
        result = reproject_to_wgs84(np.array([[1656431.13, 8190610.64, 37.15]]), crs_info)
        assert result[0][0] == pytest.approx(2.4055, abs=1e-3)
        assert result[0][1] == pytest.approx(48.9140, abs=1e-3)
