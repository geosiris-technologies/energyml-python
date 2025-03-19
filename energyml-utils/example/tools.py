# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import argparse
import json
import os
import pathlib
from typing import Optional, List, Dict, Any

from src.energyml.utils.constants import get_property_kind_dict_path_as_xml
from src.energyml.utils.data.datasets_io import CSVFileReader, HDF5FileWriter, ParquetFileWriter, DATFileReader
from src.energyml.utils.data.mesh import MeshFileFormat, export_multiple_data
from src.energyml.utils.epc import Epc, gen_energyml_object_path
from src.energyml.utils.introspection import (
    get_class_from_simple_name,
    random_value_from_class,
    set_attribute_from_path,
    get_object_attribute,
    get_qualified_type_from_class,
    get_content_type_from_class,
    get_object_attribute_rgx,
    get_direct_dor_list,
    get_obj_uuid,
    get_class_from_qualified_type,
    get_object_attribute_or_create,
)
from src.energyml.utils.serialization import (
    serialize_json,
    JSON_VERSION,
    serialize_xml,
    read_energyml_json_bytes,
    read_energyml_xml_bytes,
    read_energyml_xml_str,
)


def dat_to_h5(
    csv_in,
    h5_out,
    dataset_name: Optional[str] = None,
    datasets_prefix: Optional[str] = None,
    ignore: List[str] = None,
    map_col_name_to_csv_col: Dict[str, List[str]] = None,
    **csvparams,
):
    """
    :param csv_in:
    :param h5_out:
    :param dataset_name: if None, csv headers are used
    :param ignore:
    :param map_col_name_to_csv_col:
    :param csvparams:
    :return:
    """
    reader = DATFileReader()
    writer = HDF5FileWriter()

    _ignore = list(map(lambda x: x.lower(), ignore or []))

    if dataset_name is None:
        csv_data = reader.read_array(csv_in, **csvparams)

        if map_col_name_to_csv_col is not None:
            for k, col_list in map_col_name_to_csv_col.items():
                col_list = list(map(lambda x: x.lower(), col_list))

                print("csv_data")
                print(csv_data)
                data = []
                if len(col_list) > 1:
                    for h in col_list:
                        if h.lower() not in _ignore:
                            try:
                                data = data + [csv_data[h]]
                            except KeyError:
                                pass
                        _ignore.append(h)
                else:
                    h = col_list[0] if isinstance(col_list, list) else col_list
                    data = csv_data[h]
                    _ignore.append(h)
                try:
                    writer.write_array(h5_out, list(map(list, zip(*data))), (datasets_prefix or "") + k)
                except ValueError:
                    continue
                except Exception as e:
                    raise e
        headers = csv_data.keys()
        for h in headers:
            if h not in _ignore:
                try:
                    writer.write_array(h5_out, csv_data[h], (datasets_prefix or "") + h)
                except ValueError:
                    continue
                # except Exception as e:
                #     raise e


def csv_to_h5(
    csv_in,
    h5_out,
    dataset_name: Optional[str] = None,
    datasets_prefix: Optional[str] = None,
    ignore: List[str] = None,
    map_col_name_to_csv_col: Dict[str, List[str]] = None,
    **csvparams,
):
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
                print(csv_data)
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


def csv_to_parquet(
    csv_in,
    parquet_out,
    dataset_name: Optional[str] = None,
    datasets_prefix: Optional[str] = None,
    ignore: List[str] = None,
    map_col_name_to_csv_col: Dict[str, List[str]] = None,
    **csvparams,
):
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
    sample = {"FINAL_DATASET_NAME_A": ["CSV_COL_NAME_0", "CSV_COL_NAME_N"], "FINAL_DATASET_NAME_B": ["CSV_COL_NAME_X"]}
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", "-f", type=str, help="Csv file path")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--prefix", "-p", type=str, default="", help="Dataset path prefix")
    parser.add_argument("--csv-delimiter", "-d", type=str, default=",", help="CSV delimiter")
    parser.add_argument(
        "--mapping",
        "-m",
        type=str,
        help=f"Json file path. The json content should look like this : {json.dumps(sample)}",
    )
    parser.add_argument(
        "--mapping-line", "-ml", type=str, help=f"A json dict that should look like this : {json.dumps(sample)}"
    )
    parser.add_argument("--ignore", "-i", type=str, help="A csv column name to ignore", nargs="+")

    args = parser.parse_args()

    print(args.csv_delimiter)
    print(args.mapping_line)

    mapping = args.mapping_line or args.mapping
    if mapping is not None:
        mapping = json.loads(mapping)

    print(mapping)

    output_file_path = args.output
    if output_file_path.lower().endswith(".parquet") or output_file_path.lower().endswith(".pqt"):
        csv_to_parquet(
            csv_in=args.csv,
            parquet_out=output_file_path,
            datasets_prefix=args.prefix,
            ignore=args.ignore,
            map_col_name_to_csv_col=mapping,
            delimiter=args.csv_delimiter,
        )
    else:
        csv_to_h5(
            csv_in=args.csv,
            h5_out=output_file_path,
            datasets_prefix=args.prefix,
            ignore=args.ignore,
            map_col_name_to_csv_col=mapping,
            delimiter=args.csv_delimiter,
        )


