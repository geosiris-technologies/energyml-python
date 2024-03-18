import re
from dataclasses import dataclass, field, Field
from enum import Enum
from typing import Any, List

from src.energyml.utils.epc import (
    get_obj_identifier,
)
from src.energyml.utils.introspection import (
    get_class_fields,
    get_object_attribute,
    search_attribute_matching_type_with_path,
    get_object_attribute_no_verif,
    get_object_attribute_rgx,
    get_matching_class_attribute_name, get_obj_uuid, get_obj_version, get_content_type_from_class,
    get_qualified_type_from_class,
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


@dataclass
class ValidationObjectError(ValidationError):

    target_obj: Any = field(default=None)

    attribute_dot_path: str = field(default=None)

    def __str__(self):
        return f"{ValidationError.__str__(self)}\n\t{get_obj_identifier(self.target_obj)} : '{self.attribute_dot_path}'"


@dataclass
class MandatoryError(ValidationObjectError):
    def __str__(self):
        return f"{ValidationError.__str__(self)}\n\tMandatory value is None for {get_obj_identifier(self.target_obj)} : '{self.attribute_dot_path}'"


def dor_verification(energyml_objects: List[Any]) -> List[ValidationError]:
    errs = []

    dict_obj_identifier = {
        get_obj_identifier(obj): obj for obj in energyml_objects
    }
    dict_obj_uuid = {}
    for obj in energyml_objects:
        uuid = get_obj_uuid(obj)
        if uuid not in dict_obj_uuid:
            dict_obj_uuid[uuid] = []
        dict_obj_uuid[uuid].append(obj)

    # TODO: chercher dans les objets les AbstractObject (en Witsml des sous objet peuvent etre aussi references)

    for obj in energyml_objects:
        dor_list = search_attribute_matching_type_with_path(
            obj, "DataObjectReference"
        )
        for dor_path, dor in dor_list:
            dor_target_id = get_obj_identifier(dor)
            if dor_target_id not in dict_obj_identifier:
                dor_uuid = get_obj_uuid(dor)
                dor_version = get_obj_version(dor)
                if dor_uuid not in dict_obj_uuid:
                    errs.append(
                        ValidationObjectError(
                            error_type=ErrorType.CRITICAL,
                            target_obj=obj,
                            attribute_dot_path=dor_path,
                            msg=f"[DOR ERR] has wrong information. Unkown object with uuid '{dor_uuid}'",
                        )
                    )
                else:
                    accessible_version = [
                        get_obj_version(ref_obj)
                        for ref_obj in dict_obj_uuid[dor_uuid]
                    ]
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
                target_title = get_object_attribute_rgx(
                    target, "citation.title"
                )
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

                if (
                    get_matching_class_attribute_name(dor, "content_type")
                    is not None
                ):
                    dor_content_type = get_object_attribute_no_verif(
                        dor, "content_type"
                    )
                    if dor_content_type != target_content_type:
                        errs.append(
                            ValidationObjectError(
                                error_type=ErrorType.CRITICAL,
                                target_obj=obj,
                                attribute_dot_path=dor_path,
                                msg=f"[DOR ERR] has wrong information. ContentType should be '{target_content_type}' and not '{dor_content_type}'",
                            )
                        )

                if (
                    get_matching_class_attribute_name(dor, "qualified_type")
                    is not None
                ):
                    dor_qualified_type = get_object_attribute_no_verif(
                        dor, "qualified_type"
                    )
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


def patterns_verification(obj: Any) -> List[ValidationError]:
    return _patterns_verification(obj, obj, "")


def _patterns_verification(
    obj: Any, root_obj: Any, current_attribute_dot_path: str = ""
) -> List[ValidationError]:
    error_list = []

    if isinstance(obj, list):
        cpt = 0
        for val in obj:
            error_list = error_list + _patterns_verification(
                val, root_obj, f"{current_attribute_dot_path}.{cpt}"
            )
            cpt = cpt + 1
    elif isinstance(obj, dict):
        for k, val in obj.items():
            error_list = error_list + _patterns_verification(
                val, root_obj, f"{current_attribute_dot_path}.{k}"
            )
    else:
        # print(get_class_fields(obj))
        for att_name, att_field in get_class_fields(obj).items():
            # print(f"att_name : {att_field.metadata}")
            error_list = error_list + validate_attribute(
                get_object_attribute(obj, att_name, False),
                root_obj,
                att_field,
                f"{current_attribute_dot_path}.{att_name}",
            )

    return error_list


def validate_attribute(
    value: Any, root_obj: Any, att_field: Field, path: str
) -> List[ValidationError]:
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
    else:
        min_length = att_field.metadata.get("min_length", None)
        max_length = att_field.metadata.get("max_length", None)
        pattern = att_field.metadata.get("pattern", None)
        # white_space
        # min_occurs
        # min_inclusive

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

        if pattern is not None:
            if re.match(pattern, value) is None:
                errs.append(
                    ValidationObjectError(
                        error_type=ErrorType.CRITICAL,
                        target_obj=root_obj,
                        attribute_dot_path=path,
                        msg=f"Pattern error. Value '{value}' was supposed to respect pattern '{pattern}'",
                    )
                )

    return errs + _patterns_verification(
        obj=value,
        root_obj=root_obj,
        current_attribute_dot_path=path,
    )
