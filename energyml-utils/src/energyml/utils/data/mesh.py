# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import logging
import os
import re
import sys
from energyml.utils.epc_file import EpcAccessMode, EpcFile
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from io import BytesIO
from typing import List, Optional, Any, Callable, Union


from energyml.utils.data.helper import read_grid2d_patch
from energyml.utils.data.crs import PointFrame, extract_crs_info, to_frame
from energyml.utils.data.mesh_numpy import (
    _fit_grid_dimensions,
    read_numpy_grid2d_representation,
    read_numpy_point_representation,
    read_numpy_polyline_representation,
    read_numpy_representation_set_representation,
    read_numpy_sub_representation,
    read_numpy_triangulated_set_representation,
    read_numpy_wellbore_frame_representation,
    read_numpy_wellbore_trajectory_representation,
)
from energyml.utils.constants import sanitize_file_name
from energyml.utils.epc_utils import gen_energyml_object_path
from energyml.utils.exception import NotSupportedError
from energyml.utils.introspection import (
    get_obj_uri,
    search_attribute_matching_name,
    snake_case,
    get_object_attribute,
)
from energyml.utils.storage_interface import EnergymlStorageInterface


# Import export functions from new export module for backward compatibility
# The writers now live in the export package; re-exported here so existing imports
# (`from energyml.utils.data.mesh import export_off`) keep working.
# Property / table / time-series readers moved to properties.py; re-exported so that
# `from energyml.utils.data.mesh import read_property` keeps working.
from energyml.utils.data.properties import (  # noqa: F401
    get_property_reader_function,
    read_abstract_values_property,
    read_categorical_property,
    read_column_based_table,
    read_comment_property,
    read_continuous_property,
    read_discrete_property,
    read_property,
    read_property_interpreted_with_cbt,
    read_time_series,
)
from energyml.utils.data.export import export_obj as _export_obj_new
from energyml.utils.data.export import export_off, export_off_part  # noqa: F401
from energyml.utils.data.export.geojson import (  # noqa: F401
    GeoJsonGeometryType,
    energyml_type_to_geojson_type,
    export_geojson_dict,
    export_geojson_io,
    mesh_to_geojson_type,
    to_geojson_feature,
    write_geojson_feature,
)

_FILE_HEADER: bytes = b"# file exported by energyml-utils python module (Geosiris)\n"

Point = list[float]

# ============================
# TODO :

# obj_GridConnectionSetRepresentation
# obj_IjkGridRepresentation
# obj_PlaneSetRepresentation
# obj_RepresentationSetRepresentation
# obj_SealedSurfaceFrameworkRepresentation
# obj_SealedVolumeFrameworkRepresentation
# obj_SubRepresentation
# obj_UnstructuredGridRepresentation
# obj_WellboreMarkerFrameRepresentation
# obj_WellboreTrajectoryRepresentation

# ============================


class MeshFileFormat(Enum):
    OFF = "off"
    OBJ = "obj"
    GEOJSON = "geojson"


@dataclass
class AbstractMesh:
    energyml_object: Any = field(default=None)

    crs_object: Any = field(default=None)

    point_list: Union[List[Point], np.ndarray] = field(
        default_factory=list,
    )

    identifier: str = field(
        default="",
    )

    frame: PointFrame = field(default=PointFrame.LOCAL)
    """
    Coordinate frame :attr:`point_list` is expressed in.

    Readers set it to what they produced; :func:`read_mesh_object` then applies only the missing
    pipeline stages, so a CRS transform cannot be applied twice.
    """

    def get_nb_edges(self) -> int:
        return 0

    def get_nb_faces(self) -> int:
        return 0

    def get_indices(self) -> Union[List[List[int]], np.ndarray]:
        return []


@dataclass
class PointSetMesh(AbstractMesh):
    pass


@dataclass
class PolylineSetMesh(AbstractMesh):
    line_indices: Union[List[List[int]], np.ndarray] = field(
        default_factory=list,
    )

    def get_nb_edges(self) -> int:
        return sum(list(map(lambda li: len(li) - 1, self.line_indices)))

    def get_nb_faces(self) -> int:
        return 0

    def get_indices(self) -> Union[List[List[int]], np.ndarray]:
        return self.line_indices


