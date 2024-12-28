# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import logging
import sys
from typing import Any, Optional, Callable, List, Union

from .datasets_io import read_external_dataset_array
from ..constants import flatten_concatenation
from ..epc import get_obj_identifier
from ..exception import ObjectNotFoundNotError
from ..introspection import (
    snake_case,
    get_object_attribute_no_verif,
    search_attribute_matching_name_with_path,
    search_attribute_matching_name,
    search_attribute_in_upper_matching_name,
    get_obj_uuid,
    get_object_attribute,
    get_object_attribute_rgx,
)
from ..workspace import EnergymlWorkspace

_ARRAY_NAMES_ = [
    "BooleanArrayFromDiscretePropertyArray",
    "BooleanArrayFromIndexArray",
    "BooleanConstantArray",
    "BooleanExternalArray",
    "BooleanHdf5Array",
    "BooleanXmlArray",
    "CompoundExternalArray",
    "DasTimeArray",
    "DoubleConstantArray",
    "DoubleHdf5Array",
    "DoubleLatticeArray",
    "ExternalDataArray",
    "FloatingPointConstantArray",
    "FloatingPointExternalArray",
    "FloatingPointLatticeArray",
    "FloatingPointXmlArray",
    "IntegerArrayFromBooleanMaskArray",
    "IntegerConstantArray",
    "IntegerExternalArray",
    "IntegerHdf5Array",
    "IntegerLatticeArray",
    "IntegerRangeArray",
    "IntegerXmlArray",
    "JaggedArray",
    "ParametricLineArray",
    "ParametricLineFromRepresentationLatticeArray",
    "Point2DHdf5Array",
    "Point3DFromRepresentationLatticeArray",
    "Point3DHdf5Array",
    "Point3DLatticeArray",
    "Point3DParametricArray",
    "Point3DZvalueArray",
    "ResqmlJaggedArray",
    "StringConstantArray",
    "StringExternalArray",
    "StringHdf5Array",
    "StringXmlArray",
]


def _point_as_array(point: Any) -> List:
    """
    Transform a point that has "coordinate1", "coordinate2", "coordinate3" as attributes into a list.
    :param point:
    :return:
    """
    return [
        get_object_attribute_no_verif(point, "coordinate1"),
        get_object_attribute_no_verif(point, "coordinate2"),
        get_object_attribute_no_verif(point, "coordinate3"),
    ]


def is_z_reversed(crs: Optional[Any]) -> bool:
    """
    Returns True if the Z axe is reverse (ZIncreasingDownward=='True' or VerticalAxis.Direction=='down')
    :param crs: a CRS object
    :return: By default, False is returned (if 'crs' is None)
    """
    reverse_z_values = False
    if crs is not None:
        # resqml 201
        zincreasing_downward = search_attribute_matching_name(crs, "ZIncreasingDownward")
        if len(zincreasing_downward) > 0:
            reverse_z_values = zincreasing_downward[0]

        # resqml >= 22
        vert_axis = search_attribute_matching_name(crs, "VerticalAxis.Direction")
        if len(vert_axis) > 0:
            vert_axis_str = str(vert_axis[0])
            if "." in vert_axis_str:
                vert_axis_str = vert_axis_str.split(".")[-1]

            reverse_z_values = vert_axis_str.lower() == "down"

    return reverse_z_values


def get_vertical_epsg_code(crs_object: Any):
    vertical_epsg_code = None
    if crs_object is not None:  # LocalDepth3dCRS
        vertical_epsg_code = get_object_attribute_rgx(crs_object, "VerticalCrs.EpsgCode")
        if vertical_epsg_code is None:  # LocalEngineering2DCrs
            vertical_epsg_code = get_object_attribute_rgx(
                crs_object, "OriginProjectedCrs.AbstractProjectedCrs.EpsgCode"
            )
    return vertical_epsg_code


