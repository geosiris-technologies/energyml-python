from enum import Enum
from typing import Any, List, Optional, Union
import re
import ast
import sys

from src.energyml.utils.xml import parse_content_type, ENERGYML_NAMESPACES


primitives = (bool, str, int, float, type(None))


def is_primitive(cls: Union[type, Any]) -> bool:
    if isinstance(cls, type):
        return cls in primitives or Enum in cls.__bases__
    return is_primitive(type(cls))


def get_class_from_name(class_name_and_module: str) -> Optional[type]:
    module_name = class_name_and_module[:class_name_and_module.rindex(".")]
    last_ns_part = class_name_and_module[class_name_and_module.rindex(".") + 1:]
    try:
        return getattr(sys.modules[module_name], last_ns_part)
    except AttributeError as e:
        if "2d" in last_ns_part:
            return get_class_from_name(class_name_and_module.replace("2d", "2D"))
        elif "3d" in last_ns_part:
            return get_class_from_name(class_name_and_module.replace("3d", "3D"))
        elif last_ns_part[0].islower():
            return get_class_from_name(module_name + "." + last_ns_part[0].upper() + last_ns_part[1:])
        else:
            print(e)
    return None


def get_class_from_content_type(content_type: str) -> Optional[type]:
    ct = parse_content_type(content_type)
    domain = ct.group("domain")
    if domain is None:
        domain = "opc"
    if domain == "opc":
        xml_domain = ct.group("xmlDomain")
        opc_type = pascal_case(xml_domain[xml_domain.rindex(".") + 1:])
        print("energyml.opc.opc." + opc_type)
        return get_class_from_name("energyml.opc.opc." + opc_type)
    else:
        ns = ENERGYML_NAMESPACES[domain]
        return get_class_from_name(
            "energyml."
            + ct.group("domain")
            + ".v" + str(ct.group("domainVersion")).replace(".", "_")
            + "." + ns[ns.rindex("/") + 1:]
            + "." + ct.group("type")
        )


def snake_case(s: str) -> str:
    """
    Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    and add an underscore between words, finally convert the result to lowercase
    """
    return '_'.join(
        re.sub('([A-Z][a-z]+)', r' \1',
               re.sub('([A-Z]+)', r' \1',
                      s.replace('-', ' '))).split()).lower()


def pascal_case(s: str) -> str:
    return snake_case(s).replace("_", " ").title().replace(" ", "")


def get_class_attributes(cls: Union[type, Any]) -> List[str]:
    """
    returns a list of attributes (not private ones)
    """
    if not isinstance(cls, type):  # if cls is an instance
        cls = type(cls)
    return list(filter(lambda a: not a.startswith("__"), dir(cls)))


def get_matching_class_attribute_name(cls: Union[type, Any], attribute_name: str) -> Optional[str]:
    """
    From an object and an attribute name, returns the correct attribute name of the class.
    Example : "ObjectVersion" --> object_version.
    This method doesn't only transform to snake case but search into the obj class attributes
    """
    class_attr = get_class_attributes(cls)

    # a search with the exact value
    if attribute_name in class_attr:
        return attribute_name

    # now search with little differences
    for an in class_attr:
        if snake_case(an) == snake_case(attribute_name):
            return an

    # search regex
    pattern = re.compile(attribute_name)
    for an in class_attr:
        if pattern.match(an):
            return an

    return None


def get_object_attribute(obj: Any, attr_dot_path: str, force_snake_case=True) -> Any:
    """
    returns the value of an attribute given by a dot representation of its path in the object
    example "Citation.Title"
    """
    current_attrib_name = attr_dot_path

    if '.' in attr_dot_path:
        current_attrib_name = attr_dot_path.split('.')[0]

    if force_snake_case:
        current_attrib_name = snake_case(current_attrib_name)

    value = None
    if isinstance(obj, list):
        value = obj[int(current_attrib_name)]
    elif isinstance(obj, dict):
        value = obj[current_attrib_name]
    else:
        value = getattr(obj, current_attrib_name)

    if '.' in attr_dot_path:
        return get_object_attribute(value, attr_dot_path[len(current_attrib_name) + 1:])
    else:
        return value


