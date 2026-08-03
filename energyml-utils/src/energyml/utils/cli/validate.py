# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""``validate`` — report the schema and consistency errors of an energyml file or folder."""

from __future__ import annotations

import argparse
import json
import logging
from typing import Dict, List, Optional

from energyml.utils.cli._common import package_file_or_folder_in_epc, parse_args
from energyml.utils.introspection import get_enum_values
from energyml.utils.validation import ErrorType, validate_epc

logger = logging.getLogger(__name__)


def validate_files(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``validate`` command: print the validation errors as JSON."""
    parser = argparse.ArgumentParser(
        prog="validate",
        description="Validate every energyml object of a file or a folder and print the errors as JSON "
        "on the standard output.",
    )
    parser.add_argument("--file", "-f", type=str, required=True, help="Input file (json or xml or epc) or folder")
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

    args = parse_args(parser, argv)

    epc = package_file_or_folder_in_epc(args.file)
    if epc is None:
        return

    ignored = {et.lower() for et in (args.ignore_err_type or [])}
    err_json = [err.toJson() for err in validate_epc(epc) if str(err.error_type).lower() not in ignored]

    err_json_sorted = sorted(err_json, key=lambda x: (x["err_class"], x["error_type"], x.get("object_uuid", "")))

    if args.ignore_prodml_version_errs:
        err_json_sorted = [err for err in err_json_sorted if "prodml23" not in err.get("msg", "")]

    if args.group_by_err_class:
        grouped: Dict[str, List[Dict]] = {}
        for err in err_json_sorted:
            grouped.setdefault(err.get("err_class", "UnknownErrorClass"), []).append(err)
        print(json.dumps(grouped, indent=4))
    else:
        print(json.dumps(err_json_sorted, indent=4))


__all__ = ["validate_files"]
