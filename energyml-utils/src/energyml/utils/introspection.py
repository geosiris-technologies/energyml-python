import datetime
import random
import re
import sys
import typing
import uuid as uuid_mod
from dataclasses import Field
from enum import Enum
from importlib import import_module
from typing import Any, List, Optional, Union, Dict, Tuple

from src.energyml.utils.manager import get_class_pkg, get_class_pkg_version
from src.energyml.utils.xml import parse_content_type, ENERGYML_NAMESPACES

RELATED_MODULES = [
    ["energyml.eml.v2_0.commonv2", "energyml.resqml.v2_0_1.resqmlv2"],
    [
        "energyml.eml.v2_1.commonv2",
        "energyml.prodml.v2_0.prodmlv2",
        "energyml.witsml.v2_0.witsmlv2",
    ],
    ["energyml.eml.v2_2.commonv2", "energyml.resqml.v2_2_dev3.resqmlv2"],
    [
        "energyml.eml.v2_3.commonv2",
        "energyml.resqml.v2_2.resqmlv2",
        "energyml.prodml.v2_2.prodmlv2",
        "energyml.witsml.v2_1.witsmlv2",
    ],
]

primitives = (bool, str, int, float, type(None))


def is_enum(cls: Union[type, Any]):
    if isinstance(cls, type):
        return Enum in cls.__bases__
    return is_enum(type(cls))


def is_primitive(cls: Union[type, Any]) -> bool:
    if isinstance(cls, type):
        return cls in primitives or Enum in cls.__bases__
    return is_primitive(type(cls))


def get_class_from_name(class_name_and_module: str) -> Optional[type]:
    module_name = class_name_and_module[: class_name_and_module.rindex(".")]
    last_ns_part = class_name_and_module[
                   class_name_and_module.rindex(".") + 1:
                   ]
    try:
        # Required to read "CustomData" on eml objects that may contain resqml values
        # ==> we need to import all modules related to the same version of the common
        import_related_module(module_name)
        return getattr(sys.modules[module_name], last_ns_part)
    except AttributeError as e:
        if "2d" in last_ns_part:
            return get_class_from_name(
                class_name_and_module.replace("2d", "2D")
            )
        elif "3d" in last_ns_part:
            return get_class_from_name(
                class_name_and_module.replace("3d", "3D")
            )
        elif last_ns_part[0].islower():
            return get_class_from_name(
                module_name + "." + last_ns_part[0].upper() + last_ns_part[1:]
            )
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
        # print("energyml.opc.opc." + opc_type)
        return get_class_from_name("energyml.opc.opc." + opc_type)
    else:
        ns = ENERGYML_NAMESPACES[domain]
        domain = ct.group("domain")
        obj_type = ct.group("type")
        if obj_type.lower().startswith("obj_"):  # for resqml201
            obj_type = "Obj" + obj_type[4:]
        version_num = str(ct.group("domainVersion")).replace(".", "_")
        if domain.lower() == "resqml" and version_num.startswith("2_0"):
            version_num = "2_0_1"
        return get_class_from_name(
            "energyml."
            + domain
            + ".v"
            + version_num
            + "."
            + ns[ns.rindex("/") + 1:]
            + "."
            + obj_type
        )


def snake_case(s: str) -> str:
    """
    Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    and add an underscore between words, finally convert the result to lowercase
    """
    return "_".join(
        re.sub(
            "([A-Z][a-z]+)",
            r" \1",
            re.sub("([A-Z]+)", r" \1", s.replace("-", " ")),
        ).split()
    ).lower()


def pascal_case(s: str) -> str:
    return snake_case(s).replace("_", " ").title().replace(" ", "")


def import_related_module(energyml_module_name: str) -> None:
    for related in RELATED_MODULES:
        if energyml_module_name in related:
            for m in related:
                try:
                    import_module(m)
                except Exception as e:
                    print(e)


def get_related_energyml_modules_name(cls: Union[type, Any]):
    if isinstance(cls, type):
        for related in RELATED_MODULES:
            if cls.__module__ in related:
                return related
    return get_related_energyml_modules_name(type(cls))


