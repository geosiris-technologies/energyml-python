# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Integration examples for :mod:`energyml.utils.data.crs`.

Reads real EPC files from ``rc/epc/`` and exercises :func:`extract_crs_info`
against every CRS object they contain.  Also shows how to walk from a
``Grid2DRepresentation`` to its CRS and call ``extract_crs_info`` on the
resolved object.

Run from the workspace root::

    poetry run python example/attic/crs_info_from_epc.py

Expected output: all test cases show ``[PASS]``.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, List, Optional


# Run $env:PYTHONPATH="src" if it fails to be executed from the project root.

# ── make the local ``src/`` take precedence when running directly ──────────
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from energyml.utils.epc import Epc
from energyml.utils.introspection import get_obj_uuid, get_object_attribute_rgx
from energyml.utils.data.crs import CrsInfo, extract_crs_info

# suppress noise from EPC loading
logging.basicConfig(level=logging.ERROR)

# ── EPC file paths (relative to workspace root) ────────────────────────────
_ROOT = Path(__file__).parent.parent.parent
EPC20_PATH = str(_ROOT / "rc" / "epc" / "testingPackageCpp.epc")
EPC22_PATH = str(_ROOT / "rc" / "epc" / "testingPackageCpp22.epc")

# ── Simple test harness ────────────────────────────────────────────────────
_passed = 0
_failed = 0


def check(label: str, expected: Any, actual: Any, *, approx: bool = False) -> None:
    """Print PASS / FAIL and update counters."""
    global _passed, _failed
    if approx:
        import math
        ok = (expected is None and actual is None) or (
            isinstance(expected, (int, float))
            and isinstance(actual, (int, float))
            and math.isclose(float(expected), float(actual), rel_tol=1e-6)
        )
    else:
        ok = expected == actual
    if ok:
        _passed += 1
        print(f"  [PASS] {label}")
    else:
        _failed += 1
        print(f"  [FAIL] {label}")
        print(f"         expected : {expected!r}")
        print(f"         actual   : {actual!r}")


