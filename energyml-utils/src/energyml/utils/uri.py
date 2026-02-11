# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import re
from typing import Optional
from dataclasses import dataclass, field

from energyml.utils.exception import ContentTypeValidationError, NotUriError
from .constants import (
    RGX_CT_ENERGYML_DOMAIN,
    RGX_CT_TOKEN_TYPE,
    RGX_CT_TOKEN_VERSION,
    URI_RGX_GRP_DATASPACE,
    URI_RGX_GRP_DOMAIN,
    URI_RGX_GRP_DOMAIN_VERSION,
    URI_RGX_GRP_OBJECT_TYPE,
    URI_RGX_GRP_UUID,
    URI_RGX_GRP_UUID2,
    URI_RGX_GRP_VERSION,
    URI_RGX_GRP_COLLECTION_DOMAIN,
    URI_RGX_GRP_COLLECTION_DOMAIN_VERSION,
    URI_RGX_GRP_COLLECTION_TYPE,
    URI_RGX_GRP_QUERY,
    OptimizedRegex,
    parse_content_or_qualified_type,
)


@dataclass(
    init=True,
    eq=True,
)
class Uri:
    """
    A class to represent an ETP URI
    """

    dataspace: Optional[str] = field(default=None)
    domain: Optional[str] = field(default=None)
    domain_version: Optional[str] = field(default=None)
    object_type: Optional[str] = field(default=None)
    uuid: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)
    collection_domain: Optional[str] = field(default=None)
    collection_domain_version: Optional[str] = field(default=None)
    collection_domain_type: Optional[str] = field(default=None)
    query: Optional[str] = field(default=None)

    @classmethod
    def parse(cls, uri: str) -> "Uri":
        m = OptimizedRegex.URI.match(uri)
        if m is not None:
            res = Uri()
            res.dataspace = m.group(URI_RGX_GRP_DATASPACE)
            res.domain = m.group(URI_RGX_GRP_DOMAIN)
            if res.domain is not None and len(res.domain) <= 0:
                res.domain = None
            res.domain_version = m.group(URI_RGX_GRP_DOMAIN_VERSION)
            res.object_type = m.group(URI_RGX_GRP_OBJECT_TYPE)
            res.uuid = m.group(URI_RGX_GRP_UUID) or m.group(URI_RGX_GRP_UUID2)
            res.version = m.group(URI_RGX_GRP_VERSION)
            res.collection_domain = m.group(URI_RGX_GRP_COLLECTION_DOMAIN)
            res.collection_domain_version = m.group(URI_RGX_GRP_COLLECTION_DOMAIN_VERSION)
            res.collection_domain_type = m.group(URI_RGX_GRP_COLLECTION_TYPE)
            res.query = m.group(URI_RGX_GRP_QUERY)
            return res
        else:
            raise NotUriError(uri)

    def is_dataspace_uri(self):
        return (
            self.domain is None
            and self.object_type is None
            and self.query is None
            and self.collection_domain_type is None
        )

    def is_object_uri(self):
        return (
            self.domain is not None
            and self.domain_version is not None
            and self.object_type is not None
            and self.uuid is not None
        )

    def get_qualified_type(self) -> str:
        if self.domain is None or self.domain_version is None or self.object_type is None:
            raise ValueError("The URI must have a domain, domain version and object type to get the qualified type")
        return f"{self.domain}{self.domain_version}.{self.object_type}"

    def get_content_type(self) -> str:
        if self.domain is None or self.domain_version is None or self.object_type is None:
            raise ValueError("The URI must have a domain, domain version and object type to get the content type")
        # Format version with dots
        formatted_version = re.sub(r"(\d)(\d)", r"\1.\2", self.domain_version)
        return f"application/x-{self.domain}+xml;" f"version={formatted_version};" f"type={self.object_type}"

    def as_identifier(self) -> str:
        if not self.is_object_uri():
            raise ValueError("Only object URIs can be converted to identifiers")
        return f"{self.uuid}.{self.version if self.version is not None else ''}"

    def __str__(self):
        res = "eml:///"
        if self.dataspace is not None and len(self.dataspace) > 0:
            res += f"dataspace('{self.dataspace}')"
            if self.domain is not None:
                res += "/"
        if self.domain is not None and self.domain_version is not None:
            res += f"{self.domain}{self.domain_version}.{self.object_type}"
            if self.uuid is not None:
                res += "("
                if self.version is not None:
                    res += f"uuid={self.uuid},version='{self.version}'"
                else:
                    res += self.uuid
                res += ")"
        if self.collection_domain is not None and self.collection_domain_version:
            res += f"/{self.collection_domain}{self.collection_domain_version}"
            if self.collection_domain_type is not None:
                res += f".{self.collection_domain_type}"

        if self.query is not None:
            res += f"?{self.query}"

        return res

    def __hash__(self) -> int:
        return hash(str(self))


def parse_uri_raise_if_failed(uri: str) -> Uri:
    if uri is None or len(uri) <= 0:
        raise NotUriError(uri)
    return Uri.parse(uri.strip())


def parse_uri(uri: str) -> Optional[Uri]:
    try:
        return parse_uri_raise_if_failed(uri)
    except NotUriError:
        return None


def create_uri_from_content_type_or_qualified_type(ct_or_qt: str, uuid: str, version: Optional[str] = None) -> Uri:
    """Create a URI from a content type or a qualified type and a uuid (and optionally an object version)
    :param ct_or_qt: the content type or qualified type to create the URI from
    :param uuid: the uuid of the object
    :param version: the version of the object (optional)
    :return: the created URI
    """
    if ct_or_qt is None or len(ct_or_qt) <= 0:
        raise ContentTypeValidationError("Content type or qualified type cannot be null or empty")
    if uuid is None or len(uuid) <= 0:
        raise ValueError("UUID cannot be null or empty")
    m = parse_content_or_qualified_type(ct_or_qt)
    if m is not None:
        try:
            domain = m.group("domain")
            domain_version = m.group("domainVersion")
            # ensure domaine version has no dots and is in the format of digits only
            formatted_version = re.sub(r"(\d)[^\d]+(\d)", r"\1\2", domain_version)
            object_type = m.group("type")
            return Uri(
                domain=domain, domain_version=formatted_version, object_type=object_type, uuid=uuid, version=version
            )
        except Exception as e:
            raise ContentTypeValidationError(
                f"Failed to parse content type or qualified type: {ct_or_qt} -- {m}"
            ) from e
    raise NotUriError(f"Unable to parse content type: {ct_or_qt}")
