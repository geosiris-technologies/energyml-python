from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union, Any
from xsdata.models.datatype import XmlDate
from generated.eml.v2_2.gmd import ExExtent
from generated.eml.v2_2.xlink import (
    ActuateValue,
    ShowValue,
)

__NAMESPACE__ = "http://www.opengis.net/gml/3.2"


class AggregationType(Enum):
    SET = "set"
    BAG = "bag"
    SEQUENCE = "sequence"
    ARRAY = "array"
    RECORD = "record"
    TABLE = "table"


@dataclass
class CodeType:
    """Gml:CodeType is a generalized type to be used for a term, keyword or name.

    It adds a XML attribute codeSpace to a term, where the value of the
    codeSpace attribute (if present) shall indicate a dictionary,
    thesaurus, classification scheme, authority, or pattern for the
    term.
    """

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    code_space: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeSpace",
            "type": "Attribute",
        },
    )


class NilReasonEnumerationValue(Enum):
    INAPPLICABLE = "inapplicable"
    MISSING = "missing"
    TEMPLATE = "template"
    UNKNOWN = "unknown"
    WITHHELD = "withheld"


class RelatedTimeTypeRelativePosition(Enum):
    BEFORE = "Before"
    AFTER = "After"
    BEGINS = "Begins"
    ENDS = "Ends"
    DURING = "During"
    EQUALS = "Equals"
    CONTAINS = "Contains"
    OVERLAPS = "Overlaps"
    MEETS = "Meets"
    OVERLAPPED_BY = "OverlappedBy"
    MET_BY = "MetBy"
    BEGUN_BY = "BegunBy"
    ENDED_BY = "EndedBy"


@dataclass
class SecondDefiningParameter1:
    class Meta:
        name = "SecondDefiningParameter"
        namespace = "http://www.opengis.net/gml/3.2"

    inverse_flattening: Optional[float] = field(
        default=None,
        metadata={
            "name": "inverseFlattening",
            "type": "Element",
        },
    )
    semi_minor_axis: Optional[float] = field(
        default=None,
        metadata={
            "name": "semiMinorAxis",
            "type": "Element",
        },
    )
    is_sphere: bool = field(
        default=True,
        metadata={
            "name": "isSphere",
            "type": "Element",
        },
    )