def section(title: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def _resolve_crs_from_grid(grid_obj: Any, epc: Epc) -> Optional[Any]:
    """
    Walk from a representation object to its CRS document.

    The CRS DOR is always present in ``LocalCrs`` — the difference between
    RESQML versions is the depth of the path:

    * **v2.2** : ``Geometry.LocalCrs``  (``PointGeometry`` sits directly on the object)
    * **v2.0.1**: ``Grid2dPatch.Geometry.LocalCrs``  (geometry is inside a patch sub-object)

    ``get_object_attribute_rgx`` resolves dot-delimited paths at exactly the
    depth specified, so we try the shallower v2.2 path first, then fall back
    to the deeper v2.0.1 path.

    Returns the resolved CRS object or ``None``.
    """
    # v2.2: Geometry.LocalCrs (PointGeometry directly on the object)
    dor = get_object_attribute_rgx(grid_obj, "[Gg]eometry.[Ll]ocal[_]?[Cc]rs")

    if dor is None:
        # v2.0.1: Grid2dPatch.Geometry.LocalCrs (geometry wrapped in a patch)
        dor = get_object_attribute_rgx(
            grid_obj,
            "[Gg]rid2[Dd][Pp]atch.[Gg]eometry.[Ll]ocal[_]?[Cc]rs",
        )

    if dor is None:
        return None

    uuid = get_obj_uuid(dor)
    if not uuid:
        return None

    candidates = epc.get_object_by_uuid(uuid)
    return candidates[0] if candidates else None


def resolve_crs_from_triangulated_set(triangulated_obj: Any, epc: Epc) -> List[Optional[Any]]:
    """
    Walk from a TriangulatedSetRepresentation to its CRS document.

    Each patch of a TriangulatedSetRepresentation may reference a CRS via its
    ``local_crs`` attribute.  This function tries to resolve the first patch's CRS.
    """
    dor = get_object_attribute_rgx(triangulated_obj, "triangle_patch.\d+.geometry.local_crs")
    # print(f"  Found DOR for TriangulatedSetRepresentation patch CRS: {dor}")
    if dor is None:
        return []
    
    if isinstance(dor, list):
        candidates = []
        for d in dor:
            uuid = get_obj_uuid(d)
            if uuid:
                obj_candidates = epc.get_object_by_uuid(uuid)
                print(f"  Found DOR for TriangulatedSetRepresentation patch CRS: {d} → candidates: {len(obj_candidates)}")
                candidates.append(obj_candidates[0] if obj_candidates else None)
        return candidates

    return None


# ===========================================================================
# RESQML v2.0.1  —  testingPackageCpp.epc
# ===========================================================================

section("Loading testingPackageCpp.epc  (RESQML v2.0.1)")
epc20 = Epc.read_file(EPC20_PATH)
print(f"  Loaded {len(epc20.energyml_objects)} objects.")

# ── LocalTime3DCrs ─────────────────────────────────────────────────────────

section("v2.0.1 · LocalTime3DCrs  (uuid dbd637d5…)")

local_time_crs = epc20.get_object_by_uuid("dbd637d5-4528-4145-908b-5f7136824f6d")[0]

# Test: extract without workspace (all data is inline for v2.0.1)
info: CrsInfo = extract_crs_info(local_time_crs)

check("source_type", "LocalTime3DCrs", info.source_type)
check("x_offset", 1.0, info.x_offset, approx=True)
check("y_offset", 0.1, info.y_offset, approx=True)
check("z_offset", 15.0, info.z_offset, approx=True)
check("projected_uom (raw from xsdata enum)", "M", info.projected_uom)
check("vertical_uom  (raw from xsdata enum)", "M", info.vertical_uom)
# ZIncreasingDownward=true in the file; VerticalUnknownCrs sub-object carries
# no direction field, so the sentinel correctly preserves the top-level value.
check("z_increasing_downward", True, info.z_increasing_downward)
check("areal_rotation_value", 0.0, info.areal_rotation_value, approx=True)
check("projected_epsg_code", None, info.projected_epsg_code)
check("vertical_epsg_code", None, info.vertical_epsg_code)
check("azimuth_reference", None, info.azimuth_reference)

# ── LocalDepth3DCrs ────────────────────────────────────────────────────────

section("v2.0.1 · LocalDepth3DCrs  (uuid 0ae56ef3…)")

local_depth_crs = epc20.get_object_by_uuid("0ae56ef3-fc79-405b-8deb-6942e0f2e77c")[0]
info = extract_crs_info(local_depth_crs)

check("source_type", "LocalDepth3DCrs", info.source_type)
check("projected_epsg_code", 23031, info.projected_epsg_code)
check("projected_uom", "M", info.projected_uom)
check("vertical_uom", "M", info.vertical_uom)
# ZIncreasingDownward=true in the raw file; the linked VerticalUnknownCrs
# carries no direction field, so the sentinel correctly preserves the value.
check("z_increasing_downward", True, info.z_increasing_downward)
check("x_offset", 0.0, info.x_offset, approx=True)
check("y_offset", 0.0, info.y_offset, approx=True)
check("z_offset", 0.0, info.z_offset, approx=True)

# ── LocalEngineeringCompoundCrs (inside v2.0.1 EPC) ───────────────────────
# This file mixes v2.0.1 and v2.3/v2.2 objects; the compound CRS is v2.3.

section("v2.0.1 EPC · LocalEngineeringCompoundCrs  (uuid 95330cec…)")

compound_crs_20 = epc20.get_object_by_uuid("95330cec-164c-4165-9fb9-c56477ae7f8a")[0]

# Without workspace: only inline z-axis info (no DOR resolution)
info_no_ws = extract_crs_info(compound_crs_20, workspace=None)
check("z_increasing_downward (inline VerticalAxis)", True, info_no_ws.z_increasing_downward)

# With workspace: DORs resolved → full CRS info
info = extract_crs_info(compound_crs_20, workspace=epc20)
check("projected_epsg_code (resolved via DOR)", 23031, info.projected_epsg_code)
check("projected_uom", "M", info.projected_uom)
check("vertical_uom", "M", info.vertical_uom)
check("z_increasing_downward", True, info.z_increasing_downward)
check("azimuth_reference", "grid north", info.azimuth_reference)

# ── LocalEngineering2DCrs (inside v2.0.1 EPC) ─────────────────────────────

section("v2.0.1 EPC · LocalEngineering2DCrs  (uuid 811f8e68…)")

eng2d_crs_20 = epc20.get_object_by_uuid("811f8e68-c0e4-5f90-b9cf-03f7e3d53ca4")[0]
info = extract_crs_info(eng2d_crs_20)

check("projected_epsg_code", 23031, info.projected_epsg_code)
check("projected_uom", "M", info.projected_uom)
check("vertical_uom", None, info.vertical_uom) #  (none — 2D CRS has no Z)
check("z_increasing_downward", False, info.z_increasing_downward)
check("azimuth_reference", "grid north", info.azimuth_reference)

# ── VerticalCrs (inside v2.0.1 EPC) ───────────────────────────────────────

section("v2.0.1 EPC · VerticalCrs  (uuid 1f6cf904…)")

vert_crs_20 = epc20.get_object_by_uuid("1f6cf904-336c-5202-a13d-7c9b142cd406")[0]
info = extract_crs_info(vert_crs_20)

check("vertical_uom", "M", info.vertical_uom)
check("z_increasing_downward", True, info.z_increasing_downward)
check("projected_epsg_code", None, info.projected_epsg_code)  # (vertical has none)
check("projected_uom", None, info.projected_uom)  # (vertical has none)

# ── Grid2DRepresentation → CRS  (v2.0.1 approach) ─────────────────────────

section("v2.0.1 · Grid2DRepresentation → CRS via geometry.local_crs DOR")

# Grid 030a82f6 → LocalTime3DCrs (dbd637d5)
grid_time = epc20.get_object_by_uuid("030a82f6-10a7-4ecf-af03-54749e098624")[0]
resolved_crs = _resolve_crs_from_grid(grid_time, epc20)
check("resolved CRS type", "LocalTime3DCrs", type(resolved_crs).__name__ if resolved_crs else None)
if resolved_crs:
    info = extract_crs_info(resolved_crs, workspace=epc20)
    check("  x_offset", 1.0, info.x_offset, approx=True)
    check("  y_offset", 0.1, info.y_offset, approx=True)
    check("  z_offset", 15.0, info.z_offset, approx=True)
    check("  projected_uom", "M", info.projected_uom)

# Grid aa5b90f1 → LocalDepth3DCrs (0ae56ef3)
grid_depth = epc20.get_object_by_uuid("aa5b90f1-2eab-4fa6-8720-69dd4fd51a4d")[0]
resolved_crs = _resolve_crs_from_grid(grid_depth, epc20)
check("resolved CRS type", "LocalDepth3DCrs", type(resolved_crs).__name__ if resolved_crs else None)
if resolved_crs:
    info = extract_crs_info(resolved_crs, workspace=epc20)
    check("  projected_epsg_code", 23031, info.projected_epsg_code)
    check("  projected_uom", "M", info.projected_uom)
    # Same LocalDepth3DCrs — ZIncreasingDownward=true in the raw file.
    check("  z_increasing_downward", True, info.z_increasing_downward)

# Grid 4e56b0e4 → also LocalDepth3DCrs (same uuid)
grid_depth2 = epc20.get_object_by_uuid("4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80")[0]
resolved_crs = _resolve_crs_from_grid(grid_depth2, epc20)
check("Grid 4e56b0e4 resolved CRS uuid", "0ae56ef3-fc79-405b-8deb-6942e0f2e77c",
      getattr(resolved_crs, "uuid", None))



# ===========================================================================
# RESQML v2.2 / EML v2.3  —  testingPackageCpp22.epc
# ===========================================================================

section("Loading testingPackageCpp22.epc  (RESQML v2.2 / EML v2.3)")
epc22 = Epc.read_file(EPC22_PATH)
print(f"  Loaded {len(epc22.energyml_objects)} objects.")

# ── LocalEngineering2DCrs  (no EPSG, has offsets) ─────────────────────────

section("v2.2 · LocalEngineering2DCrs  (uuid 997796f5…)  — offsets, no EPSG")

eng2d_no_epsg = epc22.get_object_by_uuid("997796f5-da9d-5175-9fb7-e592957b73fb")[0]
info = extract_crs_info(eng2d_no_epsg)

check("x_offset", 1.0, info.x_offset, approx=True)
check("y_offset", 0.1, info.y_offset, approx=True)
check("projected_uom", "M", info.projected_uom)
check("projected_epsg_code", None, info.projected_epsg_code)
check("azimuth_reference", "grid north", info.azimuth_reference)
check("z_increasing_downward", False, info.z_increasing_downward)

# ── LocalEngineering2DCrs  (with EPSG 23031) ──────────────────────────────

section("v2.2 · LocalEngineering2DCrs  (uuid 671ffdeb…)  — EPSG 23031")

eng2d_epsg = epc22.get_object_by_uuid("671ffdeb-f25c-513a-a4a2-1774d3ac20c6")[0]
info = extract_crs_info(eng2d_epsg)

check("projected_epsg_code", 23031, info.projected_epsg_code)
check("projected_uom", "M", info.projected_uom)
check("azimuth_reference", "grid north", info.azimuth_reference)
check("z_increasing_downward", False, info.z_increasing_downward)

# ── LocalEngineeringCompoundCrs  (no EPSG, has offsets + z) ──────────────

section("v2.2 · LocalEngineeringCompoundCrs  (uuid f0e9f421…)  — offsets + z offset")

compound_no_epsg = epc22.get_object_by_uuid("f0e9f421-b902-4392-87d8-6495c02f2fbe")[0]

# Without workspace: only inline VerticalAxis info available
info_no_ws = extract_crs_info(compound_no_epsg, workspace=None)
check("z_offset (inline origin_vertical_coordinate)", 15.0, info_no_ws.z_offset, approx=True)
check("z_increasing_downward (inline VerticalAxis)", True, info_no_ws.z_increasing_downward)
# This particular compound CRS mixes a time-domain vertical axis (uom='S')
# with a depth-domain resolved VerticalCrs (uom='M') — inline returns 'S'
check("vertical_uom (inline VerticalAxis — time domain)", "S", info_no_ws.vertical_uom)
check("x_offset without workspace", 0.0, info_no_ws.x_offset, approx=True)

# With workspace: DORs resolved → horizontal CRS merged in
info = extract_crs_info(compound_no_epsg, workspace=epc22)
check("x_offset (from resolved LocalEngineering2DCrs)", 1.0, info.x_offset, approx=True)
check("y_offset (from resolved LocalEngineering2DCrs)", 0.1, info.y_offset, approx=True)
check("z_offset (inline)", 15.0, info.z_offset, approx=True)
check("projected_uom (from 2D CRS)", "M", info.projected_uom)
check("projected_epsg_code (2D CRS has none)", None, info.projected_epsg_code)
check("vertical_uom", "M", info.vertical_uom)
check("z_increasing_downward", True, info.z_increasing_downward)
check("azimuth_reference", "grid north", info.azimuth_reference)

# ── LocalEngineeringCompoundCrs  (EPSG 23031) ─────────────────────────────

section("v2.2 · LocalEngineeringCompoundCrs  (uuid 6a18c177…)  — EPSG 23031")

compound_epsg = epc22.get_object_by_uuid("6a18c177-93be-41ac-9084-f84bbb31f46d")[0]
info = extract_crs_info(compound_epsg, workspace=epc22)

check("projected_epsg_code (resolved)", 23031, info.projected_epsg_code)
check("projected_uom", "M", info.projected_uom)
check("vertical_uom", "M", info.vertical_uom)
check("z_increasing_downward", True, info.z_increasing_downward)
check("x_offset", 0.0, info.x_offset, approx=True)
check("y_offset", 0.0, info.y_offset, approx=True)
check("z_offset", 0.0, info.z_offset, approx=True)
check("azimuth_reference", "grid north", info.azimuth_reference)

# ── VerticalCrs  (uuid 65cd199f) ──────────────────────────────────────────

section("v2.2 · VerticalCrs  (uuid 65cd199f…)")

vert_crs_22a = epc22.get_object_by_uuid("65cd199f-156b-5112-ad3e-b4f54a2aa77b")[0]
info = extract_crs_info(vert_crs_22a)

check("vertical_uom", "M", info.vertical_uom)
check("z_increasing_downward", True, info.z_increasing_downward)
check("projected_epsg_code (none for vertical)", None, info.projected_epsg_code)

# ── VerticalCrs  (uuid 355174db) ──────────────────────────────────────────

section("v2.2 · VerticalCrs  (uuid 355174db…)")

vert_crs_22b = epc22.get_object_by_uuid("355174db-6226-57ae-a5a6-92f33825fed4")[0]
info = extract_crs_info(vert_crs_22b)

check("vertical_uom", "M", info.vertical_uom)
check("z_increasing_downward", True, info.z_increasing_downward)

# ── Grid2D v2.2 — CRS note ────────────────────────────────────────────────
section("v2.2 · Grid2DRepresentation  — CRS resolution")
print("""
  In RESQML v2.2, Grid2DRepresentation DOES embed a LocalCrs DOR, but at
  a shallower path than v2.0.1:

    v2.2  : Geometry.LocalCrs  (PointGeometry sits directly on the object)
    v2.0.1: Grid2dPatch.Geometry.LocalCrs  (geometry is wrapped in a patch sub-object)

  Both paths are resolved by trying the shallower v2.2 path first with
  ``get_object_attribute_rgx``, then falling back to the deeper v2.0.1 path.
  No indirect lookup through framework associations is needed.

  All LocalEngineeringCompoundCrs objects in this EPC:
""")

for obj in epc22.energyml_objects:
    if "localengineeringcompoundcrs" in type(obj).__name__.lower():
        info = extract_crs_info(obj, workspace=epc22)
        print(f"  CompoundCrs {obj.uuid}")
        print(f"    projected_epsg={info.projected_epsg_code}  projected_uom={info.projected_uom}")
        print(f"    vertical_uom={info.vertical_uom}  z_down={info.z_increasing_downward}")
        print(f"    offsets: x={info.x_offset}  y={info.y_offset}  z={info.z_offset}")

# ── Grid2DRepresentation v2.2 → CRS via Geometry.LocalCrs ─────────────────

section("v2.2 · Grid2DRepresentation (uuid 4e56b0e4) → CRS via Geometry.LocalCrs")

grid22 = epc22.get_object_by_uuid("4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80")
if grid22:
    grid22 = grid22[0]
    resolved_crs22 = _resolve_crs_from_grid(grid22, epc22)
    check("resolved CRS type", "LocalEngineeringCompoundCrs",
          type(resolved_crs22).__name__ if resolved_crs22 else None)
    check("resolved CRS uuid", "6a18c177-93be-41ac-9084-f84bbb31f46d",
          getattr(resolved_crs22, "uuid", None))
    if resolved_crs22:
        info = extract_crs_info(resolved_crs22, workspace=epc22)
        check("  projected_epsg_code", 23031, info.projected_epsg_code)
        check("  projected_uom", "M", info.projected_uom)
        check("  vertical_uom", "M", info.vertical_uom)
        check("  z_increasing_downward", True, info.z_increasing_downward)
        check("  x_offset", 0.0, info.x_offset, approx=True)
        check("  y_offset", 0.0, info.y_offset, approx=True)
        check("  z_offset", 0.0, info.z_offset, approx=True)
else:
    print("  [SKIP] Grid 4e56b0e4 not found in testingPackageCpp22.epc")


# TriangulatedSetRepresentation 1a4112fa → LocalEngineeringCompoundCrs (6a18c177)
triangulated_set = epc22.get_object_by_uuid("1a4112fa-c4ef-4c8d-aed0-47d9273bebc5")[0]
resolved_crs_list = resolve_crs_from_triangulated_set(triangulated_set, epc22)
check("TriangulatedSetRepresentation resolved CRS uuid", 5,
      len(resolved_crs_list))

for i, resolved_crs in enumerate(resolved_crs_list):
    check(f"{i})  patch {i} resolved CRS type", "LocalEngineeringCompoundCrs",
          type(resolved_crs).__name__ if resolved_crs else None)
    if resolved_crs:
        info = extract_crs_info(resolved_crs, workspace=epc22)
        check("        projected_epsg_code (resolved)", 23031, info.projected_epsg_code)
        check("        projected_uom", "M", info.projected_uom)
        check("        vertical_uom", "M", info.vertical_uom)
        check("        z_increasing_downward", True, info.z_increasing_downward)
        check("        x_offset", 0.0, info.x_offset, approx=True)
        check("        y_offset", 0.0, info.y_offset, approx=True)
        check("        z_offset", 0.0, info.z_offset, approx=True)
        check("        azimuth_reference", "grid north", info.azimuth_reference)

# ===========================================================================
# Convenience helpers (delegates in helper.py)
# ===========================================================================

section("Legacy helper delegates still work correctly")

from energyml.utils.data.helper import (
    is_z_reversed,
    get_projected_epsg_code,
    get_projected_uom,
    get_vertical_epsg_code,
    get_crs_offsets_and_angle,
)

depth_crs = epc20.get_object_by_uuid("0ae56ef3-fc79-405b-8deb-6942e0f2e77c")[0]
# ZIncreasingDownward=true in the raw file → is_z_reversed returns True.
check("is_z_reversed(LocalDepth3DCrs)", True, is_z_reversed(depth_crs))
check("get_projected_epsg_code", 23031, get_projected_epsg_code(depth_crs))
check("get_projected_uom", "M", get_projected_uom(depth_crs))

time_crs = epc20.get_object_by_uuid("dbd637d5-4528-4145-908b-5f7136824f6d")[0]
x, y, z, (angle, uom) = get_crs_offsets_and_angle(time_crs)
check("get_crs_offsets_and_angle x", 1.0, x, approx=True)
check("get_crs_offsets_and_angle y", 0.1, y, approx=True)
check("get_crs_offsets_and_angle z", 15.0, z, approx=True)

# ===========================================================================
# Summary
# ===========================================================================

section("Summary")
total = _passed + _failed
print(f"  {_passed}/{total} checks passed.")
if _failed:
    print(f"  {_failed} checks FAILED — see [FAIL] lines above.")
    sys.exit(1)
else:
    print("  All checks passed!")
