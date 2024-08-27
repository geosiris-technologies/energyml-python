# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import argparse
import json
from tkinter import EXCEPTION
from typing import Optional, List, Dict, Any

from energyml.resqml.v2_2.resqmlv2 import BoundaryFeature

from example.main_data import test_array
from src.energyml.utils.data.datasets_io import CSVFileReader, HDF5FileWriter, ParquetFileWriter, read_dataset
from src.energyml.utils.data.mesh import MeshFileFormat, export_multiple_data
from src.energyml.utils.introspection import get_class_from_simple_name, random_value_from_class, copy_attributes, \
    set_attribute_from_path, get_object_attribute, set_attribute_value, get_class_attribute_type
from src.energyml.utils.serialization import serialize_json, JSON_VERSION, serialize_xml
from utils.constants import path_last_attribute
from utils.introspection import get_object_attribute_or_create


def csv_to_h5(csv_in,
              h5_out,
              dataset_name: Optional[str]=None,
              datasets_prefix: Optional[str] = None,
              ignore: List[str] = None,
              map_col_name_to_csv_col: Dict[str, List[str]] = None,
              **csvparams):
    """
    :param csv_in:
    :param h5_out:
    :param dataset_name: if None, csv headers are used
    :param ignore:
    :param map_col_name_to_csv_col:
    :param csvparams:
    :return:
    """
    reader = CSVFileReader()
    writer = HDF5FileWriter()

    ignore = ignore or []

    if dataset_name is None:
        csv_data = reader.read_array_as_panda_dict(csv_in, **csvparams)

        if map_col_name_to_csv_col is not None:
            for k, col_list in map_col_name_to_csv_col.items():
                data = []
                if len(col_list) > 1:
                    for h in col_list:
                        if h not in ignore:
                            try:
                                data = data + [csv_data[h]]
                            except KeyError:
                                pass
                        ignore.append(h)
                else:
                    h = col_list[0] if isinstance(col_list, list) else col_list
                    data = csv_data[h]
                    ignore.append(h)
                try:
                    writer.write_array(h5_out, list(map(list, zip(*data))), (datasets_prefix or "") + k)
                except ValueError:
                    continue
                except Exception as e:
                    raise e
        headers = csv_data.keys()
        for h in headers:
            if h not in ignore:
                try:
                    writer.write_array(h5_out, csv_data[h], (datasets_prefix or "") + h)
                except ValueError:
                    continue
                # except Exception as e:
                #     raise e


def csv_to_parquet(csv_in,
                   parquet_out,
                   dataset_name: Optional[str]=None,
                   datasets_prefix: Optional[str] = None,
                   ignore: List[str] = None,
                   map_col_name_to_csv_col: Dict[str, List[str]] = None,
                   **csvparams):
    """
    :param csv_in:
    :param parquet_out:
    :param dataset_name: if None, csv headers are used
    :param ignore:
    :param map_col_name_to_csv_col:
    :param csvparams:
    :return:
    """
    reader = CSVFileReader()
    writer = ParquetFileWriter()

    ignore = ignore or []

    if dataset_name is None:
        csv_data = reader.read_array_as_panda_dict(csv_in, **csvparams)
        # print(csv_data)
        datadict = {}
        if map_col_name_to_csv_col is not None:
            for k, col_list in map_col_name_to_csv_col.items():
                data = []
                if len(col_list) > 1:
                    for h in col_list:
                        if h not in ignore:
                            try:
                                data = data + [csv_data[h]]
                            except KeyError:
                                pass
                        ignore.append(h)
                else:
                    h = col_list[0] if isinstance(col_list, list) else col_list
                    data = csv_data[h]
                    ignore.append(h)
                try:
                    datadict[(datasets_prefix or "") + k] = list(map(list, zip(*data)))
                except ValueError:
                    continue
                except Exception as e:
                    raise e

        headers = csv_data.keys()
        for h in headers:
            if h not in ignore:
                try:
                    datadict[(datasets_prefix or "") + h] = csv_data[h]
                except ValueError:
                    continue
                except Exception as e:
                    raise e
        keys = list(datadict.keys())
        writer.write_array(parquet_out, [datadict[k] for k in keys], keys)


