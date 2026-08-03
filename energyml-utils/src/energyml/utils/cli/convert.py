# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""``xml_to_json``, ``json_to_xml``, ``json_to_epc`` and ``loadNsave`` — format conversions."""

from __future__ import annotations

import argparse
import json
import logging
import pathlib
from typing import Any, Dict, List, Optional

from energyml.utils.cli._common import package_file_or_folder_in_epc, parse_args, read_energyml_json_any_version
from energyml.utils.constants import EpcExportVersion, get_property_kind_dict_path_as_xml
from energyml.utils.epc import Epc, gen_energyml_object_path
from energyml.utils.introspection import (
    get_object_attribute,
    get_object_attribute_or_create,
    set_attribute_from_path,
)
from energyml.utils.serialization import (
    JSON_VERSION,
    read_energyml_xml_bytes,
    read_energyml_xml_str,
    serialize_json,
    serialize_xml,
)

logger = logging.getLogger(__name__)

#: Example mapping from the OSDU schema to the energyml attribute paths, for
#: :func:`osdu_schema_to_energyml`.
SAMPLE_OSDU_MAP = {
    "acl.owners": "osduintegration.OwnerGroup",
    "acl.viewers": "osduintegration.ViewerGroup",
    "legal.legaltags": "osduintegration.LegalTags",
    "createTime": "Citation.Creation",
    "modifyTime": "Citation.LastUpdate",
    "modifyUser": "Citation.Editor",
    "createUser": "Citation.Originator",
    "data.Name": "Citation.Title",
}


def osdu_schema_to_energyml(input: str, target_obj: Any, attrib_map: Dict) -> Any:
    """Copy the attributes of an OSDU JSON payload into *target_obj*, following *attrib_map*."""
    obj_in = json.loads(input)
    for osdu_path, energyml_path in attrib_map.items():
        get_object_attribute_or_create(target_obj, energyml_path)
        new_value = get_object_attribute(obj_in, osdu_path, force_snake_case=False)
        set_attribute_from_path(target_obj, energyml_path, new_value)
    return target_obj


def prop_kind_to_json(argv: Optional[List[str]] = None) -> None:
    """Regenerate the packaged ``PropertyKindDictionary_v2.3.json`` from its XML counterpart."""
    from importlib.resources import files

    import energyml.utils.rc as RC

    parser = argparse.ArgumentParser(
        prog="prop_kind_to_json",
        description="Regenerate the packaged PropertyKindDictionary json from the packaged xml.",
    )
    parse_args(parser, argv)

    with files(RC).joinpath("PropertyKindDictionary_v2.3.json").open("w", encoding="utf-8") as f:
        f.write(serialize_json(read_energyml_xml_str(get_property_kind_dict_path_as_xml())))
    print("PropertyKindDictionary_v2.3.json regenerated")


def xml_to_json(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``xml_to_json`` command: convert an energyml xml or epc file to json."""
    parser = argparse.ArgumentParser(
        prog="xml_to_json",
        description="Convert an energyml XML file (or every object of an EPC) into OSDU JSON.",
    )
    parser.add_argument("--file", "-f", type=str, required=True, help="Input file (xml or epc)")
    parser.add_argument("--out", "-o", type=str, default=None, help="Output file")

    args = parse_args(parser, argv)

    output_path = args.out or args.file[:-4] + ".json"

    json_content = None
    if args.file.lower().endswith(".xml"):
        with open(args.file, "rb") as f:
            json_content = serialize_json(read_energyml_xml_bytes(f.read()), JSON_VERSION.OSDU_OFFICIAL)
    elif args.file.lower().endswith(".epc"):
        epc = Epc.read_file(args.file)
        json_content = (
            "[\n" + ",".join(serialize_json(o, JSON_VERSION.OSDU_OFFICIAL) for o in epc.energyml_objects) + "]"
        )
    else:
        logger.error("Unsupported input file '%s': expected a .xml or a .epc file.", args.file)
        return

    with open(output_path, "w", encoding="utf-8") as fout:
        fout.write(json_content)
    print(f"Written in {output_path}")


def json_to_xml(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``json_to_xml`` command: one xml file per object of a json input."""
    parser = argparse.ArgumentParser(
        prog="json_to_xml",
        description="Convert an energyml JSON file into one XML file per object it contains.",
    )
    parser.add_argument("--file", "-f", type=str, required=True, help="Input file (json)")
    parser.add_argument("--out", "-o", type=str, default=None, help="Output folder (defaults to the input folder)")

    args = parse_args(parser, argv)

    with open(args.file, "rb") as f:
        objs = read_energyml_json_any_version(f.read())

    output_folder = pathlib.Path(args.out or args.file).parent.resolve()
    for obj in objs:
        file_path = output_folder / gen_energyml_object_path(obj)
        with open(file_path, "w", encoding="utf-8") as fout:
            fout.write(serialize_xml(obj))
        print(f"Written in {file_path}")


def json_to_epc(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``json_to_epc`` command: package the objects of a json input in an EPC."""
    parser = argparse.ArgumentParser(
        prog="json_to_epc",
        description="Package every energyml object of a JSON file into a single EPC.",
    )
    parser.add_argument("--file", "-f", type=str, required=True, help="Input file (json)")
    parser.add_argument("--out", "-o", type=str, required=True, help="Output EPC file")

    args = parse_args(parser, argv)

    epc = Epc(epc_file_path=args.out)
    with open(args.file, "rb") as f:
        for obj in read_energyml_json_any_version(f.read()):
            epc.energyml_objects.append(obj)

    epc.export_file(args.out)
    print(f"Written in {args.out}")


def load_n_save(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``loadNsave`` command: read a file or a folder and write it back as an EPC."""
    parser = argparse.ArgumentParser(
        prog="loadNsave",
        description="Read every energyml object of a file or a folder (json / xml / epc) and write them "
        "back into a single EPC.",
    )
    parser.add_argument("--file", "-f", type=str, required=True, help="Input file (json or xml or epc) or folder")
    parser.add_argument("--output", "-o", type=str, help="Output file epc path")
    parser.add_argument(
        "--pkg-classical", action="store_true", help="Use classical packaging (one file per object) instead of EPC"
    )

    args = parse_args(parser, argv)

    epc = package_file_or_folder_in_epc(args.file)
    if epc is None:
        return
    epc.export_version = EpcExportVersion.CLASSIC if args.pkg_classical else EpcExportVersion.EXPANDED

    output_path = args.output or (
        args.file[:-4] + "_bis.epc" if args.file.lower().endswith(".epc") else args.file + "_bis.epc"
    )
    epc.export_file(output_path)
    print(f"Written in {output_path}")


__all__ = [
    "SAMPLE_OSDU_MAP",
    "osdu_schema_to_energyml",
    "prop_kind_to_json",
    "xml_to_json",
    "json_to_xml",
    "json_to_epc",
    "load_n_save",
]
