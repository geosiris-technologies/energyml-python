# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import json
import logging
import os
import re
import sys
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import List, Optional, Any, Callable, Dict, Union, Tuple


from .helper import (
    apply_crs_transform,
    generate_vertical_well_points,
    get_crs_offsets_and_angle,
    get_datum_information,
    get_wellbore_points,
    hermite_interpolation,
    read_array,
    read_grid2d_patch,
    get_crs_obj,
    get_crs_origin_offset,
    is_z_reversed,
    read_parametric_geometry,
)
from energyml.utils.epc_utils import gen_energyml_object_path
from energyml.utils.epc_stream import EpcStreamReader
from energyml.utils.exception import NotSupportedError, ObjectNotFoundNotError
from energyml.utils.introspection import (
    get_obj_uri,
    search_attribute_matching_name,
    search_attribute_matching_name_with_path,
    snake_case,
    get_object_attribute,
    get_object_attribute_rgx,
)
from energyml.utils.storage_interface import EnergymlStorageInterface


# Import export functions from new export module for backward compatibility
from .export import export_obj as _export_obj_new

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


def crs_displacement(points: List[Point], crs_obj: Any) -> Tuple[List[Point], Point]:
    """
    Transform a point list with CRS information (XYZ offset and ZIncreasingDownward)
    :param points: in/out : the list is directly modified
    :param crs_obj:
    :return: The translated points and the crs offset vector.
    """
    crs_point_offset = get_crs_origin_offset(crs_obj=crs_obj)
    zincreasing_downward = is_z_reversed(crs_obj)

    if crs_point_offset != [0, 0, 0]:
        for p in points:
            for xyz in range(len(p)):
                p[xyz] = (p[xyz] + crs_point_offset[xyz]) if p[xyz] is not None else None
            if zincreasing_downward and len(p) >= 3:
                p[2] = -p[2]

    return points, crs_point_offset


