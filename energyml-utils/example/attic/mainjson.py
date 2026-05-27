import json
import os

from src.energyml.utils.introspection import (
    get_obj_identifier,
    search_attribute_matching_type_with_path,
    search_attribute_matching_name_with_path,
)
from src.energyml.utils.serialization import (
    read_energyml_json_str,
    JSON_VERSION,
    read_energyml_xml_bytes,
    serialize_json,
    read_energyml_xml_file,
    read_energyml_json_bytes,
    serialize_xml,
)
from src.energyml.utils.serialization import to_json_dict


def read_json0():
    filePath = "../rc/resqml20.obj_Grid2dRepresentation_7194be4d-169d-420c-98a5-d3ec4671f0cc.json"
    with open(filePath, "r") as f:
        f_content = f.read()
        for o in read_energyml_json_str(f_content, JSON_VERSION.OSDU_OFFICIAL):
            print("> ", o)


# import energyml.resqml.v2_0_1.resqmlv2


def write_json0():
    filePath = "../rc/resqml20.obj_Grid2dRepresentation_7194be4d-169d-420c-98a5-d3ec4671f0cc.json"
    with open(filePath, "r") as f:
        f_content = f.read()
        objs = read_energyml_json_str(f_content, JSON_VERSION.OSDU_OFFICIAL)
        result = json.dumps(
            to_json_dict(objs[0], {get_obj_identifier(o): o for o in objs}),
            indent=4,
        )

        print(json.dumps(json.loads(f_content), sort_keys=True))
        print(json.dumps(json.loads(result), sort_keys=True))

        assert json.dumps(json.loads(f_content), sort_keys=True) == json.dumps(json.loads(result), sort_keys=True)


