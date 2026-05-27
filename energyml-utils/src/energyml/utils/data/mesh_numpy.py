# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""Optimised, zero-copy-first EPC/HDF5 3-D object reader.

This module is a high-performance companion to :mod:`mesh.py`. It keeps the
same ``read_<type>(energyml_object, workspace)`` dispatcher philosophy but
always returns :class:`NumpyMultiMesh` containers whose geometry arrays are
:class:`numpy.ndarray` objects (never plain Python lists).

Design goals
------------
* **No list conversion** - no ``.tolist()`` calls anywhere.  Arrays stay as
  numpy throughout.
* **Best-effort zero-copy** - geometry is read via
  :meth:`EnergymlStorageInterface.read_array_view`.  For contiguous,
  uncompressed HDF5 datasets this returns a numpy view backed directly by the
  memory-mapped file buffer (no RAM copy).  Chunked / compressed datasets fall
  back silently to a copy.
* **PyVista-ready connectivity** - ``faces`` / ``lines`` / ``cells`` arrays
  use the VTK flat-count-prefixed format consumed directly by
  ``pyvista.PolyData`` and ``pyvista.UnstructuredGrid`` without additional
  allocation.
* **Patch-level control** - every representation is returned as a
  :class:`NumpyMultiMesh` container.  Each RESQML patch becomes a separate
  :class:`NumpyMesh` entry in ``NumpyMultiMesh.patches``, carrying
  ``patch_index``, ``patch_label``, ``source_uuid``, and ``source_type``
  metadata.  ``RepresentationSetRepresentation`` members are stored as nested
  ``NumpyMultiMesh.children`` so visibility can be toggled per-child in
  PyVista ``MultiBlock`` viewers.
* **Backward compatible** - :mod:`mesh.py` is untouched; both modules can be
  used side by side.

Usage
-----
>>> from energyml.utils.epc import Epc
>>> from energyml.utils.data.mesh_numpy import read_numpy_mesh_object, numpy_multi_mesh_to_pyvista
>>> epc = Epc.read_file("my_model.epc")
>>> obj = epc.get_object_by_uuid("...")[0]
>>> multi = read_numpy_mesh_object(obj, workspace=epc, use_crs_displacement=True)
>>> block = numpy_multi_mesh_to_pyvista(multi)   # pyvista.MultiBlock
>>> block.plot()
"""
from __future__ import annotations

import inspect
import logging
import re
import sys
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np

from energyml.utils.data.helper import (
    apply_crs_transform,
    evaluate_parametric_line_array,
    generate_vertical_well_points,
    get_crs_offsets_and_angle,
    get_crs_obj,
    get_crs_origin_offset,
    get_datum_information,
    is_z_reversed,
    read_array,
    read_grid2d_patch,
    read_parametric_geometry,
    resolve_parametric_line_array,
    get_wellbore_points,
)
from energyml.utils.data.crs import extract_crs_info, apply_from_crs_info
from energyml.utils.exception import NotSupportedError, ObjectNotFoundNotError
from energyml.utils.introspection import (
    get_obj_uri,
    get_obj_uuid,
    get_object_attribute,
    search_attribute_matching_name,
    search_attribute_matching_name_with_path,
    snake_case,
)
from energyml.utils.storage_interface import EnergymlStorageInterface

# ---------------------------------------------------------------------------
# Internal helper: thin proxy that makes read_array_view look like read_array
# so that helper.read_array benefits from zero-copy semantics transparently.
# ---------------------------------------------------------------------------


class _ViewWorkspace:
    """Transparent proxy that routes ``read_array`` → ``read_array_view``.

    ``helper.read_array`` internally calls ``workspace.read_array``.  By
    wrapping the real workspace with this proxy we redirect those calls to
    :meth:`read_array_view` without touching ``helper.py``.  All other
    attribute accesses are forwarded as-is.
    """

    __slots__ = ("_ws",)

    def __init__(self, ws: EnergymlStorageInterface) -> None:
        self._ws = ws

    def __getattr__(self, name: str) -> Any:
        return getattr(self._ws, name)

    def read_array(  # noqa: D102 - mirrors EnergymlStorageInterface
        self,
        proxy: Any,
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        return self._ws.read_array_view(proxy, path_in_external, start_indices, counts, external_uri)


def _view_workspace(workspace: Optional[EnergymlStorageInterface]) -> Optional[Any]:
    """Wrap *workspace* in ``_ViewWorkspace`` when available, else return as-is."""
    if workspace is None:
        return None
    if isinstance(workspace, _ViewWorkspace):
        return workspace
    return _ViewWorkspace(workspace)


# ---------------------------------------------------------------------------
# Dataclass hierarchy
# ---------------------------------------------------------------------------


@dataclass
class NumpyMesh:
    """Base class for all numpy-backed mesh objects.

    Subclasses guarantee:
    * ``points``  - shape ``(N, 3)``,  dtype ``float64``
    * Connectivity arrays - dtype ``int64``, VTK flat format
    """

    energyml_object: Any = field(default=None)
    crs_object: Any = field(default=None)
    identifier: str = field(default="")
    #: Points array, shape (N, 3), dtype float64.  May be a numpy view.
    points: np.ndarray = field(default_factory=lambda: np.empty((0, 3), dtype=np.float64))
    #: Index of this patch within the source representation (0-based).
    patch_index: Optional[int] = field(default=None)
    #: Human-readable label for this patch.
    patch_label: Optional[str] = field(default=None)
    #: UUID of the source RESQML object that produced this patch.
    source_uuid: Optional[str] = field(default=None)
    #: Python class name of the source RESQML object.
    source_type: Optional[str] = field(default=None)
    #: Optional named arrays attached to this mesh (e.g. ``node_time_values``).
    extra_arrays: Dict[str, np.ndarray] = field(default_factory=dict)

    def to_pyvista(self) -> Any:  # return type: pv.DataSet
        """Convert to a PyVista dataset.  Requires ``pyvista`` to be installed."""
        return numpy_mesh_to_pyvista(self)


@dataclass
class NumpyPointSetMesh(NumpyMesh):
    """A cloud of unconnected points."""


@dataclass
class NumpyPolylineMesh(NumpyMesh):
    """A set of poly-lines.

    ``lines`` uses the VTK flat format:
    ``[n0, i0, i1, …, n1, j0, j1, …]`` where *n* is the vertex count of that
    line.  Can be passed directly to ``pyvista.PolyData(points, lines=lines)``.
    """

    lines: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=np.int64))


@dataclass
class NumpySurfaceMesh(NumpyMesh):
    """A triangulated or quad surface.

    ``faces`` uses the VTK flat format:
    ``[nv0, v0, v1, v2, nv1, v0, v1, v2, …]``.  Can be passed directly to
    ``pyvista.PolyData(points, faces=faces)``.
    """

    faces: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=np.int64))


@dataclass
class NumpyVolumeMesh(NumpyMesh):
    """A volumetric mesh (hexahedral, polyhedral, …).

    ``cells`` - VTK flat format, ``cell_types`` - uint8 VTK cell-type codes.
    ``pyvista.UnstructuredGrid(cells, cell_types, points)`` accepts them
    directly.
    """

    cells: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=np.int64))
    cell_types: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=np.uint8))


@dataclass
class NumpyMultiMesh:
    """Container for one or more :class:`NumpyMesh` patches from a single
    energyml representation, plus optional nested child containers for
    ``RepresentationSetRepresentation``.

    Hierarchy
    ---------
    * **patches** — flat list of :class:`NumpyMesh` subclass instances
      produced directly by this representation (one per RESQML patch).
    * **children** — nested :class:`NumpyMultiMesh` instances; populated only
      by :func:`read_numpy_representation_set_representation` (one child per
      member representation).

    The design is intentionally shallow: at most 2 levels (container →
    patches) except for ``RepresentationSet`` which adds one extra level.
    """

    energyml_object: Any = field(default=None)
    identifier: str = field(default="")
    #: UUID of the source energyml object.
    source_uuid: Optional[str] = field(default=None)
    #: Python class name of the source energyml object.
    source_type: Optional[str] = field(default=None)
    #: Ordered list of patches produced by reading this representation.
    patches: List["NumpyMesh"] = field(default_factory=list)
    #: Child containers (only for RepresentationSetRepresentation).
    children: List["NumpyMultiMesh"] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def patch_count(self) -> int:
        """Total number of leaf patches (recursive across children)."""
        return len(self.patches) + sum(c.patch_count() for c in self.children)

    def flat_patches(self) -> List["NumpyMesh"]:
        """Return all leaf patches in depth-first order."""
        result: List[NumpyMesh] = list(self.patches)
        for child in self.children:
            result.extend(child.flat_patches())
        return result

    def flat_children(self) -> List["NumpyMultiMesh"]:
        """Return all child containers in depth-first order."""
        result: List[NumpyMultiMesh] = list(self.children)
        for child in self.children:
            result.extend(child.flat_children())
        return result

    def to_pyvista(self) -> Any:  # return type: pv.MultiBlock
        """Convert to a PyVista ``MultiBlock``.  Requires ``pyvista``."""
        return numpy_multi_mesh_to_pyvista(self)


# ---------------------------------------------------------------------------
# CRS displacement (vectorised)
# ---------------------------------------------------------------------------


def crs_displacement_np(
    points: np.ndarray,
    crs_obj: Any,
    *,
    inplace: bool = True,
) -> np.ndarray:
    """Apply CRS origin offset and optional Z-axis inversion to *points*.

    Operates on an ``(N, 3)`` numpy array using broadcast arithmetic — no
    Python-level loops.  Prefer :func:`apply_from_crs_info` for full CRS
    transforms (rotation, axis-order swap, etc.).

    Args:
        points: Shape ``(N, 3)``, dtype ``float64``.  Modified in-place when
                *inplace* is ``True`` (default).
        crs_obj:  CRS object exposing the same attributes as accepted by
                  :func:`helper.get_crs_origin_offset` and
                  :func:`helper.is_z_reversed`.
        inplace:  When ``False`` a copy is returned and *points* is unchanged.

    Returns:
        The (possibly same) array with CRS displacement applied.
    """
    if crs_obj is None:
        return points

    offset = get_crs_origin_offset(crs_obj=crs_obj)
    z_reversed = is_z_reversed(crs_obj)

    if not np.any(offset) and not z_reversed:
        return points

    if not inplace:
        points = points.copy()

    off = np.asarray(offset, dtype=np.float64)  # shape (3,)
    points += off  # broadcast: (N, 3) + (3,)
    if z_reversed:
        points[:, 2] *= -1.0

    return points


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _ensure_float64_points(arr: Any) -> np.ndarray:
    """Convert *arr* to ``(N, 3) float64``.

    Accepts numpy arrays (any shape that contains N*3 elements) or nested
    Python lists.  Returns a 2-D view/cast when possible, copy only when
    dtype conversion is required.
    """
    a = np.asarray(arr, dtype=np.float64)
    if a.ndim == 1:
        a = a.reshape(-1, 3)
    elif a.ndim == 2 and a.shape[1] == 2:
        # 2-D points (e.g. seismic / plan view) — pad Z column with zeros
        a = np.column_stack([a, np.zeros(len(a), dtype=np.float64)])
    elif a.ndim == 2 and a.shape[1] != 3:
        raise ValueError(f"Expected (N, 2) or (N, 3) points array, got shape {a.shape}")
    return a


def _ensure_int64(arr: Any) -> np.ndarray:
    """Return *arr* as a flat ``int64`` numpy array."""
    a = np.asarray(arr, dtype=np.int64)
    return a.ravel()


def _build_vtk_faces_from_triangles(tri: np.ndarray) -> np.ndarray:
    """Build VTK flat face array from ``(M, 3)`` triangle index array.

    Result: ``[3, a, b, c,  3, a, b, c, …]``.
    """
    m = tri.shape[0]
    counts = np.full((m, 1), 3, dtype=np.int64)
    return np.concatenate([counts, tri], axis=1).ravel()


def _build_vtk_faces_from_quads(quad: np.ndarray) -> np.ndarray:
    """Build VTK flat face array from ``(M, 4)`` quad index array.

    Result: ``[4, a, b, c, d,  4, a, b, c, d, …]``.
    """
    m = quad.shape[0]
    counts = np.full((m, 1), 4, dtype=np.int64)
    return np.concatenate([counts, quad], axis=1).ravel()


def _build_vtk_lines_from_segments(n_points: int) -> np.ndarray:
    """Build VTK flat lines array for a single poly-line of *n_points* nodes.

    Segments: (0,1), (1,2), …, (n-2, n-1).
    Result: ``[2, 0, 1,  2, 1, 2, …]``.
    """
    if n_points < 2:
        return np.empty(0, dtype=np.int64)
    idx = np.arange(n_points - 1, dtype=np.int64)
    pairs = np.column_stack([idx, idx + 1])  # (n-1, 2)
    counts = np.full((n_points - 1, 1), 2, dtype=np.int64)
    return np.concatenate([counts, pairs], axis=1).ravel()


def _build_vtk_lines_from_node_counts(node_counts: np.ndarray) -> np.ndarray:
    """Build VTK flat lines array from per-polyline node counts.

    For each polyline of length *n* we emit ``[n, 0, 1, …, n-1]`` with
    indices local to the global point array (starting at the correct offset).

    Returns ``(total_entries,)`` int64 array.
    """
    result_parts = []
    offset = 0
    for n in node_counts:
        n = int(n)
        local = np.arange(offset, offset + n, dtype=np.int64)
        part = np.empty(n + 1, dtype=np.int64)
        part[0] = n
        part[1:] = local
        result_parts.append(part)
        offset += n
    if not result_parts:
        return np.empty(0, dtype=np.int64)
    return np.concatenate(result_parts)


def _read_array_np(
    energyml_array: Any,
    root_obj: Any,
    path_in_root: str,
    workspace: Optional[Any],  # _ViewWorkspace or EnergymlStorageInterface
) -> np.ndarray:
    """Thin wrapper around :func:`helper.read_array` that guarantees ndarray output."""
    result = read_array(
        energyml_array=energyml_array,
        root_obj=root_obj,
        path_in_root=path_in_root,
        workspace=workspace,
    )
    if result is None:
        return np.empty(0)
    if isinstance(result, np.ndarray):
        return result
    return np.asarray(result)


def _decode_jagged_array(
    jagged: Any,
    root_obj: Any,
    base_path: str,
    workspace: Optional[Any],
) -> List[np.ndarray]:
    """Decode a RESQML ``JaggedArray`` into a list of numpy sub-arrays.

    ``JaggedArray`` stores data as:
    * ``Elements``          — flat 1-D array of all values concatenated.
    * ``CumulativeLength``  — 1-D array of end-offsets; ``CumulativeLength[i]``
      is the exclusive end index of sub-array *i* in ``Elements``.

    Returns an empty list when either component is missing.
    """
    elem_list = search_attribute_matching_name_with_path(jagged, "Elements")
    cum_list = search_attribute_matching_name_with_path(jagged, "CumulativeLength")
    if not elem_list or not cum_list:
        return []
    elem_path, elem_obj = elem_list[0]
    cum_path, cum_obj = cum_list[0]
    elements = _read_array_np(elem_obj, root_obj, f"{base_path}.{elem_path}", workspace)
    cum_len = _read_array_np(cum_obj, root_obj, f"{base_path}.{cum_path}", workspace).astype(np.int64)
    result: List[np.ndarray] = []
    prev = 0
    for c in cum_len:
        c = int(c)
        result.append(elements[prev:c])
        prev = c
    return result


# ---------------------------------------------------------------------------
# Dispatcher machinery (mirrors mesh.py but prefixed with 'numpy_')
# ---------------------------------------------------------------------------


def _numpy_mesh_name_mapping(arr_type_name: str) -> str:
    """Normalise the energyml type name to match a ``read_numpy_<name>`` function."""
    arr_type_name = arr_type_name.replace("3D", "3d").replace("2D", "2d")
    arr_type_name = re.sub(r"^[Oo]bj([A-Z])", r"\1", arr_type_name)
    arr_type_name = re.sub(r"(Polyline|Point)Set", r"\1", arr_type_name)
    return arr_type_name


def get_numpy_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """Return the ``read_numpy_<type>`` function for *mesh_type_name*, or ``None``."""
    target = f"read_numpy_{snake_case(mesh_type_name)}"
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name == target:
            return obj
    return None


# ---------------------------------------------------------------------------
# Representation readers
# ---------------------------------------------------------------------------


def read_numpy_point_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``PointRepresentation`` / ``PointSetRepresentation``."""
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )
    patch_idx = 0
    total_size = 0

    patches_geom = search_attribute_matching_name_with_path(
        energyml_object, r"NodePatch.[\d]+.Geometry.Points"
    ) + search_attribute_matching_name_with_path(energyml_object, r"NodePatchGeometry.[\d]+.Points")

    for points_path_in_obj, points_obj in patches_geom:
        raw = _read_array_np(points_obj, energyml_object, points_path_in_obj, ws)
        points = _ensure_float64_points(raw)  # (N,3)

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=points_obj,
                path_in_root=points_path_in_obj,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError:
            pass

        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < len(points))
            points = points[t_idx[mask]]
            total_size += len(points)

        # Apply full CRS transform per patch; crs_object kept for reference,
        # outer dispatcher is guarded to skip crs_displacement_np for this type.
        if use_crs_displacement and crs is not None and len(points) > 0:
            apply_from_crs_info(points, extract_crs_info(crs, workspace), inplace=True)

        label = f"{src_type}_patch_{patch_idx}"
        multi.patches.append(
            NumpyPointSetMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=points,
                patch_index=patch_idx,
                patch_label=label,
                source_uuid=src_uuid,
                source_type=src_type,
            )
        )
        patch_idx += 1

    return multi


