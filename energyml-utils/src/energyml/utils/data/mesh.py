# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import json
import logging
import os
import re
import sys
import traceback
from energyml.utils.epc_file import EpcAccessMode, EpcFile
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import List, Optional, Any, Callable, Dict, Union, Tuple


from energyml.utils.data.helper import (
    apply_crs_transform,
    generate_vertical_well_points,
    get_crs_offsets_and_angle,
    get_datum_information,
    get_wellbore_points,
    hermite_interpolation,
    read_array,
    read_grid2d_patch,
    get_crs_obj,
    read_parametric_geometry,
)
from energyml.utils.data.crs import (
    extract_crs_info,
    apply_from_crs_info,
    is_pyproj_available,
    reproject_to_wgs84,
)
from energyml.utils.epc_utils import gen_energyml_object_path
from energyml.utils.epc_stream import EpcStreamReader
from energyml.utils.exception import NotSupportedError, ObjectNotFoundNotError
from energyml.utils.introspection import (
    get_obj_uri,
    get_object_metadata,
    search_attribute_matching_name,
    search_attribute_matching_name_with_path,
    snake_case,
    get_object_attribute,
    get_object_attribute_rgx,
)
from energyml.utils.storage_interface import EnergymlStorageInterface


# Import export functions from new export module for backward compatibility
from energyml.utils.data.export import export_obj as _export_obj_new
from energyml.utils.data.export import _geojson_crs_members

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
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[AbstractMesh]:
    """
    Read and "meshable" object. If :param:`energyml_object` is not supported, an exception will be raised.
    :param energyml_object:
    :param workspace:
    :param use_crs_displacement: If true :func:`apply_from_crs_info` is used to apply the full CRS
    transform (rotation, offsets, Z-flip, axis-order swap) to the mesh points
    :return:
    """

    if isinstance(energyml_object, list):
        return energyml_object
    array_type_name = _mesh_name_mapping(type(energyml_object).__name__)

    reader_func = get_object_reader_function(array_type_name)
    if reader_func is not None:
        # logging.info(f"using function {reader_func} to read type {array_type_name}")
        surfaces: List[AbstractMesh] = reader_func(
            energyml_object=energyml_object,
            workspace=workspace,
            sub_indices=sub_indices,
            use_crs_displacement=use_crs_displacement,
        )
        _tn = array_type_name.lower()
        if (
            use_crs_displacement
            and "wellbore" not in _tn
            and "triangulated" not in _tn  # per-patch CRS applied inside reader
            and "point" not in _tn  # per-patch CRS applied inside reader
            and "polyline" not in _tn  # per-patch CRS applied inside reader
            and "representationset" not in _tn  # each sub-mesh already had CRS applied by its own reader
            and "subrepresentation" not in _tn  # delegates entirely to inner read_mesh_object call
        ):
            for s in surfaces:
                crs = s.crs_object[0] if isinstance(s.crs_object, list) and s.crs_object else s.crs_object
                if crs is None:
                    continue
                logging.debug(f"Applying CRS transform to surface {s.identifier}")
                pts_arr = np.asarray(s.point_list, dtype=np.float64).reshape(-1, 3)
                apply_from_crs_info(pts_arr, extract_crs_info(crs, workspace), inplace=True)
                s.point_list = pts_arr.tolist()
        return surfaces
    else:
        # logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise NotSupportedError(
            f"Type {array_type_name} is not supported\n\tfunction read_{snake_case(array_type_name)} not found"
        )


def read_ijk_grid_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[Any]:
    raise NotSupportedError("IJKGrid representation reading is not supported yet.")


