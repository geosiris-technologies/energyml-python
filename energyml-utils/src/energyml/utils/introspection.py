# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
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

from src.energyml.utils.manager import get_class_pkg, get_class_pkg_version, RELATED_MODULES, \
    get_related_energyml_modules_name, get_sub_classes, get_classes_matching_name
from src.energyml.utils.xml import parse_content_type, ENERGYML_NAMESPACES


primitives = (bool, str, int, float, type(None))


def is_enum(cls: Union[type, Any]):
    """
    Returns True if @cls is an Enum
    :param cls:
    :return:
    """
    if isinstance(cls, type):
        return Enum in cls.__bases__
    return is_enum(type(cls))


def is_primitive(cls: Union[type, Any]) -> bool:
    """
    Returns True if @cls is a primitiv type or extends Enum
    :param cls:
    :return: bool
    """
    if isinstance(cls, type):
        return cls in primitives or Enum in cls.__bases__
    return is_primitive(type(cls))


def is_abstract(cls: Union[type, Any]) -> bool:
    """
    Returns True if @cls is an abstract class
    :param cls:
    :return: bool
    """
    if isinstance(cls, type):
        return not is_primitive(cls) and (cls.__name__.startswith("Abstract") or (hasattr(cls, "__dataclass_fields__") and len(cls.__dataclass_fields__)) == 0) and len(get_class_methods(cls)) == 0
    return is_abstract(type(cls))


def get_class_methods(cls: Union[type, Any]):
    return [func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("__") and not isinstance(getattr(cls, func), type)]


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
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    s = re.sub('__([A-Z])', r'_\1', s)
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()


def pascal_case(s: str) -> str:
    return snake_case(s).replace("_", " ").title().replace(" ", "")


def import_related_module(energyml_module_name: str) -> None:
    for related in RELATED_MODULES:
        if energyml_module_name in related:
            for m in related:
                try:
                    import_module(m)
                except Exception as e:
                    pass
                    # print(e)


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
    class_fields = get_class_fields(cls)

    # a search with the exact value
    for name, cf in class_fields.items():
        if (
                snake_case(name) == snake_case(attribute_name)
                or ('name' in cf.metadata and cf.metadata['name'] == attribute_name)
        ):
            return name

    # search regex after to avoid shadowing perfect match
    pattern = re.compile(attribute_name)
    for name, cf in class_fields.items():
        if pattern.match(name) or ('name' in cf.metadata and pattern.match(cf.metadata['name'])):
            return name

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
    Example : [Cc]itation.[Tt]it\\.*
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
    if real_attrib_name is not None:
        value = get_object_attribute_no_verif(obj, real_attrib_name)

        if len(attrib_list) > 1:
            return get_object_attribute_rgx(
                value, attr_dot_path_rgx[len(current_attrib_name) + 1:]
            )
        else:
            return value
    return None


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
                super_class_search=super_class_search,
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
                super_class_search=super_class_search,
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
                super_class_search=super_class_search,
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


def search_attribute_matching_name_with_path(
        obj: Any,
        name_rgx: str,
        re_flags=re.IGNORECASE,
        deep_search: bool = True,  # Search inside a matching object
        current_path: str = "",
) -> List[Tuple[str, Any]]:
    """
    Returns a list of tuple (path, value) for each sub attribute with type matching param "name_rgx".
    The path is a dot-version like ".Citation.Title"
    :param obj:
    :param name_rgx:
    :param re_flags:
    :param deep_search:
    :param current_path:
    :return:
    """
    res = []
    if isinstance(obj, list):
        cpt = 0
        for s_o in obj:
            match = re.match(name_rgx, str(cpt))
            if match is not None:
                res.append((f"{current_path}.{match}", get_object_attribute_no_verif(obj, match.group(0))))
            res = res + search_attribute_matching_name_with_path(
                obj=s_o,
                name_rgx=name_rgx,
                re_flags=re_flags,
                deep_search=deep_search,
                current_path=f"{current_path}.{cpt}",
            )
            cpt = cpt + 1
    elif isinstance(obj, dict):
        for k, s_o in obj.items():
            match = re.match(name_rgx, k)
            if match is not None:
                res.append((f"{current_path}.{match}", get_object_attribute_no_verif(obj, match.group(0))))
            res = res + search_attribute_matching_name_with_path(
                obj=s_o,
                name_rgx=name_rgx,
                re_flags=re_flags,
                deep_search=deep_search,
                current_path=f"{current_path}.{k}",
            )
    elif not is_primitive(obj):
        match = get_matching_class_attribute_name(obj, name_rgx)
        if match is not None:
            res.append((f"{current_path}.{match}", get_object_attribute_no_verif(obj, match)))

        for att_name in get_class_attributes(obj):
            res = res + search_attribute_matching_name_with_path(
                obj=get_object_attribute_rgx(obj, att_name),
                name_rgx=name_rgx,
                re_flags=re_flags,
                deep_search=deep_search,
                current_path=f"{current_path}.{att_name}",
            )

    return res