@dataclass
class SurfaceMesh(AbstractMesh):
    faces_indices: Union[List[List[int]], np.ndarray] = field(
        default_factory=list,
    )

    def get_nb_edges(self) -> int:
        return sum(list(map(lambda li: len(li) - 1, self.faces_indices)))

    def get_nb_faces(self) -> int:
        return len(self.faces_indices)

    def get_indices(self) -> Union[List[List[int]], np.ndarray]:
        return self.faces_indices


@lru_cache(maxsize=None)
def get_object_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """
    Returns the potential appropriate function to read an object whose type is named mesh_type_name.

    The lookup is a cached ``getattr`` on this module rather than a scan of every module member:
    the dispatcher is called once per object, and :func:`inspect.getmembers` sorts and reads
    *all* the attributes of the module on each call.

    Only functions **defined in this module** are eligible. The ``read_`` prefix is otherwise
    shared with helpers imported here (``read_array``, ``read_grid2d_patch``,
    ``read_parametric_geometry``), so a type named ``Array`` or ``Grid2dPatch`` used to resolve
    to one of them and then fail on its signature.

    :param mesh_type_name: the initial type name
    :return: the reader function, or None when no ``read_<snake_case(type)>`` function exists
    """
    reader = getattr(sys.modules[__name__], f"read_{snake_case(mesh_type_name)}", None)
    if not callable(reader) or getattr(reader, "__module__", None) != __name__:
        return None
    return reader


def get_mesh_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """@deprecated use get_object_reader_function instead"""
    return get_object_reader_function(mesh_type_name)


def _mesh_name_mapping(array_type_name: str) -> str:
    """
    Transform the type name to match existing reader function.

    Accepts the three spellings the same type takes across the code base: the python class name
    (``ObjTriangulatedSetRepresentation``), the schema type carried by a content type or a
    :class:`ResourceMetadata` (``obj_TriangulatedSetRepresentation``, RESQML 2.0.1 keeps the
    ``obj_`` prefix), and a qualified type (``resqml20.obj_TriangulatedSetRepresentation``).

    :param array_type_name:
    :return:
    """
    array_type_name = array_type_name.rsplit(".", 1)[-1]
    array_type_name = array_type_name.replace("3D", "3d").replace("2D", "2d")
    array_type_name = re.sub(r"^[Oo]bj_?([A-Z])", r"\1", array_type_name)
    array_type_name = re.sub(r"(Polyline|Point)Set", r"\1", array_type_name)
    return array_type_name


def read_mesh_object(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    frame: Optional[PointFrame] = None,
    use_network: bool = False,
) -> List[AbstractMesh]:
    """
    Read and "meshable" object. If :param:`energyml_object` is not supported, an exception will be raised.
    :param energyml_object: a single energyml object, or a list of them (each one is read in turn
                            and the resulting meshes are concatenated)
    :param workspace:
    :param use_crs_displacement: legacy switch, kept for compatibility. It selects the default
    target frame: :attr:`PointFrame.PROJECTED` when True (rotation, offsets, Z-flip, axis-order
    swap), :attr:`PointFrame.LOCAL` when False. Ignored when :param:`frame` is given.
    :param frame: explicit target frame, e.g. :attr:`PointFrame.WGS84`.
    :param use_network: allow PROJ to download the geoid grids used by the vertical datum
    transformation. Only relevant for :attr:`PointFrame.WGS84`.
    :return:
    """

    if isinstance(energyml_object, list):
        # a list of objects is read recursively: returning it as-is would hand back the energyml
        # objects themselves instead of the List[AbstractMesh] this function is declared to return.
        return [
            mesh
            for obj in energyml_object
            for mesh in read_mesh_object(
                energyml_object=obj,
                workspace=workspace,
                use_crs_displacement=use_crs_displacement,
                sub_indices=sub_indices,
                frame=frame,
                use_network=use_network,
            )
        ]
    array_type_name = _mesh_name_mapping(type(energyml_object).__name__)

    reader_func = get_object_reader_function(array_type_name)
    if reader_func is not None:
        surfaces: List[AbstractMesh] = reader_func(
            energyml_object=energyml_object,
            workspace=workspace,
            sub_indices=sub_indices,
            use_crs_displacement=use_crs_displacement,
        )
        # Each mesh reports the frame its reader produced, so only the missing stages are applied.
        # This replaces the previous list of type-name substrings, where a missing entry silently
        # transformed the points twice and an extra one left them untransformed.
        target = frame if frame is not None else (PointFrame.PROJECTED if use_crs_displacement else PointFrame.LOCAL)
        for s in surfaces:
            if s.frame is target or s.point_list is None or len(s.point_list) == 0:
                continue
            crs = s.crs_object[0] if isinstance(s.crs_object, list) and s.crs_object else s.crs_object
            logging.debug(f"Bringing surface {s.identifier} from {s.frame.value} to {target.value}")
            pts_arr = np.asarray(s.point_list, dtype=np.float64).reshape(-1, 3)
            framed = to_frame(
                pts_arr,
                extract_crs_info(crs, workspace) if crs is not None else None,
                target,
                s.frame,
                use_network=use_network,
                inplace=True,
            )
            s.point_list = framed.points.tolist()
            s.frame = framed.frame
        return surfaces
    else:
        # logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise NotSupportedError(
            f"Type {array_type_name} is not supported\n\tfunction read_{snake_case(array_type_name)} not found"
        )