def get_projected_epsg_code(crs_object: Any, workspace: Optional[EnergymlWorkspace] = None):
    if crs_object is not None:  # LocalDepth3dCRS
        projected_epsg_code = get_object_attribute_rgx(crs_object, "ProjectedCrs.EpsgCode")
        if projected_epsg_code is None:  # LocalEngineering2DCrs
            projected_epsg_code = get_object_attribute_rgx(
                crs_object, "OriginProjectedCrs.AbstractProjectedCrs.EpsgCode"
            )

        if projected_epsg_code is None and workspace is not None:
            return get_projected_epsg_code(
                workspace.get_object_by_uuid(get_object_attribute_rgx(crs_object, "LocalEngineering2[dD]Crs.Uuid"))
            )
        return projected_epsg_code
    return None


def get_projected_uom(crs_object: Any, workspace: Optional[EnergymlWorkspace] = None):
    if crs_object is not None:
        projected_epsg_uom = get_object_attribute_rgx(crs_object, "ProjectedUom")
        if projected_epsg_uom is None:
            projected_epsg_uom = get_object_attribute_rgx(crs_object, "HorizontalAxes.ProjectedUom")

        if projected_epsg_uom is None and workspace is not None:
            return get_projected_uom(
                workspace.get_object_by_uuid(get_object_attribute_rgx(crs_object, "LocalEngineering2[dD]Crs.Uuid"))
            )
        return projected_epsg_uom
    return None


def get_crs_origin_offset(crs_obj: Any) -> List[float]:
    """
    Return a list [X,Y,Z] corresponding to the crs Offset [XOffset/OriginProjectedCoordinate1, ... ] depending on the
    crs energyml version.
    :param crs_obj:
    :return:
    """
    tmp_offset_x = get_object_attribute_rgx(crs_obj, "XOffset")
    if tmp_offset_x is None:
        tmp_offset_x = get_object_attribute_rgx(crs_obj, "OriginProjectedCoordinate1")

    tmp_offset_y = get_object_attribute_rgx(crs_obj, "YOffset")
    if tmp_offset_y is None:
        tmp_offset_y = get_object_attribute_rgx(crs_obj, "OriginProjectedCoordinate2")

    tmp_offset_z = get_object_attribute_rgx(crs_obj, "ZOffset")
    if tmp_offset_z is None:
        tmp_offset_z = get_object_attribute_rgx(crs_obj, "OriginProjectedCoordinate3")

    crs_point_offset = [0, 0, 0]
    try:
        crs_point_offset = [
            float(tmp_offset_x) if tmp_offset_x is not None else 0,
            float(tmp_offset_y) if tmp_offset_y is not None else 0,
            float(tmp_offset_z) if tmp_offset_z is not None else 0,
        ]
    except Exception as e:
        logging.info(f"ERR reading crs offset {e}")

    return crs_point_offset


def prod_n_tab(val: Union[float, int, str], tab: List[Union[float, int, str]]):
    """
    Multiply every value of the list 'tab' by the constant 'val'
    :param val:
    :param tab:
    :return:
    """
    return list(map(lambda x: x * val, tab))


def sum_lists(l1: List, l2: List):
    """
    Sums 2 lists values.

    Example:
        [1,1,1] and [2,2,3,6] gives : [3,3,4,6]

    :param l1:
    :param l2:
    :return:
    """
    return [l1[i] + l2[i] for i in range(min(len(l1), len(l2)))] + max(l1, l2, key=len)[min(len(l1), len(l2)) :]


def get_crs_obj(
    context_obj: Any,
    path_in_root: Optional[str] = None,
    root_obj: Optional[Any] = None,
    workspace: Optional[EnergymlWorkspace] = None,
) -> Optional[Any]:
    """
    Search for the CRS object related to :param:`context_obj` into the :param:`workspace`
    :param context_obj:
    :param path_in_root:
    :param root_obj:
    :param workspace:
    :return:
    """
    if workspace is None:
        logging.error("@get_crs_obj no Epc file given")
    else:
        crs_list = search_attribute_matching_name(context_obj, r"\.*Crs", search_in_sub_obj=True, deep_search=False)
        if crs_list is not None and len(crs_list) > 0:
            # logging.debug(crs_list[0])
            crs = workspace.get_object_by_identifier(get_obj_identifier(crs_list[0]))
            if crs is None:
                crs = workspace.get_object_by_uuid(get_obj_uuid(crs_list[0]))
            if crs is None:
                logging.error(f"CRS {crs_list[0]} not found (or not read correctly)")
                raise ObjectNotFoundNotError(get_obj_identifier(crs_list[0]))
            if crs is not None:
                return crs

        if context_obj != root_obj:
            upper_path = path_in_root[: path_in_root.rindex(".")]
            if len(upper_path) > 0:
                return get_crs_obj(
                    context_obj=get_object_attribute(root_obj, upper_path),
                    path_in_root=upper_path,
                    root_obj=root_obj,
                    workspace=workspace,
                )

    return None


