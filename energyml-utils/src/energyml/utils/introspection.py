# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import json
import logging
import random
import re
import sys
import typing
from dataclasses import Field, field
from enum import Enum
from importlib import import_module
from types import ModuleType
from typing import Any, List, Optional, Union, Dict, Tuple

from .constants import (
    primitives,
    epoch_to_date,
    epoch,
    gen_uuid,
    snake_case,
    pascal_case,
    path_next_attribute,
)
from .manager import (
    get_class_pkg,
    get_class_pkg_version,
    RELATED_MODULES,
    get_related_energyml_modules_name,
    get_sub_classes,
    get_classes_matching_name,
    dict_energyml_modules,
)
from .uri import Uri, parse_uri
from .xml import parse_content_type, ENERGYML_NAMESPACES, parse_qualified_type


def is_enum(cls: Union[type, Any]):
    """
    Returns True if :param:`cls` is an Enum
    :param cls:
    :return:
    """
    if isinstance(cls, type):
        return Enum in cls.__bases__
    return is_enum(type(cls))


def is_primitive(cls: Union[type, Any]) -> bool:
    """
    Returns True if :param:`cls` is a primitiv type or extends Enum
    :param cls:
    :return: bool
    """
    if isinstance(cls, type):
        return cls in primitives or Enum in cls.__bases__
    return is_primitive(type(cls))


def is_abstract(cls: Union[type, Any]) -> bool:
    """
    Returns True if :param:`cls` is an abstract class
    :param cls:
    :return: bool
    """
    if isinstance(cls, type):
        return (
            not is_primitive(cls)
            and (
                cls.__name__.startswith("Abstract")
                or (hasattr(cls, "__dataclass_fields__") and len(cls.__dataclass_fields__)) == 0
            )
            and len(get_class_methods(cls)) == 0
        )
    return is_abstract(type(cls))


def get_module_classes_from_name(mod_name: str) -> List:
    return get_module_classes(sys.modules[mod_name])


def get_module_classes(mod: ModuleType) -> List:
    return inspect.getmembers(mod, inspect.isclass)


def find_class_in_module(module_name, class_name):
    try:
        return getattr(sys.modules[module_name], class_name)
    except:
        for cls_name, cls in get_module_classes_from_name(module_name):
            try:
                if cls_name == class_name or cls.Meta.name == class_name:
                    return cls
            except Exception as e:
                pass
    logging.error(f"Not Found : {module_name}; {class_name}")
    return None


def search_class_in_module_from_partial_name(module_name: str, class_partial_name: str) -> Optional[List[type]]:
    """
    Search a class in a module using a partial name.
    :param module_name: The name of the module to search in.
    :param class_partial_name: The partial name of the class to search for.
    :return: A list of classes that match the partial name.

    """
    try:
        module = import_module(module_name)
        classes = get_module_classes_from_name(module_name)
        matching_classes = [cls for cls_name, cls in classes if class_partial_name.lower() in cls_name.lower()]
        return matching_classes
    except ImportError as e:
        logging.error(f"Module '{module_name}' not found: {e}")
    return None


def get_class_methods(cls: Union[type, Any]) -> List[str]:
    """
    Returns the list of the methods names for a specific class.
    :param cls:
    :return:
    """
    return [
        func
        for func in dir(cls)
        if callable(getattr(cls, func)) and not func.startswith("__") and not isinstance(getattr(cls, func), type)
    ]


def get_class_from_name(class_name_and_module: str) -> Optional[type]:
    """
    Return a :class:`type` object matching with the name :param:`class_name_and_module`.
    :param class_name_and_module:
    :return:
    """
    module_name = class_name_and_module[: class_name_and_module.rindex(".")]
    last_ns_part = class_name_and_module[class_name_and_module.rindex(".") + 1 :]
    try:
        # Required to read "CustomData" on eml objects that may contain resqml values
        # ==> we need to import all modules related to the same version of the common
        import_related_module(module_name)
        # return getattr(sys.modules[module_name], last_ns_part)
        return find_class_in_module(module_name, last_ns_part)
    except AttributeError as e:
        # if "2d" in last_ns_part:
        #     logging.debug("replace 2D")
        #     return get_class_from_name(
        #         class_name_and_module.replace("2d", "2D")
        #     )
        # elif "3d" in last_ns_part:
        #     return get_class_from_name(
        #         class_name_and_module.replace("3d", "3D")
        #     )
        # elif last_ns_part[0].islower():
        #     return get_class_from_name(
        #         module_name + "." + last_ns_part[0].upper() + last_ns_part[1:]
        #     )
        # elif "2D" in last_ns_part or "3D" in last_ns_part:
        #     idx = -1
        #     logging.debug(class_name_and_module)
        #     try:
        #         idx = class_name_and_module.rindex("2D") + 2
        #     except:
        #         idx = class_name_and_module.rindex("3D") + 2
        #     if class_name_and_module[idx].isupper():
        #         reformated = (
        #                 class_name_and_module[:idx]
        #                 + class_name_and_module[idx].lower()
        #                 + class_name_and_module[idx + 1:]
        #         )
        #         logging.debug(f"reformated {reformated}")
        #         return get_class_from_name(reformated)
        # else:
        #     logging.debug(e)
        logging.error(e)
    except KeyError:
        logging.error(f"[ERR] module not found : '{module_name}'")
    return None


def get_energyml_module_dev_version(pkg: str, current_version: str):
    accessible_modules = dict_energyml_modules()
    if not current_version.startswith("v"):
        current_version = "v" + current_version

    current_version = current_version.replace("-", "_").replace(".", "_")
    res = []
    if pkg in accessible_modules:
        # logging.debug("\t", pkg, current_version)
        for am_pkg_version in accessible_modules[pkg]:
            if am_pkg_version != current_version and am_pkg_version.startswith(current_version):
                # logging.debug("\t\t", am_pkg_version)
                res.append(get_module_name(pkg, am_pkg_version))

    return res