def read_numpy_polyline_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``PolylineRepresentation`` / ``PolylineSetRepresentation``."""
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )
    patch_idx = 0
    total_size = 0

    for patch_path_in_obj, patch in search_attribute_matching_name_with_path(
        energyml_object, "NodePatch"
    ) + search_attribute_matching_name_with_path(energyml_object, r"LinePatch.[\d]+"):
        # --- Points ---
        pts_list = search_attribute_matching_name_with_path(patch, "Geometry.Points")
        if not pts_list:
            pts_list = search_attribute_matching_name_with_path(patch, "Points")
        if not pts_list:
            logging.error(f"Cannot find points for patch {patch_path_in_obj}")
            continue

        points_path, points_obj = pts_list[0]
        raw_pts = _read_array_np(points_obj, energyml_object, patch_path_in_obj + "." + points_path, ws)
        points = _ensure_float64_points(raw_pts)  # (N, 3)

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=points_obj,
                path_in_root=patch_path_in_obj + "." + points_path,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError:
            pass

        # --- Closed polylines flag (optional) ---
        close_poly: Optional[np.ndarray] = None
        try:
            cp_path, cp_obj = search_attribute_matching_name_with_path(patch, "ClosedPolylines")[0]
            close_poly = _read_array_np(cp_obj, energyml_object, patch_path_in_obj + "." + cp_path, ws)
        except IndexError:
            pass

        # --- Node counts per polyline ---
        # nc_arr holds the *original* counts (before closing); used both for
        # VTK-array construction and for sub_indices filtering below.
        nc_arr: Optional[np.ndarray] = None
        lines: np.ndarray
        try:
            nc_path, nc_obj = search_attribute_matching_name_with_path(patch, "NodeCountPerPolyline")[0]
            nc_arr = _read_array_np(nc_obj, energyml_object, patch_path_in_obj + nc_path, ws).astype(np.int64).ravel()

            # Build VTK lines array respecting closed flags
            parts: List[np.ndarray] = []
            offset = 0
            for poly_idx, n in enumerate(nc_arr):
                n = int(n)
                indices = np.arange(offset, offset + n, dtype=np.int64)
                if close_poly is not None and poly_idx < len(close_poly) and close_poly[poly_idx]:
                    indices = np.append(indices, offset)  # close the loop
                    n += 1
                part = np.empty(n + 1, dtype=np.int64)
                part[0] = n
                part[1:] = indices
                parts.append(part)
                offset += n if close_poly is None or poly_idx >= len(close_poly) or not close_poly[poly_idx] else n - 1
            lines = np.concatenate(parts) if parts else np.empty(0, dtype=np.int64)
        except IndexError:
            # Single polyline — all points in sequence
            lines = _build_vtk_lines_from_segments(len(points))

        # --- sub_indices filtering ---
        # sub_indices select individual *polylines* (by index within this patch).
        # We filter the VTK flat `lines` buffer and also subset `points` to
        # keep only the nodes referenced by the surviving polylines.
        if sub_indices is not None and len(sub_indices) > 0:
            total_polylines = len(nc_arr) if nc_arr is not None else 1
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            _valid = np.sort(t_idx[(t_idx >= 0) & (t_idx < total_polylines)])
            total_size += total_polylines

            if nc_arr is not None and len(_valid) > 0:
                # Walk the VTK flat buffer once to record per-polyline slice bounds.
                pos = 0
                poly_slices: List[Tuple[int, int]] = []
                for _ in range(total_polylines):
                    n_vtk = int(lines[pos])
                    poly_slices.append((pos, pos + n_vtk + 1))
                    pos += n_vtk + 1

                # Original point ranges per polyline (nc_arr gives node counts).
                pt_offsets = np.concatenate([[0], np.cumsum(nc_arr)])

                # Gather contiguous point ranges for the selected polylines.
                keep_ranges = [np.arange(int(pt_offsets[i]), int(pt_offsets[i + 1]), dtype=np.int64) for i in _valid]
                keep_pts = np.concatenate(keep_ranges) if keep_ranges else np.empty(0, dtype=np.int64)

                # Build a full remapping: old_pt_idx → new_pt_idx (-1 = not kept).
                new_pt_idx = np.full(len(points), -1, dtype=np.int64)
                new_pt_idx[keep_pts] = np.arange(len(keep_pts), dtype=np.int64)
                points = points[keep_pts]

                # Re-index VTK segments for the selected polylines.
                rebuilt: List[np.ndarray] = []
                for i in _valid:
                    s, e = poly_slices[i]
                    seg = lines[s:e].copy()
                    seg[1:] = new_pt_idx[seg[1:]]
                    rebuilt.append(seg)
                lines = np.concatenate(rebuilt) if rebuilt else np.empty(0, dtype=np.int64)
            elif len(_valid) == 0:
                points = np.empty((0, 3), dtype=np.float64)
                lines = np.empty(0, dtype=np.int64)
        else:
            total_size += 1  # at least one polyline

        # Apply full CRS transform per patch; crs_object kept for reference,
        # outer dispatcher is guarded to skip crs_displacement_np for this type.
        if use_crs_displacement and crs is not None and len(points) > 0:
            apply_from_crs_info(points, extract_crs_info(crs, workspace), inplace=True)

        if len(points) > 0:
            label = f"{src_type}_patch_{patch_idx}"
            multi.patches.append(
                NumpyPolylineMesh(
                    identifier=label,
                    energyml_object=energyml_object,
                    crs_object=crs,
                    points=points,
                    lines=lines,
                    patch_index=patch_idx,
                    patch_label=label,
                    source_uuid=src_uuid,
                    source_type=src_type,
                )
            )
        patch_idx += 1

    return multi


def read_numpy_triangulated_set_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``TriangulatedSetRepresentation`` as numpy-backed surface meshes.

    Key differences vs :func:`mesh.read_triangulated_set_representation`:

    * No ``.tolist()`` — geometry stays in numpy arrays.
    * Point-offset arithmetic is done via in-place numpy broadcast.
    * VTK flat face connectivity is built with :func:`numpy.concatenate` and
      :func:`numpy.column_stack` — no Python loops over triangles.
    """
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )
    point_offset = 0
    patch_idx = 0
    total_size = 0

    patches = search_attribute_matching_name_with_path(
        energyml_object,
        r"\w*Patch.\d+",
        deep_search=False,
        search_in_sub_obj=False,
    )

    for patch_path, patch in patches:
        crs = None
        try:
            crs = get_crs_obj(
                context_obj=patch,
                path_in_root=patch_path,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError:
            pass

        # --- Points ---
        pts_parts: List[np.ndarray] = []
        for point_path, point_obj in search_attribute_matching_name_with_path(patch, "Geometry.Points"):
            raw = _read_array_np(point_obj, energyml_object, patch_path + "." + point_path, ws)
            pts_parts.append(_ensure_float64_points(raw))

        if not pts_parts:
            patch_idx += 1
            continue
        points = np.concatenate(pts_parts, axis=0)  # (N, 3)

        # Apply full CRS transform (rotation + offsets + z-flip + axis-swap) per patch.
        # Setting crs_object=None on the resulting mesh prevents the outer
        # read_numpy_mesh_object dispatcher from calling crs_displacement_np() again.
        if use_crs_displacement and crs is not None and len(points) > 0:
            crs_info = extract_crs_info(crs, workspace)
            apply_from_crs_info(points, crs_info, inplace=True)

        # --- Triangles ---
        tri_parts: List[np.ndarray] = []
        for tri_path, tri_obj in search_attribute_matching_name_with_path(patch, "Triangles"):
            raw = _read_array_np(tri_obj, energyml_object, patch_path + "." + tri_path, ws)
            tri_parts.append(raw.astype(np.int64).reshape(-1, 3))

        if not tri_parts:
            patch_idx += 1
            continue
        triangles = np.concatenate(tri_parts, axis=0)  # (M, 3)

        # Apply point offset (in-place broadcast — no copy when dtype matches)
        if point_offset != 0:
            triangles -= point_offset  # local 0-based indices

        # sub_indices face filtering
        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < len(triangles))
            triangles = triangles[t_idx[mask]]
        total_size += len(triangles)

        # Build VTK flat faces array: [3, v0, v1, v2, 3, v0, v1, v2, …]
        faces = _build_vtk_faces_from_triangles(triangles)

        label = f"{src_type}_patch_{patch_idx}"
        multi.patches.append(
            NumpySurfaceMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=points,
                faces=faces,
                patch_index=patch_idx,
                patch_label=label,
                source_uuid=src_uuid,
                source_type=src_type,
            )
        )
        point_offset += len(points)
        patch_idx += 1

    return multi


