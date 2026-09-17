# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""Wavefront OBJ export (geometry + optional .mtl colour)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional, BinaryIO

from energyml.utils.data.export._base import (
    ExportFormat,
    MeshGroupKey,
    MeshNamer,
    resolve_origin_shift,
    _get_context_color,
    _get_export_points,
    _get_faces_or_cells,
    _normalize_to_patches,
    _parse_vtk_flat_faces,
    _parse_vtk_flat_lines,
    _patch_identifier,
    _workspace_from_contexts,
)

from energyml.utils.data.export._registry import FormatSpec, register_format

if TYPE_CHECKING:
    from energyml.utils.data.crs import PointFrame
    from energyml.utils.data.representation_context import RepresentationContext

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OBJ export
# ---------------------------------------------------------------------------


def default_object_name(mesh: Any) -> str:
    """Default ``o`` namer: the URI of the patch's source object.

    Reads it fresh off ``patch.energyml_object`` rather than ``patch.identifier`` — the legacy
    ``AbstractMesh`` suffixes that identifier with ``_patch{n}``, which is the right label for a
    single patch's ``g`` line but not for the ``o`` line naming the whole (possibly multi-patch)
    object. Falls back to the patch's own identifier when no source object is attached.
    """
    energyml_object = getattr(mesh, "energyml_object", None)
    if energyml_object is not None:
        try:
            from energyml.utils.introspection import get_obj_uri

            uri = get_obj_uri(energyml_object)
            if uri.uuid:  # a foreign/malformed object resolves to an empty "eml:///" otherwise
                return str(uri)
        except Exception:
            pass
    return _patch_identifier(mesh) or "mesh"


def default_group_name(mesh: Any) -> str:
    """Default ``g`` namer: ``{source_uuid}_{patch_index}``, falling back to the patch label.

    This is the mapping OBJ export always used, kept as the default so existing callers see no
    change; pass *group_namer* to :func:`export_obj` to use another one.
    """
    source_uuid = getattr(mesh, "source_uuid", None) or getattr(mesh, "uuid", None)
    patch_idx = getattr(mesh, "patch_index", None)
    patch_label = getattr(mesh, "patch_label", None) or getattr(mesh, "identifier", None) or "mesh"
    return f"{source_uuid}_{patch_idx}" if source_uuid and patch_idx is not None else patch_label


