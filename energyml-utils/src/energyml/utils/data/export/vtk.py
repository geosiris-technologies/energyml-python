# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""VTK export: legacy POLYDATA (ASCII / binary) and XML (.vtu / .vtp)."""

from __future__ import annotations

import base64
import logging
import struct
from typing import TYPE_CHECKING, Any, Dict, List, Optional, BinaryIO

import numpy as np

from energyml.utils.data.export._base import (
    ExportFormat,
    resolve_origin_shift,
    VTKExportOptions,
    VTKFormat,
    _VTK_POLYGON,
    _VTK_POLY_LINE,
    _VTK_TRIANGLE,
    _VTK_VERTEX,
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
    from energyml.utils.data.representation_context import RepresentationContext

log = logging.getLogger(__name__)

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
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    use_network: bool = False,
) -> tuple:
    """Merge all patches into flat VTK geometry arrays.

    Returns:
        (all_pts, poly_conn, poly_off, line_conn, line_off,
         vert_conn, vert_off, cell_types, patch_meta)

    *patch_meta* is a list of ``(source_uuid, n_cells)`` tuples used to
    assign per-cell colour data.
    """
    from energyml.utils.data.mesh import PolylineSetMesh
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
        pts, _pts_frame, _ = _get_export_points(mesh, use_crs_displacement, workspace, frame, origin_shift, use_network)
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
    frame: Optional["PointFrame"] = None,
    _origin_shift: Optional[Any] = None,
    use_network: bool = False,
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
    ) = _collect_vtk_geometry(patches, True, workspace, frame, _origin_shift, use_network)

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
    frame: Optional["PointFrame"] = None,
    _origin_shift: Optional[Any] = None,
    use_network: bool = False,
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
    ) = _collect_vtk_geometry(patches, True, workspace, frame, _origin_shift, use_network)

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
    frame: Optional["PointFrame"] = None,
    _origin_shift: Optional[Any] = None,
    use_network: bool = False,
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
    ) = _collect_vtk_geometry(patches, True, workspace, frame, _origin_shift, use_network)

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
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    use_network: bool = False,
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
    _origin_shift = resolve_origin_shift(patches, use_crs_displacement, workspace, frame, origin_shift, use_network)

    fmt = options.vtk_format
    if fmt in (VTKFormat.LEGACY_ASCII, VTKFormat.LEGACY_BINARY):
        _export_vtk_legacy(patches, out, options, contexts, workspace, frame, _origin_shift, use_network)
    elif fmt == VTKFormat.VTU:
        _export_vtk_vtu(patches, out, options, contexts, workspace, frame, _origin_shift, use_network)
    elif fmt == VTKFormat.VTP:
        _export_vtk_vtp(patches, out, options, contexts, workspace, frame, _origin_shift, use_network)
    else:  # pragma: no cover
        raise ValueError(f"Unknown VTKFormat: {fmt}")


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def _write(
    mesh_list: Any,
    out: BinaryIO,
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
    export_vtk(
        mesh_list,
        out,
        options,
        contexts,
        use_crs_displacement,
        frame=frame,
        origin_shift=origin_shift,
    )


for _fmt, _label, _desc, _sub in (
    (
        ExportFormat.VTK,
        "VTK Files (*.vtk)",
        "VTK Legacy (ASCII or binary) — POLYDATA format",
        None,
    ),
    (
        ExportFormat.VTU,
        "VTK XML UnstructuredGrid Files (*.vtu)",
        "VTK XML UnstructuredGrid (.vtu) — volumes + mixed topologies",
        VTKFormat.VTU,
    ),
    (
        ExportFormat.VTP,
        "VTK XML PolyData Files (*.vtp)",
        "VTK XML PolyData (.vtp) — surfaces and polylines",
        VTKFormat.VTP,
    ),
):
    # .vtu / .vtp share this writer and only pin its sub-format, which the registry applies
    # through force_options instead of an extra branch in the dispatcher.
    register_format(
        FormatSpec(
            format=_fmt,
            description=_desc,
            filter_label=_label,
            writer=_write,
            binary=True,
            options_class=VTKExportOptions,
            force_options={"vtk_format": _sub} if _sub is not None else None,
        )
    )
