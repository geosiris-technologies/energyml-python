# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Integration tests for :mod:`energyml.utils.data.crs`.

Real energyml objects are loaded from the EPC test fixtures shipped in
``rc/epc/``.  No mock dataclasses — the installed ``energyml-resqml2*`` and
``energyml-eml*`` packages provide the actual xsdata-generated classes.

EPC fixtures
─────────────
* ``testingPackageCpp.epc``   — RESQML v2.0.1 (also contains mixed v2.3 CRS)
* ``testingPackageCpp22.epc`` — RESQML v2.2 / EML v2.3

Both files are committed to ``rc/epc/`` and are available in CI once the
parent workspace dev-dependencies are installed.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Optional

import pytest

from energyml.utils.data.crs import CrsInfo, _uom_to_str, extract_crs_info
from energyml.utils.data.helper import (
    get_crs_offsets_and_angle,
    get_projected_epsg_code,
    get_projected_uom,
    get_vertical_epsg_code,
    is_z_reversed,
)
from energyml.utils.epc import Epc
from energyml.utils.introspection import get_obj_uuid, get_object_attribute_rgx

# ---------------------------------------------------------------------------
# EPC file paths
# ---------------------------------------------------------------------------

_RC = Path(__file__).parent.parent / "rc" / "epc"
EPC20_PATH = _RC / "testingPackageCpp.epc"
EPC22_PATH = _RC / "testingPackageCpp22.epc"


# ---------------------------------------------------------------------------
# Session-scoped fixtures (EPC loaded once per test session)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def epc20() -> Epc:
    if not EPC20_PATH.exists():
        pytest.skip(f"EPC fixture not found: {EPC20_PATH}")
    return Epc.read_file(str(EPC20_PATH))


@pytest.fixture(scope="session")
def epc22() -> Epc:
    if not EPC22_PATH.exists():
        pytest.skip(f"EPC fixture not found: {EPC22_PATH}")
    return Epc.read_file(str(EPC22_PATH))


# ---------------------------------------------------------------------------
# Shared helper — walk representation → CRS DOR → resolved object
# ---------------------------------------------------------------------------


def _resolve_crs_from_grid(grid_obj: Any, epc: Epc) -> Optional[Any]:
    """Resolve the CRS object linked from a Grid2DRepresentation."""
    # v2.0.1: local_crs sits on the geometry patch
    dor = get_object_attribute_rgx(grid_obj, "[Ll]ocal[_]?[Cc]rs")
    if dor is None:
        dor = get_object_attribute_rgx(
            grid_obj,
            "[Gg]rid2[Dd][Pp]atch.[Gg]eometry.[Ll]ocal[_]?[Cc]rs",
        )
    if dor is None:
        return None
    uuid = get_obj_uuid(dor)
    candidates = epc.get_object_by_uuid(uuid) if uuid else []
    return candidates[0] if candidates else None


# ===========================================================================
# DTO and pure-function tests (no EPC required)
# ===========================================================================


class TestCrsInfoDto:
    def test_defaults(self):
        info = CrsInfo()
        assert info.x_offset == 0.0
        assert info.y_offset == 0.0
        assert info.z_offset == 0.0
        assert info.projected_epsg_code is None
        assert info.projected_uom is None
        assert info.vertical_epsg_code is None
        assert info.vertical_uom is None
        assert info.z_increasing_downward is False
        assert info.areal_rotation_value == 0.0
        assert info.areal_rotation_uom == "rad"
        assert info.azimuth_reference is None
        assert info.source_type is None

    def test_areal_rotation_rad_already_radians(self):
        info = CrsInfo(areal_rotation_value=1.5708, areal_rotation_uom="rad")
        assert info.areal_rotation_rad() == pytest.approx(1.5708)

    def test_areal_rotation_rad_degrees(self):
        info = CrsInfo(areal_rotation_value=90.0, areal_rotation_uom="degr")
        assert info.areal_rotation_rad() == pytest.approx(math.pi / 2)

    def test_areal_rotation_rad_zero(self):
        assert CrsInfo(areal_rotation_value=0.0, areal_rotation_uom="degr").areal_rotation_rad() == 0.0

    def test_as_transform_args(self):
        info = CrsInfo(
            x_offset=100.0,
            y_offset=200.0,
            z_offset=-50.0,
            areal_rotation_value=0.5,
            areal_rotation_uom="rad",
            z_increasing_downward=True,
        )
        kwargs = info.as_transform_args()
        assert kwargs["x_offset"] == 100.0
        assert kwargs["y_offset"] == 200.0
        assert kwargs["z_offset"] == -50.0
        assert kwargs["areal_rotation"] == 0.5
        assert kwargs["rotation_uom"] == "rad"
        assert kwargs["z_is_up"] is False  # z_increasing_downward=True → z_is_up=False

    def test_none_returns_default(self):
        info = extract_crs_info(None)
        assert info.x_offset == 0.0
        assert info.z_increasing_downward is False
        assert info.source_type is None