def read_numpy_grid2d_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    keep_holes: bool = False,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``Grid2dRepresentation`` as a numpy quad-surface mesh.

    NaN-hole handling is done with boolean masks and cumsum-based index remapping
    (O(N) vs the O(N) dict-based approach in :func:`mesh.gen_surface_grid_geometry`,
    but avoids Python dict overhead for large grids).
    """
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )
    patch_idx = 0
    total_size = 0

    def _process_patch(patch: Any, patch_path: str, crs: Any) -> Optional[NumpySurfaceMesh]:
        nonlocal total_size, patch_idx
        # read_grid2d_patch returns List[List[float]] — convert to ndarray
        raw_pts = read_grid2d_patch(
            patch=patch,
            grid2d=energyml_object,
            path_in_root=patch_path,
            workspace=workspace,
        )
        pts = np.asarray(raw_pts, dtype=np.float64) if raw_pts is not None else np.empty((0, 3))
        if pts.size == 0:
            return None

        if pts.ndim == 1:
            pts = pts.reshape(-1, 3)

        # Grid dimensions
        fa_count = search_attribute_matching_name(patch, "FastestAxisCount") or search_attribute_matching_name(
            energyml_object, "FastestAxisCount"
        )
        sa_count = search_attribute_matching_name(patch, "SlowestAxisCount") or search_attribute_matching_name(
            energyml_object, "SlowestAxisCount"
        )
        if not fa_count or not sa_count:
            return None
        fa = int(fa_count[0])
        sa = int(sa_count[0])

        # Clamp dimensions to actual number of points
        total_pts = len(pts)
        while sa * fa > total_pts and sa > 0 and fa > 0:
            sa -= 1
            fa -= 1
        while sa * fa < total_pts:
            sa += 1
            fa += 1

        z_col = pts[:, 2]
        nan_mask = np.isnan(z_col)  # True where Z is NaN (hole)

        if keep_holes:
            pts[nan_mask, 2] = 0.0
            final_pts = pts
            # All original indices are valid
            local_idx = np.arange(total_pts, dtype=np.int64)
            remap = local_idx  # identity
        else:
            valid_mask = ~nan_mask
            final_pts = pts[valid_mask]
            # remap[original_index] = final_index (-1 ⟹ invalid/NaN)
            remap = np.full(total_pts, -1, dtype=np.int64)
            remap[valid_mask] = np.arange(valid_mask.sum(), dtype=np.int64)

        # Build quad face list (vectorised)
        quad_rows = []
        for sa_i in range(sa - 1):
            for fa_i in range(fa - 1):
                line = sa_i * fa
                a = line + fa_i
                b = line + fa_i + 1
                c = line + fa + fa_i + 1
                d = line + fa + fa_i
                if keep_holes:
                    quad_rows.append([a, b, c, d])
                else:
                    ra, rb, rc, rd = remap[a], remap[b], remap[c], remap[d]
                    if ra >= 0 and rb >= 0 and rc >= 0 and rd >= 0:
                        quad_rows.append([ra, rb, rc, rd])

        if not quad_rows:
            return None
        quads = np.asarray(quad_rows, dtype=np.int64)  # (M, 4)

        # sub_indices filtering
        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < len(quads))
            quads = quads[t_idx[mask]]
        total_size += len(quads)

        faces = _build_vtk_faces_from_quads(quads)
        label = f"{src_type}_patch_{patch_idx}"
        mesh = NumpySurfaceMesh(
            identifier=label,
            energyml_object=energyml_object,
            crs_object=crs,
            points=final_pts,
            faces=faces,
            patch_index=patch_idx,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
        patch_idx += 1
        return mesh

    # RESQML 2.0.1 — patches
    for patch_path, patch in search_attribute_matching_name_with_path(energyml_object, "Grid2dPatch"):
        crs = None
        try:
            crs = get_crs_obj(
                context_obj=patch,
                path_in_root=patch_path,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError:
            pass
        m = _process_patch(patch, patch_path, crs)
        if m is not None:
            multi.patches.append(m)

    # RESQML 2.2 — geometry directly on the object
    if hasattr(energyml_object, "geometry"):
        crs = None
        try:
            crs = get_crs_obj(
                context_obj=energyml_object,
                path_in_root=".",
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError as e:
            logging.error(e)
        m = _process_patch(energyml_object, "", crs)
        if m is not None:
            multi.patches.append(m)

    return multi


def read_numpy_wellbore_trajectory_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    wellbore_frame_mds: Optional[Union[List[float], np.ndarray]] = None,
    step_meter: float = 5.0,
) -> "NumpyMultiMesh":
    """Read a ``WellboreTrajectoryRepresentation`` as a numpy polyline mesh."""
    if energyml_object is None:
        return NumpyMultiMesh(identifier="empty_wellbore_trajectory")

    if isinstance(energyml_object, list):
        synthetic = NumpyMultiMesh(identifier="WellboreTrajectoryRepresentation_list")
        for obj in energyml_object:
            synthetic.children.append(
                read_numpy_wellbore_trajectory_representation(
                    obj, workspace, use_crs_displacement, sub_indices, wellbore_frame_mds, step_meter
                )
            )
        return synthetic

    crs = None
    head_x = head_y = head_z = 0.0
    z_increasing_downward = False

    try:
        crs_attr = get_object_attribute(energyml_object, "geometry.LocalCrs")
        if crs_attr is not None:
            crs = workspace.get_object(get_obj_uri(crs_attr))
        else:
            raise ObjectNotFoundNotError("LocalCrs not found")
    except Exception:
        logging.debug("Could not get CRS from trajectory geometry")

    # MD datum / reference point (fixes always-at-origin bug)
    try:
        md_datum_dor = None
        try:
            md_datum_dor = search_attribute_matching_name(obj=energyml_object, name_rgx=r"MdDatum")[0]
        except IndexError:
            try:
                md_datum_dor = search_attribute_matching_name(obj=energyml_object, name_rgx=r"MdInterval.Datum")[0]
            except IndexError:
                pass

        if md_datum_dor is not None:
            md_datum_identifier = get_obj_uri(md_datum_dor)
            md_datum_obj = workspace.get_object(md_datum_identifier) if workspace else None
            if md_datum_obj is not None:
                head_x, head_y, head_z, z_increasing_downward, _, _, crs = get_datum_information(
                    md_datum_obj, workspace
                )
    except Exception as e:
        logging.debug(f"Could not resolve MdDatum from trajectory: {e}")

    try:
        crs_info = extract_crs_info(crs, workspace)
        traj_mds, traj_points, traj_tangents = read_parametric_geometry(
            getattr(energyml_object, "geometry", None), workspace
        )
        well_points_list = get_wellbore_points(wellbore_frame_mds, traj_mds, traj_points, traj_tangents, step_meter)
        if use_crs_displacement:
            well_points_list = apply_from_crs_info(
                np.asarray(well_points_list, dtype=np.float64),
                crs_info,
            )
    except Exception as e:
        if wellbore_frame_mds is not None:
            logging.debug(f"Trajectory parametric geometry unavailable, treating as vertical: {e}")
            well_points_list = generate_vertical_well_points(
                head_x=head_x,
                head_y=head_y,
                head_z=head_z,
                wellbore_mds=wellbore_frame_mds
                if isinstance(wellbore_frame_mds, np.ndarray)
                else np.asarray(wellbore_frame_mds),
                z_increasing_downward=z_increasing_downward,
            )
        else:
            traceback.print_exc()
            raise ValueError(
                "Cannot read WellboreTrajectoryRepresentation: "
                "no parametric geometry and no measured depth information available."
            )

    if well_points_list is None or len(well_points_list) == 0:
        return NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(get_obj_uri(energyml_object)),
            source_uuid=get_obj_uuid(energyml_object),
            source_type=type(energyml_object).__name__,
        )

    pts = _ensure_float64_points(np.asarray(well_points_list, dtype=np.float64))
    lines = _build_vtk_lines_from_segments(len(pts))
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    label = f"{src_type}_patch_0"
    return NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
        patches=[
            NumpyPolylineMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=pts,
                lines=lines,
                patch_index=0,
                patch_label=label,
                source_uuid=src_uuid,
                source_type=src_type,
            )
        ],
    )


def read_numpy_wellbore_frame_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``WellboreFrameRepresentation`` as a numpy polyline mesh."""
    ws = _view_workspace(workspace)
    empty = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=get_obj_uuid(energyml_object),
        source_type=type(energyml_object).__name__,
    )

    try:
        node_md_path, node_md_obj = search_attribute_matching_name_with_path(energyml_object, "NodeMd")[0]
        wellbore_frame_mds = _read_array_np(node_md_obj, energyml_object, node_md_path, ws)
        if not isinstance(wellbore_frame_mds, np.ndarray):
            wellbore_frame_mds = np.asarray(wellbore_frame_mds, dtype=np.float64)
    except (IndexError, AttributeError) as e:
        logging.warning(f"Could not read NodeMd from wellbore frame: {e}")
        return empty

    md_min = float(wellbore_frame_mds.min()) if len(wellbore_frame_mds) > 0 else 0.0
    md_max = float(wellbore_frame_mds.max()) if len(wellbore_frame_mds) > 0 else 0.0

    try:
        _md_min = get_object_attribute(energyml_object, "md_interval.md_min")
        if _md_min is not None:
            md_min = float(_md_min)
        _md_max = get_object_attribute(energyml_object, "md_interval.md_max")
        if _md_max is not None:
            md_max = float(_md_max)
    except AttributeError:
        pass

    wellbore_frame_mds = wellbore_frame_mds[(wellbore_frame_mds >= md_min) & (wellbore_frame_mds <= md_max)]

    trajectory_dor = search_attribute_matching_name(obj=energyml_object, name_rgx="Trajectory")[0]
    trajectory_obj = workspace.get_object(get_obj_uri(trajectory_dor))

    result = read_numpy_wellbore_trajectory_representation(
        energyml_object=trajectory_obj,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
        wellbore_frame_mds=wellbore_frame_mds,
    )
    frame_uri = str(get_obj_uri(energyml_object))
    for m in result.flat_patches():
        m.identifier = frame_uri
    result.identifier = frame_uri
    result.source_uuid = get_obj_uuid(energyml_object)
    result.source_type = type(energyml_object).__name__
    result.energyml_object = energyml_object
    return result


