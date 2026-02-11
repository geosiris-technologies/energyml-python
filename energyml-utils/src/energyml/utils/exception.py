# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from typing import Optional


class DetailedNotImplementedError(Exception):
    """Exception for not implemented functions"""

    def __init__(self, msg):
        super().__init__(msg)


class MissingExtraInstallation(DetailedNotImplementedError):
    """Exception for missing extra installation"""

    def __init__(self, extra_name):
        super().__init__(msg=f"Missing energml-utils extras installation '{extra_name}'")


class NoCrsError(Exception):
    pass


class ObjectNotFoundNotError(Exception):
    def __init__(self, obj_id):
        super().__init__(f"Object id: {obj_id}")


class UnknownTypeFromQualifiedType(Exception):
    def __init__(self, qt: Optional[str] = None):
        super().__init__(f"not matchable qualified type: {qt}")


class NotParsableType(Exception):
    def __init__(self, t: Optional[str] = None):
        super().__init__(f"type: {t}")


class UnparsableFile(Exception):
    def __init__(self, t: Optional[str] = None):
        super().__init__("File is not parsable for an EPC file. Please use RawFile class for non energyml files.")


class NotSupportedError(Exception):
    """Exception for not supported features"""

    def __init__(self, msg):
        super().__init__(msg)


# EPC Validation Exceptions


class EpcValidationError(Exception):
    """Base exception for EPC validation errors."""

    def __init__(self, message: str, details: Optional[dict] = None):
        """Initialize EPC validation error.

        Args:
            message: Error message describing the validation failure.
            details: Optional dictionary with additional error context.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class ZipIntegrityError(EpcValidationError):
    """Exception raised when ZIP container integrity check fails."""

    pass


class MissingRequiredFileError(EpcValidationError):
    """Exception raised when required EPC files are missing."""

    pass


class InvalidXmlStructureError(EpcValidationError):
    """Exception raised when XML structure is invalid."""

    pass


class RelationshipValidationError(EpcValidationError):
    """Exception raised when relationship validation fails."""

    pass


class NamingConventionError(EpcValidationError):
    """Exception raised when naming conventions are violated."""

    pass


class ContentTypeValidationError(EpcValidationError):
    """Exception raised when content type validation fails."""

    pass


class CorePropertiesValidationError(EpcValidationError):
    """Exception raised when core properties validation fails."""

    pass


class NotUriError(Exception):
    def __init__(self, uri: Optional[str] = None):
        super().__init__(f"Not a valid URI: {uri}")
