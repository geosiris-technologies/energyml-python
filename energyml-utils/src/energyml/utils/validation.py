# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import re
from dataclasses import dataclass, field, Field
from enum import Enum
from typing import Any, List

from .epc import (
    get_obj_identifier,
    Epc,
)
from .introspection import (
    get_class_fields,
    get_object_attribute,
    search_attribute_matching_type_with_path,
    get_object_attribute_no_verif,
    get_object_attribute_rgx,
    get_matching_class_attribute_name,
    get_obj_uuid,
    get_obj_version,
    get_content_type_from_class,
    get_qualified_type_from_class,
    is_enum, get_object_uri,
)

class ErrorType(Enum):
    CRITICAL = "critical"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"


@dataclass
class ValidationError:

    msg: str = field(default="Validation error")

    error_type: ErrorType = field(default=ErrorType.INFO)

    def __str__(self):
        return f"[{str(self.error_type).upper()}] : {self.msg}"

    def toJson(self):
        return {
            "msg": self.msg,
            "error_type": self.error_type.value,
        }


@dataclass
class ValidationObjectError(ValidationError):

    target_obj: Any = field(default=None)

    attribute_dot_path: str = field(default=None)

    def __str__(self):
        return f"{ValidationError.__str__(self)}\n\t{get_obj_identifier(self.target_obj)} : '{self.attribute_dot_path}'"

    def toJson(self):
        return super().toJson() | {"target_obj": str(get_object_uri(self.target_obj)), "attribute_dot_path": self.attribute_dot_path}


@dataclass
class MandatoryError(ValidationObjectError):
    def __str__(self):
        return f"{ValidationError.__str__(self)}\n\tMandatory value is None for {get_obj_identifier(self.target_obj)} : '{self.attribute_dot_path}'"


@dataclass
class MissingEntityError(ValidationObjectError):
    missing_uuid: str = field(default=None)

    def __str__(self):
        return f"{ValidationError.__str__(self)}\n\tMissing entity in {get_obj_identifier(self.target_obj)} at path '{self.attribute_dot_path}'. Missing entity uuid: {self.missing_uuid}"


def validate_epc(epc: Epc) -> List[ValidationError]:
    """
    Verify if all :param:`epc`'s objects are valid.
    :param epc:
    :return:
    """
    errs = []
    for obj in epc.energyml_objects:
        errs = errs + patterns_validation(obj)

    errs = errs + dor_validation(epc.energyml_objects)

    return errs


