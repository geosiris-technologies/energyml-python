# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import json
import logging
import numpy as np
import traceback
from enum import Enum
from io import BytesIO
from typing import Optional, Any, Union, List, Dict, Callable, Type

import xsdata
from lxml import etree
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.models.generics import DerivedElement
from xsdata.formats.dataclass.parsers import XmlParser, JsonParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import (
    LxmlEventHandler,
    XmlEventHandler,
)
from xsdata.formats.dataclass.serializers import JsonSerializer
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .exception import UnknownTypeFromQualifiedType, NotParsableType
from .introspection import (
    as_obj_prefixed_class_if_possible,
    get_class_from_name,
    get_energyml_class_in_related_dev_pkg,
    get_class_from_content_type,
    get_qualified_type_from_class,
    get_class_fields,
    get_obj_identifier,
    is_primitive,
    search_attribute_matching_name,
    get_class_from_qualified_type,
    get_matching_class_attribute_name,
    is_enum,
)
from .xml import (
    get_class_name_from_xml,
    get_tree,
    get_xml_encoding,
    ENERGYML_NAMESPACES,
)


class JSON_VERSION(Enum):
    XSDATA = "XSDATA"
    OSDU_OFFICIAL = "OSDU_OFFICIAL"


def _read_energyml_xml_bytes_as_class(
    file: bytes,
    obj_class: Type,
    fail_on_unknown_properties=True,
    fail_on_unknown_attributes=True,
) -> Any:
    """
    Read a xml file into the instance of type :param:`obj_class`.
    :param file:
    :param obj_class:
    :return:
    """
    config = ParserConfig(
        fail_on_unknown_properties=fail_on_unknown_properties,
        fail_on_unknown_attributes=fail_on_unknown_attributes,
        # process_xinclude=True,
    )
    parser = XmlParser(config=config)
    try:
        return parser.from_bytes(file, obj_class)
    except ParserError as e:
        logging.error(f"Failed to parse file {file} as class {obj_class}")
        if len(e.args) > 0:
            if "unknown property" in e.args[0].lower():
                logging.error(e)
                logging.error(
                    "A property has not been found, please check if your 'xsi::type' values contains "
                    "the xml namespace (e.g. 'xsi:type=\"eml:VerticalCrsEpsgCode\"')."
                )
        raise e


def read_energyml_xml_tree(file: etree, obj_type: Optional[type] = None) -> Any:
    # if obj_type is None:
    #     obj_type = get_class_from_name(get_class_name_from_xml(file))
    # parser = XmlParser(handler=XmlEventHandler)
    # # parser = XmlParser(handler=LxmlEventHandler)
    # return parser.parse(file, obj_type)
    return read_energyml_xml_bytes(etree.tostring(file, encoding="utf8"))


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
        if len(e.args) > 0:
            if "unknown property" in e.args[0].lower():
                logging.error(f"Trying reading without fail on unknown attribute/property")
                try:
                    return _read_energyml_xml_bytes_as_class(file, obj_type, False, False)
                except Exception as e:
                    logging.error(traceback.print_stack())
                    pass

        # Otherwise
        for obj_type_dev in get_energyml_class_in_related_dev_pkg(obj_type):
            try:
                logging.debug(f"Trying with class : {obj_type_dev}")
                obj = _read_energyml_xml_bytes_as_class(file, obj_type_dev)
                logging.debug(f" ==> succeed read with {obj_type_dev}")
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
            logging.error(f"Failed to parse file {file} as class {obj_class}")
            raise e
    elif json_version == JSON_VERSION.OSDU_OFFICIAL:
        return read_json_dict(json.loads(file))


def read_energyml_json_bytes(
    file: Union[dict, bytes], json_version: JSON_VERSION, obj_type: Optional[type] = None
) -> Union[List, Any]:
    """
    Read a json file into energyml object. If json_version==JSON_VERSION.XSDATA the instance will be of type :param:`obj_class`.
    For json_version==JSON_VERSION.OSDU_OFFICIAL a list of read objects is returned
    :param file:
    :param json_version:
    :param obj_type: ignored if the json file is a list
    :return:
    """

    if isinstance(file, bytes):
        json_obj = json.loads(file)
    else:
        json_obj = file

    if not isinstance(json_obj, list):
        json_obj = [json_obj]
    else:
        obj_type = None

    result = []
    for obj in json_obj:
        try:
            if obj_type is None:
                obj_type = get_class_from_content_type(get_class_from_json_dict(obj))
            if json_version == JSON_VERSION.XSDATA:
                try:
                    result = result + _read_energyml_json_bytes_as_class(obj, obj_type)
                except xsdata.exceptions.ParserError as e:
                    logging.error(
                        f"Failed to read file with type {obj_type}: {get_energyml_class_in_related_dev_pkg(obj_type)}"
                    )
                    for obj_type_dev in get_energyml_class_in_related_dev_pkg(obj_type):
                        try:
                            logging.debug(f"Trying with class : {obj_type_dev}")
                            obj = _read_energyml_json_bytes_as_class(obj, obj_type_dev)
                            logging.debug(f" ==> succeed read with {obj_type_dev}")
                            result = result + obj
                        except Exception:
                            pass
                    raise e
            elif json_version == JSON_VERSION.OSDU_OFFICIAL:
                result = result + read_json_dict(obj)
        except Exception as e:
            logging.error(e)
            logging.error(obj)
            raise e
        obj_type = None

    return result