def read_point_representation(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[PointSetMesh]:
    # pt_geoms = search_attribute_matching_type(point_set, "AbstractGeometry")

    meshes = []

    patch_idx = 0
    total_size = 0

    patches_geom = search_attribute_matching_name_with_path(
        energyml_object, r"NodePatch.[\d]+.Geometry.Points"
    ) + search_attribute_matching_name_with_path(  # resqml 2.0.1
        energyml_object, r"NodePatchGeometry.[\d]+.Points"
    )
    # logging.debug(f"Found {len(patches_geom)} patches for point representation")
    # logging.debug(f"\t=> {patches_geom}")

    for points_path_in_obj, points_obj in patches_geom:
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

        # Apply full CRS transform per patch; crs_object kept on mesh for reference
        # but the outer dispatcher is guarded to skip crs_displacement for this type.
        if use_crs_displacement and crs is not None and points is not None and len(points) > 0:
            pts_arr = np.asarray(points, dtype=np.float64).reshape(-1, 3)
            apply_from_crs_info(pts_arr, extract_crs_info(crs, workspace), inplace=True)
            points = pts_arr.tolist()

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
    use_crs_displacement: bool = True,
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
            (close_poly_path, close_poly_obj,) = search_attribute_matching_name_with_path(
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
            (node_count_per_poly_path_in_obj, node_count_per_poly,) = search_attribute_matching_name_with_path(
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

        # Apply full CRS transform per patch; crs_object kept on mesh for reference
        # but the outer dispatcher is guarded to skip crs_displacement for this type.
        if use_crs_displacement and crs is not None and len(points) > 0:
            pts_arr = np.asarray(points, dtype=np.float64).reshape(-1, 3)
            apply_from_crs_info(pts_arr, extract_crs_info(crs, workspace), inplace=True)
            points = pts_arr.tolist()

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
    use_crs_displacement: bool = True,
    keep_holes: bool = False,
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
        logging.debug("Trying to read Grid2d representation with Resqml 2.0.1 schema (Grid2dPatch)")
        logging.debug(f" > {get_obj_uri(energyml_object)}Found patch at path {patch_path} with object {patch}")
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
        logging.debug(
            "Trying to read Grid2d representation with Resqml 2.2 schema (geometry attribute on the representation)"
        )
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
    use_crs_displacement: bool = True,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[SurfaceMesh]:
    meshes = []

    point_offset = 0
    patch_idx = 0
    total_size = 0

    patches = search_attribute_matching_name_with_path(
        energyml_object,
        "\\w*Patch.\\d+",
        deep_search=False,
        search_in_sub_obj=False,
    )
    # logging.debug(f"Found {len(patches)} patches for triangulated set representation")

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

        # Apply full CRS transform (rotation + offsets + z-flip + axis-swap) per patch.
        # Setting crs_object=None on the resulting mesh prevents the outer
        # read_mesh_object dispatcher from calling crs_displacement() a second time.
        logging.debug(
            f"Applying use_crs_displacement {use_crs_displacement} with crs {crs} on patch {patch_path} with {len(point_list)} points for triangulated set representation {get_obj_uri(energyml_object)}"
        )
        if use_crs_displacement and crs is not None and point_list:
            logging.debug(f"Original points sample: {point_list[0:5]}")
            pts_arr = np.asarray(point_list, dtype=np.float64).reshape(-1, 3)
            crs_info = extract_crs_info(crs, workspace)
            apply_from_crs_info(pts_arr, crs_info, inplace=True)
            logging.debug(f"Transformed points sample: {pts_arr[0:5]}")
            point_list = pts_arr.tolist()

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

        # print(f"Mds {wellbore_frame_mds}")

        meshes = read_wellbore_trajectory_representation(
            energyml_object=trajectory_obj,
            workspace=workspace,
            use_crs_displacement=use_crs_displacement,
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
    use_crs_displacement: bool = True,
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
                obj, workspace, use_crs_displacement, sub_indices, wellbore_frame_mds, step_meter
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
        crs_attr = get_object_attribute(energyml_object, "geometry.LocalCrs")
        if crs_attr is not None:
            crs = workspace.get_object(get_obj_uri(crs_attr))
        else:
            raise ObjectNotFoundNotError("LocalCrs attribute not found in trajectory geometry")
    except Exception:
        logging.debug("Could not get CRS from trajectory geometry")

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
                (
                    head_x,
                    head_y,
                    head_z,
                    z_increasing_downward,
                    projected_epsg_code,
                    vertical_epsg_code,
                    crs,
                ) = get_datum_information(md_datum_obj, workspace)
                # if crs is None:
                #     crs = get_crs_obj(
                #         context_obj=md_datum_obj,
                #         path_in_root=".",
                #         root_obj=energyml_object,
                #         workspace=workspace,
                #     )
    except Exception as e:
        logging.debug(f"Could not get reference point / Datum from trajectory: {e}")

    # ==========
    well_points = None
    logging.debug(
        f"wellbore mds : {wellbore_frame_mds}\n\tCRs : {crs}\n\thead x,y,z : {head_x}, {head_y}, {head_z}\n\tz increasing downward : {z_increasing_downward}"
    )
    try:
        crs_info = extract_crs_info(crs, workspace)
        # Try to read parametric Geometry from the trajectory.
        traj_mds, traj_points, traj_tangents = read_parametric_geometry(
            getattr(energyml_object, "geometry", None), workspace
        )
        well_points = get_wellbore_points(wellbore_frame_mds, traj_mds, traj_points, traj_tangents, step_meter)
        if use_crs_displacement:
            well_points = apply_from_crs_info(
                np.asarray(well_points, dtype=np.float64),
                crs_info,
            )
    except Exception as e:
        if wellbore_frame_mds is not None:
            logging.debug(f"Could not read parametric geometry from trajectory. Well is interpreted as vertical: {e}")
            well_points = generate_vertical_well_points(
                head_x=head_x,
                head_y=head_y,
                head_z=head_z,
                wellbore_mds=wellbore_frame_mds,
                z_increasing_downward=z_increasing_downward,
            )
        else:
            traceback.print_exc()
            raise ValueError(
                "Cannot read wellbore trajectory representation: no parametric geometry and no measured depth information available to generate points"
            )

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
    use_crs_displacement: bool = True,
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
        use_crs_displacement=use_crs_displacement,
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
                # Transpose so that each index corresponds to a category (column), not a row.
                # logging.debug(f"category_lookup_data dict : {category_lookup_data}")

                # Guard against inhomogeneous column lengths (e.g. one column is
                # empty while another is not).  Pad all columns with None up to
                # the maximum column length so that np.array() can build a
                # rectangular (n_columns, max_rows) matrix before transposing.
                col_values = [list(v) if not isinstance(v, list) else v for v in category_lookup_data.values()]
                max_len = max((len(c) for c in col_values), default=0)
                if max_len == 0:
                    # All columns empty — nothing to look up.
                    return prop_arrays if not _return_none_if_no_category_lookup else None

                padded = [c + [None] * (max_len - len(c)) for c in col_values]
                category_lookup_matrice = np.array(padded, dtype=object).T
                # logging.debug(f"category_lookup_matrice : {category_lookup_matrice}")
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
) -> List[Tuple[str, int]]:
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


class _JsonIndent:
    """
    Whitespace emitter for the streaming GeoJSON writers.

    Only the *structure* is indented: the collection, the features, the geometry
    and the containers of the coordinates. The innermost coordinate arrays stay
    on a single line — unrolling every ``[x, y, z]`` over four lines does not make
    a document more readable, it inflates it (measured x2.5 on a real export), and
    it would put the indentation on the only hot path of these writers, the one
    that runs once per point.

    ``_JsonIndent(None)`` is the disabled form: every method returns the exact
    bytes the writers used before, so the single-line output is unchanged.
    """

    __slots__ = ("unit", "_depth", "_cache")

    def __init__(self, indent: Optional[Union[int, str, "_JsonIndent"]] = None):
        if indent is None:
            self.unit: Optional[str] = None
        elif isinstance(indent, int):
            self.unit = " " * max(0, indent)
        else:
            self.unit = str(indent)
        self._depth = 0
        self._cache: Dict[int, bytes] = {}

    @classmethod
    def coerce(cls, indent: Optional[Union[int, str, "_JsonIndent"]]) -> "_JsonIndent":
        """Accept an already built indenter, so it can be threaded through the recursion."""
        return indent if isinstance(indent, cls) else cls(indent)

    @property
    def enabled(self) -> bool:
        return self.unit is not None

    def nl(self) -> bytes:
        """Line break followed by the indentation of the current level (``b""`` when disabled)."""
        if self.unit is None:
            return b""
        cached = self._cache.get(self._depth)
        if cached is None:
            cached = ("\n" + self.unit * self._depth).encode()
            self._cache[self._depth] = cached
        return cached

    def open(self) -> bytes:
        """Enter a nesting level, and return the break that starts its first item."""
        self._depth += 1
        return self.nl()

    def close(self) -> bytes:
        """Leave a nesting level, and return the break that puts its closing bracket in place."""
        self._depth = max(0, self._depth - 1)
        return self.nl()

    def sep(self) -> bytes:
        """Comma between two items or two members, with the break (or space) that follows it."""
        return b"," + (self.nl() if self.unit is not None else b" ")


def _dumps_at_depth(value: Any, ind: _JsonIndent) -> bytes:
    """
    Serialise a small value with :func:`json.dumps`, re-indenting its continuation
    lines so that they line up with the current depth.

    Only used for the metadata members (``properties``, ``name``): they weigh a few
    dozen bytes, so the extra string work is irrelevant — unlike on the coordinates.
    """
    if not ind.enabled:
        return json.dumps(value).encode()
    text = json.dumps(value, indent=ind.unit)
    if "\n" not in text:
        return text.encode()
    return text.replace("\n", ind.nl().decode()).encode()


def _write_geojson_shape(
    out: BytesIO,
    geo_type: GeoJsonGeometryType,
    point_list: List[List[float]],
    indices: Optional[Union[List[List[int]], List[int]]] = None,
    point_offset: int = 0,
    logger: Optional[Any] = None,
    _print_list_boundaries: Optional[bool] = True,
    ind: Optional[Union[int, str, _JsonIndent]] = None,
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
    :param ind: indentation of the *containers* of the coordinates. The list of points of a
                line or a ring is always written on a single line.
    :return shape, minXYZ (as list), maxXYZ (as list)
    """
    mins = []
    maxs = []
    ind = _JsonIndent.coerce(ind)
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
                    out.write(ind.open())
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
                        ind=ind,
                    )
                    if cpt < len(indices) - 1:
                        out.write(ind.sep())
                    cpt += 1
                    _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
            else:
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
                _min, _max = _write_geojson_shape(
                    out=out,
                    geo_type=GeoJsonGeometryType.LineString,
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                    ind=ind,
                )
                _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
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
                ind=ind,
            )
        elif geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None and len(indices) > 0 and isinstance(indices[0], list):
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
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
                        ind=ind,
                    )
                    if cpt < len(indices) - 1:
                        out.write(ind.sep())
                    cpt += 1
                    _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
            else:
                if _print_list_boundaries:
                    out.write(b"[")
                    out.write(ind.open())
                _min, _max = _write_geojson_shape(
                    out=out,
                    geo_type=GeoJsonGeometryType.Polygon,  # Here we only provide 1 line, the external one (outer-ring)
                    point_list=point_list,
                    indices=indices,
                    point_offset=point_offset,
                    logger=logger,
                    ind=ind,
                )
                _recompute_min_max(mins, maxs, _min, _max)
                if _print_list_boundaries:
                    out.write(ind.close())
                    out.write(b"]")
    except Exception as e:
        # never swallow silently: a failure here produces a geometry without coordinates
        (logger or logging).error(
            f"@_write_geojson_shape failed for a {geo_type.name} geometry: {type(e).__name__}: {e}"
        )
        # raise e
    return mins, maxs


def _as_json_ready_list(value: Any) -> Any:
    """
    Convert numpy arrays / numpy scalars into plain python lists and floats.

    The GeoJSON writers below serialize the points with :func:`json.dumps`, which does not
    support numpy types : depending on the representation and on the way its points were read,
    ``AbstractMesh.point_list`` may be a ``list`` *or* an ``ndarray``.  Without this conversion
    the serialization raises ``TypeError: Object of type ndarray is not JSON serializable``.
    """
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [_as_json_ready_list(v) for v in value]
    return value


def to_geojson_feature(
    mesh: AbstractMesh,
    geo_type: GeoJsonGeometryType = GeoJsonGeometryType.Point,
    geo_type_prefix: Optional[str] = "",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger=None,
    feature_id: Optional[str] = None,
) -> Dict:
    """
    Build a GeoJSON Feature as a dict.

    :param geo_type_prefix: prefix of the ``type`` member. Empty (default) for a standard
                            RFC 7946 ``"Feature"``; ``"AnyCrs"`` marks non-WGS84 coordinates.
    :param feature_id: value of the RFC 7946 ``id`` member (the energyml uuid, typically).
    """
    feature = {}

    if mesh.point_list is not None and len(mesh.point_list) > 0:
        # point_list / indices may be numpy arrays : json.dumps only accepts plain python types
        points = _as_json_ready_list(mesh.point_list)

        indices = _as_json_ready_list(mesh.get_indices())
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

        feature = {"type": f"{geo_type_prefix or ''}Feature"}
        if feature_id is not None:
            feature["id"] = feature_id
        feature["properties"] = properties or {}
        feature["geometry"] = geometry

    return feature


def write_geojson_feature(
    out: BytesIO,
    mesh: AbstractMesh,
    geo_type: GeoJsonGeometryType = GeoJsonGeometryType.Point,
    geo_type_prefix: Optional[str] = "",
    properties: Optional[dict] = None,
    point_offset: int = 0,
    logger=None,
    feature_id: Optional[str] = None,
    indent: Optional[Union[int, str, _JsonIndent]] = None,
) -> None:
    """
    Write a single GeoJSON Feature.

    :param geo_type_prefix: prefix of the ``type`` member. Empty (default) for a standard
                            RFC 7946 ``"Feature"``; the historical ``"AnyCrs"`` value marks
                            coordinates that are *not* in WGS84.
    :param feature_id: value of the RFC 7946 ``id`` member (the energyml uuid, typically).
    :param indent: number of spaces (or indentation string) of the pretty-printed form.
                   None (default) keeps everything on a single line. See :class:`_JsonIndent`
                   for what is indented and what deliberately is not.
    """
    ind = _JsonIndent.coerce(indent)
    if mesh.point_list is not None and len(mesh.point_list) > 0:
        # point_list / indices may be numpy arrays : json.dumps only accepts plain python types
        points = _as_json_ready_list(mesh.point_list)

        indices = _as_json_ready_list(mesh.get_indices())
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
        out.write(ind.open())
        out.write(f'"type": "{geo_type_prefix or ""}Feature"'.encode())
        if feature_id is not None:
            out.write(ind.sep())
            out.write(f'"id": {json.dumps(feature_id)}'.encode())
        out.write(ind.sep())
        out.write(b'"properties": ')
        out.write(_dumps_at_depth(properties or {}, ind))
        out.write(ind.sep())
        out.write(b'"geometry": ')

        out.write(b"{")  # start geometry
        out.write(ind.open())
        # "type": f"{geo_type_prefix}{geo_type.name}",
        out.write(f'"type": "{geo_type.name}"'.encode())
        out.write(ind.sep())
        out.write('"coordinates": '.encode())
        coordinates_start = out.tell()
        mins, maxs = _write_geojson_shape(
            out=out,
            geo_type=geo_type,
            point_list=points,
            indices=indices,
            point_offset=point_offset,
            logger=logger,
            ind=ind,
        )
        if out.tell() == coordinates_start:
            # the shape could not be written (see the error logged by _write_geojson_shape) :
            # write an empty coordinate list so that the document stays valid JSON
            (logger or logging).error(
                f"No coordinate written for the {geo_type.name} geometry of '{mesh.identifier}' "
                f"({len(points)} points) — an empty geometry is written instead."
            )
            out.write(b"[]")

        bbox_geometry = mins + maxs  # TODO : see : https://www.rfc-editor.org/rfc/rfc7946#section-5

        out.write(ind.sep())
        # the bbox is a flat list of 4 or 6 numbers: it stays on one line
        out.write(f'"bbox": {json.dumps(bbox_geometry)}'.encode())
        out.write(ind.close())
        out.write(b"}")  # end geometry

        # Pop previously added last :
        if geo_type == GeoJsonGeometryType.Polygon or geo_type == GeoJsonGeometryType.MultiPolygon:
            if indices is not None:
                for indices_i in indices:
                    indices_i.pop()

        if logger is not None:
            logger.debug("\t# to_geojson_feature > shaped")

        out.write(ind.close())
        out.write(b"}")  # End feature


def mesh_to_geojson_type(obj: AbstractMesh) -> GeoJsonGeometryType:
    if isinstance(obj, SurfaceMesh):
        return GeoJsonGeometryType.MultiPolygon
    elif isinstance(obj, PolylineSetMesh):
        return GeoJsonGeometryType.MultiLineString
    else:
        return GeoJsonGeometryType.MultiPoint


def _geojson_mesh_metadata(mesh: AbstractMesh, workspace: Optional[EnergymlStorageInterface] = None) -> Dict:
    """
    Build the properties of a feature from the energyml object carried by *mesh* :
    uuid, qualified type, Citation fields, and EPSG codes when a CRS is available.
    """
    properties: Dict = dict(get_object_metadata(getattr(mesh, "energyml_object", None)))

    crs_obj = getattr(mesh, "crs_object", None)
    if isinstance(crs_obj, list):
        crs_obj = crs_obj[0] if crs_obj else None
    if crs_obj is not None:
        crs_info = extract_crs_info(crs_obj, workspace)
        if crs_info.projected_epsg_code is not None:
            properties["projected_epsg_code"] = crs_info.projected_epsg_code
        if crs_info.vertical_epsg_code is not None:
            properties["vertical_epsg_code"] = crs_info.vertical_epsg_code
    if getattr(mesh, "identifier", None):
        properties["identifier"] = mesh.identifier
    return properties


def _geojson_reproject_mesh(
    mesh: AbstractMesh,
    workspace: Optional[EnergymlStorageInterface] = None,
    use_network: bool = False,
    logger: Optional[Any] = None,
) -> Tuple[AbstractMesh, bool, Optional[int], Optional[int]]:
    """
    Return ``(mesh, is_wgs84, projected_epsg_code, vertical_epsg_code)`` where *mesh* is a shallow
    copy whose ``point_list`` has been reprojected to WGS84, or the original mesh when the
    reprojection is impossible (no EPSG code, pyproj missing, transformation error).
    """
    from dataclasses import replace

    crs_obj = getattr(mesh, "crs_object", None)
    if isinstance(crs_obj, list):
        crs_obj = crs_obj[0] if crs_obj else None
    if crs_obj is None or mesh.point_list is None or len(mesh.point_list) == 0:
        return mesh, False, None, None

    crs_info = extract_crs_info(crs_obj, workspace)
    if crs_info.projected_epsg_code is None:
        (logger or logging).warning(
            "GeoJSON export: no projected EPSG code found — coordinates are left in their source CRS "
            "(non RFC 7946 conformant)."
        )
        return mesh, False, None, crs_info.vertical_epsg_code

    if not is_pyproj_available():
        (logger or logging).warning(
            "GeoJSON export: pyproj is not installed (pip install energyml-utils[crs]) — "
            f"coordinates are left in EPSG:{crs_info.projected_epsg_code} instead of WGS84."
        )
        return mesh, False, crs_info.projected_epsg_code, crs_info.vertical_epsg_code

    try:
        points = np.asarray(mesh.point_list, dtype=np.float64).reshape(-1, 3)
        reprojected = reproject_to_wgs84(points, crs_info, use_network=use_network)
        return (
            replace(mesh, point_list=reprojected.tolist()),
            True,
            crs_info.projected_epsg_code,
            (crs_info.vertical_epsg_code),
        )
    except Exception as e:
        (logger or logging).warning(f"GeoJSON export: reprojection to WGS84 failed ({e}) — keeping source coordinates.")
        return mesh, False, crs_info.projected_epsg_code, crs_info.vertical_epsg_code


def export_geojson_io(
    out: BytesIO,
    mesh_list: List[AbstractMesh],
    obj_name: Optional[str] = None,
    properties: Optional[List[Optional[Dict]]] = None,
    global_properties: Optional[Dict] = None,
    logger: Optional[Any] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    to_wgs84: bool = True,
    include_metadata: bool = True,
    use_network: bool = False,
    indent: Optional[Union[int, str]] = None,
):
    """
    Stream a list of meshes as a GeoJSON FeatureCollection.

    :param out: output stream
    :param mesh_list: meshes to export
    :param obj_name: value of the ``name`` member of the collection
    :param properties: explicit per-mesh properties; when None (and :param:`include_metadata` is
                       True) they are built from the energyml object of each mesh (uuid,
                       qualified type, Citation fields, EPSG codes)
    :param global_properties: extra members written at the collection level
    :param logger:
    :param workspace: used to resolve the CRS objects (needed for the v2.2 compound CRS)
    :param to_wgs84: when True (default), coordinates are reprojected to WGS84 as required by
                     RFC 7946.  When the reprojection is not possible, the source CRS is
                     advertised through the ``crs`` / ``coordRefSys`` members.
    :param include_metadata: add the energyml metadata to the properties of every feature
    :param use_network: allow PROJ to download the geoid grids used by vertical transformations
    :param indent: number of spaces (or indentation string) for a pretty-printed document.
                   None (default) keeps the historical single-line output.

                   The document structure is indented but the coordinates of a line or a ring
                   stay on one line: that is what keeps the file readable without inflating it,
                   and it leaves the per-point write path untouched, so the export costs about
                   the same as the compact one — far less than serialising, re-reading and
                   re-dumping the document with ``json.dumps(indent=...)``.
    """
    # the source index is kept so that `properties` stays aligned on `mesh_list`
    exported: List[Tuple[int, AbstractMesh, Dict]] = []
    crs_states: set = set()

    for mesh_index, mesh in enumerate(mesh_list):
        if mesh.point_list is None or len(mesh.point_list) == 0:
            # write_geojson_feature() would write nothing for it; dropping it here keeps the
            # separator logic below exact (an empty mesh in last position used to leave a
            # trailing comma, which is not valid JSON).
            continue
        feature_properties: Dict = {}
        if include_metadata:
            feature_properties.update(_geojson_mesh_metadata(mesh, workspace))

        is_wgs84 = False
        projected_epsg_code = feature_properties.get("projected_epsg_code")
        vertical_epsg_code = feature_properties.get("vertical_epsg_code")
        if to_wgs84:
            mesh, is_wgs84, projected_epsg_code, vertical_epsg_code = _geojson_reproject_mesh(
                mesh, workspace=workspace, use_network=use_network, logger=logger
            )
        if is_wgs84:
            feature_properties["source_crs"] = f"EPSG:{projected_epsg_code}"
            feature_properties["coordinates_crs"] = "OGC:CRS84"
        crs_states.add((projected_epsg_code, vertical_epsg_code, is_wgs84))
        exported.append((mesh_index, mesh, feature_properties))

    ind = _JsonIndent(indent)

    out.write(b"{")
    out.write(ind.open())
    out.write(b'"type": "FeatureCollection"')
    if obj_name is not None:
        out.write(ind.sep())
        # json.dumps rather than a raw concatenation: a title may contain a quote
        out.write(f'"name": {json.dumps(obj_name)}'.encode())

    # A WGS84 document is implicitly in CRS84 and must not carry a 'crs' member (RFC 7946).
    not_wgs84 = [state for state in crs_states if not state[2] and state[0] is not None]
    if len(not_wgs84) == 1:
        for k, v in _geojson_crs_members(not_wgs84[0][0], not_wgs84[0][1]).items():
            out.write(ind.sep())
            out.write(f'"{k}": '.encode())
            out.write(_dumps_at_depth(v, ind))
    elif len(not_wgs84) > 1:
        (logger or logging).warning(
            f"GeoJSON export: {len(not_wgs84)} different source CRS in the same FeatureCollection — "
            "no collection-level CRS is declared, see the per-feature 'projected_epsg_code' property."
        )

    if global_properties is not None and len(global_properties) > 0:
        for k, v in global_properties.items():
            out.write(ind.sep())
            out.write(f"{json.dumps(k)}: ".encode())
            out.write(_dumps_at_depth(v, ind))

    out.write(ind.sep())
    out.write(b'"features": [')
    out.write(ind.open())

    cpt = 0
    point_offset = 0

    for mesh_index, mesh, feature_properties in exported:
        if cpt > 0:
            out.write(ind.sep())
        explicit = properties[mesh_index] if properties is not None and len(properties) > mesh_index else None
        write_geojson_feature(
            out=out,
            mesh=mesh,
            geo_type=mesh_to_geojson_type(mesh),
            # "AnyCrsFeature" keeps flagging the features whose coordinates are not WGS84
            geo_type_prefix="" if feature_properties.get("coordinates_crs") == "OGC:CRS84" else "AnyCrs",
            properties={**feature_properties, **(explicit or {})},
            feature_id=feature_properties.get("uuid"),
            point_offset=0,  # point_offset,
            logger=logger,
            indent=ind,
        )
        cpt += 1
        point_offset = point_offset + len(mesh.point_list)

    out.write(ind.close())
    out.write(b"]")  # end features
    out.write(ind.close())
    out.write(b"}")  # end geojson


def export_geojson_dict(
    mesh_list: List[AbstractMesh],
    obj_name: Optional[str] = None,
    properties: Optional[List[Optional[Dict]]] = None,
    logger: Optional[Any] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    include_metadata: bool = True,
):
    """
    Same as :func:`export_geojson_io` but returns a dict instead of streaming.

    Note: this variant does **not** reproject to WGS84; use :func:`export_geojson_io` or
    :func:`energyml.utils.data.export.export_geojson` when a standard RFC 7946 output is needed.
    """
    res = {"type": "FeatureCollection", "features": []}
    cpt = 0
    point_offset = 0
    for mesh in mesh_list:
        explicit = properties[cpt] if properties is not None and len(properties) > cpt else None
        feature_properties = _geojson_mesh_metadata(mesh, workspace) if include_metadata else {}
        feature_properties.update(explicit or {})
        feature = to_geojson_feature(
            mesh=mesh,
            geo_type=mesh_to_geojson_type(mesh),
            geo_type_prefix="AnyCrs",  # coordinates are left in their source CRS here
            properties=feature_properties,
            feature_id=feature_properties.get("uuid"),
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
    # epc = EpcStreamReader(epc_path)
    logging.debug(f"Opening epc : {epc_path}")
    epc = EpcFile(epc_file_path=epc_path, mode=EpcAccessMode.MANUAL, compact_on_close=False)
    logging.debug(f"Opened")

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
                    )
            else:
                logging.error(f"Code is not written for format {file_format}")
        except Exception as e:
            (logger or logging).error(f"Failed to export the object {uuid} : {type(e).__name__}: {e}")