def get_object_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """
    Returns the name of the potential appropriate function to read an object with type is named mesh_type_name
    :param mesh_type_name: the initial type name
    :return:
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name == f"read_{snake_case(mesh_type_name)}":
            return obj
    return None


def get_mesh_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """@deprecated use get_object_reader_function instead"""
    return get_object_reader_function(mesh_type_name)


def _mesh_name_mapping(array_type_name: str) -> str:
    """
    Transform the type name to match existing reader function
    :param array_type_name:
    :return:
    """
    array_type_name = array_type_name.replace("3D", "3d").replace("2D", "2d")
    array_type_name = re.sub(r"^[Oo]bj([A-Z])", r"\1", array_type_name)
    array_type_name = re.sub(r"(Polyline|Point)Set", r"\1", array_type_name)
    return array_type_name


def read_mesh_object(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_crs_displacement: bool = False,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[AbstractMesh]:
    """
    Read and "meshable" object. If :param:`energyml_object` is not supported, an exception will be raised.
    :param energyml_object:
    :param workspace:
    :param use_crs_displacement: If true the :py:function:`crs_displacement <energyml.utils.mesh.crs_displacement>`
    is used to translate the data with the CRS offsets
    :return:
    """

    if isinstance(energyml_object, list):
        return energyml_object
    array_type_name = _mesh_name_mapping(type(energyml_object).__name__)

    reader_func = get_object_reader_function(array_type_name)
    if reader_func is not None:
        # logging.info(f"using function {reader_func} to read type {array_type_name}")
        surfaces: List[AbstractMesh] = reader_func(
            energyml_object=energyml_object, workspace=workspace, sub_indices=sub_indices
        )
        if (
            use_crs_displacement and "wellbore" not in array_type_name.lower()
        ):  # WellboreFrameRep has allready the displacement applied
            # TODO: the displacement should be done in each reader function to manage specific cases
            for s in surfaces:
                print("CRS : ", s.crs_object.uuid if s.crs_object is not None else "None")
                crs_displacement(s.point_list, s.crs_object)
        return surfaces
    else:
        # logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise NotSupportedError(
            f"Type {array_type_name} is not supported\n\tfunction read_{snake_case(array_type_name)} not found"
        )


def read_ijk_grid_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[Any]:
    raise NotSupportedError("IJKGrid representation reading is not supported yet.")


def read_point_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PointSetMesh]:
    # pt_geoms = search_attribute_matching_type(point_set, "AbstractGeometry")

    meshes = []

    patch_idx = 0
    total_size = 0
    for (
        points_path_in_obj,
        points_obj,
    ) in search_attribute_matching_name_with_path(
        energyml_object, r"NodePatch.[\d]+.Geometry.Points"
    ) + search_attribute_matching_name_with_path(  # resqml 2.0.1
        energyml_object, r"NodePatchGeometry.[\d]+.Points"
    ):  # resqml 2.2
        points = read_array(
            energyml_array=points_obj,
            root_obj=energyml_object,
            path_in_root=points_path_in_obj,
            workspace=workspace,
        )

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=points_obj,
                path_in_root=points_path_in_obj,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError as e:
            logging.error(e)
            pass

        if sub_indices is not None and len(sub_indices) > 0:
            new_points = []
            for idx in sub_indices:
                t_idx = idx - total_size
                if 0 <= t_idx < len(points):
                    new_points.append(points[t_idx])
            total_size = total_size + len(points)
            points = new_points
        # else:
        #     total_size = total_size + len(points)

        if points is not None:
            meshes.append(
                PointSetMesh(
                    identifier=f"Patch num {patch_idx}",
                    energyml_object=energyml_object,
                    crs_object=crs,
                    point_list=points,
                )
            )

        patch_idx = patch_idx + 1

    return meshes


def read_polyline_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PolylineSetMesh]:
    # pt_geoms = search_attribute_matching_type(point_set, "AbstractGeometry")

    meshes = []

    patch_idx = 0
    total_size = 0
    for patch_path_in_obj, patch in search_attribute_matching_name_with_path(
        energyml_object, "NodePatch"
    ) + search_attribute_matching_name_with_path(energyml_object, r"LinePatch.[\d]+"):

        pts = search_attribute_matching_name_with_path(patch, "Geometry.Points")
        if pts is None or len(pts) == 0:
            pts = search_attribute_matching_name_with_path(patch, "Points")

        try:
            points_path, points_obj = pts[0]
        except Exception as e:
            logging.error(f"Cannot find points for patch {patch_path_in_obj} : {e}")
            logging.error(patch)
            raise e

        points = read_array(
            energyml_array=points_obj,
            root_obj=energyml_object,
            path_in_root=patch_path_in_obj + "." + points_path,
            workspace=workspace,
        )

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=points_obj,
                path_in_root=patch_path_in_obj + "." + points_path,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError as e:
            logging.error(e)

        close_poly = None
        try:
            (
                close_poly_path,
                close_poly_obj,
            ) = search_attribute_matching_name_with_path(
                patch, "ClosedPolylines"
            )[0]
            close_poly = read_array(
                energyml_array=close_poly_obj,
                root_obj=energyml_object,
                path_in_root=patch_path_in_obj + "." + close_poly_path,
                workspace=workspace,
            )
        except IndexError:
            pass

        point_indices = []
        try:
            (
                node_count_per_poly_path_in_obj,
                node_count_per_poly,
            ) = search_attribute_matching_name_with_path(
                patch, "NodeCountPerPolyline"
            )[0]
            node_counts_list = read_array(
                energyml_array=node_count_per_poly,
                root_obj=energyml_object,
                path_in_root=patch_path_in_obj + node_count_per_poly_path_in_obj,
                workspace=workspace,
            )
            idx = 0
            poly_idx = 0
            for nb_node in node_counts_list:
                point_indices.append([x for x in range(idx, idx + nb_node)])
                if close_poly is not None and len(close_poly) > poly_idx and close_poly[poly_idx]:
                    point_indices[len(point_indices) - 1].append(idx)
                idx = idx + nb_node
                poly_idx = poly_idx + 1
        except IndexError:
            # No NodeCountPerPolyline for Polyline but only in PolylineSet
            pass

        if point_indices is None or len(point_indices) == 0:
            # No indices ==> all point in the polyline
            point_indices = [list(range(len(points)))]

        if sub_indices is not None and len(sub_indices) > 0:
            new_indices = []
            for idx in sub_indices:
                t_idx = idx - total_size
                if 0 <= t_idx < len(point_indices):
                    new_indices.append(point_indices[t_idx])
            total_size = total_size + len(point_indices)
            point_indices = new_indices
        else:
            total_size = total_size + len(point_indices)

        if len(points) > 0:
            meshes.append(
                PolylineSetMesh(
                    identifier=f"{get_obj_uri(energyml_object)}_patch{patch_idx}",
                    energyml_object=energyml_object,
                    crs_object=crs,
                    point_list=points,
                    line_indices=point_indices,
                )
            )

        patch_idx = patch_idx + 1

    return meshes


def gen_surface_grid_geometry(
    energyml_object: Any,
    patch: Any,
    patch_path: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    keep_holes=False,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    offset: int = 0,
):
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

    while sa_count * fa_count > len(points):
        sa_count = sa_count - 1
        fa_count = fa_count - 1

    while sa_count * fa_count < len(points):
        sa_count = sa_count + 1
        fa_count = fa_count + 1

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


def read_grid2d_representation(
    energyml_object: Any,
    workspace: Optional[EnergymlStorageInterface] = None,
    keep_holes=False,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[SurfaceMesh]:
    # h5_reader = HDF5FileReader()
    meshes = []

    if sub_indices is not None:
        sub_indices = list(sorted(sub_indices))

    patch_idx = 0
    total_size = 0

    # Resqml 201
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

        points, indices = gen_surface_grid_geometry(
            energyml_object=energyml_object,
            patch=patch,
            patch_path=patch_path,
            workspace=workspace,
            keep_holes=keep_holes,
            sub_indices=sub_indices,
            offset=total_size,
        )

        total_size = total_size + len(indices)

        meshes.append(
            SurfaceMesh(
                identifier=f"{get_obj_uri(energyml_object)}_patch{patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=points,
                faces_indices=indices,
            )
        )
        patch_idx = patch_idx + 1

    # Resqml 22
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
        # geometry = energyml_object.geometry
        # points = read_grid2d_patch(
        #     patch=energyml_object,
        #     grid2d=energyml_object,
        #     path_in_root="",
        #     workspace=workspace,
        # )
        points, indices = gen_surface_grid_geometry(
            energyml_object=energyml_object,
            patch=energyml_object,
            patch_path="",
            workspace=workspace,
            keep_holes=keep_holes,
            sub_indices=sub_indices,
            offset=total_size,
        )
        meshes.append(
            SurfaceMesh(
                identifier=f"{get_obj_uri(energyml_object)}_patch{patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=points,
                faces_indices=indices,
            )
        )

    return meshes


def read_triangulated_set_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[SurfaceMesh]:
    meshes = []

    point_offset = 0
    patch_idx = 0
    total_size = 0
    for patch_path, patch in search_attribute_matching_name_with_path(
        energyml_object,
        "\\.*Patch.\\d+",
        deep_search=False,
        search_in_sub_obj=False,
    ):
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

        point_list: List[Point] = []
        for point_path, point_obj in search_attribute_matching_name_with_path(patch, "Geometry.Points"):
            _array = read_array(
                energyml_array=point_obj,
                root_obj=energyml_object,
                path_in_root=patch_path + "." + point_path,
                workspace=workspace,
            )
            if isinstance(_array, np.ndarray):
                _array = _array.tolist()

            point_list = point_list + _array

        triangles_list: List[List[int]] = []
        for (
            triangles_path,
            triangles_obj,
        ) in search_attribute_matching_name_with_path(patch, "Triangles"):
            _array = read_array(
                energyml_array=triangles_obj,
                root_obj=energyml_object,
                path_in_root=patch_path + "." + triangles_path,
                workspace=workspace,
            )
            if isinstance(_array, np.ndarray):
                _array = _array.tolist()
            triangles_list = triangles_list + _array

        triangles_list = list(map(lambda tr: [ti - point_offset for ti in tr], triangles_list))
        if sub_indices is not None and len(sub_indices) > 0:
            new_triangles_list = []
            for idx in sub_indices:
                t_idx = idx - total_size
                if 0 <= t_idx < len(triangles_list):
                    new_triangles_list.append(triangles_list[t_idx])
            total_size = total_size + len(triangles_list)
            triangles_list = new_triangles_list
        else:
            total_size = total_size + len(triangles_list)
        meshes.append(
            SurfaceMesh(
                identifier=f"{get_obj_uri(energyml_object)}_patch{patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=point_list,
                faces_indices=triangles_list,
            )
        )
        point_offset = point_offset + len(point_list)
        patch_idx += 1

    return meshes


def read_wellbore_frame_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PolylineSetMesh]:
    """
    Read a WellboreFrameRepresentation and construct a polyline mesh from the trajectory.

    :param energyml_object: The WellboreFrameRepresentation object
    :param workspace: The EnergymlStorageInterface to access related objects
    :param sub_indices: Optional list of indices to filter specific nodes
    :return: List containing a single PolylineSetMesh representing the wellbore
    """

    meshes = []

    try:
        # Read measured depths (NodeMd)
        wellbore_frame_mds = None
        try:
            node_md_path, node_md_obj = search_attribute_matching_name_with_path(energyml_object, "NodeMd")[0]
            wellbore_frame_mds = read_array(
                energyml_array=node_md_obj,
                root_obj=energyml_object,
                path_in_root=node_md_path,
                workspace=workspace,
            )
            # Ensure wellbore_frame_mds is a numpy array for filtering operations
            if not isinstance(wellbore_frame_mds, np.ndarray):
                wellbore_frame_mds = np.array(wellbore_frame_mds)
        except (IndexError, AttributeError) as e:
            logging.warning(f"Could not read NodeMd from wellbore frame: {e}")
            return meshes

        # Get reference point (wellhead location) - try different attribute paths for different versions
        md_min = np.min(wellbore_frame_mds) if len(wellbore_frame_mds) > 0 else 0.0
        md_max = np.max(wellbore_frame_mds) if len(wellbore_frame_mds) > 0 else 0.0

        try:
            # Only works for RESQML 2.2+
            _md_min = get_object_attribute(energyml_object, "md_interval.md_min")
            if _md_min is not None:
                md_min = _md_min
            _md_max = get_object_attribute(energyml_object, "md_interval.md_max")
            if _md_max is not None:
                md_max = _md_max
        except AttributeError:
            # logging.debug(
            #     "Could not get md_interval.md_min or md_interval.md_max, using NodeMd min/max instead"
            # )
            pass

        # remove md values from array if outside of md_min/md_max range (can happen if md_interval is used and NodeMd contains values outside of the interval)
        wellbore_frame_mds = wellbore_frame_mds[(wellbore_frame_mds >= md_min) & (wellbore_frame_mds <= md_max)]

        # Get trajectory reference
        trajectory_dor = search_attribute_matching_name(obj=energyml_object, name_rgx="Trajectory")[0]
        trajectory_obj = workspace.get_object(get_obj_uri(trajectory_dor))

        meshes = read_wellbore_trajectory_representation(
            energyml_object=trajectory_obj,
            workspace=workspace,
            sub_indices=sub_indices,
            wellbore_frame_mds=wellbore_frame_mds,
        )
        for mesh in meshes:
            mesh.identifier = f"{get_obj_uri(energyml_object)}"
        return meshes
    except Exception as e:
        logging.error(f"Failed to read wellbore frame representation: {e}")
        import traceback

        traceback.print_exc()

    return meshes


def read_wellbore_trajectory_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
    wellbore_frame_mds: Optional[Union[List[float], np.ndarray]] = None,
    step_meter: float = 5.0,
) -> List[PolylineSetMesh]:
    if energyml_object is None:
        return []

    if isinstance(energyml_object, list):
        return [
            mesh
            for obj in energyml_object
            for mesh in read_wellbore_trajectory_representation(
                obj, workspace, sub_indices, wellbore_frame_mds, step_meter
            )
        ]

    # CRS
    crs = None
    head_x, head_y, head_z, z_increasing_downward, projected_epsg_code, vertical_epsg_code = (
        0.0,
        0.0,
        0.0,
        False,
        None,
        None,
    )

    # Get CRS from trajectory geometry if available
    try:
        crs = workspace.get_object(get_obj_uri(get_object_attribute(energyml_object, "geometry.LocalCrs")))
    except Exception as e:
        logging.debug(f"Could not get CRS from trajectory geometry")

    # ==========
    # MD Datum
    # ==========
    try:
        # Try to get MdDatum (RESQML 2.0.1) or MdInterval.Datum (RESQML 2.2+)
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
            md_datum_obj = workspace.get_object(md_datum_identifier)

            if md_datum_obj is not None:
                head_x, head_y, head_z, z_increasing_downward, projected_epsg_code, vertical_epsg_code = (
                    get_datum_information(md_datum_obj, workspace)
                )
    except Exception as e:
        logging.debug(f"Could not get reference point / Datum from trajectory: {e}")

    # ==========
    well_points = None
    try:
        x_offset, y_offset, z_offset, (azimuth, azimuth_uom) = get_crs_offsets_and_angle(crs, workspace)
        # Try to read parametric Geometry from the trajectory.
        traj_mds, traj_points, traj_tangents = read_parametric_geometry(
            getattr(energyml_object, "geometry", None), workspace
        )
        well_points = get_wellbore_points(wellbore_frame_mds, traj_mds, traj_points, traj_tangents, step_meter)

        well_points = apply_crs_transform(
            well_points,
            x_offset=x_offset,
            y_offset=y_offset,
            z_offset=z_offset,
            z_is_up=not z_increasing_downward,
            areal_rotation=azimuth,
            rotation_uom=azimuth_uom,
        )
    except Exception as e:
        if wellbore_frame_mds is not None:
            logging.debug(f"Could not read parametric geometry from trajectory. Well is interpreted as vertical: {e}")
            well_points = generate_vertical_well_points(
                head_x=head_x,
                head_y=head_y,
                head_z=head_z,
                wellbore_mds=wellbore_frame_mds,
            )
        else:
            raise ValueError(
                "Cannot read wellbore trajectory representation: no parametric geometry and no measured depth information available to generate points"
            ) from e

    meshes = []
    if well_points is not None and len(well_points) > 0:

        meshes.append(
            PolylineSetMesh(
                identifier=f"{get_obj_uri(energyml_object)}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=well_points,
                line_indices=[[i, i + 1] for i in range(len(well_points) - 1)],
            )
        )
    return meshes


def read_sub_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[AbstractMesh]:
    supporting_rep_dor = search_attribute_matching_name(
        obj=energyml_object, name_rgx=r"(SupportingRepresentation|RepresentedObject)"
    )[0]
    supporting_rep_identifier = get_obj_uri(supporting_rep_dor)
    supporting_rep = workspace.get_object(supporting_rep_identifier)

    total_size = 0
    all_indices = None
    for patch_path, patch_indices in search_attribute_matching_name_with_path(
        obj=energyml_object,
        name_rgx="SubRepresentationPatch.\\d+.ElementIndices.\\d+.Indices",
        deep_search=False,
        search_in_sub_obj=False,
    ) + search_attribute_matching_name_with_path(
        obj=energyml_object,
        name_rgx="SubRepresentationPatch.\\d+.Indices",
        deep_search=False,
        search_in_sub_obj=False,
    ):
        array = read_array(
            energyml_array=patch_indices,
            root_obj=energyml_object,
            path_in_root=patch_path,
            workspace=workspace,
            sub_indices=sub_indices,
        )

        if sub_indices is not None and len(sub_indices) > 0:
            new_array = []
            for idx in sub_indices:
                t_idx = idx - total_size
                if 0 <= t_idx < len(array):
                    new_array.append(array[t_idx])
            total_size = total_size + len(array)
            array = new_array
        else:
            total_size = total_size + len(array)

        all_indices = all_indices + array if all_indices is not None else array
    meshes = read_mesh_object(
        energyml_object=supporting_rep,
        workspace=workspace,
        sub_indices=all_indices,
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

    repr_list = get_object_attribute(energyml_object, "representation")
    if repr_list is None or not isinstance(repr_list, list):
        logging.error(
            f"RepresentationSetRepresentation {get_obj_uri(energyml_object)} has no 'representation' list attribute"
        )
        return []

    meshes = []
    for repr_dor in repr_list:
        rpr_uri = get_obj_uri(repr_dor)
        repr_obj = workspace.get_object(rpr_uri)
        if repr_obj is None:
            logging.error(f"Representation {rpr_uri} in RepresentationSetRepresentation not found")
            continue
        meshes.extend(
            read_mesh_object(energyml_object=repr_obj, workspace=workspace, use_crs_displacement=use_crs_displacement)
        )

    return meshes


def read_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a property or column-based table from an Energyml object.

    Dispatches to the appropriate reader function based on the object's type name.
    If no specific reader is found, raises a NotSupportedError.

    Args:
        energyml_object: The Energyml object to read from.
        workspace: The storage interface for accessing related objects.

    Returns:
        np.ndarray: The read property or table data.

    Raises:
        NotSupportedError: If the object type is not supported.
    """
    property_type = type(energyml_object).__name__
    reader_func = get_object_reader_function(property_type)
    if reader_func is not None:
        return reader_func(energyml_object=energyml_object, workspace=workspace)
    else:
        # logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise NotSupportedError(
            f"Type {property_type} is not supported\n\tfunction read_{snake_case(property_type)} not found"
        )


