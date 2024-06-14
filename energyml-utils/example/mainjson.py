import json

from src.energyml.utils.introspection import get_obj_identifier
from src.energyml.utils.serialization import read_energyml_json_str, \
    JSON_VERSION
from src.energyml.utils.serialization import to_json_dict


def read_json0():
    filePath = "../rc/resqml20.obj_Grid2dRepresentation_7194be4d-169d-420c-98a5-d3ec4671f0cc.json"
    with open(filePath, "r") as f:
        f_content = f.read()
        for o in read_energyml_json_str(f_content, JSON_VERSION.OSDU_OFFICIAL):
            print("> ", o)


# import energyml.resqml.v2_0_1.resqmlv2


def write_json0():
    filePath = "../rc/resqml20.obj_Grid2dRepresentation_7194be4d-169d-420c-98a5-d3ec4671f0cc.json"
    with open(filePath, "r") as f:
        f_content = f.read()
        objs = read_energyml_json_str(f_content, JSON_VERSION.OSDU_OFFICIAL)
        result = json.dumps(to_json_dict(objs[0], {get_obj_identifier(o): o for o in objs}), indent=4)

        print(json.dumps(json.loads(f_content), sort_keys=True))
        print(json.dumps(json.loads(result), sort_keys=True))

        assert json.dumps(json.loads(f_content), sort_keys=True) == json.dumps(json.loads(result), sort_keys=True)


if __name__ == "__main__":
    # read_json0()
    write_json0()
    # print(sys.modules["energyml.resqml.v2_0_1.resqmlv2"].__dict__)
    # for name, obj in inspect.getmembers(sys.modules["energyml.resqml.v2_0_1.resqmlv2"], inspect.isclass):
    #     print(obj)