def csv_to_dataset():
    sample = {
        "FINAL_DATASET_NAME_A": ["CSV_COL_NAME_0", "CSV_COL_NAME_N"],
        "FINAL_DATASET_NAME_B": ["CSV_COL_NAME_X"]
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", "-f", type=str, help="Csv file path")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--prefix", "-p", type=str, default="", help="Output file path")
    parser.add_argument("--csv-delimiter", "-d", type=str, default=",", help="CSV delimiter")
    parser.add_argument("--mapping", "-m", type=str, help=f'Json file path. The json content should look like this : {json.dumps(sample)}')
    parser.add_argument("--mapping-line", "-ml", type=str, help=f'A json dict that should look like this : {json.dumps(sample)}')
    parser.add_argument("--ignore", "-i", type=str, help="A csv column name to ignore", nargs='+')

    args = parser.parse_args()

    mapping = args.mapping_line or args.mapping
    if mapping is not None:
        mapping = json.loads(mapping)

    output_file_path = args.output
    if output_file_path.lower().endswith(".parquet") or output_file_path.lower().endswith(".pqt"):
        csv_to_parquet(
            csv_in=args.csv,
            parquet_out=output_file_path,
            datasets_prefix=args.prefix,
            ignore=args.ignore,
            map_col_name_to_csv_col=mapping,
            delimiter=args.csv_delimiter
        )
    else:
        csv_to_h5(
            csv_in=args.csv,
            h5_out=output_file_path,
            datasets_prefix=args.prefix,
            ignore=args.ignore,
            map_col_name_to_csv_col=mapping,
            delimiter=args.csv_delimiter
        )


def generate_data():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", "-t", type=str, default="energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation", help="Object type (e.g. energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation)")
    parser.add_argument("--file-format", "-ff", type=str, default="json", help=f"Type of the output files (one of : ['json', 'xml']). Default is 'json'")

    args = parser.parse_args()
    obj = random_value_from_class(get_class_from_simple_name(args.type[args.type.rindex(".")+1:], [args.type[:args.type.rindex(".")]]))
    if args.file_format.lower() == "xml":
        print(serialize_xml(obj))
    else:
        print(serialize_json(obj, JSON_VERSION.OSDU_OFFICIAL))


map = {
    "acl.owners" : "osduintegration.OwnerGroup",
    "acl.viewers" : "osduintegration.ViewerGroup",
    "legal.legaltags" : "osduintegration.LegalTags",
    "createTime": "Citation.Creation",
    "modifyTime": "Citation.LastUpdate",
    "modifyUser": "Citation.Editor",
    "createUser": "Citation.Originator",
    "data.Name": "Citation.Title"
}


def osdu_schema_to_energyml(input: str, target_obj: Any):
    obj_in = json.loads(input)
    for k, k_o in map.items():
        try:
            get_object_attribute_or_create(target_obj, k_o)
            print(target_obj)
            new_value = get_object_attribute(obj_in, k, force_snake_case=False)
            set_attribute_from_path(target_obj, k_o, new_value)
        except Exception as e:
            raise e
    return target_obj



def extract_representation_in_3d_file():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epc", "-f", type=str, help="Epc file path")
    parser.add_argument("--output", "-o", type=str, help="Output folder path")
    parser.add_argument("--no-crs", action="store_false", help="Disable crs displacement")
    parser.add_argument("--file-format", "-ff", type=MeshFileFormat, default=MeshFileFormat.OBJ, help=f"Type of the output files (one of : {[e.value for e in MeshFileFormat]}). Default is 'obj'")
    parser.add_argument("--uuid", "-u", type=str, help="The uuids of representations to extract", nargs='+')

    args = parser.parse_args()

    export_multiple_data(
        epc_path=args.epc,
        uuid_list=args.uuid,
        output_folder_path=args.output,
        file_format=args.file_format,
        use_crs_displacement=args.crs
    )