def read_numpy_sub_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Delegate to the supporting representation with filtered indices."""
    ws = _view_workspace(workspace)
    supporting_rep_dor = search_attribute_matching_name(
        obj=energyml_object, name_rgx=r"(SupportingRepresentation|RepresentedObject)"
    )[0]
    supporting_rep = workspace.get_object(get_obj_uri(supporting_rep_dor))

    total_size = 0
    all_indices: Optional[np.ndarray] = None
    for patch_path, patch_indices in search_attribute_matching_name_with_path(
        obj=energyml_object,
        name_rgx=r"SubRepresentationPatch.\d+.ElementIndices.\d+.Indices",
        deep_search=False,
        search_in_sub_obj=False,
    ) + search_attribute_matching_name_with_path(
        obj=energyml_object,
        name_rgx=r"SubRepresentationPatch.\d+.Indices",
        deep_search=False,
        search_in_sub_obj=False,
    ):
        arr = _read_array_np(patch_indices, energyml_object, patch_path, ws).astype(np.int64).ravel()
        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < len(arr))
            arr = arr[t_idx[mask]]
        total_size += len(arr)
        all_indices = np.concatenate([all_indices, arr]) if all_indices is not None else arr

    inner = read_numpy_mesh_object(
        energyml_object=supporting_rep,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=all_indices.tolist() if all_indices is not None else None,
    )
    sub_uri = str(get_obj_uri(energyml_object))
    for m in inner.flat_patches():
        m.identifier = f"sub_rep_{sub_uri}/{m.identifier}"
    return NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=sub_uri,
        source_uuid=get_obj_uuid(energyml_object),
        source_type=type(energyml_object).__name__,
        patches=[],
        children=[inner],
    )


def read_numpy_representation_set_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Delegate to each child representation; nest results as children."""
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=get_obj_uuid(energyml_object),
        source_type=type(energyml_object).__name__,
    )
    repr_list = get_object_attribute(energyml_object, "representation")
    if repr_list is None or not isinstance(repr_list, list):
        return multi
    for repr_dor in repr_list:
        rpr_uri = get_obj_uri(repr_dor)
        repr_obj = workspace.get_object(rpr_uri)
        if repr_obj is None:
            logging.error(f"Representation {rpr_uri} not found in RepresentationSetRepresentation")
            continue
        child = read_numpy_mesh_object(
            energyml_object=repr_obj,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
        )
        multi.children.append(child)
    return multi


# ---------------------------------------------------------------------------
# VTK cell-type codes (subset used by RESQML readers)
# ---------------------------------------------------------------------------

_VTK_TETRA = 10
_VTK_HEXAHEDRON = 12
_VTK_WEDGE = 13
_VTK_PYRAMID = 14
_VTK_POLYHEDRON = 42