def generate_data():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        "-t",
        type=str,
        default="energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation",
        help="Object type (e.g. energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation)",
    )

    parser.add_argument(
        "--file-format",
        "-ff",
        type=str,
        default="json",
        help=f"Type of the output files (one of : ['json', 'xml']). Default is 'json'",
    )

    args = parser.parse_args()

    obj_class = None
    try:
        obj_class = get_class_from_simple_name(
            args.type[args.type.rindex(".") + 1 :], [args.type[: args.type.rindex(".")]]
        )
    except NameError:
        obj_class = get_class_from_qualified_type(args.type)

    obj = random_value_from_class(obj_class)
    if args.file_format.lower() == "xml":
        print(serialize_xml(obj))
    else:
        print(serialize_json(obj, JSON_VERSION.OSDU_OFFICIAL))


_sample_osdu_map_ = {
    "acl.owners": "osduintegration.OwnerGroup",
    "acl.viewers": "osduintegration.ViewerGroup",
    "legal.legaltags": "osduintegration.LegalTags",
    "createTime": "Citation.Creation",
    "modifyTime": "Citation.LastUpdate",
    "modifyUser": "Citation.Editor",
    "createUser": "Citation.Originator",
    "data.Name": "Citation.Title",
}


def osdu_schema_to_energyml(input: str, target_obj: Any, attrib_map: Dict):
    obj_in = json.loads(input)
    for k, k_o in attrib_map.items():
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
    parser.add_argument(
        "--file-format",
        "-ff",
        type=MeshFileFormat,
        default=MeshFileFormat.OBJ,
        help=f"Type of the output files (one of : {[e.value for e in MeshFileFormat]}). Default is 'obj'",
    )
    parser.add_argument("--uuid", "-u", type=str, help="The uuids of representations to extract", nargs="+")

    args = parser.parse_args()

    export_multiple_data(
        epc_path=args.epc,
        uuid_list=args.uuid,
        output_folder_path=args.output,
        file_format=args.file_format,
        use_crs_displacement=args.crs,
    )


def prop_kind_to_json():
    from importlib.resources import files

    try:
        import energyml.utils.rc as RC
    except:
        import src.energyml.utils.rc as RC
    with files(RC).joinpath(f"PropertyKindDictionary_v2.3.json").open("w", encoding="utf-8") as f:
        f.write(serialize_json(read_energyml_xml_str(get_property_kind_dict_path_as_xml())))


def xml_to_json():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, help="Input File")
    parser.add_argument("--out", "-o", type=str, default=None, help=f"Output file")

    args = parser.parse_args()

    output_path = args.out or args.file[:-4] + ".json"

    json_content = None
    if args.file.lower().endswith(".xml"):
        with open(args.file, "rb") as f:
            f_content = f.read()
            objs = read_energyml_xml_bytes(f_content)
            json_content = serialize_json(objs, JSON_VERSION.OSDU_OFFICIAL)
    elif args.file.lower().endswith(".epc"):
        epc = Epc.read_file(args.file)
        # print(epc.energyml_objects)
        json_content = (
            "[\n"
            + ",".join(list(map(lambda o: serialize_json(o, JSON_VERSION.OSDU_OFFICIAL), epc.energyml_objects)))
            + "]"
        )

    with open(output_path, "w") as fout:
        # print(json_content)
        if json_content is not None:
            fout.write(json_content)


