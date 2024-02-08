from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union, Any
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod


class Dcmitype1(Enum):
    COLLECTION = "Collection"
    DATASET = "Dataset"
    EVENT = "Event"
    IMAGE = "Image"
    INTERACTIVE_RESOURCE = "InteractiveResource"
    SERVICE = "Service"
    SOFTWARE = "Software"
    SOUND = "Sound"
    TEXT = "Text"
    PHYSICAL_OBJECT = "PhysicalObject"


@dataclass
class Contributor:
    class Meta:
        name = "contributor"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Coverage:
    class Meta:
        name = "coverage"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Creator:
    class Meta:
        name = "creator"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Date:
    class Meta:
        name = "date"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Description:
    class Meta:
        name = "description"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Format:
    class Meta:
        name = "format"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Identifier:
    class Meta:
        name = "identifier"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Language:
    class Meta:
        name = "language"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Publisher:
    class Meta:
        name = "publisher"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Relation:
    class Meta:
        name = "relation"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Rights:
    class Meta:
        name = "rights"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Source:
    class Meta:
        name = "source"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Subject:
    class Meta:
        name = "subject"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Title:
    class Meta:
        name = "title"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class TypeType:
    class Meta:
        name = "type"
        namespace = "http://purl.org/dc/elements/1.1/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Abstract:
    class Meta:
        name = "abstract"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class AccessRights:
    class Meta:
        name = "accessRights"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Alternative:
    class Meta:
        name = "alternative"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Audience:
    class Meta:
        name = "audience"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Available:
    class Meta:
        name = "available"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class BibliographicCitation:
    class Meta:
        name = "bibliographicCitation"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class ConformsTo:
    class Meta:
        name = "conformsTo"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Created:
    class Meta:
        name = "created"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class DateAccepted:
    class Meta:
        name = "dateAccepted"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class DateCopyrighted:
    class Meta:
        name = "dateCopyrighted"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class DateSubmitted:
    class Meta:
        name = "dateSubmitted"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class EducationLevel:
    class Meta:
        name = "educationLevel"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Extent:
    class Meta:
        name = "extent"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class HasFormat:
    class Meta:
        name = "hasFormat"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class HasPart:
    class Meta:
        name = "hasPart"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class HasVersion:
    class Meta:
        name = "hasVersion"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class IsFormatOf:
    class Meta:
        name = "isFormatOf"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class IsPartOf:
    class Meta:
        name = "isPartOf"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class IsReferencedBy:
    class Meta:
        name = "isReferencedBy"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class IsReplacedBy:
    class Meta:
        name = "isReplacedBy"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class IsRequiredBy:
    class Meta:
        name = "isRequiredBy"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class IsVersionOf:
    class Meta:
        name = "isVersionOf"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Issued:
    class Meta:
        name = "issued"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Mediator:
    class Meta:
        name = "mediator"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Medium:
    class Meta:
        name = "medium"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Modified:
    class Meta:
        name = "modified"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class References:
    class Meta:
        name = "references"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Replaces:
    class Meta:
        name = "replaces"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Requires:
    class Meta:
        name = "requires"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Spatial:
    class Meta:
        name = "spatial"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class TableOfContents:
    class Meta:
        name = "tableOfContents"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Temporal:
    class Meta:
        name = "temporal"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Valid:
    class Meta:
        name = "valid"
        namespace = "http://purl.org/dc/terms/"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class Default:
    class Meta:
        namespace = (
            "http://schemas.openxmlformats.org/package/2006/content-types"
        )

    extension: Optional[str] = field(
        default=None,
        metadata={
            "name": "Extension",
            "type": "Attribute",
            "required": True,
            "pattern": r"([!$&'\(\)\*\+,:=]|(%[0-9a-fA-F][0-9a-fA-F])|[:@]|[a-zA-Z0-9\-_~])+",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContentType",
            "type": "Attribute",
            "required": True,
            "pattern": r"(((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+))/((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+))((\s+)*;(\s+)*(((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+))=((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+)|(\"(([\p{IsLatin-1Supplement}\p{IsBasicLatin}-[\p{Cc}\"\n\r]]|(\s+))|(\\[\p{IsBasicLatin}]))*\"))))*)",
        },
    )