@dataclass
class GreenwichLongitude:
    """Gml:greenwichLongitude is the longitude of the prime meridian measured from
    the Greenwich meridian, positive eastward.

    If the value of the prime meridian "name" is "Greenwich" then the
    value of greenwichLongitude shall be 0 degrees.
    """

    class Meta:
        name = "greenwichLongitude"
        namespace = "http://www.opengis.net/gml/3.2"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class MaximumValue:
    """The gml:minimumValue and gml:maximumValue properties allow the specification
    of minimum and maximum value normally allowed for this axis, in the unit of
    measure for the axis.

    For a continuous angular axis such as longitude, the values wrap-
    around at this value. Also, values beyond this minimum/maximum can
    be used for specified purposes, such as in a bounding box. A value
    of minus infinity shall be allowed for the gml:minimumValue element,
    a value of plus infiniy for the gml:maximumValue element. If these
    elements are omitted, the value is unspecified.
    """

    class Meta:
        name = "maximumValue"
        namespace = "http://www.opengis.net/gml/3.2"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class MinimumValue:
    """The gml:minimumValue and gml:maximumValue properties allow the specification
    of minimum and maximum value normally allowed for this axis, in the unit of
    measure for the axis.

    For a continuous angular axis such as longitude, the values wrap-
    around at this value. Also, values beyond this minimum/maximum can
    be used for specified purposes, such as in a bounding box. A value
    of minus infinity shall be allowed for the gml:minimumValue element,
    a value of plus infiniy for the gml:maximumValue element. If these
    elements are omitted, the value is unspecified.
    """

    class Meta:
        name = "minimumValue"
        namespace = "http://www.opengis.net/gml/3.2"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class OperationVersion:
    """Gml:operationVersion is the version of the coordinate transformation (i.e.,
    instantiation due to the stochastic nature of the parameters).

    Mandatory when describing a transformation, and should not be
    supplied for a conversion.
    """

    class Meta:
        name = "operationVersion"
        namespace = "http://www.opengis.net/gml/3.2"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class RealizationEpoch:
    """Gml:realizationEpoch is the time after which this datum definition is valid.

    See ISO 19111 Table 32 for details.
    """

    class Meta:
        name = "realizationEpoch"
        namespace = "http://www.opengis.net/gml/3.2"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class Remarks:
    class Meta:
        name = "remarks"
        namespace = "http://www.opengis.net/gml/3.2"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Scope:
    """The gml:scope property provides a description of the usage, or limitations
    of usage, for which this CRS-related object is valid.

    If unknown, enter "not known".
    """

    class Meta:
        name = "scope"
        namespace = "http://www.opengis.net/gml/3.2"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class SemiMajorAxis:
    """Gml:semiMajorAxis specifies the length of the semi-major axis of the
    ellipsoid, with its units.

    Uses the MeasureType with the restriction that the unit of measure
    referenced by uom must be suitable for a length, such as metres or
    feet.
    """

    class Meta:
        name = "semiMajorAxis"
        namespace = "http://www.opengis.net/gml/3.2"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class CodeWithAuthorityType(CodeType):
    """
    Gml:CodeWithAuthorityType requires that the codeSpace attribute is provided in
    an instance.
    """

    code_space: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeSpace",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class GeneralConversionPropertyType:
    """
    Gml:GeneralConversionPropertyType is a property type for association roles to a
    general conversion, either referencing or containing the definition of that
    conversion.
    """

    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ReferenceType:
    """
    Gml:ReferenceType is intended to be used in application schemas directly, if a
    property element shall use a "by-reference only" encoding.
    """

    owns: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class StringOrRefType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class TimePrimitivePropertyType:
    """
    Gml:TimePrimitivePropertyType provides a standard content model for
    associations between an arbitrary member of the substitution group whose head
    is gml:AbstractTimePrimitive and another object.
    """

    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )
    owns: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AnchorDefinition(CodeType):
    """Gml:anchorDefinition is a description, possibly including coordinates, of
    the definition used to anchor the datum to the Earth. Also known as the
    "origin", especially for engineering and image datums. The codeSpace attribute
    may be used to reference a source of more detailed on this point or surface, or
    on a set of such descriptions.

    -       For a geodetic datum, this point is also known as the fundamental point, which is traditionally the point where the relationship between geoid and ellipsoid is defined. In some cases, the "fundamental point" may consist of a number of points. In those cases, the parameters defining the geoid/ellipsoid relationship have been averaged for these points, and the averages adopted as the datum definition.
    -       For an engineering datum, the anchor definition may be a physical point, or it may be a point with defined coordinates in another CRS.may
    -       For an image datum, the anchor definition is usually either the centre of the image or the corner of the image.
    -       For a temporal datum, this attribute is not defined. Instead of the anchor definition, a temporal datum carries a separate time origin of type DateTime.
    """

    class Meta:
        name = "anchorDefinition"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class AxisAbbrev(CodeType):
    """Gml:axisAbbrev is the abbreviation used for this coordinate system axis;
    this abbreviation is also used to identify the coordinates in the coordinate
    tuple.

    The codeSpace attribute may reference a source of more information
    on a set of standardized abbreviations, or on this abbreviation.
    """

    class Meta:
        name = "axisAbbrev"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class CoordinateOperationAccuracy:
    """Gml:coordinateOperationAccuracy is an association role to a
    DQ_PositionalAccuracy object as encoded in ISO/TS 19139, either referencing or
    containing the definition of that positional accuracy.

    That object contains an estimate of the impact of this coordinate
    operation on point accuracy. That is, it gives position error
    estimates for the target coordinates of this coordinate operation,
    assuming no errors in the source coordinates.
    """

    class Meta:
        name = "coordinateOperationAccuracy"
        namespace = "http://www.opengis.net/gml/3.2"

    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class DomainOfValidity:
    """
    The gml:domainOfValidity property implements an association role to an
    EX_Extent object as encoded in ISO/TS 19139, either referencing or containing
    the definition of that extent.
    """

    class Meta:
        name = "domainOfValidity"
        namespace = "http://www.opengis.net/gml/3.2"

    ex_extent: Optional[ExExtent] = field(
        default=None,
        metadata={
            "name": "EX_Extent",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class Name(CodeType):
    """The gml:name property provides a label or identifier for the object,
    commonly a descriptive name.

    An object may have several names, typically assigned by different
    authorities. gml:name uses the gml:CodeType content model.  The
    authority for a name is indicated by the value of its (optional)
    codeSpace attribute.  The name may or may not be unique, as
    determined by the rules of the organization responsible for the
    codeSpace.  In common usage there will be one name per authority, so
    a processing application may select the name from its preferred
    codeSpace.
    """

    class Meta:
        name = "name"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class SecondDefiningParameter2:
    """Gml:secondDefiningParameter is a property containing the definition of the
    second parameter that defines the shape of an ellipsoid.

    An ellipsoid requires two defining parameters: semi-major axis and inverse flattening or semi-major axis and semi-minor axis. When the reference body is a sphere rather than an ellipsoid, only a single defining parameter is required, namely the radius of the sphere; in that case, the semi-major axis "degenerates" into the radius of the sphere.
    The inverseFlattening element contains the inverse flattening value of the ellipsoid. This value is a scale factor (or ratio). It uses gml:LengthType with the restriction that the unit of measure referenced by the uom attribute must be suitable for a scale factor, such as percent, permil, or parts-per-million.
    The semiMinorAxis element contains the length of the semi-minor axis of the ellipsoid. When the isSphere element is included, the ellipsoid is degenerate and is actually a sphere. The sphere is completely defined by the semi-major axis, which is the radius of the sphere.
    """

    class Meta:
        name = "secondDefiningParameter"
        namespace = "http://www.opengis.net/gml/3.2"

    second_defining_parameter: Optional[SecondDefiningParameter1] = field(
        default=None,
        metadata={
            "name": "SecondDefiningParameter",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class RelatedTimeType(TimePrimitivePropertyType):
    """Gml:RelatedTimeType provides a content model for indicating the relative
    position of an arbitrary member of the substitution group whose head is
    gml:AbstractTimePrimitive.

    It extends the generic gml:TimePrimitivePropertyType with an XML
    attribute relativePosition, whose value is selected from the set of
    13 temporal relationships identified by Allen (1983)
    """

    relative_position: Optional[RelatedTimeTypeRelativePosition] = field(
        default=None,
        metadata={
            "name": "relativePosition",
            "type": "Attribute",
        },
    )


@dataclass
class AxisDirection(CodeWithAuthorityType):
    """Gml:axisDirection is the direction of this coordinate system axis (or in the
    case of Cartesian projected coordinates, the direction of this coordinate
    system axis at the origin).

    Within any set of coordinate system axes, only one of each pair of
    terms may be used. For earth-fixed CRSs, this direction is often
    approximate and intended to provide a human interpretable meaning to
    the axis. When a geodetic datum is used, the precise directions of
    the axes may therefore vary slightly from this approximate
    direction. The codeSpace attribute shall reference a source of
    information specifying the values and meanings of all the allowed
    string values for this property.
    """

    class Meta:
        name = "axisDirection"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class Conversion(GeneralConversionPropertyType):
    """
    Gml:conversion is an association role to the coordinate conversion used to
    define the derived CRS.
    """

    class Meta:
        name = "conversion"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class Description(StringOrRefType):
    """The value of this property is a text description of the object.

    gml:description uses gml:StringOrRefType as its content model, so it
    may contain a simple text string content, or carry a reference to an
    external description. The use of gml:description to reference an
    external description has been deprecated and replaced by the
    gml:descriptionReference property.
    """

    class Meta:
        name = "description"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class DescriptionReference(ReferenceType):
    """The value of this property is a remote text description of the object.

    The xlink:href attribute of the gml:descriptionReference property
    references the external description.
    """

    class Meta:
        name = "descriptionReference"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class Identifier(CodeWithAuthorityType):
    """Often, a special identifier is assigned to an object by the maintaining
    authority with the intention that it is used in references to the object For
    such cases, the codeSpace shall be provided.

    That identifier is usually unique either globally or within an
    application domain. gml:identifier is a pre-defined property for
    such identifiers.
    """

    class Meta:
        name = "identifier"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class RangeMeaning(CodeWithAuthorityType):
    """Gml:rangeMeaning describes the meaning of axis value range specified by
    gml:minimumValue and gml:maximumValue.

    This element shall be omitted when both gml:minimumValue and
    gml:maximumValue are omitted. This element should be included when
    gml:minimumValue and/or gml:maximumValue are included. If this
    element is omitted when the gml:minimumValue and/or gml:maximumValue
    are included, the meaning is unspecified. The codeSpace attribute
    shall reference a source of information specifying the values and
    meanings of all the allowed string values for this property.
    """

    class Meta:
        name = "rangeMeaning"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class AbstractGmltype:
    class Meta:
        name = "AbstractGMLType"

    description: Optional[Description] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    description_reference: Optional[DescriptionReference] = field(
        default=None,
        metadata={
            "name": "descriptionReference",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    name: List[Name] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class AbstractTimeObjectType(AbstractGmltype):
    pass


@dataclass
class DefinitionBaseType(AbstractGmltype):
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class AbstractTimePrimitiveType(AbstractTimeObjectType):
    related_time: List[RelatedTimeType] = field(
        default_factory=list,
        metadata={
            "name": "relatedTime",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )


@dataclass
class DefinitionType(DefinitionBaseType):
    remarks: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )


@dataclass
class Definition(DefinitionType):
    """The basic gml:Definition element specifies a definition, which can be
    included in or referenced by a dictionary.

    The content model for a generic definition is a derivation from
    gml:AbstractGMLType. The gml:description property element shall hold
    the definition if this can be captured in a simple text string, or
    the gml:descriptionReference property element may carry a link to a
    description elsewhere. The gml:identifier element shall provide one
    identifier identifying this definition. The identifier shall be
    unique within the dictionaries using this definition. The gml:name
    elements shall provide zero or more terms and synonyms for which
    this is the definition. The gml:remarks element shall be used to
    hold additional textual information that is not conceptually part of
    the definition but is useful in understanding the definition.
    """

    class Meta:
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class IdentifiedObjectType(DefinitionType):
    """Gml:IdentifiedObjectType provides identification properties of a CRS-related
    object.

    In gml:DefinitionType, the gml:identifier element shall be the
    primary name by which this object is identified, encoding the "name"
    attribute in the UML model. Zero or more of the gml:name elements
    can be an unordered set of "identifiers", encoding the "identifier"
    attribute in the UML model. Each of these gml:name elements can
    reference elsewhere the object's defining information or be an
    identifier by which this object can be referenced. Zero or more
    other gml:name elements can be an unordered set of "alias"
    alternative names by which this CRS related object is identified,
    encoding the "alias" attributes in the UML model. An object may have
    several aliases, typically used in different contexts. The context
    for an alias is indicated by the value of its (optional) codeSpace
    attribute. Any needed version information shall be included in the
    codeSpace attribute of a gml:identifier and gml:name elements. In
    this use, the gml:remarks element in the gml:DefinitionType shall
    contain comments on or information about this object, including data
    source information.
    """


@dataclass
class AbstractCrstype(IdentifiedObjectType):
    class Meta:
        name = "AbstractCRSType"

    domain_of_validity: List[DomainOfValidity] = field(
        default_factory=list,
        metadata={
            "name": "domainOfValidity",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    scope: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "min_occurs": 1,
        },
    )


@dataclass
class AbstractDatumType(IdentifiedObjectType):
    domain_of_validity: Optional[DomainOfValidity] = field(
        default=None,
        metadata={
            "name": "domainOfValidity",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    scope: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "min_occurs": 1,
        },
    )
    anchor_definition: Optional[AnchorDefinition] = field(
        default=None,
        metadata={
            "name": "anchorDefinition",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    realization_epoch: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "realizationEpoch",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )


@dataclass
class CoordinateSystemAxisType(IdentifiedObjectType):
    axis_abbrev: Optional[AxisAbbrev] = field(
        default=None,
        metadata={
            "name": "axisAbbrev",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )
    axis_direction: Optional[AxisDirection] = field(
        default=None,
        metadata={
            "name": "axisDirection",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )
    minimum_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "minimumValue",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    maximum_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "maximumValue",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    range_meaning: Optional[RangeMeaning] = field(
        default=None,
        metadata={
            "name": "rangeMeaning",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )


@dataclass
class EllipsoidType(IdentifiedObjectType):
    semi_major_axis: Optional[float] = field(
        default=None,
        metadata={
            "name": "semiMajorAxis",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )
    second_defining_parameter: Optional[SecondDefiningParameter2] = field(
        default=None,
        metadata={
            "name": "secondDefiningParameter",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class PrimeMeridianType(IdentifiedObjectType):
    greenwich_longitude: Optional[float] = field(
        default=None,
        metadata={
            "name": "greenwichLongitude",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class AbstractGeneralDerivedCrstype(AbstractCrstype):
    class Meta:
        name = "AbstractGeneralDerivedCRSType"

    conversion: Optional[Conversion] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class CoordinateSystemAxis(CoordinateSystemAxisType):
    """
    Gml:CoordinateSystemAxis is a definition of a coordinate system axis.
    """

    class Meta:
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class Ellipsoid1(EllipsoidType):
    """A gml:Ellipsoid is a geometric figure that may be used to describe the
    approximate shape of the earth.

    In mathematical terms, it is a surface formed by the rotation of an
    ellipse about its minor axis.
    """

    class Meta:
        name = "Ellipsoid"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class PrimeMeridian1(PrimeMeridianType):
    """A gml:PrimeMeridian defines the origin from which longitude values are
    determined.

    The default value for the prime meridian gml:identifier value is
    "Greenwich".
    """

    class Meta:
        name = "PrimeMeridian"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class VerticalDatumType(AbstractDatumType):
    pass


@dataclass
class CoordinateSystemAxisPropertyType:
    """
    Gml:CoordinateSystemAxisPropertyType is a property type for association roles
    to a coordinate system axis, either referencing or containing the definition of
    that axis.
    """

    coordinate_system_axis: Optional[CoordinateSystemAxis] = field(
        default=None,
        metadata={
            "name": "CoordinateSystemAxis",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class EllipsoidPropertyType:
    """
    Gml:EllipsoidPropertyType is a property type for association roles to an
    ellipsoid, either referencing or containing the definition of that ellipsoid.
    """

    ellipsoid: Optional[Ellipsoid1] = field(
        default=None,
        metadata={
            "name": "Ellipsoid",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class PrimeMeridianPropertyType:
    """
    Gml:PrimeMeridianPropertyType is a property type for association roles to a
    prime meridian, either referencing or containing the definition of that
    meridian.
    """

    prime_meridian: Optional[PrimeMeridian1] = field(
        default=None,
        metadata={
            "name": "PrimeMeridian",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class VerticalDatum1(VerticalDatumType):
    """
    Gml:VerticalDatum is a textual description and/or a set of parameters
    identifying a particular reference level surface used as a zero-height surface,
    including its position with respect to the Earth for any of the height types
    recognized by this International Standard.
    """

    class Meta:
        name = "VerticalDatum"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class VerticalDatumPropertyType:
    """
    Gml:VerticalDatumPropertyType is property type for association roles to a
    vertical datum, either referencing or containing the definition of that datum.
    """

    vertical_datum: Optional[VerticalDatum1] = field(
        default=None,
        metadata={
            "name": "VerticalDatum",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class Axis(CoordinateSystemAxisPropertyType):
    """The gml:axis property is an association role (ordered sequence) to the
    coordinate system axes included in this coordinate system.

    The coordinate values in a coordinate tuple shall be recorded in the
    order in which the coordinate system axes associations are recorded,
    whenever those coordinates use a coordinate reference system that
    uses this coordinate system. The gml:AggregationAttributeGroup
    should be used to specify that the axis objects are ordered.
    """

    class Meta:
        name = "axis"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class Ellipsoid2(EllipsoidPropertyType):
    """
    Gml:ellipsoid is an association role to the ellipsoid used by this geodetic
    datum.
    """

    class Meta:
        name = "ellipsoid"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class PrimeMeridian2(PrimeMeridianPropertyType):
    """
    Gml:primeMeridian is an association role to the prime meridian used by this
    geodetic datum.
    """

    class Meta:
        name = "primeMeridian"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class AbstractCoordinateSystemType(IdentifiedObjectType):
    axis: List[Axis] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "min_occurs": 1,
        },
    )
    aggregation_type: Optional[AggregationType] = field(
        default=None,
        metadata={
            "name": "aggregationType",
            "type": "Attribute",
        },
    )


@dataclass
class GeodeticDatumType(AbstractDatumType):
    prime_meridian: Optional[PrimeMeridian2] = field(
        default=None,
        metadata={
            "name": "primeMeridian",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )
    ellipsoid: Optional[Ellipsoid2] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class VerticalDatum2(VerticalDatumPropertyType):
    """
    Gml:verticalDatum is an association role to the vertical datum used by this
    CRS.
    """

    class Meta:
        name = "verticalDatum"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class CartesianCstype(AbstractCoordinateSystemType):
    class Meta:
        name = "CartesianCSType"


@dataclass
class EllipsoidalCstype(AbstractCoordinateSystemType):
    class Meta:
        name = "EllipsoidalCSType"


@dataclass
class GeodeticDatum1(GeodeticDatumType):
    """
    Gml:GeodeticDatum is a geodetic datum defines the precise location and
    orientation in 3-dimensional space of a defined ellipsoid (or sphere), or of a
    Cartesian coordinate system centered in this ellipsoid (or sphere).
    """

    class Meta:
        name = "GeodeticDatum"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class SphericalCstype(AbstractCoordinateSystemType):
    class Meta:
        name = "SphericalCSType"


@dataclass
class VerticalCstype(AbstractCoordinateSystemType):
    class Meta:
        name = "VerticalCSType"


@dataclass
class CartesianCs1(CartesianCstype):
    """Gml:CartesianCS is a 1-, 2-, or 3-dimensional coordinate system.

    In the 1-dimensional case, it contains a single straight coordinate
    axis. In the 2- and 3-dimensional cases gives the position of points
    relative to orthogonal straight axes. In the multi-dimensional case,
    all axes shall have the same length unit of measure. A CartesianCS
    shall have one, two, or three gml:axis property elements.
    """

    class Meta:
        name = "CartesianCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class EllipsoidalCs1(EllipsoidalCstype):
    """Gml:EllipsoidalCS is a two- or three-dimensional coordinate system in which
    position is specified by geodetic latitude, geodetic longitude, and (in the
    three-dimensional case) ellipsoidal height.

    An EllipsoidalCS shall have two or three gml:axis property elements;
    the number of associations shall equal the dimension of the CS.
    """

    class Meta:
        name = "EllipsoidalCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class GeodeticDatumPropertyType:
    """
    Gml:GeodeticDatumPropertyType is a property type for association roles to a
    geodetic datum, either referencing or containing the definition of that datum.
    """

    geodetic_datum: Optional[GeodeticDatum1] = field(
        default=None,
        metadata={
            "name": "GeodeticDatum",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class SphericalCs1(SphericalCstype):
    """Gml:SphericalCS is a three-dimensional coordinate system with one distance
    measured from the origin and two angular coordinates.

    A SphericalCS shall have three gml:axis property elements.
    """

    class Meta:
        name = "SphericalCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class VerticalCs1(VerticalCstype):
    """Gml:VerticalCS is a one-dimensional coordinate system used to record the
    heights or depths of points.

    Such a coordinate system is usually dependent on the Earth's gravity
    field, perhaps loosely as when atmospheric pressure is the basis for
    the vertical coordinate system axis. A VerticalCS shall have one
    gml:axis property element.
    """

    class Meta:
        name = "VerticalCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class CartesianCspropertyType:
    """
    Gml:CartesianCSPropertyType is a property type for association roles to a
    Cartesian coordinate system, either referencing or containing the definition of
    that coordinate system.
    """

    class Meta:
        name = "CartesianCSPropertyType"

    cartesian_cs: Optional[CartesianCs1] = field(
        default=None,
        metadata={
            "name": "CartesianCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class EllipsoidalCspropertyType:
    """
    Gml:EllipsoidalCSPropertyType is a property type for association roles to an
    ellipsoidal coordinate system, either referencing or containing the definition
    of that coordinate system.
    """

    class Meta:
        name = "EllipsoidalCSPropertyType"

    ellipsoidal_cs: Optional[EllipsoidalCs1] = field(
        default=None,
        metadata={
            "name": "EllipsoidalCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class SphericalCspropertyType:
    """
    Gml:SphericalCSPropertyType is property type for association roles to a
    spherical coordinate system, either referencing or containing the definition of
    that coordinate system.
    """

    class Meta:
        name = "SphericalCSPropertyType"

    spherical_cs: Optional[SphericalCs1] = field(
        default=None,
        metadata={
            "name": "SphericalCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class VerticalCspropertyType:
    """
    Gml:VerticalCSPropertyType is a property type for association roles to a
    vertical coordinate system, either referencing or containing the definition of
    that coordinate system.
    """

    class Meta:
        name = "VerticalCSPropertyType"

    vertical_cs: Optional[VerticalCs1] = field(
        default=None,
        metadata={
            "name": "VerticalCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class GeodeticDatum2(GeodeticDatumPropertyType):
    """
    Gml:geodeticDatum is an association role to the geodetic datum used by this
    CRS.
    """

    class Meta:
        name = "geodeticDatum"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class CartesianCs2(CartesianCspropertyType):
    """
    Gml:cartesianCS is an association role to the Cartesian coordinate system used
    by this CRS.
    """

    class Meta:
        name = "cartesianCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class EllipsoidalCs2(EllipsoidalCspropertyType):
    """
    Gml:ellipsoidalCS is an association role to the ellipsoidal coordinate system
    used by this CRS.
    """

    class Meta:
        name = "ellipsoidalCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class SphericalCs2(SphericalCspropertyType):
    """
    Gml:sphericalCS is an association role to the spherical coordinate system used
    by this CRS.
    """

    class Meta:
        name = "sphericalCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class VerticalCs2(VerticalCspropertyType):
    """
    Gml:verticalCS is an association role to the vertical coordinate system used by
    this CRS.
    """

    class Meta:
        name = "verticalCS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class GeodeticCrstype(AbstractCrstype):
    """
    Gml:GeodeticCRS is a coordinate reference system based on a geodetic datum.
    """

    class Meta:
        name = "GeodeticCRSType"

    ellipsoidal_cs: Optional[EllipsoidalCs2] = field(
        default=None,
        metadata={
            "name": "ellipsoidalCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    cartesian_cs: Optional[CartesianCs2] = field(
        default=None,
        metadata={
            "name": "cartesianCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    spherical_cs: Optional[SphericalCs2] = field(
        default=None,
        metadata={
            "name": "sphericalCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    geodetic_datum: Optional[GeodeticDatum2] = field(
        default=None,
        metadata={
            "name": "geodeticDatum",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class VerticalCrstype(AbstractCrstype):
    class Meta:
        name = "VerticalCRSType"

    vertical_cs: Optional[VerticalCs2] = field(
        default=None,
        metadata={
            "name": "verticalCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )
    vertical_datum: Optional[VerticalDatum2] = field(
        default=None,
        metadata={
            "name": "verticalDatum",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class GeodeticCrs(GeodeticCrstype):
    class Meta:
        name = "GeodeticCRS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class VerticalCrs(VerticalCrstype):
    """Gml:VerticalCRS is a 1D coordinate reference system used for recording
    heights or depths.

    Vertical CRSs make use of the direction of gravity to define the
    concept of height or depth, but the relationship with gravity may
    not be straightforward. By implication, ellipsoidal heights (h)
    cannot be captured in a vertical coordinate reference system.
    Ellipsoidal heights cannot exist independently, but only as an
    inseparable part of a 3D coordinate tuple defined in a geographic 3D
    coordinate reference system.
    """

    class Meta:
        name = "VerticalCRS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class CrspropertyType:
    """
    Gml:CRSPropertyType is a property type for association roles to a CRS abstract
    coordinate reference system, either referencing or containing the definition of
    that CRS.
    """

    class Meta:
        name = "CRSPropertyType"

    vertical_crs: Optional[VerticalCrs] = field(
        default=None,
        metadata={
            "name": "VerticalCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    projected_crs: Optional[ProjectedCrs] = field(
        default=None,
        metadata={
            "name": "ProjectedCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    geodetic_crs: Optional[GeodeticCrs] = field(
        default=None,
        metadata={
            "name": "GeodeticCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class GeodeticCrspropertyType:
    """
    Gml:GeodeticCRSPropertyType is a property type for association roles to a
    geodetic coordinate reference system, either referencing or containing the
    definition of that reference system.
    """

    class Meta:
        name = "GeodeticCRSPropertyType"

    geodetic_crs: Optional[GeodeticCrs] = field(
        default=None,
        metadata={
            "name": "GeodeticCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    type_value: str = field(
        init=False,
        default="simple",
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    arcrole: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    show: Optional[ShowValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    actuate: Optional[ActuateValue] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/1999/xlink",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class BaseGeodeticCrs(GeodeticCrspropertyType):
    """
    Gml:baseGeodeticCRS is an association role to the geodetic coordinate reference
    system used by this projected CRS.
    """

    class Meta:
        name = "baseGeodeticCRS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class SourceCrs(CrspropertyType):
    """
    Gml:sourceCRS is an association role to the source CRS (coordinate reference
    system) of this coordinate operation.
    """

    class Meta:
        name = "sourceCRS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class TargetCrs(CrspropertyType):
    """
    Gml:targetCRS is an association role to the target CRS (coordinate reference
    system) of this coordinate operation.
    """

    class Meta:
        name = "targetCRS"
        namespace = "http://www.opengis.net/gml/3.2"


@dataclass
class AbstractCoordinateOperationType(IdentifiedObjectType):
    domain_of_validity: Optional[DomainOfValidity] = field(
        default=None,
        metadata={
            "name": "domainOfValidity",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    scope: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "min_occurs": 1,
        },
    )
    operation_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "operationVersion",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    coordinate_operation_accuracy: List[CoordinateOperationAccuracy] = field(
        default_factory=list,
        metadata={
            "name": "coordinateOperationAccuracy",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    source_crs: Optional[SourceCrs] = field(
        default=None,
        metadata={
            "name": "sourceCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )
    target_crs: Optional[TargetCrs] = field(
        default=None,
        metadata={
            "name": "targetCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
        },
    )


@dataclass
class ProjectedCrstype(AbstractGeneralDerivedCrstype):
    class Meta:
        name = "ProjectedCRSType"

    base_geodetic_crs: Optional[BaseGeodeticCrs] = field(
        default=None,
        metadata={
            "name": "baseGeodeticCRS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )
    cartesian_cs: Optional[CartesianCs2] = field(
        default=None,
        metadata={
            "name": "cartesianCS",
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class AbstractGeneralConversionType(AbstractCoordinateOperationType):
    operation_version: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    source_crs: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    target_crs: Any = field(
        init=False,
        metadata={
            "type": "Ignore",
        },
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.opengis.net/gml/3.2",
            "required": True,
        },
    )


@dataclass
class ProjectedCrs(ProjectedCrstype):
    """Gml:ProjectedCRS is a 2D coordinate reference system used to approximate the
    shape of the earth on a planar surface, but in such a way that the distortion
    that is inherent to the approximation is carefully controlled and known.

    Distortion correction is commonly applied to calculated bearings and
    distances to produce values that are a close match to actual field
    values.
    """

    class Meta:
        name = "ProjectedCRS"
        namespace = "http://www.opengis.net/gml/3.2"
