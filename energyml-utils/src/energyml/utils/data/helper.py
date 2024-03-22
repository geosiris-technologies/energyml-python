# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import sys
from typing import Any, Optional, Callable

from src.energyml.utils.data.hdf import get_hdf5_path_from_external_path, HDF5FileReader, get_hdf_reference
from src.energyml.utils.epc import Epc
from src.energyml.utils.introspection import snake_case, get_object_attribute_no_verif


def testall():
    return [(name, inspect.isfunction(obj)) for name, obj in inspect.getmembers(sys.modules[__name__])
                     if inspect.isfunction(obj)# and
                     #     name.startswith('read_'))
            ]
    # return any(f(arg) for f in testfunctions)


def get_array_reader_function(array_type_name: str) -> Optional[Callable]:
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name == f"read_{snake_case(array_type_name)}":
            return obj
    return None


def read_array(
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        epc: Optional[Epc] = None
):
    if isinstance(energyml_array, list):
        return energyml_array
    array_type_name = type(energyml_array).__name__

    if array_type_name.endswith("ConstantArray"):
        array_type_name = "ConstantArray"
    elif array_type_name.endswith("ExternalArray"):
        array_type_name = "ExternalArray"
    elif array_type_name.endswith("XmlArray"):
        array_type_name = "XmlArray"

    reader_func = get_array_reader_function(array_type_name)
    if reader_func is not None:
        return reader_func(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
            epc=epc,
        )
    else:
        raise Exception(f"Type {array_type_name} is not supported\n\t{energyml_array}")


#  TODO :
# [
#     "BooleanArrayFromDiscretePropertyArray",
#     "BooleanArrayFromIndexArray",
#     "BooleanConstantArray",
#     "BooleanExternalArray",
#     "BooleanHdf5Array",
#     "BooleanXmlArray",
#     "CompoundExternalArray",
#     "DasTimeArray",
#     "DoubleConstantArray",
#     "DoubleHdf5Array",
#     "DoubleLatticeArray",
#     "ExternalDataArray",
#     "FloatingPointConstantArray",
#     "FloatingPointExternalArray",
#     "FloatingPointLatticeArray",
#     "FloatingPointXmlArray",
#     "IntegerArrayFromBooleanMaskArray",
#     "IntegerConstantArray",
#     "IntegerExternalArray",
#     "IntegerHdf5Array",
#     "IntegerLatticeArray",
#     "IntegerRangeArray",
#     "IntegerXmlArray",
#     "JaggedArray",
#     "ParametricLineArray",
#     "ParametricLineFromRepresentationLatticeArray",
#     "Point2DHdf5Array",
#     "Point3DFromRepresentationLatticeArray",
#     "Point3DHdf5Array",
#     "Point3DLatticeArray",
#     "Point3DParametricArray",
#     "Point3DZvalueArray",
#     "ResqmlJaggedArray",
#     "StringConstantArray",
#     "StringExternalArray",
#     "StringHdf5Array",
#     "StringXmlArray"
# ]


def read_constant_array(
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        epc: Optional[Epc] = None
):
    # print(f"Reading constant array\n\t{energyml_array}")

    value = get_object_attribute_no_verif(energyml_array, "value")
    count = get_object_attribute_no_verif(energyml_array, "count")

    # print(f"\tValue : {[value for i in range(0, count)]}")

    return [value for i in range(0, count)]


def read_xml_array(
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        epc: Optional[Epc] = None
):
    values = get_object_attribute_no_verif(energyml_array, "values")
    # count = get_object_attribute_no_verif(energyml_array, "count_per_value")
    return values


def read_jagged_array(
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        epc: Optional[Epc] = None
):
    elements = read_array(
        energyml_array=get_object_attribute_no_verif(energyml_array, "elements"),
        root_obj=root_obj,
        path_in_root=path_in_root + ".elements",
        epc=epc,
    )
    cumulative_length = read_array(
        energyml_array=read_array(get_object_attribute_no_verif(energyml_array, "cumulative_length")),
        root_obj=root_obj,
        path_in_root=path_in_root + ".cumulative_length",
        epc=epc,
    )

    res = []
    previous = 0
    for cl in cumulative_length:
        res.append(elements[previous: cl])
        previous = cl
    return res


def read_external_array(
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        epc: Optional[Epc] = None
):
    hdf5_path = get_hdf5_path_from_external_path(
                external_path_obj=energyml_array,
                path_in_root=path_in_root,
                root_obj=root_obj,
                epc=epc,
    )
    h5_reader = HDF5FileReader()
    path_in_external = get_hdf_reference(energyml_array)[0]
    return h5_reader.read_array(hdf5_path, path_in_external)


# def read_boolean_constant_array(
#         energyml_array: Any,
#         root_obj: Optional[Any] = None,
#         path_in_root: Optional[str] = None,
#         epc: Optional[Epc] = None
# ):
#     print(energyml_array)