def _legacy_identifier(patch: Any, patch_index: int) -> str:
    """Rebuild the identifier the legacy readers used to produce.

    The numpy readers label their patches ``"{TypeName}_patch_{n}"``; the legacy ones used the
    object URI (and a different wording for point sets). The strings are regenerated from the
    patch metadata rather than translated, so they stay exactly what they were.
    """
    from energyml.utils.data.mesh_numpy import NumpyPointSetMesh

    if isinstance(patch, NumpyPointSetMesh):
        return f"Patch num {patch_index}"
    # Wellbore representations were named after the object alone, with no patch suffix — and that
    # must hold whichever entry point was used, including when they are reached through a
    # RepresentationSetRepresentation.
    if "wellbore" in (patch.source_type or "").lower():
        return f"{get_obj_uri(patch.energyml_object)}"
    return f"{get_obj_uri(patch.energyml_object)}_patch{patch_index}"


def _to_legacy_meshes(
    multi: Any,
    identifier: Optional[Callable[[Any, int], str]] = None,
) -> List[AbstractMesh]:
    """Convert a :class:`~energyml.utils.data.mesh_numpy.NumpyMultiMesh` to the legacy containers.

    ``point_list`` keeps the ``(N, 3)`` float64 array produced by the numpy reader — the field is
    annotated ``Union[List[Point], np.ndarray]`` and every writer in this package already handles
    both — and the VTK flat connectivity is expanded back into the lists of indices the legacy
    containers expose through ``get_indices()``.

    :param identifier: overrides the identifier rule; called as ``identifier(patch, index)``.
    :raises NotSupportedError: for volumetric patches, which have no legacy container.
    """
    from energyml.utils.data.export._base import _parse_vtk_flat_faces, _parse_vtk_flat_lines
    from energyml.utils.data.mesh_numpy import (
        NumpyPointSetMesh,
        NumpyPolylineMesh,
        NumpySurfaceMesh,
        NumpyVolumeMesh,
    )

    meshes: List[AbstractMesh] = []
    for position, patch in enumerate(multi.flat_patches()):
        patch_index = patch.patch_index if patch.patch_index is not None else position
        name = identifier(patch, patch_index) if identifier is not None else _legacy_identifier(patch, patch_index)
        common = dict(
            identifier=name,
            energyml_object=patch.energyml_object,
            crs_object=patch.crs_object,
            point_list=patch.points,
            frame=patch.frame,
        )

        if isinstance(patch, NumpyVolumeMesh):
            raise NotSupportedError(
                f"{patch.source_type} produces a volumetric mesh, which AbstractMesh cannot hold. "
                "Use energyml.utils.data.mesh_numpy.read_numpy_mesh_object instead."
            )
        if isinstance(patch, NumpySurfaceMesh):
            meshes.append(SurfaceMesh(faces_indices=[f.tolist() for f in _parse_vtk_flat_faces(patch.faces)], **common))
        elif isinstance(patch, NumpyPolylineMesh):
            meshes.append(
                PolylineSetMesh(line_indices=[line.tolist() for line in _parse_vtk_flat_lines(patch.lines)], **common)
            )
        elif isinstance(patch, NumpyPointSetMesh):
            meshes.append(PointSetMesh(**common))
        else:
            meshes.append(AbstractMesh(**common))

    return meshes