def translate_xml_to_json(input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        f_content = f.read()
        objs = read_energyml_xml_bytes(f_content)
        json_content = serialize_json(objs, JSON_VERSION.OSDU_OFFICIAL)
        with open(output_path, "w") as fout:
            fout.write(json_content)


def translate_json_to_xml(input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        f_content = f.read()
        objs = read_energyml_json_bytes(f_content, JSON_VERSION.OSDU_OFFICIAL)[0]
        xml_content = serialize_xml(objs)
        with open(output_path, "w") as fout:
            fout.write(xml_content)


def test_translate():
    folder_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/RESQML_XML_SHETLAND/"
    for f in os.listdir(folder_path):
        if f.endswith(".xml"):
            translate_xml_to_json(folder_path + f, folder_path + f[:-4] + ".json")


def test_read_raw_json():
    tr = read_energyml_json_str(
        json.dumps(
            {
                "$type": "resqml22.TriangulatedSetRepresentation",
                "Citation": {
                    "$type": "eml23.Citation",
                    "Creation": "2024-08-08T14:57:28.842Z",
                    "Description": "2D GRID Representation direct from seismic",
                    "Editor": "SHELL",
                    "Format": "Geosiris WebStudio",
                    "LastUpdate": "2024-08-20T08:47:24.164Z",
                    "Originator": "Geosiris user (JFR)",
                    "Title": "Shetland SeismicHorizon",
                },
                "RepresentedObject": {
                    "$type": "eml23.DataObjectReference",
                    "QualifiedType": "resqml22.HorizonInterpretation",
                    "Title": "ShetLand JFR",
                    "Uuid": "8bc7e14e-90b3-4ee2-93d3-13f60e22dde4",
                },
                "SchemaVersion": "2.2",
                "Uuid": "6567dc5c-4bf5-491a-b019-bd067d355587",
            }
        ),
        JSON_VERSION.OSDU_OFFICIAL,
    )[0]
    print(tr)

    grid = read_energyml_json_str(
        json.dumps(
            {
                "$type": "resqml22.Grid2dRepresentation",
                "Citation": {
                    "$type": "eml23.Citation",
                    "Creation": "2024-08-08T14:57:28.842Z",
                    "Description": "2D GRID Representation direct from seismic",
                    "Editor": "SHELL",
                    "Format": "Geosiris WebStudio",
                    "LastUpdate": "2024-08-20T08:47:24.164Z",
                    "Originator": "Geosiris user (JFR)",
                    "Title": "Shetland SeismicHorizon",
                },
                "Existence": "ExistenceKind.ACTUAL",
                "FastestAxisCount": 13,
                "Geometry": {
                    "$type": "resqml22.PointGeometry",
                    "LocalCrs": {
                        "$type": "eml23.DataObjectReference",
                        "QualifiedType": "eml23.LocalEngineeringCompoundCrs",
                        "Title": "Default",
                        "Uuid": "545c6ab8-c941-4d4e-bd13-efe7d6dbf125",
                    },
                    "Points": {
                        "$type": "resqml22.Point3dExternalArray",
                        "Coordinates": {
                            "$type": "eml23.ExternalDataArray",
                            "ExternalDataArrayPart": [
                                {
                                    "$type": "eml23.ExternalDataArrayPart",
                                    "Count": [65],
                                    "MimeType": "application/x-hdf5",
                                    "PathInExternalFile": "/RESQML/6567dc5c-4bf5-491a-b019-bd067d355587/points_patch0",
                                    "StartIndex": [0],
                                    "URI": "Volve_Demo_Fault_Horizon_TIME.h5",
                                }
                            ],
                        },
                    },
                },
                "RepresentedObject": {
                    "$type": "eml23.DataObjectReference",
                    "QualifiedType": "resqml22.HorizonInterpretation",
                    "Title": "ShetLand JFR",
                    "Uuid": "8bc7e14e-90b3-4ee2-93d3-13f60e22dde4",
                },
                "SchemaVersion": "2.2",
                "SlowestAxisCount": 5,
                "SurfaceRole": "SurfaceRole.PICK",
                "Uuid": "6567dc5c-4bf5-491a-b019-bd067d355587",
            }
        ),
        JSON_VERSION.OSDU_OFFICIAL,
    )[0]
    print(grid)
    print(grid.citation.title)

    print(search_attribute_matching_type_with_path(grid, "ExternalDataArrayPart"))


def test_search_attribute():
    folder = "../rc/"
    files = [
        # "obj_PointSetRepresentation_ab112e76-3f2a-4911-96e4-3e0db629ced3.xml",
        "obj_TriangulatedSetRepresentation_b043a321-f1e4-4b12-bdb8-221a26a1eb89.xml",
        "TriangulatedSetRepresentation_3a9c9577-27db-34e8-8a5a-a1c6e051d4df.xml",
        # "PointSetRepresentation_5ccc6d3c-5870-4381-92fc-ed9c45db7ef3.xml"
    ]
    for fp in files:
        obj = read_energyml_xml_file(folder + fp)
        da_paths = search_attribute_matching_name_with_path(obj, "PathInHdfFile|PathInExternalFile")
        da_paths.reverse()
        print(fp + " > ", da_paths)
        print(fp + " > ", list(filter(lambda x: "points" in x[0], sorted(da_paths, key=lambda x: x[0]))))


if __name__ == "__main__":
    # read_json0()
    # write_json0()
    # print(sys.modules["energyml.resqml.v2_0_1.resqmlv2"].__dict__)
    # for name, obj in inspect.getmembers(sys.modules["energyml.resqml.v2_0_1.resqmlv2"], inspect.isclass):
    #     print(obj)
    # test_read_raw_json()
    # folder_path = "../rc/"
    # f_path = "TriangulatedSetRepresentation_3a9c9577-27db-34e8-8a5a-a1c6e051d4df.xml"
    # translate_xml_to_json(folder_path + f_path, folder_path + f_path[:-4] + '.json')
    # translate_xml_to_json(
    #     "C:/Users/Cryptaro/Downloads/Activity_36eaddb5-1e07-49e0-b11f-2e31518d8ca0.xml",
    #     "C:/Users/Cryptaro/Downloads/Activity_36eaddb5-1e07-49e0-b11f-2e31518d8ca0.json"
    # )
    # translate_xml_to_json(
    #     "C:/Users/Cryptaro/Downloads/Activity_b383a349-f601-47d7-b5d0-9ee1c1430f27.xml",
    #     "C:/Users/Cryptaro/Downloads/Activity_b383a349-f601-47d7-b5d0-9ee1c1430f27.json"
    # )
    translate_xml_to_json(
        "C:/Users/Cryptaro/Downloads/obj_Grid2dRepresentation_7c43bad9-4cad-4ab0-bb50-9afb24a4b883.xml",
        "C:/Users/Cryptaro/Downloads/obj_Grid2dRepresentation_7c43bad9-4cad-4ab0-bb50-9afb24a4b883.json",
    )
    translate_json_to_xml(
        "C:/Users/Cryptaro/Downloads/obj_Grid2dRepresentation_7c43bad9-4cad-4ab0-bb50-9afb24a4b883.json",
        "C:/Users/Cryptaro/Downloads/obj_Grid2dRepresentation_7c43bad9-4cad-4ab0-bb50-9afb24a4b883_reverted.xml",
    )

    # test_search_attribute()
