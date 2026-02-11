# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
EPC (Energistics Packaging Conventions) Validator Module.

This module provides comprehensive validation for EPC v1.0 files according to
the Energistics Packaging Conventions specification. It validates:
- ZIP container integrity
- Presence and validity of Core Properties
- Content Types XML structure and validity
- Relationships (.rels) consistency
- Compliance with EPC naming conventions and structure
"""

import logging
import re
import zipfile
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from energyml.opc.opc import CoreProperties, Override, Relationship, Relationships, Types
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.exceptions import ParserError

from .constants import RELS_CONTENT_TYPE, EpcExportVersion
from .exception import (
    ContentTypeValidationError,
    CorePropertiesValidationError,
    EpcValidationError,
    InvalidXmlStructureError,
    MissingRequiredFileError,
    NamingConventionError,
    RelationshipValidationError,
    ZipIntegrityError,
)

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Results from EPC validation.

    Attributes:
        is_valid: Whether the EPC file passed validation.
        errors: List of critical errors that prevent file from being valid.
        warnings: List of non-critical issues that should be reviewed.
        info: List of informational messages about the validation.
    """

    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error and mark validation as failed.

        Args:
            message: Error message to add.
        """
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message.

        Args:
            message: Warning message to add.
        """
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        """Add an informational message.

        Args:
            message: Info message to add.
        """
        self.info.append(message)

    def __str__(self) -> str:
        """Return formatted validation result."""
        lines = [f"Validation Result: {'PASSED' if self.is_valid else 'FAILED'}"]
        if self.errors:
            lines.append(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  - {error}")
        if self.warnings:
            lines.append(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        if self.info:
            lines.append(f"\nInfo ({len(self.info)}):")
            for info in self.info:
                lines.append(f"  - {info}")
        return "\n".join(lines)


class EpcParser:
    """Parser for EPC file components.

    This class handles parsing of EPC files without performing validation.
    It extracts and parses the various components of an EPC file.
    """

    def __init__(self, epc_path: Union[str, Path, BytesIO]):
        """Initialize EPC parser.

        Args:
            epc_path: Path to EPC file or BytesIO object containing EPC data.

        Raises:
            FileNotFoundError: If the specified file doesn't exist.
            ZipIntegrityError: If the file is not a valid ZIP archive.
        """
        self.epc_path = epc_path
        self._zip_file: Optional[zipfile.ZipFile] = None
        self._content_types: Optional[Types] = None
        self._core_properties: Optional[CoreProperties] = None
        self._relationships: Dict[str, Relationships] = {}
        self._xml_parser = XmlParser()

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def open(self) -> None:
        """Open the EPC ZIP file.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ZipIntegrityError: If the file is not a valid ZIP archive.
        """
        try:
            if isinstance(self.epc_path, BytesIO):
                self._zip_file = zipfile.ZipFile(self.epc_path, "r")
            else:
                path = Path(self.epc_path)
                if not path.exists():
                    raise FileNotFoundError(f"EPC file not found: {self.epc_path}")
                self._zip_file = zipfile.ZipFile(path, "r")
        except zipfile.BadZipFile as e:
            raise ZipIntegrityError(f"Invalid ZIP file: {e}") from e

    def close(self) -> None:
        """Close the ZIP file."""
        if self._zip_file:
            self._zip_file.close()
            self._zip_file = None

    def list_files(self) -> List[str]:
        """List all files in the EPC archive.

        Returns:
            List of file paths within the archive.

        Raises:
            ZipIntegrityError: If ZIP file is not open.
        """
        if not self._zip_file:
            raise ZipIntegrityError("ZIP file is not open")
        return self._zip_file.namelist()

    def read_file(self, path: str) -> bytes:
        """Read a file from the EPC archive.

        Args:
            path: Path to file within the archive.

        Returns:
            File contents as bytes.

        Raises:
            MissingRequiredFileError: If the file doesn't exist in the archive.
        """
        if not self._zip_file:
            raise ZipIntegrityError("ZIP file is not open")
        try:
            return self._zip_file.read(path)
        except KeyError as e:
            raise MissingRequiredFileError(f"File not found in archive: {path}") from e

    def parse_content_types(self) -> Types:
        """Parse [Content_Types].xml file.

        Returns:
            Parsed Types object.

        Raises:
            MissingRequiredFileError: If [Content_Types].xml is missing.
            InvalidXmlStructureError: If XML is malformed.
        """
        if self._content_types is not None:
            return self._content_types

        content_types_path = "[Content_Types].xml"
        try:
            xml_content = self.read_file(content_types_path)
            self._content_types = self._xml_parser.from_bytes(xml_content, Types)
            return self._content_types
        except MissingRequiredFileError:
            raise
        except (ParserError, Exception) as e:
            raise InvalidXmlStructureError(
                f"Failed to parse {content_types_path}: {e}",
                details={"file": content_types_path},
            ) from e

    def parse_core_properties(self, core_props_path: str = "docProps/core.xml") -> Optional[CoreProperties]:
        """Parse core properties XML file.

        Args:
            core_props_path: Path to core properties file.

        Returns:
            Parsed CoreProperties object or None if file doesn't exist.

        Raises:
            InvalidXmlStructureError: If XML is malformed.
        """
        if self._core_properties is not None:
            return self._core_properties

        try:
            xml_content = self.read_file(core_props_path)
            self._core_properties = self._xml_parser.from_bytes(xml_content, CoreProperties)
            return self._core_properties
        except MissingRequiredFileError:
            return None
        except (ParserError, Exception) as e:
            raise InvalidXmlStructureError(
                f"Failed to parse {core_props_path}: {e}",
                details={"file": core_props_path},
            ) from e

    def parse_relationships(self, rels_path: str) -> Relationships:
        """Parse a relationships file.

        Args:
            rels_path: Path to .rels file.

        Returns:
            Parsed Relationships object.

        Raises:
            InvalidXmlStructureError: If XML is malformed.
        """
        if rels_path in self._relationships:
            return self._relationships[rels_path]

        try:
            xml_content = self.read_file(rels_path)
            relationships = self._xml_parser.from_bytes(xml_content, Relationships)
            self._relationships[rels_path] = relationships
            return relationships
        except MissingRequiredFileError:
            # Return empty relationships if file doesn't exist
            return Relationships(relationship=[])
        except (ParserError, Exception) as e:
            raise InvalidXmlStructureError(
                f"Failed to parse {rels_path}: {e}",
                details={"file": rels_path},
            ) from e

    def find_all_rels_files(self) -> List[str]:
        """Find all .rels files in the archive.

        Returns:
            List of paths to .rels files.
        """
        if not self._zip_file:
            raise ZipIntegrityError("ZIP file is not open")
        return [f for f in self._zip_file.namelist() if f.endswith(".rels")]


class EpcValidator:
    """Validator for EPC (Energistics Packaging Conventions) files.

    This class provides comprehensive validation of EPC v1.0 files according
    to the Energistics Packaging Conventions specification.

    Example:
        >>> validator = EpcValidator("my_file.epc")
        >>> result = validator.validate()
        >>> if result.is_valid:
        ...     print("EPC file is valid!")
        ... else:
        ...     print("Validation errors:")
        ...     for error in result.errors:
        ...         print(f"  - {error}")
    """

    # Required EPC files
    REQUIRED_FILES = ["[Content_Types].xml", "_rels/.rels"]

    # Core properties content type
    CORE_PROPS_CONTENT_TYPE = "application/vnd.openxmlformats-package.core-properties+xml"

    # Correct relationships content type (note: the constant RELS_CONTENT_TYPE in constants.py is incorrect)
    RELS_CONTENT_TYPE_CORRECT = "application/vnd.openxmlformats-package.relationships+xml"

    # Valid EPC object content type patterns
    ENERGYML_CONTENT_TYPE_PATTERN = re.compile(r"^application/x-(resqml|witsml|prodml)\+xml;version=\d+\.\d+;type=obj_")

    def __init__(
        self,
        epc_path: Union[str, Path, BytesIO],
        strict: bool = True,
        check_relationships: bool = True,
    ):
        """Initialize EPC validator.

        Args:
            epc_path: Path to EPC file or BytesIO object.
            strict: If True, enforce strict validation rules.
            check_relationships: If True, validate relationship consistency.
        """
        self.epc_path = epc_path
        self.strict = strict
        self.check_relationships = check_relationships
        self.parser = EpcParser(epc_path)
        self.result = ValidationResult()

    def validate(self) -> ValidationResult:
        """Perform comprehensive EPC validation.

        Returns:
            ValidationResult with validation outcome and any issues found.
        """
        try:
            with self.parser:
                self._validate_zip_integrity()
                self._validate_required_files()
                self._validate_content_types()
                self._validate_core_properties()

                if self.check_relationships:
                    self._validate_relationships()

                self._validate_naming_conventions()

            if self.result.is_valid:
                self.result.add_info("EPC file validation passed successfully")

        except EpcValidationError as e:
            self.result.add_error(str(e))
        except Exception as e:
            self.result.add_error(f"Unexpected error during validation: {e}")
            logger.exception("Unexpected validation error")

        return self.result

    def _validate_zip_integrity(self) -> None:
        """Validate ZIP container integrity.

        Raises:
            ZipIntegrityError: If ZIP structure is corrupt.
        """
        try:
            # Test ZIP integrity by attempting to list files
            files = self.parser.list_files()
            self.result.add_info(f"ZIP container contains {len(files)} files")

            # Check for directory entries
            directories = [f for f in files if f.endswith("/")]
            if directories:
                self.result.add_info(f"Found {len(directories)} directory entries")

        except Exception as e:
            raise ZipIntegrityError(f"ZIP integrity check failed: {e}") from e

    def _validate_required_files(self) -> None:
        """Validate presence of required EPC files.

        Raises:
            MissingRequiredFileError: If required files are missing.
        """
        files = self.parser.list_files()
        files_lower = {f.lower(): f for f in files}

        for required_file in self.REQUIRED_FILES:
            # Case-insensitive check
            if required_file.lower() not in files_lower:
                raise MissingRequiredFileError(
                    f"Required file missing: {required_file}",
                    details={"file": required_file},
                )
            self.result.add_info(f"Found required file: {required_file}")

    def _validate_content_types(self) -> None:
        """Validate [Content_Types].xml structure and content.

        Raises:
            ContentTypeValidationError: If content types are invalid.
        """
        try:
            content_types = self.parser.parse_content_types()

            # Validate that .rels extension has correct content type
            rels_default = None
            if content_types.default:
                for default in content_types.default:
                    if default.extension == "rels":
                        rels_default = default
                        if default.content_type != self.RELS_CONTENT_TYPE_CORRECT:
                            self.result.add_warning(
                                f"Non-standard content type for .rels files: {default.content_type}. "
                                f"Expected: {self.RELS_CONTENT_TYPE_CORRECT}"
                            )
                        break

            if not rels_default:
                self.result.add_warning("No default content type defined for .rels files")

            # Validate overrides
            if content_types.override:
                self.result.add_info(f"Found {len(content_types.override)} content type overrides")

                energyml_objects = 0
                core_props_found = False

                for override in content_types.override:
                    # Check for core properties
                    if override.content_type == self.CORE_PROPS_CONTENT_TYPE:
                        core_props_found = True
                        self.result.add_info(f"Core properties defined at: {override.part_name}")

                    # Check for Energyml objects
                    elif override.content_type and self.ENERGYML_CONTENT_TYPE_PATTERN.match(override.content_type):
                        energyml_objects += 1

                    # Validate part name format
                    if override.part_name and not override.part_name.startswith("/"):
                        if self.strict:
                            self.result.add_error(f"Part name must start with '/': {override.part_name}")
                        else:
                            self.result.add_warning(f"Part name should start with '/': {override.part_name}")

                self.result.add_info(f"Found {energyml_objects} Energyml objects")

                if not core_props_found:
                    self.result.add_warning("No core properties override found in content types")

            else:
                self.result.add_warning("No content type overrides defined")

        except InvalidXmlStructureError:
            raise
        except Exception as e:
            raise ContentTypeValidationError(f"Content types validation failed: {e}") from e

    def _validate_core_properties(self) -> None:
        """Validate core properties file.

        Raises:
            CorePropertiesValidationError: If core properties are invalid.
        """
        try:
            # Try different possible paths for core properties
            core_props_paths = [
                "docProps/core.xml",
                "/docProps/core.xml",
                "metadata/core.xml",
                "/metadata/core.xml",
            ]

            core_props = None
            found_path = None

            for path in core_props_paths:
                core_props = self.parser.parse_core_properties(path)
                if core_props:
                    found_path = path
                    break

            if not core_props:
                if self.strict:
                    raise CorePropertiesValidationError("Core properties file not found")
                else:
                    self.result.add_warning("Core properties file not found")
                    return

            self.result.add_info(f"Found core properties at: {found_path}")

            # Validate core properties content
            if hasattr(core_props, "creator") and core_props.creator:
                self.result.add_info(f"Creator: {core_props.creator}")
            else:
                self.result.add_warning("Core properties missing 'creator' field")

            if hasattr(core_props, "created") and core_props.created:
                self.result.add_info("Core properties contain creation date")
            else:
                self.result.add_warning("Core properties missing 'created' field")

        except InvalidXmlStructureError:
            raise
        except Exception as e:
            raise CorePropertiesValidationError(f"Core properties validation failed: {e}") from e

    def _validate_relationships(self) -> None:
        """Validate relationships consistency.

        Raises:
            RelationshipValidationError: If relationships are invalid.
        """
        try:
            # Find all .rels files
            rels_files = self.parser.find_all_rels_files()
            self.result.add_info(f"Found {len(rels_files)} relationship files")

            all_files = set(self.parser.list_files())
            relationship_targets: Set[str] = set()

            for rels_file in rels_files:
                try:
                    relationships = self.parser.parse_relationships(rels_file)

                    if not relationships.relationship:
                        self.result.add_warning(f"Empty relationships file: {rels_file}")
                        continue

                    for rel in relationships.relationship:
                        # Validate relationship has required attributes
                        if not rel.id or rel.id.strip() == "":
                            self.result.add_error(f"Relationship missing or has empty 'Id' in {rels_file}")

                        if not rel.type_value:
                            self.result.add_error(f"Relationship missing 'Type' in {rels_file}")

                        if not rel.target:
                            self.result.add_error(f"Relationship missing 'Target' in {rels_file}")
                            continue

                        # Check if target exists (for internal targets)
                        if not rel.target.startswith("http"):
                            # Normalize target path
                            target = rel.target.lstrip("/")
                            relationship_targets.add(target)

                            if target not in all_files:
                                # Check with leading slash
                                target_with_slash = "/" + target
                                if target_with_slash not in all_files:
                                    self.result.add_error(
                                        f"Relationship target not found: {rel.target} (from {rels_file})"
                                    )

                except InvalidXmlStructureError as e:
                    self.result.add_error(f"Invalid relationships file {rels_file}: {e}")

        except Exception as e:
            raise RelationshipValidationError(f"Relationships validation failed: {e}") from e

    def _validate_naming_conventions(self) -> None:
        """Validate EPC naming conventions.

        Raises:
            NamingConventionError: If naming conventions are violated.
        """
        try:
            files = self.parser.list_files()

            # Check for invalid characters in file names
            invalid_chars = ["\\", ":", "*", "?", '"', "<", ">", "|"]

            for file_path in files:
                # Check for invalid characters
                for char in invalid_chars:
                    if char in file_path:
                        self.result.add_error(f"Invalid character '{char}' in file path: {file_path}")

                # Check _rels folder naming
                if "_rels" in file_path and not file_path.startswith("_rels/"):
                    parts = file_path.split("/")
                    valid_rels = any(i > 0 and parts[i] == "_rels" and parts[i - 1] != "" for i in range(len(parts)))
                    if not valid_rels and file_path != "_rels/.rels":
                        self.result.add_warning(f"Unusual _rels folder location: {file_path}")

                # Check .rels file naming
                if file_path.endswith(".rels"):
                    if not file_path.endswith("/.rels"):
                        # Should be in _rels folder with corresponding source file
                        if "/_rels/" not in file_path:
                            self.result.add_warning(f"Relationship file not in _rels folder: {file_path}")

        except Exception as e:
            raise NamingConventionError(f"Naming convention validation failed: {e}") from e


def validate_epc_file(
    epc_path: Union[str, Path, BytesIO],
    strict: bool = True,
    check_relationships: bool = True,
) -> ValidationResult:
    """Convenience function to validate an EPC file.

    Args:
        epc_path: Path to EPC file or BytesIO object.
        strict: If True, enforce strict validation rules.
        check_relationships: If True, validate relationship consistency.

    Returns:
        ValidationResult with validation outcome.

    Example:
        >>> result = validate_epc_file("my_file.epc")
        >>> print(result)
    """
    validator = EpcValidator(epc_path, strict=strict, check_relationships=check_relationships)
    return validator.validate()
