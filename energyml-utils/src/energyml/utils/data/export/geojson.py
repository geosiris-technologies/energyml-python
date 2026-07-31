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

log = logging.getLogger(__name__)

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


def _geojson_crs_info(mesh: Any, options: "GeoJSONExportOptions", workspace: Any):
    """Return ``(crs_info, projected_epsg_code, vertical_epsg_code)`` for *mesh*.

    The EPSG codes forced through the options win over the ones read from the CRS object, and are
    folded back into the returned ``CrsInfo`` so the reprojection uses them too.
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
            log.debug("CRS info extraction failed: %s", exc)

    projected_epsg_code = options.projected_epsg_code or getattr(crs_info, "projected_epsg_code", None)
    vertical_epsg_code = options.vertical_epsg_code or getattr(crs_info, "vertical_epsg_code", None)

    if crs_info is not None and (
        projected_epsg_code != crs_info.projected_epsg_code or vertical_epsg_code != crs_info.vertical_epsg_code
    ):
        crs_info = replace(
            crs_info,
            projected_epsg_code=projected_epsg_code,
            vertical_epsg_code=vertical_epsg_code,
        )
    return crs_info, projected_epsg_code, vertical_epsg_code


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
        log.warning(
            "GeoJSON export: %s stays in its source CRS (non RFC 7946 conformant) — %s",
            getattr(mesh, "source_uuid", None) or getattr(mesh, "identifier", "?"),
            framed.degraded_reason or "unknown reason",
        )
    return framed.points, projected_epsg_code, vertical_epsg_code, is_wgs84


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
    """
    from energyml.utils.data.mesh import PolylineSetMesh, SurfaceMesh
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPointSetMesh, NumpyPolylineMesh
    from energyml.utils.introspection import get_object_metadata

    if options is None:
        options = GeoJSONExportOptions()

    patches = _normalize_to_patches(mesh_list)
    workspace = _workspace_from_contexts(contexts)
    _origin_shift = resolve_origin_shift(patches, use_crs_displacement, workspace, frame, origin_shift, use_network)
    features: List[dict] = []
    exported_points: List[np.ndarray] = []
    #: (projected_epsg, vertical_epsg, is_wgs84) of every patch — used to declare the CRS.
    crs_states: set = set()

    for mesh in patches:
        pts, _pts_frame, _ = _get_export_points(
            mesh, use_crs_displacement, workspace, frame, _origin_shift, use_network
        )
        pts, projected_epsg_code, vertical_epsg_code, is_wgs84 = _prepare_geojson_points(
            mesh, np.asarray(pts, dtype=np.float64).reshape(-1, 3), options, workspace, _pts_frame
        )
        crs_states.add((projected_epsg_code, vertical_epsg_code, is_wgs84))
        exported_points.append(pts)

        source_uuid = getattr(mesh, "source_uuid", None)
        patch_idx = getattr(mesh, "patch_index", None)
        color = _get_context_color(source_uuid, contexts)

        base_props: dict = {**options.properties}
        if options.include_metadata:
            base_props.update(get_object_metadata(getattr(mesh, "energyml_object", None)))
        base_props["source_uuid"] = source_uuid or base_props.get("uuid")
        base_props["patch_index"] = patch_idx
        if projected_epsg_code is not None:
            base_props["projected_epsg_code"] = projected_epsg_code
        if vertical_epsg_code is not None:
            base_props["vertical_epsg_code"] = vertical_epsg_code
        if is_wgs84:
            # keep the provenance of the coordinates now that they have been converted
            base_props["source_crs"] = f"EPSG:{projected_epsg_code}"
            base_props["coordinates_crs"] = "OGC:CRS84"
        if color:
            r, g, b, a = color
            base_props["color"] = f"#{r:02x}{g:02x}{b:02x}"
            base_props["opacity"] = round(a / 255.0, 4)

        def _feature(geometry: dict, element_index: Optional[int] = None, extra: Optional[dict] = None) -> dict:
            feature: dict = {"type": "Feature"}
            feature_id = _feature_id(source_uuid, patch_idx, element_index)
            if feature_id is not None:
                feature["id"] = feature_id
            feature["geometry"] = geometry
            feature["properties"] = base_props if extra is None else {**base_props, **extra}
            return feature

        # --- Collect the elements of this patch as coordinate lists ---
        # A patch is one feature. Exploding it into one feature per triangle or per segment
        # repeats the whole metadata block — uuid, citation, EPSG codes — on every element:
        # a 882-triangle surface became 882 features carrying 882 copies of its citation, and
        # a wellbore came out as N-1 two-point LineStrings instead of one line.
        # `explode_elements` restores the old behaviour for callers that relied on it.
        lines_coords: List[list] = []
        rings_coords: List[list] = []

        if isinstance(mesh, NumpyMesh):
            if isinstance(mesh, NumpyPointSetMesh):
                features.append(_feature({"type": "MultiPoint", "coordinates": pts.tolist()}))
            elif isinstance(mesh, NumpyPolylineMesh):
                lines_coords = [pts[seg].tolist() for seg in _parse_vtk_flat_lines(mesh.lines) if len(seg) >= 2]
            else:
                # NumpySurfaceMesh / NumpyVolumeMesh
                for face in _parse_vtk_flat_faces(_get_faces_or_cells(mesh)):
                    if len(face) < 3:
                        continue
                    ring = pts[face].tolist()
                    ring.append(ring[0])  # close ring
                    rings_coords.append(ring)
        else:
            # AbstractMesh legacy path — .tolist() because json.dump rejects numpy scalars
            for elem in mesh.get_indices():
                idx = np.asarray(elem, dtype=np.int64)
                if isinstance(mesh, PolylineSetMesh):
                    if len(idx) >= 2:
                        lines_coords.append(pts[idx].tolist())
                elif isinstance(mesh, SurfaceMesh):
                    if len(idx) >= 3:
                        ring = pts[idx].tolist()
                        ring.append(ring[0])
                        rings_coords.append(ring)

        if options.explode_elements:
            for seg_idx, coords in enumerate(lines_coords):
                features.append(
                    _feature(
                        {"type": "LineString", "coordinates": coords},
                        element_index=seg_idx,
                        extra={"element_index": seg_idx},
                    )
                )
            for face_idx, ring in enumerate(rings_coords):
                features.append(
                    _feature(
                        {"type": "Polygon", "coordinates": [ring]},
                        element_index=face_idx,
                        extra={"element_index": face_idx},
                    )
                )
        else:
            if len(lines_coords) == 1:
                features.append(_feature({"type": "LineString", "coordinates": lines_coords[0]}))
            elif lines_coords:
                features.append(_feature({"type": "MultiLineString", "coordinates": lines_coords}))
            if len(rings_coords) == 1:
                features.append(_feature({"type": "Polygon", "coordinates": [rings_coords[0]]}))
            elif rings_coords:
                features.append(_feature({"type": "MultiPolygon", "coordinates": [[r] for r in rings_coords]}))

    collection: dict = {"type": "FeatureCollection"}

    # Advertise the CRS only when the coordinates are NOT WGS84 : an RFC 7946 document is
    # implicitly in CRS84 and must not carry a 'crs' member.
    not_wgs84 = [state for state in crs_states if not state[2]]
    if len(not_wgs84) == 1:
        collection.update(_geojson_crs_members(not_wgs84[0][0], not_wgs84[0][1]))
    elif len(not_wgs84) > 1:
        log.warning(
            "GeoJSON export: %d different source CRS in the same FeatureCollection — "
            "no collection-level CRS is declared, see the per-feature 'projected_epsg_code' property.",
            len(not_wgs84),
        )

    bbox = _geojson_bbox(exported_points)
    if bbox is not None:
        collection["bbox"] = bbox

    collection["features"] = features

    json.dump(collection, out, indent=options.indent)


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
        (logger or logging).error(
            f"@_write_geojson_shape failed for a {geo_type.name} geometry: {type(e).__name__}: {e}"
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
    if mesh.point_list is None or len(mesh.point_list) == 0:
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
) -> None:
    """
    Write a single GeoJSON Feature.

    :param geo_type_prefix: prefix of the ``type`` member. Empty (default) for a standard
                            RFC 7946 ``"Feature"``; the historical ``"AnyCrs"`` value marks
                            coordinates that are *not* in WGS84.
    :param feature_id: value of the RFC 7946 ``id`` member (the energyml uuid, typically).
    :param indent: number of spaces (or indentation string) of the pretty-printed form.
                   None (default) keeps everything on a single line. See :class:`_JsonIndent`
                   for what is indented and what deliberately is not.
    """
    ind = _JsonIndent.coerce(indent)
    if mesh.point_list is not None and len(mesh.point_list) > 0:
        # point_list / indices may be numpy arrays : json.dumps only accepts plain python types
        points = _as_json_ready_list(mesh.point_list)

        indices = _as_json_ready_list(mesh.get_indices())
        # polygon must have the first and last point as the same
        if geo_type == GeoJsonGeometryType.Polygon or geo_type == GeoJsonGeometryType.MultiPolygon:
            if logger is not None:
                logger.debug("# to_geojson_feature > Reshaping indices for polygons")
            if indices is not None:
                for indices_i in indices:
                    indices_i.append(indices_i[0])
            if logger is not None:
                logger.debug("\t# to_geojson_feature > Indices reshaped")

        if logger is not None:
            logger.debug("# to_geojson_feature > Computing shape")

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
        # "type": f"{geo_type_prefix}{geo_type.name}",
        out.write(f'"type": "{geo_type.name}"'.encode())
        out.write(ind.sep())
        out.write('"coordinates": '.encode())
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
            (logger or logging).error(
                f"No coordinate written for the {geo_type.name} geometry of '{mesh.identifier}' "
                f"({len(points)} points) — an empty geometry is written instead."
            )
            out.write(b"[]")

        bbox_geometry = mins + maxs  # TODO : see : https://www.rfc-editor.org/rfc/rfc7946#section-5

        out.write(ind.sep())
        # the bbox is a flat list of 4 or 6 numbers: it stays on one line
        out.write(f'"bbox": {json.dumps(bbox_geometry)}'.encode())
        out.write(ind.close())
        out.write(b"}")  # end geometry

        # Pop previously added last :
        if geo_type == GeoJsonGeometryType.Polygon or geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None:
                for indices_i in indices:
                    indices_i.pop()

        if logger is not None:
            logger.debug("\t# to_geojson_feature > shaped")

        out.write(ind.close())
        out.write(b"}")  # End feature


