# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""Shared building blocks of the export package: formats, options and geometry helpers."""

from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import numpy as np

if TYPE_CHECKING:
    from energyml.utils.data.crs import PointFrame

logger = logging.getLogger(__name__)

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


#: Header line stamped at the top of the text-based mesh formats.
_FILE_HEADER: bytes = b"# file exported by energyml-utils python module (Geosiris)\n"


class ExportFormat(Enum):
    """Supported mesh export formats."""

    OBJ = "obj"
    OFF = "off"
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

    def __init__(
        self,
        indent: Optional[int] = 2,
        properties: Optional[dict] = None,
        to_wgs84: bool = True,
        include_metadata: bool = True,
        use_network: bool = False,
        projected_epsg_code: Optional[int] = None,
        vertical_epsg_code: Optional[int] = None,
        explode_elements: bool = False,
    ):
        """
        :param indent: JSON indentation level (None for compact output).
        :param properties: Extra properties merged into every feature.
        :param to_wgs84: When True (default), coordinates are reprojected to WGS84
                         (longitude, latitude, ellipsoidal height) as required by RFC 7946.
                         Silently disabled when no EPSG code can be found or when ``pyproj``
                         (extra ``crs``) is not installed — the source CRS is then advertised
                         in the output instead.
        :param include_metadata: When True (default), the ``uuid``, ``qualified_type`` and
                                 ``Citation`` fields of the source object are written in the
                                 properties of every feature.
        :param use_network: Allow PROJ to download the geoid grids needed by vertical datum
                            transformations.  Without them the height conversion is skipped.
        :param projected_epsg_code: Force the horizontal EPSG code instead of reading it from the CRS.
        :param vertical_epsg_code: Force the vertical EPSG code instead of reading it from the CRS.
        :param explode_elements: Emit one feature per triangle / per line segment instead of one
                            feature per patch. Off by default: a patch is the unit a RESQML
                            representation is made of, and exploding it repeats the whole
                            metadata block — uuid, citation, EPSG codes — on every element,
                            which on a triangulated surface means one copy per triangle.
        """
        self.indent = indent
        self.properties = properties or {}
        self.to_wgs84 = to_wgs84
        self.include_metadata = include_metadata
        self.use_network = use_network
        self.projected_epsg_code = projected_epsg_code
        self.vertical_epsg_code = vertical_epsg_code
        self.explode_elements = explode_elements


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


class EmptyMeshError(ValueError):
    """Raised when an export would produce a file with no geometry in it."""


