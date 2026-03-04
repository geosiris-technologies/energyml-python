# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
CRS (Coordinate Reference System) extraction module.

Provides a version-neutral ``CrsInfo`` DTO that captures all CRS metadata
relevant for 3D rendering (offsets, UOMs, EPSG codes, rotation / azimuth),
and a single ``extract_crs_info`` factory that handles both:

- **RESQML v2.0.1** — ``LocalDepth3dCrs`` / ``LocalTime3dCrs`` /
  ``AbstractLocal3dCrs``
- **RESQML v2.2 / EML v2.3** — ``LocalEngineeringCompoundCrs`` →
  ``LocalEngineering2dCrs`` + ``VerticalCrs``

Usage::

    from energyml.utils.data.crs import CrsInfo, extract_crs_info

    info: CrsInfo = extract_crs_info(my_crs_obj, workspace=epc)
    print(info.projected_epsg_code, info.x_offset, info.z_increasing_downward)
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Any, Optional

from energyml.utils.storage_interface import EnergymlStorageInterface
from energyml.utils.introspection import (
    get_obj_uri,
    get_obj_uuid,
    get_object_attribute,
    get_object_attribute_rgx,
    search_attribute_matching_name,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# DTO
# ---------------------------------------------------------------------------


@dataclass
class CrsInfo:
    """
    Version-neutral DTO holding all extractable CRS metadata.

    All fields are optional / defaulted so that a ``CrsInfo`` can be returned
    even when only partial information could be retrieved (e.g. when
    ``workspace`` is ``None`` for a v2.2 compound CRS).
    """

    # ------------------------------------------------------------------
    # Origin offsets  (local → project translation)
    # ------------------------------------------------------------------
    x_offset: float = 0.0
    """X translation of the local origin in the projected CRS units."""

    y_offset: float = 0.0
    """Y translation of the local origin in the projected CRS units."""

    z_offset: float = 0.0
    """Z translation of the local origin in the vertical CRS units."""

    # ------------------------------------------------------------------
    # Horizontal / projected CRS
    # ------------------------------------------------------------------
    projected_epsg_code: Optional[int] = None
    """EPSG code of the projected horizontal CRS, if any."""

    projected_uom: Optional[str] = None
    """Unit of measure for XY coordinates (e.g. ``"m"``, ``"ft"``)."""

    projected_axis_order: Optional[str] = None
    """Axis order of the projected CRS (e.g. ``"easting northing"``)."""

    projected_wkt: Optional[str] = None
    """Well-Known Text representation of the projected CRS, if provided."""

    projected_unknown: Optional[str] = None
    """Free-text CRS descriptor when no authority code / WKT is available."""

    # ------------------------------------------------------------------
    # Vertical CRS
    # ------------------------------------------------------------------
    vertical_epsg_code: Optional[int] = None
    """EPSG code of the vertical CRS, if any."""

    vertical_uom: Optional[str] = None
    """Unit of measure for Z coordinates (e.g. ``"m"``, ``"ft"``, ``"s"``)."""

    z_increasing_downward: bool = False
    """
    ``True`` when the Z axis increases *downward* (i.e. depth convention).
    ``False`` means Z increases *upward* (elevation convention).
    """

    vertical_wkt: Optional[str] = None
    """Well-Known Text representation of the vertical CRS, if provided."""

    vertical_unknown: Optional[str] = None
    """Free-text vertical CRS descriptor."""

    # ------------------------------------------------------------------
    # Rotation / azimuth
    # ------------------------------------------------------------------
    areal_rotation_value: float = 0.0
    """
    Rotation angle of the local grid relative to the projected CRS.
    Corresponds to ``ArealRotation`` (v2.0.1) or ``Azimuth`` (v2.2).
    """

    areal_rotation_uom: str = "rad"
    """Unit of the rotation angle: ``"rad"`` or ``"degr"``."""

    azimuth_reference: Optional[str] = None
    """
    (v2.2 only) Reference for the azimuth, e.g. ``"true north"``,
    ``"grid north"``, ``"magnetic north"`` (from ``NorthReferenceKind``).
    """

    # ------------------------------------------------------------------
    # Traceability
    # ------------------------------------------------------------------
    source_type: Optional[str] = None
    """
    Simple type name of the energyml object this info was extracted from.
    Useful for debugging and logging.
    """

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def areal_rotation_rad(self) -> float:
        """Return ``areal_rotation_value`` converted to **radians**."""
        if self.areal_rotation_uom == "degr":
            return math.radians(self.areal_rotation_value)
        return self.areal_rotation_value

    def as_transform_args(self) -> dict:
        """
        Return a kwargs dict ready to be unpacked into
        :func:`energyml.utils.data.helper.apply_crs_transform`.
        """
        return {
            "x_offset": self.x_offset,
            "y_offset": self.y_offset,
            "z_offset": self.z_offset,
            "areal_rotation": self.areal_rotation_value,
            "rotation_uom": self.areal_rotation_uom,
            "z_is_up": not self.z_increasing_downward,
        }


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _uom_to_str(uom: Any) -> Optional[str]:
    """
    Normalise a ``LengthUom`` / ``TimeUom`` enum value (or plain string) to a
    plain lowercase string like ``"m"``, ``"ft"``, ``"s"``.

    Handles patterns like:
    - ``LengthUom.M`` → ``"m"``
    - ``"LengthUom.ft"`` → ``"ft"``
    - ``"m"`` → ``"m"``
    """
    if uom is None:
        return None
    s = str(uom)
    if "." in s:
        s = s.split(".")[-1]
    return s.strip() or None


def _extract_abstract_projected_crs(abstract_projected_crs: Any) -> dict:
    """
    Extract details from an ``AbstractProjectedCrs`` concrete instance.

    Returns a dict with keys: ``epsg_code``, ``wkt``, ``unknown``.
    """
    result: dict = {"epsg_code": None, "wkt": None, "unknown": None}
    if abstract_projected_crs is None:
        return result

    type_name = type(abstract_projected_crs).__name__.lower()

    if "epsg" in type_name:
        result["epsg_code"] = getattr(abstract_projected_crs, "epsg_code", None)
    elif "wkt" in type_name:
        result["wkt"] = getattr(abstract_projected_crs, "well_known_text", None)
    elif "unknown" in type_name:
        result["unknown"] = getattr(abstract_projected_crs, "unknown", None)

    # Fallback: generic attribute search
    if result["epsg_code"] is None:
        result["epsg_code"] = get_object_attribute_rgx(abstract_projected_crs, "[Ee]psg[_]?[Cc]ode")

    return result


def _extract_projected_crs_details(projected_crs_obj: Any) -> dict:
    """
    Extract details from a ``ProjectedCrs`` (v2.2 EML) or from an
    ``AbstractProjectedCrs`` inline object (v2.0.1).

    Returns a dict with keys: ``epsg_code``, ``wkt``, ``unknown``, ``uom``,
    ``axis_order``.
    """
    result: dict = {
        "epsg_code": None,
        "wkt": None,
        "unknown": None,
        "uom": None,
        "axis_order": None,
    }
    if projected_crs_obj is None:
        return result

    # UOM — may be an XML attribute on ProjectedCrs
    result["uom"] = _uom_to_str(get_object_attribute_rgx(projected_crs_obj, "[Uu]om"))

    # Axis order
    axis_order_raw = get_object_attribute_rgx(projected_crs_obj, "[Aa]xis[_]?[Oo]rder")
    if axis_order_raw is not None:
        ao = str(axis_order_raw)
        if "." in ao:
            ao = ao.split(".")[-1]
        result["axis_order"] = ao.replace("_", " ").lower()

    # EPSG from direct attribute (e.g. v2.2 ProjectedEpsgCrs inside ProjectedCrs)
    epsg = get_object_attribute_rgx(projected_crs_obj, "[Ee]psg[_]?[Cc]ode")
    if epsg is not None:
        result["epsg_code"] = epsg
        return result

    # Navigate into AbstractProjectedCrs choice (v2.2 encapsulation pattern)
    abstract_crs = get_object_attribute_rgx(projected_crs_obj, "[Aa]bstract[_]?[Pp]rojected[_]?[Cc]rs")
    if abstract_crs is not None:
        details = _extract_abstract_projected_crs(abstract_crs)
        result.update({k: v for k, v in details.items() if v is not None})

    return result


def _extract_abstract_vertical_crs(abstract_vertical_crs: Any) -> dict:
    """
    Extract details from an ``AbstractVerticalCrs`` concrete instance.

    Returns a dict with keys: ``epsg_code``, ``wkt``, ``unknown``.
    """
    result: dict = {"epsg_code": None, "wkt": None, "unknown": None}
    if abstract_vertical_crs is None:
        return result

    type_name = type(abstract_vertical_crs).__name__.lower()

    if "epsg" in type_name:
        result["epsg_code"] = getattr(abstract_vertical_crs, "epsg_code", None)
    elif "wkt" in type_name:
        result["wkt"] = getattr(abstract_vertical_crs, "well_known_text", None)
    elif "unknown" in type_name:
        result["unknown"] = getattr(abstract_vertical_crs, "unknown", None)

    if result["epsg_code"] is None:
        result["epsg_code"] = get_object_attribute_rgx(abstract_vertical_crs, "[Ee]psg[_]?[Cc]ode")

    return result


def _extract_vertical_crs_details(vertical_crs_obj: Any) -> dict:
    """
    Extract details from a ``VerticalCrs`` (v2.2 EML) or from an
    ``AbstractVerticalCrs`` inline object (v2.0.1).

    Returns a dict with keys: ``epsg_code``, ``wkt``, ``unknown``, ``uom``,
    ``z_increasing_downward``.
    """
    result: dict = {
        "epsg_code": None,
        "wkt": None,
        "unknown": None,
        "uom": None,
        "z_increasing_downward": False,
    }
    if vertical_crs_obj is None:
        return result

    # UOM
    result["uom"] = _uom_to_str(get_object_attribute_rgx(vertical_crs_obj, "[Uu]om"))

    # Direction (VerticalCrs in v2.2 has a top-level Direction field)
    direction = get_object_attribute_rgx(vertical_crs_obj, "[Dd]irection")
    if direction is not None:
        d = str(direction)
        if "." in d:
            d = d.split(".")[-1]
        result["z_increasing_downward"] = d.lower() == "down"

    # EPSG from direct attribute
    epsg = get_object_attribute_rgx(vertical_crs_obj, "[Ee]psg[_]?[Cc]ode")
    if epsg is not None:
        result["epsg_code"] = epsg
        return result

    # Navigate into AbstractVerticalCrs choice
    abstract_crs = get_object_attribute_rgx(vertical_crs_obj, "[Aa]bstract[_]?[Vv]ertical[_]?[Cc]rs")
    if abstract_crs is not None:
        details = _extract_abstract_vertical_crs(abstract_crs)
        result.update({k: v for k, v in details.items() if v is not None})

    return result


def _extract_rotation(crs_obj: Any) -> tuple[float, str]:
    """
    Extract the areal rotation / azimuth (value, uom) from *any* CRS object.

    Handles both v2.0.1 ``ArealRotation.value/uom`` and v2.2
    ``Azimuth.value/uom`` styles.

    Returns ``(0.0, "rad")`` if no rotation field is found.
    """
    # v2.2 style  (azimuth.value / azimuth.uom)
    azimuth_value = get_object_attribute_rgx(crs_obj, "[Aa]zimuth.value")
    if azimuth_value is not None:
        azimuth_uom = _uom_to_str(get_object_attribute_rgx(crs_obj, "[Aa]zimuth.uom")) or "rad"
        try:
            return float(azimuth_value), azimuth_uom
        except (ValueError, TypeError):
            pass

    # v2.0.1 style  (areal_rotation.value / areal_rotation.uom)
    rotation_value = get_object_attribute_rgx(crs_obj, "[Aa]real[_]?[Rr]otation.value")
    if rotation_value is not None:
        rotation_uom = _uom_to_str(get_object_attribute_rgx(crs_obj, "[Aa]real[_]?[Rr]otation.uom")) or "rad"
        try:
            return float(rotation_value), rotation_uom
        except (ValueError, TypeError):
            pass

    return 0.0, "rad"


# ---------------------------------------------------------------------------
# Branch extractors (one per top-level CRS type)
# ---------------------------------------------------------------------------


def _from_abstract_local3dcrs(crs_obj: Any) -> CrsInfo:
    """
    Handle ``AbstractLocal3dCrs`` and its concrete subclasses
    (``ObjLocalDepth3DCrs``, ``ObjLocalTime3DCrs``) — **RESQML v2.0.1**.

    All data is inline; no workspace lookup needed.
    """
    type_name = type(crs_obj).__name__

    # --- Offsets -----------------------------------------------------------
    x_offset = 0.0
    y_offset = 0.0
    z_offset = 0.0
    try:
        _x = get_object_attribute_rgx(crs_obj, "[Xx][Oo]ffset")
        _y = get_object_attribute_rgx(crs_obj, "[Yy][Oo]ffset")
        _z = get_object_attribute_rgx(crs_obj, "[Zz][Oo]ffset")
        x_offset = float(_x) if _x is not None else 0.0
        y_offset = float(_y) if _y is not None else 0.0
        z_offset = float(_z) if _z is not None else 0.0
    except (ValueError, TypeError) as exc:
        logger.debug("v2.0.1 offset read error: %s", exc)

    # --- Rotation ----------------------------------------------------------
    areal_rotation_value, areal_rotation_uom = _extract_rotation(crs_obj)

    # --- Z direction -------------------------------------------------------
    z_increasing_downward: bool = False
    zid_raw = get_object_attribute_rgx(crs_obj, "[Zz]increasing[_]?[Dd]ownward")
    if zid_raw is not None:
        if isinstance(zid_raw, bool):
            z_increasing_downward = zid_raw
        else:
            z_increasing_downward = str(zid_raw).lower() in ("true", "1", "yes")

    # --- Projected UOM -----------------------------------------------------
    projected_uom: Optional[str] = _uom_to_str(
        get_object_attribute_rgx(crs_obj, "[Pp]rojected[Uu]om")
    )

    # --- Vertical UOM (length or time) ------------------------------------
    vertical_uom: Optional[str] = _uom_to_str(
        get_object_attribute_rgx(crs_obj, "[Vv]ertical[Uu]om")
    )
    if vertical_uom is None:
        vertical_uom = _uom_to_str(
            get_object_attribute_rgx(crs_obj, "[Tt]ime[Uu]om")
        )

    # --- Axis order --------------------------------------------------------
    axis_order_raw = get_object_attribute_rgx(crs_obj, "[Pp]rojected[Aa]xis[Oo]rder")
    projected_axis_order: Optional[str] = None
    if axis_order_raw is not None:
        ao = str(axis_order_raw)
        if "." in ao:
            ao = ao.split(".")[-1]
        projected_axis_order = ao.replace("_", " ").lower()

    # --- Projected CRS -----------------------------------------------------
    projected_crs_obj = get_object_attribute_rgx(crs_obj, "[Pp]rojected[Cc]rs")
    projected_details = _extract_projected_crs_details(projected_crs_obj)

    # Projected UOM from inline ProjectedCrs takes precedence if present
    if projected_details.get("uom"):
        projected_uom = projected_details["uom"]
    if projected_details.get("axis_order"):
        projected_axis_order = projected_details["axis_order"]

    # --- Vertical CRS ------------------------------------------------------
    vertical_crs_obj = get_object_attribute_rgx(crs_obj, "[Vv]ertical[Cc]rs")
    vertical_details = _extract_vertical_crs_details(vertical_crs_obj)

    # Direction from VerticalCrs overrides the top-level ZIncreasingDownward
    # only when explicitly set.
    if vertical_crs_obj is not None and vertical_details.get("z_increasing_downward") is not None:
        z_increasing_downward = vertical_details["z_increasing_downward"]
    if vertical_details.get("uom"):
        vertical_uom = vertical_details["uom"]

    return CrsInfo(
        x_offset=x_offset,
        y_offset=y_offset,
        z_offset=z_offset,
        projected_epsg_code=projected_details.get("epsg_code"),
        projected_uom=projected_uom,
        projected_axis_order=projected_axis_order,
        projected_wkt=projected_details.get("wkt"),
        projected_unknown=projected_details.get("unknown"),
        vertical_epsg_code=vertical_details.get("epsg_code"),
        vertical_uom=vertical_uom,
        z_increasing_downward=z_increasing_downward,
        vertical_wkt=vertical_details.get("wkt"),
        vertical_unknown=vertical_details.get("unknown"),
        areal_rotation_value=areal_rotation_value,
        areal_rotation_uom=areal_rotation_uom,
        source_type=type_name,
    )


def _from_local_engineering2d_crs(crs_obj: Any) -> CrsInfo:
    """
    Handle ``LocalEngineering2dCrs`` — **EML v2.3 / RESQML v2.2**.

    Contains: XY offsets, azimuth, inline ``ProjectedCrs``,
    ``HorizontalAxes.ProjectedUom``.
    Does **not** contain Z offset or vertical CRS — those live in the
    enclosing ``LocalEngineeringCompoundCrs``.
    """
    type_name = type(crs_obj).__name__

    # --- XY offsets --------------------------------------------------------
    x_offset = 0.0
    y_offset = 0.0
    try:
        _x = get_object_attribute_rgx(crs_obj, "[Oo]rigin[Pp]rojected[Cc]oordinate1")
        _y = get_object_attribute_rgx(crs_obj, "[Oo]rigin[Pp]rojected[Cc]oordinate2")
        x_offset = float(_x) if _x is not None else 0.0
        y_offset = float(_y) if _y is not None else 0.0
    except (ValueError, TypeError) as exc:
        logger.debug("LocalEngineering2dCrs offset read error: %s", exc)

    # --- Azimuth -----------------------------------------------------------
    areal_rotation_value, areal_rotation_uom = _extract_rotation(crs_obj)

    # --- Azimuth reference -------------------------------------------------
    azimuth_ref_raw = get_object_attribute_rgx(crs_obj, "[Aa]zimuth[Rr]eference")
    azimuth_reference: Optional[str] = None
    if azimuth_ref_raw is not None:
        ar = str(azimuth_ref_raw)
        if "." in ar:
            ar = ar.split(".")[-1]
        azimuth_reference = ar.replace("_", " ").lower()

    # --- Horizontal UOM (HorizontalAxes.ProjectedUom or uom on ProjectedCrs) ---
    projected_uom: Optional[str] = _uom_to_str(
        get_object_attribute_rgx(crs_obj, "[Hh]orizontal[_]?[Aa]xes.[Pp]rojected[_]?[Uu]om")
    )

    # --- Inline ProjectedCrs -----------------------------------------------
    projected_crs_obj = get_object_attribute_rgx(crs_obj, "[Oo]rigin[Pp]rojected[Cc]rs")
    projected_details = _extract_projected_crs_details(projected_crs_obj)

    if projected_details.get("uom") and projected_uom is None:
        projected_uom = projected_details["uom"]

    return CrsInfo(
        x_offset=x_offset,
        y_offset=y_offset,
        z_offset=0.0,  # Z lives in the compound CRS
        projected_epsg_code=projected_details.get("epsg_code"),
        projected_uom=projected_uom,
        projected_axis_order=projected_details.get("axis_order"),
        projected_wkt=projected_details.get("wkt"),
        projected_unknown=projected_details.get("unknown"),
        areal_rotation_value=areal_rotation_value,
        areal_rotation_uom=areal_rotation_uom,
        azimuth_reference=azimuth_reference,
        source_type=type_name,
    )


def _from_vertical_crs(crs_obj: Any) -> CrsInfo:
    """
    Handle a standalone ``VerticalCrs`` document object — **EML v2.3 / RESQML v2.2**.
    """
    type_name = type(crs_obj).__name__
    details = _extract_vertical_crs_details(crs_obj)
    return CrsInfo(
        vertical_epsg_code=details.get("epsg_code"),
        vertical_uom=details.get("uom"),
        z_increasing_downward=details.get("z_increasing_downward", False),
        vertical_wkt=details.get("wkt"),
        vertical_unknown=details.get("unknown"),
        source_type=type_name,
    )


def _from_local_engineering_compound_crs(
    crs_obj: Any,
    workspace: Optional[EnergymlStorageInterface],
) -> CrsInfo:
    """
    Handle ``LocalEngineeringCompoundCrs`` — **EML v2.3 / RESQML v2.2**.

    Resolves:
    - ``local_engineering2d_crs`` → DOR → ``LocalEngineering2dCrs``
    - ``vertical_crs`` → DOR (inherited from ``AbstractCompoundCrs``)  → ``VerticalCrs``

    When ``workspace`` is ``None``, only inline data (z offset, vertical axis
    from the compound itself) can be populated.
    """
    type_name = type(crs_obj).__name__

    # --- Z offset (origin_vertical_coordinate) --------------------------------
    z_offset = 0.0
    try:
        _z = get_object_attribute_rgx(crs_obj, "[Oo]rigin[Vv]ertical[Cc]oordinate")
        z_offset = float(_z) if _z is not None else 0.0
    except (ValueError, TypeError) as exc:
        logger.debug("LocalEngineeringCompoundCrs z-offset read error: %s", exc)

    # --- Vertical axis (inline — gives direction + uom without workspace) --
    vert_axis_direction: Optional[str] = None
    vert_axis_uom: Optional[str] = None
    vert_axis_uom_raw = get_object_attribute_rgx(crs_obj, "[Vv]ertical[_]?[Aa]xis.[Uu]om")
    if vert_axis_uom_raw is not None:
        vert_axis_uom = _uom_to_str(vert_axis_uom_raw)
    vert_axis_dir_raw = get_object_attribute_rgx(crs_obj, "[Vv]ertical[_]?[Aa]xis.[Dd]irection")
    if vert_axis_dir_raw is not None:
        d = str(vert_axis_dir_raw)
        if "." in d:
            d = d.split(".")[-1]
        vert_axis_direction = d.lower()

    z_increasing_downward: bool = vert_axis_direction == "down" if vert_axis_direction else False

    # --- Resolve LocalEngineering2dCrs via DOR ----------------------------
    horiz_info: Optional[CrsInfo] = None
    horiz_dor = get_object_attribute_rgx(crs_obj, "[Ll]ocal[Ee]ngineering2[dD][Cc]rs")
    if horiz_dor is not None and workspace is not None:
        horiz_uuid = get_obj_uuid(horiz_dor)
        if horiz_uuid:
            candidates = workspace.get_object_by_uuid(horiz_uuid)
            if candidates:
                horiz_info = _from_local_engineering2d_crs(candidates[0])
        if horiz_info is None:
            horiz_uri = get_obj_uri(horiz_dor)
            if horiz_uri:
                horiz_obj = workspace.get_object(horiz_uri)
                if horiz_obj is not None:
                    horiz_info = _from_local_engineering2d_crs(horiz_obj)
    elif horiz_dor is not None:
        logger.debug(
            "LocalEngineeringCompoundCrs: workspace is None — cannot resolve "
            "LocalEngineering2dCrs DOR; horizontal info will be partial."
        )

    # --- Resolve VerticalCrs via DOR (inherited AbstractCompoundCrs.vertical_crs) ---
    vert_info: Optional[CrsInfo] = None
    vert_dor = get_object_attribute_rgx(crs_obj, "[Vv]ertical[Cc]rs")
    if vert_dor is not None and workspace is not None:
        vert_uuid = get_obj_uuid(vert_dor)
        if vert_uuid:
            candidates = workspace.get_object_by_uuid(vert_uuid)
            if candidates:
                vert_info = _from_vertical_crs(candidates[0])
        if vert_info is None:
            vert_uri = get_obj_uri(vert_dor)
            if vert_uri:
                vert_obj = workspace.get_object(vert_uri)
                if vert_obj is not None:
                    vert_info = _from_vertical_crs(vert_obj)
    elif vert_dor is not None:
        logger.debug(
            "LocalEngineeringCompoundCrs: workspace is None — cannot resolve "
            "VerticalCrs DOR; vertical info will be partial."
        )

    # --- Merge results -----------------------------------------------------
    return CrsInfo(
        # XY offsets and rotation come from the 2D CRS
        x_offset=horiz_info.x_offset if horiz_info else 0.0,
        y_offset=horiz_info.y_offset if horiz_info else 0.0,
        z_offset=z_offset,
        projected_epsg_code=horiz_info.projected_epsg_code if horiz_info else None,
        projected_uom=horiz_info.projected_uom if horiz_info else None,
        projected_axis_order=horiz_info.projected_axis_order if horiz_info else None,
        projected_wkt=horiz_info.projected_wkt if horiz_info else None,
        projected_unknown=horiz_info.projected_unknown if horiz_info else None,
        areal_rotation_value=horiz_info.areal_rotation_value if horiz_info else 0.0,
        areal_rotation_uom=horiz_info.areal_rotation_uom if horiz_info else "rad",
        azimuth_reference=horiz_info.azimuth_reference if horiz_info else None,
        # Vertical info: prefer resolved VerticalCrs object, else inline VerticalAxis
        vertical_epsg_code=vert_info.vertical_epsg_code if vert_info else None,
        vertical_uom=(vert_info.vertical_uom if vert_info else None) or vert_axis_uom,
        z_increasing_downward=(
            vert_info.z_increasing_downward if vert_info else z_increasing_downward
        ),
        vertical_wkt=vert_info.vertical_wkt if vert_info else None,
        vertical_unknown=vert_info.vertical_unknown if vert_info else None,
        source_type=type_name,
    )


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------


def extract_crs_info(
    crs_obj: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
) -> CrsInfo:
    """
    Extract all available CRS metadata from *any* energyml CRS object into a
    version-neutral :class:`CrsInfo` DTO.

    Supported types (matched case-insensitively on the class name):

    **RESQML v2.0.1**

    - ``ObjLocalDepth3DCrs`` / ``LocalDepth3dCrs``
    - ``ObjLocalTime3DCrs`` / ``LocalTime3dCrs``
    - Any subclass of ``AbstractLocal3dCrs``

    **EML v2.3 / RESQML v2.2**

    - ``LocalEngineeringCompoundCrs``
    - ``LocalEngineering2dCrs`` (also handled standalone)
    - ``VerticalCrs`` (also handled standalone)

    Parameters
    ----------
    crs_obj:
        An energyml CRS data object. May be ``None`` — in that case a default
        ``CrsInfo()`` is returned (all zeros / None).
    workspace:
        Optional storage interface used to resolve
        ``DataObjectReference`` links in v2.2 compound CRS objects.
        When ``None``, only inline data is extracted (partial result).

    Returns
    -------
    CrsInfo
        Populated DTO.  Never raises — errors are logged at DEBUG / WARNING
        level and graceful defaults are returned.
    """
    if crs_obj is None:
        return CrsInfo()

    type_name_lower = type(crs_obj).__name__.lower()

    # ------------------------------------------------------------------
    # v2.2 / EML v2.3 types
    # ------------------------------------------------------------------
    if "localengineeringcompoundcrs" in type_name_lower:
        return _from_local_engineering_compound_crs(crs_obj, workspace)

    if "localengineering2dcrs" in type_name_lower or "localengineering2" in type_name_lower:
        return _from_local_engineering2d_crs(crs_obj)

    if type_name_lower == "verticalcrs":
        return _from_vertical_crs(crs_obj)

    # ------------------------------------------------------------------
    # v2.0.1 types  (LocalDepth3dCrs, LocalTime3dCrs, AbstractLocal3dCrs)
    # ------------------------------------------------------------------
    if any(
        kw in type_name_lower
        for kw in ("localdepth3dcrs", "localtime3dcrs", "abstractlocal3dcrs", "local3dcrs")
    ):
        return _from_abstract_local3dcrs(crs_obj)

    # ------------------------------------------------------------------
    # Heuristic fallback: inspect the object's attributes to guess version
    # ------------------------------------------------------------------
    # v2.0.1 pattern: has XOffset / YOffset
    if get_object_attribute_rgx(crs_obj, "[Xx][Oo]ffset") is not None:
        logger.debug(
            "extract_crs_info: unrecognised type '%s' — treating as AbstractLocal3dCrs (v2.0.1 pattern).",
            type(crs_obj).__name__,
        )
        return _from_abstract_local3dcrs(crs_obj)

    # v2.2 pattern: has OriginProjectedCoordinate1 (LocalEngineering2dCrs)
    if get_object_attribute_rgx(crs_obj, "[Oo]rigin[Pp]rojected[Cc]oordinate1") is not None:
        logger.debug(
            "extract_crs_info: unrecognised type '%s' — treating as LocalEngineering2dCrs (v2.2 pattern).",
            type(crs_obj).__name__,
        )
        return _from_local_engineering2d_crs(crs_obj)

    # v2.2 pattern: has LocalEngineering2dCrs DOR → compound
    if get_object_attribute_rgx(crs_obj, "[Ll]ocal[Ee]ngineering2[dD][Cc]rs") is not None:
        logger.debug(
            "extract_crs_info: unrecognised type '%s' — treating as LocalEngineeringCompoundCrs (v2.2 pattern).",
            type(crs_obj).__name__,
        )
        return _from_local_engineering_compound_crs(crs_obj, workspace)

    logger.warning(
        "extract_crs_info: unsupported CRS type '%s' — returning default CrsInfo.",
        type(crs_obj).__name__,
    )
    return CrsInfo(source_type=type(crs_obj).__name__)
