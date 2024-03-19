import importlib
import inspect
import pkgutil
import re
from typing import List

REGEX_ENERGYML_MODULE_NAME = r"energyml\.(?P<pkg>.*)\.v(?P<version>(?P<versionNumber>\d+(_\d+)*)(_dev(?P<versionDev>.*))?)\..*"
REGEX_PROJECT_VERSION = r"(?P<n0>[\d]+)(.(?P<n1>[\d]+)(.(?P<n2>[\d]+))?)?"

ENERGYML_MODULES_NAMES = ["eml", "prodml", "witsml", "resqml"]


def dict_energyml_modules():
    modules = {}

    energyml_module = importlib.import_module("energyml")
    # print("> energyml")

    for mod in pkgutil.iter_modules(energyml_module.__path__):
        # print(f"{mod.name}")
        if mod.name in ENERGYML_MODULES_NAMES:
            energyml_sub_module = importlib.import_module(
                f"energyml.{mod.name}"
            )
            if mod.name not in modules:
                modules[mod.name] = []
            for sub_mod in pkgutil.iter_modules(energyml_sub_module.__path__):
                modules[mod.name].append(sub_mod.name)
                # modules[mod.name].append(re.sub(r"^\D*(?P<number>\d+(.\d+)*$)",
                # r"\g<number>", sub_mod.name).replace("_", "."))
    return modules


def list_energyml_modules():
    try:
        energyml_module = importlib.import_module("energyml")
        modules = []
        for obj in pkgutil.iter_modules(energyml_module.__path__):
            # print(f"{obj.name}")
            if obj.name in ENERGYML_MODULES_NAMES:
                modules.append(obj.name)
        return modules
    except ModuleNotFoundError:
        return []


def list_classes(module_path: str) -> List:
    try:
        module = importlib.import_module(module_path)
        class_list = []
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                class_list.append(obj)
        return class_list
    except ModuleNotFoundError:
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


def get_class_pkg(cls):
    try:
        p = re.compile(REGEX_ENERGYML_MODULE_NAME)
        m = p.search(cls.__module__)
        return m.group("pkg")
    except AttributeError as e:
        print(f"Exception to get class package for '{cls}'")
        raise e


def reshape_version(version: str, nb_digit: int) -> str:
    """
    Reshape a project version to have only specific number of digits. If 0 < nbDigit < 4 then the reshape is done,
    else, the original version is returned.
    Example : reshapeVersion("v2.0.1", 2) ==> "2.0" and reshapeVersion("version2.0.1.3.2.5", 4) ==> "version2.0.1.3.2.5"
    """
    p = re.compile(REGEX_PROJECT_VERSION)
    m = p.search(version)
    if m is not None:
        n0 = m.group("n0")
        n1 = m.group("n1")
        n2 = m.group("n2")
        if nb_digit == 1:
            return n0
        elif nb_digit == 2:
            return n0 + ("." + n1 if n1 is not None else "")
        elif nb_digit == 3:
            return n0 + (
                "." + n1 + ("." + n2 if n2 is not None else "")
                if n1 is not None
                else ""
            )

    return version


def get_class_pkg_version(
    cls, print_dev_version: bool = True, nb_max_version_digits: int = 2
):
    p = re.compile(REGEX_ENERGYML_MODULE_NAME)
    m = p.search(
        cls.__module__ if isinstance(cls, type) else type(cls).__module__
    )
    return reshape_version(m.group("versionNumber"), nb_max_version_digits) + (
        m.group("versionDev")
        if m.group("versionDev") is not None and print_dev_version
        else ""
    )


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