def get_object_attribute_advanced(obj: Any, attr_dot_path: str) -> Any:
    """
    see @get_matching_class_attribute_name and @get_object_attribute
    """
    current_attrib_name = attr_dot_path

    if '.' in attr_dot_path:
        current_attrib_name = attr_dot_path.split('.')[0]

    current_attrib_name = get_matching_class_attribute_name(obj, current_attrib_name)

    value = None
    if isinstance(obj, list):
        value = obj[int(current_attrib_name)]
    elif isinstance(obj, dict):
        value = obj[current_attrib_name]
    else:
        value = getattr(obj, current_attrib_name)

    if '.' in attr_dot_path:
        return get_object_attribute_advanced(value, attr_dot_path[len(current_attrib_name) + 1:])
    else:
        return value


def get_object_attribute_rgx(obj: Any, attr_dot_path_rgx: str) -> Any:
    """
    see @get_object_attribute. Search the attribute name using regex for values between dots.
    Example : [Cc]itation.[Tt]it\.*
    """
    current_attrib_name = attr_dot_path_rgx

    attrib_list = re.split(r"(?<!\\)\.+", attr_dot_path_rgx)

    if len(attrib_list) > 0:
        current_attrib_name = attrib_list[0]

    # unescape Dot
    current_attrib_name = current_attrib_name.replace("\\.", ".")

    real_attrib_name = get_matching_class_attribute_name(obj, current_attrib_name)

    value = None
    if isinstance(obj, list):
        value = obj[int(real_attrib_name)]
    elif isinstance(obj, dict):
        value = obj[real_attrib_name]
    else:
        value = getattr(obj, real_attrib_name)

    if len(attrib_list) > 1:
        return get_object_attribute_rgx(value, attr_dot_path_rgx[len(current_attrib_name) + 1:])
    else:
        return value


def t_get_attribute_type(cls: Union[type, Any], attribute_name: str):
    if not isinstance(cls, type):  # if cls is an instance
        cls = type(cls)

    attrib_as_field = cls.__dataclass_fields__[attribute_name]

    # TODO : retourner le type sans les Optional,


def get_obj_type(obj: Any) -> str:
    if isinstance(obj, type):
        return str(obj.__name__)
    return get_obj_type(type(obj))


def class_match_rgx(cls: Union[type, Any], rgx: str, super_class_search: bool = True, re_flags=re.IGNORECASE):
    if not isinstance(cls, type):
        cls = type(cls)

    if re.match(rgx, cls.__name__, re_flags):
        return True

    if not is_primitive(cls) and super_class_search:
        for base in cls.__bases__:
            if class_match_rgx(base, rgx, super_class_search, re_flags):
                return True
    return False


def search_attribute_matching_type(
        obj: Any,
        type_rgx: str,
        re_flags=re.IGNORECASE,
        return_self: bool = True,  # test directly on input object and not only in its attributes
        deep_search: bool = True,  # Search inside a matching object
        super_class_search: bool = True,  # Search inside in super classes of the object
) -> List[Any]:
    res = []
    if obj is not None:
        if return_self and class_match_rgx(obj, type_rgx, super_class_search, re_flags):
            res.append(obj)
            if not deep_search:
                return res

    if isinstance(obj, list):
        for s_o in obj:
            res = res + search_attribute_matching_type(
                obj=s_o,
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
            )
    elif isinstance(obj, dict):
        for k, s_o in obj.items():
            res = res + search_attribute_matching_type(
                obj=s_o,
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
            )
    elif not is_primitive(obj):
        for att_name in get_class_attributes(obj):
            res = res + search_attribute_matching_type(
                obj=get_object_attribute_rgx(obj, att_name),
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
            )

    return res