def json_to_xml():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, help="Input File")
    parser.add_argument("--out", "-o", type=str, default=None, help=f"Output file")

    args = parser.parse_args()

    with open(args.file, "rb") as f:
        f_content = f.read()
        objs = []
        try:
            objs = read_energyml_json_bytes(f_content, JSON_VERSION.OSDU_OFFICIAL)
        except:
            objs = read_energyml_json_bytes(f_content, JSON_VERSION.XSDATA)

        dir = pathlib.Path(args.out or args.file).parent.resolve()
        for obj in objs:
            fname = gen_energyml_object_path(obj)
            xml_content = serialize_xml(obj)
            with open(f"{dir}/{fname}", "w") as fout:
                fout.write(xml_content)


def json_to_epc():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, help="Input File")
    parser.add_argument("--out", "-o", type=str, default=None, help=f"Output EPC file")

    args = parser.parse_args()

    epc = Epc(epc_file_path=args.out)
    with open(args.file, "rb") as f:
        f_content = f.read()
        objs = []
        try:
            objs = read_energyml_json_bytes(f_content, JSON_VERSION.OSDU_OFFICIAL)
        except:
            objs = read_energyml_json_bytes(f_content, JSON_VERSION.XSDATA)

        dir = pathlib.Path(args.out or args.file).parent.resolve()
        for obj in objs:
            epc.energyml_objects.append(obj)

    epc.export_file(args.out)


def describe_as_csv():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", "-f", type=str, help="Input File")
    parser.add_argument(
        "--columnsNames",
        "-c",
        type=str,
        default=["Title", "QualifiedType", "Uuid", "SchemaVersion", "Path", "Dors uuids"],
        nargs="*",
        help=f"Columns titles",
    )
    parser.add_argument(
        "--columnsValues",
        "-v",
        type=str,
        default=["citation.title", "$qualifiedtype", "Uuid|Uid", "schemaVersion", "$Path", "$Dor"],
        nargs="*",
        help=f"Columns values. Use $type/$qualifiedType/$contentType/$path/$dor or simpler, a regex matching an attribute",
    )

    args = parser.parse_args()
    print(f"folder : {args.folder}")
    objects = []
    print("Reading files")
    for filename in os.listdir(args.folder):
        f = os.path.join(args.folder, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if f.endswith(".json"):
                with open(f, "rb") as file:
                    f_content = file.read()
                    objs = []
                    try:
                        objs = read_energyml_json_bytes(f_content, JSON_VERSION.OSDU_OFFICIAL)
                    except:
                        objs = read_energyml_json_bytes(f_content, JSON_VERSION.XSDATA)
                objects = objects + list(map(lambda _o: (_o, f), objs))
            elif f.endswith(".xml"):
                with open(f, "rb") as file:
                    f_content = file.read()
                    obj = read_energyml_xml_bytes(f_content)
                    objects.append((obj, f))
            elif f.endswith(".epc"):
                epc = Epc.read_file(f)
                objects = objects + list(map(lambda _o: (_o, f), epc.energyml_objects))

    out_name = "describe.csv"
    cpt = 0
    while os.path.exists(os.path.join(args.folder, out_name)):
        out_name = f"describe_{cpt}.csv"
        cpt += 1

    print("Parsing objects")

    out_path = os.path.join(args.folder, out_name)
    with open(out_path, "w") as out:
        for c in args.columnsNames:
            out.write(c)
            out.write(";")

        out.write("\n")

        for o, path in objects:
            for c in args.columnsValues:
                if c.startswith("$"):
                    clw = c.lower()
                    if clw == "$type":
                        out.write(type(o))
                    elif clw == "$qualifiedtype":
                        out.write(get_qualified_type_from_class(o))
                    elif clw == "$contenttype":
                        out.write(get_content_type_from_class(o))
                    elif clw == "$path":
                        out.write(path)
                    elif clw == "$dor":
                        out.write(
                            str(list(set(list(map(lambda _o: get_obj_uuid(_o), get_direct_dor_list(o)))))).replace(
                                ";", ", "
                            )
                        )
                else:
                    out.write(get_object_attribute_rgx(o, c))
                out.write(";")
            out.write("\n")

    print("Finished")
