# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import List, Optional, Any, Callable, Dict, Union, Tuple


from .helper import (
    read_array,
    read_grid2d_patch,
    EnergymlWorkspace,
    get_crs_obj,
    get_crs_origin_offset,
    is_z_reversed,
)
from ..epc import Epc, get_obj_identifier, gen_energyml_object_path
from ..exception import ObjectNotFoundNotError
from ..introspection import (
    search_attribute_matching_name,
    search_attribute_matching_name_with_path,
    snake_case,
    get_object_attribute,
)

_FILE_HEADER: bytes = b"# file exported by energyml-utils python module (Geosiris)\n"

Point = list[float]


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

    point_list: List[Point] = field(
        default_factory=list,
    )

    identifier: str = field(
        default=None,
    )

    def get_nb_edges(self) -> int:
        return 0

    def get_nb_faces(self) -> int:
        return 0

    def get_indices(self) -> List[List[int]]:
        return []


@dataclass
class PointSetMesh(AbstractMesh):
    pass


@dataclass
class PolylineSetMesh(AbstractMesh):
    line_indices: List[List[int]] = field(
        default_factory=list,
    )

    def get_nb_edges(self) -> int:
        return sum(list(map(lambda li: len(li) - 1, self.line_indices)))

    def get_nb_faces(self) -> int:
        return 0

    def get_indices(self) -> List[List[int]]:
        return self.line_indices


@dataclass
class SurfaceMesh(AbstractMesh):
    faces_indices: List[List[int]] = field(
        default_factory=list,
    )

    def get_nb_edges(self) -> int:
        return sum(list(map(lambda li: len(li) - 1, self.faces_indices)))

    def get_nb_faces(self) -> int:
        return len(self.faces_indices)

    def get_indices(self) -> List[List[int]]:
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
                p[xyz] = p[xyz] + crs_point_offset[xyz]
            if zincreasing_downward and len(p) >= 3:
                p[2] = -p[2]

    return points, crs_point_offset


def get_mesh_reader_function(mesh_type_name: str) -> Optional[Callable]:
    """
    Returns the name of the potential appropriate function to read an object with type is named mesh_type_name
    :param mesh_type_name: the initial type name
    :return:
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name == f"read_{snake_case(mesh_type_name)}":
            return obj
    return None


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
    workspace: Optional[EnergymlWorkspace] = None,
    use_crs_displacement: bool = False,
    sub_indices: List[int] = None,
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

    reader_func = get_mesh_reader_function(array_type_name)
    if reader_func is not None:
        surfaces: List[AbstractMesh] = reader_func(
            energyml_object=energyml_object, workspace=workspace, sub_indices=sub_indices
        )
        if use_crs_displacement:
            for s in surfaces:
                crs_displacement(s.point_list, s.crs_object)
        return surfaces
    else:
        logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise Exception(
            f"Type {array_type_name} is not supported\n\t{energyml_object}: \n\tfunction read_{snake_case(array_type_name)} not found"
        )


def read_point_representation(
    energyml_object: Any, workspace: EnergymlWorkspace, sub_indices: List[int] = None
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
    energyml_object: Any, workspace: EnergymlWorkspace, sub_indices: List[int] = None
) -> List[PolylineSetMesh]:
    # pt_geoms = search_attribute_matching_type(point_set, "AbstractGeometry")

    meshes = []

    patch_idx = 0
    total_size = 0
    for patch_path_in_obj, patch in search_attribute_matching_name_with_path(
        energyml_object, "NodePatch"
    ) + search_attribute_matching_name_with_path(energyml_object, r"LinePatch.[\d]+"):
        points_path, points_obj = search_attribute_matching_name_with_path(patch, "Geometry.Points")[0]
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
                    identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
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
    workspace: Optional[EnergymlWorkspace] = None,
    keep_holes=False,
    sub_indices: List[int] = None,
    offset: int = 0,
):
    points = read_grid2d_patch(
        patch=patch,
        grid2d=energyml_object,
        path_in_root=patch_path,
        workspace=workspace,
    )

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

    # logging.debug(f"sa_count {sa_count} fa_count {fa_count} : {sa_count*fa_count} - {len(points)} ")

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
    energyml_object: Any, workspace: Optional[EnergymlWorkspace] = None, keep_holes=False, sub_indices: List[int] = None
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
        except ObjectNotFoundNotError as e:
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
                identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
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
                identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=points,
                faces_indices=indices,
            )
        )

    return meshes


def read_triangulated_set_representation(
    energyml_object: Any,
    workspace: EnergymlWorkspace,
    sub_indices: List[int] = None,
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
        except ObjectNotFoundNotError as e:
            pass

        point_list: List[Point] = []
        for point_path, point_obj in search_attribute_matching_name_with_path(patch, "Geometry.Points"):
            point_list = point_list + read_array(
                energyml_array=point_obj,
                root_obj=energyml_object,
                path_in_root=patch_path + "." + point_path,
                workspace=workspace,
            )

        triangles_list: List[List[int]] = []
        for (
            triangles_path,
            triangles_obj,
        ) in search_attribute_matching_name_with_path(patch, "Triangles"):
            triangles_list = triangles_list + read_array(
                energyml_array=triangles_obj,
                root_obj=energyml_object,
                path_in_root=patch_path + "." + triangles_path,
                workspace=workspace,
            )
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
                identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=point_list,
                faces_indices=triangles_list,
            )
        )
        point_offset = point_offset + len(point_list)
        patch_idx += 1

    return meshes


def read_sub_representation(
    energyml_object: Any,
    workspace: EnergymlWorkspace,
    sub_indices: List[int] = None,
) -> List[AbstractMesh]:
    supporting_rep_dor = search_attribute_matching_name(
        obj=energyml_object, name_rgx=r"(SupportingRepresentation|RepresentedObject)"
    )[0]
    supporting_rep_identifier = get_obj_identifier(supporting_rep_dor)
    supporting_rep = workspace.get_object_by_identifier(supporting_rep_identifier)

    total_size = 0
    all_indices = []
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

        all_indices = all_indices + array
    meshes = read_mesh_object(
        energyml_object=supporting_rep,
        workspace=workspace,
        sub_indices=all_indices,
    )

    for m in meshes:
        m.identifier = f"sub representation {get_obj_identifier(energyml_object)} of {m.identifier}"

    return meshes


# MESH FILES


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
        out.write(f'"coordinates": '.encode())
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

    Each AbstractMesh from the list :param:`mesh_list` will be placed into its own group.
    :param mesh_list:
    :param out:
    :param obj_name:
    :return:
    """
    out.write("# Generated by energyml-utils a Geosiris python module\n\n".encode("utf-8"))

    if obj_name is not None:
        out.write(f"o {obj_name}\n\n".encode("utf-8"))

    point_offset = 0
    for m in mesh_list:
        out.write(f"g {m.identifier}\n\n".encode("utf-8"))
        _export_obj_elt(
            off_point_part=out,
            off_face_part=out,
            points=m.point_list,
            indices=m.get_indices(),
            point_offset=point_offset,
            colors=[],
            elt_letter="l" if isinstance(m, PolylineSetMesh) else "f",
        )
        point_offset = point_offset + len(m.point_list)
        out.write("\n".encode("utf-8"))


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
    epc = Epc.read_file(epc_path)

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