def get_energyml_class_in_related_dev_pkg(cls: type):
    class_name = cls.__name__
    class_pkg = get_class_pkg(cls)
    class_pkg_version = get_class_pkg_version(cls)

    res = []

    for dev_module_name in get_energyml_module_dev_version(class_pkg, class_pkg_version):
        try:
            res.append(get_class_from_name(f"{dev_module_name}.{class_name}"))
        except Exception as e:
            logging.error(f"FAILED {dev_module_name}.{class_name}")
            logging.error(e)
            pass

    return res


def get_module_name_and_type_from_content_or_qualified_type(cqt: str) -> Tuple[str, str]:
    """
    Return a tuple (module_name, type) from a content-type or qualified-type string.
    """
    ct = None
    try:
        ct = parse_content_type(cqt)
    except AttributeError:
        pass
    if ct is None:
        try:
            ct = parse_qualified_type(cqt)
        except AttributeError:
            pass

    domain = ct.group("domain")
    if domain is None:
        # logging.debug(f"\tdomain {domain} xmlDomain {ct.group('xmlDomain')} ")
        domain = "opc"

    if domain == "opc":
        xml_domain = ct.group("xmlDomain")
        if "." in xml_domain:
            xml_domain = xml_domain[xml_domain.rindex(".") + 1 :]
        opc_type = pascal_case(xml_domain).replace("-", "")
        return ("energyml.opc.opc", opc_type)
    else:
        domain = ct.group("domain")
        obj_type = ct.group("type")
        if obj_type.lower().startswith("obj_"):  # for resqml201
            # obj_type = "Obj" + obj_type[4:]
            obj_type = obj_type[4:]
        version_num = str(ct.group("domainVersion")).replace(".", "_")
        if "_" not in version_num:
            version_num = re.sub(r"(\d)(\d)", r"\1_\2", version_num)
        if domain.lower() == "resqml" and version_num.startswith("2_0"):
            version_num = "2_0_1"

        return (get_module_name(domain, version_num), obj_type)


def get_class_from_qualified_type(qualified_type: str) -> Optional[type]:
    return get_class_from_content_type(qualified_type)


def get_class_from_content_type(content_type: str) -> Optional[type]:
    """
    Return a :class:`type` object matching with the content-type :param:`content_type`.
    :param content_type:
    :return:
    """
    module_name, object_type = get_module_name_and_type_from_content_or_qualified_type(content_type)
    return get_class_from_name(module_name + "." + object_type)


def get_module_name(domain: str, domain_version: str):
    ns = ENERGYML_NAMESPACES[domain]
    if not domain_version.startswith("v"):
        domain_version = "v" + domain_version
    return f"energyml.{domain}.{domain_version}.{ns[ns.rindex('/') + 1:]}"


def import_related_module(energyml_module_name: str) -> None:
    """
    Import related modules for a specific energyml module. (See. :const:`RELATED_MODULES`)
    :param energyml_module_name:
    :return:
    """
    for related in RELATED_MODULES:
        if energyml_module_name in related:
            for m in related:
                try:
                    import_module(m)
                except Exception as e:
                    pass
                    # logging.error(e)


def list_function_parameters_with_types(func, is_class_function: bool = False) -> Dict[str, Any]:
    """Retrieve parameter names and their types from a function

    Args:
        func (_type_): the function
        is_class_function (bool, optional): If True, remove the first argumen (self or cls). Defaults to False.

    Returns:
        _type_: A dict with parameter name as key and their type as value
    """

    code = func.__code__
    param_names = code.co_varnames[1 : code.co_argcount]  # Get parameter names
    annotations = func.__annotations__  # Get type hints

    # Map parameters to their type hints (if available)
    param_types = {param: annotations.get(param, "Unknown") for param in param_names}

    return param_types


def get_class_fields(cls: Union[type, Any]) -> Dict[str, Field]:
    """
    Return all class fields names, mapped to their :class:`Field` value.
    If a dict is given, this function is the identity
    :param cls:
    :return:
    """
    # for dict object, no change
    if isinstance(cls, dict):
        return cls
    if not isinstance(cls, type):  # if cls is an instance
        cls = type(cls)
    try:
        return cls.__dataclass_fields__
    except AttributeError:
        try:
            # print(list_function_parameters_with_types(cls.__new__, True))
            return list_function_parameters_with_types(cls.__new__, True)
        except AttributeError as e:
            # For not working types like proxy type for C++ binding
            res = {}
            for a_name, a_type in inspect.getmembers(cls):
                # print(f"{a_name} => {inspect.getmembers(a_type)}")
                if not a_name.startswith("_") and not callable(getattr(cls, a_name, None)):
                    res[a_name] = field()

            return res


def get_class_attributes(cls: Union[type, Any]) -> List[str]:
    """
    returns a list of attributes (not private ones)
    """
    # if not isinstance(cls, type):  # if cls is an instance
    #     cls = type(cls)
    # return list(filter(lambda a: not a.startswith("__"), dir(cls)))
    return list(get_class_fields(cls).keys())


def get_class_attribute_type(cls: Union[type, Any], attribute_name: str):
    fields = get_class_fields(cls)
    try:
        return fields[attribute_name].type
    except IndexError:
        for fn, ft in fields:
            _m = re.match(attribute_name, fn)
            if _m is not None:
                return ft.type

    return None


