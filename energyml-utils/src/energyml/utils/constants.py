# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import datetime
import json
import re
import uuid as uuid_mod
from dataclasses import field, dataclass
from enum import Enum
from io import BytesIO
from re import findall
from typing import List, Optional, Tuple

from importlib.resources import files


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
        "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    ],
}
"""
dict of all energyml namespace packages
"""  # pylint: disable=W0105

RGX_ENERGYML_MODULE_NAME = r"energyml\.(?P<pkg>.*)\.v(?P<version>(?P<versionNumber>\d+(_\d+)*)(_dev(?P<versionDev>.*))?)\..*"  # pylint: disable=C0301
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

RGX_UUID_NO_GRP = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
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
    RGX_MIME_TYPE_MEDIA
    + "/"
    + "(?P<rawDomain>("
    + RGX_CT_ENERGYML_DOMAIN
    + ")|("
    + RGX_CT_XML_DOMAIN
    + r")|([\w-]+\.?)+)"
    + "(;(("
    + RGX_CT_TOKEN_VERSION
    + ")|("
    + RGX_CT_TOKEN_TYPE
    + ")))*"
)
RGX_QUALIFIED_TYPE = r"(?P<domain>[a-zA-Z]+)" + RGX_DOMAIN_VERSION_FLAT + r"\.(?P<type>[\w_]+)"
# =========

RGX_SCHEMA_VERSION = (
    r"(?P<name>[eE]ml|[cC]ommon|[rR]esqml|[wW]itsml|[pP]rodml|[oO]pc)?\s*v?" + RGX_DOMAIN_VERSION + r"\s*$"
)

RGX_ENERGYML_FILE_NAME_OLD = r"(?P<type>[\w]+)_" + RGX_UUID_NO_GRP + r"\.xml$"
RGX_ENERGYML_FILE_NAME_NEW = RGX_UUID_NO_GRP + r"\.(?P<objectVersion>\d+(\.\d+)*)\.xml$"
RGX_ENERGYML_FILE_NAME = rf"^(.*/)?({RGX_ENERGYML_FILE_NAME_OLD})|({RGX_ENERGYML_FILE_NAME_NEW})"

RGX_XML_HEADER = r"^\s*<\?xml(\s+(encoding\s*=\s*\"(?P<encoding>[^\"]+)\"|version\s*=\s*\"(?P<version>[^\"]+)\"|standalone\s*=\s*\"(?P<standalone>[^\"]+)\"))+"  # pylint: disable=C0301

RGX_IDENTIFIER = rf"{RGX_UUID}(.(?P<version>\w+)?)?"


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
_URI_RGX_PKG_NAME = "|".join(ENERGYML_NAMESPACES.keys())  # "[a-zA-Z]+\w+" //witsml|resqml|prodml|eml
URI_RGX = (
    r"^eml:\/\/\/(?:dataspace\('(?P<"
    + URI_RGX_GRP_DATASPACE
    + r">[^']*?(?:''[^']*?)*)'\)\/?)?((?P<"
    + URI_RGX_GRP_DOMAIN
    + r">"
    + _URI_RGX_PKG_NAME
    + r")(?P<"
    + URI_RGX_GRP_DOMAIN_VERSION
    + r">[1-9]\d)\.(?P<"
    + URI_RGX_GRP_OBJECT_TYPE
    + r">\w+)(\((?:(?P<"
    + URI_RGX_GRP_UUID
    + r">(uuid=)?"
    + RGX_UUID_NO_GRP
    + r")|uuid=(?P<"
    + URI_RGX_GRP_UUID2
    + r">"
    + RGX_UUID_NO_GRP
    + r"),\s*version='(?P<"
    + URI_RGX_GRP_VERSION
    + r">[^']*?(?:''[^']*?)*)')\))?)?(\/(?P<"
    + URI_RGX_GRP_COLLECTION_DOMAIN
    + r">"
    + _URI_RGX_PKG_NAME
    + r")(?P<"
    + URI_RGX_GRP_COLLECTION_DOMAIN_VERSION
    + r">[1-9]\d)\.(?P<"
    + URI_RGX_GRP_COLLECTION_TYPE
    + r">\w+))?(?:\?(?P<"
    + URI_RGX_GRP_QUERY
    + r">[^#]+))?$"
)

# ================================
RELS_CONTENT_TYPE = "application/vnd.openxmlformats-package.core-properties+xml"
RELS_FOLDER_NAME = "_rels"

primitives = (bool, str, int, float, type(None))

DOT_PATH_ATTRIBUTE = r"(?:(?<=\\)\.|[^\.])+"
DOT_PATH = rf"\.*(?P<first>{DOT_PATH_ATTRIBUTE})(?P<next>(\.(?P<last>{DOT_PATH_ATTRIBUTE}))*)"


