# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""``generate_data`` / ``generate_multiple_data`` — generate random energyml objects."""

from __future__ import annotations

import argparse
import logging
import os
import pathlib
from typing import Any, List, Optional

from energyml.utils.cli._common import (
    file_name_prefix,
    find_class_from_type_name,
    generate_random_objects,
    parse_args,
    print_close_type_names,
    serialize_object,
)
from energyml.utils.introspection import get_obj_uuid

logger = logging.getLogger(__name__)

_DEFAULT_TYPE = "energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation"
_FILE_FORMATS = ["json", "xml"]


def generate_data(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``generate_data`` command: print one random object of a given type."""
    parser = argparse.ArgumentParser(
        prog="generate_data",
        description="Generate a random energyml object of the given type and print it on the standard output. "
        "When the type is abstract, one object per non abstract sub class is generated.",
    )
    parser.add_argument(
        "--type",
        "-t",
        type=str,
        default=_DEFAULT_TYPE,
        help=f"Object type (e.g. {_DEFAULT_TYPE})",
    )
    parser.add_argument(
        "--file-format",
        "-ff",
        type=str,
        choices=_FILE_FORMATS,
        default="json",
        help=f"Type of the output files (one of : {_FILE_FORMATS}). Default is 'json'",
    )

    args = parse_args(parser, argv)

    obj_class = find_class_from_type_name(args.type)
    if obj_class is None:
        print_close_type_names(args.type)
        return

    for obj in generate_random_objects(obj_class):
        # a class that cannot be serialized must not stop the ones that follow it — the same
        # policy `generate_multiple_data` already applies
        try:
            print(serialize_object(obj, args.file_format))
        except Exception as e:
            logger.error("Failed to serialize an object of type '%s': %s: %s", type(obj).__name__, type(e).__name__, e)


def generate_multiple_data(argv: Optional[List[str]] = None) -> None:
    """
    Entry point of the ``generate_multiple_data`` command.

    Same as :func:`generate_data` but for several object types at once, sharing a common file
    format. If an output folder is given, one file per object is written in it (as soon as it is
    generated), else all objects are printed on stdout.
    """
    parser = argparse.ArgumentParser(
        prog="generate_multiple_data",
        description="Generate random energyml objects for several types at once.",
    )
    parser.add_argument(
        "--type",
        "-t",
        type=str,
        nargs="+",
        default=[_DEFAULT_TYPE],
        help=f"Object types (e.g. {_DEFAULT_TYPE} energyml.resqml.v2_2.resqmlv2.PolylineSetRepresentation)",
    )
    parser.add_argument(
        "--file-format",
        "-ff",
        type=str,
        choices=_FILE_FORMATS,
        default="json",
        help=f"Type of the output files (one of : {_FILE_FORMATS}). Default is 'json'",
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

    args = parse_args(parser, argv)

    file_format = args.file_format.lower()
    if args.output is not None:
        pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)

    def export_object(obj: Any) -> None:
        """Export an object as soon as it has been generated : one file per object, or the standard output."""
        try:
            content = serialize_object(obj, file_format)
        except Exception as e:
            logger.error("Failed to serialize an object of type '%s': %s: %s", type(obj).__name__, type(e).__name__, e)
            return

        if args.output is None:
            print(f"# ----- {type(obj).__name__} -----")
            print(content)
        else:
            file_path = os.path.join(args.output, f"{file_name_prefix(obj)}_{get_obj_uuid(obj)}.{file_format}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Object written in {file_path}")

    for type_name in args.type:
        obj_class = find_class_from_type_name(type_name)
        if obj_class is None:
            print_close_type_names(type_name)
            continue
        generate_random_objects(obj_class, callback=export_object, exclude=args.exclude)


__all__ = [
    "generate_data",
    "generate_multiple_data",
]