def export_obj(
    mesh_list: Any,
    out: BinaryIO,
    obj_name: Optional[str] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    mtl_out: Optional[BinaryIO] = None,
    use_crs_displacement: bool = True,
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
    use_network: bool = False,
    object_namer: Optional[MeshNamer] = None,
    group_namer: Optional[MeshNamer] = None,
    group_by: Optional[MeshGroupKey] = None,
) -> None:
    """Export mesh data to Wavefront OBJ format.

    :param mesh_list: One or more meshes (``AbstractMesh``, ``NumpyMesh``,
        ``NumpyMultiMesh``, or a list thereof). Meshes coming from several source energyml
        objects can be passed together (nested lists are flattened) — combine that with
        *group_by* to keep them distinguishable inside the single output file.
    :param out: Binary output stream for the ``.obj`` content.
    :param obj_name: Explicit name for the (single, implicit) ``o`` line. Wins over
        *object_namer* as long as *group_by* leaves everything in one group — this is what keeps
        existing callers (``export_mesh`` passes the output file stem) unchanged.
    :param contexts: Optional dict of :class:`RepresentationContext` keyed by
        ``source_uuid``; used to emit companion ``.mtl`` material colours when
        *mtl_out* is also provided.
    :param mtl_out: Optional binary stream for the companion ``.mtl`` file.
        Colour requires *contexts* to be supplied.
    :param use_crs_displacement: When True (default), CRS origin offset and
        axis transforms are applied to ``NumpyMesh`` points at export time.
    :param object_namer: Callable ``mesh -> str`` naming each group's ``o`` line. Called once per
        group (see *group_by*) with that group's first patch. Defaults to
        :func:`default_object_name` (the patch's URI). Wrap a function of the source energyml
        object with :func:`~energyml.utils.data.export.by_energyml_object` to name objects after
        e.g. their Citation title.
    :param group_namer: Callable ``mesh -> str`` naming each patch's ``g`` line. Defaults to
        :func:`default_group_name`, the pre-existing mapping.
    :param group_by: Callable ``mesh -> key`` splitting the export into several ``o`` objects —
        e.g. :func:`~energyml.utils.data.export.group_by_source_object` (one object per source
        representation) or :func:`~energyml.utils.data.export.group_by_qualified_type` (one per
        RESQML/EML type). ``None`` (default) keeps every patch under the single implicit object
        named by *obj_name* / *object_namer*.
    """
    from energyml.utils.data.mesh import PolylineSetMesh
    from energyml.utils.data.mesh_numpy import NumpyMesh, NumpyPointSetMesh, NumpyPolylineMesh

    patches = _normalize_to_patches(mesh_list)
    workspace = _workspace_from_contexts(contexts)
    _origin_shift = resolve_origin_shift(patches, use_crs_displacement, workspace, frame, origin_shift, use_network)

    group_namer = group_namer or default_group_name
    key_fn = group_by or (lambda _mesh: None)

    groups: Dict[Any, list] = {}
    for mesh in patches:
        groups.setdefault(key_fn(mesh), []).append(mesh)
    single_group = len(groups) <= 1

    out.write(b"# Generated by energyml-utils (Geosiris)\n\n")

    mtl_lib_name = obj_name or "materials"
    if mtl_out is not None:
        out.write(f"mtllib {mtl_lib_name}.mtl\n\n".encode())
        mtl_out.write(b"# MTL generated by energyml-utils\n\n")

    point_offset = 0

    for group_patches in groups.values():
        if single_group:
            # Exact pre-existing behaviour: obj_name wins, then object_namer, then no `o` line.
            if obj_name is not None:
                object_name = obj_name
            elif object_namer is not None:
                object_name = object_namer(group_patches[0])
            else:
                object_name = None
        else:
            # group_by produced more than one object: they need distinguishing names even when
            # the caller supplied neither obj_name nor object_namer, so fall back to
            # default_object_name instead of silently omitting every `o` line.
            object_name = (object_namer or default_object_name)(group_patches[0])

        if object_name is not None:
            out.write(f"o {object_name}\n\n".encode())

        for mesh in group_patches:
            pts, _pts_frame, _ = _get_export_points(
                mesh, use_crs_displacement, workspace, frame, _origin_shift, use_network
            )
            group_name = group_namer(mesh)
            source_uuid = getattr(mesh, "source_uuid", None) or getattr(mesh, "uuid", None)

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
                mtl_out.write(f"Kd {r / 255:.6f} {g / 255:.6f} {b / 255:.6f}\n\n".encode())

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
    companion: Optional[BinaryIO] = None,
    object_namer: Optional[MeshNamer] = None,
    group_namer: Optional[MeshNamer] = None,
    group_by: Optional[MeshGroupKey] = None,
) -> None:
    """Uniform adapter used by the registry; ``options`` is unused by OBJ."""
    export_obj(
        mesh_list,
        out,
        obj_name,
        contexts,
        companion,
        use_crs_displacement,
        frame=frame,
        origin_shift=origin_shift,
        object_namer=object_namer,
        group_namer=group_namer,
        group_by=group_by,
    )


register_format(
    FormatSpec(
        format=ExportFormat.OBJ,
        description="Wavefront OBJ — 3D geometry with optional .mtl colour",
        filter_label="OBJ Files (*.obj)",
        writer=_write,
        binary=True,
        options_class=None,
        companion_suffix=".mtl",
        supports_naming=True,
    )
)


#: Public API of this module. Declared explicitly so that renaming or removing anything
#: else is not a breaking change, and so `from ... import *` does not leak the imports.
__all__ = [
    "export_obj",
    "default_object_name",
    "default_group_name",
]
