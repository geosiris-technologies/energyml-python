# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""GeoJSON export (RFC 7946), dict-building and streaming writers."""

from __future__ import annotations

import json
import logging
from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TextIO, Tuple, Union

import numpy as np

from energyml.utils.data.export._base import (
    ExportFormat,
    resolve_origin_shift,
    GeoJSONExportOptions,
    _get_context_color,
    _get_export_points,
    _get_faces_or_cells,
    _normalize_to_patches,
    _parse_vtk_flat_faces,
    _parse_vtk_flat_lines,
    _workspace_from_contexts,
)

from energyml.utils.data.export._registry import FormatSpec, register_format

if TYPE_CHECKING:
    from energyml.utils.data.crs import PointFrame
    from energyml.utils.data.mesh import AbstractMesh
    from energyml.utils.storage_interface import EnergymlStorageInterface
    from energyml.utils.data.representation_context import RepresentationContext

logger = logging.getLogger(__name__)
#: Alias of the module logger, for the functions that take a caller-supplied ``logger``
#: parameter — the parameter shadows the module-level name inside their body.
_MODULE_LOGGER = logger

# ---------------------------------------------------------------------------
# GeoJSON export
# ---------------------------------------------------------------------------


def _geojson_crs_members(
    projected_epsg_code: Optional[int],
    vertical_epsg_code: Optional[int],
) -> dict:
    """
    Build the members advertising a **non-WGS84** CRS in a GeoJSON document.

    RFC 7946 mandates WGS84 (CRS84) and removed the ``crs`` member, so when the coordinates
    are left in their projected CRS the document is, strictly speaking, non conformant.
    Two complementary standard-ish identifiers are then written:

    - ``crs`` — the GeoJSON 2008 named-CRS member.  Deprecated, but it is what GDAL / OGR
      and QGIS actually read.
    - ``coordRefSys`` — the OGC JSON-FG member, given as OGC URI(s).  A list is used for a
      compound CRS (horizontal + vertical), as allowed by JSON-FG.

    Returns an empty dict when no EPSG code is available.
    """
    if projected_epsg_code is None:
        return {}

    from energyml.utils.data.crs import crs_ogc_uri, crs_urn

    members: dict = {
        "crs": {"type": "name", "properties": {"name": crs_urn(projected_epsg_code)}},
    }
    if vertical_epsg_code is not None:
        members["coordRefSys"] = [crs_ogc_uri(projected_epsg_code), crs_ogc_uri(vertical_epsg_code)]
    else:
        members["coordRefSys"] = crs_ogc_uri(projected_epsg_code)
    return members


def _feature_id(
    source_uuid: Optional[str],
    patch_index: Optional[int] = None,
    element_index: Optional[int] = None,
) -> Optional[str]:
    """
    Build the RFC 7946 ``id`` member of a feature (§3.2 : "If a Feature has a commonly used
    identifier, that identifier SHOULD be included").  The energyml uuid is used, suffixed by
    the patch / element indices when a single object yields several features.
    """
    if not source_uuid:
        return None
    parts = [source_uuid]
    if patch_index is not None:
        parts.append(str(patch_index))
    if element_index is not None:
        parts.append(str(element_index))
    return "_".join(parts)


def _geojson_bbox(all_points: List[np.ndarray]) -> Optional[List[float]]:
    """
    Compute the RFC 7946 §5 ``bbox`` of the whole collection :
    ``[min_x, min_y, min_z, max_x, max_y, max_z]``.
    """
    non_empty = [p for p in all_points if p is not None and len(p) > 0]
    if not non_empty:
        return None
    stacked = np.concatenate([np.asarray(p, dtype=np.float64).reshape(-1, 3) for p in non_empty], axis=0)
    mins = stacked.min(axis=0)
    maxs = stacked.max(axis=0)
    return [float(mins[0]), float(mins[1]), float(mins[2]), float(maxs[0]), float(maxs[1]), float(maxs[2])]


def _resolve_crs(
    mesh: Any,
    workspace: Any = None,
    projected_epsg_code: Optional[int] = None,
    vertical_epsg_code: Optional[int] = None,
) -> Tuple[Any, Optional[int], Optional[int]]:
    """Return ``(crs_info, projected_epsg_code, vertical_epsg_code)`` for *mesh*.

    The single place where a mesh's CRS is resolved for the GeoJSON writers. The forced EPSG
    codes win over the ones read from the CRS object, and are folded back into the returned
    ``CrsInfo`` so the reprojection uses them too.
    """
    from dataclasses import replace

    from energyml.utils.data.crs import extract_crs_info

    crs_info = None
    crs_obj = getattr(mesh, "crs_object", None)
    if isinstance(crs_obj, list):
        crs_obj = crs_obj[0] if crs_obj else None
    if crs_obj is not None:
        try:
            crs_info = extract_crs_info(crs_obj, workspace)
        except Exception as exc:  # pragma: no cover — extract_crs_info is already defensive
            logger.debug("CRS info extraction failed: %s", exc)

    projected_epsg_code = projected_epsg_code or getattr(crs_info, "projected_epsg_code", None)
    vertical_epsg_code = vertical_epsg_code or getattr(crs_info, "vertical_epsg_code", None)

    if crs_info is not None and (
        projected_epsg_code != crs_info.projected_epsg_code or vertical_epsg_code != crs_info.vertical_epsg_code
    ):
        crs_info = replace(
            crs_info,
            projected_epsg_code=projected_epsg_code,
            vertical_epsg_code=vertical_epsg_code,
        )
    return crs_info, projected_epsg_code, vertical_epsg_code


def _geojson_crs_info(mesh: Any, options: "GeoJSONExportOptions", workspace: Any):
    """Backward-compatible wrapper over :func:`_resolve_crs` taking the option object."""
    return _resolve_crs(mesh, workspace, options.projected_epsg_code, options.vertical_epsg_code)


