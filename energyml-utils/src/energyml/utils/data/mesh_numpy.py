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
from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np

from energyml.utils.data.helper import (
    apply_crs_transform,
    generate_vertical_well_points,
    get_crs_offsets_and_angle,
    get_crs_obj,
    get_crs_origin_offset,
    get_datum_information,
    is_z_reversed,
    read_array,
    read_grid2d_patch,
    read_parametric_geometry,
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
                keep_ranges = [
                    np.arange(int(pt_offsets[i]), int(pt_offsets[i + 1]), dtype=np.int64)
                    for i in _valid
                ]
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


def read_numpy_ijk_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Stub — IjkGridRepresentation is not yet implemented."""
    raise NotSupportedError(
        "IjkGridRepresentation is not yet supported in mesh_numpy. "
        "Contributions welcome — see TODO in mesh.py for the cell-corner extraction algorithm."
    )


def read_numpy_unstructured_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Stub — UnstructuredGridRepresentation is not yet implemented."""
    raise NotSupportedError(
        "UnstructuredGridRepresentation is not yet supported in mesh_numpy. "
        "Contributions welcome — see TODO in mesh.py for the cell list extraction algorithm."
    )


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
    ):
        for m in result.flat_patches():
            crs = m.crs_object[0] if isinstance(m.crs_object, list) and m.crs_object else m.crs_object
            if crs is not None and len(m.points) > 0:
                crs_displacement_np(m.points, crs, inplace=True)

    return result


# ---------------------------------------------------------------------------
# PyVista converters
# ---------------------------------------------------------------------------


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
    try:
        import pyvista as pv  # type: ignore[import]
    except ImportError as exc:
        raise ImportError("pyvista is not installed.  " "Install it with: pip install pyvista") from exc

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
    try:
        import pyvista as pv  # type: ignore[import]
    except ImportError as exc:
        raise ImportError("pyvista is not installed.  Install it with: pip install pyvista") from exc

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
    "read_numpy_ijk_grid_representation",
    "read_numpy_unstructured_grid_representation",
    # Converters
    "numpy_mesh_to_pyvista",
    "numpy_multi_mesh_to_pyvista",
]