def get_class_fields(cls: Union[type, Any]) -> Dict[str, Field]:
    if not isinstance(cls, type):  # if cls is an instance
        cls = type(cls)
    try:
        return cls.__dataclass_fields__
    except AttributeError:
        return {}


def get_class_attributes(cls: Union[type, Any]) -> List[str]:
    """
    returns a list of attributes (not private ones)
    """
    # if not isinstance(cls, type):  # if cls is an instance
    #     cls = type(cls)
    # return list(filter(lambda a: not a.startswith("__"), dir(cls)))
    return list(get_class_fields(cls).keys())


def get_matching_class_attribute_name(
        cls: Union[type, Any], attribute_name: str
) -> Optional[str]:
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


def get_object_attribute(
        obj: Any, attr_dot_path: str, force_snake_case=True
) -> Any:
    """
    returns the value of an attribute given by a dot representation of its path in the object
    example "Citation.Title"
    """
    current_attrib_name = attr_dot_path

    if "." in attr_dot_path:
        current_attrib_name = attr_dot_path.split(".")[0]

    if force_snake_case:
        current_attrib_name = snake_case(current_attrib_name)

    value = None
    if isinstance(obj, list):
        value = obj[int(current_attrib_name)]
    elif isinstance(obj, dict):
        value = obj[current_attrib_name]
    else:
        value = getattr(obj, current_attrib_name)

    if "." in attr_dot_path:
        return get_object_attribute(
            value, attr_dot_path[len(current_attrib_name) + 1:]
        )
    else:
        return value


def get_object_attribute_advanced(obj: Any, attr_dot_path: str) -> Any:
    """
    see @get_matching_class_attribute_name and @get_object_attribute
    """
    current_attrib_name = attr_dot_path

    if "." in attr_dot_path:
        current_attrib_name = attr_dot_path.split(".")[0]

    current_attrib_name = get_matching_class_attribute_name(
        obj, current_attrib_name
    )

    value = None
    if isinstance(obj, list):
        value = obj[int(current_attrib_name)]
    elif isinstance(obj, dict):
        value = obj[current_attrib_name]
    else:
        value = getattr(obj, current_attrib_name)

    if "." in attr_dot_path:
        return get_object_attribute_advanced(
            value, attr_dot_path[len(current_attrib_name) + 1:]
        )
    else:
        return value


def get_object_attribute_no_verif(obj: Any, attr_name: str) -> Any:
    if isinstance(obj, list):
        return obj[int(attr_name)]
    elif isinstance(obj, dict):
        return obj[attr_name]
    else:
        return getattr(obj, attr_name)


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

    real_attrib_name = get_matching_class_attribute_name(
        obj, current_attrib_name
    )

    value = get_object_attribute_no_verif(obj, real_attrib_name)

    if len(attrib_list) > 1:
        return get_object_attribute_rgx(
            value, attr_dot_path_rgx[len(current_attrib_name) + 1:]
        )
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


def class_match_rgx(
        cls: Union[type, Any],
        rgx: str,
        super_class_search: bool = True,
        re_flags=re.IGNORECASE,
):
    if not isinstance(cls, type):
        cls = type(cls)

    if re.match(rgx, cls.__name__, re_flags):
        return True

    if not is_primitive(cls) and super_class_search:
        for base in cls.__bases__:
            if class_match_rgx(base, rgx, super_class_search, re_flags):
                return True
    return False