def _collection_crs_members(crs_states: set, logger: Optional[Any] = None) -> dict:
    """Members declaring the CRS of a whole FeatureCollection, or ``{}``.

    *crs_states* holds one ``(projected_epsg, vertical_epsg, is_wgs84)`` triple per feature. An
    RFC 7946 document is implicitly in CRS84 and must **not** carry a ``crs`` member, so only the
    non-WGS84 states are considered — and only when they all agree, since a single collection
    cannot advertise two different source CRS.
    """
    not_wgs84 = [state for state in crs_states if not state[2] and state[0] is not None]
    if len(not_wgs84) == 1:
        return _geojson_crs_members(not_wgs84[0][0], not_wgs84[0][1])
    if len(not_wgs84) > 1:
        (logger or _MODULE_LOGGER).warning(
            "GeoJSON export: %d different source CRS in the same FeatureCollection — "
            "no collection-level CRS is declared, see the per-feature 'projected_epsg_code' property.",
            len(not_wgs84),
        )
    return {}


def _prepare_geojson_points(
    mesh: Any,
    pts: np.ndarray,
    options: "GeoJSONExportOptions",
    workspace: Any,
    current_frame: Optional["PointFrame"] = None,
) -> tuple:
    """
    Bring *pts* to WGS84 when possible and return
    ``(points, projected_epsg_code, vertical_epsg_code, is_wgs84)``.

    The transform itself, and the decision to fall back to the projected coordinates when no EPSG
    code is available / ``pyproj`` is missing / PROJ fails, all live in
    :func:`~energyml.utils.data.crs.to_frame`. This function only resolves which CRS applies and
    reports what was reached, so the GeoJSON writer and the 3-D writers degrade identically.
    """
    from energyml.utils.data.crs import PointFrame, to_frame

    crs_info, projected_epsg_code, vertical_epsg_code = _geojson_crs_info(mesh, options, workspace)

    if not options.to_wgs84 or len(pts) == 0:
        return pts, projected_epsg_code, vertical_epsg_code, False

    framed = to_frame(
        pts,
        crs_info,
        PointFrame.WGS84,
        current_frame or PointFrame.PROJECTED,
        use_network=options.use_network,
        inplace=False,
    )
    is_wgs84 = framed.frame is PointFrame.WGS84
    if not is_wgs84:
        logger.warning(
            "GeoJSON export: %s stays in its source CRS (non RFC 7946 conformant) — %s",
            getattr(mesh, "source_uuid", None) or getattr(mesh, "identifier", "?"),
            framed.degraded_reason or "unknown reason",
        )
    return framed.points, projected_epsg_code, vertical_epsg_code, is_wgs84


def _with_points(mesh: Any, points: np.ndarray, frame: Optional["PointFrame"] = None) -> Any:
    """Shallow copy of *mesh* carrying *points* (and *frame*), whatever mesh family it is.

    The coordinate field is named ``point_list`` in the legacy hierarchy and ``points`` in the
    numpy one; both are dataclasses, so the copy shares every other field with the original and
    the caller's array is never written back into the source mesh.
    """
    from dataclasses import replace

    if hasattr(mesh, "point_list"):
        updates: Dict[str, Any] = {"point_list": points.tolist()}
    else:
        updates = {"points": points}
    if frame is not None:
        updates["frame"] = frame
    return replace(mesh, **updates)


def export_geojson(
    mesh_list: Any,
    out: TextIO,
    options: Optional[GeoJSONExportOptions] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    use_network: bool = False,
) -> None:
    """Export mesh data to GeoJSON FeatureCollection.

    Coordinates are reprojected to WGS84 (longitude, latitude, ellipsoidal height) by default,
    as required by RFC 7946 — see :class:`GeoJSONExportOptions`.  When the reprojection cannot
    be done, the source CRS is advertised through the ``crs`` (GeoJSON 2008) and
    ``coordRefSys`` (OGC JSON-FG) members instead.

    Every feature carries the identification metadata of its source object : the RFC 7946
    ``id`` member holds the energyml uuid, and ``properties`` holds the ``uuid``,
    ``qualified_type`` and ``Citation`` fields (title, creation, last_update, …).

    :param mesh_list: One or more meshes.
    :param out: Text output stream.
    :param options: GeoJSON export options.
    :param contexts: Optional colour / metadata context dict.
    :param use_crs_displacement: Apply CRS displacement to ``NumpyMesh`` points.

    .. note::
        This function is the *frame* half of the export — it resolves the coordinate frame
        (``use_crs_displacement`` / ``frame`` / ``origin_shift``) and the presentation properties
        (colours from *contexts*, ``source_uuid``, ``patch_index``) — and then hands the meshes to
        :func:`export_geojson_io`, which owns the one implementation of the geometry, of the CRS
        declaration and of the bounding boxes. It used to assemble the FeatureCollection a second
        time on its own, with its own reprojection call and its own geometry rules; the two
        assemblies had already drifted apart (no point-set branch on this side, ``MultiLineString``
        instead of ``LineString`` on the other).
    """
    from energyml.utils.introspection import get_object_metadata

    if options is None:
        options = GeoJSONExportOptions()

    patches = _normalize_to_patches(mesh_list)
    workspace = _workspace_from_contexts(contexts)
    _origin_shift = resolve_origin_shift(patches, use_crs_displacement, workspace, frame, origin_shift, use_network)

    prepared: List[Any] = []
    extra_properties: List[Optional[Dict]] = []
    feature_ids: List[Optional[str]] = []

    for mesh in patches:
        pts, pts_frame, _ = _get_export_points(mesh, use_crs_displacement, workspace, frame, _origin_shift, use_network)
        prepared.append(_with_points(mesh, np.asarray(pts, dtype=np.float64).reshape(-1, 3), pts_frame))

        source_uuid = getattr(mesh, "source_uuid", None) or get_object_metadata(
            getattr(mesh, "energyml_object", None)
        ).get("uuid")
        patch_index = getattr(mesh, "patch_index", None)

        props: Dict[str, Any] = {**options.properties, "source_uuid": source_uuid, "patch_index": patch_index}
        color = _get_context_color(getattr(mesh, "source_uuid", None), contexts)
        if color:
            r, g, b, a = color
            props["color"] = f"#{r:02x}{g:02x}{b:02x}"
            props["opacity"] = round(a / 255.0, 4)

        extra_properties.append(props)
        feature_ids.append(_feature_id(source_uuid, patch_index))

    buffer = BytesIO()
    export_geojson_io(
        out=buffer,
        mesh_list=prepared,
        properties=extra_properties,
        workspace=workspace,
        to_wgs84=options.to_wgs84,
        include_metadata=options.include_metadata,
        use_network=options.use_network,
        indent=options.indent,
        explode_elements=options.explode_elements,
        feature_ids=feature_ids,
        anycrs_prefix=False,
        projected_epsg_code=options.projected_epsg_code,
        vertical_epsg_code=options.vertical_epsg_code,
    )
    out.write(buffer.getvalue().decode("utf-8"))


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def _write(
    mesh_list: Any,
    out: TextIO,
    *,
    obj_name: Optional[str] = None,
    options: Any = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    companion: Any = None,
) -> None:
    """Uniform adapter used by the registry."""
    export_geojson(
        mesh_list,
        out,
        options,
        contexts,
        use_crs_displacement,
        frame=frame,
        origin_shift=origin_shift,
    )