@dataclass
class Override:
    class Meta:
        namespace = (
            "http://schemas.openxmlformats.org/package/2006/content-types"
        )

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContentType",
            "type": "Attribute",
            "required": True,
            "pattern": r"(((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+))/((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+))((\s+)*;(\s+)*(((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+))=((([\p{IsBasicLatin}-[\p{Cc}\(\)<>@,;:\"/\[\]\?=\{\}\s\t]])+)|(\"(([\p{IsLatin-1Supplement}\p{IsBasicLatin}-[\p{Cc}\"\n\r]]|(\s+))|(\\[\p{IsBasicLatin}]))*\"))))*)",
        },
    )
    part_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartName",
            "type": "Attribute",
            "required": True,
        },
    )


class TargetMode(Enum):
    EXTERNAL = "External"
    INTERNAL = "Internal"


class LangValue(Enum):
    VALUE = ""


@dataclass
class SimpleLiteral:
    """This is the default type for all of the DC elements.

    It permits text content only with optional xml:lang attribute. Text
    is allowed because mixed="true", but sub-elements are disallowed
    because minOccurs="0" and maxOccurs="0" are on the xs:any tag. This
    complexType allows for restriction or extension permitting child
    elements.
    """

    class Meta:
        target_namespace = "http://purl.org/dc/elements/1.1/"

    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ElementContainer:
    """
    This complexType is included as a convenience for schema authors who need to
    define a root or container element for all of the DC elements.
    """

    class Meta:
        name = "elementContainer"
        target_namespace = "http://purl.org/dc/elements/1.1/"

    education_level: List[EducationLevel] = field(
        default_factory=list,
        metadata={
            "name": "educationLevel",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    mediator: List[Mediator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    audience: List[Audience] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    access_rights: List[AccessRights] = field(
        default_factory=list,
        metadata={
            "name": "accessRights",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    rights: List[Rights] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    temporal: List[Temporal] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    spatial: List[Spatial] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    coverage: List[Coverage] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    conforms_to: List[ConformsTo] = field(
        default_factory=list,
        metadata={
            "name": "conformsTo",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    has_format: List[HasFormat] = field(
        default_factory=list,
        metadata={
            "name": "hasFormat",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_format_of: List[IsFormatOf] = field(
        default_factory=list,
        metadata={
            "name": "isFormatOf",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    references: List[References] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_referenced_by: List[IsReferencedBy] = field(
        default_factory=list,
        metadata={
            "name": "isReferencedBy",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    has_part: List[HasPart] = field(
        default_factory=list,
        metadata={
            "name": "hasPart",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_part_of: List[IsPartOf] = field(
        default_factory=list,
        metadata={
            "name": "isPartOf",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    requires: List[Requires] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_required_by: List[IsRequiredBy] = field(
        default_factory=list,
        metadata={
            "name": "isRequiredBy",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    replaces: List[Replaces] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_replaced_by: List[IsReplacedBy] = field(
        default_factory=list,
        metadata={
            "name": "isReplacedBy",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    has_version: List[HasVersion] = field(
        default_factory=list,
        metadata={
            "name": "hasVersion",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_version_of: List[IsVersionOf] = field(
        default_factory=list,
        metadata={
            "name": "isVersionOf",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    relation: List[Relation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    language: List[Language] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    source: List[Source] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    bibliographic_citation: List[BibliographicCitation] = field(
        default_factory=list,
        metadata={
            "name": "bibliographicCitation",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    identifier: List[Identifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    medium: List[Medium] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    extent: List[Extent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    format: List[Format] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    type_value: List[TypeType] = field(
        default_factory=list,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    date_submitted: List[DateSubmitted] = field(
        default_factory=list,
        metadata={
            "name": "dateSubmitted",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    date_copyrighted: List[DateCopyrighted] = field(
        default_factory=list,
        metadata={
            "name": "dateCopyrighted",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    date_accepted: List[DateAccepted] = field(
        default_factory=list,
        metadata={
            "name": "dateAccepted",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    modified: List[Modified] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    issued: List[Issued] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    available: List[Available] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    valid: List[Valid] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    created: List[Created] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    date: List[Date] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    contributor: List[Contributor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    publisher: List[Publisher] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    abstract: List[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    table_of_contents: List[TableOfContents] = field(
        default_factory=list,
        metadata={
            "name": "tableOfContents",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    description: List[Description] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    subject: List[Subject] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    creator: List[Creator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    alternative: List[Alternative] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    title: List[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )


@dataclass
class ElementOrRefinementContainer:
    """
    This is included as a convenience for schema authors who need to define a root
    or container element for all of the DC elements and element refinements.
    """

    class Meta:
        name = "elementOrRefinementContainer"
        target_namespace = "http://purl.org/dc/terms/"

    education_level: List[EducationLevel] = field(
        default_factory=list,
        metadata={
            "name": "educationLevel",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    mediator: List[Mediator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    audience: List[Audience] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    access_rights: List[AccessRights] = field(
        default_factory=list,
        metadata={
            "name": "accessRights",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    rights: List[Rights] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    temporal: List[Temporal] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    spatial: List[Spatial] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    coverage: List[Coverage] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    conforms_to: List[ConformsTo] = field(
        default_factory=list,
        metadata={
            "name": "conformsTo",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    has_format: List[HasFormat] = field(
        default_factory=list,
        metadata={
            "name": "hasFormat",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_format_of: List[IsFormatOf] = field(
        default_factory=list,
        metadata={
            "name": "isFormatOf",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    references: List[References] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_referenced_by: List[IsReferencedBy] = field(
        default_factory=list,
        metadata={
            "name": "isReferencedBy",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    has_part: List[HasPart] = field(
        default_factory=list,
        metadata={
            "name": "hasPart",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_part_of: List[IsPartOf] = field(
        default_factory=list,
        metadata={
            "name": "isPartOf",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    requires: List[Requires] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_required_by: List[IsRequiredBy] = field(
        default_factory=list,
        metadata={
            "name": "isRequiredBy",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    replaces: List[Replaces] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_replaced_by: List[IsReplacedBy] = field(
        default_factory=list,
        metadata={
            "name": "isReplacedBy",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    has_version: List[HasVersion] = field(
        default_factory=list,
        metadata={
            "name": "hasVersion",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    is_version_of: List[IsVersionOf] = field(
        default_factory=list,
        metadata={
            "name": "isVersionOf",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    relation: List[Relation] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    language: List[Language] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    source: List[Source] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    bibliographic_citation: List[BibliographicCitation] = field(
        default_factory=list,
        metadata={
            "name": "bibliographicCitation",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    identifier: List[Identifier] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    medium: List[Medium] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    extent: List[Extent] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    format: List[Format] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    type_value: List[TypeType] = field(
        default_factory=list,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    date_submitted: List[DateSubmitted] = field(
        default_factory=list,
        metadata={
            "name": "dateSubmitted",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    date_copyrighted: List[DateCopyrighted] = field(
        default_factory=list,
        metadata={
            "name": "dateCopyrighted",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    date_accepted: List[DateAccepted] = field(
        default_factory=list,
        metadata={
            "name": "dateAccepted",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    modified: List[Modified] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    issued: List[Issued] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    available: List[Available] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    valid: List[Valid] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    created: List[Created] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    date: List[Date] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    contributor: List[Contributor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    publisher: List[Publisher] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    abstract: List[Abstract] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    table_of_contents: List[TableOfContents] = field(
        default_factory=list,
        metadata={
            "name": "tableOfContents",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    description: List[Description] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    subject: List[Subject] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    creator: List[Creator] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    alternative: List[Alternative] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    title: List[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )


@dataclass
class Types:
    class Meta:
        namespace = (
            "http://schemas.openxmlformats.org/package/2006/content-types"
        )

    default: List[Default] = field(
        default_factory=list,
        metadata={
            "name": "Default",
            "type": "Element",
        },
    )
    override: List[Override] = field(
        default_factory=list,
        metadata={
            "name": "Override",
            "type": "Element",
        },
    )


@dataclass
class Keyword1:
    class Meta:
        name = "Keyword"
        target_namespace = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )


@dataclass
class Relationship:
    class Meta:
        namespace = (
            "http://schemas.openxmlformats.org/package/2006/relationships"
        )

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    target_mode: Optional[TargetMode] = field(
        default=None,
        metadata={
            "name": "TargetMode",
            "type": "Attribute",
        },
    )
    target: Optional[str] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Attribute",
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "required": True,
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Box(SimpleLiteral):
    class Meta:
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Dcmitype2(SimpleLiteral):
    class Meta:
        name = "DCMIType"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: Optional[Dcmitype1] = field(default=None)
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Ddc(SimpleLiteral):
    class Meta:
        name = "DDC"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Imt(SimpleLiteral):
    class Meta:
        name = "IMT"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Iso3166(SimpleLiteral):
    class Meta:
        name = "ISO3166"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Iso6392(SimpleLiteral):
    class Meta:
        name = "ISO639-2"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Lcc(SimpleLiteral):
    class Meta:
        name = "LCC"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Lcsh(SimpleLiteral):
    class Meta:
        name = "LCSH"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Mesh(SimpleLiteral):
    class Meta:
        name = "MESH"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Period(SimpleLiteral):
    class Meta:
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Point(SimpleLiteral):
    class Meta:
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Rfc1766(SimpleLiteral):
    class Meta:
        name = "RFC1766"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Rfc3066(SimpleLiteral):
    class Meta:
        name = "RFC3066"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Tgn(SimpleLiteral):
    class Meta:
        name = "TGN"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Udc(SimpleLiteral):
    class Meta:
        name = "UDC"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Uri(SimpleLiteral):
    class Meta:
        name = "URI"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: str = field(default="")
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class W3Cdtf(SimpleLiteral):
    class Meta:
        name = "W3CDTF"
        target_namespace = "http://purl.org/dc/terms/"

    content: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    value: Optional[Union[XmlPeriod, XmlDate, XmlDateTime]] = field(
        default=None
    )
    lang: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class Keywords1:
    class Meta:
        name = "Keywords"
        target_namespace = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"

    lang: Optional[Union[str, LangValue]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
        },
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "value",
                    "type": Keyword1,
                    "namespace": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
                },
            ),
        },
    )


@dataclass
class Keyword(Keyword1):
    class Meta:
        name = "keyword"
        namespace = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"


@dataclass
class Relationships:
    class Meta:
        namespace = (
            "http://schemas.openxmlformats.org/package/2006/relationships"
        )

    relationship: List[Relationship] = field(
        default_factory=list,
        metadata={
            "name": "Relationship",
            "type": "Element",
        },
    )


@dataclass
class CoreProperties:
    class Meta:
        name = "coreProperties"
        namespace = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"

    category: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    content_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentStatus",
            "type": "Element",
        },
    )
    created: Optional[Created] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    creator: Optional[Creator] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    abstract: Optional[Abstract] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    table_of_contents: Optional[TableOfContents] = field(
        default=None,
        metadata={
            "name": "tableOfContents",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    description: Optional[Description] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    bibliographic_citation: Optional[BibliographicCitation] = field(
        default=None,
        metadata={
            "name": "bibliographicCitation",
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    keywords: Optional[Keywords1] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    last_modified_by: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastModifiedBy",
            "type": "Element",
        },
    )
    last_printed: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastPrinted",
            "type": "Element",
        },
    )
    modified: Optional[Modified] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    revision: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )
    subject: Optional[Subject] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    alternative: Optional[Alternative] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/terms/",
        },
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://purl.org/dc/elements/1.1/",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        },
    )


@dataclass
class Keywords(Keywords1):
    class Meta:
        name = "keywords"
        namespace = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