if __name__ == "__main__":
    # csv_to_h5("D:/Geosiris/Github/energyml/energyml-python/energyml-utils/wip/test_with_header.csv",
    #           "D:/Geosiris/Github/energyml/energyml-python/energyml-utils/wip/test_with_headerbis.h5",
    #           datasets_prefix="RESQML/")
    # csv_to_h5("D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/Export_of_database.csv",
    #           "D:/Geosiris/Github/energyml/energyml-python/energyml-utils/wip/Export_of_database.h5",
    #           datasets_prefix="RESQML/")
    # csv_to_h5("D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/shetland-horizon_Truncated_with_ColumnName.txt",
    #           "D:/Geosiris/Github/energyml/energyml-python/energyml-utils/wip/horizon_Truncated_with_ColumnName.h5",
    #           datasets_prefix="RESQML/e3249f8d-1468-4380-b065-1ed4544bf67a/",
    #           map_col_name_to_csv_col={
    #               "point_patch": ["X", "Y", "Z", "T", "TWT"]
    #           })
    # csv_to_parquet("D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/shetland-horizon_Truncated_with_ColumnName.txt",
    #                "D:/Geosiris/Github/energyml/energyml-python/energyml-utils/wip/horizon_Truncated_with_ColumnName.parquet",
    #                datasets_prefix="RESQML/e3249f8d-1468-4380-b065-1ed4544bf67a/",
    #                map_col_name_to_csv_col={
    #                    "point_patch": ["X", "Y", "Z", "T", "TWT"]
    #                })
    #
    # print(read_dataset("D:/Geosiris/Github/energyml/energyml-python/energyml-utils/wip/horizon_Truncated_with_ColumnName.parquet", None, None))

    data = """{
                "id": "osdu:work-product-component--LocalBoundaryFeature:0c383f06-e429-4941-86a9-dbe739e98f0d:",
                "kind": "osdu:wks:work-product-component--LocalBoundaryFeature:1.0.0",
                "version": 1680038644536750.0,
                "acl": {
                    "owners": [
                        "data.default.owners@osdu.osdu-gcp.go3-nrg.projects.epam.com"
                    ],
                    "viewers": [
                        "data.default.viewers@osdu.osdu-gcp.go3-nrg.projects.epam.com"
                    ]
                },
                "legal": {
                    "legaltags": [
                        "osdu-demo-legaltag"
                    ],
                    "otherRelevantDataCountries": [
                        "FR",
                        "US",
                        "CA"
                    ]
                },
                "createTime": "2018-11-26T14:59:52Z",
                "createUser": "ATsoblefack",
                "modifyTime": "2018-11-26T14:59:52Z",
                "modifyUser": "dalsaab",
                "ancestry": {
                    "parents": []
                },
                "data": {
                    "IsDiscoverable": true,
                    "Datasets": [
                        "osdu:dataset--File.Generic:577b1fbb3d894496afe04ac9349decfe:"
                    ],
                    "Artefacts": [],
                    "Name": "Hugin_Fm_Top",
                    "Source": "Paradigm SKUA-GOCAD 22 Alpha 1 Build:20210830-0200 (id: origin/master|56050|1fb1cf919c2|20210827-1108) for Linux_x64_2.17_gcc91"
                },
                "meta": []
            }"""
    # with open("D:/Geosiris/Git/OSDU/manifestTranslation/DATA/resqml-parser/Volve_Demo_Horizons_Depth_manifest_use.json") as f:
    print(get_class_attribute_type(BoundaryFeature, "osduintegration"))
    print(serialize_json(osdu_schema_to_energyml(data, BoundaryFeature())))


    data_in = {
        "a": {"b": "v_0", "c": "v_1"},
        "uuid": "215f8219-cabd-4e24-9e4f-e371cabc9622",
        "objectVersion": "Resqml 2.0",
        "non_existing": 42,
    }
    data_out = {
        "a": None,
        "Uuid": "8291afd6-ae01-49f5-bc96-267e7b27450d",
        "object_version": "Resqml 2.0",
    }
    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=False,
        ignore_case=True,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] == data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert data_out["non_existing"] == data_in["non_existing"]