def mesh_to_geojson_type(obj: "AbstractMesh") -> GeoJsonGeometryType:
    """Pick the GeoJSON geometry type matching the legacy mesh class of *obj*."""
    # Imported lazily: mesh.py imports this module, so a module-level import would be circular.
    from energyml.utils.data.mesh import PolylineSetMesh, SurfaceMesh

    if isinstance(obj, SurfaceMesh):
        return GeoJsonGeometryType.MultiPolygon
    elif isinstance(obj, PolylineSetMesh):
        return GeoJsonGeometryType.MultiLineString
    else:
        return GeoJsonGeometryType.MultiPoint


def _geojson_mesh_metadata(mesh: "AbstractMesh", workspace: Optional["EnergymlStorageInterface"] = None) -> Dict:
    """
    Build the properties of a feature from the energyml object carried by *mesh* :
    uuid, qualified type, Citation fields, and EPSG codes when a CRS is available.
    """
    from energyml.utils.data.crs import extract_crs_info
    from energyml.utils.introspection import get_object_metadata

    properties: Dict = dict(get_object_metadata(getattr(mesh, "energyml_object", None)))

    crs_obj = getattr(mesh, "crs_object", None)
    if isinstance(crs_obj, list):
        crs_obj = crs_obj[0] if crs_obj else None
    if crs_obj is not None:
        crs_info = extract_crs_info(crs_obj, workspace)
        if crs_info.projected_epsg_code is not None:
            properties["projected_epsg_code"] = crs_info.projected_epsg_code
        if crs_info.vertical_epsg_code is not None:
            properties["vertical_epsg_code"] = crs_info.vertical_epsg_code
    if getattr(mesh, "identifier", None):
        properties["identifier"] = mesh.identifier
    return properties