class TestUomToStr:
    def test_plain_string(self):
        assert _uom_to_str("m") == "m"

    def test_enum_like_with_dot(self):
        assert _uom_to_str("LengthUom.ft") == "ft"

    def test_none_returns_none(self):
        assert _uom_to_str(None) is None

    def test_empty_after_split_returns_none(self):
        assert _uom_to_str("") is None


# ===========================================================================
# RESQML v2.0.1 — testingPackageCpp.epc
# ===========================================================================


class TestV201LocalTime3DCrs:
    """
    LocalTime3DCrs  uuid=dbd637d5-4528-4145-908b-5f7136824f6d
    xoffset=1.0  yoffset=0.1  zoffset=15.0  projected_uom=M  z_down=False
    """

    UUID = "dbd637d5-4528-4145-908b-5f7136824f6d"

    @pytest.fixture(scope="class")
    def info(self, epc20):
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj)

    def test_source_type(self, info):
        assert "LocalTime3DCrs" in info.source_type

    def test_offsets(self, info):
        assert info.x_offset == pytest.approx(1.0)
        assert info.y_offset == pytest.approx(0.1)
        assert info.z_offset == pytest.approx(15.0)

    def test_projected_uom(self, info):
        # xsdata v2.0.1 enum → _uom_to_str keeps the enum member name casing
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"

    def test_vertical_uom(self, info):
        assert info.vertical_uom is not None
        assert info.vertical_uom.lower() == "m"

    def test_z_increasing_downward(self, info):
        assert info.z_increasing_downward is False

    def test_no_epsg(self, info):
        assert info.projected_epsg_code is None
        assert info.vertical_epsg_code is None

    def test_rotation_zero(self, info):
        assert info.areal_rotation_value == pytest.approx(0.0)


class TestV201LocalDepth3DCrs:
    """
    LocalDepth3DCrs  uuid=0ae56ef3-fc79-405b-8deb-6942e0f2e77c
    projected_epsg=23031  projected_uom=M  z_down=False  offsets all zero
    """

    UUID = "0ae56ef3-fc79-405b-8deb-6942e0f2e77c"

    @pytest.fixture(scope="class")
    def info(self, epc20):
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj)

    def test_source_type(self, info):
        assert "LocalDepth3DCrs" in info.source_type

    def test_projected_epsg(self, info):
        assert info.projected_epsg_code == 23031

    def test_projected_uom(self, info):
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"

    def test_z_increasing_downward(self, info):
        # The linked VerticalCrs has direction=up (or not set) in this fixture
        assert info.z_increasing_downward is False

    def test_offsets_zero(self, info):
        assert info.x_offset == pytest.approx(0.0)
        assert info.y_offset == pytest.approx(0.0)
        assert info.z_offset == pytest.approx(0.0)