register_format(
    FormatSpec(
        format=ExportFormat.GEOJSON,
        description="GeoJSON — geographic data (lines, polygons, point clouds)",
        filter_label="GeoJSON Files (*.geojson)",
        writer=_write,
        binary=False,
        options_class=GeoJSONExportOptions,
    )
)


# ---------------------------------------------------------------------------
# Streaming writers (moved from mesh.py)
#
# These build a GeoJSON document incrementally into a byte stream, so the peak memory is
# bounded by one feature instead of the whole FeatureCollection. The dict-building helpers
# above and below are thin wrappers over them, so there is a single implementation of the
# geometry: mesh.py used to carry a second, independent one (_create_shape).
# ---------------------------------------------------------------------------


class GeoJsonGeometryType(Enum):
    """GeoJson type enum"""

    Point = "Point"
    MultiPoint = "MultiPoint"
    LineString = "LineString"
    MultiLineString = "MultiLineString"
    Polygon = "Polygon"
    MultiPolygon = "MultiPolygon"


def energyml_type_to_geojson_type(energyml_type: str):
    if "PolylineSet" in energyml_type:
        return GeoJsonGeometryType.MultiLineString
    elif "Polyline" in energyml_type:
        return GeoJsonGeometryType.LineString
    elif "PointSet" in energyml_type:
        return GeoJsonGeometryType.MultiPoint
    elif "Point" in energyml_type:
        return GeoJsonGeometryType.Point
    elif "TriangulatedSet" in energyml_type:
        return GeoJsonGeometryType.MultiPolygon
    elif "Triangulated" in energyml_type:
        return GeoJsonGeometryType.Polygon
    elif "Grid2" in energyml_type:
        return GeoJsonGeometryType.MultiPolygon
    return GeoJsonGeometryType.Point


def _recompute_min_max(
    old_min: List,  # out parameter
    old_max: List,  # out parameter
    potential_min: List,
    potential_max: List,
) -> None:
    """Merge one candidate bounding box into the accumulators, extending them when needed."""
    for i in range(len(potential_min)):
        if i >= len(old_min):
            old_min.append(potential_min[i])
        elif potential_min[i] is not None:
            old_min[i] = min(old_min[i], potential_min[i])

    for i in range(len(potential_max)):
        if i >= len(old_max):
            old_max.append(potential_max[i])
        elif potential_max[i] is not None:
            old_max[i] = max(old_max[i], potential_max[i])


def _recompute_min_max_from_points(
    old_min: List,  # out parameter
    old_max: List,  # out parameter
    points: Any,
) -> None:
    """Merge the bounding box of *points* into the accumulators.

    Reduced with numpy in one pass. The previous version recursed once per point and compared
    each coordinate with the built-in ``min`` / ``max``, i.e. a handful of Python calls per point
    on the only loop of the export that runs per point.
    """
    arr = np.asarray(points, dtype=np.float64)
    if arr.size == 0:
        return
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    else:
        arr = arr.reshape(-1, arr.shape[-1])
    _recompute_min_max(old_min, old_max, arr.min(axis=0).tolist(), arr.max(axis=0).tolist())


class _JsonIndent:
    """
    Whitespace emitter for the streaming GeoJSON writers.

    Only the *structure* is indented: the collection, the features, the geometry
    and the containers of the coordinates. The innermost coordinate arrays stay
    on a single line — unrolling every ``[x, y, z]`` over four lines does not make
    a document more readable, it inflates it (measured x2.5 on a real export), and
    it would put the indentation on the only hot path of these writers, the one
    that runs once per point.

    ``_JsonIndent(None)`` is the disabled form: every method returns the exact
    bytes the writers used before, so the single-line output is unchanged.
    """

    __slots__ = ("unit", "_depth", "_cache")

    def __init__(self, indent: Optional[Union[int, str, "_JsonIndent"]] = None):
        if indent is None:
            self.unit: Optional[str] = None
        elif isinstance(indent, int):
            self.unit = " " * max(0, indent)
        else:
            self.unit = str(indent)
        self._depth = 0
        self._cache: Dict[int, bytes] = {}

    @classmethod
    def coerce(cls, indent: Optional[Union[int, str, "_JsonIndent"]]) -> "_JsonIndent":
        """Accept an already built indenter, so it can be threaded through the recursion."""
        return indent if isinstance(indent, cls) else cls(indent)

    @property
    def enabled(self) -> bool:
        return self.unit is not None

    def nl(self) -> bytes:
        """Line break followed by the indentation of the current level (``b""`` when disabled)."""
        if self.unit is None:
            return b""
        cached = self._cache.get(self._depth)
        if cached is None:
            cached = ("\n" + self.unit * self._depth).encode()
            self._cache[self._depth] = cached
        return cached

    def open(self) -> bytes:
        """Enter a nesting level, and return the break that starts its first item."""
        self._depth += 1
        return self.nl()

    def close(self) -> bytes:
        """Leave a nesting level, and return the break that puts its closing bracket in place."""
        self._depth = max(0, self._depth - 1)
        return self.nl()

    def sep(self) -> bytes:
        """Comma between two items or two members, with the break (or space) that follows it."""
        return b"," + (self.nl() if self.unit is not None else b" ")


