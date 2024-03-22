# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import os
import re
import sys

from energyml.eml.v2_3.commonv2 import JaggedArray, AbstractValueArray, AbstractIntegerArray, IntegerConstantArray, \
    StringXmlArray, IntegerXmlArray

from src.energyml.utils.data.helper import read_array, testall, get_array_reader_function
from src.energyml.utils.data.mesh import *
from src.energyml.utils.data.hdf import *
from src.energyml.utils.introspection import is_abstract
from src.energyml.utils.manager import get_sub_classes
from src.energyml.utils.serialization import read_energyml_xml_file, serialize_xml


def test_off():
    print("hello")
    indices = [
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3],
    ]

    print(sum(list(map(lambda x: len(x), indices))))

    points = [
        [0., 0., 0.],
        [1., 0., 0.],
        [0., 1., 0.],
        [1., 1., 0.],
    ]

    indices = [
        [0, 1, 3],
        [0, 3, 2],
    ]

    off_file = export_off(points, indices)

    print(off_file.getvalue())

    tmp_folder = "../../../#data/tmp"
    print(os.listdir(tmp_folder))

    try:
        os.mkdir(tmp_folder)
    except Exception as e:
        print(e)

    with open(f"{tmp_folder}/hdf-test0.off", "wb") as f:
        f.write(off_file.getvalue())


def test_array():

    hdf5filereader = HDF5FileReader()

    hdf5filereader.read_array("../../../#data/Volve_Horizons_and_Faults_Depth_originEQN_Plus.h5", "/RESQML/d9b95bb5-019d-4341-bcf6-df392338187f/points_patch0")
    print(hdf5filereader.get_array_dimension("../../../#data/Volve_Horizons_and_Faults_Depth_originEQN_Plus.h5", "/RESQML/d9b95bb5-019d-4341-bcf6-df392338187f/points_patch0"))
    # print(hdf5filereader.read_array("../../../#data/Volve_Horizons_and_Faults_Depth_originEQN_Plus.h5", "/RESQML/d9b95bb5-019d-4341-bcf6-df392338187f/points_patch0"))


def test_h5_path():
    epc = Epc.read_file(
        "D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc"
    )

    ref_obj = epc.get_object_by_uuid("2bbac140-ff17-4649-ae85-52a9285a4373")[0]
    for refer_path, refer_value in get_hdf_reference_with_path(ref_obj):
        try:
            print(get_hdf5_path_from_external_path(
                        external_path_obj=get_object_attribute(ref_obj, refer_path),
                        path_in_root=refer_path,
                        root_obj=ref_obj,
                        epc=epc,
            ))
            print("CRS:", get_crs_obj(
                        context_obj=get_object_attribute(ref_obj, refer_path),
                        path_in_root=refer_path,
                        root_obj=ref_obj,
                        epc=epc,
            ))
        except Exception as e:
            print(f"Error with path {refer_path} -- {ref_obj}")
            raise e

    print("\n--------------\n")

    epc201 = Epc.read_file(
        "D:/Geosiris/OSDU/manifestTranslation/#Data/VOLVE_STRUCT.epc"
    )

    print(epc201.additional_rels)

    ref_obj = epc201.get_object_by_uuid("2bbac140-ff17-4649-ae85-52a9285a4373")[0]
    for refer_path, refer_value in get_hdf_reference_with_path(ref_obj):
        try:
            print(get_hdf5_path_from_external_path(
                        external_path_obj=refer_value,
                        path_in_root=refer_path,
                        root_obj=ref_obj,
                        epc=epc201,
            ))
            crs = get_crs_obj(
                        context_obj=refer_value,
                        path_in_root=refer_path,
                        root_obj=ref_obj,
                        epc=epc201,
            )
            print("CRS:", get_obj_identifier(crs), " - ", crs)
        except Exception as e:
            print(f"Error with path {refer_path} -- {ref_obj}")
            raise e


def read_h5_datasets():
    epc201 = Epc.read_file(
        "D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/01_ALWYN_DEPTH/V2.2/Alwyn-surface_input.epc"
    )

    psr = epc201.get_object_by_uuid("a320b62b-c327-4eaa-848f-05847da5a94f")

    print(epc201.epc_file_path)

    pt_set_list = read_point_set_representation(
        point_set=psr,
        epc=epc201
    )

    with open("file_point_set.off", "wb") as f:
        export_off(
            mesh_list=pt_set_list,
            out=f,
        )

    with open("file_point_set.obj", "wb") as f:
        export_obj(
            mesh_list=pt_set_list,
            out=f,
        )


def read_h5_polyline():
    epc201 = Epc.read_file(
        "D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/01_ALWYN_DEPTH/V2.2/Alwyn-surface_input.epc"
    )

    poly = epc201.get_object_by_uuid("77bfb696-1bc0-4858-a304-f8faeb37d809")[0]
    poly_set_list = read_polyline_set_representation(
        polyline_set=poly,
        epc=epc201,
    )
    with open("polyline_set.obj", "wb") as f:
        export_obj(
            mesh_list=poly_set_list,
            out=f,
        )


def read_arrays():

    poly = read_energyml_xml_file("../rc/polyline_set_for_array_tests.xml")

    print(testall())
    print(get_array_reader_function("BooleanConstantArray"))

    print("=====] ", r"LinePatch.\d+")
    for array_path, array_value in search_attribute_matching_name_with_path(poly, r"LinePatch.\d+.ClosedPolylines"):
        # print(f"{array_path}\n\t{array_value}")
        try:
            val = read_array(
                energyml_array=array_value,
                root_obj=poly,
                path_in_root=array_path,
                epc=None,
            )
            print(f"{type(array_value)} \n\t{val}")
        except Exception as e:
            print(e)

    print([x for x in get_sub_classes(AbstractValueArray) if not is_abstract(x)])
    print([x for x in get_sub_classes(AbstractIntegerArray) if not is_abstract(x)])

    jagged_array = JaggedArray(
        elements=StringXmlArray(
            count_per_value=0,
            values=["a", "b", "c", "d", "e", "f", "g", "h"],
        ),
        cumulative_length=IntegerXmlArray(
            count_per_value=0,
            values=[3, 7, 8],
        ),
    )

    val = read_array(
        energyml_array=jagged_array,
        root_obj=poly,
        path_in_root="",
        epc=None,
    )
    print(f"{type(jagged_array)} \n\t{val}")


if __name__ == "__main__":
    # test_off()
    # test_array
    # test_h5_path()
    # read_h5_datasets()
    # read_h5_polyline()
    read_arrays()
