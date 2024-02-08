import re
import importlib
import inspect
from typing import List
# from energyml.eml.v2_3

import pkgutil

import energyml

energyml_modules_names = ["eml", "prodml", "witsml", "resqml"]


def dict_energyml_modules():
    modules = {}

    energyml_module = importlib.import_module("energyml")
    print("> energyml")
    for mod in pkgutil.iter_modules(energyml_module.__path__):
        print(f"{mod.name}")
        if mod.name in energyml_modules_names:
            energyml_sub_module = importlib.import_module(f"energyml.{mod.name}")
            if mod.name not in modules:
                modules[mod.name] = []
            for sub_mod in pkgutil.iter_modules(energyml_sub_module.__path__):
                modules[mod.name].append(sub_mod.name)
                # modules[mod.name].append(re.sub(r"^\D*(?P<number>\d+(.\d+)*$)", r"\g<number>", sub_mod.name).replace("_", "."))
    return modules


def list_energyml_modules():
    try:
        energyml_module = importlib.import_module("energyml")
        modules = []
        for obj in pkgutil.iter_modules(energyml_module.__path__):
            # print(f"{obj.name}")
            if obj.name in energyml_modules_names:
                modules.append(obj.name)
        return modules
    except ModuleNotFoundError as e:
        return []


def list_classes(module_path: str) -> List:
    try:
        module = importlib.import_module(module_path)
        class_list = []
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                class_list.append(obj)
        return class_list
    except ModuleNotFoundError as e:
        print(f"Err : module {module_path} not found")
        return []


def get_all_energyml_classes() -> dict:
    result = {}
    for mod_name, versions in dict_energyml_modules().items():
        for version in versions:
            result = result | get_all_classes(mod_name, version)
    return result


def get_all_classes(module_name: str, version: str) -> dict:
    result = {}
    pkg_path = f"energyml.{module_name}.{version}"
    package = importlib.import_module(pkg_path)
    for _, modname, _ in pkgutil.walk_packages(
        path=getattr(package, "__path__"),
        prefix=package.__name__ + ".",
        onerror=lambda x: None,
    ):
        result[pkg_path] = []
        for classFound in list_classes(modname):
            try:
                result[pkg_path].append(classFound)
            except Exception:
                pass

    return result



# ProtocolDict = DefaultDict[str, MessageDict]
# def get_all__classes() -> ProtocolDict:
#     protocolDict: ProtocolDict = defaultdict(
#         lambda: defaultdict(type(ETPModel))
#     )
#     package = energyml
#     for _, modname, _ in pkgutil.walk_packages(
#         path=getattr(package, "__path__"),
#         prefix=package.__name__ + ".",
#         onerror=lambda x: None,
#     ):
#         for classFound in list_classes(modname):
#             try:
#                 schem = json.loads(avro_schema(classFound))
#                 protocolId = schem["protocol"]
#                 messageType = schem["messageType"]
#                 protocolDict[protocolId][messageType] = classFound
#             except Exception:
#                 pass
#     return protocolDict