class TestV201LocalEngineeringCompoundCrs:
    """
    LocalEngineeringCompoundCrs  uuid=95330cec-164c-4165-9fb9-c56477ae7f8a
    (EML v2.3 object inside the v2.0.1 EPC)
    projected_epsg=23031 (only when workspace provided)
    z_down=True  azref=grid north
    """

    UUID = "95330cec-164c-4165-9fb9-c56477ae7f8a"

    def test_z_down_inline_no_workspace(self, epc20):
        """VerticalAxis direction is readable without workspace."""
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=None)
        assert info.z_increasing_downward is True

    def test_projected_epsg_requires_workspace(self, epc20):
        """EPSG is on linked LocalEngineering2DCrs — only available via workspace."""
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        info_no_ws = extract_crs_info(obj, workspace=None)
        assert info_no_ws.projected_epsg_code is None

        info_ws = extract_crs_info(obj, workspace=epc20)
        assert info_ws.projected_epsg_code == 23031

    def test_full_resolution_with_workspace(self, epc20):
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=epc20)
        assert info.projected_epsg_code == 23031
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"
        assert info.vertical_uom is not None
        assert info.vertical_uom.lower() == "m"
        assert info.z_increasing_downward is True
        assert info.azimuth_reference == "grid north"


class TestV201LocalEngineering2DCrs:
    """
    LocalEngineering2DCrs  uuid=811f8e68-c0e4-5f90-b9cf-03f7e3d53ca4
    (EML v2.3 object inside the v2.0.1 EPC)
    projected_epsg=23031  projected_uom=M  azref=grid north  offsets zero
    """

    UUID = "811f8e68-c0e4-5f90-b9cf-03f7e3d53ca4"

    @pytest.fixture(scope="class")
    def info(self, epc20):
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj)

    def test_projected_epsg(self, info):
        assert info.projected_epsg_code == 23031

    def test_projected_uom(self, info):
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"

    def test_no_vertical_uom(self, info):
        # 2D CRS carries no Z information
        assert info.vertical_uom is None

    def test_z_increasing_downward(self, info):
        assert info.z_increasing_downward is False

    def test_azimuth_reference(self, info):
        assert info.azimuth_reference == "grid north"

    def test_offsets_zero(self, info):
        assert info.x_offset == pytest.approx(0.0)
        assert info.y_offset == pytest.approx(0.0)


class TestV201VerticalCrs:
    """
    VerticalCrs  uuid=1f6cf904-336c-5202-a13d-7c9b142cd406
    (EML v2.3 object inside the v2.0.1 EPC)
    vertical_uom=M  z_down=True  no projected info
    """

    UUID = "1f6cf904-336c-5202-a13d-7c9b142cd406"

    @pytest.fixture(scope="class")
    def info(self, epc20):
        obj = epc20.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj)

    def test_vertical_uom(self, info):
        assert info.vertical_uom is not None
        assert info.vertical_uom.lower() == "m"

    def test_z_increasing_downward(self, info):
        assert info.z_increasing_downward is True

    def test_no_projected_info(self, info):
        assert info.projected_epsg_code is None
        assert info.projected_uom is None


class TestV201Grid2DCrsResolution:
    """
    Grid2DRepresentation → local_crs DOR → resolved CRS → extract_crs_info.
    """

    def test_grid_030a82f6_resolves_to_local_time_crs(self, epc20):
        grid = epc20.get_object_by_uuid("030a82f6-10a7-4ecf-af03-54749e098624")[0]
        crs = _resolve_crs_from_grid(grid, epc20)
        assert crs is not None
        assert crs.uuid == "dbd637d5-4528-4145-908b-5f7136824f6d"
        assert "LocalTime3DCrs" in type(crs).__name__
        info = extract_crs_info(crs, workspace=epc20)
        assert info.x_offset == pytest.approx(1.0)
        assert info.y_offset == pytest.approx(0.1)
        assert info.z_offset == pytest.approx(15.0)

    def test_grid_aa5b90f1_resolves_to_local_depth_crs(self, epc20):
        grid = epc20.get_object_by_uuid("aa5b90f1-2eab-4fa6-8720-69dd4fd51a4d")[0]
        crs = _resolve_crs_from_grid(grid, epc20)
        assert crs is not None
        assert crs.uuid == "0ae56ef3-fc79-405b-8deb-6942e0f2e77c"
        info = extract_crs_info(crs, workspace=epc20)
        assert info.projected_epsg_code == 23031

    def test_grid_4e56b0e4_resolves_to_same_depth_crs(self, epc20):
        grid = epc20.get_object_by_uuid("4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80")[0]
        crs = _resolve_crs_from_grid(grid, epc20)
        assert crs is not None
        assert crs.uuid == "0ae56ef3-fc79-405b-8deb-6942e0f2e77c"


