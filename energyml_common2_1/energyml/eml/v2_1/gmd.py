from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Union
from generated.eml.v2_1.gsr import ScCrsPropertyType
from generated.eml.v2_1.mod_3 import NilReasonEnumerationValue
from generated.eml.v2_1.gco import (
    AbstractObjectType,
    BooleanPropertyType,
    CharacterStringPropertyType,
    CodeListValueType,
    DateTimePropertyType,
    DatePropertyType,
    RealPropertyType,
)
from generated.eml.v2_1.gts import TmPrimitivePropertyType
from generated.eml.v2_1.xlink import (
    ActuateValue,
    ShowValue,
)

__NAMESPACE__ = "http://www.isotc211.org/2005/gmd"


@dataclass
class Url:
    class Meta:
        name = "URL"
        namespace = "http://www.isotc211.org/2005/gmd"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class AbstractDqResultType(AbstractObjectType):
    class Meta:
        name = "AbstractDQ_Result_Type"


@dataclass
class AbstractExGeographicExtentType(AbstractObjectType):
    """
    Geographic area of the dataset.
    """

    class Meta:
        name = "AbstractEX_GeographicExtent_Type"

    extent_type_code: Optional[BooleanPropertyType] = field(
        default=None,
        metadata={
            "name": "extentTypeCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiAddressType(AbstractObjectType):
    """
    Location of the responsible individual or organisation.
    """

    class Meta:
        name = "CI_Address_Type"

    delivery_point: List[CharacterStringPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "deliveryPoint",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    city: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    administrative_area: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "administrativeArea",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    postal_code: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "postalCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    country: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    electronic_mail_address: List[CharacterStringPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "electronicMailAddress",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiDateTypeCode(CodeListValueType):
    class Meta:
        name = "CI_DateTypeCode"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiOnLineFunctionCode(CodeListValueType):
    class Meta:
        name = "CI_OnLineFunctionCode"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiPresentationFormCode(CodeListValueType):
    class Meta:
        name = "CI_PresentationFormCode"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiRoleCode(CodeListValueType):
    class Meta:
        name = "CI_RoleCode"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiSeriesType(AbstractObjectType):
    class Meta:
        name = "CI_Series_Type"

    name: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    issue_identification: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "issueIdentification",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    page: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiTelephoneType(AbstractObjectType):
    """
    Telephone numbers for contacting the responsible individual or organisation.
    """

    class Meta:
        name = "CI_Telephone_Type"

    voice: List[CharacterStringPropertyType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    facsimile: List[CharacterStringPropertyType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class DqEvaluationMethodTypeCode(CodeListValueType):
    class Meta:
        name = "DQ_EvaluationMethodTypeCode"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class DqResultPropertyType:
    class Meta:
        name = "DQ_Result_PropertyType"

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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ExGeographicExtentPropertyType:
    class Meta:
        name = "EX_GeographicExtent_PropertyType"

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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ExTemporalExtentType(AbstractObjectType):
    """
    Time period covered by the content of the dataset.
    """

    class Meta:
        name = "EX_TemporalExtent_Type"

    extent: Optional[TmPrimitivePropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )


@dataclass
class ExVerticalExtentType(AbstractObjectType):
    """
    Vertical domain of dataset.
    """

    class Meta:
        name = "EX_VerticalExtent_Type"

    minimum_value: Optional[RealPropertyType] = field(
        default=None,
        metadata={
            "name": "minimumValue",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )
    maximum_value: Optional[RealPropertyType] = field(
        default=None,
        metadata={
            "name": "maximumValue",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )
    vertical_crs: Optional[ScCrsPropertyType] = field(
        default=None,
        metadata={
            "name": "verticalCRS",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )


@dataclass
class UrlPropertyType:
    class Meta:
        name = "URL_PropertyType"

    url: Optional[str] = field(
        default=None,
        metadata={
            "name": "URL",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiAddress(CiAddressType):
    class Meta:
        name = "CI_Address"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiDateTypeCodePropertyType:
    class Meta:
        name = "CI_DateTypeCode_PropertyType"

    ci_date_type_code: Optional[CiDateTypeCode] = field(
        default=None,
        metadata={
            "name": "CI_DateTypeCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiOnLineFunctionCodePropertyType:
    class Meta:
        name = "CI_OnLineFunctionCode_PropertyType"

    ci_on_line_function_code: Optional[CiOnLineFunctionCode] = field(
        default=None,
        metadata={
            "name": "CI_OnLineFunctionCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiPresentationFormCodePropertyType:
    class Meta:
        name = "CI_PresentationFormCode_PropertyType"

    ci_presentation_form_code: Optional[CiPresentationFormCode] = field(
        default=None,
        metadata={
            "name": "CI_PresentationFormCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiRoleCodePropertyType:
    class Meta:
        name = "CI_RoleCode_PropertyType"

    ci_role_code: Optional[CiRoleCode] = field(
        default=None,
        metadata={
            "name": "CI_RoleCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiSeries(CiSeriesType):
    class Meta:
        name = "CI_Series"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiTelephone(CiTelephoneType):
    class Meta:
        name = "CI_Telephone"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class DqEvaluationMethodTypeCodePropertyType:
    class Meta:
        name = "DQ_EvaluationMethodTypeCode_PropertyType"

    dq_evaluation_method_type_code: Optional[
        DqEvaluationMethodTypeCode
    ] = field(
        default=None,
        metadata={
            "name": "DQ_EvaluationMethodTypeCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ExTemporalExtent(ExTemporalExtentType):
    class Meta:
        name = "EX_TemporalExtent"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class ExVerticalExtent(ExVerticalExtentType):
    class Meta:
        name = "EX_VerticalExtent"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiAddressPropertyType:
    class Meta:
        name = "CI_Address_PropertyType"

    ci_address: Optional[CiAddress] = field(
        default=None,
        metadata={
            "name": "CI_Address",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiDateType(AbstractObjectType):
    class Meta:
        name = "CI_Date_Type"

    date: Optional[DatePropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )
    date_type: Optional[CiDateTypeCodePropertyType] = field(
        default=None,
        metadata={
            "name": "dateType",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )


@dataclass
class CiOnlineResourceType(AbstractObjectType):
    """
    Information about online sources from which the dataset, specification, or
    community profile name and extended metadata elements can be obtained.
    """

    class Meta:
        name = "CI_OnlineResource_Type"

    linkage: Optional[UrlPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )
    protocol: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    application_profile: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "applicationProfile",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    name: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    description: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    function: Optional[CiOnLineFunctionCodePropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiSeriesPropertyType:
    class Meta:
        name = "CI_Series_PropertyType"

    ci_series: Optional[CiSeries] = field(
        default=None,
        metadata={
            "name": "CI_Series",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiTelephonePropertyType:
    class Meta:
        name = "CI_Telephone_PropertyType"

    ci_telephone: Optional[CiTelephone] = field(
        default=None,
        metadata={
            "name": "CI_Telephone",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ExTemporalExtentPropertyType:
    class Meta:
        name = "EX_TemporalExtent_PropertyType"

    ex_temporal_extent: Optional[ExTemporalExtent] = field(
        default=None,
        metadata={
            "name": "EX_TemporalExtent",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ExVerticalExtentPropertyType:
    class Meta:
        name = "EX_VerticalExtent_PropertyType"

    ex_vertical_extent: Optional[ExVerticalExtent] = field(
        default=None,
        metadata={
            "name": "EX_VerticalExtent",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiDate(CiDateType):
    class Meta:
        name = "CI_Date"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiOnlineResource(CiOnlineResourceType):
    class Meta:
        name = "CI_OnlineResource"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class ExExtentType(AbstractObjectType):
    """
    Information about spatial, vertical, and temporal extent.
    """

    class Meta:
        name = "EX_Extent_Type"

    description: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    geographic_element: List[ExGeographicExtentPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "geographicElement",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    temporal_element: List[ExTemporalExtentPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "temporalElement",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    vertical_element: List[ExVerticalExtentPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "verticalElement",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiDatePropertyType:
    class Meta:
        name = "CI_Date_PropertyType"

    ci_date: Optional[CiDate] = field(
        default=None,
        metadata={
            "name": "CI_Date",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiOnlineResourcePropertyType:
    class Meta:
        name = "CI_OnlineResource_PropertyType"

    ci_online_resource: Optional[CiOnlineResource] = field(
        default=None,
        metadata={
            "name": "CI_OnlineResource",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class ExExtent(ExExtentType):
    class Meta:
        name = "EX_Extent"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiContactType(AbstractObjectType):
    """
    Information required enabling contact with the  responsible person and/or
    organisation.
    """

    class Meta:
        name = "CI_Contact_Type"

    phone: Optional[CiTelephonePropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    address: Optional[CiAddressPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    online_resource: Optional[CiOnlineResourcePropertyType] = field(
        default=None,
        metadata={
            "name": "onlineResource",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    hours_of_service: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "hoursOfService",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    contact_instructions: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "contactInstructions",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiContact(CiContactType):
    class Meta:
        name = "CI_Contact"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiContactPropertyType:
    class Meta:
        name = "CI_Contact_PropertyType"

    ci_contact: Optional[CiContact] = field(
        default=None,
        metadata={
            "name": "CI_Contact",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiResponsiblePartyType(AbstractObjectType):
    """
    Identification of, and means of communication with, person(s) and organisations
    associated with the dataset.
    """

    class Meta:
        name = "CI_ResponsibleParty_Type"

    individual_name: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "individualName",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    organisation_name: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "organisationName",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    position_name: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "positionName",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    contact_info: Optional[CiContactPropertyType] = field(
        default=None,
        metadata={
            "name": "contactInfo",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    role: Optional[CiRoleCodePropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )


@dataclass
class CiResponsibleParty(CiResponsiblePartyType):
    class Meta:
        name = "CI_ResponsibleParty"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiResponsiblePartyPropertyType:
    class Meta:
        name = "CI_ResponsibleParty_PropertyType"

    ci_responsible_party: Optional[CiResponsibleParty] = field(
        default=None,
        metadata={
            "name": "CI_ResponsibleParty",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class CiCitationType(AbstractObjectType):
    """
    Standardized resource reference.
    """

    class Meta:
        name = "CI_Citation_Type"

    title: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )
    alternate_title: List[CharacterStringPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "alternateTitle",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    date: List[CiDatePropertyType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "min_occurs": 1,
        },
    )
    edition: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    edition_date: Optional[DatePropertyType] = field(
        default=None,
        metadata={
            "name": "editionDate",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    identifier: List[MdIdentifierPropertyType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    cited_responsible_party: List[CiResponsiblePartyPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "citedResponsibleParty",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    presentation_form: List[CiPresentationFormCodePropertyType] = field(
        default_factory=list,
        metadata={
            "name": "presentationForm",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    series: Optional[CiSeriesPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    other_citation_details: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "otherCitationDetails",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    collective_title: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "collectiveTitle",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    isbn: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "ISBN",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    issn: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "ISSN",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )


@dataclass
class CiCitation(CiCitationType):
    class Meta:
        name = "CI_Citation"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class CiCitationPropertyType:
    class Meta:
        name = "CI_Citation_PropertyType"

    ci_citation: Optional[CiCitation] = field(
        default=None,
        metadata={
            "name": "CI_Citation",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class MdIdentifierType(AbstractObjectType):
    class Meta:
        name = "MD_Identifier_Type"

    authority: Optional[CiCitationPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    code: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "required": True,
        },
    )


@dataclass
class MdIdentifier(MdIdentifierType):
    class Meta:
        name = "MD_Identifier"
        namespace = "http://www.isotc211.org/2005/gmd"


@dataclass
class MdIdentifierPropertyType:
    class Meta:
        name = "MD_Identifier_PropertyType"

    md_identifier: Optional[MdIdentifier] = field(
        default=None,
        metadata={
            "name": "MD_Identifier",
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
    uuidref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    nil_reason: Optional[Union[str, NilReasonEnumerationValue]] = field(
        default=None,
        metadata={
            "name": "nilReason",
            "type": "Attribute",
            "namespace": "http://www.isotc211.org/2005/gco",
            "pattern": r"other:\w{2,}",
        },
    )


@dataclass
class AbstractDqElementType(AbstractObjectType):
    class Meta:
        name = "AbstractDQ_Element_Type"

    name_of_measure: List[CharacterStringPropertyType] = field(
        default_factory=list,
        metadata={
            "name": "nameOfMeasure",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    measure_identification: Optional[MdIdentifierPropertyType] = field(
        default=None,
        metadata={
            "name": "measureIdentification",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    measure_description: Optional[CharacterStringPropertyType] = field(
        default=None,
        metadata={
            "name": "measureDescription",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    evaluation_method_type: Optional[
        DqEvaluationMethodTypeCodePropertyType
    ] = field(
        default=None,
        metadata={
            "name": "evaluationMethodType",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    evaluation_method_description: Optional[
        CharacterStringPropertyType
    ] = field(
        default=None,
        metadata={
            "name": "evaluationMethodDescription",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    evaluation_procedure: Optional[CiCitationPropertyType] = field(
        default=None,
        metadata={
            "name": "evaluationProcedure",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    date_time: List[DateTimePropertyType] = field(
        default_factory=list,
        metadata={
            "name": "dateTime",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    result: List[DqResultPropertyType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
            "min_occurs": 1,
            "max_occurs": 2,
        },
    )


@dataclass
class AbstractDqPositionalAccuracyType(AbstractDqElementType):
    class Meta:
        name = "AbstractDQ_PositionalAccuracy_Type"