def search_attribute_matching_type_with_path(
        obj: Any,
        type_rgx: str,
        re_flags=re.IGNORECASE,
        return_self: bool = True,  # test directly on input object and not only in its attributes
        deep_search: bool = True,  # Search inside a matching object
        super_class_search: bool = True,  # Search inside in super classes of the object
        current_path: str = "",
) -> List[Tuple[str, Any]]:
    """
    Returns a list of tuple (path, value) for each sub attribute with type matching param "type_rgx".
    The path is a dot-version like ".Citation.Title"
    :param obj:
    :param type_rgx:
    :param re_flags:
    :param return_self:
    :param deep_search:
    :param super_class_search:
    :param current_path:
    :return:
    """
    res = []
    if obj is not None:
        if return_self and class_match_rgx(
                obj, type_rgx, super_class_search, re_flags
        ):
            res.append((current_path, obj))
            if not deep_search:
                return res

    if isinstance(obj, list):
        cpt = 0
        for s_o in obj:
            res = res + search_attribute_matching_type_with_path(
                obj=s_o,
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
                current_path=f"{current_path}.{cpt}",
            )
            cpt = cpt + 1
    elif isinstance(obj, dict):
        for k, s_o in obj.items():
            res = res + search_attribute_matching_type_with_path(
                obj=s_o,
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
                current_path=f"{current_path}.{k}",
            )
    elif not is_primitive(obj):
        for att_name in get_class_attributes(obj):
            res = res + search_attribute_matching_type_with_path(
                obj=get_object_attribute_rgx(obj, att_name),
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
                current_path=f"{current_path}.{att_name}",
            )

    return res


def search_attribute_matching_type(
        obj: Any,
        type_rgx: str,
        re_flags=re.IGNORECASE,
        return_self: bool = True,  # test directly on input object and not only in its attributes
        deep_search: bool = True,  # Search inside a matching object
        super_class_search: bool = True,  # Search inside in super classes of the object
) -> List[Any]:
    return [
        val
        for path, val in search_attribute_matching_type_with_path(
            obj=obj,
            type_rgx=type_rgx,
            re_flags=re_flags,
            return_self=return_self,
            deep_search=deep_search,
            super_class_search=super_class_search,
        )
    ]


# Utility functions


def gen_uuid() -> str:
    return str(uuid_mod.uuid4())


def get_obj_uuid(obj: Any) -> str:
    return get_object_attribute_rgx(obj, "[Uu]u?id|UUID")


def get_obj_version(obj: Any) -> str:
    try:
        return get_object_attribute_no_verif(obj, "object_version")
    except AttributeError as e:
        try:
            return get_object_attribute_no_verif(obj, "version_string")
        except Exception:
            raise e


def get_direct_dor_list(obj: Any) -> List[Any]:
    return search_attribute_matching_type(obj, "DataObjectreference")


def get_data_object_type(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    return get_class_pkg(cls) + "." + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits)


def get_qualified_type_from_class(cls: Union[type, Any], print_dev_version=True):
    return (
            get_data_object_type(cls, print_dev_version, 2)
            .replace(".", "") + "." + get_object_type_for_file_path_from_class(cls)
    )


def get_content_type_from_class(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    if not isinstance(cls, type):
        cls = type(cls)

    if ".opc." in cls.__module__:
        if cls.__name__.lower() == "coreproperties":
            return "application/vnd.openxmlformats-package.core-properties+xml"
    else:
        return ("application/x-" + get_class_pkg(cls)
                + "+xml;version=" + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits) + ";type="
                + get_object_type_for_file_path_from_class(cls))

    print(f"@get_content_type_from_class not supported type : {cls}")
    return None


def get_object_type_for_file_path_from_class(cls) -> str:
    # obj_type = get_obj_type(cls)
    # pkg = get_class_pkg(cls)
    # if re.match(r"Obj[A-Z].*", obj_type) is not None and pkg == "resqml":
    #     return "obj_" + obj_type[3:]
    # return obj_type

    try:
        return cls.Meta.name  # to work with 3d transformed in 3D and Obj[A-Z] in obj_[A-Z]
    except AttributeError:
        pkg = get_class_pkg(cls)
        return get_obj_type(cls)


def now(time_zone=datetime.timezone(datetime.timedelta(hours=1), "UTC")) -> int:
    return int(datetime.datetime.timestamp(datetime.datetime.now(time_zone)))


def epoch(time_zone=datetime.timezone(datetime.timedelta(hours=1), "UTC")) -> int:
    return int(now(time_zone))


