
ENERGYML_NAMESPACES = {
    "eml": "http://www.energistics.org/energyml/data/commonv2",
    "prodml": "http://www.energistics.org/energyml/data/prodmlv2",
    "witsml": "http://www.energistics.org/energyml/data/witsmlv2",
    "resqml": "http://www.energistics.org/energyml/data/resqmlv2",
}
"""
dict of all energyml namespaces
"""  # pylint: disable=W0105

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
"""
dict of all energyml namespace packages
"""  # pylint: disable=W0105

RGX_ENERGYML_MODULE_NAME = r"energyml\.(?P<pkg>.*)\.v(?P<version>(?P<versionNumber>\d+(_\d+)*)(_dev(?P<versionDev>.*))?)\..*"
RGX_PROJECT_VERSION = r"(?P<n0>[\d]+)(.(?P<n1>[\d]+)(.(?P<n2>[\d]+))?)?"

ENERGYML_MODULES_NAMES = ["eml", "prodml", "witsml", "resqml"]

RELATED_MODULES = [
    ["energyml.eml.v2_0.commonv2", "energyml.resqml.v2_0_1.resqmlv2"],
    [
        "energyml.eml.v2_1.commonv2",
        "energyml.prodml.v2_0.prodmlv2",
        "energyml.witsml.v2_0.witsmlv2",
    ],
    ["energyml.eml.v2_2.commonv2", "energyml.resqml.v2_2_dev3.resqmlv2"],
    [
        "energyml.eml.v2_3.commonv2",
        "energyml.resqml.v2_2.resqmlv2",
        "energyml.prodml.v2_2.prodmlv2",
        "energyml.witsml.v2_1.witsmlv2",
    ],
]

RGX_UUID_NO_GRP = (
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
RGX_UUID = r"(?P<uuid>" + RGX_UUID_NO_GRP + ")"
RGX_DOMAIN_VERSION = r"(?P<domainVersion>(?P<versionNum>([\d]+[\._])*\d)\s*(?P<dev>dev\s*(?P<devNum>[\d]+))?)"
RGX_DOMAIN_VERSION_FLAT = r"(?P<domainVersion>(?P<versionNumFlat>([\d]+)*\d)\s*(?P<dev>dev\s*(?P<devNum>[\d]+))?)"


# ContentType
RGX_MIME_TYPE_MEDIA = r"(?P<media>application|audio|font|example|image|message|model|multipart|text|video)"
RGX_CT_ENERGYML_DOMAIN = r"(?P<energymlDomain>x-(?P<domain>[\w]+)\+xml)"
RGX_CT_XML_DOMAIN = r"(?P<xmlRawDomain>(x\-)?(?P<xmlDomain>.+)\+xml)"
RGX_CT_TOKEN_VERSION = r"version=" + RGX_DOMAIN_VERSION
RGX_CT_TOKEN_TYPE = r"type=(?P<type>[\w\_]+)"

RGX_CONTENT_TYPE = (
        RGX_MIME_TYPE_MEDIA + "/"
        + "(?P<rawDomain>(" + RGX_CT_ENERGYML_DOMAIN + ")|(" + RGX_CT_XML_DOMAIN + r")|([\w-]+\.?)+)"
        + "(;((" + RGX_CT_TOKEN_VERSION + ")|(" + RGX_CT_TOKEN_TYPE + ")))*"
)
RGX_QUALIFIED_TYPE = (
        r"(?P<domain>[a-zA-Z]+)" + RGX_DOMAIN_VERSION_FLAT + r"\.(?P<type>[\w_]+)"
)
# =========

RGX_SCHEMA_VERSION = (
        r"(?P<name>[eE]ml|[cC]ommon|[rR]esqml|[wW]itsml|[pP]rodml|[oO]pc)?\s*v?"
        + RGX_DOMAIN_VERSION
        + r"\s*$"
)

RGX_ENERGYML_FILE_NAME_OLD = r"(?P<type>[\w]+)_" + RGX_UUID_NO_GRP + r"\.xml$"
RGX_ENERGYML_FILE_NAME_NEW = (
        RGX_UUID_NO_GRP + r"\.(?P<objectVersion>\d+(\.\d+)*)\.xml$"
)
RGX_ENERGYML_FILE_NAME = (
    rf"^(.*/)?({RGX_ENERGYML_FILE_NAME_OLD})|({RGX_ENERGYML_FILE_NAME_NEW})"
)

RGX_XML_HEADER = r"^\s*<\?xml(\s+(encoding\s*=\s*\"(?P<encoding>[^\"]+)\"|version\s*=\s*\"(?P<version>[^\"]+)\"|standalone\s*=\s*\"(?P<standalone>[^\"]+)\"))+"

#    __  ______  ____
#   / / / / __ \/  _/
#  / / / / /_/ // /
# / /_/ / _, _// /
# \____/_/ |_/___/

URI_RGX_GRP_DOMAIN = "domain"
URI_RGX_GRP_DOMAIN_VERSION = "domainVersion"
URI_RGX_GRP_UUID = "uuid"
URI_RGX_GRP_DATASPACE = "dataspace"
URI_RGX_GRP_VERSION = "version"
URI_RGX_GRP_OBJECT_TYPE = "objectType"
URI_RGX_GRP_UUID2 = "uuid2"
URI_RGX_GRP_COLLECTION_DOMAIN = "collectionDomain"
URI_RGX_GRP_COLLECTION_DOMAIN_VERSION = "collectionDomainVersion"
URI_RGX_GRP_COLLECTION_TYPE = "collectionType"
URI_RGX_GRP_QUERY = "query"

# Patterns
_uri_rgx_pkg_name = "|".join(ENERGYML_NAMESPACES.keys())  # "[a-zA-Z]+\w+" //witsml|resqml|prodml|eml
URI_RGX = (
        r"^eml:\/\/\/(?:dataspace\('(?P<" + URI_RGX_GRP_DATASPACE + r">[^']*?(?:''[^']*?)*)'\)\/?)?((?P<" + URI_RGX_GRP_DOMAIN
        + r">" + _uri_rgx_pkg_name + r")(?P<" + URI_RGX_GRP_DOMAIN_VERSION + r">[1-9]\d)\.(?P<" + URI_RGX_GRP_OBJECT_TYPE
        + r">\w+)(\((?:(?P<" + URI_RGX_GRP_UUID + r">(uuid=)?" + RGX_UUID_NO_GRP + r")|uuid=(?P<" + URI_RGX_GRP_UUID2
        + r">" + RGX_UUID_NO_GRP + r"),\s*version='(?P<" + URI_RGX_GRP_VERSION + r">[^']*?(?:''[^']*?)*)')\))?)?(\/(?P<"
        + URI_RGX_GRP_COLLECTION_DOMAIN + r">" + _uri_rgx_pkg_name + r")(?P<" + URI_RGX_GRP_COLLECTION_DOMAIN_VERSION
        + r">[1-9]\d)\.(?P<" + URI_RGX_GRP_COLLECTION_TYPE + r">\w+))?(?:\?(?P<" + URI_RGX_GRP_QUERY + r">[^#]+))?$"
)

# ================================
RELS_CONTENT_TYPE = "application/vnd.openxmlformats-package.core-properties+xml"
RELS_FOLDER_NAME = "_rels"

primitives = (bool, str, int, float, type(None))