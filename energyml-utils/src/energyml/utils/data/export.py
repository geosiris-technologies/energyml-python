# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Module for exporting mesh data to various file formats.

Supports OBJ, GeoJSON, VTK Legacy (ASCII + binary), VTK XML (.vtu / .vtp),
and STL formats.

Both the legacy :class:`AbstractMesh` hierarchy (``mesh.py``) and the
high-performance :class:`NumpyMesh` / :class:`NumpyMultiMesh` hierarchy
(``mesh_numpy.py``) are accepted by every export function.

CRS-displacement can be applied at export time (rather than at read time) by
passing ``use_crs_displacement=True`` (default) when a workspace is reachable
through the ``contexts`` dict.  The original ``NumpyMesh.points`` arrays are
**never mutated** — a copy is made whenever CRS needs to be applied.

Color metadata is sourced from :class:`RepresentationContext` objects keyed
by ``source_uuid``; if none are provided a default palette is used.
"""

from __future__ import annotations

import base64
import json
import logging
import struct
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, BinaryIO, Dict, List, Optional, TextIO, Union

import numpy as np

if TYPE_CHECKING:
    from energyml.utils.data.mesh import AbstractMesh
    from energyml.utils.data.mesh_numpy import (
        NumpyMesh,
        NumpyMultiMesh,
        NumpyPolylineMesh,
        NumpyPointSetMesh,
        NumpySurfaceMesh,
        NumpyVolumeMesh,
    )
    from energyml.utils.data.representation_context import RepresentationContext

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# VTK cell-type constants (subset)
# ---------------------------------------------------------------------------
_VTK_VERTEX = 1
_VTK_POLY_LINE = 4
_VTK_TRIANGLE = 5
_VTK_POLYGON = 7
_VTK_TETRA = 10
_VTK_HEXAHEDRON = 12

# ---------------------------------------------------------------------------
# Enumerations / option classes
# ---------------------------------------------------------------------------


class ExportFormat(Enum):
    """Supported mesh export formats."""

    OBJ = "obj"
    GEOJSON = "geojson"
    VTK = "vtk"
    VTU = "vtu"
    VTP = "vtp"
    STL = "stl"

    @classmethod
    def from_extension(cls, extension: str) -> "ExportFormat":
        """Get format from file extension."""
        ext = extension.lower().lstrip(".")
        for fmt in cls:
            if fmt.value == ext:
                return fmt
        raise ValueError(f"Unsupported file extension: {extension}")

    @classmethod
    def all_extensions(cls) -> List[str]:
        """Get all supported file extensions."""
        return [fmt.value for fmt in cls]


class ExportOptions:
    """Base class for export options."""


class STLExportOptions(ExportOptions):
    """Options for STL export."""

    def __init__(self, binary: bool = True, ascii_precision: int = 6):
        """
        :param binary: If True, export as binary STL; if False, export as ASCII STL.
        :param ascii_precision: Number of decimal places for ASCII format.
        """
        self.binary = binary
        self.ascii_precision = ascii_precision


class VTKFormat(Enum):
    """Sub-format selector for VTK export."""

    LEGACY_ASCII = "legacy_ascii"
    """VTK legacy format, ASCII encoding (version 3.0)."""

    LEGACY_BINARY = "legacy_binary"
    """VTK legacy format, big-endian binary encoding (version 3.0)."""

    VTU = "vtu"
    """VTK XML UnstructuredGrid (.vtu) — best for volumetric meshes."""

    VTP = "vtp"
    """VTK XML PolyData (.vtp) — best for surface / polyline meshes."""


class VTKExportOptions(ExportOptions):
    """Options for VTK export."""

    def __init__(
        self,
        vtk_format: VTKFormat = VTKFormat.LEGACY_ASCII,
        dataset_name: str = "mesh",
        # Legacy compatibility: binary=True is equivalent to vtk_format=VTKFormat.LEGACY_BINARY
        binary: bool = False,
    ):
        """
        :param vtk_format: VTK sub-format (legacy ASCII, legacy binary, VTU, VTP).
        :param dataset_name: Dataset name embedded in legacy VTK header or XML title.
        :param binary: Deprecated shorthand; when True, forces LEGACY_BINARY sub-format.
        """
        self.dataset_name = dataset_name
        if binary and vtk_format == VTKFormat.LEGACY_ASCII:
            # Honour the legacy binary=True flag so old call-sites still work.
            self.vtk_format = VTKFormat.LEGACY_BINARY
        else:
            self.vtk_format = vtk_format

    # Backward-compat property so code that reads ``options.binary`` still works.
    @property
    def binary(self) -> bool:
        return self.vtk_format == VTKFormat.LEGACY_BINARY


class GeoJSONExportOptions(ExportOptions):
    """Options for GeoJSON export."""

    def __init__(self, indent: Optional[int] = 2, properties: Optional[dict] = None):
        """
        :param indent: JSON indentation level (None for compact output).
        :param properties: Extra properties merged into every feature.
        """
        self.indent = indent
        self.properties = properties or {}


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _normalize_to_patches(meshes: Any) -> List[Any]:
    """Flatten *meshes* into a list of individual mesh patches.

    Handles:
    - :class:`NumpyMultiMesh` → calls ``flat_patches()``
    - Single :class:`NumpyMesh` → ``[mesh]``
    - ``list`` / ``tuple`` → recursive
    - :class:`AbstractMesh` → passthrough as ``[mesh]``
    """
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyMultiMesh

    if isinstance(meshes, NumpyMultiMesh):
        return meshes.flat_patches()
    if isinstance(meshes, NumpyMesh):
        return [meshes]
    if isinstance(meshes, (list, tuple)):
        result: List[Any] = []
        for m in meshes:
            result.extend(_normalize_to_patches(m))
        return result
    # AbstractMesh or unknown — pass through as single element
    return [meshes]


def _parse_vtk_flat_faces(flat: np.ndarray) -> List[np.ndarray]:
    """Decode VTK flat face array ``[nv, v0, …, nv, v0, …]`` into a list of
    per-face index arrays."""
    faces: List[np.ndarray] = []
    pos = 0
    flat = np.asarray(flat, dtype=np.int64)
    while pos < len(flat):
        nv = int(flat[pos])
        pos += 1
        if pos + nv > len(flat):
            break
        faces.append(flat[pos : pos + nv])
        pos += nv
    return faces


def _parse_vtk_flat_lines(flat: np.ndarray) -> List[np.ndarray]:
    """Decode VTK flat lines array ``[n, i0, i1, …, n, i0, …]`` into a list
    of per-line index arrays."""
    lines: List[np.ndarray] = []
    pos = 0
    flat = np.asarray(flat, dtype=np.int64)
    while pos < len(flat):
        n = int(flat[pos])
        pos += 1
        if pos + n > len(flat):
            break
        lines.append(flat[pos : pos + n])
        pos += n
    return lines


def _get_export_points(
    mesh: Any,
    use_crs_displacement: bool,
    workspace: Any = None,
) -> np.ndarray:
    """Return the point array for *mesh*, optionally applying CRS displacement.

    - For :class:`NumpyMesh`: if ``use_crs_displacement`` is True and a CRS
      object is present, returns a *copy* with CRS applied (never mutates the
      original ``mesh.points``).
    - For :class:`AbstractMesh` (legacy): returns ``mesh.point_list`` as-is;
      CRS was already applied by the reader.
    """
    from energyml.utils.data.mesh_numpy import NumpyMesh

    if isinstance(mesh, NumpyMesh):
        if use_crs_displacement and mesh.crs_object is not None and workspace is not None:
            from energyml.utils.data.crs import apply_from_crs_info, extract_crs_info

            crs = mesh.crs_object[0] if isinstance(mesh.crs_object, list) and mesh.crs_object else mesh.crs_object
            if crs is not None:
                try:
                    crs_info = extract_crs_info(crs, workspace)
                    pts = mesh.points.copy()
                    apply_from_crs_info(pts, crs_info, inplace=True)
                    return pts
                except Exception as exc:  # pragma: no cover
                    log.warning("CRS displacement failed for %s: %s", mesh.source_uuid, exc)
        return mesh.points
    # AbstractMesh — point_list is a list-of-lists; convert to ndarray for uniform handling
    return np.array(getattr(mesh, "point_list", []), dtype=np.float64)


def _get_context_color(
    source_uuid: Optional[str],
    contexts: Optional[Dict[str, Any]],
) -> Optional[tuple]:
    """Return an (r, g, b, a) tuple in 0–255 range for *source_uuid*, or None."""
    if not contexts or not source_uuid:
        return None
    ctx = contexts.get(source_uuid)
    if ctx is None:
        return None
    try:
        rendering = ctx.get_default_color()
        if rendering is not None and rendering.constant_color is not None:
            return rendering.constant_color.to_uint8()
    except Exception as exc:  # pragma: no cover
        log.debug("Failed to read color for %s: %s", source_uuid, exc)
    return None


def _workspace_from_contexts(contexts: Optional[Dict[str, Any]]) -> Any:
    """Return the workspace from the first available RepresentationContext."""
    if not contexts:
        return None
    for ctx in contexts.values():
        ws = getattr(ctx, "workspace", None)
        if ws is not None:
            return ws
    return None


def _get_faces_or_cells(mesh: Any) -> np.ndarray:
    """Return the face or cell connectivity array for a NumpyMesh.

    Uses ``mesh.faces`` when present and non-empty, then falls back to
    ``mesh.cells``.  Avoids the numpy-unsafe ``arr or other`` pattern which
    raises ``ValueError`` for arrays with more than one element.
    """
    faces = getattr(mesh, "faces", None)
    if faces is not None and len(faces) > 0:
        return faces
    cells = getattr(mesh, "cells", None)
    if cells is not None and len(cells) > 0:
        return cells
    return np.empty(0, dtype=np.int64)


# ---------------------------------------------------------------------------
# OBJ export
# ---------------------------------------------------------------------------


def export_obj(
    mesh_list: Any,
    out: BinaryIO,
    obj_name: Optional[str] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    mtl_out: Optional[BinaryIO] = None,
    use_crs_displacement: bool = True,
) -> None:
    """Export mesh data to Wavefront OBJ format.

    :param mesh_list: One or more meshes (``AbstractMesh``, ``NumpyMesh``,
        ``NumpyMultiMesh``, or a list thereof).
    :param out: Binary output stream for the ``.obj`` content.
    :param obj_name: Optional object name written to the OBJ header.
    :param contexts: Optional dict of :class:`RepresentationContext` keyed by
        ``source_uuid``; used to emit companion ``.mtl`` material colours when
        *mtl_out* is also provided.
    :param mtl_out: Optional binary stream for the companion ``.mtl`` file.
        Colour requires *contexts* to be supplied.
    :param use_crs_displacement: When True (default), CRS origin offset and
        axis transforms are applied to ``NumpyMesh`` points at export time.
    """
    from energyml.utils.data.mesh import PolylineSetMesh
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPointSetMesh, NumpyPolylineMesh

    patches = _normalize_to_patches(mesh_list)
    workspace = _workspace_from_contexts(contexts)

    out.write(b"# Generated by energyml-utils (Geosiris)\n\n")
    if obj_name is not None:
        out.write(f"o {obj_name}\n\n".encode())

    mtl_lib_name = obj_name or "materials"
    if mtl_out is not None:
        out.write(f"mtllib {mtl_lib_name}.mtl\n\n".encode())
        mtl_out.write(b"# MTL generated by energyml-utils\n\n")

    point_offset = 0

    for mesh in patches:
        pts = _get_export_points(mesh, use_crs_displacement, workspace)
        patch_label = getattr(mesh, "patch_label", None) or getattr(mesh, "identifier", None) or "mesh"
        source_uuid = getattr(mesh, "source_uuid", None) or getattr(mesh, "uuid", None)
        patch_idx = getattr(mesh, "patch_index", None)
        group_name = f"{source_uuid}_{patch_idx}" if source_uuid and patch_idx is not None else patch_label

        out.write(f"g {group_name}\n\n".encode())

        # emit material reference when mtl output is available
        if mtl_out is not None:
            mat_name = f"mat_{group_name}"
            color = _get_context_color(source_uuid, contexts)
            if color is None:
                color = (200, 200, 200, 255)
            r, g, b, _a = color
            out.write(f"usemtl {mat_name}\n".encode())
            mtl_out.write(f"newmtl {mat_name}\n".encode())
            mtl_out.write(f"Kd {r/255:.6f} {g/255:.6f} {b/255:.6f}\n\n".encode())

        # write vertices
        for pt in pts:
            out.write(f"v {pt[0]} {pt[1]} {pt[2]}\n".encode())

        # write connectivity
        if isinstance(mesh, NumpyMesh):
            if isinstance(mesh, NumpyPointSetMesh):
                # bare vertex elements
                for i in range(len(pts)):
                    out.write(f"p {i + point_offset + 1}\n".encode())
            elif isinstance(mesh, NumpyPolylineMesh):
                for seg in _parse_vtk_flat_lines(mesh.lines):
                    if len(seg) > 1:
                        idx_str = " ".join(str(i + point_offset + 1) for i in seg)
                        out.write(f"l {idx_str}\n".encode())
            else:
                # NumpySurfaceMesh (or NumpyVolumeMesh — export as faces)
                faces_arr = _get_faces_or_cells(mesh)
                for face in _parse_vtk_flat_faces(faces_arr):
                    if len(face) >= 3:
                        idx_str = " ".join(str(i + point_offset + 1) for i in face)
                        out.write(f"f {idx_str}\n".encode())
        else:
            # AbstractMesh legacy path
            indices = mesh.get_indices()
            elt = "l" if isinstance(mesh, PolylineSetMesh) else "f"
            for elem in indices:
                if len(elem) > 1:
                    idx_str = " ".join(str(i + point_offset + 1) for i in elem)
                    out.write(f"{elt} {idx_str}\n".encode())

        out.write(b"\n")
        point_offset += len(pts)


# ---------------------------------------------------------------------------
# GeoJSON export
# ---------------------------------------------------------------------------


def export_geojson(
    mesh_list: Any,
    out: TextIO,
    options: Optional[GeoJSONExportOptions] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
) -> None:
    """Export mesh data to GeoJSON FeatureCollection.

    :param mesh_list: One or more meshes.
    :param out: Text output stream.
    :param options: GeoJSON export options.
    :param contexts: Optional colour / metadata context dict.
    :param use_crs_displacement: Apply CRS displacement to ``NumpyMesh`` points.
    """
    from energyml.utils.data.mesh import PolylineSetMesh, SurfaceMesh
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPointSetMesh, NumpyPolylineMesh

    if options is None:
        options = GeoJSONExportOptions()

    patches = _normalize_to_patches(mesh_list)
    workspace = _workspace_from_contexts(contexts)
    features: List[dict] = []

    for mesh in patches:
        pts = _get_export_points(mesh, use_crs_displacement, workspace)
        source_uuid = getattr(mesh, "source_uuid", None)
        patch_idx = getattr(mesh, "patch_index", None)
        color = _get_context_color(source_uuid, contexts)
        base_props: dict = {
            **options.properties,
            "source_uuid": source_uuid,
            "patch_index": patch_idx,
        }
        if color:
            r, g, b, a = color
            base_props["color"] = f"#{r:02x}{g:02x}{b:02x}"
            base_props["opacity"] = round(a / 255.0, 4)

        if isinstance(mesh, NumpyMesh):
            if isinstance(mesh, NumpyPointSetMesh):
                coords = pts.tolist()
                features.append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "MultiPoint", "coordinates": coords},
                        "properties": base_props,
                    }
                )
            elif isinstance(mesh, NumpyPolylineMesh):
                for seg in _parse_vtk_flat_lines(mesh.lines):
                    if len(seg) < 2:
                        continue
                    coords = pts[seg].tolist()
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {"type": "LineString", "coordinates": coords},
                            "properties": base_props,
                        }
                    )
            else:
                # NumpySurfaceMesh / NumpyVolumeMesh
                for face in _parse_vtk_flat_faces(_get_faces_or_cells(mesh)):
                    if len(face) < 3:
                        continue
                    coords = pts[face].tolist()
                    coords.append(coords[0])  # close ring
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {"type": "Polygon", "coordinates": [coords]},
                            "properties": base_props,
                        }
                    )
        else:
            # AbstractMesh legacy path
            indices = mesh.get_indices()
            for elem_idx, elem in enumerate(indices):
                if isinstance(mesh, PolylineSetMesh):
                    if len(elem) < 2:
                        continue
                    coords = [list(pts[i]) for i in elem]
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {"type": "LineString", "coordinates": coords},
                            "properties": {**base_props, "element_index": elem_idx},
                        }
                    )
                elif isinstance(mesh, SurfaceMesh):
                    if len(elem) < 3:
                        continue
                    coords = [list(pts[i]) for i in elem]
                    coords.append(coords[0])
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {"type": "Polygon", "coordinates": [coords]},
                            "properties": {**base_props, "element_index": elem_idx},
                        }
                    )

    json.dump({"type": "FeatureCollection", "features": features}, out, indent=options.indent)


# ---------------------------------------------------------------------------
# VTK export — private helpers
# ---------------------------------------------------------------------------


def _b64_vtk(arr: np.ndarray) -> str:
    """Base64-encode a numpy array for VTK XML inline binary format.

    VTK prepends a 4-byte uint32 header with the byte count of the payload.
    """
    raw = arr.tobytes()
    header = struct.pack("<I", len(raw))
    return base64.b64encode(header + raw).decode("ascii")


def _vtk_xml_data_array(
    name: str,
    arr: np.ndarray,
    n_components: int = 1,
    vtk_type: str = "Int64",
) -> str:
    """Return a VTK XML ``<DataArray … />`` element string (base64 inline)."""
    return (
        f'<DataArray type="{vtk_type}" Name="{name}" '
        f'NumberOfComponents="{n_components}" format="binary">'
        f"{_b64_vtk(arr)}"
        f"</DataArray>"
    )


def _collect_vtk_geometry(
    patches: List[Any],
    use_crs_displacement: bool,
    workspace: Any,
) -> tuple:
    """Merge all patches into flat VTK geometry arrays.

    Returns:
        (all_pts, poly_conn, poly_off, line_conn, line_off,
         vert_conn, vert_off, cell_types, patch_meta)

    *patch_meta* is a list of ``(source_uuid, n_cells)`` tuples used to
    assign per-cell colour data.
    """
    from energyml.utils.data.mesh import PolylineSetMesh, SurfaceMesh
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPointSetMesh, NumpyPolylineMesh

    all_pts: List[np.ndarray] = []
    poly_conn: List[int] = []
    poly_off: List[int] = []
    line_conn: List[int] = []
    line_off: List[int] = []
    vert_conn: List[int] = []
    vert_off: List[int] = []
    cell_types: List[int] = []
    patch_meta: List[tuple] = []  # (source_uuid, cell_count)

    pt_offset = 0

    for mesh in patches:
        pts = _get_export_points(mesh, use_crs_displacement, workspace)
        all_pts.append(np.asarray(pts, dtype=np.float64).reshape(-1, 3))
        source_uuid = getattr(mesh, "source_uuid", None)
        cell_count = 0

        if isinstance(mesh, NumpyMesh):
            if isinstance(mesh, NumpyPointSetMesh):
                for i in range(len(pts)):
                    vert_conn.append(i + pt_offset)
                    vert_off.append(len(vert_conn))
                    cell_types.append(_VTK_VERTEX)
                    cell_count += 1
            elif isinstance(mesh, NumpyPolylineMesh):
                for seg in _parse_vtk_flat_lines(mesh.lines):
                    for vi in seg:
                        line_conn.append(int(vi) + pt_offset)
                    line_off.append(len(line_conn))
                    cell_types.append(_VTK_POLY_LINE)
                    cell_count += 1
            else:
                faces_arr = _get_faces_or_cells(mesh)
                for face in _parse_vtk_flat_faces(faces_arr):
                    nv = len(face)
                    for vi in face:
                        poly_conn.append(int(vi) + pt_offset)
                    poly_off.append(len(poly_conn))
                    cell_types.append(_VTK_TRIANGLE if nv == 3 else _VTK_POLYGON)
                    cell_count += 1
        else:
            # AbstractMesh legacy
            indices = mesh.get_indices()
            if isinstance(mesh, PolylineSetMesh):
                for line in indices:
                    for vi in line:
                        line_conn.append(int(vi) + pt_offset)
                    line_off.append(len(line_conn))
                    cell_types.append(_VTK_POLY_LINE)
                    cell_count += 1
            else:
                for face in indices:
                    nv = len(face)
                    for vi in face:
                        poly_conn.append(int(vi) + pt_offset)
                    poly_off.append(len(poly_conn))
                    cell_types.append(_VTK_TRIANGLE if nv == 3 else _VTK_POLYGON)
                    cell_count += 1

        pt_offset += len(pts)
        patch_meta.append((source_uuid, cell_count))

    merged_pts = np.concatenate(all_pts) if all_pts else np.empty((0, 3), dtype=np.float64)
    return (
        merged_pts,
        np.array(poly_conn, dtype=np.int64),
        np.array(poly_off, dtype=np.int64),
        np.array(line_conn, dtype=np.int64),
        np.array(line_off, dtype=np.int64),
        np.array(vert_conn, dtype=np.int64),
        np.array(vert_off, dtype=np.int64),
        np.array(cell_types, dtype=np.uint8),
        patch_meta,
    )


def _build_color_scalars(
    patch_meta: List[tuple],
    contexts: Optional[Dict[str, Any]],
    total_cells: int,
) -> Optional[np.ndarray]:
    """Build a ``(total_cells, 4)`` float32 RGBA array, or None when no colors found."""
    if not contexts:
        return None
    colors = np.full((total_cells, 4), 0.8, dtype=np.float32)
    colors[:, 3] = 1.0
    any_found = False
    cell_idx = 0
    for source_uuid, n_cells in patch_meta:
        rgba = _get_context_color(source_uuid, contexts)
        if rgba is not None:
            any_found = True
            r, g, b, a = rgba
            colors[cell_idx : cell_idx + n_cells, 0] = r / 255.0
            colors[cell_idx : cell_idx + n_cells, 1] = g / 255.0
            colors[cell_idx : cell_idx + n_cells, 2] = b / 255.0
            colors[cell_idx : cell_idx + n_cells, 3] = a / 255.0
        cell_idx += n_cells
    return colors if any_found else None


# ---------------------------------------------------------------------------
# VTK export — legacy (ASCII / binary)
# ---------------------------------------------------------------------------


def _export_vtk_legacy(
    patches: List[Any],
    out: BinaryIO,
    options: VTKExportOptions,
    contexts: Optional[Dict[str, Any]],
    workspace: Any,
) -> None:
    ascii_mode = options.vtk_format == VTKFormat.LEGACY_ASCII
    (
        all_pts,
        poly_conn,
        poly_off,
        line_conn,
        line_off,
        vert_conn,
        vert_off,
        cell_types,
        patch_meta,
    ) = _collect_vtk_geometry(patches, True, workspace)

    n_pts = len(all_pts)
    n_poly = len(poly_off)
    n_line = len(line_off)
    n_vert = len(vert_off)

    def _unflatten(conn: np.ndarray, offs: np.ndarray) -> List[List[int]]:
        result = []
        prev = 0
        for o in offs:
            result.append(conn[prev:o].tolist())
            prev = o
        return result

    polygons = _unflatten(poly_conn, poly_off)
    lines = _unflatten(line_conn, line_off)
    verts = _unflatten(vert_conn, vert_off)

    out.write(b"# vtk DataFile Version 3.0\n")
    out.write(f"{options.dataset_name}\n".encode())
    out.write(b"ASCII\n" if ascii_mode else b"BINARY\n")
    out.write(b"DATASET POLYDATA\n")

    if ascii_mode:
        out.write(f"POINTS {n_pts} float\n".encode())
        for pt in all_pts:
            out.write(f"{pt[0]} {pt[1]} {pt[2]}\n".encode())
    else:
        out.write(f"POINTS {n_pts} float\n".encode())
        out.write(all_pts.astype(">f4").tobytes())
        out.write(b"\n")

    def _write_section(name: str, cells: List[List[int]]) -> None:
        if not cells:
            return
        total = sum(len(c) + 1 for c in cells)
        out.write(f"{name} {len(cells)} {total}\n".encode())
        if ascii_mode:
            for c in cells:
                out.write(f"{len(c)} {' '.join(str(i) for i in c)}\n".encode())
        else:
            for c in cells:
                row = np.array([len(c)] + c, dtype=np.int32).byteswap().astype(">i4")
                out.write(row.tobytes())
            out.write(b"\n")

    _write_section("POLYGONS", polygons)
    _write_section("LINES", lines)
    _write_section("VERTICES", verts)

    total_cells = n_poly + n_line + n_vert
    if total_cells > 0 and contexts:
        colors = _build_color_scalars(patch_meta, contexts, total_cells)
        if colors is not None:
            out.write(f"CELL_DATA {total_cells}\n".encode())
            out.write(b"COLOR_SCALARS patch_color 4\n")
            if ascii_mode:
                for row in colors:
                    out.write(f"{row[0]:.6f} {row[1]:.6f} {row[2]:.6f} {row[3]:.6f}\n".encode())
            else:
                out.write(colors.astype(">f4").tobytes())
                out.write(b"\n")


# ---------------------------------------------------------------------------
# VTK export — XML VTU
# ---------------------------------------------------------------------------


def _export_vtk_vtu(
    patches: List[Any],
    out: BinaryIO,
    options: VTKExportOptions,
    contexts: Optional[Dict[str, Any]],
    workspace: Any,
) -> None:
    """Write VTK XML UnstructuredGrid (.vtu)."""
    (
        all_pts,
        poly_conn,
        poly_off,
        line_conn,
        line_off,
        vert_conn,
        vert_off,
        cell_types,
        patch_meta,
    ) = _collect_vtk_geometry(patches, True, workspace)

    # Build a single merged connectivity / offsets / types for UnstructuredGrid.
    conn_parts: List[np.ndarray] = []
    off_parts: List[int] = []
    types_list: List[int] = []
    running = 0

    def _add_vtu_section(conn: np.ndarray, offs: np.ndarray, default_type: int) -> None:
        nonlocal running
        prev = 0
        for o in offs:
            seg = conn[prev:o]
            conn_parts.append(seg)
            running += len(seg)
            off_parts.append(running)
            types_list.append(default_type)
            prev = o

    _add_vtu_section(vert_conn, vert_off, _VTK_VERTEX)
    _add_vtu_section(line_conn, line_off, _VTK_POLY_LINE)

    # Polygons: honour per-cell type from cell_types array (triangle vs polygon).
    n_verts_cells = len(vert_off)
    n_lines_cells = len(line_off)
    prev = 0
    for poly_i, o in enumerate(poly_off):
        seg = poly_conn[prev:o]
        conn_parts.append(seg)
        running += len(seg)
        off_parts.append(running)
        abs_idx = n_verts_cells + n_lines_cells + poly_i
        types_list.append(int(cell_types[abs_idx]) if abs_idx < len(cell_types) else _VTK_POLYGON)
        prev = o

    all_conn = (
        np.concatenate([np.asarray(p, dtype=np.int64) for p in conn_parts])
        if conn_parts
        else np.empty(0, dtype=np.int64)
    )
    all_off = np.array(off_parts, dtype=np.int64)
    all_types = np.array(types_list, dtype=np.uint8)
    n_cells = len(all_types)
    n_pts = len(all_pts)

    xml_lines: List[str] = [
        '<?xml version="1.0"?>',
        '<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">',
        "  <UnstructuredGrid>",
        f'    <Piece NumberOfPoints="{n_pts}" NumberOfCells="{n_cells}">',
        "      <Points>",
        "        " + _vtk_xml_data_array("Points", all_pts.astype(np.float32).ravel(), 3, "Float32"),
        "      </Points>",
        "      <Cells>",
        "        " + _vtk_xml_data_array("connectivity", all_conn, 1, "Int64"),
        "        " + _vtk_xml_data_array("offsets", all_off, 1, "Int64"),
        "        " + _vtk_xml_data_array("types", all_types, 1, "UInt8"),
        "      </Cells>",
    ]

    if contexts and n_cells > 0:
        colors = _build_color_scalars(patch_meta, contexts, n_cells)
        if colors is not None:
            xml_lines.append("      <CellData>")
            xml_lines.append("        " + _vtk_xml_data_array("patch_color", colors.ravel(), 4, "Float32"))
            xml_lines.append("      </CellData>")

    xml_lines += ["    </Piece>", "  </UnstructuredGrid>", "</VTKFile>"]
    out.write("\n".join(xml_lines).encode("utf-8"))


# ---------------------------------------------------------------------------
# VTK export — XML VTP
# ---------------------------------------------------------------------------


def _export_vtk_vtp(
    patches: List[Any],
    out: BinaryIO,
    options: VTKExportOptions,
    contexts: Optional[Dict[str, Any]],
    workspace: Any,
) -> None:
    """Write VTK XML PolyData (.vtp)."""
    (
        all_pts,
        poly_conn,
        poly_off,
        line_conn,
        line_off,
        vert_conn,
        vert_off,
        cell_types,
        patch_meta,
    ) = _collect_vtk_geometry(patches, True, workspace)

    n_pts = len(all_pts)
    n_polys = len(poly_off)
    n_lines = len(line_off)
    n_verts = len(vert_off)
    total_cells = n_polys + n_lines + n_verts

    xml_lines: List[str] = [
        '<?xml version="1.0"?>',
        '<VTKFile type="PolyData" version="0.1" byte_order="LittleEndian">',
        "  <PolyData>",
        (
            f'    <Piece NumberOfPoints="{n_pts}" NumberOfPolys="{n_polys}" '
            f'NumberOfLines="{n_lines}" NumberOfVerts="{n_verts}">'
        ),
        "      <Points>",
        "        " + _vtk_xml_data_array("Points", all_pts.astype(np.float32).ravel(), 3, "Float32"),
        "      </Points>",
    ]

    def _topo_section(tag: str, conn: np.ndarray, offs: np.ndarray) -> List[str]:
        return [
            f"      <{tag}>",
            "        " + _vtk_xml_data_array("connectivity", conn, 1, "Int64"),
            "        " + _vtk_xml_data_array("offsets", offs, 1, "Int64"),
            f"      </{tag}>",
        ]

    if n_polys:
        xml_lines.extend(_topo_section("Polys", poly_conn, poly_off))
    if n_lines:
        xml_lines.extend(_topo_section("Lines", line_conn, line_off))
    if n_verts:
        xml_lines.extend(_topo_section("Verts", vert_conn, vert_off))

    if contexts and total_cells > 0:
        colors = _build_color_scalars(patch_meta, contexts, total_cells)
        if colors is not None:
            xml_lines.append("      <CellData>")
            xml_lines.append("        " + _vtk_xml_data_array("patch_color", colors.ravel(), 4, "Float32"))
            xml_lines.append("      </CellData>")

    xml_lines += ["    </Piece>", "  </PolyData>", "</VTKFile>"]
    out.write("\n".join(xml_lines).encode("utf-8"))


# ---------------------------------------------------------------------------
# VTK export — public entry point
# ---------------------------------------------------------------------------


def export_vtk(
    mesh_list: Any,
    out: BinaryIO,
    options: Optional[VTKExportOptions] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
) -> None:
    """Export mesh data to a VTK format.

    The sub-format is controlled by ``options.vtk_format`` (default:
    ``VTKFormat.LEGACY_ASCII``).  Supported variants:

    * **LEGACY_ASCII** — VTK 3.0 POLYDATA, ASCII encoding
    * **LEGACY_BINARY** — VTK 3.0 POLYDATA, big-endian binary encoding
    * **VTU** — VTK XML UnstructuredGrid (``.vtu``), base64 inline binary
    * **VTP** — VTK XML PolyData (``.vtp``), base64 inline binary

    :param mesh_list: Meshes to export.
    :param out: Binary output stream.
    :param options: VTK export options.
    :param contexts: Optional colour context dict keyed by ``source_uuid``.
    :param use_crs_displacement: Apply CRS displacement to ``NumpyMesh`` points.
    """
    if options is None:
        options = VTKExportOptions()

    patches = _normalize_to_patches(mesh_list)
    # Pass workspace only when CRS displacement is actually requested.
    workspace = _workspace_from_contexts(contexts) if use_crs_displacement else None

    fmt = options.vtk_format
    if fmt in (VTKFormat.LEGACY_ASCII, VTKFormat.LEGACY_BINARY):
        _export_vtk_legacy(patches, out, options, contexts, workspace)
    elif fmt == VTKFormat.VTU:
        _export_vtk_vtu(patches, out, options, contexts, workspace)
    elif fmt == VTKFormat.VTP:
        _export_vtk_vtp(patches, out, options, contexts, workspace)
    else:  # pragma: no cover
        raise ValueError(f"Unknown VTKFormat: {fmt}")


# ---------------------------------------------------------------------------
# STL export
# ---------------------------------------------------------------------------


def export_stl(
    mesh_list: Any,
    out: BinaryIO,
    options: Optional[STLExportOptions] = None,
    use_crs_displacement: bool = True,
) -> None:
    """Export triangulated mesh data to STL format (binary or ASCII).

    Non-triangular polygons are fan-triangulated (vertex 0 + consecutive pairs).
    Polylines and point sets are silently skipped.

    :param mesh_list: Meshes to export.
    :param out: Binary output stream.
    :param options: STL export options.
    :param use_crs_displacement: Apply CRS displacement to ``NumpyMesh`` points.
    """
    from energyml.utils.data.mesh import SurfaceMesh
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPolylineMesh, NumpyPointSetMesh

    if options is None:
        options = STLExportOptions(binary=True)

    patches = _normalize_to_patches(mesh_list)
    # STL carries no colour / context; workspace not needed unless CRS is requested.
    workspace = None  # CRS requires a workspace — callers may read with CRS pre-applied.

    all_triangles: List[tuple] = []

    for mesh in patches:
        if isinstance(mesh, (NumpyPolylineMesh, NumpyPointSetMesh)):
            continue  # STL is surface-only
        pts = _get_export_points(mesh, use_crs_displacement, workspace)
        pts_np = np.asarray(pts, dtype=np.float64).reshape(-1, 3)

        if isinstance(mesh, NumpyMesh):
            face_list = _parse_vtk_flat_faces(_get_faces_or_cells(mesh))
        else:
            if not isinstance(mesh, SurfaceMesh):
                continue
            face_list = mesh.get_indices()

        for face in face_list:
            face = list(face)
            if len(face) < 3:
                continue
            if len(face) == 3:
                all_triangles.append((pts_np[face[0]], pts_np[face[1]], pts_np[face[2]]))
            else:
                # Fan triangulation for quads and polygons
                for j in range(1, len(face) - 1):
                    all_triangles.append((pts_np[face[0]], pts_np[face[j]], pts_np[face[j + 1]]))

    if options.binary:
        _export_stl_binary(all_triangles, out)
    else:
        _export_stl_ascii(all_triangles, out, options.ascii_precision)


def _compute_normal(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    v1, v2 = p1 - p0, p2 - p0
    n = np.cross(v1, v2)
    norm = np.linalg.norm(n)
    return n / norm if norm > 0 else np.zeros(3)


def _export_stl_binary(triangles: List[tuple], out: BinaryIO) -> None:
    header = b"Binary STL file generated by energyml-utils" + b"\0" * (80 - 44)
    out.write(header)
    out.write(struct.pack("<I", len(triangles)))
    for p0, p1, p2 in triangles:
        normal = _compute_normal(p0, p1, p2)
        out.write(struct.pack("<fff", *normal.tolist()))
        for pt in (p0, p1, p2):
            out.write(struct.pack("<fff", float(pt[0]), float(pt[1]), float(pt[2])))
        out.write(struct.pack("<H", 0))


def _export_stl_ascii(triangles: List[tuple], out: BinaryIO, precision: int) -> None:
    out.write(b"solid mesh\n")
    for p0, p1, p2 in triangles:
        normal = _compute_normal(p0, p1, p2)
        out.write(
            f"  facet normal {normal[0]:.{precision}e} {normal[1]:.{precision}e} {normal[2]:.{precision}e}\n".encode()
        )
        out.write(b"    outer loop\n")
        for pt in (p0, p1, p2):
            out.write(f"      vertex {pt[0]:.{precision}e} {pt[1]:.{precision}e} {pt[2]:.{precision}e}\n".encode())
        out.write(b"    endloop\n  endfacet\n")
    out.write(b"endsolid mesh\n")


# ---------------------------------------------------------------------------
# High-level dispatcher
# ---------------------------------------------------------------------------


def export_mesh(
    mesh_list: Any,
    output_path: Union[str, Path],
    format: Optional[ExportFormat] = None,
    options: Optional[ExportOptions] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
) -> None:
    """Export mesh data to a file.

    Format is auto-detected from the file extension when *format* is None.
    Supported extensions: ``.obj``, ``.geojson``, ``.vtk``, ``.vtu``,
    ``.vtp``, ``.stl``.

    :param mesh_list: Meshes to export.
    :param output_path: Destination file path.
    :param format: Explicit format; auto-detected from extension when None.
    :param options: Format-specific options.
    :param contexts: Color / metadata context dict.
    :param use_crs_displacement: Apply CRS displacement to ``NumpyMesh`` points.
    """
    path = Path(output_path)
    if format is None:
        format = ExportFormat.from_extension(path.suffix)

    if format == ExportFormat.GEOJSON:
        with path.open("w", encoding="utf-8") as f:
            export_geojson(mesh_list, f, options, contexts, use_crs_displacement)
        return

    # All remaining formats use binary streams
    with path.open("wb") as f:
        if format == ExportFormat.OBJ:
            if contexts:
                mtl_path = path.with_suffix(".mtl")
                with mtl_path.open("wb") as mf:
                    export_obj(mesh_list, f, path.stem, contexts, mf, use_crs_displacement)
            else:
                export_obj(mesh_list, f, path.stem, None, None, use_crs_displacement)
        elif format == ExportFormat.STL:
            export_stl(mesh_list, f, options, use_crs_displacement)
        elif format == ExportFormat.VTK:
            export_vtk(mesh_list, f, options, contexts, use_crs_displacement)
        elif format == ExportFormat.VTU:
            vtk_opts = options if isinstance(options, VTKExportOptions) else VTKExportOptions()
            vtk_opts.vtk_format = VTKFormat.VTU
            export_vtk(mesh_list, f, vtk_opts, contexts, use_crs_displacement)
        elif format == ExportFormat.VTP:
            vtk_opts = options if isinstance(options, VTKExportOptions) else VTKExportOptions()
            vtk_opts.vtk_format = VTKFormat.VTP
            export_vtk(mesh_list, f, vtk_opts, contexts, use_crs_displacement)
        else:
            raise ValueError(f"Unsupported format: {format}")


# ---------------------------------------------------------------------------
# UI Helper Functions
# ---------------------------------------------------------------------------


def supported_formats() -> List[str]:
    """Return all supported export format extensions."""
    return ExportFormat.all_extensions()


def format_description(format: Union[str, ExportFormat]) -> str:
    """Return a human-readable description of *format*."""
    if isinstance(format, str):
        format = ExportFormat.from_extension(format)
    descriptions = {
        ExportFormat.OBJ: "Wavefront OBJ — 3D geometry with optional .mtl colour",
        ExportFormat.GEOJSON: "GeoJSON — geographic data (lines, polygons, point clouds)",
        ExportFormat.VTK: "VTK Legacy (ASCII or binary) — POLYDATA format",
        ExportFormat.VTU: "VTK XML UnstructuredGrid (.vtu) — volumes + mixed topologies",
        ExportFormat.VTP: "VTK XML PolyData (.vtp) — surfaces and polylines",
        ExportFormat.STL: "STL — stereolithography (triangles only)",
    }
    return descriptions.get(format, "Unknown format")


def format_filter_string(format: Union[str, ExportFormat]) -> str:
    """Return a file-dialog filter string (e.g. ``"VTU Files (*.vtu)"``)."""
    if isinstance(format, str):
        format = ExportFormat.from_extension(format)
    filters = {
        ExportFormat.OBJ: "OBJ Files (*.obj)",
        ExportFormat.GEOJSON: "GeoJSON Files (*.geojson)",
        ExportFormat.VTK: "VTK Files (*.vtk)",
        ExportFormat.VTU: "VTK XML UnstructuredGrid Files (*.vtu)",
        ExportFormat.VTP: "VTK XML PolyData Files (*.vtp)",
        ExportFormat.STL: "STL Files (*.stl)",
    }
    return filters.get(format, "All Files (*.*)")


def all_formats_filter_string() -> str:
    """Return a ``;;``-joined filter string for all supported formats."""
    return ";;".join(format_filter_string(fmt) for fmt in ExportFormat)


def get_format_options_class(format: Union[str, ExportFormat]) -> Optional[type]:
    """Return the options class for *format*, or None."""
    if isinstance(format, str):
        format = ExportFormat.from_extension(format)
    return {
        ExportFormat.STL: STLExportOptions,
        ExportFormat.VTK: VTKExportOptions,
        ExportFormat.VTU: VTKExportOptions,
        ExportFormat.VTP: VTKExportOptions,
        ExportFormat.GEOJSON: GeoJSONExportOptions,
    }.get(format)


def supports_lines(format: Union[str, ExportFormat]) -> bool:
    """Return True when *format* can represent polyline primitives."""
    if isinstance(format, str):
        format = ExportFormat.from_extension(format)
    return format in {ExportFormat.OBJ, ExportFormat.GEOJSON, ExportFormat.VTK, ExportFormat.VTU, ExportFormat.VTP}


def supports_triangles(format: Union[str, ExportFormat]) -> bool:
    """Return True when *format* can represent triangle / polygon primitives."""
    return True  # All formats support triangles


def supports_pointsets(format: Union[str, ExportFormat]) -> bool:
    """Return True when *format* can represent point-cloud primitives."""
    if isinstance(format, str):
        format = ExportFormat.from_extension(format)
    return format in {ExportFormat.OBJ, ExportFormat.GEOJSON, ExportFormat.VTK, ExportFormat.VTU, ExportFormat.VTP}