# ---------------------------------------------------------------------------
# New representation readers
# ---------------------------------------------------------------------------


def read_numpy_plane_set_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    horizontal_plane_half_extent: float = 1e5,
) -> "NumpyMultiMesh":
    """Read a ``PlaneSetRepresentation`` into numpy surface meshes.

    * ``HorizontalPlaneGeometry`` — synthesises a large finite quad centred at the
      CRS origin at the given Z coordinate.  The half-extent is controlled by
      *horizontal_plane_half_extent* (default 100 km in CRS length units).
    * ``TiltedPlaneGeometry`` — each ``ThreePoint3D`` entry becomes a triangle.

    Args:
        horizontal_plane_half_extent: Half-width in CRS length units of the
            synthesised quad used for ``HorizontalPlaneGeometry`` patches.
    """
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )

    crs = None
    try:
        crs = get_crs_obj(
            context_obj=energyml_object,
            path_in_root=".",
            root_obj=energyml_object,
            workspace=workspace,
        )
    except (ObjectNotFoundNotError, Exception):
        pass

    planes_list = search_attribute_matching_name_with_path(energyml_object, "Planes")
    patch_idx = 0

    for _plane_path, plane_geom in planes_list:
        geom_type = type(plane_geom).__name__

        if geom_type == "HorizontalPlaneGeometry":
            z = float(getattr(plane_geom, "coordinate", 0.0))
            hx = hy = float(horizontal_plane_half_extent)
            points = np.array(
                [[-hx, -hy, z], [hx, -hy, z], [hx, hy, z], [-hx, hy, z]],
                dtype=np.float64,
            )
            faces = np.array([4, 0, 1, 2, 3], dtype=np.int64)

        elif geom_type == "TiltedPlaneGeometry":
            pts_list: List[np.ndarray] = []
            tri_list: List[List[int]] = []
            pt_offset = 0
            for three_pt in getattr(plane_geom, "plane", []):
                pts3 = getattr(three_pt, "point3d", [])
                if len(pts3) < 3:
                    continue
                tri_pts = np.array(
                    [[p.coordinate1, p.coordinate2, p.coordinate3] for p in pts3[:3]],
                    dtype=np.float64,
                )
                pts_list.append(tri_pts)
                tri_list.append([pt_offset, pt_offset + 1, pt_offset + 2])
                pt_offset += 3
            if not pts_list:
                patch_idx += 1
                continue
            points = np.concatenate(pts_list, axis=0)
            tris = np.array(tri_list, dtype=np.int64)  # (M, 3)
            faces = _build_vtk_faces_from_triangles(tris)

        else:
            logging.warning(f"PlaneSetRepresentation: unknown geometry type {geom_type!r} — skipping patch {patch_idx}")
            patch_idx += 1
            continue

        if use_crs_displacement and crs is not None and len(points) > 0:
            apply_from_crs_info(points, extract_crs_info(crs, workspace), inplace=True)

        label = f"{src_type}_patch_{patch_idx}"
        multi.patches.append(
            NumpySurfaceMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=points,
                faces=faces,
                patch_index=patch_idx,
                patch_label=label,
                source_uuid=src_uuid,
                source_type=src_type,
            )
        )
        patch_idx += 1

    return multi


def read_numpy_seismic_wellbore_frame_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``SeismicWellboreFrameRepresentation``.

    ``SeismicWellboreFrameRepresentation`` extends ``WellboreFrameRepresentation``
    and adds a ``NodeTimeValues`` array (one time value per frame node).  This
    reader delegates geometry to :func:`read_numpy_wellbore_frame_representation`
    and stores the extra time values in ``patch.extra_arrays["node_time_values"]``
    on every returned patch.
    """
    ws = _view_workspace(workspace)
    result = read_numpy_wellbore_frame_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    # Attach NodeTimeValues to each patch as extra data
    try:
        ntv_path, ntv_obj = search_attribute_matching_name_with_path(energyml_object, "NodeTimeValues")[0]
        node_time_values = _read_array_np(ntv_obj, energyml_object, ntv_path, ws)
        for patch in result.flat_patches():
            patch.extra_arrays["node_time_values"] = node_time_values
    except (IndexError, Exception) as exc:
        logging.warning(f"SeismicWellboreFrameRepresentation: could not read NodeTimeValues: {exc}")
    result.source_type = type(energyml_object).__name__
    return result


def read_numpy_sealed_surface_framework_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``SealedSurfaceFrameworkRepresentation``.

    ``SealedSurfaceFrameworkRepresentation`` is a subtype of
    ``RepresentationSetRepresentation`` (via ``AbstractSurfaceFrameworkRepresentation``).
    Geometry is delegated to :func:`read_numpy_representation_set_representation`
    which reads each member representation.
    """
    result = read_numpy_representation_set_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    result.source_type = type(energyml_object).__name__
    return result


# ---------------------------------------------------------------------------
# IJK-grid helpers
# ---------------------------------------------------------------------------