# ===========================================================================
# RESQML v2.2 / EML v2.3 — testingPackageCpp22.epc
# ===========================================================================


class TestV22LocalEngineering2DCrsNoEpsg:
    """
    LocalEngineering2DCrs  uuid=997796f5-da9d-5175-9fb7-e592957b73fb
    x=1.0  y=0.1  projected_uom=M  no EPSG  azref=grid north
    """

    UUID = "997796f5-da9d-5175-9fb7-e592957b73fb"

    @pytest.fixture(scope="class")
    def info(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj)

    def test_offsets(self, info):
        assert info.x_offset == pytest.approx(1.0)
        assert info.y_offset == pytest.approx(0.1)
        assert info.z_offset == pytest.approx(0.0)

    def test_no_epsg(self, info):
        assert info.projected_epsg_code is None

    def test_projected_uom(self, info):
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"

    def test_azimuth_reference(self, info):
        assert info.azimuth_reference == "grid north"

    def test_z_increasing_downward(self, info):
        assert info.z_increasing_downward is False


class TestV22LocalEngineering2DCrsWithEpsg:
    """
    LocalEngineering2DCrs  uuid=671ffdeb-f25c-513a-a4a2-1774d3ac20c6
    projected_epsg=23031  projected_uom=M  azref=grid north  offsets zero
    """

    UUID = "671ffdeb-f25c-513a-a4a2-1774d3ac20c6"

    @pytest.fixture(scope="class")
    def info(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj)

    def test_projected_epsg(self, info):
        assert info.projected_epsg_code == 23031

    def test_projected_uom(self, info):
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"

    def test_azimuth_reference(self, info):
        assert info.azimuth_reference == "grid north"

    def test_offsets_zero(self, info):
        assert info.x_offset == pytest.approx(0.0)
        assert info.y_offset == pytest.approx(0.0)


class TestV22CompoundCrsWithOffsets:
    """
    LocalEngineeringCompoundCrs  uuid=f0e9f421-b902-4392-87d8-6495c02f2fbe
    Links to LocalEngineering2DCrs (997796f5) with x=1.0, y=0.1.
    z=15.0  z_down=True  no projected EPSG.
    Note: the inline VerticalAxis uses a time UOM (S), the resolved
    VerticalCrs uses depth UOM (M) — demonstrates with/without workspace.
    """

    UUID = "f0e9f421-b902-4392-87d8-6495c02f2fbe"

    def test_inline_z_offset_without_workspace(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=None)
        assert info.z_offset == pytest.approx(15.0)

    def test_inline_z_direction_without_workspace(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=None)
        assert info.z_increasing_downward is True

    def test_no_horizontal_info_without_workspace(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=None)
        assert info.projected_epsg_code is None
        assert info.x_offset == pytest.approx(0.0)
        assert info.y_offset == pytest.approx(0.0)

    def test_full_resolution_with_workspace(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=epc22)
        # Horizontal from linked LocalEngineering2DCrs (997796f5)
        assert info.x_offset == pytest.approx(1.0)
        assert info.y_offset == pytest.approx(0.1)
        assert info.z_offset == pytest.approx(15.0)
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"
        assert info.projected_epsg_code is None
        assert info.z_increasing_downward is True
        assert info.azimuth_reference == "grid north"

    def test_vertical_uom_resolved_from_vertical_crs(self, epc22):
        """With workspace the vertical UOM comes from the linked VerticalCrs (M), not the inline time axis (S)."""
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        info = extract_crs_info(obj, workspace=epc22)
        assert info.vertical_uom is not None
        assert info.vertical_uom.lower() == "m"


