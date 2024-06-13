# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

from energyml.eml.v2_3.commonv2 import JaggedArray, AbstractValueArray, AbstractIntegerArray, StringXmlArray, \
    IntegerXmlArray
from energyml.resqml.v2_0_1.resqmlv2 import WellboreMarkerFrameRepresentation

from src.energyml.utils.data.hdf import get_hdf_reference_with_path, get_hdf5_path_from_external_path
from src.energyml.utils.data.helper import get_array_reader_function, get_supported_array, get_not_supported_array
from src.energyml.utils.data.mesh import *
from src.energyml.utils.epc import gen_energyml_object_path
from src.energyml.utils.introspection import is_abstract, get_obj_uuid
from src.energyml.utils.manager import get_sub_classes
from src.energyml.utils.serialization import read_energyml_xml_file, read_energyml_xml_str, read_energyml_xml_bytes
from src.energyml.utils.validation import validate_epc
from src.energyml.utils.xml import RGX_CONTENT_TYPE


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

    pt_set_list = read_point_representation(
        energyml_object=psr,
        workspace=EPCWorkspace(epc=epc201)
    )

    with open("../example/result/file_point_set.off", "wb") as f:
        export_off(
            mesh_list=pt_set_list,
            out=f,
        )

    with open("../example/result/file_point_set.obj", "wb") as f:
        export_obj(
            mesh_list=pt_set_list,
            out=f,
        )


def read_h5_polyline():
    epc201 = Epc.read_file(
        "D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/01_ALWYN_DEPTH/V2.2/Alwyn-surface_input.epc"
    )

    poly = epc201.get_object_by_uuid("77bfb696-1bc0-4858-a304-f8faeb37d809")[0]
    poly_set_list = read_polyline_representation(
        energyml_object=poly,
        workspace=EPCWorkspace(epc201),
    )
    with open("../example/result/polyline_set.obj", "wb") as f:
        export_obj(
            mesh_list=poly_set_list,
            out=f,
        )


def read_h5_grid2d_bis():
    path = "../rc/obj_Grid2dRepresentation_7c43bad9-4cad-4ab0-bb50-9afb24a4b883.xml"

    xml_content = ""
    with open(path, "r") as f:
        xml_content = f.read()

    grid = read_energyml_xml_str(xml_content)

    grid_list = read_grid2d_representation(
        energyml_object=grid,
        workspace=None,
    )
    uuid = get_obj_uuid(grid)
    print("Exporting")
    with open(f"result/grid2d_{uuid}.obj", "wb") as f:
        export_obj(
            mesh_list=grid_list,
            out=f,
        )
    with open(f"result/grid2d_{uuid}_bis.off", "wb") as f:
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
        workspace=EPCWorkspace(epc22),
        # keep_holes=False
    )
    print("Exporting")
    with open(f"result/grid2d_{uuid}.obj", "wb") as f:
        export_obj(
            mesh_list=grid_list,
            out=f,
        )
    with open(f"result/grid2d_{uuid}.off", "wb") as f:
        export_off(
            mesh_list=grid_list,
            out=f,
        )


def read_meshes():
    uuid = "a3f31b20-c93a-4682-8f6c-71be087202a4"  # with supporting representation
    epc22 = Epc.read_file(
        "D:/UniversitePoitiers/git/gitlab-xlim/demos/geosimplification/rc/resqml/2.0.1/"
        "Volve_Horizons_and_Faults_Depth_originEQN_Plus.epc"
    )
    energyml_obj = epc22.get_object_by_uuid(uuid)[0]
    mesh_list = read_mesh_object(
        energyml_object=energyml_obj,
        workspace=EPCWorkspace(epc22),
    )
    print("Exporting")
    with open(f"result/{gen_energyml_object_path(energyml_obj)}.obj", "wb") as f:
        export_obj(
            mesh_list=mesh_list,
            out=f,
        )
    with open(f"result/{gen_energyml_object_path(energyml_obj)}.off", "wb") as f:
        export_off(
            mesh_list=mesh_list,
            out=f,
        )


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
                workspace=None,
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
        workspace=None,
    )
    print(f"{type(jagged_array)} \n\t{val}")


