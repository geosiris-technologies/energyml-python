# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""OFF (Object File Format) export.

Moved here from :mod:`energyml.utils.data.mesh`, which re-exports both functions so existing
imports keep working. The writer now accepts the numpy mesh hierarchy as well as the legacy one,
like every other format of this package.
"""

from __future__ import annotations

import logging
from io import BytesIO
from typing import TYPE_CHECKING, Any, BinaryIO, Dict, List, Optional

import numpy as np

from energyml.utils.data.export._base import (
    _FILE_HEADER,
    ExportFormat,
    _get_export_points,
    _get_faces_or_cells,
    _normalize_to_patches,
    _parse_vtk_flat_faces,
    _workspace_from_contexts,
    resolve_origin_shift,
)
from energyml.utils.data.export._registry import FormatSpec, register_format

if TYPE_CHECKING:
    from energyml.utils.data.crs import PointFrame
    from energyml.utils.data.representation_context import RepresentationContext

log = logging.getLogger(__name__)


def _face_list(mesh: Any) -> List[np.ndarray]:
    """Return the faces of *mesh* as a list of index arrays, for either hierarchy."""
    from energyml.utils.data.mesh_numpy import NumpyMesh

    if isinstance(mesh, NumpyMesh):
        return _parse_vtk_flat_faces(_get_faces_or_cells(mesh))
    return [np.asarray(face, dtype=np.int64) for face in (mesh.get_indices() or [])]


def _edge_count(mesh: Any, faces: List[np.ndarray]) -> int:
    """Number written in the third field of the OFF header.

    ``AbstractMesh.get_nb_edges`` is used when present so the legacy output stays byte-identical
    (it counts ``len(face) - 1`` per face, which undercounts a closed polygon by one — OFF readers
    ignore this field, so the historical value is preserved rather than corrected).
    """
    if hasattr(mesh, "get_nb_edges"):
        return mesh.get_nb_edges()
    return sum(max(len(f) - 1, 0) for f in faces)


def export_off(
    mesh_list: Any,
    out: BinaryIO,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    use_network: bool = False,
) -> None:
    """Export mesh data to OFF format.

    :param mesh_list: One or more meshes (``AbstractMesh``, ``NumpyMesh``, ``NumpyMultiMesh``,
        or a list thereof).
    :param out: Binary output stream.
    :param contexts: Color / metadata context dict (only used to reach a workspace here).
    :param use_crs_displacement: Legacy switch selecting the default target frame.
    :param frame: Explicit target :class:`~energyml.utils.data.crs.PointFrame`.
    :param origin_shift: ``None``, ``"auto"``, or an explicit ``(dx, dy, dz)`` vector.
    :param use_network: Allow PROJ to download the geoid grids (``PointFrame.WGS84`` only).
    """
    patches = _normalize_to_patches(mesh_list)
    workspace = _workspace_from_contexts(contexts)
    _origin_shift = resolve_origin_shift(patches, use_crs_displacement, workspace, frame, origin_shift, use_network)

    points_io = BytesIO()
    faces_io = BytesIO()

    nb_points = 0
    nb_faces = 0
    nb_edges = 0
    point_offset = 0

    for mesh in patches:
        pts, _pts_frame, _ = _get_export_points(
            mesh, use_crs_displacement, workspace, frame, _origin_shift, use_network
        )
        pts = np.asarray(pts, dtype=np.float64).reshape(-1, 3)
        faces = _face_list(mesh)

        nb_points += len(pts)
        nb_faces += len(faces)
        nb_edges += _edge_count(mesh, faces)

        export_off_part(
            off_point_part=points_io,
            off_face_part=faces_io,
            points=pts,
            indices=faces,
            point_offset=point_offset,
            colors=[],
        )
        point_offset += len(pts)

    out.write(b"OFF\n")
    out.write(_FILE_HEADER)
    out.write(f"{nb_points} {nb_faces} {nb_edges}\n".encode("utf-8"))
    out.write(points_io.getbuffer())
    out.write(faces_io.getbuffer())


def export_off_part(
    off_point_part: BinaryIO,
    off_face_part: BinaryIO,
    points: Any,
    indices: Any,
    point_offset: Optional[int] = 0,
    colors: Optional[List[List[int]]] = None,
) -> None:
    """Append one mesh to the point and face sections of an OFF document.

    The two sections are written to separate streams because OFF wants all the vertices before
    any face, while the meshes are walked one at a time.
    """
    for p in points:
        for pi in p:
            off_point_part.write(f"{pi} ".encode("utf-8"))
        off_point_part.write(b"\n")

    for cpt, face in enumerate(indices):
        if len(face) > 1:
            off_face_part.write(f"{len(face)} ".encode("utf-8"))
            for pi in face:
                off_face_part.write(f"{pi + point_offset} ".encode("utf-8"))

            if colors is not None and len(colors) > cpt and colors[cpt] is not None and len(colors[cpt]) > 0:
                for col in colors[cpt]:
                    off_face_part.write(f"{col} ".encode("utf-8"))

            off_face_part.write(b"\n")


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
    """Uniform adapter used by the registry; OFF takes no options."""
    export_off(
        mesh_list,
        out,
        contexts,
        use_crs_displacement,
        frame=frame,
        origin_shift=origin_shift,
    )


register_format(
    FormatSpec(
        format=ExportFormat.OFF,
        description="OFF — Object File Format (vertices + faces, plain text)",
        filter_label="OFF Files (*.off)",
        writer=_write,
        binary=True,
        options_class=None,
    )
)