def read_property_interpreted_with_cbt(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    _cache_property_arrays: Optional[np.ndarray] = None,
    _return_none_if_no_category_lookup: bool = False,
) -> Optional[np.ndarray]:
    """
    Read a property with category lookup interpretation.

    Reads property arrays and applies category lookup mapping if available.
    Supports both array and dictionary-based category lookups.

    Args:
        energyml_object: The Energyml property object.
        workspace: The storage interface for accessing related objects.
        _cache_property_arrays: Optional cached property arrays to avoid re-reading.
        _return_none_if_no_category_lookup: If True, return None when no category lookup is found.

    Returns:
        Optional[np.ndarray]: The interpreted property values, or None if no lookup and flag is set.
    """

    result = None

    prop_arrays = (
        read_property(energyml_object, workspace) if _cache_property_arrays is None else _cache_property_arrays
    )

    category_lookup_dor = get_object_attribute(energyml_object, "category_lookup")
    if category_lookup_dor is not None:
        category_lookup_obj = workspace.get_object(get_obj_uri(category_lookup_dor))
        if category_lookup_obj is not None:
            category_lookup_data = read_column_based_table(category_lookup_obj, workspace)

            # print(f"category_lookup_array : {category_lookup_data}")
            if isinstance(category_lookup_data, list):
                category_lookup_data = np.array(category_lookup_data)
            if isinstance(category_lookup_data, np.ndarray):
                # map props values to category lookup values using prop value as index in category lookup array
                result = (
                    np.array(
                        [
                            (
                                category_lookup_data[prop]
                                if prop is not None and prop < len(category_lookup_data)
                                else None
                            )
                            for prop in prop_arrays
                        ]
                    )
                    if prop_arrays is not None
                    else None
                )
            elif isinstance(category_lookup_data, dict):
                # Transpose so that each index corresponds to a category (column), not a row
                category_lookup_matrice = np.array(list(category_lookup_data.values())).T
                print(f"category_lookup_matrice : {category_lookup_matrice}")
                # return a matrice with the same shape as prop_arrays but with the values from the category lookup array using the prop value as key in the category lookup array
                result = (
                    np.array(
                        [
                            [
                                (
                                    category_lookup_matrice[prop].tolist()
                                    if prop is not None and 0 <= prop < len(category_lookup_matrice)
                                    else None
                                )
                                for prop in prop_row
                            ]
                            for prop_row in prop_arrays
                        ]
                    )
                    if prop_arrays is not None
                    else None
                )
            else:
                raise NotSupportedError(
                    f"Category lookup array type {type(category_lookup_matrice)} is not supported, expected list or dict"
                )

    return prop_arrays if result is None and not _return_none_if_no_category_lookup else result


