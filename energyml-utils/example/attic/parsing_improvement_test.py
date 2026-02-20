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
import os
import sys
import time
from typing import Optional

from energyml.utils.epc import Epc


def reexport_in_memory_par_read(filepath: str, output_folder: Optional[str] = None):
    is_opti = os.environ.get("__ENV__IMPROVEMENT__", "0") == "1"

    suffix = "opti" if is_opti else "std"
    if os.environ.get("__ENV__IMPROVEMENT_LXML__", "0") == "1":
        suffix += "_lxml"

    path_in_memory = filepath.replace(".epc", f"_parsing_imp_xml_{suffix}.epc")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        path_in_memory = f"{output_folder}/{path_in_memory.split('/')[-1]}"
    epc = Epc.read_file(epc_file_path=filepath, read_rels_from_files=False, read_parallel=True, recompute_rels=False)

    if os.path.exists(path_in_memory):
        os.remove(path_in_memory)
    epc.export_file(path_in_memory, parallel=True)


def time_test(f: callable, **kwargs):
    print(f"⏳ Testing {f.__name__}...")
    start = time.perf_counter()
    f(**kwargs)
    elapsed_inmem = time.perf_counter() - start
    # results.append(("In-Memory (Epc)", elapsed_inmem))
    print(f"   ✓ Completed in {elapsed_inmem:.3f}s\n")
    return ("In-Memory (Epc)", elapsed_inmem)


if __name__ == "__main__":
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
