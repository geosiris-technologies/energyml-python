# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

import logging

from src.energyml.utils.xml import *

CT_20 = "application/x-resqml+xml;version=2.0;type=obj_TriangulatedSetRepresentation"
CT_22 = "application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"
CT_22_DEV = "application/x-resqml+xml;version=2.2dev3;type=TriangulatedSetRepresentation"

QT_20 = "resqml20.obj_TriangulatedSetRepresentation"
QT_22 = "resqml22.TriangulatedSetRepresentation"
QT_22_DEV = "resqml22dev3.TriangulatedSetRepresentation"

# Following xml are not correct but are modified to make some test on the different ways to write attributes
# like the UUID that can be written (depending on the package) ["UUID", "Uuid", "Uid" ...]
tr_xml20 = """<?xml version="1.0" encoding="us-ascii"?>
<resqml:TriangulatedSetRepresentation 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2"
    xmlns:eml="http://www.energistics.org/energyml/data/commonv2"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    schemaVersion="2.0"
    uuid="3d2af068-bd16-4b53-932c-d1c2ff6913c3"
    xsi:type="resqml:obj_TriangulatedSetRepresentation"
>
    <eml:Citation xsi:type="eml:Citation">
        <eml:Title xsi:type="eml:DescriptionString">A title</eml:Title>
        <eml:Originator xsi:type="eml:NameString">An originator</eml:Originator>
        <eml:Creation xsi:type="xsd:dateTime">2020-01-08T13:41:24Z</eml:Creation>
        <eml:Format xsi:type="eml:DescriptionString">A description</eml:Format>
        <eml:Editor xsi:type="eml:NameString">A name</eml:Editor>
        <eml:LastUpdate xsi:type="xsd:dateTime">2020-01-08T13:41:25Z</eml:LastUpdate>
    </eml:Citation>
    <eml:TestBalise>
        <eml:Title xsi:type="eml:DescriptionString">A title</eml:Title>
    </eml:TestBalise>
</resqml:TriangulatedSetRepresentation>
"""

tr_xml22 = """<?xml version="1.0" encoding="windows-1250"?>
<resqml:TriangulatedSetRepresentation 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2" 
    xmlns:eml="http://www.energistics.org/energyml/data/commonv2" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    schemaVersion="Resqml 2.2"
    UUID="3d2af068-bd16-4b53-932c-d1c2ff6913c3"
    xsi:type="resqml:TriangulatedSetRepresentation"
>
    <eml:Citation xsi:type="eml:Citation">
        <eml:Title xsi:type="eml:DescriptionString">A title</eml:Title>
        <eml:Originator xsi:type="eml:NameString">An originator</eml:Originator>
        <eml:Creation xsi:type="xsd:dateTime">2020-01-08T13:41:24Z</eml:Creation>
        <eml:Format xsi:type="eml:DescriptionString">A description</eml:Format>
        <eml:Editor xsi:type="eml:NameString">A name</eml:Editor>
        <eml:LastUpdate xsi:type="xsd:dateTime">2020-01-08T13:41:25Z</eml:LastUpdate>
    </eml:Citation>
    <eml:TestBalise>
        <eml:Title xsi:type="eml:DescriptionString">A title</eml:Title>
    </eml:TestBalise>
</resqml:TriangulatedSetRepresentation>
"""

tr_xml22dev3 = """<?xml version="1.0" encoding="UTF-8"?>
<resqml:TriangulatedSetRepresentation 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2" 
    xmlns:eml="http://www.energistics.org/energyml/data/commonv2" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    schemaVersion="Resqml 2.2dev3"
    uid="3d2af068-bd16-4b53-932c-d1c2ff6913c3"
    xsi:type="resqml:TriangulatedSetRepresentation"
>
    <eml:Citation xsi:type="eml:Citation">
        <eml:Title xsi:type="eml:DescriptionString">A title</eml:Title>
        <eml:Originator xsi:type="eml:NameString">An originator</eml:Originator>
        <eml:Creation xsi:type="xsd:dateTime">2020-01-08T13:41:24Z</eml:Creation>
        <eml:Format xsi:type="eml:DescriptionString">A description</eml:Format>
        <eml:Editor xsi:type="eml:NameString">A name</eml:Editor>
        <eml:LastUpdate xsi:type="xsd:dateTime">2020-01-08T13:41:25Z</eml:LastUpdate>
    </eml:Citation>
    <eml:TestBalise>
        <eml:Title xsi:type="eml:DescriptionString">A title</eml:Title>
    </eml:TestBalise>
</resqml:TriangulatedSetRepresentation>
"""