def _geojson_reproject_mesh(
    mesh: "AbstractMesh",
    workspace: Optional["EnergymlStorageInterface"] = None,
    use_network: bool = False,
    logger: Optional[Any] = None,
) -> Tuple["AbstractMesh", bool, Optional[int], Optional[int]]:
    """
    Return ``(mesh, is_wgs84, projected_epsg_code, vertical_epsg_code)`` where *mesh* is a shallow
    copy whose ``point_list`` has been reprojected to WGS84, or the original mesh when the
    reprojection is impossible (no EPSG code, pyproj missing, transformation error).

    The transform and its fallbacks live in :func:`~energyml.utils.data.crs.to_frame`; this
    function only adapts the legacy mesh container to it. It used to re-implement the whole
    degradation ladder (missing EPSG / missing pyproj / PROJ failure) a second time.
    """
    from dataclasses import replace

    from energyml.utils.data.crs import PointFrame, extract_crs_info, to_frame

    crs_obj = getattr(mesh, "crs_object", None)
    if isinstance(crs_obj, list):
        crs_obj = crs_obj[0] if crs_obj else None
    if crs_obj is None or mesh.point_list is None or len(mesh.point_list) == 0:
        return mesh, False, None, None

    crs_info = extract_crs_info(crs_obj, workspace)
    points = np.asarray(mesh.point_list, dtype=np.float64).reshape(-1, 3)
    framed = to_frame(
        points,
        crs_info,
        PointFrame.WGS84,
        getattr(mesh, "frame", PointFrame.PROJECTED),
        use_network=use_network,
        inplace=False,
    )

    if framed.frame is not PointFrame.WGS84:
        (logger or logging).warning(
            "GeoJSON export: coordinates are left in their source CRS (non RFC 7946 conformant) — %s",
            framed.degraded_reason or "unknown reason",
        )
        return mesh, False, crs_info.projected_epsg_code, crs_info.vertical_epsg_code

    return (
        replace(mesh, point_list=framed.points.tolist(), frame=framed.frame),
        True,
        crs_info.projected_epsg_code,
        crs_info.vertical_epsg_code,
    )


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
):
    """
    Stream a list of meshes as a GeoJSON FeatureCollection.

    :param out: output stream
    :param mesh_list: meshes to export
    :param obj_name: value of the ``name`` member of the collection
    :param properties: explicit per-mesh properties; when None (and :param:`include_metadata` is
                       True) they are built from the energyml object of each mesh (uuid,
                       qualified type, Citation fields, EPSG codes)
    :param global_properties: extra members written at the collection level
    :param logger:
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
    """
    # the source index is kept so that `properties` stays aligned on `mesh_list`
    exported: List[Tuple[int, AbstractMesh, Dict]] = []
    crs_states: set = set()

    for mesh_index, mesh in enumerate(mesh_list):
        if mesh.point_list is None or len(mesh.point_list) == 0:
            # write_geojson_feature() would write nothing for it; dropping it here keeps the
            # separator logic below exact (an empty mesh in last position used to leave a
            # trailing comma, which is not valid JSON).
            continue
        feature_properties: Dict = {}
        if include_metadata:
            feature_properties.update(_geojson_mesh_metadata(mesh, workspace))

        is_wgs84 = False
        projected_epsg_code = feature_properties.get("projected_epsg_code")
        vertical_epsg_code = feature_properties.get("vertical_epsg_code")
        if to_wgs84:
            mesh, is_wgs84, projected_epsg_code, vertical_epsg_code = _geojson_reproject_mesh(
                mesh, workspace=workspace, use_network=use_network, logger=logger
            )
        if is_wgs84:
            feature_properties["source_crs"] = f"EPSG:{projected_epsg_code}"
            feature_properties["coordinates_crs"] = "OGC:CRS84"
        crs_states.add((projected_epsg_code, vertical_epsg_code, is_wgs84))
        exported.append((mesh_index, mesh, feature_properties))

    ind = _JsonIndent(indent)

    out.write(b"{")
    out.write(ind.open())
    out.write(b'"type": "FeatureCollection"')
    if obj_name is not None:
        out.write(ind.sep())
        # json.dumps rather than a raw concatenation: a title may contain a quote
        out.write(f'"name": {json.dumps(obj_name)}'.encode())

    # A WGS84 document is implicitly in CRS84 and must not carry a 'crs' member (RFC 7946).
    not_wgs84 = [state for state in crs_states if not state[2] and state[0] is not None]
    if len(not_wgs84) == 1:
        for k, v in _geojson_crs_members(not_wgs84[0][0], not_wgs84[0][1]).items():
            out.write(ind.sep())
            out.write(f'"{k}": '.encode())
            out.write(_dumps_at_depth(v, ind))
    elif len(not_wgs84) > 1:
        (logger or logging).warning(
            f"GeoJSON export: {len(not_wgs84)} different source CRS in the same FeatureCollection — "
            "no collection-level CRS is declared, see the per-feature 'projected_epsg_code' property."
        )

    if global_properties is not None and len(global_properties) > 0:
        for k, v in global_properties.items():
            out.write(ind.sep())
            out.write(f"{json.dumps(k)}: ".encode())
            out.write(_dumps_at_depth(v, ind))

    out.write(ind.sep())
    out.write(b'"features": [')
    out.write(ind.open())

    cpt = 0
    point_offset = 0

    for mesh_index, mesh, feature_properties in exported:
        if cpt > 0:
            out.write(ind.sep())
        explicit = properties[mesh_index] if properties is not None and len(properties) > mesh_index else None
        write_geojson_feature(
            out=out,
            mesh=mesh,
            geo_type=mesh_to_geojson_type(mesh),
            # "AnyCrsFeature" keeps flagging the features whose coordinates are not WGS84
            geo_type_prefix="" if feature_properties.get("coordinates_crs") == "OGC:CRS84" else "AnyCrs",
            properties={**feature_properties, **(explicit or {})},
            feature_id=feature_properties.get("uuid"),
            point_offset=0,  # point_offset,
            logger=logger,
            indent=ind,
        )
        cpt += 1
        point_offset = point_offset + len(mesh.point_list)

    out.write(ind.close())
    out.write(b"]")  # end features
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
