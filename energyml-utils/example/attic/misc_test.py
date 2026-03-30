import json

from energyml.utils.epc import Epc
from energyml.utils.epc_utils import as_dor, get_dor_uris_from_obj
from energyml.utils.introspection import get_obj_uri, search_attribute_matching_type_with_path
from energyml.utils.serialization import (
    serialize_json,
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
        
        
def test_serialize_dor(xml_path: str):
    obj = read_energyml_xml_file(xml_path)
    dor = as_dor(obj)
    print(dor)
    json_dict = json.loads(serialize_json(dor))
    print(json_dict)
    
    print(get_obj_uri(json_dict))
    

def load_epc_22dev3(file_path: str):
    obj = Epc.read_file(file_path, recompute_rels=True)
    print(obj)
    
def dumps_repr_ctx(file_path: str, uuid: str):
    epc = Epc.read_file(file_path, recompute_rels=True)
    obj = epc.get_object_by_uuid(uuid)[0]
    
    if obj is None:
        raise ValueError(f"Object with UUID {uuid} not found in EPC file {file_path}")
    
    from energyml.utils.data.representation_context import RepresentationContext
    repr_ctx = RepresentationContext(obj, epc)
    
    if not isinstance(repr_ctx, RepresentationContext):
        raise ValueError("Expected a RepresentationContext object")
    
    print(repr_ctx.dump())


if __name__ == "__main__":
    # Run $env:PYTHONPATH="src" if it fails to be executed from the project root.
    # test_as_uri("rc/ContinuousProperty_1d34249c-4c4f-4705-870e-b5dea9c0d78e.xml")
    # test_as_uri("rc/DiscreteProperty.xml")
    # test_serialize_dor("rc/DiscreteProperty.xml")
    # load_epc_22dev3("D:/Geosiris/Clients/Egis/Documents/Data/4 MNT Trojena/MNT_Trojena_2024-03-18 _val.epc")
    dumps_repr_ctx("D:/Geosiris/Cloud/Resqml_Tools/2026-DATA/CARL_DGI/carl_volve_horizons.epc", "8a9833b9-46bf-4f4a-9a0a-adb77ee3b17a")

