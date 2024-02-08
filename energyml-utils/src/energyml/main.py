import json
from dataclasses import fields

from energyml.eml.v2_3.commonv2 import *

from energyml_utils.utils.manager import (
    list_energyml_modules,
    dict_energyml_modules,
    get_all_energyml_classes
)

if __name__ == "__main__":
    print(list_energyml_modules())
    print(dict_energyml_modules())
    print(get_all_energyml_classes())

    print(fields(Activity)[0].metadata)