def read_ijk_grid_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[AbstractMesh]:
    """
    Not available through the legacy containers: an IJK grid is volumetric and :class:`AbstractMesh`
    only models points, polylines and surfaces.

    :func:`energyml.utils.data.mesh_numpy.read_numpy_ijk_grid_representation` does support it.
    """
    raise NotSupportedError(
        "IjkGridRepresentation is volumetric and has no legacy AbstractMesh container. "
        "Use energyml.utils.data.mesh_numpy.read_numpy_mesh_object instead."
    )


def read_point_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PointSetMesh]:
    """Read a ``PointRepresentation`` / ``PointSetRepresentation`` into legacy containers."""
    return _to_legacy_meshes(
        read_numpy_point_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
        )
    )


def read_polyline_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PolylineSetMesh]:
    """Read a ``PolylineRepresentation`` / ``PolylineSetRepresentation`` into legacy containers."""
    return _to_legacy_meshes(
        read_numpy_polyline_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
        )
    )


def read_grid2d_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = True,
    keep_holes: bool = False,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[SurfaceMesh]:
    """Read a ``Grid2dRepresentation`` into legacy containers."""
    return _to_legacy_meshes(
        read_numpy_grid2d_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            keep_holes=keep_holes,
            sub_indices=sub_indices,
        )
    )


def read_triangulated_set_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[SurfaceMesh]:
    """Read a ``TriangulatedSetRepresentation`` into legacy containers."""
    return _to_legacy_meshes(
        read_numpy_triangulated_set_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
        )
    )


def read_wellbore_frame_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PolylineSetMesh]:
    """
    Read a WellboreFrameRepresentation and construct a polyline mesh from the trajectory.

    :param energyml_object: The WellboreFrameRepresentation object
    :param workspace: The EnergymlStorageInterface to access related objects
    :param sub_indices: Optional list of indices to filter specific nodes
    :return: List containing a single PolylineSetMesh representing the wellbore
    """
    frame_uri = f"{get_obj_uri(energyml_object)}"
    return _to_legacy_meshes(
        read_numpy_wellbore_frame_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
        ),
        identifier=lambda _patch, _index: frame_uri,
    )


def read_wellbore_trajectory_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    wellbore_frame_mds: Optional[Union[List[float], np.ndarray]] = None,
    step_meter: float = 5.0,
) -> List[PolylineSetMesh]:
    """Read a ``WellboreTrajectoryRepresentation`` into legacy containers.

    A list of trajectories is accepted and read in turn, as before.
    """
    if energyml_object is None:
        return []
    if isinstance(energyml_object, list):
        return [
            mesh
            for obj in energyml_object
            for mesh in read_wellbore_trajectory_representation(
                obj, workspace, use_crs_displacement, sub_indices, wellbore_frame_mds, step_meter
            )
        ]

    return _to_legacy_meshes(
        read_numpy_wellbore_trajectory_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
            wellbore_frame_mds=wellbore_frame_mds,
            step_meter=step_meter,
        ),
        identifier=lambda patch, _index: f"{get_obj_uri(patch.energyml_object)}",
    )


def read_sub_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[AbstractMesh]:
    """Read a ``SubRepresentation`` by delegating to its supporting representation."""
    meshes = _to_legacy_meshes(
        read_numpy_sub_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
        )
    )
    for m in meshes:
        m.identifier = f"sub representation {get_obj_uri(energyml_object)} of {m.identifier}"
    return meshes


def read_representation_set_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[AbstractMesh]:
    """Read every member representation of a ``RepresentationSetRepresentation``."""
    return _to_legacy_meshes(
        read_numpy_representation_set_representation(
            energyml_object=energyml_object,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
            sub_indices=sub_indices,
        )
    )


