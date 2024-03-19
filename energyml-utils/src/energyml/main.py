from dataclasses import fields

from energyml.eml.v2_3.commonv2 import *
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    FaultInterpretation,
    ContactElement,
)

from src.energyml.utils.validation import (
    patterns_verification,
    dor_verification, validate_epc, correct_dor,
)
from utils.epc import *
from utils.introspection import *
from utils.manager import *
from utils.serialization import *
from utils.xml import *


fi_cit = Citation(
    title="An interpretation",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

fi = FaultInterpretation(
    citation=fi_cit,
    uuid=gen_uuid(),
    object_version="0",
)

tr_cit = Citation(
    title="",
    # title="test title",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

dor = DataObjectReference(
    uuid=fi.uuid,
    title="a DOR title",
    object_version="0",
    qualified_type="a wrong qualified type",
)

tr = TriangulatedSetRepresentation(
    citation=tr_cit,
    uuid=gen_uuid(),
    represented_object=dor,
)


def tests_0():
    print(list_energyml_modules())
    print(dict_energyml_modules())
    # print(get_all_energyml_classes())

    print(fields(Activity)[0].metadata)

    print(epoch_to_date(epoch()))
    print(date_to_epoch("2024-03-05T17:50:17.757+01:00"))
    print(epoch_to_date(date_to_epoch("2024-03-05T17:50:17.757+01:00")))

    print(serialize_xml(tr_cit))

    print(serialize_json(tr))
    print(tr.citation)
    print(get_obj_uuid(tr))
    print("path: ", gen_energyml_object_path(tr))

    print(dir(Citation))
    print(get_class_attributes(Citation))

    alist = ["a", "b", "c", "d"]
    adict = {"a": 10}

    print("==>", get_object_attribute(alist, "0"))
    print("==>", get_object_attribute(adict, "a"))
    print("==>", get_object_attribute(tr, "citation.title"))

    print(re.split(r"(?<!\\)\.+", "[Cc]itation.[Tt]it\.*"))
    print("==>", get_object_attribute_rgx(tr, "[Cc]itation.[Tt]it\.*"))

    # print("==>", type(cit), type(Citation))
    # print("==>", type(cit) == type, type(Citation) == type)
    # print("==>", isinstance(cit, type), isinstance(Citation, type))

    print(gen_uuid())
    print(re.match(r"Obj[A-Z].*", "ObjTriangulatedSetRepresentation"))
    print(re.match(r"Obj[A-Z].*", "TriangulatedSetRepresentation"))


def file_test():
    print(get_class_pkg_version(TriangulatedSetRepresentation))
    print(get_content_type_from_class(TriangulatedSetRepresentation))

    path = "D:/Geosiris/Github/energyml/#data/TriangulatedSetRepresentation_2_2.xml"

    xml_content = ""
    with open(path, "r") as f:
        xml_content = f.read()

    print(get_xml_encoding(xml_content))
    print(get_root_type(get_tree(xml_content)))
    print(get_root_namespace(get_tree(xml_content)))
    print(find_schema_version_in_element(get_tree(xml_content)))
    print(get_class_name_from_xml(get_tree(xml_content)))

    print(
        get_class_from_name(
            "energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation"
        )
    )

    print(read_energyml_xml_str(xml_content))
    print(read_energyml_xml_file(path))


def tests_content_type():
    print(REGEX_CONTENT_TYPE)

    print(
        parse_content_type(
            "application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"
        )
    )
    print(
        parse_content_type(
            "application/vnd.openxmlformats-package.core-properties+xml"
        ).group("domain")
    )

    print(
        get_class_from_content_type(
            "application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"
        )
    )
    print(
        "CT 201 : ",
        get_class_from_content_type(
            "application/x-resqml+xml;version=2.0;type=obj_HorizonInterpretation"
        ),
    )
    print(
        parse_content_type(
            "application/x-resqml+xml;version=2.0;type=obj_HorizonInterpretation"
        )
    )

    print(
        get_class_from_content_type(
            "application/vnd.openxmlformats-package.core-properties+xml"
        )
    )

    print(get_content_type_from_class(tr))
    print(get_qualified_type_from_class(tr))

    print(gen_energyml_object_path(tr, EpcExportVersion.EXPANDED))
    print(gen_energyml_object_path(tr))


def tests_epc():
    epc = Epc.read_file(
        "D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc"
    )
    print(serialize_json(epc.gen_opc_content_type()))
    print(epc)
    epc.export_file("D:/Geosiris/Github/energyml/energyml-python/test.epc")
    epc.export_version = EpcExportVersion.EXPANDED
    epc.export_file(
        "D:/Geosiris/Github/energyml/energyml-python/test_EXPANDED.epc"
    )

    epc201 = Epc.read_file(
        "D:/Geosiris/OSDU/manifestTranslation/#Data/VOLVE_STRUCT.epc"
    )
    print(epc201)

    print(f"NB errors {len(validate_epc(epc201))}")

    correct_dor(epc201.energyml_objects)

    err_after_correction = validate_epc(epc201)
    print(f"NB errors after correction {len(err_after_correction)}")

    for err in err_after_correction:
        print(err)


def tests_dor():
    import json

    epc = Epc.read_file(
        "D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc"
    )

    print(EPCRelsRelationshipType.DESTINATION_OBJECT.get_type())

    print(
        json.dumps(
            {
                k: [get_obj_uuid(x) for x in v]
                for k, v in get_reverse_dor_list(epc.energyml_objects).items()
            },
            indent=4,
        )
    )
    print(epc.compute_rels())


def test_verif():

    print(get_class_fields(tr))
    for err in patterns_verification(tr):
        print(err)

    print("DOR verif no fi")
    for err in dor_verification([tr]):
        print(err)

    print("DOR verif with fi")
    for err in dor_verification([tr, fi]):
        print(err)


def test_ast():
    import ast

    exp = ast.parse("Optional[Union[ExistenceKind, str]]", mode="eval")
    print(exp.body.__dict__)
    print(exp.body.value.__dict__)
    print(exp.body.slice.__dict__)
    print(tr.__class__.__dataclass_fields__["aliases"])
    print(tr.__class__.__dataclass_fields__["aliases"].default_factory())
    print(tr.__class__.__module__)
    print(get_class_pkg(tr))

    print(tr.__class__.__dict__)

    print(t_get_attribute_type(tr, "citation"))

    print(get_class_fields(tr))
    print(ast.parse("TriangulatedSetRepresentation"))
    print(eval("TriangulatedSetRepresentation"))
    print(eval("Optional[Union[ExistenceKind, str]]"))
    print(list(eval("Optional[Union[ExistenceKind, str]]").__args__))
    ll = list(eval("Optional[Union[ExistenceKind, str]]").__args__)
    ll.remove(type(None))
    if type(None) in ll:
        ll.remove(type(None))
    print(ll)
    print(list(eval("List[ObjectAlias]").__args__))
    print(random_value_from_class(tr))


def test_introspection():
    print(search_attribute_matching_type(tr, "int"))
    print(search_attribute_matching_type(tr, "float"))
    print(search_attribute_matching_type(tr, "list"))
    print(search_attribute_matching_type(tr, "str"))
    print(search_attribute_matching_type(tr, "^str$"))
    print(search_attribute_matching_type(tr, "Citation"))
    print(search_attribute_matching_type(tr, "DataObjectreference"))
    print(search_attribute_matching_type_with_path(tr, "DataObjectreference"))
    print(
        class_match_rgx(
            ContactElement, "DataObjectreference", super_class_search=False
        )
    )
    print(
        class_match_rgx(
            ContactElement, "DataObjectreference", super_class_search=True
        )
    )
    print(Enum in ExistenceKind.__bases__)
    print(Enum in TriangulatedSetRepresentation.__bases__)
    print(is_primitive(int))
    print(is_primitive(str))
    print(is_primitive(TriangulatedSetRepresentation))
    print(is_primitive(Citation))
    print(is_primitive(ExistenceKind))
    print(ExistenceKind.__bases__)
    print(Enum in ExistenceKind.__bases__)
    print(get_class_fields(tr))
    print(list(get_class_attributes(tr)))
    print(get_class_fields(tr)["citation"])

    print(EPCRelsRelationshipType._member_names_)
    print(EPCRelsRelationshipType['DESTINATION_OBJECT'].value)
    print(random_value_from_class(EPCRelsRelationshipType))
    print(random_value_from_class(EPCRelsRelationshipType))
    print(TriangulatedSetRepresentation.__dataclass_params__)

    # print(random_value_from_class(int))
    print(serialize_xml(random_value_from_class(TriangulatedSetRepresentation)))
    # print(serialize_json(random_value_from_class(TriangulatedSetRepresentation)))


if __name__ == "__main__":
    # tests_0()
    # ast_test()
    # tests_content_type()

    tests_epc()
    # tests_dor()
    # test_verif()
    # test_ast()
    # test_introspection()
