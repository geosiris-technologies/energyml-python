import re
from dataclasses import dataclass, field
from typing import Optional

from .constants import *


@dataclass
class Uri:
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
        res = Uri()
        m = re.match(URI_RGX, uri, re.IGNORECASE)
        if m is not None:
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
            # print(f"\t{m.groupdict()}\n\t{res.__dict__}")
        else:
            return None

        return res

    def is_dataspace_uri(self):
        return self.domain is None and self.object_type is None and self.query is None and self.collection_domain_type is None

    def is_object_uri(self):
        return self.domain is not None and self.domain_version is not None and self.object_type is not None and self.uuid is not None

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


if __name__ == "__main__":
    uris = [
        "eml:///witsml20.Well/witsml20.Wellbore", "eml:///", "eml:///dataspace('')", "eml:///dataspace('rdms-db')",
        "eml:///dataspace('/folder-name/project-name')",
        "eml:///resqml20.obj_HorizonInterpretation(421a7a05-033a-450d-bcef-051352023578)",
        "eml:///dataspace('rdms-db')?$filter=Name eq 'mydb'",
        "eml:///dataspace('/folder-name/project-name')/resqml20.obj_HorizonInterpretation?query",
        "eml:///witsml20.Well(uuid=ec8c3f16-1454-4f36-ae10-27d2a2680cf2)",
        "eml:///dataspace('/folder-name/project-name')/resqml20.obj_HorizonInterpretation(uuid=421a7a05-033a-450d-bcef-051352023578,version='2.0')?query",
        "eml:///dataspace('test')/witsml20.Well(ec8c3f16-1454-4f36-ae10-27d2a2680cf2)/witsml20.Wellbore?query",
        "eml:///witsml20.Well(uuid=ec8c3f16-1454-4f36-ae10-27d2a2680cf2,version='1.0')/witsml20.Wellbore?query"
    ]

    for uria in uris:
        print(f"Parsing {uria}")
        parsed = Uri.parse(uria)
        if uria != str(parsed):
            print("\t[FALSE] : " + str(parsed))
        else:
            print("\t[YES] " + str(parsed))