def _dumps_at_depth(value: Any, ind: _JsonIndent) -> bytes:
    """
    Serialise a small value with :func:`json.dumps`, re-indenting its continuation
    lines so that they line up with the current depth.

    Only used for the metadata members (``properties``, ``name``): they weigh a few
    dozen bytes, so the extra string work is irrelevant — unlike on the coordinates.
    """
    if not ind.enabled:
        return json.dumps(value).encode()
    text = json.dumps(value, indent=ind.unit)
    if "\n" not in text:
        return text.encode()
    return text.replace("\n", ind.nl().decode()).encode()


def _write_geojson_shape(
    out: BytesIO,
    geo_type: GeoJsonGeometryType,
    point_list: List[List[float]],
    indices: Optional[Union[List[List[int]], List[int]]] = None,
    point_offset: int = 0,
    logger: Optional[Any] = None,
    _print_list_boundaries: Optional[bool] = True,
    ind: Optional[Union[int, str, _JsonIndent]] = None,
) -> Tuple[List[float], List[float]]:
    """
    Write a shape from a point list [ [x0, y0 (, z0)? ], ..., [xn, yn (, zn)? ] ]
    using indices. If indices is a simple list, result will be a line like :  [p0, ..., pn]. With p0 and pn
    a list of coordinate from "points" parameter (like [x0, y0 (, z0)? ])
    If the indices are a list of list, result will be polygones like :
    [
        [poly0_p0, ..., poly0_pn],
        ...
        [polyn_p0, ..., polyn_pn],
    ]
    :param ind: indentation of the *containers* of the coordinates. The list of points of a
                line or a ring is always written on a single line.
    :return shape, minXYZ (as list), maxXYZ (as list)
    """
    mins = []
    maxs = []
    ind = _JsonIndent.coerce(ind)
    try:
        if geo_type == GeoJsonGeometryType.LineString:
            if indices is not None and len(indices) > 0:
                cpt = 0
                if _print_list_boundaries:
                    out.write(b"[")
                for idx in indices:
                    out.write(json.dumps(point_list[idx + point_offset]).encode("utf-8"))
                    if cpt < len(indices) - 1:
                        out.write(b", ")
                    cpt += 1
                if _print_list_boundaries:
                    out.write(b"]")
                # One reduction for the whole line rather than one per point: this loop is the
                # only hot path of the writer.
                _recompute_min_max_from_points(mins, maxs, [point_list[i + point_offset] for i in indices])
            else:
                out.write(json.dumps(point_list).encode("utf-8"))
                _recompute_min_max_from_points(mins, maxs, point_list)
        elif geo_type == GeoJsonGeometryType.MultiPoint or geo_type == GeoJsonGeometryType.Point:
            out.write(json.dumps(point_list).encode("utf-8"))
            _recompute_min_max_from_points(mins, maxs, point_list)
        elif geo_type == GeoJsonGeometryType.MultiLineString:
            if indices is not None and len(indices) > 0 and isinstance(indices[0], list):
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
                cpt = 0
                for idx in indices:
                    _min, _max = _write_geojson_shape(
                        out=out,
                        geo_type=GeoJsonGeometryType.MultiLineString,
                        point_list=point_list,
                        indices=idx,
                        point_offset=point_offset,
                        logger=logger,
                        _print_list_boundaries=False,
                        ind=ind,
                    )
                    if cpt < len(indices) - 1:
                        out.write(ind.sep())
                    cpt += 1
                    _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
            else:
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
                _min, _max = _write_geojson_shape(
                    out=out,
                    geo_type=GeoJsonGeometryType.LineString,
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                    ind=ind,
                )
                _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
        elif geo_type == GeoJsonGeometryType.Polygon:
            # First and last must be the same
            if indices is not None and len(indices) > 0:
                if indices[0] != indices[-1]:
                    indices.append(indices[0])
            elif point_list[0] != point_list[-1]:
                point_list.append(point_list[0])

            mins, maxs = _write_geojson_shape(
                out=out,
                geo_type=GeoJsonGeometryType.MultiLineString,  # Here we only provide 1 line, the external one (outer-ring)
                point_list=point_list,
                indices=indices,
                point_offset=point_offset,
                logger=logger,
                _print_list_boundaries=_print_list_boundaries,
                ind=ind,
            )
        elif geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None and len(indices) > 0 and isinstance(indices[0], list):
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
                cpt = 0
                for idx in indices:
                    _min, _max = _write_geojson_shape(
                        out=out,
                        geo_type=GeoJsonGeometryType.MultiPolygon,  # Here we only provide 1 line, the external one (outer-ring)
                        point_list=point_list,
                        indices=idx,
                        point_offset=point_offset,
                        logger=logger,
                        _print_list_boundaries=False,
                        ind=ind,
                    )
                    if cpt < len(indices) - 1:
                        out.write(ind.sep())
                    cpt += 1
                    _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
            else:
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
                _min, _max = _write_geojson_shape(
                    out=out,
                    geo_type=GeoJsonGeometryType.Polygon,  # Here we only provide 1 line, the external one (outer-ring)
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                    ind=ind,
                )
                _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
    except Exception as e:
        # never swallow silently: a failure here produces a geometry without coordinates
        (logger or _MODULE_LOGGER).error(
            "@_write_geojson_shape failed for a %s geometry: %s: %s", geo_type.name, type(e).__name__, e
        )
        # raise e
    return mins, maxs


def _as_json_ready_list(value: Any) -> Any:
    """
    Convert numpy arrays / numpy scalars into plain python lists and floats.

    The GeoJSON writers below serialize the points with :func:`json.dumps`, which does not
    support numpy types : depending on the representation and on the way its points were read,
    ``AbstractMesh.point_list`` may be a ``list`` *or* an ``ndarray``.  Without this conversion
    the serialization raises ``TypeError: Object of type ndarray is not JSON serializable``.
    """
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [_as_json_ready_list(v) for v in value]
    return value


