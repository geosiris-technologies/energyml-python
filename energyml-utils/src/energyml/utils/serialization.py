# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from io import BytesIO
from typing import Optional, Any

import energyml
import xsdata
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import JsonSerializer
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .introspection import get_class_from_name, get_energyml_class_in_related_dev_pkg
from .manager import dict_energyml_modules, get_class_pkg_version, get_class_pkg
from .xml import get_class_name_from_xml, get_tree, get_xml_encoding


def _read_energyml_xml_bytes_as_class(file: bytes, obj_class: type) -> Any:
    """
    Read an xml file into the instance of type :param:`obj_class`.
    :param file:
    :param obj_class:
    :return:
    """
    parser = XmlParser()
    try:
        return parser.from_bytes(file, obj_class)
    except ParserError as e:
        print(f"Failed to parse file {file} as class {obj_class}")
        raise e


def read_energyml_xml_bytes(file: bytes, obj_type: Optional[type] = None) -> Any:
    """
    Read an xml file. The type of object is searched from the xml root name if not given.
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
        return read_energyml_xml_bytes_as_class(file.getbuffer(), obj_class)
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


def serialize_xml(obj) -> str:
    context = XmlContext(
        # element_name_generator=text.camel_case,
        # attribute_name_generator=text.kebab_case
    )
    serializer_config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(context=context, config=serializer_config)
    return serializer.render(obj)


def serialize_json(obj) -> str:
    context = XmlContext(
        # element_name_generator=text.camel_case,
        # attribute_name_generator=text.kebab_case
    )
    serializer_config = SerializerConfig(indent="  ")
    serializer = JsonSerializer(context=context, config=serializer_config)
    return serializer.render(obj)
