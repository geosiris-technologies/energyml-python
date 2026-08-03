# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""Helpers shared by the command line entry points.

Nothing here is part of the public API of the library: these are the pieces the commands of
:mod:`energyml.utils.cli` have in common (logging setup, class lookup from a type name, packaging
of an input path into an :class:`~energyml.utils.epc.Epc`).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Any, Callable, List, Optional

from energyml.utils.epc import Epc
from energyml.utils.epc_utils import get_epc_content_type_path
from energyml.utils.introspection import (
    get_class_from_qualified_type,
    get_class_from_simple_name,
    get_non_abstract_classes,
    get_module_name_and_type_from_content_or_qualified_type,
    get_qualified_type_from_class,
    is_abstract,
    random_value_from_class,
    search_class_in_module_from_partial_name,
)
from energyml.utils.serialization import (
    JSON_VERSION,
    read_energyml_json_bytes,
    read_energyml_xml_bytes,
    serialize_json,
    serialize_xml,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def _free_flags(parser: argparse.ArgumentParser, *flags: str) -> List[str]:
    """Keep only the *flags* the parser does not already use.

    The short forms are conveniences, not contracts: ``describe_as_csv`` already spends ``-v`` on
    ``--columnsValues``, and stealing it would break every existing command line.
    """
    taken = {opt for action in parser._actions for opt in action.option_strings}
    return [flag for flag in flags if flag not in taken]


def add_verbosity_argument(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add the ``--verbose`` / ``--quiet`` flags (and their short forms when free) to *parser*."""
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        *_free_flags(parser, "--verbose", "-v"),
        action="count",
        default=0,
        help="Increase verbosity (-v for INFO, -vv for DEBUG)",
    )
    group.add_argument(
        *_free_flags(parser, "--quiet", "-q"),
        action="store_true",
        help="Only report errors",
    )
    return parser


def configure_logging(args: argparse.Namespace) -> None:
    """Configure the root logger from the verbosity flags of *args*.

    Only a command line entry point may do this: a library must never call
    :func:`logging.basicConfig`, since it would silently take over the configuration of the
    application that imports it. ``extract_3d`` used to force ``level=logging.DEBUG``
    unconditionally, which buried its own output under thousands of lines.
    """
    verbose = getattr(args, "verbose", 0)
    if getattr(args, "quiet", False):
        level = logging.ERROR
    elif verbose >= 2:
        level = logging.DEBUG
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s", stream=sys.stderr)


def parse_args(parser: argparse.ArgumentParser, argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse *argv* with *parser* and apply the verbosity flags."""
    add_verbosity_argument(parser)
    args = parser.parse_args(argv)
    configure_logging(args)
    return args


# ---------------------------------------------------------------------------
# Class lookup
# ---------------------------------------------------------------------------


def find_class_from_type_name(type_name: str) -> Optional[type]:
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


def print_close_type_names(type_name: str) -> None:
    """Print the types that look like *type_name*, to help the user fix their input."""
    print(f"Class not found for '{type_name}', please check the type name.")
    try:
        module_name, object_type = get_module_name_and_type_from_content_or_qualified_type(type_name)
    except ValueError:
        return
    print("Possible types are :")
    for cn in search_class_in_module_from_partial_name(module_name, object_type):
        print(f" - {cn.__name__}")


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def serialize_object(obj: Any, file_format: str) -> str:
    """Serialize *obj* as XML or as OSDU JSON."""
    if file_format.lower() == "xml":
        return serialize_xml(obj)
    return serialize_json(obj, JSON_VERSION.OSDU_OFFICIAL)


def file_name_prefix(obj: Any) -> str:
    """
    File name prefix for a generated object : its qualified type (e.g. 'resqml22.TriangulatedSetRepresentation'),
    or its class name if the qualified type cannot be computed.

    :param obj:
    :return: str
    """
    try:
        return get_qualified_type_from_class(obj) or type(obj).__name__
    except Exception:  # pragma: no cover — defensive: any class without a qualified type
        return type(obj).__name__


def read_energyml_json_any_version(content: bytes) -> List[Any]:
    """Read an energyml JSON payload, trying the OSDU flavour first then the xsdata one."""
    try:
        return read_energyml_json_bytes(content, JSON_VERSION.OSDU_OFFICIAL)
    except Exception as osdu_error:
        logger.debug("Not an OSDU JSON payload (%s), retrying with the xsdata flavour.", osdu_error)
        return read_energyml_json_bytes(content, JSON_VERSION.XSDATA)


# ---------------------------------------------------------------------------
# Random object generation
# ---------------------------------------------------------------------------


def is_excluded(cls: type, exclude: Optional[List[str]]) -> bool:
    """
    Test if the class *cls* must be excluded : it is the case if one of the *exclude* values is contained (case
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
    except Exception:  # pragma: no cover — defensive: any class without a qualified type
        pass
    searched_in = [value.lower() for value in searched_in if len(value) > 0]

    return any(excluded.lower() in value for excluded in exclude for value in searched_in)


def generate_random_objects(
    obj_class: type,
    callback: Optional[Callable[[Any], None]] = None,
    exclude: Optional[List[str]] = None,
) -> List[Any]:
    """
    Generate a random object for *obj_class*, or, if *obj_class* is abstract, one random object per non abstract
    sub class of *obj_class*.

    :param obj_class:
    :param callback: if not None, it is called with each object right after its generation (e.g. to write it on the
                     disk without waiting for the end of the whole generation). In that case, the objects are not
                     kept in memory and an empty list is returned.
    :param exclude: list of values : every class matching one of them (see :func:`is_excluded`) is not generated
    :return: a list of generated objects, or an empty list if a *callback* was given
    """
    if is_abstract(obj_class):
        classes_to_generate = get_non_abstract_classes(obj_class)
        if len(classes_to_generate) == 0:
            print(f"No instanciable sub class found for the abstract class '{obj_class.__name__}'.")
            return []

        nb_found = len(classes_to_generate)
        classes_to_generate = [cls for cls in classes_to_generate if not is_excluded(cls, exclude)]
        nb_excluded = nb_found - len(classes_to_generate)

        excluded_msg = f", {nb_excluded} excluded" if nb_excluded > 0 else ""
        print(
            f"'{obj_class.__name__}' is abstract : generating one object per sub class "
            f"({nb_found} found{excluded_msg})."
        )
    elif is_excluded(obj_class, exclude):
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
            logger.error("Failed to generate an object for '%s': %s: %s", cls.__name__, type(e).__name__, e)
            continue

        if callback is not None:
            callback(obj)
        else:
            objs.append(obj)

    return objs


# ---------------------------------------------------------------------------
# Input packaging
# ---------------------------------------------------------------------------


def _read_objects_from_file(file_path: str) -> List[Any]:
    """Read every energyml object of a single json / xml / epc file. Never raises."""
    file_name = os.path.basename(file_path)
    try:
        if file_path.endswith(".json"):
            with open(file_path, "rb") as file:
                return list(read_energyml_json_any_version(file.read()))
        if file_path.endswith(".xml"):
            if get_epc_content_type_path() in file_path:
                return []
            with open(file_path, "rb") as file:
                return [read_energyml_xml_bytes(file.read())]
        if file_path.endswith(".epc"):
            epc = Epc.read_file(file_path)
            if epc is None:
                logger.error("File %s is NOT a valid EnergyML EPC file: empty EPC", file_name)
                return []
            return list(epc.energyml_objects)
    except Exception as e:
        logger.error("File %s is NOT a valid EnergyML file: %s: %s", file_name, type(e).__name__, e)
    return []


def package_file_or_folder_in_epc(input_path: str) -> Optional[Epc]:
    """
    Read every energyml object found in *input_path* — a json / xml / epc file, or a folder of
    them — and return them packaged in a single in-memory :class:`~energyml.utils.epc.Epc`.

    Returns ``None`` when *input_path* does not exist or is not a supported kind of input.
    """
    if not os.path.exists(input_path):
        logger.error("File %s does not exist.", input_path)
        return None
    if not os.path.isdir(input_path) and not input_path.lower().endswith((".json", ".xml", ".epc")):
        logger.error("File %s is not a valid input file (should be a folder or a json/xml/epc file).", input_path)
        return None

    objects: List[Any] = []
    if os.path.isdir(input_path):
        for filename in sorted(os.listdir(input_path)):
            candidate = os.path.join(input_path, filename)
            if os.path.isfile(candidate):
                objects.extend(_read_objects_from_file(candidate))
    else:
        objects.extend(_read_objects_from_file(input_path))

    epc = Epc()
    epc.energyml_objects = objects
    return epc


__all__ = [
    "add_verbosity_argument",
    "configure_logging",
    "parse_args",
    "find_class_from_type_name",
    "print_close_type_names",
    "serialize_object",
    "file_name_prefix",
    "read_energyml_json_any_version",
    "is_excluded",
    "generate_random_objects",
    "package_file_or_folder_in_epc",
]
