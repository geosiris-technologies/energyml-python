# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import json
import logging
from io import BytesIO
from typing import Optional, Any, Union

import xsdata
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser, JsonParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import JsonSerializer
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .introspection import get_class_from_name, get_energyml_class_in_related_dev_pkg, get_class_from_content_type
from .xml import get_class_name_from_xml, get_tree, get_xml_encoding, ENERGYML_NAMESPACES


def _read_energyml_xml_bytes_as_class(file: bytes, obj_class: type) -> Any:
    """
    Read a xml file into the instance of type :param:`obj_class`.
    :param file:
    :param obj_class:
    :return:
    """
    config = ParserConfig(
        # fail_on_unknown_properties=False,
        # fail_on_unknown_attributes=False,
        # process_xinclude=True,
    )
    parser = XmlParser(config=config)
    try:
        return parser.from_bytes(file, obj_class)
    except ParserError as e:
        logging.error(f"Failed to parse file {file} as class {obj_class}")
        if len(e.args) > 0:
            if "Unknown property" in e.args[0]:
                logging.error("A property has not been found, please check if your 'xsi::type' values contains "
                              "the xml namespace (e.g. 'xsi:type=\"eml:VerticalCrsEpsgCode\"').")
        raise e


def read_energyml_xml_bytes(file: bytes, obj_type: Optional[type] = None) -> Any:
    """
    Read a xml file. The type of object is searched from the xml root name if not given.
    :param obj_type:
    :param file:
    :return:
    """
    if obj_type is None:
        obj_type = get_class_from_name(get_class_name_from_xml(get_tree(file)))
    try:
        return _read_energyml_xml_bytes_as_class(file, obj_type)
    except xsdata.exceptions.ParserError as e:
        print(f"Failed to read file with type {obj_type}: {get_energyml_class_in_related_dev_pkg(obj_type)}")
        for obj_type_dev in get_energyml_class_in_related_dev_pkg(obj_type):
            try:
                print(f"Trying with class : {obj_type_dev}")
                obj = _read_energyml_xml_bytes_as_class(
                    file, obj_type_dev
                )
                print(f" ==> succeed read with {obj_type_dev}")
                return obj
            except Exception:
                pass
        raise e


def read_energyml_xml_io(file: BytesIO, obj_class: Optional[type] = None) -> Any:
    if obj_class is not None:
        return _read_energyml_xml_bytes_as_class(file.getbuffer(), obj_class)
    else:
        return read_energyml_xml_bytes(file.getbuffer())


def read_energyml_xml_str(file_content: str) -> Any:
    encoding = get_xml_encoding(file_content)
    return read_energyml_xml_bytes(file_content.encode(encoding))


def read_energyml_xml_file(file_path: str) -> Any:
    xml_content_b = ""
    with open(file_path, "rb") as f:
        xml_content_b = f.read()
    return read_energyml_xml_bytes(xml_content_b)


def _read_energyml_json_bytes_as_class(file: bytes, obj_class: type) -> Any:
    """
    Read a xml file into the instance of type :param:`obj_class`.
    :param file:
    :param obj_class:
    :return:
    """
    config = ParserConfig(
        # fail_on_unknown_properties=False,
        # fail_on_unknown_attributes=False,
        # process_xinclude=True,
    )
    parser = JsonParser(config=config)
    try:
        return parser.from_bytes(file, obj_class)
    except ParserError as e:
        print(f"Failed to parse file {file} as class {obj_class}")
        raise e


def read_energyml_json_bytes(file: bytes, obj_type: Optional[type] = None) -> Any:
    """
    Read a xml file. The type of object is searched from the xml root name if not given.
    :param obj_type:
    :param file:
    :return:
    """
    if obj_type is None:
        obj_type = get_class_from_content_type(get_class_from_json_dict(file))
    try:
        return _read_energyml_json_bytes_as_class(file, obj_type)
    except xsdata.exceptions.ParserError as e:
        print(f"Failed to read file with type {obj_type}: {get_energyml_class_in_related_dev_pkg(obj_type)}")
        for obj_type_dev in get_energyml_class_in_related_dev_pkg(obj_type):
            try:
                print(f"Trying with class : {obj_type_dev}")
                obj = _read_energyml_json_bytes_as_class(
                    file, obj_type_dev
                )
                print(f" ==> succeed read with {obj_type_dev}")
                return obj
            except Exception:
                pass
        raise e


def read_energyml_json_io(file: BytesIO, obj_class: Optional[type] = None) -> Any:
    if obj_class is not None:
        return _read_energyml_json_bytes_as_class(file.getbuffer(), obj_class)
    else:
        return read_energyml_json_bytes(file.getbuffer())


def read_energyml_json_str(file_content: str) -> Any:
    return read_energyml_json_bytes(file_content.encode("utf-8"))


def read_energyml_json_file(file_path: str) -> Any:
    json_content_b = ""
    with open(file_path, "rb") as f:
        json_content_b = f.read()
    return read_energyml_json_bytes(json_content_b)


def serialize_xml(obj) -> str:
    context = XmlContext(
        # element_name_generator=text.camel_case,
        # attribute_name_generator=text.kebab_case
    )
    serializer_config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(context=context, config=serializer_config)
    return serializer.render(obj, ns_map=ENERGYML_NAMESPACES)


def serialize_json(obj) -> str:
    context = XmlContext(
        # element_name_generator=text.camel_case,
        # attribute_name_generator=text.kebab_case
    )
    serializer_config = SerializerConfig(indent="  ")
    serializer = JsonSerializer(context=context, config=serializer_config)
    return serializer.render(obj)


def get_class_from_json_dict(o: Union[dict, bytes]) -> str:
    if isinstance(o, str) or isinstance(o, bytes):
        o = json.loads(o)
    print(type(o))
    for att in ["$type", "dataObjectType"]:
        if att in o:
            return o[att]
    return None
