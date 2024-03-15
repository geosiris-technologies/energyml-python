import re
from io import BytesIO
from typing import Optional, Any, Union

from lxml import etree as ETREE  # type: Any

ENERGYML_NAMESPACES = {
    "eml": "http://www.energistics.org/energyml/data/commonv2",
    "prodml": "http://www.energistics.org/energyml/data/prodmlv2",
    "witsml": "http://www.energistics.org/energyml/data/witsmlv2",
    "resqml": "http://www.energistics.org/energyml/data/resqmlv2",
}

ENERGYML_NAMESPACES_PACKAGE = {
    "eml": ["http://www.energistics.org/energyml/data/commonv2"],
    "prodml": ["http://www.energistics.org/energyml/data/prodmlv2"],
    "witsml": ["http://www.energistics.org/energyml/data/witsmlv2"],
    "resqml": ["http://www.energistics.org/energyml/data/resqmlv2"],
    "opc": [
        "http://schemas.openxmlformats.org/package/2006/content-types",
        "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
    ],
}

REGEX_UUID_NO_GRP = (
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
REGEX_UUID = r"(?P<uuid>" + REGEX_UUID_NO_GRP + ")"
REGEX_DOMAIN_VERSION = r"(?P<domainVersion>(?P<versionNum>([\d]+[\._])*\d)\s*(?P<dev>dev\s*(?P<devNum>[\d]+))?)"
REGEX_DOMAIN_VERSION_FLAT = r"(?P<domainVersion>(?P<versionNumFlat>([\d]+)*\d)\s*(?P<dev>dev\s*(?P<devNum>[\d]+))?)"


# ContentType
REGEX_MIME_TYPE_MEDIA = r"(?P<media>application|audio|font|example|image|message|model|multipart|text|video)"
REGEX_CT_ENERGYML_DOMAIN = r"(?P<energymlDomain>x-(?P<domain>[\w]+)\+xml)"
REGEX_CT_XML_DOMAIN = r"(?P<xmlRawDomain>(x\-)?(?P<xmlDomain>.+)\+xml)"
REGEX_CT_TOKEN_VERSION = r"version=" + REGEX_DOMAIN_VERSION
REGEX_CT_TOKEN_TYPE = r"type=(?P<type>[\w\_]+)"

REGEX_CONTENT_TYPE = (
        REGEX_MIME_TYPE_MEDIA + "/"
        + "(?P<rawDomain>(" + REGEX_CT_ENERGYML_DOMAIN + ")|(" + REGEX_CT_XML_DOMAIN + r")|([\w-]+\.?)+)"
        + "(;((" + REGEX_CT_TOKEN_VERSION + ")|(" + REGEX_CT_TOKEN_TYPE + ")))*"
)
REGEX_QUALIFIED_TYPE = (
        r"(?P<domain>[a-zA-Z]+)" + REGEX_DOMAIN_VERSION_FLAT + r"\.(?P<type>[\w_]+)"
)
# =========

REGEX_SCHEMA_VERSION = (
        r"(?P<name>[eE]ml|[cC]ommon|[rR]esqml|[wW]itsml|[pP]rodml)?\s*v?"
        + REGEX_DOMAIN_VERSION
        + r"\s*$"
)

REGEX_ENERGYML_FILE_NAME_OLD = r"(?P<type>[\w]+)_" + REGEX_UUID_NO_GRP + r"\.xml$"
REGEX_ENERGYML_FILE_NAME_NEW = (
        REGEX_UUID_NO_GRP + r"\.(?P<objectVersion>\d+(\.\d+)*)\.xml$"
)
REGEX_ENERGYML_FILE_NAME = (
    rf"^(.*/)?({REGEX_ENERGYML_FILE_NAME_OLD})|({REGEX_ENERGYML_FILE_NAME_NEW})"
)

REGEX_XML_HEADER = r"^\s*\<\?xml\s+((encoding\s*=\s*\"(?P<encoding>[^\"]+)\"|version\s*=\s*\"(?P<version>[^\"]+)\"|standalone\s*=\s*\"(?P<standalone>[^\"]+)\")\s+)+"


def get_pkg_from_namespace(namespace: str) -> Optional[str]:
    for (k, v) in ENERGYML_NAMESPACES_PACKAGE.items():
        if namespace in v:
            return k
    return None


def is_energyml_content_type(content_type: str) -> bool:
    ct = parse_content_type(content_type)
    return ct.group("domain") is not None


def get_root_namespace(tree: ETREE.Element) -> str:
    return tree.nsmap[tree.prefix]


def get_class_name_from_xml(tree: ETREE.Element) -> str:
    root_namespace = get_root_namespace(tree)
    pkg = get_pkg_from_namespace(root_namespace)
    if pkg is None:
        print(f"No pkg found for elt {tree}")
    else:
        if pkg == "opc":
            return "energyml.opc.opc." + get_root_type(tree)
        else:
            return ("energyml." + pkg
                    + ".v" + find_schema_version_in_element(tree).replace(".", "_").replace("-", "_")
                    + "."
                    + root_namespace[root_namespace.rindex("/") + 1:]
                    + "." + get_root_type(tree)
                    )


def get_xml_encoding(xml_content: str) -> Optional[str]:
    try:
        m = re.search(REGEX_XML_HEADER, xml_content)
        return m.group("encoding")
    except AttributeError:
        return "utf-8"


def get_tree(xml_content: Union[bytes, str]) -> ETREE.Element:
    xml_bytes = xml_content
    if isinstance(xml_bytes, str):
        xml_bytes = xml_content.encode(encoding=get_xml_encoding(xml_content).strip().lower())

    return ETREE.parse(BytesIO(xml_bytes)).getroot()


def energyml_xpath(tree: ETREE.Element, xpath: str) -> Optional[list]:
    """A xpath research that knows energyml namespaces"""
    try:
        return ETREE.XPath(xpath, namespaces=ENERGYML_NAMESPACES)(tree)
    except TypeError:
        return None


def search_element_has_child_xpath(tree: ETREE.Element, child_name: str) -> list:
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
        _uuids = tree.xpath("@uid")
    if len(_uuids) <= 0:
        _uuids = tree.xpath("@UID")
    return _uuids[0]


def get_root_type(tree: ETREE.Element) -> str:
    """ Returns the type (xml tag) of the element without the namespace """
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

    if _schema_version is not None:
        match_version = re.search(r"\d+(\.\d+)*", _schema_version[0])
        if match_version is not None:
            return match_version.group(0)
    return ""


def parse_content_type(ct: str):
    return re.search(REGEX_CONTENT_TYPE, ct)