def read_abstract_values_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read abstract values property from patches.

    Extracts and concatenates arrays from all 'values_for_patch' attributes.

    Args:
        energyml_object: The Energyml object containing the property.
        workspace: The storage interface for accessing arrays.

    Returns:
        np.ndarray: The concatenated array of property values.
    """
    arrays = []
    for values_for_patch in search_attribute_matching_name_with_path(energyml_object, "values_for_patch"):
        array = read_array(
            energyml_array=values_for_patch[1],
            root_obj=energyml_object,
            path_in_root=".",
            workspace=workspace,
        )
        if isinstance(array, list):
            array = np.array(array)
        arrays.append(array)
    if len(arrays) == 1:
        return arrays[0]
    else:
        return np.concatenate(arrays)


def read_discrete_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a discrete property.

    Delegates to read_abstract_values_property for implementation.

    Args:
        energyml_object: The discrete property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The property values.
    """

    return read_abstract_values_property(energyml_object, workspace)


def read_continuous_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a continuous property.

    Delegates to read_abstract_values_property for implementation.

    Args:
        energyml_object: The continuous property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The property values.
    """

    return read_abstract_values_property(energyml_object, workspace)


def read_categorical_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a categorical property.

    Note: Categorical values are returned as integers. Use the property's
    'code_list' attribute to map to string values.

    Args:
        energyml_object: The categorical property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The integer-coded property values.
    """
    # TODO: the categorical values should be converted to strings using the code list of the property, but for now we keep the integer values and let the user manage the conversion if needed.
    logging.warning(
        "CategoricalProperty is read as a continuous property, the categorical values are not converted to strings but kept as integers. Use the 'code_list' attribute of the property to get the list of possible string values corresponding to the integer values in the array"
    )
    return read_abstract_values_property(energyml_object, workspace)


