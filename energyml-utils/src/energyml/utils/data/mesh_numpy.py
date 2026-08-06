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
* **Best-effort zero-copy read** - geometry is read via
  :meth:`EnergymlStorageInterface.read_array_view`.  For contiguous,
  uncompressed HDF5 datasets this returns a numpy view backed directly by the
  memory-mapped file buffer (no RAM copy).  Chunked / compressed datasets fall
  back silently to a copy.

  That view must **not** be mutated (it is the reader's own buffer, possibly the
  mapped file), so ``_ensure_float64_points`` takes ownership of the *points*
  before any CRS transform is applied in place: exactly one full-size copy per
  patch, and none at all when no transform is requested
  (``frame=PointFrame.LOCAL``).  Connectivity arrays keep the zero-copy path —
  they are only ever read.

* **Explicit coordinate frame** - every patch carries the
  :class:`~energyml.utils.data.crs.PointFrame` its points are in, so
  ``read_numpy_mesh_object`` applies only the missing pipeline stages and a
  transform can never be applied twice.
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

import logging
import re
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np

from energyml.utils.data.helper import (
    evaluate_parametric_line_array,
    generate_vertical_well_points,
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
from energyml.utils.data.crs import (
    PointFrame,
    apply_from_crs_info,
    extract_crs_info,
    to_frame,
)
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

logger = logging.getLogger(__name__)

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
    #: Coordinate frame ``points`` is expressed in. Readers set it to what they produced, and
    #: :func:`read_numpy_mesh_object` only applies the stages still missing — so a CRS transform
    #: cannot be applied twice, whatever the representation type.
    frame: PointFrame = field(default=PointFrame.LOCAL)
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

    .. deprecated::
        Use :func:`~energyml.utils.data.crs.to_frame` instead. This function only applies the
        offsets and the Z flip — **not** the areal rotation nor the axis-order swap — so it does
        not produce coordinates in the projected CRS. It used to be the dispatcher's fallback,
        which is why a ``Grid2dRepresentation`` came out un-rotated from the numpy stack while the
        same object came out rotated from :mod:`mesh`. It is kept because it is part of the public
        API, but no reader calls it any more.

    Operates on an ``(N, 3)`` numpy array using broadcast arithmetic — no
    Python-level loops.

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


def _ensure_float64_points(arr: Any, *, own: bool = True) -> np.ndarray:
    """Convert *arr* to ``(N, 3) float64``, owning the buffer by default.

    Accepts numpy arrays (any shape that contains N*3 elements) or nested Python lists.

    ``own=True`` (default) guarantees the result is a writeable array backed by memory this
    module allocated. That matters because the geometry may arrive from
    :meth:`EnergymlStorageInterface.read_array_view`, whose contract is explicit — *"the caller
    must not mutate the returned array"*: for a contiguous uncompressed HDF5 dataset it is a view
    on the memory-mapped file, and the CRS transform is applied in place. Mutating it would either
    raise (read-only buffer) or corrupt the reader's cache, so that a second read of the same
    array would come back already transformed.

    Pass ``own=False`` only when the caller immediately copies anyway (e.g. feeding
    :func:`numpy.concatenate`), to save one full-size buffer.
    """
    a = np.asarray(arr, dtype=np.float64)

    # `base is not None` means we are looking at a view of someone else's buffer; a non-writeable
    # array cannot be transformed in place either. In both cases we must own a copy first.
    if own and (a.base is not None or not a.flags.writeable):
        a = a.copy()

    if a.ndim == 1:
        a = a.reshape(-1, 3)
    elif a.ndim == 2 and a.shape[1] == 2:
        # A 2-column array is ambiguous. RESQML point arrays are 3-component, and some datasets
        # store them with a shape that does not reflect that — ``80wells_surf_modified_val_color``
        # holds 4 XYZ points in a (6, 2) dataset. So a size divisible by 3 is read as XYZ, which
        # is what the legacy reader did with its plain reshape(-1, 3); only a size that cannot be
        # XYZ is treated as 2-D points (seismic / plan view) and padded with a zero Z.
        if a.size % 3 == 0:
            a = a.reshape(-1, 3)
        else:
            a = np.column_stack([a, np.zeros(len(a), dtype=np.float64)])
    elif a.ndim == 2 and a.shape[1] != 3:
        raise ValueError(f"Expected (N, 2) or (N, 3) points array, got shape {a.shape}")
    return a


def _local_to_projected(
    points: np.ndarray,
    crs: Any,
    workspace: Optional[EnergymlStorageInterface],
    use_crs_displacement: bool,
) -> PointFrame:
    """Apply the local → projected transform to *points* in place and report the frame reached.

    Readers call this instead of :func:`apply_from_crs_info` so that the frame they produced is
    recorded on the mesh. :func:`read_numpy_mesh_object` then tops the points up to the requested
    frame, and a transform can never be applied twice — which is what the hard-coded list of type
    names used to guard, one entry per reader.
    """
    if not use_crs_displacement or crs is None or len(points) == 0:
        return PointFrame.LOCAL
    return to_frame(
        points,
        extract_crs_info(crs, workspace),
        PointFrame.PROJECTED,
        PointFrame.LOCAL,
        inplace=True,
    ).frame


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


def _build_vtk_single_polyline(n_points: int) -> np.ndarray:
    """Build a VTK flat lines array holding *one* polyline through all *n_points* nodes.

    Result: ``[n, 0, 1, …, n-1]``.

    This is what a ``PolylineRepresentation`` without ``NodeCountPerPolyline`` means: a single
    polyline, not a bag of independent segments. :func:`_build_vtk_lines_from_segments` encodes the
    same geometry as ``n-1`` two-point cells, which renders identically but is a different
    topology — and produces one OBJ/OFF element per segment instead of one per line.
    """
    if n_points < 2:
        return np.empty(0, dtype=np.int64)
    part = np.empty(n_points + 1, dtype=np.int64)
    part[0] = n_points
    part[1:] = np.arange(n_points, dtype=np.int64)
    return part


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


def _fit_grid_dimensions(sa_count: int, fa_count: int, nb_points: int) -> Tuple[int, int]:
    """Reconcile the declared axis counts of a Grid2d patch with the points actually read.

    ``SlowestAxisCount`` / ``FastestAxisCount`` sometimes disagree with the length of the
    points array (truncated dataset, count declared on the representation rather than on the
    patch, …).  The fastest-axis count defines the row stride of the connectivity, so it is
    kept and the slowest-axis count is derived from it.  The result always satisfies
    ``sa * fa <= nb_points``, which is what keeps the generated indices in range.

    Both readers previously decremented (then re-incremented) *both* counts until the product
    fitted, which changed the grid shape and, with ``keep_holes=True``, could emit indices past
    the end of the points array.

    Returns:
        The (possibly adjusted) ``(sa_count, fa_count)``; ``(0, 0)`` when no face can be built.
    """
    if fa_count <= 0 or sa_count <= 0 or nb_points <= 0:
        logger.warning(
            f"Grid2d patch: unusable dimensions (slowest={sa_count}, fastest={fa_count}, "
            f"{nb_points} points) — no face is generated."
        )
        return 0, 0

    if sa_count * fa_count == nb_points:
        return sa_count, fa_count

    fitted_sa = nb_points // fa_count
    logger.warning(
        f"Grid2d patch: {sa_count} x {fa_count} = {sa_count * fa_count} nodes declared but "
        f"{nb_points} points read — keeping the fastest axis ({fa_count}) and using "
        f"{fitted_sa} for the slowest one."
    )
    return fitted_sa, fa_count


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
    """Normalise the energyml type name to match a ``read_numpy_<name>`` function.

    Accepts a python class name (``ObjTriangulatedSetRepresentation``), a schema type
    (``obj_TriangulatedSetRepresentation``, the RESQML 2.0.1 spelling) and a qualified type
    (``resqml20.obj_TriangulatedSetRepresentation``) alike.
    """
    arr_type_name = arr_type_name.rsplit(".", 1)[-1]
    arr_type_name = arr_type_name.replace("3D", "3d").replace("2D", "2d")
    arr_type_name = re.sub(r"^[Oo]bj_?([A-Z])", r"\1", arr_type_name)
    arr_type_name = re.sub(r"(Polyline|Point)Set", r"\1", arr_type_name)
    return arr_type_name


@lru_cache(maxsize=None)
def get_numpy_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """Return the ``read_numpy_<type>`` function for *mesh_type_name*, or ``None``.

    A cached ``getattr`` rather than a scan of the module members: the dispatcher runs once per
    object, and ``inspect.getmembers`` sorts and reads *every* attribute of the module on each
    call — measurable when listing the exportable objects of a large EPC.

    Only functions defined in this module are eligible, so an imported helper can never be
    mistaken for a reader (see :func:`mesh.get_object_reader_function`).
    """
    reader = getattr(sys.modules[__name__], f"read_numpy_{snake_case(mesh_type_name)}", None)
    if not callable(reader) or getattr(reader, "__module__", None) != __name__:
        return None
    return reader


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
            # total_size must advance by the number of points this patch *contributes to the
            # global numbering*, not by the number that survived the filter — otherwise every
            # subsequent patch shifts its sub_indices window.
            patch_size = len(points)
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < patch_size)
            points = points[t_idx[mask]]
            total_size += patch_size

        frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

        label = f"{src_type}_patch_{patch_idx}"
        multi.patches.append(
            NumpyPointSetMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=points,
                frame=frame,
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
            logger.error(f"Cannot find points for patch {patch_path_in_obj}")
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
            # No NodeCountPerPolyline: the patch is a single polyline through all its points.
            lines = _build_vtk_single_polyline(len(points))

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

        frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

        if len(points) > 0:
            label = f"{src_type}_patch_{patch_idx}"
            multi.patches.append(
                NumpyPolylineMesh(
                    identifier=label,
                    energyml_object=energyml_object,
                    crs_object=crs,
                    points=points,
                    lines=lines,
                    frame=frame,
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
            # own=False: np.concatenate below allocates the owned buffer anyway, even for a
            # single part, so taking ownership here would cost one extra full-size copy.
            pts_parts.append(_ensure_float64_points(raw, own=False))

        if not pts_parts:
            patch_idx += 1
            continue
        points = np.concatenate(pts_parts, axis=0)  # (N, 3), owned

        frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

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

        # sub_indices face filtering — total_size advances by the patch's own face count, not by
        # the number of faces that survived the filter (see read_numpy_point_representation).
        patch_face_count = len(triangles)
        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < patch_face_count)
            triangles = triangles[t_idx[mask]]
        total_size += patch_face_count

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
                frame=frame,
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

        # Reconcile the declared dimensions with the points actually read
        total_pts = len(pts)
        sa, fa = _fit_grid_dimensions(sa, fa, total_pts)
        if sa == 0 or fa == 0:
            return None

        z_col = pts[:, 2]
        nan_mask = np.isnan(z_col)  # True where Z is NaN (hole)

        if keep_holes:
            pts[nan_mask, 2] = 0.0
            final_pts = pts
            remap = None  # every original index stays valid: no remapping needed
        else:
            valid_mask = ~nan_mask
            final_pts = pts[valid_mask]
            # remap[original_index] = final_index (-1 ⟹ invalid/NaN)
            remap = np.full(total_pts, -1, dtype=np.int64)
            remap[valid_mask] = np.arange(valid_mask.sum(), dtype=np.int64)

        # Build the quad connectivity. The corner indices of every cell are an affine function of
        # (sa_i, fa_i), so the whole (sa-1) x (fa-1) grid is one broadcast instead of a Python
        # double loop with a list append per cell.
        if sa < 2 or fa < 2:
            return None
        sa_i = np.arange(sa - 1, dtype=np.int64).reshape(-1, 1)  # (sa-1, 1)
        fa_i = np.arange(fa - 1, dtype=np.int64).reshape(1, -1)  # (1, fa-1)
        corner_a = (sa_i * fa + fa_i).ravel()
        quads = np.empty((corner_a.size, 4), dtype=np.int64)
        quads[:, 0] = corner_a
        quads[:, 1] = corner_a + 1
        quads[:, 2] = corner_a + fa + 1
        quads[:, 3] = corner_a + fa

        if not keep_holes:
            # remap sends a NaN node to -1; a cell survives only when its four corners do.
            quads = remap[quads]
            quads = quads[(quads >= 0).all(axis=1)]

        if len(quads) == 0:
            return None

        # sub_indices filtering — total_size advances by the patch's own quad count (see
        # read_numpy_point_representation).
        patch_quad_count = len(quads)
        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < patch_quad_count)
            quads = quads[t_idx[mask]]
        total_size += patch_quad_count

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
            logger.error(e)
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
        logger.debug("Could not get CRS from trajectory geometry")

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
        logger.debug(f"Could not resolve MdDatum from trajectory: {e}")

    # The two paths below do not produce the same frame, which is why this reader could never be
    # handled by the generic CRS pass: the parametric geometry is local and gets transformed,
    # whereas the vertical fallback is built from the MD datum, whose coordinates
    # (get_datum_information) are *already* expressed in the projected CRS.
    frame = PointFrame.LOCAL
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
            frame = PointFrame.PROJECTED
    except Exception as e:
        mds = wellbore_frame_mds
        if mds is None:
            # A trajectory may carry no geometry at all and only declare the interval it spans
            # — `MdInterval` plus the `Datum` it is measured from. That is enough to place a
            # vertical well, and it is how every wellbore of a "MD interval only" package is
            # written; raising here dropped all of them.
            md_min = get_object_attribute(energyml_object, "md_interval.md_min")
            md_max = get_object_attribute(energyml_object, "md_interval.md_max")
            if md_min is not None and md_max is not None:
                logger.info(
                    f"WellboreTrajectoryRepresentation {get_obj_uuid(energyml_object)} has no geometry; "
                    f"building a vertical well from MdInterval [{md_min}, {md_max}]."
                )
                mds = np.array([float(md_min), float(md_max)], dtype=np.float64)

        if mds is not None:
            logger.debug(f"Trajectory parametric geometry unavailable, treating as vertical: {e}")
            well_points_list = generate_vertical_well_points(
                head_x=head_x,
                head_y=head_y,
                head_z=head_z,
                wellbore_mds=mds if isinstance(mds, np.ndarray) else np.asarray(mds),
                z_increasing_downward=z_increasing_downward,
            )
            # Built from the datum: already projected, whatever use_crs_displacement says.
            frame = PointFrame.PROJECTED
        else:
            raise ValueError(
                "Cannot read WellboreTrajectoryRepresentation: no parametric geometry, no measured "
                "depth information and no MdInterval available."
            ) from e

    if well_points_list is None or len(well_points_list) == 0:
        return NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(get_obj_uri(energyml_object)),
            source_uuid=get_obj_uuid(energyml_object),
            source_type=type(energyml_object).__name__,
        )

    pts = _ensure_float64_points(np.asarray(well_points_list, dtype=np.float64))
    # A trajectory is *one* polyline through its stations, not a bag of independent two-point
    # cells. Both encodings render the same, but the segment one makes every consumer that
    # iterates the cells — the GeoJSON writer, OBJ, OFF — produce N-1 elements for one well.
    lines = _build_vtk_single_polyline(len(pts))
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
                frame=frame,
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
        logger.warning(f"Could not read NodeMd from wellbore frame: {e}")
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
    # The geometry comes from the trajectory, but the patches were produced by reading *this*
    # frame, and that is what they must report — like every other reader. Leaving the trajectory
    # on them made a frame reached through a RepresentationSetRepresentation indistinguishable
    # from the trajectory itself.
    for m in result.flat_patches():
        m.identifier = frame_uri
        m.energyml_object = energyml_object
        m.source_uuid = get_obj_uuid(energyml_object)
        m.source_type = type(energyml_object).__name__
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
        # total_size advances by the patch's own index count (see read_numpy_point_representation).
        patch_index_count = len(arr)
        if sub_indices is not None and len(sub_indices) > 0:
            t_idx = np.asarray(sub_indices, dtype=np.int64) - total_size
            mask = (t_idx >= 0) & (t_idx < patch_index_count)
            arr = arr[t_idx[mask]]
        total_size += patch_index_count
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
            logger.error(f"Representation {rpr_uri} not found in RepresentationSetRepresentation")
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

