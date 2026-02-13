# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import importlib

from src.energyml.utils.epc import Epc


def import_modules():
    # import energyml.opc.opc
    # import energyml.resqml.v2_0_1.resqmlv2
    # import_modules()
    epc201 = Epc.read_file("D:/Geosiris/OSDU/manifestTranslation/#Data/VOLVE_STRUCT.epc")
    print(epc201)


if __name__ == "__main__":
    import ast

    mod = importlib.import_module("energyml.eml.v2_3.commonv2")
    oa = getattr(mod, "ObjectAlias")
    print(exec("from energyml.eml.v2_3.commonv2 import *"))
    print(eval("List[ObjectAlias]"))
    print(ast.parse("List[ObjectAlias]").body[0].value.value.__dict__)