def get_matching_class_attribute_name(
    cls: Union[type, Any],
    attribute_name: str,
    re_flags=re.IGNORECASE,
) -> Optional[str]:
    """
    From an object and an attribute name, returns the correct attribute name of the class.
    Example : "ObjectVersion" --> object_version.
    This method doesn't only transform to snake case but search into the obj class attributes (or dict keys)
    """
    if isinstance(cls, dict):
        for name in cls.keys():
            if snake_case(name) == snake_case(attribute_name):
                return name
        pattern = re.compile(attribute_name, flags=re_flags)
        for name in cls.keys():
            if pattern.match(name):
                return name
    else:
        class_fields = get_class_fields(cls)
        try:
            # a search with the exact value
            for name, cf in class_fields.items():
                if snake_case(name) == snake_case(attribute_name) or (
                    hasattr(cf, "metadata") and "name" in cf.metadata and cf.metadata["name"] == attribute_name
                ):
                    return name

            # search regex after to avoid shadowing perfect match
            pattern = re.compile(attribute_name, flags=re_flags)
            for name, cf in class_fields.items():
                # logging.error(f"\t->{name} : {attribute_name} {pattern.match(name)} {('name' in cf.metadata and pattern.match(cf.metadata['name']))}")
                if pattern.match(name) or (
                    hasattr(cf, "metadata") and "name" in cf.metadata and pattern.match(cf.metadata["name"])
                ):
                    return name
        except Exception as e:
            logging.error(f"Failed to get attribute {attribute_name} from class {cls}")
            logging.error(e)

    return None


def get_object_attribute(obj: Any, attr_dot_path: str, force_snake_case=True) -> Any:
    """
    returns the value of an attribute given by a dot representation of its path in the object
    example "Citation.Title"

    :param obj:
    :param attr_dot_path:
    :param force_snake_case:
    :return:
    """
    current_attrib_name, path_next = path_next_attribute(attr_dot_path)

    if force_snake_case:
        current_attrib_name = snake_case(current_attrib_name)

    value = None
    if isinstance(obj, list):
        value = obj[int(current_attrib_name)]
    elif isinstance(obj, dict):
        value = obj.get(current_attrib_name, None)
    else:
        try:
            value = getattr(obj, current_attrib_name)
        except AttributeError:
            return None

    # if "." in attr_dot_path:
    #     return get_object_attribute(value, attr_dot_path[len(current_attrib_name) + 1 :])
    # print(f"OLD {obj}\n\t{current_attrib_name}\n\t{path_next}\n\t{value}")
    if path_next is not None:
        return get_object_attribute(value, path_next)
    else:
        return value


def create_default_value_for_type(cls: Any):
    if cls == str:
        return ""
    elif cls == int:
        return 0
    elif cls == float:
        return 0
    elif cls == bool:
        return False
    elif is_enum(cls):
        return cls[cls._member_names_[random.randint(0, len(cls._member_names_) - 1)]]
    elif isinstance(cls, typing.Union.__class__):
        type_list = list(cls.__args__)
        if type(None) in type_list:
            type_list.remove(type(None))  # we don't want to generate none value
        chosen_type = type_list[0]
        return create_default_value_for_type(chosen_type)
    elif cls.__module__ == "typing":
        type_list = list(cls.__args__)
        if type(None) in type_list:
            type_list.remove(type(None))  # we don't want to generate none value

        if cls._name == "List":
            nb_value_for_list = 1
            # On cree une valeur pour ne pas perdre le typage du dessous
            lst = []
            for i in range(nb_value_for_list):
                chosen_type = type_list[0]
                lst.append(create_default_value_for_type(chosen_type))
            return lst
        else:
            chosen_type = type_list[random.randint(0, len(type_list) - 1)]
            return create_default_value_for_type(chosen_type)
    else:
        potential_classes = list(
            filter(
                lambda _c: not is_abstract(_c),
                [cls] + get_sub_classes(cls),
            )
        )
        if len(potential_classes) > 0:
            chosen_type = potential_classes[random.randint(0, len(potential_classes) - 1)]
            if not isinstance(chosen_type, type):
                chosen_type = type(chosen_type)
            return chosen_type()


def get_object_attribute_or_create(
    obj: Any,
    attr_dot_path: str,
    force_snake_case=True,
    fn_create: typing.Callable = lambda o, a_path: create_default_value_for_type(
        get_class_from_simple_name(
            simple_name=get_class_attribute_type(o, a_path),
            energyml_module_context=get_related_energyml_modules_name(o),
        )
    ),
) -> Any:
    """
    returns the value of an attribute given by a dot representation of its path in the object
    example "Citation.Title"

    :param obj:
    :param attr_dot_path:
    :param force_snake_case:
    :return:
    """
    current_attrib_name, path_next = path_next_attribute(attr_dot_path)

    if force_snake_case:
        current_attrib_name = snake_case(current_attrib_name)

    value = None
    try:
        if isinstance(obj, list):
            value = obj[int(current_attrib_name)]
        elif isinstance(obj, dict):
            value = obj.get(current_attrib_name, None)
        else:
            value = getattr(obj, current_attrib_name)
    except Exception:
        pass

    if value is None:
        value = fn_create(obj, current_attrib_name)
        set_attribute_value(obj, current_attrib_name, value)

    if path_next is not None:
        return get_object_attribute(value, path_next)
    else:
        return value


def get_object_attribute_advanced(obj: Any, attr_dot_path: str) -> Any:
    """
    see @get_matching_class_attribute_name and @get_object_attribute
    """
    current_attrib_name = attr_dot_path

    if "." in attr_dot_path:
        current_attrib_name = attr_dot_path.split(".")[0]

    current_attrib_name = get_matching_class_attribute_name(obj, current_attrib_name)

    value = None
    if isinstance(obj, list):
        value = obj[int(current_attrib_name)]
    elif isinstance(obj, dict):
        value = obj[current_attrib_name]
    else:
        value = getattr(obj, current_attrib_name)

    if "." in attr_dot_path:
        return get_object_attribute_advanced(value, attr_dot_path[len(current_attrib_name) + 1 :])
    else:
        return value


