from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Union
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlPeriod
from generated.eml.v2_2.mod_3 import NilReasonEnumerationValue
from generated.eml.v2_2.gmd import (
    CiDateTypeCode,
    CiOnLineFunctionCode,
    CiPresentationFormCode,
    CiRoleCode,
    DqEvaluationMethodTypeCode,
)

__NAMESPACE__ = "http://www.isotc211.org/2005/gco"


@dataclass
class AbstractObjectType:
    class Meta:
        name = "AbstractObject_Type"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class Boolean:
    class Meta:
        namespace = "http://www.isotc211.org/2005/gco"

    value: Optional[bool] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class CharacterString:
    class Meta:
        namespace = "http://www.isotc211.org/2005/gco"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class CodeListValueType:
    class Meta:
        name = "CodeListValue_Type"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    code_list: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeList",
            "type": "Attribute",
            "required": True,
        },
    )
    code_list_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "codeListValue",
            "type": "Attribute",
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


@dataclass
class Date:
    class Meta:
        nillable = True
        namespace = "http://www.isotc211.org/2005/gco"

    value: Optional[Union[XmlDate, XmlPeriod]] = field(
        default=None,
        metadata={
            "nillable": True,
        },
    )


@dataclass
class DateTime:
    class Meta:
        namespace = "http://www.isotc211.org/2005/gco"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class Real:
    class Meta:
        namespace = "http://www.isotc211.org/2005/gco"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class BooleanPropertyType:
    class Meta:
        name = "Boolean_PropertyType"

    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gco",
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
class CharacterStringPropertyType:
    class Meta:
        name = "CharacterString_PropertyType"

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
    ci_presentation_form_code: Optional[CiPresentationFormCode] = field(
        default=None,
        metadata={
            "name": "CI_PresentationFormCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    ci_role_code: Optional[CiRoleCode] = field(
        default=None,
        metadata={
            "name": "CI_RoleCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    ci_on_line_function_code: Optional[CiOnLineFunctionCode] = field(
        default=None,
        metadata={
            "name": "CI_OnLineFunctionCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    ci_date_type_code: Optional[CiDateTypeCode] = field(
        default=None,
        metadata={
            "name": "CI_DateTypeCode",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gmd",
        },
    )
    character_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "CharacterString",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gco",
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
class DateTimePropertyType:
    class Meta:
        name = "DateTime_PropertyType"

    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gco",
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
class DatePropertyType:
    class Meta:
        name = "Date_PropertyType"

    date: Optional[Union[XmlDate, XmlPeriod]] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gco",
            "nillable": True,
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gco",
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
class RealPropertyType:
    class Meta:
        name = "Real_PropertyType"

    real: Optional[float] = field(
        default=None,
        metadata={
            "name": "Real",
            "type": "Element",
            "namespace": "http://www.isotc211.org/2005/gco",
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