class TestV22CompoundCrsWithEpsg:
    """
    LocalEngineeringCompoundCrs  uuid=6a18c177-93be-41ac-9084-f84bbb31f46d
    projected_epsg=23031  z_down=True  all offsets zero  vertical_uom=M
    """

    UUID = "6a18c177-93be-41ac-9084-f84bbb31f46d"

    @pytest.fixture(scope="class")
    def info(self, epc22):
        obj = epc22.get_object_by_uuid(self.UUID)[0]
        return extract_crs_info(obj, workspace=epc22)

    def test_projected_epsg(self, info):
        assert info.projected_epsg_code == 23031

    def test_projected_uom(self, info):
        assert info.projected_uom is not None
        assert info.projected_uom.lower() == "m"

    def test_vertical_uom(self, info):
        assert info.vertical_uom is not None
        assert info.vertical_uom.lower() == "m"

    def test_z_increasing_downward(self, info):
        assert info.z_increasing_downward is True

    def test_offsets_zero(self, info):
        assert info.x_offset == pytest.approx(0.0)
        assert info.y_offset == pytest.approx(0.0)
        assert info.z_offset == pytest.approx(0.0)

    def test_azimuth_reference(self, info):
        assert info.azimuth_reference == "grid north"


class TestV22VerticalCrs:
    """
    Two standalone VerticalCrs objects in the v2.2 EPC.
    Both: vertical_uom=M  z_down=True
    """

    @pytest.mark.parametrize("uuid", [
        "65cd199f-156b-5112-ad3e-b4f54a2aa77b",
        "355174db-6226-57ae-a5a6-92f33825fed4",
    ])
    def test_vertical_uom_and_direction(self, uuid, epc22):
        obj = epc22.get_object_by_uuid(uuid)[0]
        info = extract_crs_info(obj)
        assert info.vertical_uom is not None
        assert info.vertical_uom.lower() == "m"
        assert info.z_increasing_downward is True
        assert info.projected_epsg_code is None
        assert info.projected_uom is None


# ===========================================================================
# Legacy delegate functions (helper.py forwards to extract_crs_info)
# ===========================================================================


class TestDelegateFunctions:
    """
    Verify the five legacy helpers in ``helper.py`` still work correctly now
    that they delegate to ``extract_crs_info``.

    Uses LocalDepth3DCrs (0ae56ef3) and LocalTime3DCrs (dbd637d5) from epc20.
    """

    def test_is_z_reversed_depth_crs_false(self, epc20):
        crs = epc20.get_object_by_uuid("0ae56ef3-fc79-405b-8deb-6942e0f2e77c")[0]
        assert is_z_reversed(crs) is False

    def test_is_z_reversed_compound_crs_true(self, epc20):
        # CompoundCrs 95330cec has z_increasing_downward=True
        crs = epc20.get_object_by_uuid("95330cec-164c-4165-9fb9-c56477ae7f8a")[0]
        assert is_z_reversed(crs) is True

    def test_is_z_reversed_none(self):
        assert is_z_reversed(None) is False

    def test_get_projected_epsg_code(self, epc20):
        crs = epc20.get_object_by_uuid("0ae56ef3-fc79-405b-8deb-6942e0f2e77c")[0]
        assert get_projected_epsg_code(crs) == 23031

    def test_get_projected_epsg_code_no_epsg(self, epc20):
        crs = epc20.get_object_by_uuid("dbd637d5-4528-4145-908b-5f7136824f6d")[0]
        assert get_projected_epsg_code(crs) is None

    def test_get_projected_uom(self, epc20):
        crs = epc20.get_object_by_uuid("0ae56ef3-fc79-405b-8deb-6942e0f2e77c")[0]
        uom = get_projected_uom(crs)
        assert uom is not None
        assert uom.lower() == "m"

    def test_get_vertical_epsg_code_none(self, epc20):
        # Neither CRS in this EPC has a vertical EPSG code
        crs = epc20.get_object_by_uuid("0ae56ef3-fc79-405b-8deb-6942e0f2e77c")[0]
        assert get_vertical_epsg_code(crs) is None

    def test_get_crs_offsets_and_angle_local_time(self, epc20):
        crs = epc20.get_object_by_uuid("dbd637d5-4528-4145-908b-5f7136824f6d")[0]
        x, y, z, (angle, uom) = get_crs_offsets_and_angle(crs)
        assert x == pytest.approx(1.0)
        assert y == pytest.approx(0.1)
        assert z == pytest.approx(15.0)
        assert angle == pytest.approx(0.0)

    def test_get_crs_offsets_and_angle_none(self):
        x, y, z, (angle, uom) = get_crs_offsets_and_angle(None)
        assert x == 0.0
        assert y == 0.0
        assert z == 0.0
        assert angle == 0.0
        assert uom == "rad"