def date_to_epoch(date: str) -> int:
    """
    Transform a energyml date into an epoch datetime
    :return: int
    """
    return int(datetime.datetime.fromisoformat(date).timestamp())


def epoch_to_date(epoch_value: int, time_zone=datetime.timezone(datetime.timedelta(hours=1), "UTC")) -> str:
    date = datetime.datetime.fromtimestamp(epoch_value / 1e3, time_zone)
    return date.strftime("%Y-%m-%dT%H:%M:%S%z")


#  RANDOM


def get_class_from_simple_name(simple_name: str, energyml_module_context: Optional[List[str]] = []) -> type:
    try:
        return eval(simple_name)
    except NameError as e:
        for mod in energyml_module_context:
            try:
                exec(f"from {mod} import *")
                # required to be able to access to type in
                # typing values like "List[ObjectAlias]"
            except ModuleNotFoundError:
                pass
        return eval(simple_name)
        # if energyml_module_context is not None:
        #     for module_name in energyml_module_context:
        #         print(f"\ttry for {simple_name.replace(e.name, module_name + '.' + e.name)}")
        #         try:
        #             return eval(f"{simple_name.replace(e.name, module_name + '.' + e.name)}")
        #         except Exception as e2:
        #             print(e2)
        #             pass
        # raise e


def _gen_str_from_attribute_name(attribute_name: Optional[str]) -> str:
    attribute_name_lw = attribute_name.lower()
    if attribute_name is not None:
        if attribute_name_lw == "uuid" or attribute_name_lw == "uid":
            return gen_uuid()
        elif attribute_name_lw == "title":
            return "A random title (" + str(random_value_from_class(int)) + ")"
    return "A random str " + (f"[{attribute_name}] " if attribute_name is not None else "") + "(" + str(
        random_value_from_class(int)) + ")"


def random_value_from_class(cls: type):
    energyml_module_context = []
    if not is_primitive(cls):
        # import_related_module(cls.__module__)
        energyml_module_context = get_related_energyml_modules_name(cls)
    return _random_value_from_class(cls=cls, energyml_module_context=energyml_module_context, attribute_name=None)


def _random_value_from_class(cls: Any, energyml_module_context: List[str], attribute_name: Optional[str] = None):
    try:
        if isinstance(cls, str) or cls == str:
            return _gen_str_from_attribute_name(attribute_name)
        elif isinstance(cls, int) or cls == int:
            return random.randint(0, 10000)
        elif isinstance(cls, float) or cls == float:
            return random.randint(0, 1000000) / 100.
        elif isinstance(cls, bool) or cls == bool:
            return random.randint(0, 1) == 1
        elif is_enum(cls):
            return cls[cls._member_names_[random.randint(0, len(cls._member_names_) - 1)]]
        elif isinstance(cls, typing.Union.__class__):
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value
            chosen_type = type_list[random.randint(0, len(type_list))]
            return _random_value_from_class(chosen_type, energyml_module_context, attribute_name)
        elif cls.__module__ == 'typing':
            nb_value_for_list = random.randint(2, 3)
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value

            if cls._name == "List":
                lst = []
                for i in range(nb_value_for_list):
                    chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                    lst.append(_random_value_from_class(chosen_type, energyml_module_context, attribute_name))
                return lst
            else:
                chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                return _random_value_from_class(chosen_type, energyml_module_context, attribute_name)
            # if cls._name != "List":
            #     print(f"{cls} {cls.__dict__}")
            #     exit(0)
        else:
            args = {}
            for k, v in get_class_fields(cls).items():
                # print(f"get_class_fields {k} : {v}")
                args[k] = _random_value_from_class(
                    cls=get_class_from_simple_name(simple_name=v.type, energyml_module_context=energyml_module_context),
                    energyml_module_context=energyml_module_context,
                    attribute_name=k)
            # print(f"init args {args}")
            if not isinstance(cls, type):
                cls = type(cls)
            return cls(**args)

    except Exception as e:
        print(f"exception on attribute '{attribute_name}' for class {cls} :")
        raise e

    print(f"Not supported random class {cls}")
    return None
