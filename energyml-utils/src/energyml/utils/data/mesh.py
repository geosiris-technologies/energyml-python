# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import List, Optional, Any, Callable

from .hdf import HDF5FileReader
from .helper import read_array, read_grid2d_patch, is_z_reversed, EnergymlWorkspace, get_crs_obj, EPCWorkspace
from ..epc import Epc, get_obj_identifier, gen_energyml_object_path
from ..exception import ObjectNotFoundNotError
from ..introspection import search_attribute_matching_name, \
    search_attribute_matching_name_with_path, snake_case, get_object_attribute

_FILE_HEADER: bytes = b"# file exported by energyml-utils python module (Geosiris)\n"

Point = list[float]


class MeshFileFormat(Enum):
    OFF = "off"
    OBJ = "obj"


@dataclass
class AbstractMesh:
    energyml_object: Any = field(
        default=None
    )

    crs_object: Any = field(
        default=None
    )

    point_list: List[Point] = field(
        default_factory=list,
    )

    identifier: str = field(
        default=None,
    )

    def export_off(self, out: BytesIO) -> None:
        pass

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
    array_type_name = re.sub("^[Oo]bj([A-Z])", r"\1", array_type_name)
    array_type_name = re.sub("(Polyline|Point)Set", r"\1", array_type_name)
    return array_type_name


def read_mesh_object(
        energyml_object: Any,
        workspace: Optional[EnergymlWorkspace] = None
) -> List[AbstractMesh]:
    """
    Read and "meshable" object. If :param:`energyml_object` is not supported, an exception will be raised.
    :param energyml_object:
    :param workspace:
    :return:
    """
    if isinstance(energyml_object, list):
        return energyml_object
    array_type_name = _mesh_name_mapping(type(energyml_object).__name__)

    reader_func = get_mesh_reader_function(array_type_name)
    if reader_func is not None:
        return reader_func(
            energyml_object=energyml_object,
            workspace=workspace,
        )
    else:
        print(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise Exception(
            f"Type {array_type_name} is not supported\n\t{energyml_object}: \n\tfunction read_{snake_case(array_type_name)} not found")


def read_point_representation(energyml_object: Any, workspace: EnergymlWorkspace) -> List[PointSetMesh]:
    # pt_geoms = search_attribute_matching_type(point_set, "AbstractGeometry")
    h5_reader = HDF5FileReader()

    meshes = []

    patch_idx = 0
    # resqml 2.0.1
    for points_path_in_obj, points_obj in search_attribute_matching_name_with_path(energyml_object,
                                                                                   "NodePatch.[\d]+.Geometry.Points"):
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
            pass
        if points is not None:
            meshes.append(PointSetMesh(
                identifier=f"NodePatch num {patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=points
            ))

        patch_idx = patch_idx + 1

    # resqml 2.2
    for points_path_in_obj, points_obj in search_attribute_matching_name_with_path(energyml_object,
                                                                                   "NodePatchGeometry.[\d]+.Points"):
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
            pass
        if points is not None:
            meshes.append(PointSetMesh(
                identifier=f"NodePatchGeometry num {patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=points
            ))

        patch_idx = patch_idx + 1

    return meshes


def read_polyline_representation(energyml_object: Any, workspace: EnergymlWorkspace) -> List[PolylineSetMesh]:
    # pt_geoms = search_attribute_matching_type(point_set, "AbstractGeometry")
    h5_reader = HDF5FileReader()

    meshes = []

    patch_idx = 0
    for patch_path_in_obj, patch in (
            search_attribute_matching_name_with_path(energyml_object, "NodePatch")
            + search_attribute_matching_name_with_path(energyml_object, "LinePatch.[\\d]+")
    ):
        points_path, points_obj = search_attribute_matching_name_with_path(patch, "Geometry.Points")[0]
        points = read_array(
            energyml_array=points_obj,
            root_obj=energyml_object,
            path_in_root=patch_path_in_obj + points_path,
            workspace=workspace,
        )

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=points_obj,
                path_in_root=patch_path_in_obj + points_path,
                root_obj=energyml_object,
                workspace=workspace,
            )
        except ObjectNotFoundNotError as e:
            pass

        close_poly = None
        try:
            close_poly_path, close_poly_obj = search_attribute_matching_name_with_path(patch, "ClosedPolylines")[0]
            close_poly = read_array(
                energyml_array=close_poly_obj,
                root_obj=energyml_object,
                path_in_root=patch_path_in_obj + close_poly_path,
                workspace=workspace,
            )
        except IndexError:
            pass

        point_indices = []
        try:
            node_count_per_poly_path_in_obj, node_count_per_poly = \
                search_attribute_matching_name_with_path(patch, "NodeCountPerPolyline")[0]
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

        if len(points) > 0:
            meshes.append(PolylineSetMesh(
                identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
                energyml_object=energyml_object,
                crs_object=crs,
                point_list=points,
                line_indices=point_indices
            ))

        patch_idx = patch_idx + 1

    return meshes