def get_object_attribute_no_verif(obj: Any, attr_name: str, default: Optional[Any] = None) -> Any:
    """
    Return the value of the attribute named after param :param:`attr_name` without verification (may raise an exception
    if it doesn't exists).

    Note: attr_name="0" will work if :param:`obj` is of type :class:`List`
    :param obj:
    :param attr_name:
    :return:
    """
    if isinstance(obj, list):
        if int(attr_name) < len(obj):
            return obj[int(attr_name)] or default
        else:
            raise AttributeError(obj, name=attr_name)
    elif isinstance(obj, dict):
        if attr_name in obj:
            return obj.get(attr_name, default)
        else:
            raise AttributeError(obj, name=attr_name)
    else:
        return (
            getattr(obj, attr_name) or default
        )  # we did not used the "default" of getattr to keep raising AttributeError


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

    real_attrib_name = get_matching_class_attribute_name(obj, current_attrib_name)
    if real_attrib_name is not None:
        value = get_object_attribute_no_verif(obj, real_attrib_name)

        if len(attrib_list) > 1:
            return get_object_attribute_rgx(value, attr_dot_path_rgx[len(current_attrib_name) + 1 :])
        else:
            return value
    return None


def get_obj_type(obj: Any) -> str:
    """Return the type name of an object. If obj is already a :class:`type`, return its __name__"""
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


def is_dor(obj: any) -> bool:
    return (
        "dataobjectreference" in get_obj_type(obj).lower()
        or get_object_attribute(obj, "ContentType") is not None
        or get_object_attribute(obj, "QualifiedType") is not None
    )


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
        if return_self and class_match_rgx(obj, type_rgx, super_class_search, re_flags):
            res.append((current_path, obj))
            if not deep_search:
                return res

    if current_path is None:
        current_path = ""
    if len(current_path) > 0:
        current_path = current_path + "."

    if isinstance(obj, list):
        cpt = 0
        for s_o in obj:
            res = res + search_attribute_matching_type_with_path(
                obj=s_o,
                type_rgx=type_rgx,
                re_flags=re_flags,
                return_self=True,
                deep_search=deep_search,
                current_path=f"{current_path}{cpt}",
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
                current_path=f"{current_path}{k}",
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
                current_path=f"{current_path}{att_name}",
                super_class_search=super_class_search,
            )

    return res


def search_attribute_in_upper_matching_name(
    obj: Any,
    name_rgx: str,
    root_obj: Optional[Any] = None,
    re_flags=re.IGNORECASE,
    current_path: str = "",
) -> Optional[Any]:
    """
    See :func:`search_attribute_matching_name_with_path`. It only returns the value not the path
    :param obj:
    :param name_rgx:
    :param root_obj:
    :param re_flags:
    :param current_path:
    :return:
    """
    # print(f"Searching {name_rgx} in {obj} : {root_obj}")
    elt_list = search_attribute_matching_name(obj, name_rgx, search_in_sub_obj=False, deep_search=False)
    if elt_list is not None and len(elt_list) > 0:
        return elt_list

    if len(current_path) != 0:  # obj != root_obj:
        upper_path = current_path[: current_path.rindex(".")]
        # print(f"\t {upper_path} ")
        if len(upper_path) > 0:
            return search_attribute_in_upper_matching_name(
                obj=get_object_attribute(root_obj, upper_path),
                name_rgx=name_rgx,
                root_obj=root_obj,
                re_flags=re_flags,
                current_path=upper_path,
            )
        else:
            return search_attribute_in_upper_matching_name(
                obj=root_obj,
                name_rgx=name_rgx,
                root_obj=root_obj,
                re_flags=re_flags,
                current_path=upper_path,
            )

    return None