def gen_surface_grid_geometry(
    energyml_object: Any,
    patch: Any,
    patch_path: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    keep_holes=False,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    offset: int = 0,
):
    """
    Build the points and quad indices of one Grid2d patch.

    .. deprecated::
        No longer used internally — :func:`read_grid2d_representation` delegates to
        :func:`~energyml.utils.data.mesh_numpy.read_numpy_grid2d_representation`, which builds the
        same connectivity by broadcasting instead of a Python double loop (about 16x faster on a
        1000x1000 grid). Kept because it is public. Prefer the numpy reader.
    """
    points = read_grid2d_patch(
        patch=patch,
        grid2d=energyml_object,
        path_in_root=patch_path,
        workspace=workspace,
    )
    logging.debug(f"Total points read: {len(points)}")
    logging.debug(f"Sample points: {points[0:5]}")

    fa_count = search_attribute_matching_name(patch, "FastestAxisCount")
    if fa_count is None:
        fa_count = search_attribute_matching_name(energyml_object, "FastestAxisCount")

    sa_count = search_attribute_matching_name(patch, "SlowestAxisCount")
    if sa_count is None:
        sa_count = search_attribute_matching_name(energyml_object, "SlowestAxisCount")

    fa_count = fa_count[0]
    sa_count = sa_count[0]

    # logging.debug(f"sa_count {sa_count} fa_count {fa_count}")

    points_no_nan = []

    indice_to_final_indice = {}
    if keep_holes:
        for i in range(len(points)):
            p = points[i]
            if p[2] != p[2]:  # a NaN
                points[i][2] = 0
    else:
        for i in range(len(points)):
            p = points[i]
            if p[2] == p[2]:  # not a NaN
                indice_to_final_indice[i] = len(points_no_nan)
                points_no_nan.append(p)
    indices = []

    sa_count, fa_count = _fit_grid_dimensions(sa_count, fa_count, len(points))

    logging.debug(f"sa_count {sa_count} fa_count {fa_count} : {sa_count * fa_count} - {len(points)} ")

    for sa in range(sa_count - 1):
        for fa in range(fa_count - 1):
            line = sa * fa_count
            # if sa+1 == int(sa_count / 2) and fa == int(fa_count / 2):
            #     logging.debug(
            #         "\n\t", (line + fa), " : ", (line + fa) in indice_to_final_indice,
            #         "\n\t", (line + fa + 1), " : ", (line + fa + 1) in indice_to_final_indice,
            #         "\n\t", (line + fa_count + fa + 1), " : ", (line + fa_count + fa + 1) in indice_to_final_indice,
            #         "\n\t", (line + fa_count + fa), " : ", (line + fa_count + fa) in indice_to_final_indice,
            #     )
            if keep_holes:
                indices.append(
                    [
                        line + fa,
                        line + fa + 1,
                        line + fa_count + fa + 1,
                        line + fa_count + fa,
                    ]
                )
            elif (
                (line + fa) in indice_to_final_indice
                and (line + fa + 1) in indice_to_final_indice
                and (line + fa_count + fa + 1) in indice_to_final_indice
                and (line + fa_count + fa) in indice_to_final_indice
            ):
                indices.append(
                    [
                        indice_to_final_indice[line + fa],
                        indice_to_final_indice[line + fa + 1],
                        indice_to_final_indice[line + fa_count + fa + 1],
                        indice_to_final_indice[line + fa_count + fa],
                    ]
                )
    if sub_indices is not None and len(sub_indices) > 0:
        new_indices = []
        for idx in sub_indices:
            t_idx = idx - offset
            if 0 <= t_idx < len(indices):
                new_indices.append(indices[t_idx])
        indices = new_indices
    # logging.debug(indices)

    return points if keep_holes else points_no_nan, indices


#     __  ______________ __  __   _____ __             ____                           __
#    /  |/  / ____/ ___// / / /  / __(_) /__  _____   / __/___  _________ ___  ____ _/ /_
#   / /|_/ / __/  \__ \/ /_/ /  / /_/ / / _ \/ ___/  / /_/ __ \/ ___/ __ `__ \/ __ `/ __/
#  / /  / / /___ ___/ / __  /  / __/ / /  __(__  )  / __/ /_/ / /  / / / / / / /_/ / /_
# /_/  /_/_____//____/_/ /_/  /_/ /_/_/\___/____/  /_/  \____/_/  /_/ /_/ /_/\__,_/\__/


def export_obj(mesh_list: List[AbstractMesh], out: BytesIO, obj_name: Optional[str] = None):
    """
    Export an :class:`AbstractMesh` into obj format.

    This function is maintained for backward compatibility and delegates to the
    export module. For new code, consider importing from energyml.utils.data.export.

    Each AbstractMesh from the list :param:`mesh_list` will be placed into its own group.
    :param mesh_list:
    :param out:
    :param obj_name:
    :return:
    """
    # Delegate to the new export module
    _export_obj_new(mesh_list, out, obj_name)