def test_export_multiple():
    uuid_list = [
        "a3f31b20-c93a-4682-8f6c-71be087202a4",  # grid2d
        "e6d5e3b4-ca6b-4182-89fa-96f7efee42ca",  # grid2d
        "a3f31b20-c93a-4682-8f6c-71be087202a4",  # TrSet
        "8659a66c-8727-420a-badf-578819698239",  # TrSet
        "4e23ee3e-54a7-427a-83f9-1473de6c56a4",  # polyline
        "38bf3283-9514-43ab-81e3-17080dc5826f",  # polyline

    ]
    export_multiple_data(
        epc_path="D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/03_VOLVE/V2.0.1/EQN_ORIGIN_PLUS_TRIANG_SET/"
        "Volve_Horizons_and_Faults_Depth_originEQN_Plus.epc",
        uuid_list=uuid_list,
        output_folder_path="../example/result/export-energyml-utils",
        # output_folder_path="D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/03_VOLVE/V2.0.1/EQN_ORIGIN_PLUS_TRIANG_SET/export-energyml-utils",
        file_format=MeshFileFormat.OBJ,
    )

    export_multiple_data(
        epc_path="D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/03_VOLVE/V2.0.1/EQN_ORIGIN_PLUS_TRIANG_SET/"
        "Volve_Horizons_and_Faults_Depth_originEQN_Plus.epc",
        uuid_list=uuid_list,
        output_folder_path="../example/result/export-energyml-utils",
        # output_folder_path="D:/Geosiris/Cloud/Resqml_Tools/2023-DATA/03_VOLVE/V2.0.1/EQN_ORIGIN_PLUS_TRIANG_SET/export-energyml-utils",
        file_format=MeshFileFormat.OFF,
    )


def test_export_multiple_testing_package():
    uuid_list = [
        "030a82f6-10a7-4ecf-af03-54749e098624",  # grid2d
        "aa5b90f1-2eab-4fa6-8720-69dd4fd51a4d",  # grid2d
        # "38f64a1c-356f-4d30-a9ce-4cd3b8d6ec40",  # TrSet
        # "d8a03d57-8bf3-4f75-8645-ef2fbfa5d1e3",  # TrSet
        # "154e8f89-0148-4118-b656-14d9bc4a70ad",  # polyline
        # "e7b8ad80-d92d-492c-b325-328dee619762",  # polyline
        # "65c59595-bf48-451e-94aa-120ebdf28d8b",  # polyline
        # "8442a6b7-a97b-431e-abda-f72cf7ef346f",  # pointSet
        # "fbc5466c-94cd-46ab-8b48-2ae2162b372f",  # pointSet
        # "e3219d2a-e482-4714-86d5-c3a5a2fa3727",  # pointSet
    ]
    epc_path = "D:/Geosiris/OSDU/manifestTranslation/commons/data/testingPackageCpp.epc"
    output_folder_path = "../example/result/testingPackageCpp"
    # output_folder_path = "D:/Geosiris/OSDU/manifestTranslation/commons/data/export-energyml-utils/testingPackageCpp"

    export_multiple_data(
        epc_path=epc_path,
        uuid_list=uuid_list,
        output_folder_path=output_folder_path,
        file_format=MeshFileFormat.OBJ,
    )

    export_multiple_data(
        epc_path=epc_path,
        uuid_list=uuid_list,
        output_folder_path=output_folder_path,
        file_format=MeshFileFormat.OFF,
    )