class MimeType(Enum):
    """Some mime types"""

    CSV = "text/csv"
    HDF5 = "application/x-hdf5"
    PARQUET = "application/x-parquet"
    PDF = "application/pdf"
    RELS = "application/vnd.openxmlformats-package.relationships+xml"

    def __str__(self):
        return self.value


class EpcExportVersion(Enum):
    """EPC export version."""

    #: Classical export
    CLASSIC = 1
    #: Export with objet path sorted by package (eml/resqml/witsml/prodml)
    EXPANDED = 2


class EPCRelsRelationshipType(Enum):
    """Rels relationship types"""

    #: The object in Target is the destination of the relationship.
    DESTINATION_OBJECT = "destinationObject"
    #: The current object is the source in the relationship with the target object.
    SOURCE_OBJECT = "sourceObject"
    #: The target object is a proxy object for an external data object (HDF5 file).
    ML_TO_EXTERNAL_PART_PROXY = "mlToExternalPartProxy"
    #: The current object is used as a proxy object by the target object.
    EXTERNAL_PART_PROXY_TO_ML = "externalPartProxyToMl"
    #: The target is a resource outside of the EPC package. Note that TargetMode should be "External"
    #: for this relationship.
    EXTERNAL_RESOURCE = "externalResource"
    #: The object in Target is a media representation for the current object. As a guideline, media files
    #: should be stored in a "media" folder in the ROOT of the package.
    DestinationMedia = "destinationMedia"
    #: The current object is a media representation for the object in Target.
    SOURCE_MEDIA = "sourceMedia"
    #: The target is part of a larger data object that has been chunked into several smaller files
    CHUNKED_PART = "chunkedPart"
    #: The core properties
    CORE_PROPERTIES = "core-properties"
    #: /!\ not in the norm
    EXTENDED_CORE_PROPERTIES = "extended-core-properties"

    def get_type(self) -> str:
        if self == EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES:
            return "http://schemas.f2i-consulting.com/package/2014/relationships/" + str(self.value)
        elif EPCRelsRelationshipType.CORE_PROPERTIES:
            return "http://schemas.openxmlformats.org/package/2006/relationships/metadata/" + str(self.value)
        # elif (
        #          self == EPCRelsRelationshipType.CHUNKED_PART
        #         or  self == EPCRelsRelationshipType.DESTINATION_OBJECT
        #         or  self == EPCRelsRelationshipType.SOURCE_OBJECT
        #         or  self == EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY
        #         or  self == EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML
        #         or  self == EPCRelsRelationshipType.EXTERNAL_RESOURCE
        #         or  self == EPCRelsRelationshipType.DestinationMedia
        #         or  self == EPCRelsRelationshipType.SOURCE_MEDIA
        #     ):
        return "http://schemas.energistics.org/package/2012/relationships/" + str(self.value)


@dataclass
class RawFile:
    """A class for a non energyml file to be stored in an EPC file"""

    path: str = field(default="_")
    content: BytesIO = field(default=None)


#     ______                 __  _
#    / ____/_  ______  _____/ /_(_)___  ____  _____
#   / /_  / / / / __ \/ ___/ __/ / __ \/ __ \/ ___/
#  / __/ / /_/ / / / / /__/ /_/ / /_/ / / / (__  )
# /_/    \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/


def snake_case(string: str) -> str:
    """Transform a str into snake case."""
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    string = re.sub("__([A-Z])", r"_\1", string)
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
    return string.lower()


def pascal_case(string: str) -> str:
    """Transform a str into pascal case."""
    return snake_case(string).replace("_", " ").title().replace(" ", "")


def flatten_concatenation(matrix) -> List:
    """
    Flatten a matrix.

    Example :
        [ [a,b,c], [d,e,f], [ [x,y,z], [0] ] ]
        will be translated in: [a, b, c, d, e, f, [x,y,z], [0]]
    :param matrix:
    :return:
    """
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


def parse_content_type(ct: str) -> Optional[re.Match[str]]:
    return re.search(RGX_CONTENT_TYPE, ct)


def parse_qualified_type(ct: str) -> Optional[re.Match[str]]:
    return re.search(RGX_QUALIFIED_TYPE, ct)


def parse_content_or_qualified_type(cqt: str) -> Optional[re.Match[str]]:
    """
    Give a re.Match object (or None if failed).
    You can access to groups like : "domainVersion", "versionNum", "domain", "type"

    :param cqt:
    :return:
    """
    parsed = None
    try:
        parsed = parse_content_type(cqt)
    except:
        pass
    if parsed is None:
        try:
            parsed = parse_qualified_type(cqt)
        except:
            pass

    return parsed


def content_type_to_qualified_type(ct: str):
    parsed = parse_content_or_qualified_type(ct)
    return parsed.group("domain") + parsed.group("domainVersion").replace(".", "") + "." + parsed.group("type")