def search_attribute_matching_type(
    obj: Any,
    type_rgx: str,
    re_flags=re.IGNORECASE,
    return_self: bool = True,  # test directly on input object and not only in its attributes
    deep_search: bool = True,  # Search inside a matching object
    super_class_search: bool = True,  # Search inside in super classes of the object
) -> List[Any]:
    """
    See :func:`search_attribute_matching_type_with_path`. It only returns the value not the path
    :param obj:
    :param type_rgx:
    :param re_flags:
    :param return_self:
    :param deep_search:
    :param super_class_search:
    :return:
    """
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
    current_path: str = "",
    deep_search: bool = True,  # Search inside a matching object
    search_in_sub_obj: bool = True,  # Search in obj attributes
) -> List[Tuple[str, Any]]:
    """
    Returns a list of tuple (path, value) for each sub attribute with type matching param "name_rgx".
        The path is a dot-version like ".Citation.Title"
    :param obj:
    :param name_rgx:
    :param re_flags:
    :param current_path:
    :param deep_search:
    :param search_in_sub_obj:
    :return:
    """
    # while name_rgx.startswith("."):
    #     name_rgx = name_rgx[1:]
    # current_match = name_rgx
    # next_match = current_match
    # if "." in current_match:
    #     attrib_list = re.split(r"(?<!\\)\.+", name_rgx)
    #     current_match = attrib_list[0]
    #     next_match = ".".join(attrib_list[1:])
    current_match, next_match = path_next_attribute(name_rgx)
    res = []

    if current_path is None:
        current_path = ""
    if len(current_path) > 0:
        current_path = current_path + "."

    match_path_and_obj = []
    not_match_path_and_obj = []
    if isinstance(obj, list):
        cpt = 0
        for s_o in obj:
            match = re.match(current_match.replace("\\.", "."), str(cpt), flags=re_flags)
            if match is not None:
                match_value = match.group(0)
                match_path_and_obj.append((f"{current_path}{cpt}", s_o))
            else:
                not_match_path_and_obj.append((f"{current_path}{cpt}", s_o))
            cpt = cpt + 1
    elif isinstance(obj, dict):
        for k, s_o in obj.items():
            match = re.match(current_match.replace("\\.", "."), k, flags=re_flags)
            if match is not None:
                match_value = match.group(0)
                match_path_and_obj.append((f"{current_path}{match_value}", s_o))
            else:
                not_match_path_and_obj.append((f"{current_path}{k}", s_o))
    elif not is_primitive(obj):
        match_value = get_matching_class_attribute_name(obj, current_match.replace("\\.", "."))
        if match_value is not None:
            match_path_and_obj.append(
                (
                    f"{current_path}{match_value}",
                    get_object_attribute_no_verif(obj, match_value),
                )
            )
        for att_name in get_class_attributes(obj):
            if att_name != match_value:
                not_match_path_and_obj.append(
                    (
                        f"{current_path}{att_name}",
                        get_object_attribute_no_verif(obj, att_name),
                    )
                )

    for matched_path, matched in match_path_and_obj:
        if next_match is not None:  # next_match is different, match is not final
            res = res + search_attribute_matching_name_with_path(
                obj=matched,
                name_rgx=next_match,
                re_flags=re_flags,
                current_path=matched_path,
                deep_search=False,  # no deep with partial
                search_in_sub_obj=False,  # no partial search in sub obj with no match
            )
        else:  # a complete match
            res.append((matched_path, matched))
            if deep_search:
                res = res + search_attribute_matching_name_with_path(
                    obj=matched,
                    name_rgx=name_rgx,
                    re_flags=re_flags,
                    current_path=matched_path,
                    deep_search=deep_search,  # no deep with partial
                    search_in_sub_obj=True,
                )
    if search_in_sub_obj:
        for not_matched_path, not_matched in not_match_path_and_obj:
            res = res + search_attribute_matching_name_with_path(
                obj=not_matched,
                name_rgx=name_rgx,
                re_flags=re_flags,
                current_path=not_matched_path,
                deep_search=deep_search,
                search_in_sub_obj=True,
            )

    return res


def search_attribute_matching_name(
    obj: Any,
    name_rgx: str,
    re_flags=re.IGNORECASE,
    deep_search: bool = True,  # Search inside a matching object
    search_in_sub_obj: bool = True,  # Search in obj attributes
) -> List[Any]:
    """
    See :func:`search_attribute_matching_name_with_path`. It only returns the value not the path

    :param obj:
    :param name_rgx:
    :param re_flags:
    :param deep_search:
    :param search_in_sub_obj:
    :return:
    """
    return [
        val
        for path, val in search_attribute_matching_name_with_path(
            obj=obj,
            name_rgx=name_rgx,
            re_flags=re_flags,
            deep_search=deep_search,
            search_in_sub_obj=search_in_sub_obj,
        )
    ]


def set_attribute_from_json_str(obj: Any, json_input: str) -> None:
    set_attribute_from_dict(obj=obj, values=json.loads(json_input))


def set_attribute_from_dict(obj: Any, values: Dict) -> None:
    for k, v in values.items():
        if isinstance(v, dict):
            set_attribute_from_dict(obj=get_object_attribute(obj=obj, attr_dot_path=k), values=v)
        elif isinstance(v, list):
            obj_list: List = get_object_attribute(obj=obj, attr_dot_path=k)
            while len(obj_list) > len(v):
                obj_list.pop()
            for i in range(len(v)):
                set_attribute_from_dict(obj=get_object_attribute(obj=obj_list, attr_dot_path="i"), values=v[i])
        else:
            set_attribute_from_path(obj=obj, attribute_path=k, value=v)


def set_attribute_from_path(obj: Any, attribute_path: str, value: Any):
    """
    Changes the value of a (sub)attribute.
    Example :
        data = {
            "a": {
                "b": [ "v_x", { "c": "v_old" } ]
            }
        }
        set_attribute_from_path(data, "a.b.1.c", "v_new")

        # result is :

        data == {
            "a": {
                "b": [ "v_x", { "c": "v_new" } ]
            }
        }

    :param obj:
    :param attribute_path:
    :param value:
    :return:
    """
    upper = obj
    current_attrib_name, path_next = path_next_attribute(attribute_path)
    if path_next is not None:
        set_attribute_from_path(
            get_object_attribute(
                obj,
                current_attrib_name,
            ),
            path_next,
            value,
        )
    else:
        current_attrib_real_name = get_matching_class_attribute_name(upper, current_attrib_name)
        created = False
        if current_attrib_real_name is not None:
            attrib_class = get_obj_attribute_class(upper, current_attrib_real_name)
            if attrib_class is not None and is_enum(attrib_class):
                created = True
                val_snake = snake_case(value)
                setattr(
                    upper,
                    current_attrib_real_name,
                    list(
                        filter(
                            lambda ev: snake_case(ev) == val_snake,
                            attrib_class._member_names_,
                        )
                    )[0],
                )
        if not created:  # If previous test failed, the attribute did not exist in the object, we create it
            if isinstance(upper, dict):
                upper[current_attrib_name] = value
            else:
                setattr(upper, current_attrib_name, value)


def set_attribute_value(obj: any, attribute_name_rgx, value: Any):
    copy_attributes(obj_in={attribute_name_rgx: value}, obj_out=obj, ignore_case=True)