def drop_empty_patches(meshes: Any, raise_when_empty: bool = False) -> List[Any]:
    """Return the patches of *meshes* that actually carry points.

    A representation whose external arrays could not be read still yields patches — with zero
    points. Writing them produced a valid but useless file: ``{"type": "FeatureCollection",
    "features": []}``, 54 bytes, with nothing to say that the data was missing rather than
    absent. Worse, a partially readable object exported its readable patches next to empty ones.

    :param raise_when_empty: raise :class:`EmptyMeshError` when *nothing* survives, so the caller
        fails loudly instead of writing an empty file.
    """
    patches = _normalize_to_patches(meshes)
    kept, dropped = [], 0
    for patch in patches:
        points = getattr(patch, "point_list", None)
        if points is None:
            points = getattr(patch, "points", None)
        if points is None or len(points) == 0:
            dropped += 1
            continue
        kept.append(patch)

    if dropped:
        logger.warning(
            f"{dropped} of {len(patches)} patch(es) hold no point and were dropped from the export "
            "— their external arrays were most likely unreadable."
        )
    if not kept and raise_when_empty:
        raise EmptyMeshError(
            f"Nothing to export: all {len(patches)} patch(es) are empty. The geometry could not be "
            "read — check that the external (HDF5) arrays are reachable from the workspace."
        )
    return kept


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
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    use_network: bool = False,
) -> Tuple[np.ndarray, "PointFrame", Optional[tuple]]:
    """Return ``(points, frame, applied_origin_shift)`` for *mesh* in the requested frame.

    The mesh carries the :class:`~energyml.utils.data.crs.PointFrame` its points are already in,
    so only the missing pipeline stages are applied. That is what stops the double transform this
    function used to cause: the readers apply the local → projected stage, and re-applying it here
    whenever a workspace happened to be available shifted the geometry by the CRS origin twice.

    *mesh.points* is never mutated — the transform runs on a copy.
    """
    from energyml.utils.data.crs import PointFrame, to_frame
    from energyml.utils.data.mesh_numpy import NumpyMesh

    if isinstance(mesh, NumpyMesh):
        points = mesh.points
        current = mesh.frame
    else:
        # AbstractMesh — point_list is a list-of-lists; convert to ndarray for uniform handling
        points = np.array(getattr(mesh, "point_list", []), dtype=np.float64)
        current = getattr(mesh, "frame", PointFrame.LOCAL)

    target = frame if frame is not None else (PointFrame.PROJECTED if use_crs_displacement else PointFrame.LOCAL)

    if len(points) == 0 or (current is target and origin_shift is None):
        return points, current, None

    crs_object = getattr(mesh, "crs_object", None)
    crs = crs_object[0] if isinstance(crs_object, list) and crs_object else crs_object
    crs_info = None
    if crs is not None:
        from energyml.utils.data.crs import extract_crs_info

        crs_info = extract_crs_info(crs, workspace)

    try:
        framed = to_frame(
            points,
            crs_info,
            target,
            current,
            origin_shift=origin_shift,
            use_network=use_network,
            inplace=False,  # never mutate the mesh's own array
        )
        return framed.points, framed.frame, framed.origin_shift
    except Exception as exc:  # pragma: no cover
        logger.warning("Frame conversion to %s failed for %s: %s", target.value, getattr(mesh, "source_uuid", None), exc)
        return points, current, None


def resolve_origin_shift(
    patches: List[Any],
    use_crs_displacement: bool,
    workspace: Any,
    frame: Optional["PointFrame"],
    origin_shift: Optional[Any],
    use_network: bool = False,
) -> Optional[tuple]:
    """Turn an ``origin_shift`` option into an explicit ``(dx, dy, dz)`` vector.

    ``"auto"`` recentres the export on the bounding-box centre of **all** the patches together.
    It has to be resolved once for the whole export: a per-patch centre would translate each
    patch by a different vector and pull the model apart.

    Resolving ``"auto"`` costs one extra pass, since the bounding box has to be measured in the
    target frame — that is the price of the option, and it is only paid when it is asked for.
    ``None`` and an explicit vector are returned as-is, with no pass at all.
    """
    if origin_shift is None:
        return None
    if not isinstance(origin_shift, str):
        return tuple(float(v) for v in origin_shift)
    if origin_shift != "auto":
        raise ValueError(f"origin_shift must be None, 'auto', or a (dx, dy, dz) vector — got {origin_shift!r}")

    from energyml.utils.data.crs import compute_origin_shift

    framed = [
        _get_export_points(mesh, use_crs_displacement, workspace, frame, None, use_network)[0] for mesh in patches
    ]
    return compute_origin_shift(framed)


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
        return ctx.primary_color.to_uint8()
    except Exception as exc:  # pragma: no cover
        logger.debug("Failed to read color for %s: %s", source_uuid, exc)
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


#: Public API of this module. Declared explicitly so that renaming or removing anything
#: else is not a breaking change, and so `from ... import *` does not leak the imports.
__all__ = [
    "ExportFormat",
    "ExportOptions",
    "STLExportOptions",
    "VTKFormat",
    "VTKExportOptions",
    "GeoJSONExportOptions",
    "EmptyMeshError",
    "drop_empty_patches",
    "resolve_origin_shift",
]
