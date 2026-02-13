from energyml.utils.epc_utils import get_dor_uris_from_obj
from energyml.utils.introspection import get_obj_uri, search_attribute_matching_type_with_path
from energyml.utils.serialization import (
    serialize_xml,
    read_energyml_xml_str,
    read_energyml_xml_file,
    read_energyml_xml_bytes,
    read_energyml_json_str,
    read_energyml_json_bytes,
    JSON_VERSION,
)


def test_as_uri(xml_path: str):
    obj = read_energyml_xml_file(xml_path)

    # print(obj)

    for uri in get_dor_uris_from_obj(obj):
        print(uri)
    print("=" * 40)
    print(obj.category_lookup)
    print(get_obj_uri(obj.category_lookup))

    print("=" * 40)
    for p, o in search_attribute_matching_type_with_path(obj, "DataObjectreference"):
        print(f"{p}: {o} ({get_obj_uri(o)})\n")


if __name__ == "__main__":
    # test_as_uri("rc/ContinuousProperty_1d34249c-4c4f-4705-870e-b5dea9c0d78e.xml")
    test_as_uri("rc/DiscreteProperty.xml")
