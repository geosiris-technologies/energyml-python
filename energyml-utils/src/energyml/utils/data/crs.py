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

import numpy as np

from energyml.utils.storage_interface import EnergymlStorageInterface
from energyml.utils.introspection import (
    get_obj_uri,
    get_obj_uuid,
    get_object_attribute,
    get_object_attribute_no_verif,
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

        ``z_is_up=True`` tells ``apply_crs_transform`` to negate Z (converting
        from RESQML's depth-positive / z-down convention to the z-up convention
        used by most 3-D viewers).  This negation is required when the CRS stores
        depth as positive Z (``z_increasing_downward=True``).
        """
        return {
            "x_offset": self.x_offset,
            "y_offset": self.y_offset,
            "z_offset": self.z_offset,
            "areal_rotation": self.areal_rotation_value,
            "rotation_uom": self.areal_rotation_uom,
            "z_is_up": self.z_increasing_downward,
        }


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _resolve_dor(
    obj: Any,
    workspace: Optional[EnergymlStorageInterface],
) -> Any:
    """
    If *obj* looks like a ``DataObjectReference`` (DOR), resolve it to the
    actual object via *workspace* and return it.  Otherwise return *obj* as-is.

    Detection heuristic: the class name contains ``"reference"`` or ``"dor"``
    **and** the object has a ``uuid``/``uid`` attribute (i.e. it is a pointer,
    not a value type).
    """

    if obj is None or workspace is None:
        return obj
    type_lower = type(obj).__name__.lower()
    if "reference" not in type_lower and "dor" not in type_lower:
        return obj  # already a concrete object
    uri = get_obj_uri(obj)
    if uri:
        resolved = workspace.get_object(uri)
        if resolved is not None:
            return resolved
    return obj


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

    # UOM — may be an XML attribute on ProjectedCrs (v2.2 only; absent on v2.0.1 abstract subtypes)
    result["uom"] = _uom_to_str(getattr(projected_crs_obj, "uom", None))

    # Axis order (v2.2 only)
    axis_order_raw = getattr(projected_crs_obj, "axis_order", None)
    if axis_order_raw is not None:
        ao = str(axis_order_raw)
        if "." in ao:
            ao = ao.split(".")[-1]
        result["axis_order"] = ao.replace("_", " ").lower()

    # EPSG from direct attribute
    epsg = getattr(projected_crs_obj, "epsg_code", None)
    if epsg is not None:
        result["epsg_code"] = epsg
        return result

    # Navigate into AbstractProjectedCrs choice (v2.2 encapsulation pattern)
    abstract_crs = getattr(projected_crs_obj, "abstract_projected_crs", None)
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

    ``z_increasing_downward`` is ``None`` when the sub-object carries no
    explicit direction information (e.g. ``VerticalUnknownCrs``).  Callers
    **must not** override a parent-level ``ZIncreasingDownward`` when this
    value is ``None``.
    """
    logging.debug(
        f"Extracting vertical CRS details from object of type {type(vertical_crs_obj).__name__} with URI {get_obj_uri(vertical_crs_obj)}"
    )
    result: dict = {
        "epsg_code": None,
        "wkt": None,
        "unknown": None,
        "uom": None,
        "z_increasing_downward": None,  # None = not explicitly set by this sub-object
    }
    if vertical_crs_obj is None:
        return result

    # UOM (field exists on VerticalCrs v2.2; absent on v2.0.1 abstract subtypes)
    result["uom"] = _uom_to_str(getattr(vertical_crs_obj, "uom", None))

    # Direction (VerticalCrs v2.2 has a top-level direction field)
    direction = getattr(vertical_crs_obj, "direction", None)
    if direction is not None:
        d = str(direction)
        if "." in d:
            d = d.split(".")[-1]
        result["z_increasing_downward"] = d.lower() == "down"

    # EPSG from direct attribute
    epsg = getattr(vertical_crs_obj, "epsg_code", None)
    if epsg is not None:
        result["epsg_code"] = epsg
        return result

    # Navigate into AbstractVerticalCrs choice
    abstract_crs = getattr(vertical_crs_obj, "abstract_vertical_crs", None)
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


def _from_abstract_local3dcrs(
    crs_obj: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
) -> CrsInfo:
    """
    Handle ``AbstractLocal3dCrs`` and its concrete subclasses
    (``ObjLocalDepth3DCrs``, ``ObjLocalTime3DCrs``) — **RESQML v2.0.1**.

    Although the RESQML v2.0.1 schema embeds most data inline, the
    ``ProjectedCrs`` and ``VerticalCrs`` child elements can be
    ``DataObjectReference`` values.  *workspace* is used to resolve those
    DORs when provided.
    """
    type_name = type(crs_obj).__name__
    logging.debug(f"@_from_abstract_local3dcrs Extracting CRS info from {type_name} with URI {get_obj_uri(crs_obj)}")

    # --- Offsets -----------------------------------------------------------
    x_offset = 0.0
    y_offset = 0.0
    z_offset = 0.0
    try:
        _x = get_object_attribute_no_verif(crs_obj, "xoffset")
        _y = get_object_attribute_no_verif(crs_obj, "yoffset")
        _z = get_object_attribute_no_verif(crs_obj, "zoffset")
        x_offset = float(_x) if _x is not None else 0.0
        y_offset = float(_y) if _y is not None else 0.0
        z_offset = float(_z) if _z is not None else 0.0
    except (ValueError, TypeError, AttributeError) as exc:
        logger.debug("v2.0.1 offset read error: %s", exc)

    # --- Rotation ----------------------------------------------------------
    areal_rotation_value, areal_rotation_uom = _extract_rotation(crs_obj)

    # --- Z direction -------------------------------------------------------
    z_increasing_downward: bool = False
    zid_raw = get_object_attribute_no_verif(crs_obj, "zincreasing_downward")
    logging.debug(f"v2.0.1 ZIncreasingDownward raw value: {zid_raw}")
    if zid_raw is not None:
        if isinstance(zid_raw, bool):
            z_increasing_downward = zid_raw
        else:
            z_increasing_downward = str(zid_raw).lower() in ("true", "1", "yes")

    # --- Projected UOM -----------------------------------------------------
    projected_uom: Optional[str] = _uom_to_str(get_object_attribute_no_verif(crs_obj, "projected_uom"))

    # --- Vertical UOM (length or time) ------------------------------------
    vertical_uom: Optional[str] = _uom_to_str(get_object_attribute_no_verif(crs_obj, "vertical_uom"))
    if vertical_uom is None:
        # time_uom only present on LocalTime3dCrs
        vertical_uom = _uom_to_str(getattr(crs_obj, "time_uom", None))

    # --- Axis order --------------------------------------------------------
    axis_order_raw = get_object_attribute_no_verif(crs_obj, "projected_axis_order")
    projected_axis_order: Optional[str] = None
    if axis_order_raw is not None:
        ao = str(axis_order_raw)
        if "." in ao:
            ao = ao.split(".")[-1]
        projected_axis_order = ao.replace("_", " ").lower()

    # --- Projected CRS -----------------------------------------------------
    projected_crs_obj = _resolve_dor(get_object_attribute_no_verif(crs_obj, "projected_crs"), workspace)
    projected_details = _extract_projected_crs_details(projected_crs_obj)

    # Projected UOM from inline ProjectedCrs takes precedence if present
    if projected_details.get("uom"):
        projected_uom = projected_details["uom"]
    if projected_details.get("axis_order"):
        projected_axis_order = projected_details["axis_order"]

    # --- Vertical CRS ------------------------------------------------------
    vertical_crs_obj = _resolve_dor(get_object_attribute_no_verif(crs_obj, "vertical_crs"), workspace)
    vertical_details = _extract_vertical_crs_details(vertical_crs_obj)

    # Direction from VerticalCrs overrides the top-level ZIncreasingDownward
    # only when explicitly set.
    logging.debug("z_increasing_downward before vertical CRS details: %s", z_increasing_downward)
    logging.debug(
        f"Vertical CRS details: {vertical_details} -- vertical_crs_obj type: {type(vertical_crs_obj).__name__ if vertical_crs_obj else 'None'}"
    )
    if vertical_crs_obj is not None and vertical_details.get("z_increasing_downward") is not None:
        z_increasing_downward = vertical_details["z_increasing_downward"]
    if vertical_details.get("uom"):
        vertical_uom = vertical_details["uom"]

    logging.debug("z_increasing_downward after vertical CRS details: %s", z_increasing_downward)

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


def _from_local_engineering2d_crs(
    crs_obj: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
) -> CrsInfo:
    """
    Handle ``LocalEngineering2dCrs`` — **EML v2.3 / RESQML v2.2**.

    Contains: XY offsets, azimuth, ``ProjectedCrs`` DOR,
    ``HorizontalAxes.ProjectedUom``.
    Does **not** contain Z offset or vertical CRS — those live in the
    enclosing ``LocalEngineeringCompoundCrs``.

    *workspace* is used to resolve the ``origin_projected_crs`` DOR.
    """
    type_name = type(crs_obj).__name__

    # --- XY offsets --------------------------------------------------------
    x_offset = 0.0
    y_offset = 0.0
    try:
        _x = get_object_attribute_no_verif(crs_obj, "origin_projected_coordinate1")
        _y = get_object_attribute_no_verif(crs_obj, "origin_projected_coordinate2")
        x_offset = float(_x) if _x is not None else 0.0
        y_offset = float(_y) if _y is not None else 0.0
    except (ValueError, TypeError, AttributeError) as exc:
        logger.debug("LocalEngineering2dCrs offset read error: %s", exc)

    # --- Azimuth -----------------------------------------------------------
    areal_rotation_value, areal_rotation_uom = _extract_rotation(crs_obj)

    # --- Azimuth reference -------------------------------------------------
    azimuth_ref_raw = get_object_attribute_no_verif(crs_obj, "azimuth_reference")
    azimuth_reference: Optional[str] = None
    if azimuth_ref_raw is not None:
        ar = str(azimuth_ref_raw)
        if "." in ar:
            ar = ar.split(".")[-1]
        azimuth_reference = ar.replace("_", " ").lower()

    # --- Horizontal UOM (HorizontalAxes.projected_uom or uom on ProjectedCrs) ---
    projected_uom: Optional[str] = _uom_to_str(get_object_attribute(crs_obj, "horizontal_axes.projected_uom"))

    # --- ProjectedCrs — may be an inline object OR a DOR ------------------
    projected_crs_raw = get_object_attribute_no_verif(crs_obj, "origin_projected_crs")
    projected_crs_obj = _resolve_dor(projected_crs_raw, workspace)
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

    When the object carries no explicit direction (e.g. ``VerticalUnknownCrs``),
    ``z_increasing_downward`` defaults to ``False``; the caller is responsible
    for not blindly overriding a parent-level value in that case.
    """
    type_name = type(crs_obj).__name__
    details = _extract_vertical_crs_details(crs_obj)
    # Sentinel None means direction was not explicit — default to False for the standalone CrsInfo.
    z_idc: bool = details["z_increasing_downward"] if details["z_increasing_downward"] is not None else False
    return CrsInfo(
        vertical_epsg_code=details.get("epsg_code"),
        vertical_uom=details.get("uom"),
        z_increasing_downward=z_idc,
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
        _z = get_object_attribute_no_verif(crs_obj, "origin_vertical_coordinate")
        z_offset = float(_z) if _z is not None else 0.0
    except (ValueError, TypeError, AttributeError) as exc:
        logger.debug("LocalEngineeringCompoundCrs z-offset read error: %s", exc)

    # --- Vertical axis (inline — gives direction + uom without workspace) --
    vert_axis_direction: Optional[str] = None
    vert_axis_uom: Optional[str] = None
    vert_axis_uom_raw = get_object_attribute(crs_obj, "vertical_axis.uom")
    if vert_axis_uom_raw is not None:
        vert_axis_uom = _uom_to_str(vert_axis_uom_raw)
    vert_axis_dir_raw = get_object_attribute(crs_obj, "vertical_axis.direction")
    if vert_axis_dir_raw is not None:
        d = str(vert_axis_dir_raw)
        if "." in d:
            d = d.split(".")[-1]
        vert_axis_direction = d.lower()

    z_increasing_downward: bool = vert_axis_direction == "down" if vert_axis_direction else False

    # --- Resolve LocalEngineering2dCrs via DOR ----------------------------
    horiz_info: Optional[CrsInfo] = None
    horiz_dor = get_object_attribute_no_verif(crs_obj, "local_engineering2d_crs")
    if horiz_dor is not None and workspace is not None:
        horiz_uuid = get_obj_uuid(horiz_dor)
        if horiz_uuid:
            candidates = workspace.get_object_by_uuid(horiz_uuid)
            if candidates:
                horiz_info = _from_local_engineering2d_crs(candidates[0], workspace)
        if horiz_info is None:
            horiz_uri = get_obj_uri(horiz_dor)
            if horiz_uri:
                horiz_obj = workspace.get_object(horiz_uri)
                if horiz_obj is not None:
                    horiz_info = _from_local_engineering2d_crs(horiz_obj, workspace)
    elif horiz_dor is not None:
        logger.warning(
            "LocalEngineeringCompoundCrs: workspace is None — cannot resolve "
            "LocalEngineering2dCrs DOR; horizontal info (offsets, rotation) will be missing."
        )

    # --- Resolve VerticalCrs via DOR (inherited AbstractCompoundCrs.vertical_crs) ---
    vert_details_raw: Optional[dict] = None  # raw dict, preserving None sentinel
    vert_info: Optional[CrsInfo] = None
    vert_dor = get_object_attribute_no_verif(crs_obj, "vertical_crs")
    if vert_dor is not None and workspace is not None:
        vert_uuid = get_obj_uuid(vert_dor)
        if vert_uuid:
            candidates = workspace.get_object_by_uuid(vert_uuid)
            if candidates:
                vert_details_raw = _extract_vertical_crs_details(candidates[0])
                vert_info = _from_vertical_crs(candidates[0])
        if vert_info is None:
            vert_uri = get_obj_uri(vert_dor)
            if vert_uri:
                vert_obj = workspace.get_object(vert_uri)
                if vert_obj is not None:
                    vert_details_raw = _extract_vertical_crs_details(vert_obj)
                    vert_info = _from_vertical_crs(vert_obj)
    elif vert_dor is not None:
        logger.warning(
            "LocalEngineeringCompoundCrs: workspace is None — cannot resolve "
            "VerticalCrs DOR; vertical info (EPSG, UOM) will be missing."
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
        # Vertical info: prefer resolved VerticalCrs, but only override direction
        # when the resolved CRS carries an explicit direction (not the None sentinel).
        vertical_epsg_code=vert_info.vertical_epsg_code if vert_info else None,
        vertical_uom=(vert_info.vertical_uom if vert_info else None) or vert_axis_uom,
        z_increasing_downward=(
            vert_info.z_increasing_downward
            if vert_info and vert_details_raw is not None and vert_details_raw.get("z_increasing_downward") is not None
            else z_increasing_downward
        ),
        vertical_wkt=vert_info.vertical_wkt if vert_info else None,
        vertical_unknown=vert_info.vertical_unknown if vert_info else None,
        source_type=type_name,
    )


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------


_NORTHING_FIRST_PATTERNS = (
    "northing easting",
    "north east",
    "north easting",
    "northing east",
    "latitude longitude",
    "lat lon",
    "lat long",
)


def apply_axis_order_swap(
    points: np.ndarray,
    axis_order: Optional[str],
) -> np.ndarray:
    """
    Swap X and Y columns when the CRS axis order is northing-first.

    RESQML local offsets are always stored as (easting, northing),
    but some projected CRS definitions (e.g. EPSG:4326, EPSG:27700) use
    northing as the first axis.  When ``axis_order`` indicates a
    northing-first convention the columns 0 and 1 of *points* are swapped
    so that column 0 is always easting and column 1 is always northing.

    Parameters
    ----------
    points:
        (N, 3) float64 array, **modified in-place**.
    axis_order:
        Normalised axis-order string from :class:`CrsInfo` (lower-case,
        spaces instead of underscores), e.g. ``"northing easting"``.
        ``None`` means "no swap needed".

    Returns
    -------
    np.ndarray
        The same array (in-place swap).
    """
    if axis_order is None:
        return points
    ao_lower = axis_order.lower()
    if any(ao_lower.startswith(p) for p in _NORTHING_FIRST_PATTERNS):
        points[:, 0], points[:, 1] = points[:, 1].copy(), points[:, 0].copy()
    return points


def apply_from_crs_info(
    points: np.ndarray,
    crs_info: "CrsInfo",
    *,
    inplace: bool = True,
) -> np.ndarray:
    """
    Apply the full CRS transform described by *crs_info* to *points*.

    Transform pipeline (order matters):

    1. **Areal rotation** (RESQML convention: *clockwise* angle) →
       ``x' = x·cos θ + y·sin θ``, ``y' = –x·sin θ + y·cos θ``
    2. **Translation** — add ``(x_offset, y_offset, z_offset)``
    3. **Z-axis flip** — negate Z when the CRS *is*
       z-increasing-downward (i.e. the local CRS stores depth as positive Z,
       so we flip to z-up for a consistent elevation-positive system used by
       most 3-D viewers).
    4. **Axis-order swap** — swap X/Y when :attr:`CrsInfo.projected_axis_order`
       is northing-first.

    .. note::
        ``azimuth_reference`` values of ``"true north"`` or
        ``"magnetic north"`` require an external correction
        (meridian-convergence / magnetic-declination) that is not applied
        here.  A ``WARNING`` is emitted in those cases.

    Parameters
    ----------
    points:
        (N, 3) ``float64`` array of 3-D points in the local CRS.
    crs_info:
        Populated :class:`CrsInfo` DTO.
    inplace:
        When ``True`` (default) the rotation and translation are applied
        to *points* directly.  When ``False`` a copy is made first.

    Returns
    -------
    np.ndarray
        Transformed (N, 3) array.
    """
    if not inplace:
        points = points.copy()

    pts = points.astype(np.float64, copy=False)

    # --- 0. AzimuthReference warning ---------------------------------------
    ref = (crs_info.azimuth_reference or "").lower()
    if ref in ("true north", "magnetic north"):
        logger.warning(
            "apply_from_crs_info: azimuth_reference='%s' requires a meridian-"
            "convergence / magnetic-declination correction that is NOT applied. "
            "#TODO: implement once a correction source is available.",
            crs_info.azimuth_reference,
        )

    # --- 1. Areal rotation (RESQML: clockwise) ----------------------------
    angle_rad = crs_info.areal_rotation_rad()
    if angle_rad != 0.0:
        cos_t = math.cos(angle_rad)
        sin_t = math.sin(angle_rad)
        x_orig = pts[:, 0].copy()
        y_orig = pts[:, 1].copy()
        # CW rotation: x' = x·cos + y·sin,  y' = -x·sin + y·cos
        pts[:, 0] = x_orig * cos_t + y_orig * sin_t
        pts[:, 1] = -x_orig * sin_t + y_orig * cos_t

    # --- 2. Translation ---------------------------------------------------
    pts[:, 0] += crs_info.x_offset
    pts[:, 1] += crs_info.y_offset
    pts[:, 2] += crs_info.z_offset

    # --- 3. Z-axis flip ---------------------------------------------------
    # When z-increasing-downward the local CRS stores depth as positive Z
    # (down = positive). Negate so the output uses the z-up (elevation-
    # positive) convention expected by most 3-D viewers.
    if crs_info.z_increasing_downward:
        pts[:, 2] = -pts[:, 2]

    # --- 4. Axis-order swap -----------------------------------------------
    apply_axis_order_swap(pts, crs_info.projected_axis_order)

    if inplace:
        points[:] = pts
        return points
    return pts


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

    # Transparently resolve DataObjectReference inputs (e.g. from get_datum_information)
    # so callers do not have to resolve DORs before calling this function.
    if workspace is not None:
        crs_obj = _resolve_dor(crs_obj, workspace)
        if crs_obj is None:
            return CrsInfo()

    type_name_lower = type(crs_obj).__name__.lower()

    # ------------------------------------------------------------------
    # v2.2 / EML v2.3 types
    # ------------------------------------------------------------------
    if "localengineeringcompoundcrs" in type_name_lower:
        return _from_local_engineering_compound_crs(crs_obj, workspace)

    if "localengineering2dcrs" in type_name_lower or "localengineering2" in type_name_lower:
        return _from_local_engineering2d_crs(crs_obj, workspace)

    if type_name_lower == "verticalcrs":
        return _from_vertical_crs(crs_obj)

    # ------------------------------------------------------------------
    # v2.0.1 types  (LocalDepth3dCrs, LocalTime3dCrs, AbstractLocal3dCrs)
    # ------------------------------------------------------------------
    if any(kw in type_name_lower for kw in ("localdepth3dcrs", "localtime3dcrs", "abstractlocal3dcrs", "local3dcrs")):
        return _from_abstract_local3dcrs(crs_obj, workspace)

    # ------------------------------------------------------------------
    # Heuristic fallback: inspect the object's attributes to guess version
    # ------------------------------------------------------------------
    # v2.0.1 pattern: has XOffset / YOffset
    if get_object_attribute_rgx(crs_obj, "[Xx][Oo]ffset") is not None:
        logger.debug(
            "extract_crs_info: unrecognised type '%s' — treating as AbstractLocal3dCrs (v2.0.1 pattern).",
            type(crs_obj).__name__,
        )
        return _from_abstract_local3dcrs(crs_obj, workspace)

    # v2.2 pattern: has OriginProjectedCoordinate1 (LocalEngineering2dCrs)
    if get_object_attribute_rgx(crs_obj, "[Oo]rigin[Pp]rojected[Cc]oordinate1") is not None:
        logger.debug(
            "extract_crs_info: unrecognised type '%s' — treating as LocalEngineering2dCrs (v2.2 pattern).",
            type(crs_obj).__name__,
        )
        return _from_local_engineering2d_crs(crs_obj, workspace)

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


__all__ = [
    "CrsInfo",
    "extract_crs_info",
    "apply_from_crs_info",
    "apply_axis_order_swap",
]