def qualified_type_to_content_type(qt: str):
    parsed = parse_content_or_qualified_type(qt)
    return (
        "application/x-"
        + parsed.group("domain")
        + "+xml;version="
        + re.sub(r"(\d)(\d)", r"\1.\2", parsed.group("domainVersion"))
        + ";type="
        + parsed.group("type")
    )


def get_domain_version_from_content_or_qualified_type(cqt: str) -> Optional[str]:
    """
    return a version number like "2.2" or "2.0"

    :param cqt:
    :return:
    """
    try:
        parsed = parse_content_type(cqt)
        return parsed.group("domainVersion")
    except:
        try:
            parsed = parse_qualified_type(cqt)
            return ".".join(parsed.group("domainVersion"))
        except:
            pass
    return None


def split_identifier(identifier: str) -> Tuple[str, Optional[str]]:
    match = re.match(RGX_IDENTIFIER, identifier)
    return (
        match.group(URI_RGX_GRP_UUID),
        match.group(URI_RGX_GRP_VERSION),
    )


def now(time_zone=datetime.timezone.utc) -> float:
    """Return an epoch value"""
    return datetime.datetime.timestamp(datetime.datetime.now(time_zone))


def epoch(time_zone=datetime.timezone.utc) -> int:
    return int(now(time_zone))


def date_to_epoch(date: str) -> int:
    """
    Transform a energyml date into an epoch datetime
    :return: int
    """
    return int(datetime.datetime.fromisoformat(date).timestamp())


def epoch_to_date(
    epoch_value: int,
) -> str:
    date = datetime.datetime.fromtimestamp(epoch_value, datetime.timezone.utc)
    return date.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # date = datetime.datetime.fromtimestamp(epoch_value, datetime.timezone.utc)
    # return date.astimezone(datetime.timezone(datetime.timedelta(hours=0), "UTC")).strftime('%Y-%m-%dT%H:%M:%SZ')
    # return date.strftime("%Y-%m-%dT%H:%M:%SZ%z")


def gen_uuid() -> str:
    """
    Generate a new uuid.
    :return:
    """
    return str(uuid_mod.uuid4())


def mime_type_to_file_extension(mime_type: str) -> Optional[str]:
    if mime_type is not None:
        mime_type_lw = mime_type.lower()
        if (
            mime_type_lw == "application/x-parquet"
            or mime_type_lw == "application/parquet"
            or mime_type_lw == "application/vnd.apache.parquet"
        ):
            return "parquet"
        elif mime_type_lw == "application/x-hdf5":
            return "h5"
        elif mime_type_lw == "text/csv":
            return "csv"
        elif mime_type_lw == "application/vnd.openxmlformats-package.relationships+xml":
            return "rels"
        elif mime_type_lw == "application/pdf":
            return "pdf"

    return None


def path_next_attribute(dot_path: str) -> Tuple[Optional[str], Optional[str]]:
    _m = re.match(DOT_PATH, dot_path)
    if _m is not None:
        _next = _m.group("next")
        return _m.group("first"), _next if _next is not None and len(_next) > 0 else None
    return None, None


def path_last_attribute(dot_path: str) -> str:
    _m = re.match(DOT_PATH, dot_path)
    if _m is not None:
        return _m.group("last")
    return None


def path_iter(dot_path: str) -> List[str]:
    return findall(DOT_PATH_ATTRIBUTE, dot_path)


def _get_property_kind_dict_path_as_str(file_type: str = "xml") -> str:
    try:
        import energyml.utils.rc as RC
    except:
        try:
            import src.energyml.utils.rc as RC
        except:
            import utils.rc as RC
    return files(RC).joinpath(f"PropertyKindDictionary_v2.3.{file_type.lower()}").read_text(encoding="utf-8")


def get_property_kind_dict_path_as_json() -> str:
    return _get_property_kind_dict_path_as_str("json")


def get_property_kind_dict_path_as_dict() -> dict:
    return json.loads(_get_property_kind_dict_path_as_str("json"))


def get_property_kind_dict_path_as_xml() -> str:
    return _get_property_kind_dict_path_as_str("xml")


if __name__ == "__main__":

    m = re.match(DOT_PATH, ".Citation.Title.Coucou")
    print(m.groups())
    print(m.group("first"))
    print(m.group("last"))
    print(m.group("next"))
    m = re.match(DOT_PATH, ".Citation")
    print(m.groups())
    print(m.group("first"))
    print(m.group("last"))
    print(m.group("next"))

    print(path_next_attribute(".Citation.Title.Coucou"))
    print(path_iter(".Citation.Title.Coucou"))
    print(path_iter(".Citation.Ti\\.*.Coucou"))

    print(URI_RGX)
    print(RGX_UUID_NO_GRP)
