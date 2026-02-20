"""
Test for parsing.

To test : edit _read_energyml_xml_bytes_as_class in serialization.py :

__ENV__IMPROVEMENT__ = "__ENV__IMPROVEMENT__"
"__ENV__IMPROVEMENT_LXML__" = ""__ENV__IMPROVEMENT_LXML__""

    if os.environ.get(__ENV__IMPROVEMENT__, "0") == "0":
        if os.environ.get("__ENV__IMPROVEMENT_LXML__", "0") == "1":
            parser = XmlParser(config=config, handler=LxmlEventHandler)
        else:
            parser = XmlParser(config=config)
    else:
        if os.environ.get("__ENV__IMPROVEMENT_LXML__", "0") == "1":
            parser = XmlParser(config=config, context=GLOBAL_XML_CONTEXT, handler=LxmlEventHandler)
        else:
            parser = XmlParser(config=config, context=GLOBAL_XML_CONTEXT)

"""

import logging
import operator
import os
import sys
import time
from typing import Optional

from energyml.utils.epc import Epc
from energyml.utils.introspection import (
    search_class_in_module_from_partial_name,
)
from energyml.utils.manager import get_related_energyml_modules_name
from energyml.utils.serialization import read_energyml_xml_file, serialize_json


def reexport_in_memory_par_read(filepath: str, output_folder: Optional[str] = None):
    is_opti = os.environ.get("__ENV__IMPROVEMENT__", "0") == "1"

    suffix = "opti" if is_opti else "std"
    if os.environ.get("__ENV__IMPROVEMENT_LXML__", "0") == "1":
        suffix += "_lxml"
    if os.environ.get("__ENV__IMPROVEMENT__GET_MEMBER__", "0") == "1":
        suffix += "_get_member"

    path_in_memory = filepath.replace(".epc", f"_parsing_imp_xml_{suffix}.epc")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        path_in_memory = f"{output_folder}/{path_in_memory.split('/')[-1]}"
    epc = Epc.read_file(epc_file_path=filepath, read_rels_from_files=False, read_parallel=True, recompute_rels=False)

    if os.path.exists(path_in_memory):
        os.remove(path_in_memory)
    epc.export_file(path_in_memory, parallel=True)


# ===================================


def time_test(f: callable, **kwargs):
    print(f" Testing {f.__name__}...")
    start = time.perf_counter()
    f(**kwargs)
    elapsed_inmem = time.perf_counter() - start
    # results.append(("In-Memory (Epc)", elapsed_inmem))
    print(f"    Completed in {elapsed_inmem:.3f}s\n")
    return ("In-Memory (Epc)", elapsed_inmem)


if __name__ == "__main__xmlcontext__":
    logging.basicConfig(level=logging.DEBUG)

    os.environ["__ENV__IMPROVEMENT__"] = "0"
    os.environ["__ENV__IMPROVEMENT_LXML__"] = "0"

    time_test(
        reexport_in_memory_par_read,
        filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/80wells_surf.epc",
        output_folder="results",
    )

    os.environ["__ENV__IMPROVEMENT__"] = "1"
    time_test(
        reexport_in_memory_par_read,
        filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/80wells_surf.epc",
        output_folder="results",
    )

    os.environ["__ENV__IMPROVEMENT__"] = "1"
    os.environ["__ENV__IMPROVEMENT_LXML__"] = "1"
    time_test(
        reexport_in_memory_par_read,
        filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/80wells_surf.epc",
        output_folder="results",
    )

if __name__ == "__main__":
    from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation

    print(TriangulatedSetRepresentation.__class__.__module__)
    print(TriangulatedSetRepresentation.__dataclass_fields__.keys())

    # logging.basicConfig(level=logging.DEBUG)

    # os.environ["__ENV__IMPROVEMENT__GET_MEMBER__"] = "0"

    time_test(
        reexport_in_memory_par_read,
        filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/80wells_surf.epc",
        output_folder="results",
    )

    # os.environ["__ENV__IMPROVEMENT__GET_MEMBER__"] = "1"
    # time_test(
    #     reexport_in_memory_par_read,
    #     filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/80wells_surf.epc",
    #     output_folder="results",
    # )
    # class Test:
    #     def __init__(self):
    #         self.geometry = 1

    #     def hello(self):
    #         print("Hello")


if __name__ == "__main__2":

    grid = read_energyml_xml_file("rc/Grid2dRepresentation_78bf01c0-d5bb-46d3-aa70-9cc4ee5c8230.xml")

    print(serialize_json(grid))

    # print(operator.attrgetter("geometry.points.zvalues.values.external_data_array_part.0")(grid))

    test_dict = {"geometry": {"points": {"zvalues": {"values": {"external_data_array_part": ["test"]}}}}}

    print(operator.attrgetter("geometry.points.zvalues.values.external_data_array_part.0")(test_dict))


if __name__ == "__main__":

    # print(is_abstract(Test))

    # print(len(get_module_classes("energyml.resqml.v2_2.resqmlv2")))
    # print(get_module_classes_old("energyml.resqml.v2_2.resqmlv2"))

    # tr = TriangulatedSetRepresentation()
    # print(get_class_methods(Epc))*

    # print(RELATED_MODULES_MAP)
    # print(get_related_energyml_modules_name("energyml.resqml.v2_2.resqmlv2"))

    print(len(search_class_in_module_from_partial_name("energyml.resqml.v2_2.resqmlv2", "Representation")))