def read_energyml_json_io(
    file: BytesIO, json_version: JSON_VERSION = JSON_VERSION.OSDU_OFFICIAL, obj_class: Optional[type] = None
) -> Union[List, Any]:
    if obj_class is not None:
        return _read_energyml_json_bytes_as_class(file.getbuffer(), json_version, obj_class)
    else:
        return read_energyml_json_bytes(file.getbuffer(), json_version)


def read_energyml_json_str(
    file_content: str, json_version: JSON_VERSION = JSON_VERSION.OSDU_OFFICIAL
) -> Union[List, Any]:
    return read_energyml_json_bytes(file_content.encode("utf-8"), json_version)


def read_energyml_json_file(
    file_path: str, json_version: JSON_VERSION = JSON_VERSION.OSDU_OFFICIAL
) -> Union[List, Any]:
    json_content_b = ""
    with open(file_path, "rb") as f:
        json_content_b = f.read()
    return read_energyml_json_bytes(json_content_b, json_version)


#    _____           _       ___             __  _
#   / ___/___  _____(_)___ _/ (_)___  ____ _/ /_(_)___  ____
#   \__ \/ _ \/ ___/ / __ `/ / /_  / / __ `/ __/ / __ \/ __ \
#  ___/ /  __/ /  / / /_/ / / / / /_/ /_/ / /_/ / /_/ / / / /
# /____/\___/_/  /_/\__,_/_/_/ /___/\__,_/\__/_/\____/_/ /_/


def serialize_xml(obj) -> str:
    obj = as_obj_prefixed_class_if_possible(obj)
    context = XmlContext(
        # element_name_generator=text.camel_case,
        # attribute_name_generator=text.kebab_case
    )
    serializer_config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(context=context, config=serializer_config)
    return serializer.render(obj, ns_map=ENERGYML_NAMESPACES)


def serialize_json(obj, json_version: JSON_VERSION = JSON_VERSION.OSDU_OFFICIAL) -> str:
    obj = as_obj_prefixed_class_if_possible(obj)
    if json_version == JSON_VERSION.XSDATA:
        context = XmlContext(
            # element_name_generator=text.camel_case,
            # attribute_name_generator=text.kebab_case
        )
        serializer_config = SerializerConfig(indent="  ")
        serializer = JsonSerializer(context=context, config=serializer_config)
        return serializer.render(obj)
    elif json_version == JSON_VERSION.OSDU_OFFICIAL:
        return json.dumps(to_json_dict(obj), indent=4, sort_keys=True)


def get_class_from_json_dict(o: Union[dict, bytes]) -> Optional[str]:
    """
    Searches for the attribute "$type"
    :param o:
    :return:
    """
    if isinstance(o, str) or isinstance(o, bytes):
        o = json.loads(o)
    for att in ["$type", "dataObjectType"]:
        if att in o:
            return o[att]
    return None


# RAW


def read_json_dict(obj: Any) -> List:
    """
    Reads a json dict valid with the OSDU standard.
    This means:
        - Any not "primitive" object (not str/number/bool ...) has a "$type" attribute set to its qualified type
        - None value are not given, except for mandatory attributes (depending on the energyml standard)
        - If an attribute is named 'value' (case-sensitive, this doesn't apply to 'Value'), the name of the attribute
            in the dict is "_"
        - "_data" attribute is given for DOR (not mandatory) and contains the json representation of the target object
    :param obj:
    :return: a list of read objects. This is a list due to the "_data" attribute
    """
    if "$type" in obj:
        sub_obj = []
        obj = _read_json_dict(obj, sub_obj)
        return [obj] + sub_obj
    else:
        raise UnknownTypeFromQualifiedType()


