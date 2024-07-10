# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Any, Union

from lxml import etree as ETREE  # type: Any

from .constants import *


def get_pkg_from_namespace(namespace: str) -> Optional[str]:
    for (k, v) in ENERGYML_NAMESPACES_PACKAGE.items():
        if namespace in v:
            return k
    return None


def is_energyml_content_type(content_type: str) -> bool:
    ct = parse_content_type(content_type)
    domain = ct.group("domain")
    return domain is not None and domain in ENERGYML_NAMESPACES_PACKAGE.keys()


def get_root_namespace(tree: ETREE.Element) -> str:
    return tree.nsmap[tree.prefix]


def get_class_name_from_xml(tree: ETREE.Element) -> str:
    root_namespace = get_root_namespace(tree)
    pkg = get_pkg_from_namespace(root_namespace)
    if pkg is None:
        logging.error(f"No pkg found for elt {tree}")
    else:
        if pkg == "opc":
            return "energyml.opc.opc." + get_root_type(tree)
        else:
            schema_version = (
                (find_schema_version_in_element(tree) or "")
                .replace(".", "_")
                .replace("-", "_")
            )
            if pkg == "resqml" and schema_version == "2_0":
                schema_version = "2_0_1"

            return (
                "energyml."
                + pkg
                + ".v"
                + schema_version
                + "."
                + root_namespace[root_namespace.rindex("/") + 1:]
                + "."
                + get_root_type(tree)
            )


def get_xml_encoding(xml_content: str) -> Optional[str]:
    try:
        m = re.search(RGX_XML_HEADER, xml_content)
        return m.group("encoding")
    except AttributeError:
        return "utf-8"


def get_tree(xml_content: Union[bytes, str]) -> ETREE.Element:
    xml_bytes = xml_content
    if isinstance(xml_bytes, str):
        # return ETREE.fromstring(xml_content)
        encoding = get_xml_encoding(xml_content)
        xml_bytes = xml_content.encode(
            encoding=encoding.strip().lower()
            if encoding is not None
            else "utf-8"
        )

    return ETREE.parse(BytesIO(xml_bytes)).getroot()


def energyml_xpath(tree: ETREE.Element, xpath: str) -> Optional[list]:
    """A xpath research that knows energyml namespaces"""
    try:
        return ETREE.XPath(xpath, namespaces=ENERGYML_NAMESPACES)(tree)
    except TypeError:
        return None


def search_element_has_child_xpath(
    tree: ETREE.Element, child_name: str
) -> list:
    """
    Search elements that has a child named (xml tag) as 'child_name'.
    Warning : child_name must contain the namespace (see. ENERGYML_NAMESPACES)
    """
    return list(x for x in energyml_xpath(tree, f"//{child_name}/.."))


def get_uuid(tree: ETREE.Element) -> str:
    _uuids = tree.xpath("@uuid")
    if len(_uuids) <= 0:
        _uuids = tree.xpath("@UUID")
    if len(_uuids) <= 0:
        _uuids = tree.xpath("@Uuid")
    if len(_uuids) <= 0:
        _uuids = tree.xpath("@uid")
    if len(_uuids) <= 0:
        _uuids = tree.xpath("@Uid")
    if len(_uuids) <= 0:
        _uuids = tree.xpath("@UID")
    return _uuids[0]


def get_root_type(tree: ETREE.Element) -> str:
    """Returns the type (xml tag) of the element without the namespace"""
    return tree.xpath("local-name()")


def find_schema_version_in_element(tree: ETREE.ElementTree) -> str:
    """Find the "SchemaVersion" inside an xml content of a energyml file

    :param tree: An energyml xml file content.
    :type tree: bytes

    :returns: The SchemaVersion that contains only the version number. For example, if the xml
        file contains : SchemaVersion="Resqml 2.0.1"
            the result will be : "2.0.1"
    :rtype: str
    """
    _schema_version = tree.xpath("@schemaVersion")
    if _schema_version is None:
        _schema_version = tree.xpath("@SchemaVersion")

    if _schema_version is not None and len(_schema_version) > 0:
        match_version = re.search(r"\d+(\.\d+)*(dev\d+)?", _schema_version[0])
        if match_version is not None:
            return match_version.group(0).replace("dev", "-dev")
    return None