def copy_attributes(
    obj_in: any,
    obj_out: Any,
    only_existing_attributes: bool = True,
    ignore_case: bool = True,
):
    in_att_list = get_class_attributes(obj_in)
    for k_in in in_att_list:
        p_list = search_attribute_matching_name_with_path(
            obj=obj_out,
            name_rgx=k_in,
            re_flags=re.IGNORECASE if ignore_case else 0,
            deep_search=False,
            search_in_sub_obj=False,
        )
        path = None
        if p_list is not None and len(p_list) > 0:
            path, _ = p_list[0]
        if not only_existing_attributes or path is not None:
            set_attribute_from_path(
                obj_out,
                path or k_in,
                get_object_attribute(obj_in, k_in, False),
            )


# Utility functions


def get_obj_uuid(obj: Any) -> str:
    """
    Return the object uuid (attribute must match the following regex : "[Uu]u?id|UUID").
    :param obj:
    :return:
    """
    return get_object_attribute_rgx(obj, "[Uu]u?id|UUID")


def get_obj_version(obj: Any) -> str:
    """
    Return the object version (check for "object_version" or "version_string" attribute).
    :param obj:
    :return:
    """
    try:
        return get_object_attribute_no_verif(obj, "object_version")
    except AttributeError as e:
        try:
            return get_object_attribute_no_verif(obj, "version_string")
        except Exception:
            logging.error(f"Error with {type(obj)}")
            return None
            # raise e


