import re
from dataclasses import fields

from energyml.eml.v2_3.commonv2 import *
from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation, FaultInterpretation, ContactElement

from utils.manager import *
from utils.serialization import *
from utils.epc import *
from utils.introspection import *
from utils.xml import *

cit = Citation(
    title="test title",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    last_update=epoch_to_date(epoch()),
)

dor = DataObjectReference(
    uuid=gen_uuid(),
    title="a DOR title",
    object_version="0",
    qualified_type=get_qualified_type_from_class(FaultInterpretation)
)

tr = TriangulatedSetRepresentation(
    citation=cit,
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


    print(serialize_xml(cit))

    print(serialize_json(tr))
    print(tr.citation)
    print(get_obj_uuid(tr))
    print("path: ", gen_energyml_object_path(tr))

    print(dir(Citation))
    print(get_class_attributes(Citation))

    alist = ["a", "b", "c", "d"]
    adict = {
        'a': 10
    }

    print("==>", get_object_attribute(alist, '0'))
    print("==>", get_object_attribute(adict, 'a'))
    print("==>", get_object_attribute(tr, 'citation.title'))

    print(re.split(r"(?<!\\)\.+", "[Cc]itation.[Tt]it\.*"))
    print("==>", get_object_attribute_rgx(tr, "[Cc]itation.[Tt]it\.*"))

    # print("==>", type(cit), type(Citation))
    # print("==>", type(cit) == type, type(Citation) == type)
    # print("==>", isinstance(cit, type), isinstance(Citation, type))

    print(gen_uuid())
    print(re.match(r"Obj[A-Z].*", 'ObjTriangulatedSetRepresentation'))
    print(re.match(r"Obj[A-Z].*", 'TriangulatedSetRepresentation'))


def ast_test():
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


def file_test():
    print(get_class_pkg_version(TriangulatedSetRepresentation))
    print(get_content_type_from_class(TriangulatedSetRepresentation))

    path = "D:/Geosiris/Github/energyml/#data/TriangulatedSetRepresentation_2_2.xml"

    xml_content = ""
    with open(path, 'r') as f:
        xml_content = f.read()

    print(get_xml_encoding(xml_content))
    print(get_root_type(get_tree(xml_content)))
    print(get_root_namespace(get_tree(xml_content)))
    print(find_schema_version_in_element(get_tree(xml_content)))
    print(get_class_name_from_xml(get_tree(xml_content)))

    print(get_class_from_name("energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation"))

    print(read_energyml_xml_str(xml_content))
    print(read_energyml_xml_file(path))


def tests_content_type():
    print(REGEX_CONTENT_TYPE)

    print(parse_content_type("application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"))
    print(parse_content_type("application/vnd.openxmlformats-package.core-properties+xml").group("domain"))

    print(get_class_from_content_type("application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"))

    print(get_class_from_content_type("application/vnd.openxmlformats-package.core-properties+xml"))

    print(get_content_type_from_class(tr))
    print(get_qualified_type_from_class(tr))

    print(gen_energyml_object_path(tr, EpcExportVersion.EXPANDED))
    print(gen_energyml_object_path(tr))


def tests_epc():
    epc = Epc.read_file("D:/Geosiris/Github/energyml/#data/Volve_Horizons_and_Faults_Depth_originEQN_v2.2_colorised.epc")
    print(epc)

    print(serialize_json(epc.gen_opc_content_type()))


def test_introspection():
    print(search_attribute_matching_type(tr, "int"))
    print(search_attribute_matching_type(tr, "float"))
    print(search_attribute_matching_type(tr, "list"))
    print(search_attribute_matching_type(tr, "str"))
    print(search_attribute_matching_type(tr, "^str$"))
    print(search_attribute_matching_type(tr, "Citation"))
    print(search_attribute_matching_type(tr, "DataObjectreference"))
    print(class_match_rgx(ContactElement, "DataObjectreference", super_class_search=False))
    print(class_match_rgx(ContactElement, "DataObjectreference", super_class_search=True))


if __name__ == "__main__":
    # tests_0()
    # ast_test()
    # tests_content_type()
    # tests_content_type()
    # tests_epc()
    test_introspection()