#     ___
#    /   |  ______________ ___  _______
#   / /| | / ___/ ___/ __ `/ / / / ___/
#  / ___ |/ /  / /  / /_/ / /_/ (__  )
# /_/  |_/_/  /_/   \__,_/\__, /____/
#                        /____/


def _array_name_mapping(array_type_name: str) -> str:
    """
    Transform the type name to match existing reader function
    :param array_type_name:
    :return:
    """
    array_type_name = array_type_name.replace("3D", "3d").replace("2D", "2d")
    if array_type_name.endswith("ConstantArray"):
        return "ConstantArray"
    elif "External" in array_type_name or "Hdf5" in array_type_name:
        return "ExternalArray"
    elif array_type_name.endswith("XmlArray"):
        return "XmlArray"
    elif "Jagged" in array_type_name:
        return "JaggedArray"
    elif "Lattice" in array_type_name:
        if "Integer" in array_type_name or "Double" in array_type_name:
            return "int_double_lattice_array"
    return array_type_name


def get_supported_array() -> List[str]:
    """
    Return a list of the supported arrays for the use of :py:func:`energyml.utils.data.helper.read_array` function.
    :return:
    """
    return [x for x in _ARRAY_NAMES_ if get_array_reader_function(_array_name_mapping(x)) is not None]


def get_not_supported_array():
    """
    Return a list of the NOT supported arrays for the use of :py:func:`energyml.utils.data.helper.read_array` function.
    :return:
    """
    return [x for x in _ARRAY_NAMES_ if get_array_reader_function(_array_name_mapping(x)) is None]


def read_external_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List[Any]:
    """
    Read an external array (BooleanExternalArray, BooleanHdf5Array, DoubleHdf5Array, IntegerHdf5Array, StringExternalArray ...)
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :return:
    """
    array = None
    if workspace is not None:
        array = workspace.read_external_array(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
        )
    else:
        array = read_external_dataset_array(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
        )

    if sub_indices is not None and len(sub_indices) > 0:
        res = []
        for idx in sub_indices:
            res.append(array[idx])
        array = res

    return array


def get_array_reader_function(array_type_name: str) -> Optional[Callable]:
    """
    Returns the name of the potential appropriate function to read an object with type is named :param array_type_name
    :param array_type_name: the initial type name
    :return:
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name == f"read_{snake_case(array_type_name)}":
            return obj
    return None


def read_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List[Any]:
    """
    Read an array and return a list. The array is read depending on its type. see. :py:func:`energyml.utils.data.helper.get_supported_array`
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices: for SubRepresentation
    :return:
    """
    if isinstance(energyml_array, list):
        return energyml_array
    array_type_name = _array_name_mapping(type(energyml_array).__name__)

    reader_func = get_array_reader_function(array_type_name)
    if reader_func is not None:
        return reader_func(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
            workspace=workspace,
            sub_indices=sub_indices,
        )
    else:
        logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise Exception(
            f"Type {array_type_name} is not supported\n\t{energyml_array}: \n\tfunction read_{snake_case(array_type_name)} not found"
        )


def read_constant_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List[Any]:
    """
    Read a constant array ( BooleanConstantArray, DoubleConstantArray, FloatingPointConstantArray, IntegerConstantArray ...)
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    # logging.debug(f"Reading constant array\n\t{energyml_array}")

    value = get_object_attribute_no_verif(energyml_array, "value")
    count = (
        len(sub_indices)
        if sub_indices is not None and len(sub_indices) > 0
        else get_object_attribute_no_verif(energyml_array, "count")
    )

    # logging.debug(f"\tValue : {[value for i in range(0, count)]}")

    return [value] * count