def get_obj_pkg_pkgv_type_uuid_version(
    obj: Any,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    return from an energyml object or a DOR a tuple :
        - package : e.g. resqml|eml|witsml|prodml
        - package version : e.g. 20
        - type : e.g. obj_TriangulatedSetRepresentation
        - uuid
        - object version
    :param obj:
    :return:
    """
    pkg: Optional[str] = get_class_pkg(obj)
    pkg_v: Optional[str] = get_class_pkg_version(obj)
    obj_type: Optional[str] = get_object_type_for_file_path_from_class(obj)
    obj_uuid = get_obj_uuid(obj)
    obj_version = get_obj_version(obj)

    ct = None
    try:
        ct = get_object_attribute_no_verif(obj, "content_type")
    except:
        pass

    if ct is not None:
        ct_match = parse_content_type(ct)
        logging.debug("ct : %S", ct_match)
        if ct_match is not None:
            pkg = ct_match.group("domain")
            pkg_v = ct_match.group("domainVersion")
            obj_type = ct_match.group("type")
    else:
        try:
            qt = get_object_attribute_no_verif(obj, "qualified_type")
            qt_match = parse_qualified_type(qt)
            logging.debug("qt : %s %s", qt, obj.__dict__, qt_match)
            if qt_match is not None:
                pkg = qt_match.group("domain")
                pkg_v = qt_match.group("domainVersion")
                obj_type = qt_match.group("type")
        except:
            pass

    # flattening version
    if pkg_v is not None:
        pkg_v = pkg_v.replace(".", "")

    return pkg, pkg_v, obj_type, obj_uuid, obj_version


def get_obj_identifier(obj: Any) -> str:
    """
    Generates an objet identifier as : 'OBJ_UUID.OBJ_VERSION'
    If the object version is None, the result is 'OBJ_UUID.'
    :param obj:
    :return: str
    """
    obj_obj_version = get_obj_version(obj)
    if obj_obj_version is None:
        obj_obj_version = ""
    obj_uuid = get_obj_uuid(obj)
    return f"{obj_uuid}.{obj_obj_version}"


def get_obj_uri(obj: Any, dataspace: Optional[str] = None) -> Uri:
    """
    Generates an objet etp Uri from an objet or a DOR
    :param obj:
    :param dataspace: the etp dataspace
    :return: str
    """
    (
        domain,
        domain_version,
        object_type,
        obj_uuid,
        obj_version,
    ) = get_obj_pkg_pkgv_type_uuid_version(obj)

    return Uri(
        dataspace=dataspace,
        domain=domain,
        domain_version=domain_version,
        object_type=object_type,
        uuid=obj_uuid,
        version=obj_version,
    )


def get_direct_dor_list(obj: Any) -> List[Any]:
    """
    Search all sub attribute of type "DataObjectreference".
    :param obj:
    :return:
    """
    return search_attribute_matching_type(obj, "DataObjectreference")


def get_obj_usable_class(o: Any) -> Optional[type]:
    """Used only for resqml201 that has classes Obj_TriangulatedSetRepresentation and TriangulatedSetRepresentation for example.
    This function will return Obj_TriangulatedSetRepresentation class
    """

    if o is not None:
        if not isinstance(o, type):
            o = type(o)
        if isinstance(o, type):
            if o.__bases__ is not None:
                for bc in o.__bases__:
                    # print(bc)
                    if bc.__name__.lower() == f"obj{get_obj_type(o).lower()}":
                        return bc
        return o if isinstance(o, type) else None
    return None


def as_obj_prefixed_class_if_possible(o: Any) -> Any:
    """Used only for resqml201 that has classes Obj_TriangulatedSetRepresentation and TriangulatedSetRepresentation for example.
    This function will return an instance of Obj_TriangulatedSetRepresentation if possible
    """
    if o is not None:
        if not isinstance(o, type):
            o_type = type(o)
            if o_type.__bases__ is not None:
                for bc in o_type.__bases__:
                    # print(bc)
                    if bc.__name__.lower() == f"obj{get_obj_type(o_type).lower()}":
                        try:
                            return bc(**o.__dict__)
                        except Exception as e:
                            logging.error(f"Failed to convert {o} to {bc}")
                            logging.error(e)
                            return o
        return o
    return None


def get_data_object_type(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    return get_class_pkg(cls) + "." + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits)


def get_qualified_type_from_class(cls: Union[type, Any], print_dev_version=True):
    return (
        get_data_object_type(cls, print_dev_version, 2).replace(".", "")
        + "."
        + get_object_type_for_file_path_from_class(cls)
    )


def get_object_uri(obj: any, dataspace: Optional[str] = None) -> Optional[Uri]:
    """Returns an ETP URI"""
    return parse_uri(f"eml:///dataspace('{dataspace or ''}')/{get_qualified_type_from_class(obj)}({get_obj_uuid(obj)})")


def dor_to_uris(dor: Any, dataspace: Optional[str] = None) -> Optional[Uri]:
    """
    Transform a DOR into an etp uri
    """
    result = None
    try:
        value = get_object_attribute_no_verif(dor, "qualified_type")
        result = parse_qualified_type(value)
    except Exception as e:
        print(e)
        try:
            value = get_object_attribute_no_verif(dor, "content_type")
            result = parse_content_type(value)
        except Exception as e2:
            print(e2)

    if result is None:
        return None

    return Uri(
        dataspace=dataspace,
        domain=result.group("domain"),
        domain_version=result.group("domainVersion"),
        object_type=result.group("type"),
        uuid=dor.uuid,
        version=dor.object_version,
    )


def get_content_type_from_class(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    if not isinstance(cls, type):
        cls = type(cls)

    if ".opc." in cls.__module__:
        if cls.__name__.lower() == "coreproperties":
            return "application/vnd.openxmlformats-package.core-properties+xml"
    else:
        return (
            "application/x-"
            + get_class_pkg(cls)
            + "+xml;version="
            + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits)
            + ";type="
            + get_object_type_for_file_path_from_class(cls)
        )

    logging.error(f"@get_content_type_from_class not supported type : {cls}")
    return None


def get_object_type_for_file_path_from_class(cls) -> str:
    if not isinstance(cls, type):
        cls = type(cls)
    classic_type = get_obj_type(cls)

    for parent_cls in cls.__bases__:
        try:
            if (
                classic_type.lower() in parent_cls.Meta.name.lower()
            ):  # to work with 3d transformed in 3D and Obj[A-Z] in obj_[A-Z]
                return parent_cls.Meta.name
        except AttributeError:
            pass

    return classic_type


def get_obj_attribute_class(
    cls: Any,
    attribute_name: Optional[str],
    random_for_typing: Optional[bool] = False,
    no_abstract: Optional[bool] = True,
):
    """
    Return an instantiable class for an attribute of :param cls:.
    If the attribute is defined with typing with multiple possibility (like tuple or union), the first one
    is selected or a random one (depending on the value of the :param random_for_typing:)
    :param cls:
    :param attribute_name:
    :param random_for_typing:
    :param no_abstract: if True, the returned typed will not be an abstract class
    :return:
    """
    chosen_type = None
    if cls is not None and attribute_name is not None:
        if isinstance(cls, dict):
            attribute_name_real = get_matching_class_attribute_name(cls, attribute_name)
            if attribute_name_real is not None:
                return type(cls[attribute_name_real])
        elif not isinstance(cls, type) and cls.__module__ != "typing":
            return get_obj_attribute_class(type(cls), attribute_name, random_for_typing)
        elif cls.__module__ == "typing":
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value

            if random_for_typing:
                chosen_type = type_list[random.randint(0, len(type_list) - 1)]
            else:
                chosen_type = type_list[0]
            return get_obj_attribute_class(chosen_type, None, random_for_typing)
        else:
            if attribute_name is not None and len(attribute_name) > 0:
                cls = get_class_from_simple_name(
                    simple_name=get_class_fields(cls)[attribute_name].type,
                    energyml_module_context=get_related_energyml_modules_name(cls),
                )
            potential_classes = [cls] + get_sub_classes(cls)
            if no_abstract:
                potential_classes = list(filter(lambda _c: not is_abstract(_c), potential_classes))
            if random_for_typing:
                chosen_type = potential_classes[random.randint(0, len(potential_classes) - 1)]
            else:
                chosen_type = potential_classes[0]
            #             print(f"chosen_type {chosen_type}")

            if cls.__module__ == "typing":
                return get_obj_attribute_class(chosen_type, None, random_for_typing)

    elif cls is not None:
        if isinstance(cls, typing.Union.__class__):
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value
            chosen_type = type_list[random.randint(0, len(type_list))]
        elif cls.__module__ == "typing":
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value

            if cls._name == "List":
                nb_value_for_list = random.randint(2, 3)
                lst = []
                for i in range(nb_value_for_list):
                    chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                    lst.append(
                        _random_value_from_class(
                            chosen_type,
                            get_related_energyml_modules_name(cls),
                            attribute_name,
                            list,
                        )
                    )
                return lst
            else:
                chosen_type = type_list[random.randint(0, len(type_list) - 1)]

    return chosen_type


#  RANDOM


def get_class_from_simple_name(simple_name: str, energyml_module_context=None) -> type:
    """
    Search for a :class:`type` depending on the simple class name :param:`simple_name`.
    :param simple_name:
    :param energyml_module_context:
    :return:
    """
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


def _gen_str_from_attribute_name(attribute_name: Optional[str], _parent_class: Optional[type] = None) -> str:
    """
    Generate a str from the attribute name. The result is not the same for an attribute named "Uuid" than for an
    attribute named "mime_type" for example.
    :param attribute_name:
    :param _parent_class:
    :return:
    """
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
        elif "mime_type" in attribute_name_lw and (
            "external" in _parent_class.__name__.lower() and "part" in _parent_class.__name__.lower()
        ):
            return f"application/x-hdf5"
        elif "type" in attribute_name_lw:
            if attribute_name_lw.startswith("qualified"):
                return get_qualified_type_from_class(get_classes_matching_name(_parent_class, "Abstract")[0])
            if attribute_name_lw.startswith("content"):
                return get_content_type_from_class(get_classes_matching_name(_parent_class, "Abstract")[0])
    return (
        "A random str "
        + (f"[{attribute_name}] " if attribute_name is not None else "")
        + "("
        + str(random_value_from_class(int))
        + ")"
    )


def random_value_from_class(cls: type):
    """
    Generate a random value for a :class:`type`. All attributes should be filled with random values.
    :param cls:
    :return:
    """
    energyml_module_context = []
    if not is_primitive(cls):
        # import_related_module(cls.__module__)
        energyml_module_context = get_related_energyml_modules_name(cls)
    if cls is not None:
        return _random_value_from_class(
            cls=cls,
            energyml_module_context=energyml_module_context,
            attribute_name=None,
        )
    else:
        return None


def _random_value_from_class(
    cls: Any,
    energyml_module_context: List[str],
    attribute_name: Optional[str] = None,
    _parent_class: Optional[type] = None,
):
    """
    Generate a random value for a :class:`type`. All attributes should be filled with random values.
    :param cls:
    :param energyml_module_context:
    :param attribute_name:
    :param _parent_class: the :class:`type`of the parent object
    :return:
    """

    try:
        if isinstance(cls, str) or cls == str:
            return _gen_str_from_attribute_name(attribute_name, _parent_class)
        elif isinstance(cls, int) or cls == int:
            return random.randint(0, 10000)
        elif isinstance(cls, float) or cls == float:
            return random.randint(0, 1000000) / 100.0
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
        elif cls.__module__ == "typing":
            type_list = list(cls.__args__)
            if type(None) in type_list:
                type_list.remove(type(None))  # we don't want to generate none value

            if cls._name == "List":
                nb_value_for_list = random.randint(2, 3)
                lst = []
                for i in range(nb_value_for_list):
                    chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                    lst.append(
                        _random_value_from_class(
                            chosen_type,
                            energyml_module_context,
                            attribute_name,
                            list,
                        )
                    )
                return lst
            else:
                chosen_type = type_list[random.randint(0, len(type_list) - 1)]
                return _random_value_from_class(
                    chosen_type,
                    energyml_module_context,
                    attribute_name,
                    _parent_class,
                )
        else:
            potential_classes = list(
                filter(
                    lambda _c: not is_abstract(_c),
                    [cls] + get_sub_classes(cls),
                )
            )
            if len(potential_classes) > 0:
                chosen_type = potential_classes[random.randint(0, len(potential_classes) - 1)]
                args = {}
                for k, v in get_class_fields(chosen_type).items():
                    # logging.debug(f"get_class_fields {k} : {v}, { isinstance(v, type)}, {v}")
                    args[k] = _random_value_from_class(
                        cls=(
                            get_class_from_simple_name(
                                simple_name=getattr(v, "type", v),
                                energyml_module_context=energyml_module_context,
                            )
                            if not isinstance(v, type) and not v.__module__ == "typing"
                            else v
                        ),
                        energyml_module_context=energyml_module_context,
                        attribute_name=k,
                        _parent_class=chosen_type,
                    )

                if not isinstance(chosen_type, type):
                    chosen_type = type(chosen_type)

                return chosen_type(**args)

    except Exception as e:
        logging.error(f"exception on attribute '{attribute_name}' for class {cls} :")
        raise e

    logging.error(f"@_random_value_from_class Not supported object type generation {cls}")
    return None


if __name__ == "__main__":

    from energyml.eml.v2_3.commonv2 import *
    from energyml.eml.v2_0.commonv2 import Citation as Cit201
    from energyml.resqml.v2_0_1.resqmlv2 import TriangulatedSetRepresentation as Tr20, ObjTriangulatedSetRepresentation
    from energyml.resqml.v2_2.resqmlv2 import (
        TriangulatedSetRepresentation,
        FaultInterpretation,
    )
    from .serialization import *

    fi_cit = Citation(
        title="An interpretation",
        originator="Valentin",
        creation=epoch_to_date(epoch()),
        editor="test",
        format="Geosiris",
        last_update=epoch_to_date(epoch()),
    )

    fi = FaultInterpretation(
        citation=fi_cit,
        uuid=gen_uuid(),
        object_version="0",
    )

    tr_cit = Citation(
        title="--",
        # title="test title",
        originator="Valentin",
        creation=epoch_to_date(epoch()),
        editor="test",
        format="Geosiris",
        last_update=epoch_to_date(epoch()),
    )

    tr_cit201 = Cit201(
        title="--",
        # title="test title",
        originator="Valentin",
        # creation=str(epoch_to_date(epoch()))
        editor="test",
        format="Geosiris",
        # last_update=str(epoch_to_date(epoch())),
    )
    dor = DataObjectReference(
        uuid=fi.uuid,
        title="a DOR title",
        object_version="0",
        qualified_type="a wrong qualified type",
    )
    tr = TriangulatedSetRepresentation(
        citation=tr_cit,
        uuid=gen_uuid(),
        represented_object=dor,
    )

    tr201 = Tr20(
        citation=tr_cit201,
        uuid=gen_uuid(),
    )
    tr201_bis = ObjTriangulatedSetRepresentation(
        citation=tr_cit201,
        uuid=gen_uuid(),
    )
    # print(get_obj_uri(tr201, "coucou"))

    print(get_obj_usable_class(tr))
    print(get_obj_usable_class(tr201))

    print(serialize_xml(tr201_bis))
    print(serialize_xml(tr201))
    print(serialize_json(tr201))
    print(serialize_xml(as_obj_prefixed_class_if_possible(tr201)))
    print("--> ", serialize_json(tr))
    # print(serialize_xml((get_usable_class(tr201))(tr201)))