def read_comment_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a comment property.

    Delegates to read_abstract_values_property for implementation.

    Args:
        energyml_object: The comment property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The comment values.
    """
    return read_abstract_values_property(energyml_object, workspace)


def read_column_based_table(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> Dict[str, np.ndarray]:
    """
    Read a column-based table.

    Extracts column data into a dictionary keyed by column titles.

    Args:
        energyml_object: The table object with 'column' attributes.
        workspace: The storage interface for accessing arrays.

    Returns:
        Dict[str, np.ndarray]: Dictionary of column names to arrays.
    """
    columns = {}
    for column in get_object_attribute(energyml_object, "column"):
        column_name = getattr(column, "title", "_")
        # print(f"Reading column: {column_name} : {column}")
        # print(f"getattr(column_array, 'values', None): {getattr(column, 'values', None)}")
        array = read_array(
            energyml_array=getattr(column, "values", None),
            root_obj=energyml_object,
            path_in_root=".",
            workspace=workspace,
        )
        if isinstance(array, list):
            array = np.array(array)
        columns[column_name] = array
    return columns


def read_time_series(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> List[Dict[str, Tuple[str, int]]]:
    """
    Read a time series from an Energyml object.

    Extracts date-time values and time step indices, constructing a normalized
    list of (step_index, datetime) tuples for each time step.

    Args:
        energyml_object: The Energyml time series object.
        workspace: The storage interface for accessing related objects.

    Returns:
        List[Tuple[str, int]]: List of tuples containing (step_index, datetime_string).
    """

    # 1. Extraction des DateTime
    times_iso = search_attribute_matching_name(energyml_object, "date_time")

    # 2. Extraction des TimeSteps (v2.2+)
    steps_indices = []
    time_step_obj = get_object_attribute(energyml_object, "time_step")
    if time_step_obj is not None:
        steps_indices = read_array(time_step_obj, energyml_object, ".", workspace, sub_indices=None)
    else:
        # Fallback : on utilise l'index de la liste
        steps_indices = list(range(len(times_iso)))

    # 3. Construction de la structure normalisée
    steps_data = []
    for i in range(len(times_iso)):
        steps_data.append(
            (steps_indices[i], times_iso[i])
            # {"index": i, "datetime": times_iso[i], "step_val": steps_indices[i]}  # L'index utilisé par les propriétés
        )

    return steps_data


#     __  ______________ __  __   _____ __             ____                           __
#    /  |/  / ____/ ___// / / /  / __(_) /__  _____   / __/___  _________ ___  ____ _/ /_
#   / /|_/ / __/  \__ \/ /_/ /  / /_/ / / _ \/ ___/  / /_/ __ \/ ___/ __ `__ \/ __ `/ __/
#  / /  / / /___ ___/ / __  /  / __/ / /  __(__  )  / __/ /_/ / /  / / / / / / /_/ / /_
# /_/  /_/_____//____/_/ /_/  /_/ /_/_/\___/____/  /_/  \____/_/  /_/ /_/ /_/\__,_/\__/


def _recompute_min_max(
    old_min: List,  # out parameters
    old_max: List,  # out parameters
    potential_min: List,
    potential_max: List,
) -> None:
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
    old_min: List,  # out parameters
    old_max: List,  # out parameters
    points: Union[List[Point], Point],
) -> None:
    if len(points) > 0:
        if isinstance(points[0], list):
            for p in points:
                _recompute_min_max_from_points(old_min, old_max, p)
        else:
            _recompute_min_max(old_min, old_max, points, points)


def _create_shape(
    geo_type: GeoJsonGeometryType,
    point_list: List[List[float]],
    indices: Optional[Union[List[List[int]], List[int]]] = None,
    point_offset: int = 0,
    logger: Optional[Any] = None,
) -> Tuple[List, List[float], List[float]]:
    """
    Creates a shape from a point list [ [x0, y0 (, z0)? ], ..., [xn, yn (, zn)? ] ]
    using indices. If indices is a simple list, result will be a line like :  [p0, ..., pn]. With p0 and pn
    a list of coordinate from "points" parameter (like [x0, y0 (, z0)? ])
    If the indices are a list of list, result will be polygones like :
    [
        [poly0_p0, ..., poly0_pn],
        ...
        [polyn_p0, ..., polyn_pn],
    ]
    :return shape, minXYZ (as list), maxXYZ (as list)
    """
    mins = []
    maxs = []
    result = None
    try:
        if geo_type == GeoJsonGeometryType.LineString:
            result = []
            if indices is not None and len(indices) > 0:
                for idx in indices:
                    result.append(point_list[idx + point_offset])
                    _recompute_min_max_from_points(mins, maxs, point_list[idx + point_offset])
            else:
                result = point_list
                _recompute_min_max_from_points(mins, maxs, result)
        elif geo_type == GeoJsonGeometryType.MultiPoint or geo_type == GeoJsonGeometryType.Point:
            result = point_list
            _recompute_min_max_from_points(mins, maxs, result)
        elif geo_type == GeoJsonGeometryType.MultiLineString:
            if indices is not None and len(indices) > 0 and isinstance(indices[0], list):
                result = []
                for idx in indices:
                    _res, _min, _max = _create_shape(
                        geo_type=GeoJsonGeometryType.MultiLineString,
                        point_list=point_list,
                        indices=idx,
                        point_offset=point_offset,
                        logger=logger,
                    )
                    result = result + _res
                    _recompute_min_max(mins, maxs, _min, _max)
            else:
                _res, _min, _max = _create_shape(
                    geo_type=GeoJsonGeometryType.LineString,
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                )
                result = [_res]
                _recompute_min_max(mins, maxs, _min, _max)
        elif geo_type == GeoJsonGeometryType.Polygon:
            result, mins, maxs = _create_shape(
                geo_type=GeoJsonGeometryType.MultiLineString,  # Here we only provide 1 line, the external one (outer-ring)
                point_list=point_list,
                indices=indices,
                point_offset=point_offset,
                logger=logger,
            )
            # First and last must be the same
            if len(result) > 0 and result[0] != result[-1]:
                result.append(result[0])
        elif geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None and len(indices) > 0 and isinstance(indices[0], list):
                result = []
                for idx in indices:
                    _res, _min, _max = _create_shape(
                        geo_type=GeoJsonGeometryType.MultiPolygon,  # Here we only provide 1 line, the external one (outer-ring)
                        point_list=point_list,
                        indices=idx,
                        point_offset=point_offset,
                        logger=logger,
                    )
                    result = result + _res
                    _recompute_min_max(mins, maxs, _min, _max)
            else:
                _res, _min, _max = _create_shape(
                    geo_type=GeoJsonGeometryType.Polygon,  # Here we only provide 1 line, the external one (outer-ring)
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                )
                result = [_res]
                _recompute_min_max(mins, maxs, _min, _max)
    except Exception as e:
        if logger is not None:
            logger.error(e)
        # raise e
    return result, mins, maxs


def _write_geojson_shape(
    out: BytesIO,
    geo_type: GeoJsonGeometryType,
    point_list: List[List[float]],
    indices: Optional[Union[List[List[int]], List[int]]] = None,
    point_offset: int = 0,
    logger: Optional[Any] = None,
    _print_list_boundaries: Optional[bool] = True,
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
    :return shape, minXYZ (as list), maxXYZ (as list)
    """
    mins = []
    maxs = []
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
                    _recompute_min_max_from_points(mins, maxs, point_list[idx + point_offset])
                if _print_list_boundaries:
                    out.write(b"]")
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
                    )
                    if cpt < len(indices) - 1:
                        out.write(b", ")
                    cpt += 1
                    _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(b"]")
            else:
                if _print_list_boundaries:
                    out.write(b"[")
                _min, _max = _write_geojson_shape(
                    out=out,
                    geo_type=GeoJsonGeometryType.LineString,
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                )
                _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
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
            )
        elif geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None and len(indices) > 0 and isinstance(indices[0], list):
                if _print_list_boundaries:
                    out.write(b"[")
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
                    )
                    if cpt < len(indices) - 1:
                        out.write(b", ")
                    cpt += 1
                    _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(b"]")
            else:
                if _print_list_boundaries:
                    out.write(b"[")
                _min, _max = _write_geojson_shape(
                    out=out,
                    geo_type=GeoJsonGeometryType.Polygon,  # Here we only provide 1 line, the external one (outer-ring)
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                )
                _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(b"]")
    except Exception as e:
        if logger is not None:
            logger.error(e)
        # raise e
    return mins, maxs