def dor_validation(energyml_objects: List[Any]) -> List[ValidationError]:
    """
    Verification for DOR. An error is raised if DORs contains wrong information, or if a referenced object is unknown
    in the :param:`epc`.
    :param energyml_objects:
    :return:
    """
    errs = []

    dict_obj_identifier = {get_obj_identifier(obj): obj for obj in energyml_objects}
    dict_obj_uuid = {}
    for obj in energyml_objects:
        uuid = get_obj_uuid(obj)
        if uuid not in dict_obj_uuid:
            dict_obj_uuid[uuid] = []
        dict_obj_uuid[uuid].append(obj)

    # TODO: chercher dans les objets les AbstractObject (en Witsml des sous objet peuvent etre aussi references)

    for obj in energyml_objects:
        dor_list = search_attribute_matching_type_with_path(obj, "DataObjectReference")
        for dor_path, dor in dor_list:
            dor_target_id = get_obj_identifier(dor)
            if dor_target_id not in dict_obj_identifier:
                dor_uuid = get_obj_uuid(dor)
                dor_version = get_obj_version(dor)
                if dor_uuid not in dict_obj_uuid:
                    errs.append(
                        MissingEntityError(
                            error_type=ErrorType.CRITICAL,
                            target_obj=obj,
                            attribute_dot_path=dor_path,
                            missing_uuid=dor_uuid
                            # msg=f"[DOR ERR] has wrong information. Unkown object with uuid '{dor_uuid}'",
                        )
                    )
                else:
                    accessible_version = [get_obj_version(ref_obj) for ref_obj in dict_obj_uuid[dor_uuid]]
                    errs.append(
                        ValidationObjectError(
                            error_type=ErrorType.CRITICAL,
                            target_obj=obj,
                            attribute_dot_path=dor_path,
                            msg=f"[DOR ERR] has wrong information. Unkown object version '{dor_version}'. "
                            f"Version must be one of {accessible_version}",
                        )
                    )
            else:
                target = dict_obj_identifier[dor_target_id]
                target_title = get_object_attribute_rgx(target, "citation.title")
                target_content_type = get_content_type_from_class(target)
                target_qualified_type = get_qualified_type_from_class(target)

                dor_title = get_object_attribute_rgx(dor, "title")

                if dor_title != target_title:
                    errs.append(
                        ValidationObjectError(
                            error_type=ErrorType.CRITICAL,
                            target_obj=obj,
                            attribute_dot_path=dor_path,
                            msg=f"[DOR ERR] has wrong information. Title should be '{target_title}' and not '{dor_title}'",
                        )
                    )

                if get_matching_class_attribute_name(dor, "content_type") is not None:
                    dor_content_type = get_object_attribute_no_verif(dor, "content_type")
                    if dor_content_type != target_content_type:
                        errs.append(
                            ValidationObjectError(
                                error_type=ErrorType.CRITICAL,
                                target_obj=obj,
                                attribute_dot_path=dor_path,
                                msg=f"[DOR ERR] has wrong information. ContentType should be '{target_content_type}' and not '{dor_content_type}'",
                            )
                        )

                if get_matching_class_attribute_name(dor, "qualified_type") is not None:
                    dor_qualified_type = get_object_attribute_no_verif(dor, "qualified_type")
                    if dor_qualified_type != target_qualified_type:
                        errs.append(
                            ValidationObjectError(
                                error_type=ErrorType.CRITICAL,
                                target_obj=obj,
                                attribute_dot_path=dor_path,
                                msg=f"[DOR ERR] has wrong information. QualifiedType should be '{target_qualified_type}' and not '{dor_qualified_type}'",
                            )
                        )

    return errs


def patterns_validation(obj: Any) -> List[ValidationError]:
    """
    Verification on object values, using the patterns defined in the original energyml xsd files.
    :param obj:
    :return:
    """
    return _patterns_validation(obj, obj, "")


def _patterns_validation(obj: Any, root_obj: Any, current_attribute_dot_path: str = "") -> List[ValidationError]:
    """
    Verification on object values, using the patterns defined in the original energyml xsd files.
    :param obj:
    :param root_obj:
    :param current_attribute_dot_path:
    :return:
    """
    error_list = []

    if isinstance(obj, list):
        cpt = 0
        for val in obj:
            error_list = error_list + _patterns_validation(val, root_obj, f"{current_attribute_dot_path}.{cpt}")
            cpt = cpt + 1
    elif isinstance(obj, dict):
        for k, val in obj.items():
            error_list = error_list + _patterns_validation(val, root_obj, f"{current_attribute_dot_path}.{k}")
    else:
        # logging.debug(get_class_fields(obj))
        for att_name, att_field in get_class_fields(obj).items():
            # logging.debug(f"att_name : {att_field.metadata}")
            error_list = error_list + validate_attribute(
                get_object_attribute(obj, att_name, False),
                root_obj,
                att_field,
                f"{current_attribute_dot_path}.{att_name}",
            )

    return error_list