def test_parse_content_type_20():
    match = parse_content_type(CT_20)
    assert match is not None
    assert match.group("media") == "application"
    assert match.group("domain") == "resqml"
    assert match.group("rawDomain") == "x-resqml+xml"
    assert match.group("domainVersion") == "2.0"
    assert match.group("versionNum") == "2.0"
    assert match.group("devNum") is None
    assert match.group("dev") is None
    assert match.group("type") == "obj_TriangulatedSetRepresentation"


def test_parse_content_type_22():
    match = parse_content_type(CT_22)
    logging.error(match.groupdict())
    assert match is not None
    assert match.group("media") == "application"
    assert match.group("domain") == "resqml"
    assert match.group("rawDomain") == "x-resqml+xml"
    assert match.group("domainVersion") == "2.2"
    assert match.group("versionNum") == "2.2"
    assert match.group("devNum") is None
    assert match.group("dev") is None
    assert match.group("type") == "TriangulatedSetRepresentation"


def test_parse_content_type_22_dev():
    match = parse_content_type(CT_22_DEV)
    logging.error(match.groupdict())
    assert match is not None
    assert match.group("media") == "application"
    assert match.group("domain") == "resqml"
    assert match.group("rawDomain") == "x-resqml+xml"
    assert match.group("domainVersion") == "2.2dev3"
    assert match.group("versionNum") == "2.2"
    assert match.group("devNum") == "3"
    assert match.group("dev") == "dev3"
    assert match.group("type") == "TriangulatedSetRepresentation"


def test_parse_qualified_type_20():
    match = parse_qualified_type(QT_20)
    assert match is not None
    assert match.group("domain") == "resqml"
    assert match.group("domainVersion") == "20"
    assert match.group("devNum") is None
    assert match.group("dev") is None
    assert match.group("type") == "obj_TriangulatedSetRepresentation"


def test_parse_qualified_type_22():
    match = parse_qualified_type(QT_22)
    logging.error(match.groupdict())
    assert match is not None
    assert match.group("domain") == "resqml"
    assert match.group("domainVersion") == "22"
    assert match.group("devNum") is None
    assert match.group("dev") is None
    assert match.group("type") == "TriangulatedSetRepresentation"


def test_parse_qualified_type_22_dev():
    match = parse_qualified_type(QT_22_DEV)
    logging.error(match.groupdict())
    assert match is not None
    assert match.group("domain") == "resqml"
    assert match.group("domainVersion") == "22dev3"
    assert match.group("devNum") == "3"
    assert match.group("dev") == "dev3"
    assert match.group("type") == "TriangulatedSetRepresentation"


def test_is_energyml_content_type():
    for d in ENERGYML_NAMESPACES_PACKAGE.keys():
        assert is_energyml_content_type(f"application/x-{d}+xml;version=2.0;type=obj_XXX")
    assert not is_energyml_content_type(f"application/x-randomValue+xml;version=2.0;type=obj_XXX")


def test_get_root_type_20():
    tree = get_tree(tr_xml20)
    assert get_root_type(tree) == "TriangulatedSetRepresentation"


def test_get_root_type_22dev3():
    tree = get_tree(tr_xml22dev3)
    assert get_root_type(tree) == "TriangulatedSetRepresentation"


def test_get_uuid_20():
    tree = get_tree(tr_xml20)
    assert get_uuid(tree) == "3d2af068-bd16-4b53-932c-d1c2ff6913c3"


def test_get_uuid_22():
    tree = get_tree(tr_xml22)
    assert get_uuid(tree) == "3d2af068-bd16-4b53-932c-d1c2ff6913c3"


def test_get_uuid_22dev3():
    tree = get_tree(tr_xml22dev3)
    assert get_uuid(tree) == "3d2af068-bd16-4b53-932c-d1c2ff6913c3"


def test_find_schema_version_in_element_20():
    tree = get_tree(tr_xml20)
    assert find_schema_version_in_element(tree) == "2.0"


def test_find_schema_version_in_element_22():
    tree = get_tree(tr_xml22)
    assert find_schema_version_in_element(tree) == "2.2"


def test_find_schema_version_in_element_22dev3():
    tree = get_tree(tr_xml22dev3)
    assert find_schema_version_in_element(tree) == "2.2-dev3"


def test_find_search_element_has_child_xpath():
    tree = get_tree(tr_xml22dev3)
    assert len(search_element_has_child_xpath(tree, "eml:Citation")) == 1
    assert len(search_element_has_child_xpath(tree, "eml:Title")) == 2


def test_get_xml_encoding():
    assert get_xml_encoding(tr_xml20) == "us-ascii"
    assert get_xml_encoding(tr_xml22) == "windows-1250"
    assert get_xml_encoding(tr_xml22dev3) == "UTF-8"