def to_geojson_feature(
    mesh: AbstractMesh,
    geo_type: GeoJsonGeometryType = GeoJsonGeometryType.Point,
    geo_type_prefix: Optional[str] = "AnyCrs",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger=None,
) -> Dict:
    feature = {}

    if mesh.point_list is not None and len(mesh.point_list) > 0:
        points = mesh.point_list

        #  TODO: remove :
        # points = list(map(
        #     lambda p: list(map(lambda x: round(x/10000., 4), p)),
        #     mesh.point_list
        # ))

        indices = mesh.get_indices()
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

        coordinates, mins, maxs = _create_shape(
            geo_type=geo_type,
            point_list=points,
            indices=indices,
            point_offset=point_offset,
            logger=logger,
        )

        # Pop previously added last :
        if geo_type == GeoJsonGeometryType.Polygon or geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None:
                for indices_i in indices:
                    indices_i.pop()

        if logger is not None:
            logger.debug("\t# to_geojson_feature > shaped")

        bbox_geometry = []  # TODO : see : https://www.rfc-editor.org/rfc/rfc7946#section-5

        bbox_geometry = mins + maxs

        geometry = {
            # "type": f"{geo_type_prefix}{geo_type.name}",
            "type": f"{geo_type.name}",
            "coordinates": coordinates,
            "bbox": bbox_geometry,
        }

        feature = {
            "type": f"{geo_type_prefix}Feature",
            "properties": properties or {},
            "geometry": geometry,
        }

    return feature


