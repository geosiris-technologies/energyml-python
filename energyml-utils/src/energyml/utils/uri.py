# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from .constants import *


@dataclass(init=True, eq=True,)
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
    def parse(cls, uri: str):
        m = re.match(URI_RGX, uri, re.IGNORECASE)
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
            return None

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

    def get_qualified_type(self):
        return f"{self.domain}{self.domain_version}.{self.object_type}"

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


def parse_uri(uri: str) -> Uri:
    return Uri.parse(uri)