_VTK_EMPTY_CELL = 0
_VTK_HEXAHEDRON = 12
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
    except Exception as exc:
        # `(ObjectNotFoundNotError, Exception)` was just `Exception` with misleading intent.
        # get_crs_obj can fail in several ways and a missing CRS is not fatal here.
        logger.debug(f"No CRS resolved: {type(exc).__name__}: {exc}")

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
            logger.warning(f"PlaneSetRepresentation: unknown geometry type {geom_type!r} — skipping patch {patch_idx}")
            patch_idx += 1
            continue

        frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

        label = f"{src_type}_patch_{patch_idx}"
        multi.patches.append(
            NumpySurfaceMesh(
                identifier=label,
                energyml_object=energyml_object,
                crs_object=crs,
                points=points,
                faces=faces,
                frame=frame,
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
    except Exception as exc:  # IndexError from [0] on an empty match, or any read failure
        logger.warning(f"SeismicWellboreFrameRepresentation: could not read NodeTimeValues: {exc}")
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


def _blank_undefined_pillars(
    points: np.ndarray,  # (NKL * n_pillars_total, 3), modified in place
    geom: Any,
    energyml_object: Any,
    ws: Any,
    nkl: int,
    n_pillars_base: int,
    n_pillars_total: int,
    pillar_indices_arr: Optional[np.ndarray],
) -> None:
    """Set the nodes of pillars flagged ``PillarGeometryIsDefined=false`` to NaN.

    RESQML makes the flag authoritative — "If the indicator does not indicate that the pillar
    geometry is defined, then this over-rides any other node geometry specification" — so the
    coordinates stored for such a pillar are meaningless and must not be drawn. The array is
    indexed by pillar (``#Pillars`` = ``(NI+1)(NJ+1)``, 1-D or 2-D), so a split coordinate line
    takes the flag of the pillar it was split from.

    A no-op when the flag is absent or every pillar is defined.
    """
    flag_results = search_attribute_matching_name_with_path(geom, "PillarGeometryIsDefined")
    if not flag_results:
        return
    flag_path, flag_obj = flag_results[0]
    if flag_obj is None:
        return
    try:
        defined = _read_array_np(flag_obj, energyml_object, f"geometry.{flag_path}", ws).astype(bool).ravel()
    except Exception as exc:
        logger.debug(f"Cannot read PillarGeometryIsDefined: {type(exc).__name__}: {exc}")
        return

    if defined.size != n_pillars_base:
        logger.warning(
            f"PillarGeometryIsDefined holds {defined.size} entries for {n_pillars_base} pillars; ignoring it."
        )
        return
    if defined.all():
        return

    # Map every coordinate line to its pillar, then to the flag.
    line_defined = np.ones(n_pillars_total, dtype=bool)
    line_defined[:n_pillars_base] = defined
    n_splits = n_pillars_total - n_pillars_base
    if n_splits > 0 and pillar_indices_arr is not None:
        pi = np.asarray(pillar_indices_arr, dtype=np.int64).ravel()[:n_splits]
        valid = (pi >= 0) & (pi < n_pillars_base)
        line_defined[n_pillars_base : n_pillars_base + len(pi)] = np.where(valid, defined[np.where(valid, pi, 0)], True)

    logger.info(
        f"IjkGridRepresentation: {int((~line_defined).sum())}/{n_pillars_total} coordinate lines "
        "flagged PillarGeometryIsDefined=false; their nodes are set to NaN."
    )
    points.reshape(nkl, n_pillars_total, 3)[:, ~line_defined, :] = np.nan


def _read_cell_geometry_undefined(
    geom: Any,
    energyml_object: Any,
    ws: Any,
    ni: int,
    nj: int,
    nk: int,
) -> Optional[np.ndarray]:
    """Return a ``(ni*nj*nk,)`` boolean mask of cells flagged ``CellGeometryIsDefined=false``.

    The array is cell-indexed, so it follows the grid's own ordering (I fastest, then J, then
    K) and lines up with the cells built by :func:`read_numpy_ijk_grid_representation` without
    any permutation. ``None`` when the flag is absent or unreadable.
    """
    flag_results = search_attribute_matching_name_with_path(geom, "CellGeometryIsDefined")
    if not flag_results:
        return None
    flag_path, flag_obj = flag_results[0]
    if flag_obj is None:
        return None
    try:
        defined = _read_array_np(flag_obj, energyml_object, f"geometry.{flag_path}", ws).astype(bool).ravel()
    except Exception as exc:
        logger.debug(f"Cannot read CellGeometryIsDefined: {type(exc).__name__}: {exc}")
        return None

    n_cells = ni * nj * nk
    if defined.size != n_cells:
        logger.warning(f"CellGeometryIsDefined holds {defined.size} entries for {n_cells} cells; ignoring it.")
        return None
    return ~defined


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
            f"or {expected_4d} (4-D layout, nkl={nkl}, nj+1={nj + 1}, ni+1={ni + 1})."
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
    pillar_indices_arr: Optional[np.ndarray] = None,
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
        logger.warning(
            f"Point3dParametricArray.parameters size {raw_params.size} does not match "
            f"expected {expected_3d} (3-D) or {expected_4d} (4-D). Attempting flat reshape."
        )
        query_params = raw_params.flatten()[: nkl * n_pillars_total].reshape(nkl, n_pillars_total)

    # --- 2. Handle optional parametric_line_indices ---
    # When present, each column index in query_params maps to a pillar index
    # in the ParametricLineArray (needed for grids with truncated or
    # non-contiguous pillar numbering).
    # ``ParametricLineIndices`` maps *array index → parametric line index*. It is optional
    # precisely because a column-layer grid already carries that mapping in
    # ``ColumnLayerSplitCoordinateLines.PillarIndices``: coordinate line c < nPillars is
    # pillar c, and split line nPillars+s reuses the line of pillar PillarIndices[s].
    #
    # The previous code permuted the *query* columns (``query_params[:, raw_pli]``) instead
    # of selecting lines, which reorders the grid nodes themselves, and it never derived the
    # implicit mapping at all — so a faulted parametric grid asked the evaluator for more
    # lines than the ParametricLineArray contains.
    line_indices: Optional[np.ndarray] = None
    pli_obj = getattr(pts_obj, "parametric_line_indices", None)
    if pli_obj is not None:
        raw_pli = _read_array_np(pli_obj, energyml_object, "geometry.Points.parametric_line_indices", ws)
        line_indices = raw_pli.astype(np.int64).flatten()
        if len(line_indices) != n_pillars_total:
            logger.warning(
                f"Point3dParametricArray.parametric_line_indices holds {len(line_indices)} "
                f"entries for {n_pillars_total} coordinate lines; ignoring it."
            )
            line_indices = None

    if line_indices is None:
        line_indices = np.arange(n_pillars_total, dtype=np.int64)
        n_splits = n_pillars_total - n_pillars_base
        if n_splits > 0:
            if pillar_indices_arr is None:
                logger.warning(
                    f"{n_splits} split coordinate line(s) but no "
                    "ColumnLayerSplitCoordinateLines.PillarIndices: their parametric lines "
                    "cannot be resolved."
                )
            else:
                pi = np.asarray(pillar_indices_arr, dtype=np.int64).flatten()
                line_indices[n_pillars_base : n_pillars_base + len(pi)] = pi[:n_splits]

    # --- 3. Handle optional truncated_line_indices ---
    tli_obj = getattr(pts_obj, "truncated_line_indices", None)
    if tli_obj is not None:
        logger.warning(
            "Point3dParametricArray.truncated_line_indices is present. "
            "Full truncated-pillar support is not yet implemented — "
            "truncation metadata will be ignored and results may be geometrically "
            "incorrect near truncated pillars."
        )

    # --- 4. Resolve ParametricLineArray ---
    pla_raw = getattr(pts_obj, "parametric_lines", None)
    if pla_raw is None:
        raise ValueError("Point3dParametricArray.parametric_lines is required but absent.")
    pla = resolve_parametric_line_array(pla_raw, energyml_object, ws, n_pillars_base)

    # --- 5. Evaluate pillar splines ---
    pts_3d = evaluate_parametric_line_array(
        pla=pla,
        root_obj=energyml_object,
        workspace=ws,
        query_parameters=query_params,
        ni=ni,
        nj=nj,
        line_indices=line_indices,
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
    * **Parametric pillars** — ``Point3dParametricArray`` is evaluated through
      :func:`~energyml.utils.data.helper.evaluate_parametric_line_array` (all six RESQML line
      kinds; kinds 2 and 4 need scipy). ``Point3dExternalArray`` — direct XYZ — is read as is.
    * **Handedness** — ``GridIsRighthanded`` decides the corner winding so the emitted
      hexahedra always have a positive Jacobian.
    * **Undefined geometry** — ``PillarGeometryIsDefined`` blanks the nodes of the flagged
      coordinate lines, ``CellGeometryIsDefined`` turns the flagged cells into VTK empty cells
      (kept in place, so cell-indexed properties still line up).

    Cells are emitted in the RESQML order — I fastest, then J, then K — which is the order the
    grid's cell-indexed properties use.

    Known limitation
    ----------------
    A grid whose geometry comes from a ``ParentWindow`` (LGR) instead of its own ``Geometry``
    is returned empty: the regridding of the parent's pillars is not implemented.
    """
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__

    ni = getattr(energyml_object, "ni", None)
    nj = getattr(energyml_object, "nj", None)
    nk = getattr(energyml_object, "nk", None)
    if ni is None or nj is None or nk is None:
        logger.warning("IjkGridRepresentation: ni/nj/nk not set — returning empty mesh")
        return NumpyMultiMesh(
            energyml_object=energyml_object,
            identifier=str(src_uuid),
            source_uuid=src_uuid,
            source_type=src_type,
        )
    ni, nj, nk = int(ni), int(nj), int(nk)

    geom = getattr(energyml_object, "geometry", None)
    if geom is None:
        if getattr(energyml_object, "parent_window", None) is not None:
            logger.warning(
                f"IjkGridRepresentation {src_uuid} is a local grid refinement: its geometry is "
                "inherited from the parent grid through ParentWindow, which is not implemented — "
                "returning an empty mesh."
            )
        else:
            logger.warning("IjkGridRepresentation has no geometry — returning empty mesh")
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
        logger.warning("IjkGridRepresentation: cannot find Points in geometry")
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
            pillar_indices_arr=pillar_indices_arr,
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

    # pts_3d may be a reshaped *view* of the workspace array (see _read_direct_points), and
    # astype(copy=False) would keep it that way — the CRS transform below writes in place.
    points = _ensure_float64_points(pts_3d.reshape(-1, 3))

    # --- CRS ---
    crs = None
    try:
        crs = get_crs_obj(
            context_obj=geom,
            path_in_root="geometry",
            root_obj=energyml_object,
            workspace=workspace,
        )
    except Exception as exc:
        # `(ObjectNotFoundNotError, Exception)` was just `Exception` with misleading intent.
        # get_crs_obj can fail in several ways and a missing CRS is not fatal here.
        logger.debug(f"No CRS resolved: {type(exc).__name__}: {exc}")

    # --- PILLAR MAP for faulted grids ---
    use_pillar_map = n_splits > 0 and pillar_indices_arr is not None
    pillar_map: Optional[np.ndarray] = None
    if use_pillar_map:
        pillar_map = _build_split_pillar_map(ni, nj, pillar_indices_arr, columns_per_split, n_splits)

    # --- PILLARS WITHOUT GEOMETRY ---
    # "Indicator that a pillar has at least one node with a defined cell geometry. [...] If the
    # indicator does not indicate that the pillar geometry is defined, then this over-rides any
    # other node geometry specification." The flag is indexed by *pillar*, so a split coordinate
    # line inherits the flag of the pillar it was split from.
    _blank_undefined_pillars(
        points=points,
        geom=geom,
        energyml_object=energyml_object,
        ws=ws,
        nkl=nkl,
        n_pillars_base=n_pillars_base,
        n_pillars_total=n_pillars_total,
        pillar_indices_arr=pillar_indices_arr,
    )

    # --- BUILD HEXAHEDRAL CELL CONNECTIVITY ---
    # Cell ordering is the RESQML one — I fastest, then J, then K — which is what every
    # cell-indexed array of the grid uses (properties, CellGeometryIsDefined, ...). The node
    # arrays observed in the files make the convention explicit: PillarGeometryIsDefined is
    # stored as (NJ+1, NI+1) and the point parameters as (NKL, NJ+1, NI+1).
    #
    # Neither previous path produced that order, and the two disagreed with each other: the
    # unfaulted branch enumerated K fastest then J then I, the faulted branch K fastest then I
    # then J. Any property read back onto the cells was therefore permuted, differently
    # depending on whether the grid happened to be faulted.
    ik_arr, ij_arr, ii_arr = np.meshgrid(
        np.arange(nk, dtype=np.int64),
        np.arange(nj, dtype=np.int64),
        np.arange(ni, dtype=np.int64),
        indexing="ij",
    )  # each shape (nk, nj, ni) → ravel() in C order gives I fastest, K slowest

    if pillar_map is None:
        p_tl = ij_arr * (ni + 1) + ii_arr
        p_tr = ij_arr * (ni + 1) + (ii_arr + 1)
        p_bl = (ij_arr + 1) * (ni + 1) + ii_arr
        p_br = (ij_arr + 1) * (ni + 1) + (ii_arr + 1)
    else:
        # The faulted case is a gather on the pre-built (nj, ni, 4) map — no Python loop needed.
        p_tl = pillar_map[ij_arr, ii_arr, 0]
        p_tr = pillar_map[ij_arr, ii_arr, 1]
        p_bl = pillar_map[ij_arr, ii_arr, 2]
        p_br = pillar_map[ij_arr, ii_arr, 3]

    kl_b = kl_bottom[ik_arr]
    kl_t = kl_top[ik_arr]

    # VTK requires the first four nodes to wind so that the right-hand-rule normal points at the
    # opposite face; otherwise the hexahedron has a negative Jacobian and its faces are inverted.
    # (I, J, K) is that orientation only when the grid is right-handed — which is exactly what
    # GridIsRighthanded reports, and the flag was ignored. rc/epc/80wells_surf_modified_val_color.epc
    # ships the pair "Four by Three by Two Left Handed" / "... Right Handed" for this: every cell
    # of the left-handed one came out inside-out.
    #
    # The flag describes the grid in the real-world sense, i.e. once the CRS has been applied.
    # These fixtures measure Z as a depth, so (X, Y, Z) is left-handed in the *local* frame and a
    # right-handed grid still has a negative Jacobian there; it comes out positive after the Z
    # flip of apply_from_crs_info. Orientation is therefore correct in the PROJECTED frame, which
    # is the default and the one a viewer renders.
    righthanded = getattr(geom, "grid_is_righthanded", None)
    if righthanded is None:
        logger.debug("IjkGridRepresentation: GridIsRighthanded absent, assuming right-handed.")
        righthanded = True
    base_corners = (p_tl, p_tr, p_br, p_bl) if righthanded else (p_tl, p_bl, p_br, p_tr)

    n_cells = ni * nj * nk
    node_cols = [(kl_b * n_pillars_total + p).ravel() for p in base_corners]
    node_cols += [(kl_t * n_pillars_total + p).ravel() for p in base_corners]
    rows = np.column_stack([np.full(n_cells, 8, dtype=np.int64), *node_cols])  # (n_cells, 9)

    cell_types = np.full(n_cells, _VTK_HEXAHEDRON, dtype=np.uint8)

    # --- CELLS WITHOUT GEOMETRY ---
    undefined = _read_cell_geometry_undefined(geom, energyml_object, ws, ni, nj, nk)
    if undefined is not None and undefined.any():
        logger.info(
            f"IjkGridRepresentation: {int(undefined.sum())}/{n_cells} cells flagged "
            "CellGeometryIsDefined=false; emitted as empty cells."
        )
        cell_types[undefined] = _VTK_EMPTY_CELL
        # An empty cell carries no node, so its row shrinks to the lone count prefix. Keeping the
        # cell *present* is what preserves the 1:1 match with the grid's cell-indexed properties.
        rows[undefined, 0] = 0
        keep = np.ones((n_cells, 9), dtype=bool)
        keep[undefined, 1:] = False
        cells = rows[keep]
    else:
        cells = rows.ravel()

    frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

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
            frame=frame,
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
        logger.warning("UnstructuredGridRepresentation has no geometry — returning empty mesh")
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
        logger.warning("UnstructuredGridRepresentation: cannot find Points in geometry")
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
    except Exception as exc:
        # `(ObjectNotFoundNotError, Exception)` was just `Exception` with misleading intent.
        # get_crs_obj can fail in several ways and a missing CRS is not fatal here.
        logger.debug(f"No CRS resolved: {type(exc).__name__}: {exc}")

    # --- JAGGED ARRAYS ---
    npf_obj = getattr(geom, "nodes_per_face", None)
    fpc_obj = getattr(geom, "faces_per_cell", None)
    if npf_obj is None or fpc_obj is None:
        logger.warning(
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
    except Exception as exc:  # IndexError from [0] on an empty match, or any read failure
        logger.debug(f"UnstructuredGridRepresentation: CellFaceIsRightHanded not readable: {exc}")

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

    frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

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
            frame=frame,
            patch_index=0,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
    )
    return multi


# ---------------------------------------------------------------------------
# Delegating readers
#
# These representations add semantics on top of a geometry another reader already produces.
# Dispatch is by function name, so each needs its own entry point even when the body is a
# single call — that is the registration.
# ---------------------------------------------------------------------------


def read_numpy_wellbore_marker_frame_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``WellboreMarkerFrameRepresentation`` — the markers positioned on their trajectory.

    "A well log frame where each entry represents a well marker": the geometry is a
    ``NodeMd`` list plus a ``Trajectory`` reference, exactly like
    :class:`WellboreFrameRepresentation`, so the frame reader handles it as is. The points of
    the returned polyline are the marker positions, in ``NodeMd`` order — index *i* is the
    position of ``wellbore_marker[i]``.
    """
    return read_numpy_wellbore_frame_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )


def read_numpy_blocked_wellbore_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``BlockedWellboreRepresentation`` as its trajectory sampled at the node MDs.

    A blocked wellbore is a ``WellboreFrameRepresentation`` whose intervals are annotated with
    the grid cells they cross (``IntervalGridCells``). The added information is topological, not
    geometric: the geometry is still ``NodeMd`` along ``Trajectory``.
    """
    return read_numpy_wellbore_frame_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )


def read_numpy_non_sealed_surface_framework_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``NonSealedSurfaceFrameworkRepresentation`` — its member representations.

    Like its sealed counterpart it is a ``RepresentationSetRepresentation`` subtype; the
    ``contacts`` it adds describe how the surfaces meet and carry no geometry of their own.
    """
    result = read_numpy_representation_set_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    result.source_type = type(energyml_object).__name__
    return result


def read_numpy_sealed_volume_framework_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``SealedVolumeFrameworkRepresentation`` — the surfaces bounding its regions.

    The object is a BREP: its ``regions`` assemble shells out of the surfaces of a sealed
    surface framework. Only the member representations are returned, i.e. the bounding
    surfaces; the region-to-shell assembly is not turned into closed volumes.
    """
    result = read_numpy_representation_set_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    result.source_type = type(energyml_object).__name__
    if getattr(energyml_object, "regions", None):
        logger.debug(
            "SealedVolumeFrameworkRepresentation: returning the bounding surfaces only; "
            "the volume regions are not assembled into closed shells."
        )
    return result


def read_numpy_grid2d_set_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``Grid2dSetRepresentation`` (RESQML 2.0.1) — one patch per member 2-D grid.

    "Set of representations based on a 2D grid. Each 2D grid representation corresponds to one
    patch of the set." :func:`read_numpy_grid2d_representation` already loops over every
    ``Grid2dPatch`` it finds, which is exactly the set's content.
    """
    result = read_numpy_grid2d_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    result.source_type = type(energyml_object).__name__
    return result


def read_numpy_unstructured_column_layer_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read an ``UnstructuredColumnLayerGridRepresentation`` as ``VTK_POLYHEDRON`` cells.

    "Grid whose topology is characterized by an unstructured column index and a layer index, K.
    Cell geometry is characterized by nodes on coordinate lines, where each column of the model
    may have an arbitrary number of sides."

    It is the IJK reader with the implicit ``(NI+1)(NJ+1)`` pillar lattice replaced by an
    explicit ``PillarsPerColumn`` list of lists, so everything else carries over: coordinate
    line nodes with NKL nodes per line, K-gaps, split coordinate lines, and the
    ``PillarGeometryIsDefined`` / ``CellGeometryIsDefined`` overrides.

    Each cell is emitted as a polyhedron — bottom face, top face and one quad per column edge —
    rather than a shape-specific VTK type, because ``ColumnShape`` may be ``polygonal``. Cells
    are ordered column fastest, then layer, which is the grid's own cell ordering.
    """
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    try:
        identifier = str(get_obj_uri(energyml_object))
    except Exception:
        identifier = str(src_uuid)
    multi = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=identifier,
        source_uuid=src_uuid,
        source_type=src_type,
    )

    nk = getattr(energyml_object, "nk", None)
    column_count = getattr(energyml_object, "column_count", None)
    geom = getattr(energyml_object, "geometry", None)
    if nk is None or column_count is None or geom is None:
        if geom is None and getattr(energyml_object, "parent_window", None) is not None:
            logger.warning(
                f"{src_type} {src_uuid} is a local grid refinement: its geometry is inherited "
                "through ParentWindow, which is not implemented — returning an empty mesh."
            )
        else:
            logger.warning(f"{src_type} {src_uuid}: nk / column_count / geometry missing — returning empty mesh.")
        return multi
    nk, column_count = int(nk), int(column_count)

    pillar_count = int(getattr(geom, "pillar_count", 0) or 0)
    ppc_obj = getattr(geom, "pillars_per_column", None)
    if ppc_obj is None:
        logger.warning(f"{src_type} {src_uuid}: PillarsPerColumn is required but absent.")
        return multi
    pillars_per_column = _decode_jagged_array(ppc_obj, energyml_object, "geometry.pillars_per_column", ws)
    if len(pillars_per_column) < column_count:
        logger.warning(
            f"{src_type} {src_uuid}: PillarsPerColumn describes {len(pillars_per_column)} columns "
            f"for ColumnCount={column_count}."
        )
        column_count = len(pillars_per_column)

    # --- K-GAPS (identical to the IJK case) ---
    kgaps_obj = getattr(energyml_object, "kgaps", None)
    gap_after: Optional[np.ndarray] = None
    n_kgaps = 0
    if kgaps_obj is not None:
        n_kgaps = int(getattr(kgaps_obj, "count", 0) or 0)
        gap_attr_list = search_attribute_matching_name_with_path(kgaps_obj, "GapAfterLayer")
        if gap_attr_list:
            gap_path, gap_obj = gap_attr_list[0]
            if gap_obj is not None:
                gap_after = _read_array_np(gap_obj, energyml_object, f"kgaps.{gap_path}", ws).astype(bool)
    nkl = nk + n_kgaps + 1
    kl_bottom, kl_top = _build_kl_mapping(nk, gap_after)

    # --- SPLIT COORDINATE LINES ---
    split_cl = getattr(geom, "column_layer_split_coordinate_lines", None)
    n_splits = 0
    pillar_indices_arr: Optional[np.ndarray] = None
    columns_per_split: List[np.ndarray] = []
    if split_cl is not None:
        n_splits = int(getattr(split_cl, "count", 0) or 0)
        if n_splits > 0:
            pi_list = [(p, o) for p, o in search_attribute_matching_name_with_path(split_cl, "PillarIndices") if o]
            if pi_list:
                pi_path, pi_obj = pi_list[0]
                pillar_indices_arr = _read_array_np(
                    pi_obj, energyml_object, f"geometry.column_layer_split_coordinate_lines.{pi_path}", ws
                )
            cps_obj = getattr(split_cl, "columns_per_split_coordinate_line", None)
            if cps_obj is not None:
                columns_per_split = _decode_jagged_array(
                    cps_obj,
                    energyml_object,
                    "geometry.column_layer_split_coordinate_lines.columns_per_split_coordinate_line",
                    ws,
                )

    n_lines = pillar_count + n_splits

    # --- POINTS ---
    pts_results = [(p, o) for p, o in search_attribute_matching_name_with_path(geom, "Points") if o is not None]
    if not pts_results:
        logger.warning(f"{src_type} {src_uuid}: cannot find Points in geometry.")
        return multi
    pts_path, pts_obj = pts_results[0]
    raw_pts = _read_array_np(pts_obj, energyml_object, f"geometry.{pts_path}", ws)
    if raw_pts.size != nkl * n_lines * 3:
        logger.warning(
            f"{src_type} {src_uuid}: points array holds {raw_pts.size} values, expected "
            f"NKL({nkl}) × lines({n_lines}) × 3 = {nkl * n_lines * 3}."
        )
        return multi
    points = _ensure_float64_points(raw_pts.reshape(-1, 3))

    _blank_undefined_pillars(
        points=points,
        geom=geom,
        energyml_object=energyml_object,
        ws=ws,
        nkl=nkl,
        n_pillars_base=pillar_count,
        n_pillars_total=n_lines,
        pillar_indices_arr=pillar_indices_arr,
    )

    crs = None
    try:
        crs = get_crs_obj(context_obj=geom, path_in_root="geometry", root_obj=energyml_object, workspace=workspace)
    except Exception as exc:
        logger.debug(f"No CRS resolved: {type(exc).__name__}: {exc}")

    # --- Corner coordinate line of every column, split lines substituted in ---
    corner_lines: List[np.ndarray] = [np.asarray(pillars_per_column[c], dtype=np.int64) for c in range(column_count)]
    if n_splits > 0 and pillar_indices_arr is not None:
        pi = np.asarray(pillar_indices_arr, dtype=np.int64).ravel()
        for s in range(min(n_splits, len(pi), len(columns_per_split))):
            replaced, new_line = int(pi[s]), pillar_count + s
            for col in np.asarray(columns_per_split[s], dtype=np.int64).ravel():
                col = int(col)
                if 0 <= col < column_count:
                    corner_lines[col] = np.where(corner_lines[col] == replaced, new_line, corner_lines[col])

    right_handed: Optional[np.ndarray] = None
    rh_obj = getattr(geom, "column_is_right_handed", None)
    if rh_obj is not None:
        try:
            right_handed = (
                _read_array_np(rh_obj, energyml_object, "geometry.column_is_right_handed", ws).astype(bool).ravel()
            )
        except Exception as exc:
            logger.debug(f"Cannot read ColumnIsRightHanded: {type(exc).__name__}: {exc}")

    undefined = _read_cell_geometry_undefined(geom, energyml_object, ws, column_count, 1, nk)

    # --- Cells: column fastest, then layer ---
    cells_flat: List[int] = []
    cell_types: List[int] = []
    for k in range(nk):
        kb, kt = int(kl_bottom[k]) * n_lines, int(kl_top[k]) * n_lines
        for col in range(column_count):
            cell_idx = k * column_count + col
            lines_of_col = corner_lines[col]
            n_side = len(lines_of_col)
            if (undefined is not None and cell_idx < len(undefined) and undefined[cell_idx]) or n_side < 3:
                cells_flat.append(0)
                cell_types.append(_VTK_EMPTY_CELL)
                continue
            bottom = [kb + int(p) for p in lines_of_col]
            top = [kt + int(p) for p in lines_of_col]
            # The bottom face is wound the other way round so both K faces point out of the cell.
            faces: List[List[int]] = [list(reversed(bottom)), list(top)]
            for i in range(n_side):
                j = (i + 1) % n_side
                faces.append([bottom[i], bottom[j], top[j], top[i]])
            # "List of columns that are right handed" — the flag is per column, not per cell.
            if right_handed is not None and col < len(right_handed) and not right_handed[col]:
                faces = [list(reversed(f)) for f in faces]
            body: List[int] = [len(faces)]
            for f in faces:
                body.append(len(f))
                body.extend(f)
            cells_flat.append(len(body))
            cells_flat.extend(body)
            cell_types.append(_VTK_POLYHEDRON)

    frame = _local_to_projected(points, crs, workspace, use_crs_displacement)
    label = f"{src_type}_patch_0"
    multi.patches.append(
        NumpyVolumeMesh(
            identifier=label,
            energyml_object=energyml_object,
            crs_object=crs,
            points=points,
            cells=np.array(cells_flat, dtype=np.int64),
            cell_types=np.array(cell_types, dtype=np.uint8),
            frame=frame,
            patch_index=0,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
    )
    return multi


def read_numpy_truncated_unstructured_column_layer_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``TruncatedUnstructuredColumnLayerGridRepresentation`` — its untruncated geometry.

    Same relation as ``TruncatedIjkGridRepresentation`` to ``IjkGridRepresentation``: the base
    ``UnstructuredColumnLayerGridGeometry`` is read in full, the ``TruncationCellPatch`` is not
    applied.
    """
    if getattr(energyml_object, "truncation_cell_patch", None) is not None:
        logger.warning(
            f"{type(energyml_object).__name__} {get_obj_uuid(energyml_object)}: the TruncationCellPatch "
            "is not applied — the truncated cells are returned in their untruncated form."
        )
    result = read_numpy_unstructured_column_layer_grid_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    result.source_type = type(energyml_object).__name__
    return result


def read_numpy_truncated_ijk_grid_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``TruncatedIjkGridRepresentation`` — its untruncated IJK geometry.

    The type is "a grid class with an underlying IJK topology, together with a 1D split-cell
    list", and it carries the same ``ni``/``nj``/``nk`` and ``IjkGridGeometry`` as a plain IJK
    grid. That base geometry is read here in full.

    ``TruncationCellPatch`` is **not** applied: it replaces some hexahedra with arbitrary
    polyhedra ("the truncated IJK cells have more than the usual 6 faces"). The truncated cells
    are therefore returned in their untruncated form, which is reported once per object.
    """
    if getattr(energyml_object, "truncation_cell_patch", None) is not None:
        logger.warning(
            f"TruncatedIjkGridRepresentation {get_obj_uuid(energyml_object)}: the TruncationCellPatch "
            "is not applied — the truncated cells are returned as full hexahedra."
        )
    result = read_numpy_ijk_grid_representation(
        energyml_object=energyml_object,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    result.source_type = type(energyml_object).__name__
    return result


def _read_numpy_via_supporting_representation(
    energyml_object: Any,
    attribute: str,
    workspace: Optional[EnergymlStorageInterface],
    use_crs_displacement: bool,
    sub_indices: Optional[Union[List[int], np.ndarray]],
) -> "NumpyMultiMesh":
    """Read the representation referenced by *attribute* and re-stamp it as *energyml_object*.

    Used by the representations that hold no geometry at all and simply point at the one that
    does. The patches must report the referencing object, not the referenced one, so that a
    caller can tell them apart — the same rule the wellbore-frame reader follows.
    """
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__
    empty = NumpyMultiMesh(
        energyml_object=energyml_object,
        identifier=str(get_obj_uri(energyml_object)),
        source_uuid=src_uuid,
        source_type=src_type,
    )

    dor = getattr(energyml_object, attribute, None)
    if dor is None:
        found = search_attribute_matching_name(obj=energyml_object, name_rgx=attribute)
        dor = found[0] if found else None
    if dor is None or workspace is None:
        logger.warning(f"{src_type} {src_uuid}: no '{attribute}' to take the geometry from.")
        return empty

    target = workspace.get_object(get_obj_uri(dor))
    if target is None:
        logger.warning(f"{src_type} {src_uuid}: {get_obj_uri(dor)} not found in the workspace.")
        return empty

    result = read_numpy_mesh_object(
        energyml_object=target,
        workspace=workspace,
        use_crs_displacement=use_crs_displacement,
        sub_indices=sub_indices,
    )
    uri = str(get_obj_uri(energyml_object))
    for m in result.flat_patches():
        m.identifier = uri
        m.energyml_object = energyml_object
        m.source_uuid = src_uuid
        m.source_type = src_type
    result.identifier = uri
    result.energyml_object = energyml_object
    result.source_uuid = src_uuid
    result.source_type = src_type
    return result


def read_numpy_seismic3d_post_stack_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``Seismic3dPostStackRepresentation`` — the 2-D lattice it is defined on.

    The object holds no geometry: it references the ``SeismicLatticeRepresentation``
    (a ``Grid2dRepresentation``) whose feature it shares, and adds the trace sampling. The
    lattice surface is returned; the trace samples themselves are properties, not geometry.
    """
    return _read_numpy_via_supporting_representation(
        energyml_object, "seismic_lattice_representation", workspace, use_crs_displacement, sub_indices
    )


def read_numpy_seismic2d_post_stack_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``Seismic2dPostStackRepresentation`` — the seismic line it is defined on.

    As for its 3-D counterpart the geometry is entirely in the referenced
    ``SeismicLineRepresentation`` (a ``PolylineRepresentation``).
    """
    return _read_numpy_via_supporting_representation(
        energyml_object, "seismic_line_representation", workspace, use_crs_displacement, sub_indices
    )


def read_numpy_redefined_geometry_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``RedefinedGeometryRepresentation`` — the supporting representation with the
    redefined points substituted in.

    "A representation derived from an existing representation by redefining its geometry.
    Example use cases include deformation of the geometry of an object, change of coordinate
    system, and change of time <=> depth." Topology comes from ``SupportingRepresentation``;
    each ``PatchOfGeometry`` overrides the points of one of its patches.

    A patch whose point count does not match the one it redefines is skipped with a warning
    rather than silently corrupting the connectivity.
    """
    ws = _view_workspace(workspace)
    src_uuid = get_obj_uuid(energyml_object)
    src_type = type(energyml_object).__name__

    result = _read_numpy_via_supporting_representation(
        energyml_object, "supporting_representation", workspace, use_crs_displacement, sub_indices
    )
    patches = result.flat_patches()
    if not patches:
        return result

    pog_list = getattr(energyml_object, "patch_of_geometry", None) or []
    for pog in pog_list:
        target_idx = getattr(pog, "representation_patch_index", None)
        target_idx = 0 if target_idx is None else int(target_idx)
        if target_idx >= len(patches):
            logger.warning(f"{src_type} {src_uuid}: PatchOfGeometry targets patch {target_idx}, which does not exist.")
            continue
        pts_list = [(p, o) for p, o in search_attribute_matching_name_with_path(pog, "Points") if o is not None]
        if not pts_list:
            continue
        pts_path, pts_obj = pts_list[0]
        try:
            new_pts = _ensure_float64_points(
                _read_array_np(pts_obj, energyml_object, f"patch_of_geometry.{pts_path}", ws)
            )
        except Exception as exc:
            logger.warning(f"{src_type} {src_uuid}: cannot read the redefined points: {type(exc).__name__}: {exc}")
            continue
        patch = patches[target_idx]
        if len(new_pts) != len(patch.points):
            logger.warning(
                f"{src_type} {src_uuid}: PatchOfGeometry {target_idx} holds {len(new_pts)} points but the "
                f"supporting patch has {len(patch.points)}; keeping the original geometry."
            )
            continue
        # The redefined points are expressed in this object's own CRS, i.e. back at the LOCAL
        # stage, so the frame has to be reset for read_numpy_mesh_object to transform them.
        patch.points = new_pts
        patch.frame = PointFrame.LOCAL
    return result


# ---------------------------------------------------------------------------
# Streamlines, graphs and deviation surveys
# ---------------------------------------------------------------------------


def _build_vtk_lines_from_counts(
    node_counts: Optional[np.ndarray],
    n_points: int,
    closed: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Build a VTK flat line array from per-polyline node counts."""
    if node_counts is None or len(node_counts) == 0:
        return _build_vtk_single_polyline(n_points)
    parts: List[np.ndarray] = []
    offset = 0
    for poly_idx, raw_n in enumerate(node_counts):
        n = int(raw_n)
        if n <= 0:
            continue
        indices = np.arange(offset, offset + n, dtype=np.int64)
        if closed is not None and poly_idx < len(closed) and closed[poly_idx]:
            indices = np.append(indices, offset)
        part = np.empty(len(indices) + 1, dtype=np.int64)
        part[0] = len(indices)
        part[1:] = indices
        parts.append(part)
        offset += n
    return np.concatenate(parts) if parts else np.empty(0, dtype=np.int64)


def read_numpy_streamlines_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``StreamlinesRepresentation`` as one polyline per streamline.

    ``geometry`` is a single ``PolylineSetPatch``: all the streamline nodes concatenated, split
    by ``NodeCountPerPolyline``. ``LineCount`` states how many streamlines to expect.
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

    geom = getattr(energyml_object, "geometry", None)
    if geom is None:
        logger.warning(f"StreamlinesRepresentation {src_uuid} has no geometry.")
        return multi

    pts_list = search_attribute_matching_name_with_path(geom, "Points")
    if not pts_list:
        logger.warning(f"StreamlinesRepresentation {src_uuid}: no points in geometry.")
        return multi
    pts_path, pts_obj = pts_list[0]
    points = _ensure_float64_points(_read_array_np(pts_obj, energyml_object, f"geometry.{pts_path}", ws))

    node_counts = None
    nc_list = [(p, o) for p, o in search_attribute_matching_name_with_path(geom, "NodeCountPerPolyline") if o]
    if nc_list:
        nc_path, nc_obj = nc_list[0]
        node_counts = _read_array_np(nc_obj, energyml_object, f"geometry.{nc_path}", ws).astype(np.int64).ravel()

    line_count = int(getattr(energyml_object, "line_count", 0) or 0)
    if node_counts is not None and line_count and len(node_counts) != line_count:
        logger.warning(
            f"StreamlinesRepresentation {src_uuid}: NodeCountPerPolyline holds "
            f"{len(node_counts)} entries for LineCount={line_count}."
        )

    lines = _build_vtk_lines_from_counts(node_counts, len(points))
    crs = None
    try:
        crs = get_crs_obj(context_obj=geom, path_in_root="geometry", root_obj=energyml_object, workspace=workspace)
    except Exception as exc:
        logger.debug(f"No CRS resolved: {type(exc).__name__}: {exc}")
    frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

    label = f"{src_type}_patch_0"
    multi.patches.append(
        NumpyPolylineMesh(
            identifier=label,
            energyml_object=energyml_object,
            crs_object=crs,
            points=points,
            lines=lines,
            frame=frame,
            patch_index=0,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
    )
    return multi


def read_numpy_graph2d_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``Graph2dRepresentation`` — its nodes joined by its edges.

    ``edges`` is a ``2 x #Edges`` array of node indices; each edge becomes a two-point VTK line.
    A graph with no edges comes back as a point set.
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

    geom = getattr(energyml_object, "geometry", None)
    pts_list = search_attribute_matching_name_with_path(geom, "Points") if geom is not None else []
    if not pts_list:
        logger.warning(f"Graph2dRepresentation {src_uuid} has no geometry.")
        return multi
    pts_path, pts_obj = pts_list[0]
    points = _ensure_float64_points(_read_array_np(pts_obj, energyml_object, f"geometry.{pts_path}", ws))

    edges_obj = getattr(energyml_object, "edges", None)
    edges: Optional[np.ndarray] = None
    if edges_obj is not None:
        try:
            raw = _read_array_np(edges_obj, energyml_object, "edges", ws).astype(np.int64).ravel()
            if raw.size % 2 == 0:
                edges = raw.reshape(-1, 2)
            else:
                logger.warning(f"Graph2dRepresentation {src_uuid}: Edges holds an odd number of values.")
        except Exception as exc:
            logger.warning(f"Graph2dRepresentation {src_uuid}: cannot read Edges: {type(exc).__name__}: {exc}")

    crs = None
    try:
        crs = get_crs_obj(context_obj=geom, path_in_root="geometry", root_obj=energyml_object, workspace=workspace)
    except Exception as exc:
        logger.debug(f"No CRS resolved: {type(exc).__name__}: {exc}")
    frame = _local_to_projected(points, crs, workspace, use_crs_displacement)

    label = f"{src_type}_patch_0"
    common = dict(
        identifier=label,
        energyml_object=energyml_object,
        crs_object=crs,
        points=points,
        frame=frame,
        patch_index=0,
        patch_label=label,
        source_uuid=src_uuid,
        source_type=src_type,
    )
    if edges is not None and len(edges) > 0:
        valid = (edges >= 0).all(axis=1) & (edges < len(points)).all(axis=1)
        if not valid.all():
            logger.warning(
                f"Graph2dRepresentation {src_uuid}: {int((~valid).sum())} edge(s) reference a "
                f"node outside [0, {len(points)}); dropped."
            )
        edges = edges[valid]
    if edges is not None and len(edges) > 0:
        lines = np.column_stack([np.full(len(edges), 2, dtype=np.int64), edges]).ravel()
        multi.patches.append(NumpyPolylineMesh(lines=lines, **common))
    else:
        multi.patches.append(NumpyPointSetMesh(**common))
    return multi


#: Conversion to radians of the ``PlaneAngleUom`` values a deviation survey realistically uses.
_ANGLE_TO_RAD: Dict[str, float] = {
    "dega": np.pi / 180.0,
    "rad": 1.0,
    "gon": np.pi / 200.0,
    "grad": np.pi / 200.0,
    "mrad": 1e-3,
    "urad": 1e-6,
    "krad": 1e3,
    "mila": np.pi / 3200.0,
    "mina": np.pi / (180.0 * 60.0),
    "seca": np.pi / (180.0 * 3600.0),
}


def read_numpy_deviation_survey_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``DeviationSurveyRepresentation`` as the polyline through its stations.

    The survey stores station ``Mds`` with an ``Inclinations`` / ``Azimuths`` pair rather than
    coordinates, so the positions have to be integrated. RESQML is explicit that this is not a
    lossless geometry: "The deviation survey does not provide a complete specification of the
    geometry of a wellbore trajectory. Although a minimum-curvature algorithm is used in most
    cases, the implementation varies sufficiently that no single algorithmic specification is
    available as a data transfer standard." The standard minimum-curvature integration is used
    here; where a matching ``WellboreTrajectoryRepresentation`` exists it is the authoritative
    geometry and should be preferred.

    Azimuths are measured clockwise from North, inclinations from vertical. The station chain
    starts at ``FirstStationLocation`` when present, otherwise at the ``MdDatum``.
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

    def _read(name: str) -> Optional[np.ndarray]:
        found = [(p, o) for p, o in search_attribute_matching_name_with_path(energyml_object, name) if o is not None]
        if not found:
            return None
        path, obj = found[0]
        try:
            return _read_array_np(obj, energyml_object, path, ws).astype(np.float64).ravel()
        except Exception as exc:
            logger.warning(f"DeviationSurveyRepresentation {src_uuid}: cannot read {name}: {exc}")
            return None

    mds = _read("Mds")
    incs = _read("Inclinations")
    azis = _read("Azimuths")
    if mds is None or incs is None or azis is None:
        logger.warning(f"DeviationSurveyRepresentation {src_uuid}: Mds/Inclinations/Azimuths missing.")
        return multi
    n = min(len(mds), len(incs), len(azis))
    if n < 1:
        return multi
    mds, incs, azis = mds[:n], incs[:n], azis[:n]

    angle_uom = getattr(energyml_object, "angle_uom", None)
    uom_name = str(getattr(angle_uom, "value", angle_uom) or "dega")
    if uom_name not in _ANGLE_TO_RAD:
        logger.warning(f"DeviationSurveyRepresentation {src_uuid}: unknown AngleUom '{uom_name}'; assuming degrees.")
    k = _ANGLE_TO_RAD.get(uom_name, _ANGLE_TO_RAD["dega"])
    inc = incs * k
    azi = azis * k

    # --- Origin ---
    origin = np.zeros(3, dtype=np.float64)
    z_increasing_downward = True
    crs = None
    first = getattr(energyml_object, "first_station_location", None)
    if first is not None:
        coords = getattr(first, "coordinate1", None), getattr(first, "coordinate2", None), getattr(
            first, "coordinate3", None
        )
        if all(c is not None for c in coords):
            origin = np.array([float(c) for c in coords], dtype=np.float64)
    md_datum_dor = getattr(energyml_object, "md_datum", None)
    if md_datum_dor is not None and workspace is not None:
        try:
            datum_obj = workspace.get_object(get_obj_uri(md_datum_dor))
            if datum_obj is not None:
                dx, dy, dz, z_increasing_downward, _, _, crs = get_datum_information(datum_obj, workspace)
                if first is None:
                    origin = np.array([dx, dy, dz], dtype=np.float64)
        except Exception as exc:
            logger.debug(f"Cannot resolve MdDatum of {src_uuid}: {type(exc).__name__}: {exc}")

    # --- Minimum-curvature integration ---
    points = np.empty((n, 3), dtype=np.float64)
    points[0] = origin
    for i in range(1, n):
        d_md = float(mds[i] - mds[i - 1])
        i1, i2, a1, a2 = float(inc[i - 1]), float(inc[i]), float(azi[i - 1]), float(azi[i])
        cos_dl = np.cos(i2 - i1) - np.sin(i1) * np.sin(i2) * (1.0 - np.cos(a2 - a1))
        dl = float(np.arccos(np.clip(cos_dl, -1.0, 1.0)))
        rf = (2.0 / dl) * np.tan(dl / 2.0) if dl > 1e-9 else 1.0
        half = d_md / 2.0 * rf
        d_north = half * (np.sin(i1) * np.cos(a1) + np.sin(i2) * np.cos(a2))
        d_east = half * (np.sin(i1) * np.sin(a1) + np.sin(i2) * np.sin(a2))
        d_tvd = half * (np.cos(i1) + np.cos(i2))
        points[i, 0] = points[i - 1, 0] + d_east
        points[i, 1] = points[i - 1, 1] + d_north
        points[i, 2] = points[i - 1, 2] + (d_tvd if z_increasing_downward else -d_tvd)

    # get_datum_information reports coordinates already in the projected CRS, like the
    # wellbore-trajectory reader's datum path.
    frame = PointFrame.PROJECTED if crs is not None else PointFrame.LOCAL
    label = f"{src_type}_patch_0"
    multi.patches.append(
        NumpyPolylineMesh(
            identifier=label,
            energyml_object=energyml_object,
            crs_object=crs,
            points=points,
            lines=_build_vtk_single_polyline(n),
            frame=frame,
            patch_index=0,
            patch_label=label,
            source_uuid=src_uuid,
            source_type=src_type,
        )
    )
    multi.patches[0].extra_arrays["node_md"] = mds
    return multi


# ---------------------------------------------------------------------------
# Grid connection sets
# ---------------------------------------------------------------------------

# Local face-per-cell index of an IJK cell, expressed as the pair of column corners the face
# spans. Corner names follow `_build_split_pillar_map`: TL=(j,i) TR=(j,i+1) BL=(j+1,i) BR=(j+1,i+1),
# so "L"/"R" is the I direction and "T"/"B" the J direction.
#
# The RESQML documentation states the ordering rule — "the top and bottom faces always come
# first, followed by the side faces" (11.5.3, Local Faces per Cell indexing for an IJK Grid
# Cell) — but publishes the index-to-direction assignment only as a figure. Faces 3 and 5 are
# pinned by the fixtures: in rc/epc/80wells_surf_modified_val_color.epc every connection of the
# fault sets uses the pair (3, 5) between a cell at I and its neighbour at I+1, and the nodes
# those two faces resolve to are the two walls of the fault plane at X=375 (a 50 m throw apart).
# The four side faces therefore cycle J-, I+, J+, I- around the column, which fixes 2 and 4.
_IJK_LOCAL_FACE_CORNERS: Dict[int, Tuple[str, ...]] = {
    0: ("TL", "TR", "BR", "BL"),  # K- : the whole bottom quad
    1: ("TL", "TR", "BR", "BL"),  # K+ : the whole top quad
    2: ("TL", "TR"),  # J-
    3: ("TR", "BR"),  # I+
    4: ("BL", "BR"),  # J+
    5: ("TL", "BL"),  # I-
}
_IJK_K_FACES = (0, 1)


def _ijk_corner_slots(grid_obj: Any) -> Dict[str, int]:
    """Map a column corner name to its slot in the 8-node VTK hexahedron of that grid.

    :func:`read_numpy_ijk_grid_representation` reverses the base-quad winding on a left-handed
    grid so the emitted cell has a positive Jacobian, so the slot of a given corner depends on
    ``GridIsRighthanded``.
    """
    geom = getattr(grid_obj, "geometry", None)
    righthanded = getattr(geom, "grid_is_righthanded", None) if geom is not None else None
    if righthanded is None:
        righthanded = True
    order = ("TL", "TR", "BR", "BL") if righthanded else ("TL", "BL", "BR", "TR")
    return {name: slot for slot, name in enumerate(order)}


def _split_vtk_cells(cells: np.ndarray, cell_types: np.ndarray) -> List[np.ndarray]:
    """Split a VTK flat cell array into one node array per cell."""
    out: List[np.ndarray] = []
    off = 0
    for _ in range(len(cell_types)):
        if off >= len(cells):
            break
        n = int(cells[off])
        out.append(np.asarray(cells[off + 1 : off + 1 + n], dtype=np.int64))
        off += 1 + n
    return out


def _polyhedron_faces(cell_entry: np.ndarray) -> List[np.ndarray]:
    """Decode a VTK_POLYHEDRON cell body ``[n_faces, npts, p…, npts, p…]`` into face node lists.

    The faces come back in the order :func:`read_numpy_unstructured_grid_representation` wrote
    them, which is the order of ``FacesPerCell`` — i.e. the local face index of the grid.
    """
    faces: List[np.ndarray] = []
    if len(cell_entry) == 0:
        return faces
    n_faces = int(cell_entry[0])
    off = 1
    for _ in range(n_faces):
        if off >= len(cell_entry):
            break
        npts = int(cell_entry[off])
        faces.append(np.asarray(cell_entry[off + 1 : off + 1 + npts], dtype=np.int64))
        off += 1 + npts
    return faces


def _connection_face_nodes(
    grid_obj: Any,
    cell_nodes: List[np.ndarray],
    cell_types: np.ndarray,
    corner_slots: Dict[str, int],
    cell_index: int,
    local_face: int,
) -> Optional[np.ndarray]:
    """Return the node indices of *local_face* of *cell_index*, or ``None``.

    Handles the two cell shapes a grid reader emits: the hexahedron of a column-layer grid,
    whose local faces follow :data:`_IJK_LOCAL_FACE_CORNERS`, and the polyhedron of an
    unstructured grid, whose local face index is a position in its own face list.
    """
    if cell_index < 0 or cell_index >= len(cell_nodes):
        return None
    nodes = cell_nodes[cell_index]
    ctype = int(cell_types[cell_index]) if cell_index < len(cell_types) else _VTK_EMPTY_CELL

    if ctype == _VTK_POLYHEDRON:
        faces = _polyhedron_faces(nodes)
        return faces[local_face] if 0 <= local_face < len(faces) else None

    if ctype != _VTK_HEXAHEDRON or len(nodes) != 8:
        return None  # empty cell (CellGeometryIsDefined=false) or an unexpected shape

    corners = _IJK_LOCAL_FACE_CORNERS.get(local_face)
    if corners is None:
        return None
    if local_face in _IJK_K_FACES:
        base = 0 if local_face == 0 else 4
        return np.array([nodes[corner_slots[c] + base] for c in corners], dtype=np.int64)

    # A side face is the quad swept by two column corners between the bottom and top layers.
    c0, c1 = corners
    s0, s1 = corner_slots[c0], corner_slots[c1]
    return np.array([nodes[s0], nodes[s1], nodes[s1 + 4], nodes[s0 + 4]], dtype=np.int64)


def read_numpy_grid_connection_set_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> "NumpyMultiMesh":
    """Read a ``GridConnectionSetRepresentation`` as the surface of its cell faces.

    A grid connection set is "a list of connections between grid cells [...] in the form of
    (Grid,Cell,Face)1<=>(Grid,Cell,Face)2" and is "the preferred means of representing faults on
    a grid". It carries no geometry of its own: every face is looked up on the grid(s) it
    references, which are read through :func:`read_numpy_mesh_object`.

    Output
    ------
    * With ``LocalFacePerCellIndexPairs`` — a :class:`NumpySurfaceMesh` of quads. **Both** sides
      of a connection are emitted when both are defined: across a fault the two faces are the
      two walls and do not coincide, so drawing only one hides the throw. A side whose cell or
      face index is null (the array's ``NullValue``) is skipped, which is how the boundary
      connections of a fault are stored.
    * Without it — the array is optional, "e.g., for a block-centered grid" — a
      :class:`NumpyPolylineMesh` of one segment per connection, joining the two cell centroids.

    ``extra_arrays`` carries ``connection_index`` (the connection each face/segment came from)
    and, when ``ConnectionInterpretations`` is present, ``interpretation_index`` — the first
    interpretation of that connection, which is what lets a viewer colour the set by fault.

    Grids that are missing from the workspace, or that yield no cells, are skipped with a
    warning rather than failing the whole set.
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

    count = int(getattr(energyml_object, "count", 0) or 0)
    if count <= 0:
        logger.warning(f"GridConnectionSetRepresentation {src_uuid} declares no connection.")
        return multi

    cell_pairs, cip_obj = _read_index_pairs(energyml_object, "CellIndexPairs", ws)
    if cell_pairs is None:
        logger.warning(f"GridConnectionSetRepresentation {src_uuid} has no CellIndexPairs.")
        return multi
    cell_null = _array_null_value(cip_obj)

    face_pairs, lfp_obj = _read_index_pairs(energyml_object, "LocalFacePerCellIndexPairs", ws)
    face_null = _array_null_value(lfp_obj) if face_pairs is not None else None

    grid_pairs, _ = _read_index_pairs(energyml_object, "GridIndexPairs", ws)

    # --- Resolve and read the referenced grids ---
    grid_dors = get_object_attribute(energyml_object, "grid")
    if grid_dors is None:
        grid_dors = []
    elif not isinstance(grid_dors, list):
        grid_dors = [grid_dors]
    if not grid_dors:
        logger.warning(f"GridConnectionSetRepresentation {src_uuid} references no grid.")
        return multi

    grid_objs: List[Any] = []
    grid_points: List[np.ndarray] = []
    grid_cells: List[List[np.ndarray]] = []
    grid_cell_types: List[np.ndarray] = []
    grid_slots: List[Dict[str, int]] = []
    point_offsets: List[int] = []
    all_points: List[np.ndarray] = []
    grid_frame: Optional[PointFrame] = None
    grid_crs: Any = None
    n_points = 0

    for dor in grid_dors:
        grid_obj = workspace.get_object(get_obj_uri(dor)) if workspace is not None else None
        if grid_obj is None:
            logger.warning(f"GridConnectionSetRepresentation {src_uuid}: grid {get_obj_uri(dor)} not found.")
            grid_objs.append(None)
            grid_points.append(np.empty((0, 3), dtype=np.float64))
            grid_cells.append([])
            grid_cell_types.append(np.empty(0, dtype=np.uint8))
            grid_slots.append({})
            point_offsets.append(n_points)
            continue
        # Read the grid through the public dispatcher so its points come back already in the
        # frame this call targets; the patches we build below then report that same frame and
        # read_numpy_mesh_object leaves them alone instead of transforming them a second time.
        grid_mesh = read_numpy_mesh_object(
            energyml_object=grid_obj,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
        )
        patches = [p for p in grid_mesh.flat_patches() if isinstance(p, NumpyVolumeMesh)]
        if not patches:
            logger.warning(
                f"GridConnectionSetRepresentation {src_uuid}: grid {get_obj_uuid(grid_obj)} "
                f"({type(grid_obj).__name__}) produced no volume cells."
            )
        patch = patches[0] if patches else None
        pts = patch.points if patch is not None else np.empty((0, 3), dtype=np.float64)
        grid_objs.append(grid_obj)
        grid_points.append(pts)
        grid_cells.append(_split_vtk_cells(patch.cells, patch.cell_types) if patch is not None else [])
        grid_cell_types.append(patch.cell_types if patch is not None else np.empty(0, dtype=np.uint8))
        grid_slots.append(_ijk_corner_slots(grid_obj))
        point_offsets.append(n_points)
        all_points.append(pts)
        n_points += len(pts)
        if patch is not None and grid_frame is None:
            grid_frame = patch.frame
            grid_crs = patch.crs_object

    if n_points == 0:
        logger.warning(f"GridConnectionSetRepresentation {src_uuid}: no grid geometry available.")
        return multi
    points = np.concatenate(all_points, axis=0) if len(all_points) > 1 else all_points[0]

    interp_of_connection = _first_interpretation_per_connection(energyml_object, ws, count)

    def _grid_of(conn: int, side: int) -> int:
        if grid_pairs is None or conn >= len(grid_pairs):
            return 0
        g = int(grid_pairs[conn, side])
        return g if 0 <= g < len(grid_objs) else 0

    n_conn = min(count, len(cell_pairs))
    if sub_indices is not None:
        wanted = {int(i) for i in sub_indices}
    else:
        wanted = None

    faces_flat: List[int] = []
    face_conn: List[int] = []
    lines_flat: List[int] = []
    line_conn: List[int] = []
    extra_pts: List[np.ndarray] = []  # centroids, appended after the grid points

    for conn in range(n_conn):
        if wanted is not None and conn not in wanted:
            continue
        sides = []
        for side in (0, 1):
            cell = int(cell_pairs[conn, side])
            if cell_null is not None and cell == cell_null:
                continue
            g = _grid_of(conn, side)
            if not grid_cells[g]:
                continue
            sides.append((g, cell, side))

        if face_pairs is not None:
            for g, cell, side in sides:
                lf = int(face_pairs[conn, side]) if conn < len(face_pairs) else -1
                if lf < 0 or (face_null is not None and lf == face_null):
                    continue
                nodes = _connection_face_nodes(
                    grid_objs[g], grid_cells[g], grid_cell_types[g], grid_slots[g], cell, lf
                )
                if nodes is None or len(nodes) < 3:
                    continue
                faces_flat.append(len(nodes))
                faces_flat.extend(int(x) + point_offsets[g] for x in nodes)
                face_conn.append(conn)
        else:
            # No face information: join the cell centroids, which is the only geometry the
            # connection still defines.
            centroids = []
            for g, cell, _side in sides:
                nodes = grid_cells[g][cell]
                if len(nodes) == 0:
                    continue
                centroids.append(grid_points[g][nodes].mean(axis=0))
            if len(centroids) == 2:
                base = n_points + len(extra_pts)
                extra_pts.extend(centroids)
                lines_flat.extend([2, base, base + 1])
                line_conn.append(conn)

    if faces_flat:
        mesh: NumpyMesh = NumpySurfaceMesh(
            identifier=f"{src_type}_patch_0",
            energyml_object=energyml_object,
            crs_object=grid_crs,
            points=points,
            faces=np.array(faces_flat, dtype=np.int64),
            frame=grid_frame if grid_frame is not None else PointFrame.LOCAL,
            patch_index=0,
            patch_label=f"{src_type}_patch_0",
            source_uuid=src_uuid,
            source_type=src_type,
        )
        conn_idx = np.array(face_conn, dtype=np.int64)
    elif lines_flat:
        mesh = NumpyPolylineMesh(
            identifier=f"{src_type}_patch_0",
            energyml_object=energyml_object,
            crs_object=grid_crs,
            points=np.concatenate([points, np.asarray(extra_pts, dtype=np.float64)], axis=0),
            lines=np.array(lines_flat, dtype=np.int64),
            frame=grid_frame if grid_frame is not None else PointFrame.LOCAL,
            patch_index=0,
            patch_label=f"{src_type}_patch_0",
            source_uuid=src_uuid,
            source_type=src_type,
        )
        conn_idx = np.array(line_conn, dtype=np.int64)
    else:
        logger.warning(
            f"GridConnectionSetRepresentation {src_uuid}: none of the {n_conn} connections "
            "resolved to a face or a cell pair."
        )
        return multi

    mesh.extra_arrays["connection_index"] = conn_idx
    if interp_of_connection is not None:
        mesh.extra_arrays["interpretation_index"] = interp_of_connection[conn_idx]
    multi.patches.append(mesh)
    return multi


def _read_index_pairs(
    energyml_object: Any,
    name: str,
    ws: Any,
) -> Tuple[Optional[np.ndarray], Any]:
    """Read a ``2 x #Connections`` integer array as ``(N, 2)``, or ``(None, None)``.

    ``search_attribute_matching_name_with_path`` reports an attribute that exists on the class
    even when the document left it empty, so the ``None`` has to be filtered here — the three
    index-pair arrays of a connection set are all optional but one.
    """
    results = [(p, o) for p, o in search_attribute_matching_name_with_path(energyml_object, name) if o is not None]
    if not results:
        return None, None
    path, obj = results[0]
    try:
        arr = _read_array_np(obj, energyml_object, path, ws)
    except Exception as exc:
        logger.warning(f"Cannot read {name}: {type(exc).__name__}: {exc}")
        return None, None
    arr = np.asarray(arr).astype(np.int64).ravel()
    if arr.size % 2 != 0:
        logger.warning(f"{name} holds an odd number of values ({arr.size}); ignoring it.")
        return None, None
    return arr.reshape(-1, 2), obj


def _array_null_value(array_obj: Any) -> Optional[int]:
    """Return the ``NullValue`` declared on an integer array, or ``None``."""
    null = getattr(array_obj, "null_value", None)
    try:
        return int(null) if null is not None else None
    except (TypeError, ValueError):
        return None


def _first_interpretation_per_connection(
    energyml_object: Any,
    ws: Any,
    count: int,
) -> Optional[np.ndarray]:
    """Return ``(count,)`` of the first interpretation index of each connection, or ``None``.

    ``ConnectionInterpretations.InterpretationIndices`` is a list-of-lists — a connection may
    belong to several interpretations — so only the first is kept, which is enough to colour a
    fault set by fault. ``-1`` marks a connection with no interpretation.
    """
    ci = getattr(energyml_object, "connection_interpretations", None)
    if ci is None:
        return None
    idx_obj = getattr(ci, "interpretation_indices", None)
    if idx_obj is None:
        return None
    try:
        per_conn = _decode_jagged_array(
            idx_obj, energyml_object, "connection_interpretations.interpretation_indices", ws
        )
    except Exception as exc:
        logger.debug(f"Cannot read ConnectionInterpretations.InterpretationIndices: {type(exc).__name__}: {exc}")
        return None
    out = np.full(count, -1, dtype=np.int64)
    for i, entry in enumerate(per_conn[:count]):
        if len(entry) > 0:
            out[i] = int(entry[0])
    return out


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------


def read_numpy_mesh_object(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    frame: Optional[PointFrame] = None,
    use_network: bool = False,
) -> "NumpyMultiMesh":
    """Dispatcher — equivalent to :func:`mesh.read_mesh_object` but returns
    a :class:`NumpyMultiMesh` container.

    Every returned patch carries the :class:`~energyml.utils.data.crs.PointFrame` its points are
    expressed in, and this function only applies the pipeline stages a reader has not already
    applied. That replaces the previous list of type names — one substring per reader — where a
    missing entry silently transformed the same points twice, and an extra one left them
    untransformed.

    Args:
        energyml_object: Any supported RESQML/EnergyML geometry/representation object.
        workspace:        Storage interface (``Epc``, ``EpcStreamReader`` or ``EpcFile``).
        use_crs_displacement: Legacy switch kept for compatibility. It selects the default
                          target frame: ``PointFrame.PROJECTED`` when ``True`` (default),
                          ``PointFrame.LOCAL`` when ``False``. Ignored when *frame* is given.
        sub_indices:      Optional list of face/line/point indices to include.
        frame:            Explicit target frame. ``PointFrame.WGS84`` reads the geometry directly
                          in longitude / latitude / ellipsoidal height — convenient for mapping
                          output, but note that X/Y are then degrees while Z stays metres, a ratio
                          no 3-D viewer handles sensibly.
        use_network:      Allow PROJ to download the geoid grids used by the vertical datum
                          transformation. Only relevant for ``PointFrame.WGS84``.

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
                    frame=frame,
                    use_network=use_network,
                )
            )
        return synthetic

    type_name = _numpy_mesh_name_mapping(type(energyml_object).__name__)
    reader_func = get_numpy_reader_function(type_name)

    if reader_func is None:
        raise NotSupportedError(
            f"No numpy mesh reader found for type '{type_name}'. "
            f"Expected function 'read_numpy_{snake_case(type_name)}' in {__name__}."
        )

    result: NumpyMultiMesh = reader_func(
        energyml_object=energyml_object,
        workspace=workspace,
        sub_indices=sub_indices,
        use_crs_displacement=use_crs_displacement,
    )

    target = frame if frame is not None else (PointFrame.PROJECTED if use_crs_displacement else PointFrame.LOCAL)

    for m in result.flat_patches():
        if m.frame is target or len(m.points) == 0:
            continue
        crs = m.crs_object[0] if isinstance(m.crs_object, list) and m.crs_object else m.crs_object
        framed = to_frame(
            m.points,
            extract_crs_info(crs, workspace) if crs is not None else None,
            target,
            m.frame,
            use_network=use_network,
            inplace=True,
        )
        m.points = framed.points
        m.frame = framed.frame

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
    logger.warning(f"numpy_mesh_to_pyvista: unknown mesh type {type(mesh).__name__}, exporting points only.")
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
    # Coordinate frames (re-exported from crs.py for convenience)
    "PointFrame",
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
