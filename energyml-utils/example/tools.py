# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import argparse
import json
import os
import pathlib
import traceback
from typing import Callable, Optional, List, Dict, Any
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from energyml.utils.epc_utils import get_epc_content_type_path
from energyml.utils.validation import ErrorType, validate_epc

from energyml.utils.constants import EpcExportVersion, get_property_kind_dict_path_as_xml
from energyml.utils.data.datasets_io import CSVFileReader, HDF5FileWriter, ParquetFileWriter, DATFileReader
from energyml.utils.data.mesh import MeshFileFormat, export_multiple_data, export_obj, read_mesh_object
from energyml.utils.epc import Epc, gen_energyml_object_path
from energyml.utils.introspection import (
    get_class_from_simple_name,
    get_enum_values,
    get_non_abstract_classes,
    is_abstract,
    get_module_name_and_type_from_content_or_qualified_type,
    random_value_from_class,
    search_class_in_module_from_partial_name,
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
from energyml.utils.serialization import (
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


def _find_class_from_type_name(type_name: str):
    """
    Search a class from a full python path (e.g. 'energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation')
    or from a qualified type (e.g. 'resqml22.TriangulatedSetRepresentation').
    :param type_name:
    :return: the class or None if not found
    """
    try:
        return get_class_from_simple_name(type_name[type_name.rindex(".") + 1 :], [type_name[: type_name.rindex(".")]])
    except (NameError, ValueError):
        try:
            return get_class_from_qualified_type(type_name)
        except ValueError:
            return None


def _print_close_type_names(type_name: str):
    """Print the types that look like @type_name, to help the user to fix its input."""
    print(f"Class not found for '{type_name}', please check the type name.")
    try:
        module_name, object_type = get_module_name_and_type_from_content_or_qualified_type(type_name)
    except ValueError:
        return
    print("Possible types are :")
    for cn in search_class_in_module_from_partial_name(module_name, object_type):
        print(f" - {cn.__name__}")


def _serialize_object(obj, file_format: str) -> str:
    if file_format.lower() == "xml":
        return serialize_xml(obj)
    else:
        return serialize_json(obj, JSON_VERSION.OSDU_OFFICIAL)


def _file_name_prefix(obj) -> str:
    """
    File name prefix for a generated object : its qualified type (e.g. 'resqml22.TriangulatedSetRepresentation'),
    or its class name if the qualified type cannot be computed.
    :param obj:
    :return: str
    """
    try:
        return get_qualified_type_from_class(obj) or type(obj).__name__
    except Exception:
        return type(obj).__name__


def _is_excluded(cls, exclude: Optional[List[str]]) -> bool:
    """
    Test if the class @cls must be excluded : it is the case if one of the @exclude values is contained (case
    insensitive) in one of the following values :
        - the module of the class (e.g. 'energyml.witsml.v2_1.witsmlv2'),
        - the class name (e.g. 'Trajectory'),
        - the full path 'module.ClassName',
        - the qualified type of the class (e.g. 'witsml21.Trajectory').

    E.g. '-e witsml' excludes every witsml class, '-e trajectory' excludes every class named '*Trajectory*'.
    :param cls:
    :param exclude:
    :return: bool
    """
    if not exclude:
        return False

    module_name = getattr(cls, "__module__", "") or ""
    class_name = getattr(cls, "__name__", "") or ""
    searched_in = [module_name, class_name, f"{module_name}.{class_name}"]
    try:
        searched_in.append(get_qualified_type_from_class(cls) or "")
    except Exception:
        pass
    searched_in = [value.lower() for value in searched_in if len(value) > 0]

    return any(excluded.lower() in value for excluded in exclude for value in searched_in)


def _generate_random_objects(
    obj_class,
    callback: Optional[Callable[[Any], None]] = None,
    exclude: Optional[List[str]] = None,
) -> List[Any]:
    """
    Generate a random object for @obj_class, or, if @obj_class is abstract, one random object per non abstract
    sub class of @obj_class.
    :param obj_class:
    :param callback: if not None, it is called with each object right after its generation (e.g. to write it on the
                     disk without waiting for the end of the whole generation). In that case, the objects are not
                     kept in memory and an empty list is returned.
    :param exclude: list of values : every class matching one of them (see @_is_excluded) is not generated
    :return: a list of generated objects, or an empty list if a @callback was given
    """
    if is_abstract(obj_class):
        classes_to_generate = get_non_abstract_classes(obj_class)
        if len(classes_to_generate) == 0:
            print(f"No instanciable sub class found for the abstract class '{obj_class.__name__}'.")
            return []

        nb_found = len(classes_to_generate)
        classes_to_generate = [cls for cls in classes_to_generate if not _is_excluded(cls, exclude)]
        nb_excluded = nb_found - len(classes_to_generate)

        excluded_msg = f", {nb_excluded} excluded" if nb_excluded > 0 else ""
        print(
            f"'{obj_class.__name__}' is abstract : generating one object per sub class "
            f"({nb_found} found{excluded_msg})."
        )
    elif _is_excluded(obj_class, exclude):
        print(f"'{obj_class.__name__}' is excluded by the filter.")
        return []
    else:
        classes_to_generate = [obj_class]

    objs = []
    for cls in classes_to_generate:
        # a failure on one class must not stop the generation of the others
        try:
            obj = random_value_from_class(cls)
        except Exception as e:
            print(f"Failed to generate an object for '{cls.__name__}' : {type(e).__name__}: {e}")
            continue

        if callback is not None:
            callback(obj)
        else:
            objs.append(obj)

    return objs


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
        help="Type of the output files (one of : ['json', 'xml']). Default is 'json'",
    )

    args = parser.parse_args()

    obj_class = _find_class_from_type_name(args.type)

    if obj_class is None:
        _print_close_type_names(args.type)
        return

    for obj in _generate_random_objects(obj_class):
        print(_serialize_object(obj, args.file_format))


def generate_multiple_data():
    """
    Same as @generate_data but for several object types at once, sharing a common file format.
    If an output folder is given, one file per object is written in it (as soon as it is generated), else all
    objects are printed on stdout.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        "-t",
        type=str,
        nargs="+",
        default=["energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation"],
        help="Object types (e.g. energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation "
        "energyml.resqml.v2_2.resqmlv2.PolylineSetRepresentation)",
    )

    parser.add_argument(
        "--file-format",
        "-ff",
        type=str,
        default="json",
        help="Type of the output files (one of : ['json', 'xml']). Default is 'json'",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output folder path. If not set, the objects are printed on the standard output",
    )

    parser.add_argument(
        "--exclude",
        "-e",
        type=str,
        nargs="+",
        action="extend",  # to support both '-e witsml prodml' and '-e witsml -e prodml'
        default=[],
        help="Do not generate the classes whose module, class name, 'module.ClassName' or qualified type contains "
        "one of these values (case insensitive). E.g. '-e witsml prodml' skips every witsml and prodml class",
    )

    args = parser.parse_args()

    file_format = args.file_format.lower()
    if file_format not in ["json", "xml"]:
        print(f"Unknown file format '{args.file_format}', please use one of : ['json', 'xml']")
        return

    if args.output is not None:
        pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)

    def export_object(obj):
        """Export an object as soon as it has been generated : one file per object, or the standard output."""
        try:
            content = _serialize_object(obj, file_format)
        except Exception as e:
            print(f"Failed to serialize an object of type '{type(obj).__name__}' : {type(e).__name__}: {e}")
            return

        if args.output is None:
            print(f"# ----- {type(obj).__name__} -----")
            print(content)
        else:
            file_path = os.path.join(args.output, f"{_file_name_prefix(obj)}_{get_obj_uuid(obj)}.{file_format}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Object written in {file_path}")

    for type_name in args.type:
        obj_class = _find_class_from_type_name(type_name)

        if obj_class is None:
            _print_close_type_names(type_name)
            continue

        _generate_random_objects(obj_class, callback=export_object, exclude=args.exclude)


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
        use_crs_displacement=not args.no_crs,
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
    parser.add_argument("--out", "-o", type=str, default=None, help="Output file")

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
    parser.add_argument("--out", "-o", type=str, default=None, help="Output EPC file")

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


def _package_file_or_folder_in_epc(input_path: str) -> Epc:
    objects = []

    if not os.path.exists(input_path):
        print(f"File {input_path} does not exist.")
        return
    elif not os.path.isdir(input_path) and not input_path.lower().endswith((".json", ".xml", ".epc")):
        print(f"File {input_path} is not a valid input file (should be a folder or a json/xml/epc file).")
        return
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            f = os.path.join(input_path, filename)
            if os.path.isfile(f):
                if f.endswith(".json"):
                    with open(f, "rb") as file:
                        f_content = file.read()
                        try:
                            objs = read_energyml_json_bytes(f_content, JSON_VERSION.OSDU_OFFICIAL)
                            objects.extend(objs)
                        except Exception as e:
                            print(f"File {filename} is NOT a valid EnergyML JSON file: {e}")
                elif f.endswith(".xml"):
                    if get_epc_content_type_path() not in f:
                        with open(f, "rb") as file:
                            f_content = file.read()
                            try:
                                obj = read_energyml_xml_bytes(f_content)
                                objects.append(obj)
                            except Exception as e:
                                print(f"File {filename} is NOT a valid EnergyML XML file: {e}")
                elif f.endswith(".epc"):
                    try:
                        epc = Epc.read_file(f)
                        if epc is not None:
                            objects.extend(epc.energyml_objects)
                        else:
                            print(f"File {filename} is NOT a valid EnergyML EPC file: Empty EPC")
                    except Exception as e:
                        print(f"File {filename} is NOT a valid EnergyML EPC file: {e}")
    elif os.path.isfile(input_path):
        f = input_path
        filename = os.path.basename(f)
        if f.endswith(".json"):
            with open(f, "rb") as file:
                f_content = file.read()
                try:
                    objs = read_energyml_json_bytes(f_content, JSON_VERSION.OSDU_OFFICIAL)
                    objects.extend(objs)
                except Exception as e:
                    print(f"File {filename} is NOT a valid EnergyML JSON file: {e}")
        elif f.endswith(".xml"):
            if get_epc_content_type_path() not in f:
                with open(f, "rb") as file:
                    f_content = file.read()
                    try:
                        obj = read_energyml_xml_bytes(f_content)
                        objects.append(obj)
                    except Exception as e:
                        print(f"File {filename} is NOT a valid EnergyML XML file: {e}")
        elif f.endswith(".epc"):
            try:
                epc = Epc.read_file(f)
                if epc is not None:
                    objects.extend(epc.energyml_objects)
                else:
                    print(f"File {filename} is NOT a valid EnergyML EPC file: Empty EPC")
            except Exception as e:
                traceback.print_exc()
                print(f"File {filename} is NOT a valid EnergyML EPC file: {e}")

    epc = Epc()
    epc.energyml_objects = objects
    return epc


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


def load_n_save():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--folder", type=str, help="Input folder")
    parser.add_argument("--file", "-f", type=str, help="Input file (json or xml or epc)")
    parser.add_argument("--output", "-o", type=str, help="Output file epc path")
    parser.add_argument(
        "--pkg-classical", action="store_true", help="Use classical packaging (one file per object) instead of EPC"
    )

    args = parser.parse_args()

    epc = _package_file_or_folder_in_epc(args.file)
    export_version = EpcExportVersion.CLASSIC if args.pkg_classical else EpcExportVersion.EXPANDED

    epc.export_version = export_version

    output_path = args.output or (
        args.file[:-4] + "_bis.epc" if args.file.lower().endswith(".epc") else args.file + "_bis.epc"
    )
    epc.export_file(output_path)


def validate_files():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--folder", type=str, help="Input folder")
    parser.add_argument("--file", "-f", type=str, help="Input file (json or xml or epc)")
    parser.add_argument(
        "--ignore-err-type",
        "-i",
        type=str,
        help=f"Error types to ignore. Possible values {get_enum_values(ErrorType)}",
        nargs="*",
    )

    parser.add_argument(
        "--ignore-prodml-version-errs",
        action="store_false",
        dest="ignore_prodml_version_errs",
        help="Disable ignoring errors related to Prodml version (by default, these errors are ignored)",
    )

    parser.add_argument(
        "--group-by-err-class",
        action="store_true",
        help="Group errors by their class (e.g. all validation errors together, all parsing errors together, etc.)",
    )

    args = parser.parse_args()

    epc = _package_file_or_folder_in_epc(args.file)

    err_json = [
        err.toJson()
        for err in validate_epc(epc)
        if str(err.error_type).lower() not in (et.lower() for et in (args.ignore_err_type or []))
    ]

    err_json_sorted = sorted(
        err_json, key=lambda x: (x["err_class"], x["error_type"], x["object_uuid"] if "object_uuid" in x else "")
    )

    if args.ignore_prodml_version_errs:
        err_json_sorted = [err for err in err_json_sorted if not ("prodml23" in err.get("msg", ""))]

    if args.group_by_err_class:
        err_json_grouped = {}
        for err in err_json_sorted:
            err_class = err.get("err_class", "UnknownErrorClass")
            if err_class not in err_json_grouped:
                err_json_grouped[err_class] = []
            err_json_grouped[err_class].append(err)
        print(json.dumps(err_json_grouped, indent=4))
    else:
        # print(json.dumps(err_json, indent=4))
        print(json.dumps(err_json_sorted, indent=4))


# def export_wavefront():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--epc", "-f", type=str, help="Epc file path")
#     parser.add_argument("--output", "-o", type=str, help="Output folder path")
#     parser.add_argument("--uuid", "-u", type=str, help="The uuids of representations to extract", nargs="+")

#     args = parser.parse_args()

#     epc = Epc.read_file(args.epc)
#     for uuid in args.uuid:
#         obj = epc.get_object_by_uuid(uuid)[0]

#         mesh = read_mesh_object(
#             energyml_object=obj,
#             workspace=epc,
#         )

#         if obj is not None:
#             fname = gen_energyml_object_path(obj)
#             with open(os.path.join(args.output, fname + ".obj"), "w") as f:
#                 export_obj(mesh_list=mesh, out=f)  # Assuming the object can be serialized to XML