def _list_exportable_uuids(epc: EnergymlStorageInterface, logger: Optional[Any] = None) -> List[str]:
    """
    Return the uuids of every object of the EPC that has a mesh reader (i.e. that can be
    exported as a 3D / GeoJSON file).
    """
    uuids: List[str] = []
    for metadata in epc.list_objects():
        object_type = getattr(metadata, "object_type", None)
        uuid = getattr(metadata, "uuid", None)
        if not object_type or not uuid or uuid in uuids:
            continue
        if get_object_reader_function(_mesh_name_mapping(object_type)) is not None:
            uuids.append(uuid)
    (logger or logging).debug(f"{len(uuids)} exportable representations found")
    return uuids


def export_multiple_data(
    epc_path: str,
    uuid_list: Optional[List[str]] = None,
    output_folder_path: str = ".",
    output_file_path_suffix: str = "",
    file_format: MeshFileFormat = MeshFileFormat.OBJ,
    use_crs_displacement: bool = True,
    logger: Optional[Any] = None,
    to_wgs84: bool = True,
    use_network: bool = False,
):
    """
    :param uuid_list: uuids of the representations to export. When None or empty, every
                      exportable representation of the EPC is exported.
    :param to_wgs84: GeoJSON only — reproject the coordinates to WGS84 (RFC 7946) when the EPSG
                     codes are available and ``pyproj`` is installed.
    :param use_network: GeoJSON only — allow PROJ to download the geoid grids needed by the
                        vertical datum transformation.
    """
    logging.debug(f"Opening epc : {epc_path}")
    epc = EpcFile(epc_file_path=epc_path, mode=EpcAccessMode.MANUAL, compact_on_close=False)
    logging.debug("Opened")

    if not uuid_list:
        uuid_list = _list_exportable_uuids(epc, logger)

    # with open(epc_path.replace(".epc", ".h5"), "rb") as fh:
    #     buf = BytesIO(fh.read())
    #     epc.h5_io_files.append(buf)

    try:
        os.makedirs(output_folder_path, exist_ok=True)
    except OSError:
        pass

    for uuid in uuid_list:
        energyml_obj = None
        try:
            energyml_obj = epc.get_object_by_uuid(uuid)[0]
        except Exception as e:
            # a bare `except` here also swallowed KeyboardInterrupt / SystemExit
            (logger or logging).error(f"Object with uuid {uuid} not found : {type(e).__name__}: {e}")
            continue
        # A citation title is free text and lands in the file name: sanitize it, or a title
        # containing ':' (e.g. "AUB-PRO-SP05512: Trajectory") silently writes into an NTFS
        # alternate data stream on Windows, leaving an empty extension-less file behind.
        # The extension is appended after sanitizing so it can never be truncated away.
        file_name = sanitize_file_name(
            f"{gen_energyml_object_path(energyml_obj)}_"
            f"[{get_object_attribute(energyml_obj, 'citation.title')}]"
            f"{output_file_path_suffix}"
        )
        file_path = os.path.join(output_folder_path, f"{file_name}.{file_format.value}")
        logging.debug(f"Exporting : {file_path}")

        # a representation that cannot be read (e.g. a trajectory without geometry) must not
        # stop the export of the others
        try:
            mesh_list = read_mesh_object(
                energyml_object=energyml_obj,
                workspace=epc,
                use_crs_displacement=use_crs_displacement,
            )

            if file_format == MeshFileFormat.OBJ:
                with open(file_path, "wb") as f:
                    export_obj(
                        mesh_list=mesh_list,
                        out=f,
                    )
            elif file_format == MeshFileFormat.OFF:
                with open(file_path, "wb") as f:
                    export_off(
                        mesh_list=mesh_list,
                        out=f,
                    )
            elif file_format == MeshFileFormat.GEOJSON:
                with open(file_path, "wb") as f:
                    export_geojson_io(
                        out=f,
                        mesh_list=mesh_list,
                        obj_name=get_object_attribute(energyml_obj, "citation.title"),
                        logger=logger,
                        workspace=epc,
                        to_wgs84=to_wgs84,
                        use_network=use_network,
                        global_properties={"epc_path": epc_path},
                        indent=2,
                    )
            else:
                logging.error(f"Code is not written for format {file_format}")
        except Exception as e:
            (logger or logging).error(f"Failed to export the object {uuid} : {type(e).__name__}: {e}")