def test_export_closed_poly():
    export_multiple_data(
        epc_path="D:/Geosiris/OSDU/manifestTranslation/#Data/"
        "Volve_Fault_Depth_originEQN_v201_poly_closed.epc",
        uuid_list=[
            "4e23ee3e-54a7-427a-83f9-1473de6c56a4",  # polyline
            "38bf3283-9514-43ab-81e3-17080dc5826f",  # polyline

        ],
        output_folder_path="../example/result/export-energyml-utils",
        # output_folder_path="D:/Geosiris/OSDU/manifestTranslation/#Data/export-energyml-utils",
        output_file_path_suffix="_poly_closed",
        file_format=MeshFileFormat.OBJ,
    )
    export_multiple_data(
        epc_path="D:/Geosiris/OSDU/manifestTranslation/#Data/"
        "Volve_Fault_Depth_originEQN_v201.epc",
        uuid_list=[
            "4e23ee3e-54a7-427a-83f9-1473de6c56a4",  # polyline
            "38bf3283-9514-43ab-81e3-17080dc5826f",  # polyline

        ],
        output_folder_path="../example/result/export-energyml-utils",
        # output_folder_path="D:/Geosiris/OSDU/manifestTranslation/#Data/export-energyml-utils",
        output_file_path_suffix="closed",
        file_format=MeshFileFormat.OBJ,
    )


def test_read_resqml22dev3():
    path = "../rc/BoundaryFeature_resqml22_dev3.xml"

    with open(path, "rb") as f:
        xml_content = f.read()
        print(xml_content)

        print(read_energyml_xml_bytes(xml_content))

    path = "../rc/BoundaryFeature_resqml22_dev3_wrong_schema_version.xml"

    with open(path, "rb") as f:
        xml_content = f.read()
        print(xml_content)

        print(read_energyml_xml_bytes(xml_content))

    epc_path = "D:/Geosiris/Clients/Egis/Documents/Data/4 MNT Trojena/MNT_Trojena_2024-03-18.epc"
    epc = Epc.read_file(epc_path)
    print(len(epc.energyml_objects), "files found")

    print("\n".join(list(map(lambda err: str(err), validate_epc(epc)))))

    uuid_list = ["eadd871e-b752-4985-9268-1e3ced8bf11a"]

    export_multiple_data(
        epc_path=epc_path,
        uuid_list=uuid_list,
        output_folder_path="../example/result/4 MNT Trojena/",
        # output_folder_path="D:/Geosiris/Clients/Egis/Documents/Data/4 MNT Trojena/",
        file_format=MeshFileFormat.OBJ,
    )


def test_read_external_part_with_xsi():
    path = "../rc/obj_EpcExternalPartReference_61fa2fdf-46ab-4c02-ab72-7895cce58e37.xml"

    with open(path, "rb") as f:
        xml_content = f.read()
        # print(xml_content)

        print(read_energyml_xml_bytes(xml_content))

    path = "../rc/obj_WellboreMarkerFrameRepresentation_2f8778ca-6a09-446b-b25d-b725ec759a70.xml"

    with open(path, "rb") as f:
        xml_content = f.read()
#         print(xml_content)

        print(read_energyml_xml_bytes(xml_content))


def read_unreferenced_h5_file():
    epc_path = "D:/Geosiris/#Data/RDDMS/F2F_Demo.epc"
    # epc_path = "D:/Geosiris/Cloud/Resqml_Tools/OSDU/OSDU_RESERVOIR_DDMS/F2F_Demo.epc"
    # epc = Epc.read_file(epc_path)

    uuid_list = ["3f8ee378-f3d2-40ab-9980-abb0853f69c3"]

    export_multiple_data(
        epc_path=epc_path,
        uuid_list=uuid_list,
        output_folder_path="../example/result/notReferencedH5/",
        # output_folder_path="D:/Geosiris/Clients/Egis/Documents/Data/4 MNT Trojena/",
        file_format=MeshFileFormat.OBJ,
    )


if __name__ == "__main__":
    # test_array()
    # test_h5_path()
    # read_h5_datasets()
    # read_h5_polyline()
    # read_arrays()
    #
    # print("Supported : ", get_supported_array())
    # print("Not supported : ", get_not_supported_array())
    #
    # read_h5_grid2d()
    # read_h5_grid2d_bis()
    # print(RGX_CONTENT_TYPE)
    #
    # read_meshes()
    #
    # test_export_multiple()
    # test_export_closed_poly()
    # test_export_multiple_testing_package()
    # test_read_resqml22dev3()
    # WellboreMarkerFrameRepresentation
    # test_read_external_part_with_xsi()
    read_unreferenced_h5_file()