def validate_attribute(value: Any, root_obj: Any, att_field: Field, path: str) -> List[ValidationError]:
    errs = []

    if value is None:
        if att_field.metadata.get("required", False):
            errs.append(
                MandatoryError(
                    error_type=ErrorType.CRITICAL,
                    target_obj=root_obj,
                    attribute_dot_path=path,
                )
            )
    elif not is_enum(value):  # sometimes enums values fails the validation
        min_length = att_field.metadata.get("min_length", None)
        max_length = att_field.metadata.get("max_length", None)
        pattern = att_field.metadata.get("pattern", None)
        min_occurs = att_field.metadata.get("min_occurs", None)
        min_inclusive = att_field.metadata.get("min_inclusive", None)
        # white_space

        if max_length is not None:
            length = len(value)
            if length > max_length:
                errs.append(
                    ValidationObjectError(
                        error_type=ErrorType.CRITICAL,
                        target_obj=root_obj,
                        attribute_dot_path=path,
                        msg=f"Max length was {max_length} but found {length}",
                    )
                )

        if min_length is not None:
            length = len(value)
            if length < min_length:
                errs.append(
                    ValidationObjectError(
                        error_type=ErrorType.CRITICAL,
                        target_obj=root_obj,
                        attribute_dot_path=path,
                        msg=f"Max length was {min_length} but found {length}",
                    )
                )

        if min_occurs is not None:
            if isinstance(value, list) and min_occurs > len(value):
                errs.append(
                    ValidationObjectError(
                        error_type=ErrorType.CRITICAL,
                        target_obj=root_obj,
                        attribute_dot_path=path,
                        msg=f"Min occurs was {min_occurs} but found {len(value)}",
                    )
                )

        if min_inclusive is not None:
            potential_err = ValidationObjectError(
                error_type=ErrorType.CRITICAL,
                target_obj=root_obj,
                attribute_dot_path=path,
                msg=f"Min occurs was {min_inclusive} but found {value}",
            )
            if isinstance(value, list):
                for val in value:
                    if (isinstance(val, str) and len(val) > min_inclusive) or (
                        (isinstance(val, int) or isinstance(val, float)) and val > min_inclusive
                    ):
                        errs.append(potential_err)

        if pattern is not None:
            if not isinstance(value, list):
                testing_value_list = [value]
            else:
                testing_value_list = value

            for v in testing_value_list:
                if is_enum(v):
                    v = v.value
                if re.match(pattern, v) is None:
                    errs.append(
                        ValidationObjectError(
                            error_type=ErrorType.CRITICAL,
                            target_obj=root_obj,
                            attribute_dot_path=path,
                            msg=f"Pattern error. Value '{v}' was supposed to respect pattern '{pattern}'",
                        )
                    )

    return errs + _patterns_validation(
        obj=value,
        root_obj=root_obj,
        current_attribute_dot_path=path,
    )


def correct_dor(energyml_objects: List[Any]) -> None:
    """
    Fix DOR errors (missing object_version, wrong title, wrong content-type/qualified-type ...)
    :param energyml_objects:
    :return:
    """
    dict_obj_identifier = {get_obj_identifier(obj): obj for obj in energyml_objects}
    dict_obj_uuid = {}
    for obj in energyml_objects:
        uuid = get_obj_uuid(obj)
        if uuid not in dict_obj_uuid:
            dict_obj_uuid[uuid] = []
        dict_obj_uuid[uuid].append(obj)

    # TODO: chercher dans les objets les AbstractObject (en Witsml des sous objet peuvent etre aussi references)

    for obj in energyml_objects:
        dor_list = search_attribute_matching_type_with_path(obj, "DataObjectReference")
        for dor_path, dor in dor_list:
            dor_target_id = get_obj_identifier(dor)
            if dor_target_id in dict_obj_identifier:
                target = dict_obj_identifier[dor_target_id]
                target_title = get_object_attribute_rgx(target, "citation.title")
                target_content_type = get_content_type_from_class(target)
                target_qualified_type = get_qualified_type_from_class(target)

                dor_title = get_object_attribute_rgx(dor, "title")

                if dor_title != target_title:
                    dor.title = target_title

                if get_matching_class_attribute_name(dor, "content_type") is not None:
                    dor_content_type = get_object_attribute_no_verif(dor, "content_type")
                    if dor_content_type != target_content_type:
                        dor.content_type = target_content_type

                if get_matching_class_attribute_name(dor, "qualified_type") is not None:
                    dor_qualified_type = get_object_attribute_no_verif(dor, "qualified_type")
                    if dor_qualified_type != target_qualified_type:
                        dor.qualified_type = target_qualified_type
