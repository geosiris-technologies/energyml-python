from src.energyml.utils.serialization import read_energyml_xml_bytes, read_energyml_json_bytes, read_energyml_json_str


def read_json0():
    filePath = "../rc/resqml20.obj_Grid2dRepresentation_7194be4d-169d-420c-98a5-d3ec4671f0cc.json"
    with open(filePath, "r") as f:
        print(read_energyml_json_str(f.read()))


if __name__ == "__main__":
    read_json0()