def search_attribute_matching_name(
        obj: Any,
        name_rgx: str,
        re_flags=re.IGNORECASE,
        deep_search: bool = True,  # Search inside a matching object
) -> List[Any]:
    return [
        val
        for path, val in search_attribute_matching_name_with_path(
            obj=obj,
            name_rgx=name_rgx,
            re_flags=re_flags,
            deep_search=deep_search,
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


def get_class_from_simple_name(simple_name: str, energyml_module_context=None) -> type:
    if energyml_module_context is None:
        energyml_module_context = []
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


def _gen_str_from_attribute_name(attribute_name: Optional[str], _parent_class: Optional[type]=None) -> str:
    attribute_name_lw = attribute_name.lower()
    if attribute_name is not None:
        if attribute_name_lw == "uuid" or attribute_name_lw == "uid":
            return gen_uuid()
        elif attribute_name_lw == "title":
            return f"{_parent_class.__name__} title (" + str(random_value_from_class(int)) + ")"
        elif attribute_name_lw == "schema_version" and get_class_pkg_version(_parent_class) is not None:
            return get_class_pkg_version(_parent_class)
        elif re.match(r"\w*version$", attribute_name_lw):
            return str(random_value_from_class(int))
        elif re.match(r"\w*date_.*", attribute_name_lw):
            return epoch_to_date(epoch())
        elif re.match(r"path_in_.*", attribute_name_lw):
            return f"/FOLDER/{gen_uuid()}/a_patch{random.randint(0, 30)}"
        elif "mime_type" in attribute_name_lw and ("external" in _parent_class.__name__.lower() and "part" in _parent_class.__name__.lower()):
            return f"application/x-hdf5"
        elif "type" in attribute_name_lw:
            if attribute_name_lw.startswith("qualified"):
                return get_qualified_type_from_class(get_classes_matching_name(_parent_class, "Abstract")[0])
            if attribute_name_lw.startswith("content"):
                return get_content_type_from_class(get_classes_matching_name(_parent_class, "Abstract")[0])
    return "A random str " + (f"[{attribute_name}] " if attribute_name is not None else "") + "(" + str(
        random_value_from_class(int)) + ")"


def random_value_from_class(cls: type):
    energyml_module_context = []
    if not is_primitive(cls):
        # import_related_module(cls.__module__)
        energyml_module_context = get_related_energyml_modules_name(cls)
    return _random_value_from_class(cls=cls, energyml_module_context=energyml_module_context, attribute_name=None)


def _random_value_from_class(cls: Any, energyml_module_context: List[str], attribute_name: Optional[str] = None, _parent_class: Optional[type]=None):
    try:
        if isinstance(cls, str) or cls == str:
            return _gen_str_from_attribute_name(attribute_name, _parent_class)
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
            return _random_value_from_class(chosen_type, energyml_module_context, attribute_name, cls)
        elif cls.__module__ == 'typing':
            nb_value_for_list = random.randint(2, 3)
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value

            if cls._name == "List":
                lst = []
                for i in range(nb_value_for_list):
                    chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                    lst.append(_random_value_from_class(chosen_type, energyml_module_context, attribute_name, list))
                return lst
            else:
                chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                return _random_value_from_class(chosen_type, energyml_module_context, attribute_name, _parent_class)
        else:
            potential_classes = list(filter(lambda _c: not is_abstract(_c), [cls] + get_sub_classes(cls)))
            if len(potential_classes) > 0:
                chosen_type = potential_classes[random.randint(0, len(potential_classes) - 1)]
                args = {}
                for k, v in get_class_fields(chosen_type).items():
                    # print(f"get_class_fields {k} : {v}")
                    args[k] = _random_value_from_class(
                        cls=get_class_from_simple_name(simple_name=v.type, energyml_module_context=energyml_module_context),
                        energyml_module_context=energyml_module_context,
                        attribute_name=k,
                        _parent_class=chosen_type)

                if not isinstance(chosen_type, type):
                    chosen_type = type(chosen_type)
                return chosen_type(**args)

    except Exception as e:
        print(f"exception on attribute '{attribute_name}' for class {cls} :")
        raise e

    print(f"@_random_value_from_class Not supported object type generation {cls}")
    return None