def read_xml_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List[Any]:
    """
    Read a xml array ( BooleanXmlArray, FloatingPointXmlArray, IntegerXmlArray, StringXmlArray ...)
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    values = get_object_attribute_no_verif(energyml_array, "values")
    # count = get_object_attribute_no_verif(energyml_array, "count_per_value")

    if sub_indices is not None and len(sub_indices) > 0:
        res = []
        for idx in sub_indices:
            res.append(values[idx])
        values = res
    return values


def read_jagged_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List[Any]:
    """
    Read a jagged array
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    elements = read_array(
        energyml_array=get_object_attribute_no_verif(energyml_array, "elements"),
        root_obj=root_obj,
        path_in_root=path_in_root + ".elements",
        workspace=workspace,
    )
    cumulative_length = read_array(
        energyml_array=read_array(get_object_attribute_no_verif(energyml_array, "cumulative_length")),
        root_obj=root_obj,
        path_in_root=path_in_root + ".cumulative_length",
        workspace=workspace,
    )

    array = []
    previous = 0
    for cl in cumulative_length:
        array.append(elements[previous:cl])
        previous = cl

    if sub_indices is not None and len(sub_indices) > 0:
        res = []
        for idx in sub_indices:
            res.append(array[idx])
        array = res
    return array


def read_int_double_lattice_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
):
    """
    Read DoubleLatticeArray or IntegerLatticeArray.
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    start_value = get_object_attribute_no_verif(energyml_array, "start_value")
    offset = get_object_attribute_no_verif(energyml_array, "offset")

    result = []

    # if len(offset) == 1:
    #     pass
    # elif len(offset) == 2:
    #     pass
    # else:
    raise Exception(f"{type(energyml_array)} read with an offset of length {len(offset)} is not supported")

    # return result


def read_point3d_zvalue_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
):
    """
    Read a Point3D2ValueArray
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    supporting_geometry = get_object_attribute_no_verif(energyml_array, "supporting_geometry")
    sup_geom_array = read_array(
        energyml_array=supporting_geometry,
        root_obj=root_obj,
        path_in_root=path_in_root + ".SupportingGeometry",
        workspace=workspace,
        sub_indices=sub_indices,
    )

    zvalues = get_object_attribute_no_verif(energyml_array, "zvalues")
    zvalues_array = flatten_concatenation(
        read_array(
            energyml_array=zvalues,
            root_obj=root_obj,
            path_in_root=path_in_root + ".ZValues",
            workspace=workspace,
            sub_indices=sub_indices,
        )
    )

    count = 0

    for i in range(len(sup_geom_array)):
        try:
            sup_geom_array[i][2] = zvalues_array[i]
        except Exception as e:
            if count == 0:
                logging.error(e, f": {i} is out of bound of {len(zvalues_array)}")
                count = count + 1

    return sup_geom_array