def write_geojson_feature(
    out: BytesIO,
    mesh: AbstractMesh,
    geo_type: GeoJsonGeometryType = GeoJsonGeometryType.Point,
    geo_type_prefix: Optional[str] = "AnyCrs",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger=None,
) -> None:
    if mesh.point_list is not None and len(mesh.point_list) > 0:
        points = mesh.point_list

        indices = mesh.get_indices()
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
        out.write(f'"type": "{geo_type_prefix}Feature", '.encode())
        out.write(f'"properties": {json.dumps(properties or {}) }, '.encode())
        out.write(b'"geometry": ')

        out.write(b"{")  # start geometry
        # "type": f"{geo_type_prefix}{geo_type.name}",
        out.write(f'"type": "{geo_type.name}", '.encode())
        out.write('"coordinates": '.encode())
        mins, maxs = _write_geojson_shape(
            out=out,
            geo_type=geo_type,
            point_list=points,
            indices=indices,
            point_offset=point_offset,
            logger=logger,
        )
        bbox_geometry = mins + maxs  # TODO : see : https://www.rfc-editor.org/rfc/rfc7946#section-5

        out.write(f', "bbox": {json.dumps(bbox_geometry)}'.encode())
        out.write(b"}")  # end geometry

        # Pop previously added last :
        if geo_type == GeoJsonGeometryType.Polygon or geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None:
                for indices_i in indices:
                    indices_i.pop()

        if logger is not None:
            logger.debug("\t# to_geojson_feature > shaped")

        out.write(b"}")  # End feature


def mesh_to_geojson_type(obj: AbstractMesh) -> GeoJsonGeometryType:
    if isinstance(obj, SurfaceMesh):
        return GeoJsonGeometryType.MultiPolygon
    elif isinstance(obj, PolylineSetMesh):
        return GeoJsonGeometryType.MultiLineString
    else:
        return GeoJsonGeometryType.MultiPoint


def export_geojson_io(
    out: BytesIO,
    mesh_list: List[AbstractMesh],
    obj_name: Optional[str] = None,
    properties: Optional[List[Optional[Dict]]] = None,
    global_properties: Optional[Dict] = None,
    logger: Optional[Any] = None,
):
    out.write(b"{")
    out.write(b'"type": "FeatureCollection",')
    if obj_name is not None:
        out.write(b'"name": "')
        out.write(obj_name.encode())
        out.write(b'",')

    if global_properties is not None and len(global_properties) > 0:
        for k, v in global_properties.items():
            out.write(b'"')
            out.write(k.encode())
            out.write(b'": ')
            out.write(json.dumps(v).encode())
            out.write(b",")

    out.write(b'"features": [')

    cpt = 0
    point_offset = 0

    for mesh in mesh_list:
        pos = out.tell()
        write_geojson_feature(
            out=out,
            mesh=mesh,
            geo_type=mesh_to_geojson_type(mesh),
            properties=properties[cpt] if properties is not None and len(properties) > cpt else None,
            point_offset=0,  # point_offset,
            logger=logger,
        )
        if out.tell() != pos and cpt < len(mesh_list) - 1:
            out.write(b",")
        cpt += 1
        point_offset = point_offset + len(mesh.point_list)
    out.write(b"]")  # end features
    out.write(b"}")  # end geojson


