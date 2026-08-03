# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""``describe_as_csv`` — summarize the energyml objects of a folder in a CSV table."""

from __future__ import annotations

import argparse
import logging
import os
from typing import Any, List, Optional, Tuple

from energyml.utils.cli._common import parse_args, read_energyml_json_any_version
from energyml.utils.epc import Epc
from energyml.utils.introspection import (
    get_content_type_from_class,
    get_direct_dor_list,
    get_obj_uuid,
    get_object_attribute_rgx,
    get_qualified_type_from_class,
)
from energyml.utils.serialization import read_energyml_xml_bytes

logger = logging.getLogger(__name__)

_DEFAULT_COLUMN_NAMES = ["Title", "QualifiedType", "Uuid", "SchemaVersion", "Path", "Dors uuids"]
_DEFAULT_COLUMN_VALUES = ["citation.title", "$qualifiedtype", "Uuid|Uid", "schemaVersion", "$Path", "$Dor"]


def _read_folder(folder: str) -> List[Tuple[Any, str]]:
    """Return ``[(energyml_object, source_file_path), ...]`` for every readable file of *folder*."""
    objects: List[Tuple[Any, str]] = []
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        if not os.path.isfile(path):
            continue
        try:
            if path.endswith(".json"):
                with open(path, "rb") as file:
                    objects.extend((o, path) for o in read_energyml_json_any_version(file.read()))
            elif path.endswith(".xml"):
                with open(path, "rb") as file:
                    objects.append((read_energyml_xml_bytes(file.read()), path))
            elif path.endswith(".epc"):
                objects.extend((o, path) for o in Epc.read_file(path).energyml_objects)
        except Exception as e:
            # one unreadable file must not stop the description of the others
            logger.error("File %s could not be read: %s: %s", filename, type(e).__name__, e)
    return objects


def _cell_value(obj: Any, column: str, source_path: str) -> str:
    """Value of one cell : a ``$`` directive, or a regex matching an attribute of *obj*."""
    if not column.startswith("$"):
        return str(get_object_attribute_rgx(obj, column) or "")

    directive = column.lower()
    if directive == "$type":
        return type(obj).__name__
    if directive == "$qualifiedtype":
        return str(get_qualified_type_from_class(obj) or "")
    if directive == "$contenttype":
        return str(get_content_type_from_class(obj) or "")
    if directive == "$path":
        return source_path
    if directive == "$dor":
        return str(sorted({get_obj_uuid(dor) for dor in get_direct_dor_list(obj)})).replace(";", ", ")
    logger.warning("Unknown column directive '%s' — an empty cell is written.", column)
    return ""


def describe_as_csv(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``describe_as_csv`` command."""
    parser = argparse.ArgumentParser(
        prog="describe_as_csv",
        description="Write a ';'-separated CSV describing every energyml object found in a folder.",
    )
    parser.add_argument("--folder", "-f", type=str, required=True, help="Input folder")
    parser.add_argument(
        "--columnsNames",
        "-c",
        type=str,
        default=_DEFAULT_COLUMN_NAMES,
        nargs="*",
        help="Columns titles",
    )
    parser.add_argument(
        "--columnsValues",
        "-v",
        type=str,
        default=_DEFAULT_COLUMN_VALUES,
        nargs="*",
        help="Columns values. Use $type/$qualifiedType/$contentType/$path/$dor or simpler, "
        "a regex matching an attribute",
    )

    args = parse_args(parser, argv)

    logger.info("Reading files of %s", args.folder)
    objects = _read_folder(args.folder)

    out_name = "describe.csv"
    cpt = 0
    while os.path.exists(os.path.join(args.folder, out_name)):
        out_name = f"describe_{cpt}.csv"
        cpt += 1

    logger.info("Parsing %d object(s)", len(objects))
    out_path = os.path.join(args.folder, out_name)
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(";".join(args.columnsNames))
        out.write(";\n")
        for obj, source_path in objects:
            for column in args.columnsValues:
                out.write(_cell_value(obj, column, source_path))
                out.write(";")
            out.write("\n")

    print(f"Written in {out_path}")


__all__ = ["describe_as_csv"]
