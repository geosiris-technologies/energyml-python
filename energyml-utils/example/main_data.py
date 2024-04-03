# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import os

from energyml.eml.v2_3.commonv2 import JaggedArray, AbstractValueArray, AbstractIntegerArray, StringXmlArray, \
    IntegerXmlArray

from src.energyml.utils.data.hdf import *
from src.energyml.utils.data.helper import read_array, get_array_reader_function, get_supported_array, \
    get_not_supported_array
from src.energyml.utils.data.mesh import *
from src.energyml.utils.epc import gen_energyml_object_path
from src.energyml.utils.introspection import is_abstract
from src.energyml.utils.manager import get_sub_classes
from src.energyml.utils.serialization import read_energyml_xml_file, read_energyml_xml_str
from src.energyml.utils.xml import REGEX_CONTENT_TYPE


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
            # print("CRS:", get_crs_obj(
            #             context_obj=get_object_attribute(ref_obj, refer_path),
            #             path_in_root=refer_path,
            #             root_obj=ref_obj,
            #             epc=epc,
            # ))
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
            # crs = get_crs_obj(
            #             context_obj=refer_value,
            #             path_in_root=refer_path,
            #             root_obj=ref_obj,
            #             epc=epc201,
            # )
            # print("CRS:", get_obj_identifier(crs), " - ", crs)
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


def read_h5_grid2d_bis():
    import energyml.resqml.v2_0_1.resqmlv2
    path = "D:/Geosiris/Github/energyml/energyml-python/energyml-utils/rc/obj_Grid2dRepresentation_7c43bad9-4cad-4ab0-bb50-9afb24a4b883.xml"

    xml_content = ""
    with open(path, "r") as f:
        xml_content = f.read()

    grid = read_energyml_xml_str(xml_content)

    grid_list = read_grid2d_representation(
        grid2d=grid,
        epc=None,
    )
    print("Exporting")
    # with open(f"grid2d_{uuid}.obj", "wb") as f:
    #     export_obj(
    #         mesh_list=grid_list,
    #         out=f,
    #     )
    with open(f"grid2d_7c43bad9-4cad-4ab0-bb50-9afb24a4b883_bis.off", "wb") as f:
        export_off(
            mesh_list=grid_list,
            out=f,
        )


def read_h5_grid2d():
    # uuid = "e2e08ccb-e26e-4414-942c-892c2b94e662"  # with supporting representation
    # # uuid = "7c43bad9-4cad-4ab0-bb50-9afb24a4b883"
    # epc22 = Epc.read_file(
    #     "D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/01_ALWYN_DEPTH/V2.2/Alwyn-surface_input.epc"
    # )

    # uuid = "e1734c86-0599-465c-84f3-7356ba7d1062"  # with supporting representation
    # epc22 = Epc.read_file(
    #     "D:/UniversitePoitiers/git/gitlab-xlim/demos/geosimplification/rc/resqml/2.0.1/ALWYN-RESQML.epc"
    # )

    uuid = "d9d77341-feee-4b26-bf1d-fef3e37be513"  # with supporting representation
    epc22 = Epc.read_file(
        "D:/UniversitePoitiers/git/gitlab-xlim/demos/geosimplification/rc/resqml/2.0.1/"
        "Volve_Horizons_and_Faults_Depth_originEQN_Plus.epc"
    )

    # uuid = "f48ca2a5-679b-4eeb-b10d-36aac432495a"  # with supporting representation
    # epc22 = Epc.read_file(
    #     "D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/03_VOLVE/V2.0.1/ASPEN_TECH_RDDMS_IMPORT/Volve_Demo_Horizons_Depth.epc"
    # )

    grid = epc22.get_object_by_uuid(uuid)[0]
    grid_list = read_mesh_object(
        energyml_object=grid,
        epc=epc22,
        # keep_holes=False
    )
    print("Exporting")
    with open(f"grid2d_{uuid}.obj", "wb") as f:
        export_obj(
            mesh_list=grid_list,
            out=f,
        )
    # with open(f"grid2d_{uuid}.off", "wb") as f:
    #     export_off(
    #         mesh_list=grid_list,
    #         out=f,
    #     )


def read_meshes():
    uuid = "a3f31b20-c93a-4682-8f6c-71be087202a4"  # with supporting representation
    epc22 = Epc.read_file(
        "D:/UniversitePoitiers/git/gitlab-xlim/demos/geosimplification/rc/resqml/2.0.1/"
        "Volve_Horizons_and_Faults_Depth_originEQN_Plus.epc"
    )
    energyml_obj = epc22.get_object_by_uuid(uuid)[0]
    mesh_list = read_mesh_object(
        energyml_object=energyml_obj,
        epc=epc22,
    )
    print("Exporting")
    with open(f"{gen_energyml_object_path(energyml_obj)}.obj", "wb") as f:
        export_obj(
            mesh_list=mesh_list,
            out=f,
        )
    # with open(f"{gen_energyml_object_path(energyml_obj)}.off", "wb") as f:
    #     export_off(
    #         mesh_list=mesh_list,
    #         out=f,
    #     )


def read_arrays():

    poly = read_energyml_xml_file("../rc/polyline_set_for_array_tests.xml")

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
    # test_array()
    # test_h5_path()
    # read_h5_datasets()
    # read_h5_polyline()
    # read_arrays()
    #
    # print("Supported : ", get_supported_array())
    # print("Not supported : ", get_not_supported_array())

    read_h5_grid2d()
    # read_h5_grid2d_bis()
    # print(REGEX_CONTENT_TYPE)

    read_meshes()