def export_geojson_dict(
    mesh_list: List[AbstractMesh],
    obj_name: Optional[str] = None,
    properties: Optional[List[Optional[Dict]]] = None,
    logger: Optional[Any] = None,
):
    res = {"type": "FeatureCollection", "features": []}
    cpt = 0
    point_offset = 0
    for mesh in mesh_list:
        feature = to_geojson_feature(
            mesh=mesh,
            geo_type=mesh_to_geojson_type(mesh),
            properties=properties[cpt] if properties is not None and len(properties) > cpt else None,
            point_offset=0,  # point_offset,
            logger=logger,
        )
        if feature is not None:
            res["features"].append(feature)
        cpt += 1
        point_offset = point_offset + len(mesh.point_list)

    return res


def export_off(mesh_list: List[AbstractMesh], out: BytesIO):
    """
    Export an :class:`AbstractMesh` into off format.
    :param mesh_list:
    :param out:
    :return:
    """
    nb_points = sum(list(map(lambda m: len(m.point_list), mesh_list)))
    nb_edges = sum(list(map(lambda m: m.get_nb_edges(), mesh_list)))
    nb_faces = sum(list(map(lambda m: m.get_nb_faces(), mesh_list)))

    out.write(b"OFF\n")
    out.write(_FILE_HEADER)
    out.write(f"{nb_points} {nb_faces} {nb_edges}\n".encode("utf-8"))

    points_io = BytesIO()
    faces_io = BytesIO()

    point_offset = 0
    for m in mesh_list:
        export_off_part(
            off_point_part=points_io,
            off_face_part=faces_io,
            points=m.point_list,
            indices=m.get_indices(),
            point_offset=point_offset,
            colors=[],
        )
        point_offset = point_offset + len(m.point_list)

    out.write(points_io.getbuffer())
    out.write(faces_io.getbuffer())


def export_off_part(
    off_point_part: BytesIO,
    off_face_part: BytesIO,
    points: List[List[float]],
    indices: List[List[int]],
    point_offset: Optional[int] = 0,
    colors: Optional[List[List[int]]] = None,
) -> None:
    for p in points:
        for pi in p:
            off_point_part.write(f"{pi} ".encode("utf-8"))
        off_point_part.write(b"\n")

    cpt = 0
    for face in indices:
        if len(face) > 1:
            off_face_part.write(f"{len(face)} ".encode("utf-8"))
            for pi in face:
                off_face_part.write(f"{pi + point_offset} ".encode("utf-8"))

            if colors is not None and len(colors) > cpt and colors[cpt] is not None and len(colors[cpt]) > 0:
                for col in colors[cpt]:
                    off_face_part.write(f"{col} ".encode("utf-8"))

            off_face_part.write(b"\n")
        cpt += 1


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


def _export_obj_elt(
    off_point_part: BytesIO,
    off_face_part: BytesIO,
    points: List[List[float]],
    indices: List[List[int]],
    point_offset: Optional[int] = 0,
    colors: Optional[List[List[int]]] = None,
    elt_letter: str = "f",
) -> None:
    """

    :param off_point_part:
    :param off_face_part:
    :param points:
    :param indices:
    :param point_offset:
    :param colors: currently not supported
    :param elt_letter: "l" for line and "f" for faces
    :return:
    """
    offset_obj = 1  # OBJ point indices starts at 1 not 0
    for p in points:
        if len(p) > 0:
            off_point_part.write(f"v {' '.join(list(map(lambda xyz: str(xyz), p)))}\n".encode("utf-8"))

    # cpt = 0
    for face in indices:
        if len(face) > 1:
            off_face_part.write(
                f"{elt_letter} {' '.join(list(map(lambda x: str(x + point_offset + offset_obj), face)))}\n".encode(
                    "utf-8"
                )
            )

            # if colors is not None and len(colors) > cpt and colors[cpt] is not None and len(colors[cpt]) > 0:
            #     for col in colors[cpt]:
            #         off_face_part.write(f"{col} ".encode('utf-8'))

            # off_face_part.write(b"\n")


def export_multiple_data(
    epc_path: str,
    uuid_list: List[str],
    output_folder_path: str,
    output_file_path_suffix: str = "",
    file_format: MeshFileFormat = MeshFileFormat.OBJ,
    use_crs_displacement: bool = True,
    logger: Optional[Any] = None,
):
    epc = EpcStreamReader(epc_path)

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
        except:
            if logger is not None:
                logger.error(f"Object with uuid {uuid} not found")
            else:
                logging.error(f"Object with uuid {uuid} not found")
            continue
        file_name = (
            f"{gen_energyml_object_path(energyml_obj)}_"
            f"[{get_object_attribute(energyml_obj, 'citation.title')}]"
            f"{output_file_path_suffix}"
            f".{file_format.value}"
        )
        file_path = f"{output_folder_path}/{file_name}"
        logging.debug(f"Exporting : {file_path}")
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
                    logger=logger,
                    global_properties={"epc_path": epc_path},
                )
        else:
            logging.error(f"Code is not written for format {file_format}")