def _build_kl_mapping(
    nk: int,
    gap_after: Optional[np.ndarray],
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute bottom and top NKL boundary indices for each K cell.

    Without K-gaps the mapping is trivial: cell k spans NKL nodes [k, k+1].
    When ``gap_after[k]`` is True, the NKL counter is incremented by an extra
    step between layers k and k+1, so the affected layers use distinct node
    intervals that are geometrically discontinuous.

    Args:
        nk:        Number of K cells (not layers).
        gap_after: Boolean array of length ``nk - 1``; ``True`` at index *k*
                   means there is a K-gap after layer *k*.

    Returns:
        ``(kl_bottom, kl_top)`` — two ``(nk,)`` int64 arrays giving the NKL
        index of the bottom and top node boundary for each cell.
    """
    kl_bottom = np.zeros(nk, dtype=np.int64)
    kl_top = np.zeros(nk, dtype=np.int64)
    kl = 0
    for k in range(nk):
        kl_bottom[k] = kl
        kl += 1
        kl_top[k] = kl
        if gap_after is not None and k < len(gap_after) and gap_after[k]:
            kl += 1  # skip one NKL slot for the gap
    return kl_bottom, kl_top


def _build_split_pillar_map(
    ni: int,
    nj: int,
    pillar_indices_arr: np.ndarray,
    columns_per_split: List[np.ndarray],
    n_splits: int,
) -> np.ndarray:
    """Build a per-column corner-pillar remapping for split coordinate lines.

    For each column ``(j, i)`` the four corners are labelled::

        TL = (j,   i)    TR = (j,   i+1)
        BL = (j+1, i)    BR = (j+1, i+1)

    Without splits every corner maps to the standard pillar index
    ``j*(ni+1)+i``.  Split coordinate lines displace this mapping for the
    affected columns.

    Args:
        ni, nj:              Cell counts in I and J.
        pillar_indices_arr:  ``(n_splits,)`` int64 — original pillar index for
                             each split coordinate line.
        columns_per_split:   Length-``n_splits`` list of int arrays — column
                             indices (flat, ``j*ni+i``) that use each split line.
        n_splits:            Number of split coordinate lines.

    Returns:
        ``pillar_map`` — shape ``(nj, ni, 4)`` int64; corner order is
        ``[TL, TR, BL, BR]``.
    """
    n_pillars_base = (ni + 1) * (nj + 1)
    pillar_map = np.zeros((nj, ni, 4), dtype=np.int64)
    for j in range(nj):
        for i in range(ni):
            pillar_map[j, i, 0] = j * (ni + 1) + i  # TL
            pillar_map[j, i, 1] = j * (ni + 1) + (i + 1)  # TR
            pillar_map[j, i, 2] = (j + 1) * (ni + 1) + i  # BL
            pillar_map[j, i, 3] = (j + 1) * (ni + 1) + (i + 1)  # BR

    for split_idx in range(n_splits):
        if split_idx >= len(columns_per_split):
            break
        orig_pillar_idx = int(pillar_indices_arr[split_idx])
        orig_j = orig_pillar_idx // (ni + 1)
        orig_i = orig_pillar_idx % (ni + 1)
        new_pillar_idx = n_pillars_base + split_idx
        for col_flat in columns_per_split[split_idx].astype(np.int64):
            col_j = int(col_flat) // ni
            col_i = int(col_flat) % ni
            if not (0 <= col_j < nj and 0 <= col_i < ni):
                continue
            # Identify which corner of this column corresponds to (orig_j, orig_i)
            if orig_j == col_j and orig_i == col_i:
                pillar_map[col_j, col_i, 0] = new_pillar_idx  # TL
            elif orig_j == col_j and orig_i == col_i + 1:
                pillar_map[col_j, col_i, 1] = new_pillar_idx  # TR
            elif orig_j == col_j + 1 and orig_i == col_i:
                pillar_map[col_j, col_i, 2] = new_pillar_idx  # BL
            elif orig_j == col_j + 1 and orig_i == col_i + 1:
                pillar_map[col_j, col_i, 3] = new_pillar_idx  # BR

    return pillar_map


def _read_direct_points(
    pts_obj: Any,
    pts_path: str,
    energyml_object: Any,
    ws: Any,
    nkl: int,
    n_pillars_total: int,
    n_pillars_base: int,
    n_splits: int,
    ni: int,
    nj: int,
) -> np.ndarray:
    """
    Read a non-parametric points array (e.g. ``Point3DExternalArray``) and
    return a ``(NKL, n_pillars_total, 3)`` float64 array.

    Handles both the 3-D layout ``(NKL, n_pillars, 3)`` typically used for
    faulted grids and the 4-D layout ``(NKL, NJ+1, NI+1, 3)`` used for
    unfaulted grids.

    :raises ValueError: When the raw array size matches neither layout.
    """
    raw_pts = _read_array_np(pts_obj, energyml_object, f"geometry.{pts_path}", ws)

    expected_3d = nkl * n_pillars_total * 3
    expected_4d = nkl * (nj + 1) * (ni + 1) * 3

    if n_splits > 0 or raw_pts.size == expected_3d:
        return raw_pts.reshape(nkl, n_pillars_total, 3)
    elif raw_pts.size == expected_4d:
        # Standard 4-D unfaulted layout: (NKL, NJ+1, NI+1, 3).
        # Pillar index j*(ni+1)+i matches C-order of the last two dims.
        pts_4d = raw_pts.reshape(nkl, nj + 1, ni + 1, 3)
        return pts_4d.reshape(nkl, n_pillars_base, 3)
    else:
        raise ValueError(
            f"IjkGridRepresentation: unexpected points array size {raw_pts.size}. "
            f"Expected {expected_3d} (3-D layout, nkl={nkl}, n_pillars={n_pillars_total}) "
            f"or {expected_4d} (4-D layout, nkl={nkl}, nj+1={nj+1}, ni+1={ni+1})."
        )


def _read_point3d_parametric_array(
    pts_obj: Any,
    energyml_object: Any,
    ws: Any,
    nkl: int,
    n_pillars_total: int,
    n_pillars_base: int,
    ni: int,
    nj: int,
) -> np.ndarray:
    """
    Evaluate a ``Point3dParametricArray`` and return a
    ``(NKL, n_pillars_total, 3)`` float64 array of XYZ positions.

    Algorithm outline
    -----------------
    1. Read ``pts_obj.parameters`` — the P-values (typically depth) at every
       ``(NKL × n_pillars)`` grid node.
    2. Optionally honour ``pts_obj.parametric_line_indices`` — when present it
       maps each column of *parameters* to the corresponding pillar index in
       the ``ParametricLineArray``.
    3. Resolve ``pts_obj.parametric_lines`` via
       :func:`~energyml.utils.data.helper.resolve_parametric_line_array`
       (handles both ``ParametricLineArray`` and
       ``ParametricLineFromRepresentationLatticeArray``).
    4. Evaluate the pillar splines via
       :func:`~energyml.utils.data.helper.evaluate_parametric_line_array`.

    :param pts_obj: ``Point3dParametricArray`` RESQML object.
    :param energyml_object: Root RESQML object (for ``read_array`` context).
    :param ws: Workspace (HDF5 / EPC reader).
    :param nkl: Number of node layers (``nk + n_kgaps + 1``).
    :param n_pillars_total: Total pillar count (base + split duplicates).
    :param n_pillars_base: ``(ni+1) × (nj+1)``.
    :param ni: Cell count in the I direction.
    :param nj: Cell count in the J direction.
    :return: ``(NKL, n_pillars_total, 3)`` float64 array.
    :raises ValueError: If ``parameters`` or ``parametric_lines`` are absent.
    """
    # --- 1. Read query P-values ---
    params_obj = getattr(pts_obj, "parameters", None)
    if params_obj is None:
        raise ValueError(
            "Point3dParametricArray.parameters is required but absent — "
            "cannot evaluate pillar positions without depth P-values."
        )

    raw_params = _read_array_np(params_obj, energyml_object, "geometry.Points.parameters", ws)
    raw_params = raw_params.astype(np.float64)

    # Reshape to (NKL, n_pillars_total).
    expected_3d = nkl * n_pillars_total
    expected_4d = nkl * (nj + 1) * (ni + 1)
    if raw_params.size == expected_3d:
        query_params = raw_params.reshape(nkl, n_pillars_total)
    elif raw_params.size == expected_4d:
        query_params = raw_params.reshape(nkl, nj + 1, ni + 1).reshape(nkl, n_pillars_base)
        # Pad to n_pillars_total if needed (split pillars may extend the range).
        if n_pillars_total > n_pillars_base:
            pad = np.full((nkl, n_pillars_total - n_pillars_base), np.nan, dtype=np.float64)
            query_params = np.concatenate([query_params, pad], axis=1)
    else:
        logging.warning(
            f"Point3dParametricArray.parameters size {raw_params.size} does not match "
            f"expected {expected_3d} (3-D) or {expected_4d} (4-D). Attempting flat reshape."
        )
        query_params = raw_params.flatten()[: nkl * n_pillars_total].reshape(nkl, n_pillars_total)

    # --- 2. Handle optional parametric_line_indices ---
    # When present, each column index in query_params maps to a pillar index
    # in the ParametricLineArray (needed for grids with truncated or
    # non-contiguous pillar numbering).
    pli_obj = getattr(pts_obj, "parametric_line_indices", None)
    if pli_obj is not None:
        logging.debug(
            "Point3dParametricArray.parametric_line_indices is present. "
            "This re-indexing is applied inside evaluate_parametric_line_array "
            "via the column-selection mechanism of resolve_parametric_line_array."
        )
        # The indices are handled by passing the re-ordered query_params.
        # Build a column-permuted view so pillar p of query_params maps to
        # pillar pli[p] of the ParametricLineArray.
        raw_pli = _read_array_np(pli_obj, energyml_object, "geometry.Points.parametric_line_indices", ws)
        raw_pli = raw_pli.astype(np.int64).flatten()
        # Reorder query_params columns to match the PLA pillar ordering.
        # (Each position i in query_params[:,i] uses PLA pillar raw_pli[i].)
        # We pass this as-is; evaluate_parametric_line_array iterates by
        # query_params column index, which now aligns with pli-selected pillars.
        # NOTE: If pli introduces a non-injective mapping (two query columns →
        # same PLA pillar), the evaluation is repeated — this is correct per spec.
        query_params_reordered = query_params[:, raw_pli] if len(raw_pli) > 0 else query_params
        query_params = query_params_reordered

    # --- 3. Handle optional truncated_line_indices ---
    tli_obj = getattr(pts_obj, "truncated_line_indices", None)
    if tli_obj is not None:
        logging.warning(
            "Point3dParametricArray.truncated_line_indices is present. "
            "Full truncated-pillar support is not yet implemented — "
            "truncation metadata will be ignored and results may be geometrically "
            "incorrect near truncated pillars."
        )

    # --- 4. Resolve ParametricLineArray ---
    pla_raw = getattr(pts_obj, "parametric_lines", None)
    if pla_raw is None:
        raise ValueError("Point3dParametricArray.parametric_lines is required but absent.")
    pla = resolve_parametric_line_array(pla_raw, energyml_object, ws, n_pillars_total)

    # --- 5. Evaluate pillar splines ---
    pts_3d = evaluate_parametric_line_array(
        pla=pla,
        root_obj=energyml_object,
        workspace=ws,
        query_parameters=query_params,
        ni=ni,
        nj=nj,
    )  # (NKL, n_pillars_total, 3)

    return pts_3d


def read_numpy_ijk_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read an ``IjkGridRepresentation`` as a :class:`NumpyVolumeMesh`.

    Geometry is reconstructed from the pillar (coordinate-line) nodes stored in
    ``geometry.Points``.  The cells returned are always ``VTK_HEXAHEDRON``
    (type 12), which is the correct topology for RESQML IJK corner-point grids.

    Full-fidelity features
    ----------------------
    * **K-Gaps** — ``kgaps.gap_after_layer`` is decoded so that K-gap-separated
      layers use the correct NKL node-boundary interval.
    * **Split coordinate lines (faults)** — ``column_layer_split_coordinate_lines``
      is decoded to remap per-column corner pillars to their fault-split
      equivalents.  The faulted case uses a Python loop (not fully vectorised)
      because the remapping is column-specific; for large grids prefer the
      unfaulted vectorised path when possible.
    * **Degenerate cells** — pillars with co-located nodes (e.g. wedge columns)
      are preserved; PyVista tolerates degenerate hex nodes.

    Known limitation
    ----------------
    ``Point3DParametricArray`` pillar geometry is not yet supported (only
    ``Point3DExternalArray`` — direct HDF5 XYZ coordinates — is handled).  A
    :exc:`~energyml.utils.exception.NotSupportedError` is raised for parametric
    grids.
    """
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__

    ni = getattr(energyml_object, "ni", None)
    nj = getattr(energyml_object, "nj", None)
    nk = getattr(energyml_object, "nk", None)
    if ni is None or nj is None or nk is None:
        logging.warning("IjkGridRepresentation: ni/nj/nk not set — returning empty mesh")
        return NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(src_uuid),
            source_uuid=src_uuid,
            source_type=src_type,
        )
    ni, nj, nk = int(ni), int(nj), int(nk)

    geom = getattr(energyml_object, "geometry", None)
    if geom is None:
        logging.warning("IjkGridRepresentation has no geometry — returning empty mesh")
        return NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(src_uuid),
            source_uuid=src_uuid,
            source_type=src_type,
        )

    try:
        _obj_identifier = str(get_obj_uri(energyml_object))
    except Exception:
        _obj_identifier = str(src_uuid)
    empty = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=_obj_identifier,
        source_uuid=src_uuid,
        source_type=src_type,
    )

    # --- K-GAPS ---
    kgaps_obj = getattr(energyml_object, "kgaps", None)
    gap_after: Optional[np.ndarray] = None
    n_kgaps = 0
    if kgaps_obj is not None:
        n_kgaps = int(getattr(kgaps_obj, "count", 0) or 0)
        gap_attr_list = search_attribute_matching_name_with_path(kgaps_obj, "GapAfterLayer")
        if gap_attr_list:
            gap_path, gap_obj = gap_attr_list[0]
            gap_after = _read_array_np(gap_obj, energyml_object, f"kgaps.{gap_path}", ws).astype(bool)
    nkl = nk + n_kgaps + 1  # total number of K-boundary layers

    kl_bottom, kl_top = _build_kl_mapping(nk, gap_after)

    # --- SPLIT COORDINATE LINES ---
    split_cl = getattr(geom, "column_layer_split_coordinate_lines", None)
    n_splits = 0
    pillar_indices_arr: Optional[np.ndarray] = None
    columns_per_split: List[np.ndarray] = []
    if split_cl is not None:
        n_splits = int(getattr(split_cl, "count", 0) or 0)
        if n_splits > 0:
            pi_list = search_attribute_matching_name_with_path(split_cl, "PillarIndices")
            if pi_list:
                pi_path, pi_obj = pi_list[0]
                pillar_indices_arr = _read_array_np(
                    pi_obj,
                    energyml_object,
                    f"geometry.column_layer_split_coordinate_lines.{pi_path}",
                    ws,
                )
            cps_obj = getattr(split_cl, "columns_per_split_coordinate_line", None)
            if cps_obj is not None:
                columns_per_split = _decode_jagged_array(
                    cps_obj,
                    energyml_object,
                    "geometry.column_layer_split_coordinate_lines.columns_per_split_coordinate_line",
                    ws,
                )

    n_pillars_base = (ni + 1) * (nj + 1)
    n_pillars_total = n_pillars_base + n_splits

    # --- POINTS ---
    pts_results = search_attribute_matching_name_with_path(geom, "Points")
    if not pts_results:
        logging.warning("IjkGridRepresentation: cannot find Points in geometry")
        return empty
    pts_path, pts_obj = pts_results[0]

    # Reject parametric arrays (not yet supported)
    if "Parametric" in type(pts_obj).__name__:
        # Point3dParametricArray: evaluate pillar splines at the grid P-values.
        pts_3d = _read_point3d_parametric_array(
            pts_obj=pts_obj,
            energyml_object=energyml_object,
            ws=ws,
            nkl=nkl,
            n_pillars_total=n_pillars_total,
            n_pillars_base=n_pillars_base,
            ni=ni,
            nj=nj,
        )
    else:
        pts_3d = _read_direct_points(
            pts_obj=pts_obj,
            pts_path=pts_path,
            energyml_object=energyml_object,
            ws=ws,
            nkl=nkl,
            n_pillars_total=n_pillars_total,
            n_pillars_base=n_pillars_base,
            n_splits=n_splits,
            ni=ni,
            nj=nj,
        )

    points = pts_3d.reshape(-1, 3).astype(np.float64, copy=False)

    # --- CRS ---
    crs = None
    try:
        crs = get_crs_obj(
            context_obj=geom,
            path_in_root="geometry",
            root_obj=energyml_object,
            workspace=workspace,
        )
    except (ObjectNotFoundNotError, Exception):
        pass

    # --- PILLAR MAP for faulted grids ---
    use_pillar_map = n_splits > 0 and pillar_indices_arr is not None
    pillar_map: Optional[np.ndarray] = None
    if use_pillar_map:
        pillar_map = _build_split_pillar_map(ni, nj, pillar_indices_arr, columns_per_split, n_splits)

    # --- BUILD HEXAHEDRAL CELL CONNECTIVITY ---
    if pillar_map is None:
        # Fully vectorised path for unfaulted grids
        ii_arr, ij_arr, ik_arr = np.meshgrid(
            np.arange(ni, dtype=np.int64),
            np.arange(nj, dtype=np.int64),
            np.arange(nk, dtype=np.int64),
            indexing="ij",
        )  # each shape (ni, nj, nk)

        kl_b = kl_bottom[ik_arr]  # (ni, nj, nk)
        kl_t = kl_top[ik_arr]
        p_tl = ij_arr * (ni + 1) + ii_arr  # pillar TL
        p_tr = ij_arr * (ni + 1) + (ii_arr + 1)  # pillar TR
        p_bl = (ij_arr + 1) * (ni + 1) + ii_arr  # pillar BL
        p_br = (ij_arr + 1) * (ni + 1) + (ii_arr + 1)  # pillar BR

        def _nidx(kl, pl):
            return kl * n_pillars_total + pl

        # VTK_HEXAHEDRON node ordering (bottom face ccw, top face aligned)
        n0 = _nidx(kl_b, p_tl).ravel()
        n1 = _nidx(kl_b, p_tr).ravel()
        n2 = _nidx(kl_b, p_br).ravel()
        n3 = _nidx(kl_b, p_bl).ravel()
        n4 = _nidx(kl_t, p_tl).ravel()
        n5 = _nidx(kl_t, p_tr).ravel()
        n6 = _nidx(kl_t, p_br).ravel()
        n7 = _nidx(kl_t, p_bl).ravel()

        n_cells = ni * nj * nk
        count_col = np.full(n_cells, 8, dtype=np.int64)
        cells = np.column_stack([count_col, n0, n1, n2, n3, n4, n5, n6, n7]).ravel()
        cell_types = np.full(n_cells, _VTK_HEXAHEDRON, dtype=np.uint8)

    else:
        # Per-column loop for faulted grids (pillar_map resolved)
        cells_parts: List[int] = []
        for ij_idx in range(nj):
            for ii_idx in range(ni):
                p_tl = int(pillar_map[ij_idx, ii_idx, 0])
                p_tr = int(pillar_map[ij_idx, ii_idx, 1])
                p_bl = int(pillar_map[ij_idx, ii_idx, 2])
                p_br = int(pillar_map[ij_idx, ii_idx, 3])
                for ik_idx in range(nk):
                    kl_b = int(kl_bottom[ik_idx])
                    kl_t = int(kl_top[ik_idx])
                    n0 = kl_b * n_pillars_total + p_tl
                    n1 = kl_b * n_pillars_total + p_tr
                    n2 = kl_b * n_pillars_total + p_br
                    n3 = kl_b * n_pillars_total + p_bl
                    n4 = kl_t * n_pillars_total + p_tl
                    n5 = kl_t * n_pillars_total + p_tr
                    n6 = kl_t * n_pillars_total + p_br
                    n7 = kl_t * n_pillars_total + p_bl
                    cells_parts.extend([8, n0, n1, n2, n3, n4, n5, n6, n7])
        cells = np.array(cells_parts, dtype=np.int64)
        n_cells = ni * nj * nk
        cell_types = np.full(n_cells, _VTK_HEXAHEDRON, dtype=np.uint8)

    if use_crs_displacement and crs is not None and len(points) > 0:
        apply_from_crs_info(points, extract_crs_info(crs, workspace), inplace=True)

    label = f"{src_type}_patch_0"
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )
    multi.patches.append(
        NumpyVolumeMesh(
            identifier=label,
            energyml_object=energyml_object,
            crs_object=crs,
            points=points,
            cells=cells,
            cell_types=cell_types,
            patch_index=0,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
    )
    return multi


def read_numpy_unstructured_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read an ``UnstructuredGridRepresentation`` as a :class:`NumpyVolumeMesh`.

    All cells are emitted as ``VTK_POLYHEDRON`` (type 42) regardless of the
    ``cell_shape`` metadata.  This avoids the complex winding-order reconstruction
    required to convert RESQML's face-based topology to VTK's fixed-topology node
    lists (TETRA/PYRAMID/WEDGE/HEX).  The polyhedron format is lossless and
    PyVista can display and process these cells natively.

    The ``cell_face_is_right_handed`` boolean array is respected: faces whose flag
    is ``False`` have their node ordering reversed so that all face normals point
    outward from the cell.
    """
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__

    geom = getattr(energyml_object, "geometry", None)
    if geom is None:
        logging.warning("UnstructuredGridRepresentation has no geometry — returning empty mesh")
        return NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(src_uuid),
            source_uuid=src_uuid,
            source_type=src_type,
        )

    try:
        _obj_identifier = str(get_obj_uri(energyml_object))
    except Exception:
        _obj_identifier = str(src_uuid)
    empty = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=_obj_identifier,
        source_uuid=src_uuid,
        source_type=src_type,
    )

    # --- POINTS ---
    pts_results = search_attribute_matching_name_with_path(geom, "Points")
    if not pts_results:
        logging.warning("UnstructuredGridRepresentation: cannot find Points in geometry")
        return empty
    pts_path, pts_obj = pts_results[0]
    raw_pts = _read_array_np(pts_obj, energyml_object, pts_path, ws)
    points = _ensure_float64_points(raw_pts)  # (N, 3)

    # --- CRS ---
    crs = None
    try:
        crs = get_crs_obj(
            context_obj=geom,
            path_in_root="geometry",
            root_obj=energyml_object,
            workspace=workspace,
        )
    except (ObjectNotFoundNotError, Exception):
        pass

    # --- JAGGED ARRAYS ---
    npf_obj = getattr(geom, "nodes_per_face", None)
    fpc_obj = getattr(geom, "faces_per_cell", None)
    if npf_obj is None or fpc_obj is None:
        logging.warning(
            "UnstructuredGridRepresentation: missing nodes_per_face or faces_per_cell " "— returning point-set mesh"
        )
        label = f"{src_type}_patch_0"
        multi = NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(get_obj_uri(energyml_object)),
            source_uuid=src_uuid,
            source_type=src_type,
        )
        multi.patches.append(
            NumpyPointSetMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=points,
                patch_index=0,
                patch_label=label,
                source_uuid=src_uuid,
                source_type=src_type,
            )
        )
        return multi

    nodes_per_face = _decode_jagged_array(npf_obj, energyml_object, "geometry.nodes_per_face", ws)
    faces_per_cell = _decode_jagged_array(fpc_obj, energyml_object, "geometry.faces_per_cell", ws)
    cell_count = len(faces_per_cell)
    if cell_count == 0:
        return empty

    # --- RIGHT-HANDED BOOLEAN ARRAY ---
    rh_arr: Optional[np.ndarray] = None
    try:
        rh_path, rh_obj = search_attribute_matching_name_with_path(geom, "CellFaceIsRightHanded")[0]
        rh_arr = _read_array_np(rh_obj, energyml_object, f"geometry.{rh_path}", ws).astype(bool)
    except (IndexError, Exception) as exc:
        logging.debug(f"UnstructuredGridRepresentation: CellFaceIsRightHanded not readable: {exc}")

    # --- BUILD VTK_POLYHEDRON CELL ARRAY ---
    # VTK polyhedron flat format per cell:
    #   [total_vals, n_faces, n_pts_f0, p0, p1, ..., n_pts_f1, p0, ...]
    # where total_vals = 1 + n_faces + sum(1 + n_pts_fi for each face).
    cells_flat: List[int] = []
    rh_global_idx = 0

    for face_idxs in faces_per_cell:
        face_idxs = face_idxs.astype(np.int64)
        cell_inner: List[int] = [int(len(face_idxs))]  # n_faces
        for fi in face_idxs:
            fi = int(fi)
            if fi >= len(nodes_per_face):
                rh_global_idx += 1
                continue
            node_idxs = nodes_per_face[fi].astype(np.int64)
            if rh_arr is not None and rh_global_idx < len(rh_arr) and not rh_arr[rh_global_idx]:
                node_idxs = node_idxs[::-1]  # flip to outward normal
            rh_global_idx += 1
            cell_inner.append(int(len(node_idxs)))
            cell_inner.extend(int(x) for x in node_idxs)
        cells_flat.append(len(cell_inner))  # total size of this cell entry
        cells_flat.extend(cell_inner)

    cells = np.array(cells_flat, dtype=np.int64)
    cell_types = np.full(cell_count, _VTK_POLYHEDRON, dtype=np.uint8)

    if use_crs_displacement and crs is not None and len(points) > 0:
        apply_from_crs_info(points, extract_crs_info(crs, workspace), inplace=True)

    label = f"{src_type}_patch_0"
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )
    multi.patches.append(
        NumpyVolumeMesh(
            identifier=label,
            energyml_object=energyml_object,
            crs_object=crs,
            points=points,
            cells=cells,
            cell_types=cell_types,
            patch_index=0,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
    )
    return multi


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------


def read_numpy_mesh_object(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Dispatcher — equivalent to :func:`mesh.read_mesh_object` but returns
    a :class:`NumpyMultiMesh` container.

    Args:
        energyml_object: Any supported RESQML/EnergyML geometry/representation object.
        workspace:        Storage interface (``Epc`` or ``EpcStreamReader``).
        use_crs_displacement: When ``True`` (default), applies
                          :func:`crs_displacement_np` to the points of every
                          returned mesh (excluding wellbore representations
                          which apply the transform internally).
        sub_indices:      Optional list of face/line/point indices to include.

    Returns:
        :class:`NumpyMultiMesh` containing one or more :class:`NumpyMesh` patches
        (and/or nested children for ``RepresentationSetRepresentation``).

    Raises:
        :exc:`energyml.utils.exception.NotSupportedError`: if the object type
        has no registered reader.
    """
    if isinstance(energyml_object, list):
        # Synthetic container aggregating multiple top-level objects.
        synthetic = NumpyMultiMesh(identifier="multi_object_list")
        for obj in energyml_object:
            synthetic.children.append(
                read_numpy_mesh_object(
                    energyml_object=obj,
                    workspace=workspace,
                    use_crs_displacement=use_crs_displacement,
                    sub_indices=sub_indices,
                )
            )
        return synthetic

    type_name = _numpy_mesh_name_mapping(type(energyml_object).__name__)
    reader_func = get_numpy_reader_function(type_name)

    if reader_func is None:
        from energyml.utils.exception import NotSupportedError as _NSE

        raise _NSE(
            f"No numpy mesh reader found for type '{type_name}'. "
            f"Expected function 'read_numpy_{snake_case(type_name)}' in {__name__}."
        )

    result: NumpyMultiMesh = reader_func(
        energyml_object=energyml_object,
        workspace=workspace,
        sub_indices=sub_indices,
        use_crs_displacement=use_crs_displacement,
    )

    # Apply fallback CRS displacement for readers that do NOT handle it
    # internally (e.g. Grid2d which has no per-patch CRS apply call yet).
    _tn = type_name.lower()
    if (
        use_crs_displacement
        and "wellbore" not in _tn
        and "triangulated" not in _tn  # per-patch CRS applied inside reader
        and "point" not in _tn  # per-patch CRS applied inside reader
        and "polyline" not in _tn  # per-patch CRS applied inside reader
        and "representationset" not in _tn  # each child already had CRS applied
        and "subrepresentation" not in _tn  # delegates entirely to inner call
        and "planeset" not in _tn  # per-patch CRS applied inside reader
        and "seismicwellbore" not in _tn  # delegates to wellbore reader
        and "sealedsurface" not in _tn  # delegates to representation-set reader
        and "unstructuredgrid" not in _tn  # per-patch CRS applied inside reader
        and "ijkgrid" not in _tn  # per-patch CRS applied inside reader
    ):
        for m in result.flat_patches():
            crs = m.crs_object[0] if isinstance(m.crs_object, list) and m.crs_object else m.crs_object
            if crs is not None and len(m.points) > 0:
                crs_displacement_np(m.points, crs, inplace=True)

    return result


# ---------------------------------------------------------------------------
# PyVista converters
# ---------------------------------------------------------------------------


def _import_pyvista() -> Any:
    """Import PyVista and apply forward-compatibility fixes.

    PyVista 0.43 deprecated ``PolyData.n_faces`` (which used to return the
    total cell count, equivalent to ``n_cells``); PyVista 0.46 converted that
    deprecation into a hard ``AttributeError``.  Calling
    ``use_strict_n_faces(True)`` opts into the new, permanent semantics where
    ``n_faces`` returns only the polygon (face) count — identical to
    ``n_faces_strict`` — rather than raising an error.

    This is safe to call multiple times; the flag is a class-level boolean on
    ``pyvista.PolyData`` and the call is idempotent.
    """
    try:
        import pyvista as pv  # type: ignore[import]
    except ImportError as exc:
        raise ImportError("pyvista is not installed.  Install it with: pip install pyvista") from exc
    # Enable strict n_faces mode: makes n_faces return n_faces_strict (polygon
    # count) instead of raising AttributeError in PyVista >= 0.46.
    if hasattr(pv.PolyData, "use_strict_n_faces"):
        pv.PolyData.use_strict_n_faces(True)
    return pv


def numpy_mesh_to_pyvista(mesh: NumpyMesh) -> Any:
    """Convert a :class:`NumpyMesh` to the appropriate PyVista dataset.

    Connectivity arrays are passed **without copying** when pyvista accepts
    them directly (which it does for properly formatted VTK flat arrays).

    Requires ``pyvista`` to be installed (``pip install pyvista``).  When
    pyvista is absent a helpful :exc:`ImportError` is raised rather than a
    silent failure.

    Mapping:
    * :class:`NumpyPointSetMesh`  → ``pyvista.PolyData(points)``
    * :class:`NumpyPolylineMesh`  → ``pyvista.PolyData(points, lines=lines)``
    * :class:`NumpySurfaceMesh`   → ``pyvista.PolyData(points, faces=faces)``
    * :class:`NumpyVolumeMesh`    → ``pyvista.UnstructuredGrid(cells, cell_types, points)``
    """
    pv = _import_pyvista()

    pts = mesh.points  # (N, 3) float64 — no copy

    if isinstance(mesh, NumpyVolumeMesh):
        return pv.UnstructuredGrid(mesh.cells, mesh.cell_types, pts)
    if isinstance(mesh, NumpySurfaceMesh):
        return pv.PolyData(pts, faces=mesh.faces)
    if isinstance(mesh, NumpyPolylineMesh):
        return pv.PolyData(pts, lines=mesh.lines)
    if isinstance(mesh, NumpyPointSetMesh):
        return pv.PolyData(pts)

    # Generic fallback: just export points
    logging.warning(f"numpy_mesh_to_pyvista: unknown mesh type {type(mesh).__name__}, exporting points only.")
    return pv.PolyData(pts)


def numpy_multi_mesh_to_pyvista(multi: "NumpyMultiMesh") -> Any:
    """Convert a :class:`NumpyMultiMesh` to a ``pyvista.MultiBlock``.

    The resulting ``MultiBlock`` mirrors the two-level hierarchy of
    :class:`NumpyMultiMesh`:

    * Child containers (e.g. ``RepresentationSetRepresentation`` members) become
      nested ``MultiBlock`` blocks, keyed by their ``identifier``.
    * Direct patches become leaf ``PolyData`` / ``UnstructuredGrid`` blocks,
      keyed by ``patch_label`` or ``"patch_{patch_index}"``.

    Requires ``pyvista`` to be installed (``pip install pyvista``).
    """
    pv = _import_pyvista()

    block: pv.MultiBlock = pv.MultiBlock()
    for child in multi.children:
        block.append(numpy_multi_mesh_to_pyvista(child), child.identifier or "child")
    for patch in multi.patches:
        ds = numpy_mesh_to_pyvista(patch)
        if ds is not None:
            name = patch.patch_label or (f"patch_{patch.patch_index}" if patch.patch_index is not None else "patch")
            block.append(ds, name)
    return block


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    # Dataclasses
    "NumpyMesh",
    "NumpyPointSetMesh",
    "NumpyPolylineMesh",
    "NumpySurfaceMesh",
    "NumpyVolumeMesh",
    "NumpyMultiMesh",
    # CRS
    "crs_displacement_np",
    # Readers
    "read_numpy_mesh_object",
    "read_numpy_point_representation",
    "read_numpy_polyline_representation",
    "read_numpy_triangulated_set_representation",
    "read_numpy_grid2d_representation",
    "read_numpy_wellbore_trajectory_representation",
    "read_numpy_wellbore_frame_representation",
    "read_numpy_sub_representation",
    "read_numpy_representation_set_representation",
    "read_numpy_plane_set_representation",
    "read_numpy_seismic_wellbore_frame_representation",
    "read_numpy_sealed_surface_framework_representation",
    "read_numpy_ijk_grid_representation",
    "read_numpy_unstructured_grid_representation",
    # Converters
    "numpy_mesh_to_pyvista",
    "numpy_multi_mesh_to_pyvista",
]