def to_geojson_feature(
    mesh: "AbstractMesh",
    geo_type: GeoJsonGeometryType = GeoJsonGeometryType.Point,
    geo_type_prefix: Optional[str] = "",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger=None,
    feature_id: Optional[str] = None,
) -> Dict:
    """
    Build a GeoJSON Feature as a dict.

    Serialises through :func:`write_geojson_feature` and parses the result back, so the geometry
    has a single implementation. The previous dict-building path (``_create_shape``) was a second,
    independent transcription of the same five-branch recursion — roughly 100 lines that had to be
    kept in step with the streaming one by hand.

    :param geo_type_prefix: prefix of the ``type`` member. Empty (default) for a standard
                            RFC 7946 ``"Feature"``; ``"AnyCrs"`` marks non-WGS84 coordinates.
    :param feature_id: value of the RFC 7946 ``id`` member (the energyml uuid, typically).
    """
    raw_points = mesh_points(mesh)
    if raw_points is None or len(raw_points) == 0:
        return {}

    buffer = BytesIO()
    write_geojson_feature(
        out=buffer,
        mesh=mesh,
        geo_type=geo_type,
        geo_type_prefix=geo_type_prefix,
        properties=properties,
        point_offset=point_offset,
        logger=logger,
        feature_id=feature_id,
    )
    raw = buffer.getvalue()
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _write_feature(
    out: BytesIO,
    geo_type: GeoJsonGeometryType,
    points: Any,
    indices: Optional[Union[List[List[int]], List[int]]] = None,
    geo_type_prefix: Optional[str] = "",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger: Optional[Any] = None,
    feature_id: Optional[str] = None,
    ind: Optional[Union[int, str, _JsonIndent]] = None,
    identifier: str = "?",
) -> Tuple[List[float], List[float]]:
    """
    Write one GeoJSON Feature from already-resolved coordinates, and return its ``(mins, maxs)``.

    Takes *points* / *indices* rather than a mesh so that a single element of a patch can be
    written on its own — that is what ``explode_elements`` needs, and what let the registry
    writer stop transcribing the geometry rules a second time.
    """
    ind = _JsonIndent.coerce(ind)
    if points is None or len(points) == 0:
        return [], []

    # A ring must be closed. When several rings are given (a list of index lists) the closing
    # is done here; when a single flat ring is given, _write_geojson_shape closes it itself.
    close_rings = (
        geo_type in (GeoJsonGeometryType.Polygon, GeoJsonGeometryType.MultiPolygon)
        and indices is not None
        and len(indices) > 0
        and isinstance(indices[0], list)
    )
    if close_rings:
        for ring in indices:
            ring.append(ring[0])

    try:
        out.write(b"{")  # start feature
        out.write(ind.open())
        out.write(f'"type": "{geo_type_prefix or ""}Feature"'.encode())
        if feature_id is not None:
            out.write(ind.sep())
            out.write(f'"id": {json.dumps(feature_id)}'.encode())
        out.write(ind.sep())
        out.write(b'"properties": ')
        out.write(_dumps_at_depth(properties or {}, ind))
        out.write(ind.sep())
        out.write(b'"geometry": ')

        out.write(b"{")  # start geometry
        out.write(ind.open())
        out.write(f'"type": "{geo_type.name}"'.encode())
        out.write(ind.sep())
        out.write(b'"coordinates": ')
        coordinates_start = out.tell()
        mins, maxs = _write_geojson_shape(
            out=out,
            geo_type=geo_type,
            point_list=points,
            indices=indices,
            point_offset=point_offset,
            logger=logger,
            ind=ind,
        )
        if out.tell() == coordinates_start:
            # the shape could not be written (see the error logged by _write_geojson_shape) :
            # write an empty coordinate list so that the document stays valid JSON
            (logger or _MODULE_LOGGER).error(
                "No coordinate written for the %s geometry of '%s' (%d points) — "
                "an empty geometry is written instead.",
                geo_type.name,
                identifier,
                len(points),
            )
            out.write(b"[]")

        bbox_geometry = mins + maxs  # TODO : see : https://www.rfc-editor.org/rfc/rfc7946#section-5

        out.write(ind.sep())
        # the bbox is a flat list of 4 or 6 numbers: it stays on one line
        out.write(f'"bbox": {json.dumps(bbox_geometry)}'.encode())
        out.write(ind.close())
        out.write(b"}")  # end geometry

        out.write(ind.close())
        out.write(b"}")  # End feature
    finally:
        # the closing point was appended to the caller's lists: undo it whatever happened
        if close_rings:
            for ring in indices:
                ring.pop()

    # The extents are already computed to write the per-geometry bbox; returning them lets
    # the caller build the collection-level one without a second pass over the coordinates.
    return bbox_geometry[: len(bbox_geometry) // 2], bbox_geometry[len(bbox_geometry) // 2 :]


def write_geojson_feature(
    out: BytesIO,
    mesh: AbstractMesh,
    geo_type: GeoJsonGeometryType = GeoJsonGeometryType.Point,
    geo_type_prefix: Optional[str] = "",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger=None,
    feature_id: Optional[str] = None,
    indent: Optional[Union[int, str, _JsonIndent]] = None,
) -> Tuple[List[float], List[float]]:
    """
    Write a single GeoJSON Feature for *mesh*, and return its ``(mins, maxs)`` extents.

    Resolves the coordinates and the connectivity of *mesh* — whatever mesh family it belongs
    to — and hands them to :func:`_write_feature`.

    :param geo_type_prefix: prefix of the ``type`` member. Empty (default) for a standard
                            RFC 7946 ``"Feature"``; the historical ``"AnyCrs"`` value marks
                            coordinates that are *not* in WGS84.
    :param feature_id: value of the RFC 7946 ``id`` member (the energyml uuid, typically).
    :param indent: number of spaces (or indentation string) of the pretty-printed form.
                   None (default) keeps everything on a single line. See :class:`_JsonIndent`
                   for what is indented and what deliberately is not.
    """
    raw_points = mesh_points(mesh)
    if raw_points is None or len(raw_points) == 0:
        return [], []

    # points / indices may be numpy arrays : json.dumps only accepts plain python types
    return _write_feature(
        out=out,
        geo_type=geo_type,
        points=_as_json_ready_list(raw_points),
        indices=_as_json_ready_list(mesh_indices(mesh)),
        geo_type_prefix=geo_type_prefix,
        properties=properties,
        point_offset=point_offset,
        logger=logger,
        feature_id=feature_id,
        ind=indent,
        identifier=getattr(mesh, "identifier", "?") or "?",
    )


def mesh_points(mesh: Any) -> Any:
    """Coordinates of *mesh*, whatever mesh family it belongs to.

    The legacy containers expose ``point_list``, the numpy ones ``points``. The streaming
    writer only knew the first, so passing it a ``NumpyMultiMesh`` raised
    ``TypeError: 'NumpyMultiMesh' object is not iterable`` — the two halves of the GeoJSON API
    accepted different mesh families.
    """
    points = getattr(mesh, "point_list", None)
    return getattr(mesh, "points", None) if points is None else points


def mesh_indices(mesh: Any) -> List[List[int]]:
    """Connectivity of *mesh* as a list of index lists, whatever mesh family it belongs to.

    Legacy meshes already store it that way; numpy ones store the VTK flat encoding, decoded
    here. A point set has no connectivity in either family and yields ``[]``.
    """
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPolylineMesh

    if not isinstance(mesh, NumpyMesh):
        return mesh.get_indices()

    if isinstance(mesh, NumpyPolylineMesh):
        return [idx.tolist() for idx in _parse_vtk_flat_lines(mesh.lines)]
    connectivity = _get_faces_or_cells(mesh)
    if connectivity is None or len(connectivity) == 0:
        return []
    return [idx.tolist() for idx in _parse_vtk_flat_faces(connectivity)]


def mesh_to_geojson_type(obj: Any) -> GeoJsonGeometryType:
    """Pick the GeoJSON geometry type matching *obj*, whatever mesh family it belongs to.

    The single place that maps a mesh class to a geometry kind. The registry writer used to
    repeat the rule with its own ``isinstance`` chain and had no branch for a point set, so a
    ``PointSetMesh`` — which legitimately carries points and *no* indices — went through a loop
    over its (empty) index list and produced a FeatureCollection with zero features.

    Surfaces and volumes become polygons, poly-lines become lines, and anything else is a point
    cloud: a mesh with no connectivity still has coordinates worth exporting.
    """
    # Imported lazily: mesh.py imports this module, so a module-level import would be circular.
    from energyml.utils.data.mesh import PolylineSetMesh, SurfaceMesh
    from energyml.utils.data.mesh_numpy import (
        NumpyPolylineMesh,
        NumpySurfaceMesh,
        NumpyVolumeMesh,
    )

    if isinstance(obj, (SurfaceMesh, NumpySurfaceMesh, NumpyVolumeMesh)):
        return GeoJsonGeometryType.MultiPolygon
    if isinstance(obj, (PolylineSetMesh, NumpyPolylineMesh)):
        return GeoJsonGeometryType.MultiLineString
    return GeoJsonGeometryType.MultiPoint


def _geojson_mesh_metadata(mesh: "AbstractMesh", workspace: Optional["EnergymlStorageInterface"] = None) -> Dict:
    """
    Build the properties of a feature from the energyml object carried by *mesh* :
    uuid, qualified type, Citation fields and mesh identifier.

    The EPSG codes are *not* read here: they come from :func:`_resolve_crs`, which the caller
    already runs to decide whether the coordinates can be reprojected. Extracting them twice meant
    two ``extract_crs_info`` calls per mesh, and two places able to disagree on the answer.

    :param workspace: kept for backward compatibility; unused.
    """
    from energyml.utils.introspection import get_object_metadata

    properties: Dict = dict(get_object_metadata(getattr(mesh, "energyml_object", None)))
    if getattr(mesh, "identifier", None):
        properties["identifier"] = mesh.identifier
    return properties


def _geojson_reproject_mesh(
    mesh: "AbstractMesh",
    workspace: Optional["EnergymlStorageInterface"] = None,
    use_network: bool = False,
    logger: Optional[Any] = None,
    to_wgs84: bool = True,
    projected_epsg_code: Optional[int] = None,
    vertical_epsg_code: Optional[int] = None,
) -> Tuple["AbstractMesh", bool, Optional[int], Optional[int]]:
    """
    Return ``(mesh, is_wgs84, projected_epsg_code, vertical_epsg_code)`` where *mesh* is a shallow
    copy whose points have been reprojected to WGS84, or the original mesh when the reprojection
    is not asked for or is impossible (no EPSG code, pyproj missing, transformation error).

    The transform and its fallbacks live in :func:`~energyml.utils.data.crs.to_frame`; this
    function only adapts the mesh containers to it. It used to re-implement the whole degradation
    ladder (missing EPSG / missing pyproj / PROJ failure) a second time.

    The EPSG codes are returned even when nothing is reprojected, so the caller can advertise the
    source CRS of a document it left in its projected coordinates.
    """
    from energyml.utils.data.crs import PointFrame, to_frame

    crs_info, projected_epsg_code, vertical_epsg_code = _resolve_crs(
        mesh, workspace, projected_epsg_code, vertical_epsg_code
    )

    raw_points = mesh_points(mesh)
    if not to_wgs84 or crs_info is None or raw_points is None or len(raw_points) == 0:
        return mesh, False, projected_epsg_code, vertical_epsg_code

    points = np.asarray(raw_points, dtype=np.float64).reshape(-1, 3)
    framed = to_frame(
        points,
        crs_info,
        PointFrame.WGS84,
        getattr(mesh, "frame", PointFrame.PROJECTED),
        use_network=use_network,
        inplace=False,
    )

    if framed.frame is not PointFrame.WGS84:
        (logger or _MODULE_LOGGER).warning(
            "GeoJSON export: %s stays in its source CRS (non RFC 7946 conformant) — %s",
            getattr(mesh, "source_uuid", None) or getattr(mesh, "identifier", "?"),
            framed.degraded_reason or "unknown reason",
        )
        return mesh, False, projected_epsg_code, vertical_epsg_code

    return _with_points(mesh, framed.points, framed.frame), True, projected_epsg_code, vertical_epsg_code


def _suffix_feature_id(feature_id: Optional[str], element_index: Optional[int]) -> Optional[str]:
    """Append an element index to a feature id, so exploded elements keep distinct ``id`` members."""
    if feature_id is None or element_index is None:
        return feature_id
    return f"{feature_id}_{element_index}"


def _effective_geo_type(geo_kind: GeoJsonGeometryType, element_count: int) -> GeoJsonGeometryType:
    """Collapse a ``Multi*`` kind to its singular form when the patch holds a single element.

    RFC 7946 has both forms and prefers the simplest one that fits, so a 15-station wellbore is a
    ``LineString`` and a single triangle a ``Polygon``. The two collection builders used to
    disagree exactly here — the registry one collapsed, the streaming one did not.
    """
    if element_count != 1:
        return geo_kind
    if geo_kind == GeoJsonGeometryType.MultiLineString:
        return GeoJsonGeometryType.LineString
    if geo_kind == GeoJsonGeometryType.MultiPolygon:
        return GeoJsonGeometryType.Polygon
    return geo_kind


def export_geojson_io(
    out: BytesIO,
    mesh_list: List[AbstractMesh],
    obj_name: Optional[str] = None,
    properties: Optional[List[Optional[Dict]]] = None,
    global_properties: Optional[Dict] = None,
    logger: Optional[Any] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    to_wgs84: bool = True,
    include_metadata: bool = True,
    use_network: bool = False,
    indent: Optional[Union[int, str]] = None,
    explode_elements: bool = False,
    feature_ids: Optional[List[Optional[str]]] = None,
    anycrs_prefix: bool = True,
    projected_epsg_code: Optional[int] = None,
    vertical_epsg_code: Optional[int] = None,
):
    """
    Stream a list of meshes as a GeoJSON FeatureCollection.

    This is the single implementation of the GeoJSON geometry: :func:`export_geojson` (the
    registry writer), :func:`export_geojson_dict` and :func:`to_geojson_feature` all go through
    it, so there is one set of rules for the geometry kinds, the CRS declaration and the bounding
    boxes.

    :param out: output stream
    :param mesh_list: meshes to export
    :param obj_name: value of the ``name`` member of the collection
    :param properties: extra per-mesh properties, aligned on *mesh_list*, merged on top of the
                       metadata built from the energyml object of each mesh
    :param global_properties: extra members written at the collection level
    :param logger: logger used for the per-feature diagnostics; defaults to this module's
    :param workspace: used to resolve the CRS objects (needed for the v2.2 compound CRS)
    :param to_wgs84: when True (default), coordinates are reprojected to WGS84 as required by
                     RFC 7946.  When the reprojection is not possible, the source CRS is
                     advertised through the ``crs`` / ``coordRefSys`` members.
    :param include_metadata: add the energyml metadata to the properties of every feature
    :param use_network: allow PROJ to download the geoid grids used by vertical transformations
    :param indent: number of spaces (or indentation string) for a pretty-printed document.
                   None (default) keeps the historical single-line output.

                   The document structure is indented but the coordinates of a line or a ring
                   stay on one line: that is what keeps the file readable without inflating it,
                   and it leaves the per-point write path untouched, so the export costs about
                   the same as the compact one — far less than serialising, re-reading and
                   re-dumping the document with ``json.dumps(indent=...)``.
    :param explode_elements: emit one feature per triangle / per line instead of one feature per
                             patch. Off by default: exploding repeats the whole metadata block —
                             uuid, citation, EPSG codes — on every element.
    :param feature_ids: explicit RFC 7946 ``id`` per mesh, aligned on *mesh_list*. Defaults to the
                        uuid of the source object.
    :param anycrs_prefix: when True (default), features whose coordinates are not WGS84 keep the
                          historical ``"AnyCrsFeature"`` type. Set to False for a plain
                          ``"Feature"`` in every case.
    :param projected_epsg_code: force the horizontal EPSG code instead of reading it from the CRS
    :param vertical_epsg_code: force the vertical EPSG code instead of reading it from the CRS
    """
    # Accept both mesh families and every container shape, like the registry writer: a caller
    # holding the NumpyMultiMesh returned by read_numpy_mesh_object used to get
    # `TypeError: 'NumpyMultiMesh' object is not iterable` here.
    mesh_list = _normalize_to_patches(mesh_list)

    # the source index is kept so that `properties` / `feature_ids` stay aligned on `mesh_list`
    exported: List[Tuple[int, Any, Dict]] = []
    crs_states: set = set()

    for mesh_index, mesh in enumerate(mesh_list):
        mesh_pts = mesh_points(mesh)
        if mesh_pts is None or len(mesh_pts) == 0:
            # write_geojson_feature() would write nothing for it; dropping it here keeps the
            # separator logic below exact (an empty mesh in last position used to leave a
            # trailing comma, which is not valid JSON).
            continue

        feature_properties: Dict = {}
        if include_metadata:
            feature_properties.update(_geojson_mesh_metadata(mesh))

        mesh, is_wgs84, mesh_projected, mesh_vertical = _geojson_reproject_mesh(
            mesh,
            workspace=workspace,
            use_network=use_network,
            logger=logger,
            to_wgs84=to_wgs84,
            projected_epsg_code=projected_epsg_code,
            vertical_epsg_code=vertical_epsg_code,
        )
        if mesh_projected is not None:
            feature_properties["projected_epsg_code"] = mesh_projected
        if mesh_vertical is not None:
            feature_properties["vertical_epsg_code"] = mesh_vertical
        if is_wgs84:
            # keep the provenance of the coordinates now that they have been converted
            feature_properties["source_crs"] = f"EPSG:{mesh_projected}"
            feature_properties["coordinates_crs"] = "OGC:CRS84"
        crs_states.add((mesh_projected, mesh_vertical, is_wgs84))
        exported.append((mesh_index, mesh, feature_properties))

    ind = _JsonIndent(indent)

    out.write(b"{")
    out.write(ind.open())
    out.write(b'"type": "FeatureCollection"')
    if obj_name is not None:
        out.write(ind.sep())
        # json.dumps rather than a raw concatenation: a title may contain a quote
        out.write(f'"name": {json.dumps(obj_name)}'.encode())

    for k, v in _collection_crs_members(crs_states, logger).items():
        out.write(ind.sep())
        out.write(f'"{k}": '.encode())
        out.write(_dumps_at_depth(v, ind))

    if global_properties is not None and len(global_properties) > 0:
        for k, v in global_properties.items():
            out.write(ind.sep())
            out.write(f"{json.dumps(k)}: ".encode())
            out.write(_dumps_at_depth(v, ind))

    out.write(ind.sep())
    out.write(b'"features": [')
    out.write(ind.open())

    written = 0
    collection_mins: List[float] = []
    collection_maxs: List[float] = []

    for mesh_index, mesh, feature_properties in exported:
        explicit = properties[mesh_index] if properties is not None and len(properties) > mesh_index else None
        feature_properties = {**feature_properties, **(explicit or {})}
        # "AnyCrsFeature" keeps flagging the features whose coordinates are not WGS84
        prefix = "" if not anycrs_prefix or feature_properties.get("coordinates_crs") == "OGC:CRS84" else "AnyCrs"
        base_id = feature_properties.get("uuid")
        if feature_ids is not None and len(feature_ids) > mesh_index:
            base_id = feature_ids[mesh_index]

        points = _as_json_ready_list(mesh_points(mesh))
        elements = _as_json_ready_list(mesh_indices(mesh))
        geo_kind = mesh_to_geojson_type(mesh)
        identifier = getattr(mesh, "identifier", "?") or "?"

        if geo_kind != GeoJsonGeometryType.MultiPoint and not elements:
            # Points but no usable connectivity: export the cloud rather than nothing at all.
            (logger or _MODULE_LOGGER).warning(
                "GeoJSON export: %s carries %d point(s) but no %s element — exported as a point cloud.",
                type(mesh).__name__,
                len(points),
                "line" if geo_kind == GeoJsonGeometryType.MultiLineString else "face",
            )
            geo_kind = GeoJsonGeometryType.MultiPoint

        if explode_elements and geo_kind != GeoJsonGeometryType.MultiPoint:
            single = _effective_geo_type(geo_kind, 1)
            features_to_write = [
                (single, list(element), i, {**feature_properties, "element_index": i})
                for i, element in enumerate(elements)
            ]
        else:
            features_to_write = [(_effective_geo_type(geo_kind, len(elements)), elements, None, feature_properties)]
            if features_to_write[0][0] in (GeoJsonGeometryType.LineString, GeoJsonGeometryType.Polygon):
                # a single element: the shape writer expects the flat index list, not [[...]]
                features_to_write = [(features_to_write[0][0], elements[0], None, feature_properties)]

        for geo_type, indices, element_index, props in features_to_write:
            if written > 0:
                out.write(ind.sep())
            mins, maxs = _write_feature(
                out=out,
                geo_type=geo_type,
                points=points,
                indices=indices,
                geo_type_prefix=prefix,
                properties=props,
                feature_id=_suffix_feature_id(base_id, element_index),
                logger=logger,
                ind=ind,
                identifier=identifier,
            )
            _recompute_min_max(collection_mins, collection_maxs, mins, maxs)
            written += 1

    out.write(ind.close())
    out.write(b"]")  # end features

    # RFC 7946 §5: a FeatureCollection may carry a bbox. It is written after the features
    # because the extents are only known once they have all been streamed out — member order
    # carries no meaning in JSON.
    if collection_mins and collection_maxs:
        out.write(ind.sep())
        out.write(f'"bbox": {json.dumps(collection_mins + collection_maxs)}'.encode())

    out.write(ind.close())
    out.write(b"}")  # end geojson


def export_geojson_dict(
    mesh_list: List["AbstractMesh"],
    obj_name: Optional[str] = None,
    properties: Optional[List[Optional[Dict]]] = None,
    logger: Optional[Any] = None,
    workspace: Optional["EnergymlStorageInterface"] = None,
    include_metadata: bool = True,
    to_wgs84: bool = True,
    use_network: bool = False,
) -> Dict:
    """
    Same as :func:`export_geojson_io` but returns a dict instead of streaming.

    It now runs the streaming writer and parses its output, so both variants share one
    implementation of the geometry and one CRS pipeline.

    .. note::
        **Behaviour change.** This function used to leave the coordinates in their source CRS and
        tag every feature ``"AnyCrsFeature"``, producing a document that was not RFC 7946
        conformant without saying so. It now reprojects to WGS84 like every other exporter. Pass
        ``to_wgs84=False`` to get the previous output.

    :param to_wgs84: reproject the coordinates to WGS84 (RFC 7946). When the reprojection is not
                     possible, the source CRS is advertised through the ``crs`` / ``coordRefSys``
                     members and the features keep the ``AnyCrs`` prefix.
    :param use_network: allow PROJ to download the geoid grids used by the vertical transformation.
    """
    buffer = BytesIO()
    export_geojson_io(
        out=buffer,
        mesh_list=mesh_list,
        obj_name=obj_name,
        properties=properties,
        logger=logger,
        workspace=workspace,
        to_wgs84=to_wgs84,
        include_metadata=include_metadata,
        use_network=use_network,
    )
    return json.loads(buffer.getvalue().decode("utf-8"))


#: Public API of this module. Declared explicitly so that renaming or removing anything
#: else is not a breaking change, and so `from ... import *` does not leak the imports.
__all__ = [
    "export_geojson",
    "GeoJsonGeometryType",
    "energyml_type_to_geojson_type",
    "to_geojson_feature",
    "write_geojson_feature",
    "mesh_points",
    "mesh_indices",
    "mesh_to_geojson_type",
    "export_geojson_io",
    "export_geojson_dict",
]