def _read_json_dict(obj_json: Any, sub_obj: List) -> Any:
    """
    Reads a json dict valid with the OSDU standard.
    This means:
        - Any not "primitive" object (not str/number/bool ...) has a "$type" attribute set to its qualified type
        - None value are not given, except for mandatory attributes (depending on the energyml standard)
        - If an attribute is named 'value' (case-sensitive, this doesn't apply to 'Value'), the name of the attribute
            in the dict is "_"
        - "_data" attribute is given for DOR (not mandatory) and contains the json representation of the target object
    :param obj_json:
    :param sub_obj: list of contextual external objects given inside the object that references them with a DOR
    :return: a list of read objects. This is a list due to the "_data" attribute
    """
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
                    try:
                        matching = get_matching_class_attribute_name(obj, att)
                        if matching is not None:
                            setattr(
                                obj,
                                matching,
                                _read_json_dict(val, sub_obj),
                            )
                        else:
                            logging.error(f"No matching attribute for attribute {att} in {obj}")
                    except Exception as e:
                        logging.error(f"Error assign attribute value for attribute {att} in {obj}")
        except Exception as e:
            logging.error(
                f"Err on {att}",
                search_attribute_matching_name(
                    obj=obj,
                    name_rgx=att,
                    deep_search=False,
                    search_in_sub_obj=False,
                ),
                obj,
            )
            raise e
        return obj
    elif isinstance(obj_json, list):
        return [_read_json_dict(o, sub_obj) for o in obj_json]
    elif is_primitive(obj_json):
        # logging.debug(f"PRIM : {obj_json}")
        return obj_json
    else:
        raise NotParsableType(type(obj_json) + " " + obj_json)


def to_json_dict(obj: Any, obj_id_to_obj: Optional[Dict] = None) -> Any:
    """
    Transform an object to a dict valid with the OSDU standard
    :param obj:
    :param obj_id_to_obj:
    :return:
    """
    return to_json_dict_fn(
        obj,
        lambda _id: obj_id_to_obj[_id] if obj_id_to_obj is not None and _id in obj_id_to_obj else None,
    )


def to_json_dict_fn(obj: Any, f_identifier_to_obj: Callable) -> Any:
    """
    Transform an object to a dict valid with the OSDU standard
    :param obj:
    :param f_identifier_to_obj: A function that takes an object identifier see :func:`.introspection.get_obj_identifier`
            and returns the corresponding object
    :return:
    """
    assert f_identifier_to_obj is not None
    return _to_json_dict_fn(obj, f_identifier_to_obj, None)


def _fill_dict_with_attribs(
    res: Dict,
    obj: Any,
    f_identifier_to_obj: Optional[Callable] = None,
    _parent: Optional[Any] = None,
) -> None:

    for att_name, field in get_class_fields(obj).items():
        field_name = field.metadata["name"] if "name" in field.metadata else field.name
        if field_name == "value":
            field_name = "_"
        field_name = field_name[0].upper() + field_name[1:]
        mandatory = field.metadata["required"] if "required" in field.metadata else False
        value = getattr(obj, att_name)

        if "Any_element" in str(field_name):
            logging.debug(f"\t> {field_name}, {att_name} : {value}, {type(obj)}")

        if (value is not None or mandatory) and (not isinstance(value, list) or len(value) > 0):
            res[field_name] = _to_json_dict_fn(value, f_identifier_to_obj, obj)

            if _parent is not None and (field_name.lower() == "uuid" or field_name.lower() == "uid"):
                # adding referenced data
                ref_identifier = get_obj_identifier(obj)
                if f_identifier_to_obj is not None:
                    ref_value = f_identifier_to_obj(ref_identifier)
                    if ref_value is not None:
                        res["_data"] = to_json_dict_fn(ref_value, f_identifier_to_obj)
                    else:
                        logging.debug(f"NotFound : {ref_identifier}")


def _to_json_dict_fn(
    obj: Any,
    f_identifier_to_obj: Optional[Callable] = None,
    _parent: Optional[Any] = None,
) -> Any:
    """
    Transform an object to a dict valid with the OSDU standard
    :param obj:
    :param f_identifier_to_obj: A function that takes an object identifier see :func:`.introspection.get_obj_identifier`
            and returns the corresponding object
    :param _parent: None if :param:`obj` is the one given directly by the user, else the parent object of :param:`obj`
            in the original object given by the user
    :return: Any
    """
    if obj is None:
        return None
    elif isinstance(obj, float) and np.isnan(obj):
        print("NaN found")
        return None
    elif is_enum(obj):
        return obj.value
        # return {
        #     "$type": get_qualified_type_from_class(obj),
        #     "_": obj.value
        # }
    elif is_primitive(obj):
        return obj
    elif isinstance(obj, xsdata.models.datatype.XmlDateTime):
        return str(obj)
    elif isinstance(obj, DerivedElement):
        res = {"$type": get_qualified_type_from_class(obj.value)}
        # _fill_dict_with_attribs(res, obj.value, f_identifier_to_obj, _parent)
        return res
    elif isinstance(obj, list):
        return [_to_json_dict_fn(o, f_identifier_to_obj, _parent) for o in obj]
    else:
        try:
            res = {"$type": get_qualified_type_from_class(obj)}
            _fill_dict_with_attribs(res, obj, f_identifier_to_obj, _parent)
            return res
        except Exception as e:
            logging.error(f"Except on qt: {obj} - {type(obj)}")
            raise e