def read_point3d_from_representation_lattice_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
):
    """
    Read a Point3DFromRepresentationLatticeArray.

    Note: Only works for Grid2DRepresentation.

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    supporting_rep_identifier = get_obj_identifier(
        get_object_attribute_no_verif(energyml_array, "supporting_representation")
    )
    # logging.debug(f"energyml_array : {energyml_array}\n\t{supporting_rep_identifier}")
    supporting_rep = workspace.get_object_by_identifier(supporting_rep_identifier)

    # TODO chercher un pattern \.*patch\.*.[d]+ pour trouver le numero du patch dans le path_in_root puis lire le patch
    # logging.debug(f"path_in_root {path_in_root}")

    result = []
    if "grid2d" in str(type(supporting_rep)).lower():
        patch_path, patch = search_attribute_matching_name_with_path(supporting_rep, "Grid2dPatch")[0]
        points = read_grid2d_patch(
            patch=patch, grid2d=supporting_rep, path_in_root=patch_path, workspace=workspace, sub_indices=sub_indices
        )
        # TODO: take the points by there indices from the NodeIndicesOnSupportingRepresentation
        result = points

    else:
        raise Exception(f"Not supported type {type(energyml_array)} for object {type(root_obj)}")
    # pour trouver les infos qu'il faut
    return result


def read_grid2d_patch(
    patch: Any,
    grid2d: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List:
    points_path, points_obj = search_attribute_matching_name_with_path(patch, "Geometry.Points")[0]

    return read_array(
        energyml_array=points_obj,
        root_obj=grid2d,
        path_in_root=path_in_root + "." + points_path,
        workspace=workspace,
        sub_indices=sub_indices,
    )


def read_point3d_lattice_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlWorkspace] = None,
    sub_indices: List[int] = None,
) -> List:
    """
    Read a Point3DLatticeArray.

    Note: If a CRS is found and its 'ZIncreasingDownward' is set to true or its

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    result = []
    origin = _point_as_array(get_object_attribute_no_verif(energyml_array, "origin"))
    offset = get_object_attribute_rgx(energyml_array, "offset|dimension")

    if len(offset) == 2:
        slowest = offset[0]
        fastest = offset[1]

        crs_sa_count = search_attribute_in_upper_matching_name(
            obj=energyml_array,
            name_rgx="slowestAxisCount",
            root_obj=root_obj,
            current_path=path_in_root,
        )

        crs_fa_count = search_attribute_in_upper_matching_name(
            obj=energyml_array,
            name_rgx="fastestAxisCount",
            root_obj=root_obj,
            current_path=path_in_root,
        )

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=energyml_array,
                path_in_root=path_in_root,
                root_obj=root_obj,
                workspace=workspace,
            )
        except ObjectNotFoundNotError as e:
            logging.error("No CRS found, not able to check zIncreasingDownward")

        zincreasing_downward = is_z_reversed(crs)

        slowest_vec = _point_as_array(get_object_attribute_rgx(slowest, "offset|direction"))
        slowest_spacing = read_array(get_object_attribute_no_verif(slowest, "spacing"))
        slowest_table = list(map(lambda x: prod_n_tab(x, slowest_vec), slowest_spacing))

        fastest_vec = _point_as_array(get_object_attribute_rgx(fastest, "offset|direction"))
        fastest_spacing = read_array(get_object_attribute_no_verif(fastest, "spacing"))
        fastest_table = list(map(lambda x: prod_n_tab(x, fastest_vec), fastest_spacing))

        slowest_size = len(slowest_table)
        fastest_size = len(fastest_table)

        if len(crs_sa_count) > 0 and len(crs_fa_count) > 0:
            if (crs_sa_count[0] == fastest_size and crs_fa_count[0] == slowest_size) or (
                crs_sa_count[0] == fastest_size - 1 and crs_fa_count[0] == slowest_size - 1
            ):
                logging.debug("reversing order")
                # if offset were given in the wrong order
                tmp_table = slowest_table
                slowest_table = fastest_table
                fastest_table = tmp_table

                tmp_size = slowest_size
                slowest_size = fastest_size
                fastest_size = tmp_size
            else:
                slowest_size = crs_sa_count[0]
                fastest_size = crs_fa_count[0]

        for i in range(slowest_size):
            for j in range(fastest_size):
                previous_value = origin
                # to avoid a sum of the parts of the array at each iteration, I take the previous value in the same line
                # number i and add the fastest_table[j] value

                if j > 0:
                    if i > 0:
                        line_idx = i * fastest_size  # numero de ligne
                        previous_value = result[line_idx + j - 1]
                    else:
                        previous_value = result[j - 1]
                    if zincreasing_downward:
                        result.append(sum_lists(previous_value, slowest_table[i - 1]))
                    else:
                        result.append(sum_lists(previous_value, fastest_table[j - 1]))
                else:
                    if i > 0:
                        prev_line_idx = (i - 1) * fastest_size  # numero de ligne precedent
                        previous_value = result[prev_line_idx]
                        if zincreasing_downward:
                            result.append(sum_lists(previous_value, fastest_table[j - 1]))
                        else:
                            result.append(sum_lists(previous_value, slowest_table[i - 1]))
                    else:
                        result.append(previous_value)
    else:
        raise Exception(f"{type(energyml_array)} read with an offset of length {len(offset)} is not supported")

    if sub_indices is not None and len(sub_indices) > 0:
        res = []
        for idx in sub_indices:
            res.append(result[idx])
        result = res

    return result


# def read_boolean_constant_array(
#         energyml_array: Any,
#         root_obj: Optional[Any] = None,
#         path_in_root: Optional[str] = None,
#         workspace: Optional[EnergymlWorkspace] = None
# ):
#     logging.debug(energyml_array)