def read_grid2d_representation(energyml_object: Any, workspace: Optional[EnergymlWorkspace] = None, keep_holes=False) -> List[SurfaceMesh]:
    # h5_reader = HDF5FileReader()
    meshes = []

    patch_idx = 0
    for patch_path, patch in search_attribute_matching_name_with_path(energyml_object, "Grid2dPatch"):
        reverse_z_values = False
        try:
            crs = get_crs_obj(
                context_obj=patch,
                path_in_root=patch_path,
                root_obj=energyml_object,
                workspace=workspace,
            )
            reverse_z_values = is_z_reversed(crs)
        except ObjectNotFoundNotError as e:
            pass

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

        # print(f"sa_count {sa_count} fa_count {fa_count}")

        points_no_nan = []

        indice_to_final_indice = {}
        if keep_holes:
            for i in range(len(points)):
                p = points[i]
                if p[2] != p[2]:  # a NaN
                    points[i][2] = 0
                elif reverse_z_values:
                    points[i][2] = - points[i][2]
        else:
            for i in range(len(points)):
                p = points[i]
                if p[2] == p[2]:  # not a NaN
                    if reverse_z_values:
                        points[i][2] = - points[i][2]
                    indice_to_final_indice[i] = len(points_no_nan)
                    points_no_nan.append(p)

        indices = []

        while sa_count * fa_count > len(points):
            sa_count = sa_count - 1
            fa_count = fa_count - 1

        while sa_count * fa_count < len(points):
            sa_count = sa_count + 1
            fa_count = fa_count + 1

        # print(f"sa_count {sa_count} fa_count {fa_count} : {sa_count*fa_count} - {len(points)} ")

        for sa in range(sa_count - 1):
            for fa in range(fa_count - 1):
                line = sa * fa_count
                # if sa+1 == int(sa_count / 2) and fa == int(fa_count / 2):
                #     print(
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
        # print(indices)
        meshes.append(SurfaceMesh(
            identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
            energyml_object=energyml_object,
            crs_object=None,
            point_list=points if keep_holes else points_no_nan,
            faces_indices=indices
        ))
        patch_idx = patch_idx + 1

    return meshes


def read_triangulated_set_representation(energyml_object: Any, workspace: EnergymlWorkspace) -> List[SurfaceMesh]:
    meshes = []

    point_offset = 0
    patch_idx = 0
    for patch_path, patch in search_attribute_matching_name_with_path(energyml_object, "\\.*Patch"):
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
                path_in_root=patch_path + point_path,
                workspace=workspace,
            )

        triangles_list: List[List[int]] = []
        for triangles_path, triangles_obj in search_attribute_matching_name_with_path(patch, "Triangles"):
            triangles_list = triangles_list + read_array(
                energyml_array=triangles_obj,
                root_obj=energyml_object,
                path_in_root=patch_path + triangles_path,
                workspace=workspace,
            )
        triangles_list = list(map(lambda tr: [ti - point_offset for ti in tr], triangles_list))
        meshes.append(SurfaceMesh(
            identifier=f"{get_obj_identifier(energyml_object)}_patch{patch_idx}",
            energyml_object=energyml_object,
            crs_object=crs,
            point_list=point_list,
            faces_indices=triangles_list
        ))

        point_offset = point_offset + len(point_list)

    return meshes


# MESH FILES


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
    out.write(f"{nb_points} {nb_faces} {nb_edges}\n".encode('utf-8'))

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
        colors: Optional[List[List[int]]] = None
) -> None:
    for p in points:
        for pi in p:
            off_point_part.write(f"{pi} ".encode('utf-8'))
        off_point_part.write(b"\n")

    cpt = 0
    for face in indices:
        if len(face) > 1:
            off_face_part.write(f"{len(face)} ".encode('utf-8'))
            for pi in face:
                off_face_part.write(f"{pi + point_offset} ".encode('utf-8'))

            if colors is not None and len(colors) > cpt and colors[cpt] is not None and len(colors[cpt]) > 0:
                for col in colors[cpt]:
                    off_face_part.write(f"{col} ".encode('utf-8'))

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
    out.write(f"# Generated by energyml-utils a Geosiris python module\n\n".encode('utf-8'))

    if obj_name is not None:
        out.write(f"o {obj_name}\n\n".encode('utf-8'))

    point_offset = 0
    for m in mesh_list:
        out.write(f"g {m.identifier}\n\n".encode('utf-8'))
        _export_obj_elt(
            off_point_part=out,
            off_face_part=out,
            points=m.point_list,
            indices=m.get_indices(),
            point_offset=point_offset,
            colors=[],
            elt_letter="l" if isinstance(m, PolylineSetMesh) else "f"
        )
        point_offset = point_offset + len(m.point_list)
        out.write("\n".encode('utf-8'))


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
            off_point_part.write(f"v {' '.join(list(map(lambda xyz: str(xyz), p)))}\n".encode('utf-8'))

    # cpt = 0
    for face in indices:
        if len(face) > 1:
            off_face_part.write(
                f"{elt_letter} {' '.join(list(map(lambda x: str(x + point_offset + offset_obj), face)))}\n".encode(
                    'utf-8'))

            # if colors is not None and len(colors) > cpt and colors[cpt] is not None and len(colors[cpt]) > 0:
            #     for col in colors[cpt]:
            #         off_face_part.write(f"{col} ".encode('utf-8'))

            # off_face_part.write(b"\n")


def export_multiple_data(
        epc_path: str,
        uuid_list: List[str],
        output_folder_path: str,
        output_file_path_suffix: str = "",
        file_format: MeshFileFormat = MeshFileFormat.OBJ
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
        energyml_obj = epc.get_object_by_uuid(uuid)[0]
        file_name = (f"{gen_energyml_object_path(energyml_obj)}_"
                     f"[{get_object_attribute(energyml_obj, 'citation.title')}]"
                     f"{output_file_path_suffix}"
                     f".{file_format.value}")
        file_path = f"{output_folder_path}/{file_name}"
        print(f"Exporting : {file_path}")
        mesh_list = read_mesh_object(
            energyml_object=energyml_obj,
            workspace=EPCWorkspace(epc=epc),
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
        else:
            print(f"Code is not written for format {file_format}")
