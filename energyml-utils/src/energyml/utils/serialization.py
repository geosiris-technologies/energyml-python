# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import json
import logging
from enum import Enum
from io import BytesIO
from typing import Optional, Any, Union, List, Dict

import xsdata
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser, JsonParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import JsonSerializer
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .exception import UnknownTypeFromQualifiedType, NotParsableType
from .introspection import get_class_from_name, get_energyml_class_in_related_dev_pkg, get_class_from_content_type, \
    get_qualified_type_from_class, get_class_fields, get_obj_identifier, is_primitive, \
    search_attribute_matching_name, get_class_from_qualified_type, get_matching_class_attribute_name
from .xml import get_class_name_from_xml, get_tree, get_xml_encoding, ENERGYML_NAMESPACES


class JSON_VERSION(Enum):
    XSDATA = "XSDATA"
    OSDU_OFFICIAL = "OSDU_OFFICIAL"


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


def _read_energyml_json_bytes_as_class(file: bytes, json_version: JSON_VERSION, obj_class: type) -> Union[List, Any]:
    """
    Read a json file into energyml object. If json_version==JSON_VERSION.XSDATA the instance will be of type :param:`obj_class`.
    For json_version==JSON_VERSION.OSDU_OFFICIAL a list of read objects is returned
    :param file:
    :param json_version:
    :param obj_class:
    :return:
    """
    if json_version == JSON_VERSION.XSDATA:
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
    elif json_version == JSON_VERSION.OSDU_OFFICIAL:
        return read_json_dict(json.loads(file))


def read_energyml_json_bytes(file: bytes, json_version: JSON_VERSION, obj_type: Optional[type] = None) -> Union[List, Any]:
    """
    Read a json file into energyml object. If json_version==JSON_VERSION.XSDATA the instance will be of type :param:`obj_class`.
    For json_version==JSON_VERSION.OSDU_OFFICIAL a list of read objects is returned
    :param file:
    :param json_version:
    :param obj_type:
    :return:
    """
    if obj_type is None:
        obj_type = get_class_from_content_type(get_class_from_json_dict(file))
    if json_version == JSON_VERSION.XSDATA:
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
    elif json_version == JSON_VERSION.OSDU_OFFICIAL:
        return read_json_dict(json.loads(file))


def read_energyml_json_io(file: BytesIO, json_version: JSON_VERSION, obj_class: Optional[type] = None) -> Union[List, Any]:
    if obj_class is not None:
        return _read_energyml_json_bytes_as_class(file.getbuffer(), json_version, obj_class)
    else:
        return read_energyml_json_bytes(file.getbuffer(), json_version)


def read_energyml_json_str(file_content: str, json_version: JSON_VERSION) -> Union[List, Any]:
    return read_energyml_json_bytes(file_content.encode("utf-8"), json_version)


def read_energyml_json_file(file_path: str, json_version: JSON_VERSION) -> Union[List, Any]:
    json_content_b = ""
    with open(file_path, "rb") as f:
        json_content_b = f.read()
    return read_energyml_json_bytes(json_content_b, json_version)


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


# RAW


def read_json_dict(obj: Any) -> List:
    if "$type" in obj:
        sub_obj = []
        obj = _read_json_dict(obj, sub_obj)
        return [obj] + sub_obj
    else:
        raise UnknownTypeFromQualifiedType()


def _read_json_dict(obj_json: Any, sub_obj: List) -> Any:
    if isinstance(obj_json, dict) and "$type" in obj_json:
        qt = obj_json["$type"]

        obj_class = get_class_from_qualified_type(qt)
        if obj_class is None:
            raise UnknownTypeFromQualifiedType(qt + " " + json.dumps(obj_json))
        obj = obj_class()

        try:
            for att, val in obj_json.items():  # tous les autres attributs
                if att.lower() == "_data" and isinstance(val, dict):
                    for sub in read_json_dict(val):
                        sub_obj.append(sub)
                elif not att.startswith("$"):
                    if att == "_":
                        att = "value"
                    # print(f"setting : {att} {get_matching_class_attribute_name(obj, att)}")
                    setattr(obj, get_matching_class_attribute_name(obj, att), _read_json_dict(val, sub_obj))
        except Exception as e:
            print(f"Err on {att}", search_attribute_matching_name(obj=obj, name_rgx=att, deep_search=False, search_in_sub_obj=False), obj)
            raise e
        return obj
    elif isinstance(obj_json, list):
        return [
            _read_json_dict(o, sub_obj) for o in obj_json
        ]
    elif is_primitive(obj_json):
        # print(f"PRIM : {obj_json}")
        return obj_json
    else:
        raise NotParsableType(type(obj_json) + " " + obj_json)


def to_json_dict(obj: Any, obj_id_to_obj: Optional[Dict] = None) -> Any:
    return _to_json_dict(obj, obj_id_to_obj, None)


def _to_json_dict(obj: Any, obj_id_to_obj: Optional[Dict] = None, _parent: Optional[Any] = None) -> Any:
    if is_primitive(obj):
        return obj
    elif isinstance(obj, list):
        return [
            _to_json_dict(o, obj_id_to_obj, _parent) for o in obj
        ]
    else:
        res = {
            "$type": get_qualified_type_from_class(obj)
        }
        for att_name, field in get_class_fields(obj).items():
            field_name = field.metadata["name"] if "name" in field.metadata else field.name
            if field_name == "value":
                field_name = "_"
            field_name = field_name[0].upper() + field_name[1:]
            mandatory = field.metadata["required"] if "required" in field.metadata else False
            value = getattr(obj, att_name)
            if (value is not None or mandatory) and (not isinstance(value, list) or len(value) > 0):
                res[field_name] = _to_json_dict(value, obj_id_to_obj, obj)

                if _parent is not None and (field_name.lower() == "uuid" or field_name.lower() == "uid"):
                    # adding referenced data
                    ref_identifier = get_obj_identifier(obj)
                    if obj_id_to_obj is not None and ref_identifier in obj_id_to_obj:
                        res["_data"] = to_json_dict(obj_id_to_obj[ref_identifier], obj_id_to_obj)
                    else:
                        print(f"NotFound : {ref_identifier}")

        return res

