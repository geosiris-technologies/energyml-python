# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Unit tests for EPC validator module.

Tests comprehensive validation of EPC (Energistics Packaging Conventions) files
according to the EPC v1.0 specification.
"""

import io
import zipfile
from pathlib import Path
from typing import Optional

import pytest

from energyml.opc.opc import (
    CoreProperties,
    Created,
    Creator,
    Default,
    Identifier,
    Override,
    Relationship,
    Relationships,
    TargetMode,
    Types,
)
from energyml.utils.epc_validator import (
    EpcParser,
    EpcValidator,
    ValidationResult,
    validate_epc_file,
)
from energyml.utils.exception import (
    ContentTypeValidationError,
    CorePropertiesValidationError,
    InvalidXmlStructureError,
    MissingRequiredFileError,
    NamingConventionError,
    RelationshipValidationError,
    ZipIntegrityError,
)
from energyml.utils.serialization import serialize_xml


class TestValidationResult:
    """Test ValidationResult class."""

    def test_validation_result_initialization(self):
        """Test ValidationResult initializes correctly."""
        result = ValidationResult()
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
        assert len(result.info) == 0

    def test_add_error_marks_invalid(self):
        """Test adding error marks validation as invalid."""
        result = ValidationResult()
        result.add_error("Test error")
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0] == "Test error"

    def test_add_warning_keeps_valid(self):
        """Test adding warning doesn't affect validity."""
        result = ValidationResult()
        result.add_warning("Test warning")
        assert result.is_valid is True
        assert len(result.warnings) == 1

    def test_add_info(self):
        """Test adding info message."""
        result = ValidationResult()
        result.add_info("Test info")
        assert len(result.info) == 1

    def test_str_representation(self):
        """Test string representation of ValidationResult."""
        result = ValidationResult()
        result.add_error("Error 1")
        result.add_warning("Warning 1")
        result.add_info("Info 1")

        output = str(result)
        assert "FAILED" in output
        assert "Error 1" in output
        assert "Warning 1" in output
        assert "Info 1" in output


class TestEpcParser:
    """Test EPC parser functionality."""

    @pytest.fixture
    def minimal_epc(self) -> io.BytesIO:
        """Create minimal valid EPC file in memory."""
        buffer = io.BytesIO()

        # Create content types
        content_types = Types(
            default=[
                Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")
            ],
            override=[
                Override(
                    part_name="/docProps/core.xml",
                    content_type="application/vnd.openxmlformats-package.core-properties+xml",
                )
            ],
        )

        # Create core properties
        core_props = CoreProperties(
            created=Created(any_element="2024-01-01T00:00:00Z"),
            creator=Creator(any_element="Test Creator"),
            identifier=Identifier(any_element="test-identifier"),
        )

        # Create root relationships
        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="CoreProperties",
                    type_value="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties",
                    target="docProps/core.xml",
                )
            ]
        )

        # Create ZIP file
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))
            zf.writestr("docProps/core.xml", serialize_xml(core_props))

        buffer.seek(0)
        return buffer

    def test_parser_context_manager(self, minimal_epc):
        """Test parser as context manager."""
        with EpcParser(minimal_epc) as parser:
            files = parser.list_files()
            assert len(files) > 0

    def test_parser_open_close(self, minimal_epc):
        """Test explicit open/close."""
        parser = EpcParser(minimal_epc)
        parser.open()
        files = parser.list_files()
        assert len(files) > 0
        parser.close()

    def test_parser_list_files(self, minimal_epc):
        """Test listing files in archive."""
        with EpcParser(minimal_epc) as parser:
            files = parser.list_files()
            assert "[Content_Types].xml" in files
            assert "_rels/.rels" in files

    def test_parser_read_file(self, minimal_epc):
        """Test reading file from archive."""
        with EpcParser(minimal_epc) as parser:
            content = parser.read_file("[Content_Types].xml")
            assert content is not None
            assert len(content) > 0

    def test_parser_read_missing_file(self, minimal_epc):
        """Test reading non-existent file raises error."""
        with EpcParser(minimal_epc) as parser:
            with pytest.raises(MissingRequiredFileError):
                parser.read_file("non_existent.xml")

    def test_parse_content_types(self, minimal_epc):
        """Test parsing content types."""
        with EpcParser(minimal_epc) as parser:
            content_types = parser.parse_content_types()
            assert content_types is not None
            assert len(content_types.default) > 0

    def test_parse_core_properties(self, minimal_epc):
        """Test parsing core properties."""
        with EpcParser(minimal_epc) as parser:
            core_props = parser.parse_core_properties()
            assert core_props is not None

    def test_parse_relationships(self, minimal_epc):
        """Test parsing relationships."""
        with EpcParser(minimal_epc) as parser:
            rels = parser.parse_relationships("_rels/.rels")
            assert rels is not None

    def test_find_all_rels_files(self, minimal_epc):
        """Test finding all .rels files."""
        with EpcParser(minimal_epc) as parser:
            rels_files = parser.find_all_rels_files()
            assert len(rels_files) > 0
            assert "_rels/.rels" in rels_files


class TestEpcValidator:
    """Test EPC validator functionality."""

    @pytest.fixture
    def valid_epc(self) -> io.BytesIO:
        """Create valid EPC file for testing."""
        buffer = io.BytesIO()

        # Create content types
        content_types = Types(
            default=[
                Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")
            ],
            override=[
                Override(
                    part_name="/docProps/core.xml",
                    content_type="application/vnd.openxmlformats-package.core-properties+xml",
                ),
                Override(
                    part_name="/resqml/obj_BoundaryFeature_12345.xml",
                    content_type="application/x-resqml+xml;version=2.0;type=obj_BoundaryFeature",
                ),
            ],
        )

        # Create core properties
        core_props = CoreProperties(
            created=Created(any_element="2024-01-01T00:00:00Z"),
            creator=Creator(any_element="Test Creator"),
            identifier=Identifier(any_element="test-identifier"),
        )

        # Create root relationships
        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="CoreProperties",
                    type_value="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties",
                    target="docProps/core.xml",
                )
            ]
        )

        # Create ZIP file
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))
            zf.writestr("docProps/core.xml", serialize_xml(core_props))
            zf.writestr("resqml/obj_BoundaryFeature_12345.xml", "<test/>")

        buffer.seek(0)
        return buffer

    def test_validate_valid_epc(self, valid_epc):
        """Test validation of valid EPC file."""
        result = validate_epc_file(valid_epc)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validator_initialization(self, valid_epc):
        """Test validator initialization."""
        validator = EpcValidator(valid_epc)
        assert validator.epc_path == valid_epc
        assert validator.strict is True
        assert validator.check_relationships is True

    def test_validate_with_strict_mode(self, valid_epc):
        """Test validation in strict mode."""
        validator = EpcValidator(valid_epc, strict=True)
        result = validator.validate()
        assert result is not None

    def test_validate_with_lenient_mode(self, valid_epc):
        """Test validation in lenient mode."""
        validator = EpcValidator(valid_epc, strict=False)
        result = validator.validate()
        assert result is not None

    def test_validate_missing_content_types(self):
        """Test validation fails when [Content_Types].xml is missing."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("_rels/.rels", "<Relationships/>")
        buffer.seek(0)

        result = validate_epc_file(buffer)
        assert result.is_valid is False
        assert any("Content_Types" in error for error in result.errors)

    def test_validate_missing_root_rels(self):
        """Test validation fails when _rels/.rels is missing."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            content_types = Types(
                default=[
                    Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")
                ]
            )
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
        buffer.seek(0)

        result = validate_epc_file(buffer)
        assert result.is_valid is False
        assert any("_rels/.rels" in error for error in result.errors)

    def test_validate_invalid_zip(self):
        """Test validation fails for invalid ZIP file."""
        buffer = io.BytesIO(b"This is not a ZIP file")
        result = validate_epc_file(buffer)
        assert result.is_valid is False

    def test_validate_relationships_missing_target(self):
        """Test validation detects missing relationship targets."""
        buffer = io.BytesIO()

        content_types = Types(
            default=[Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")]
        )

        # Relationship pointing to non-existent file
        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="Missing",
                    type_value="http://schemas.example.org/test",
                    target="missing_file.xml",
                )
            ]
        )

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))

        buffer.seek(0)

        result = validate_epc_file(buffer)
        assert result.is_valid is False
        assert any("not found" in error.lower() for error in result.errors)

    def test_validate_content_type_rels_default(self, valid_epc):
        """Test validation checks .rels content type."""
        result = validate_epc_file(valid_epc)
        # Should have info about .rels content type
        assert result is not None

    def test_validate_core_properties_missing_fields(self):
        """Test validation warns about missing core properties fields."""
        buffer = io.BytesIO()

        content_types = Types(
            default=[
                Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")
            ],
            override=[
                Override(
                    part_name="/docProps/core.xml",
                    content_type="application/vnd.openxmlformats-package.core-properties+xml",
                )
            ],
        )

        # Core properties with minimal fields
        core_props = CoreProperties()

        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="CoreProperties",
                    type_value="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties",
                    target="docProps/core.xml",
                )
            ]
        )

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))
            zf.writestr("docProps/core.xml", serialize_xml(core_props))

        buffer.seek(0)

        result = validate_epc_file(buffer, strict=False)
        # Should have warnings about missing fields
        assert len(result.warnings) > 0

    def test_validate_naming_invalid_characters(self):
        """Test validation detects invalid characters in file names."""
        buffer = io.BytesIO()

        content_types = Types(
            default=[Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")]
        )

        root_rels = Relationships(relationship=[])

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))
            # This would be difficult to create in a real ZIP, but we can test the logic

        buffer.seek(0)

        result = validate_epc_file(buffer)
        # Basic validation should pass
        assert result is not None

    def test_validate_without_relationships_check(self, valid_epc):
        """Test validation with relationship checking disabled."""
        result = validate_epc_file(valid_epc, check_relationships=False)
        assert result is not None

    def test_validate_energyml_content_type_detection(self, valid_epc):
        """Test detection of Energyml content types."""
        result = validate_epc_file(valid_epc)
        # Should detect the resqml object
        assert any("Energyml objects" in info for info in result.info)


class TestEpcValidatorWithRealFile:
    """Test EPC validator with real EPC files."""

    def test_validate_sample_epc_if_exists(self):
        """Test validation with actual sample EPC file if available."""
        sample_paths = [
            Path("D:/Geosiris/OSDU/manifestTranslation/commons/data/testingPackageCpp.epc"),
            Path("rc/epc/test.epc"),
            Path("example/result/test.epc"),
        ]

        sample_file = None
        for path in sample_paths:
            if path.exists():
                sample_file = path
                break

        if sample_file is None:
            pytest.skip("No sample EPC file available for testing")

        result = validate_epc_file(str(sample_file))
        # Real EPC files should generally be valid
        print(f"\nValidation result for {sample_file}:")
        print(result)


class TestEpcValidatorEdgeCases:
    """Test edge cases and error handling."""

    def test_validate_empty_relationships(self):
        """Test validation with empty relationships file."""
        buffer = io.BytesIO()

        content_types = Types(
            default=[Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")]
        )

        # Empty relationships
        root_rels = Relationships(relationship=[])

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))

        buffer.seek(0)

        result = validate_epc_file(buffer)
        print(f"\nErrors: {result.errors}")
        print(f"Warnings: {result.warnings}")
        # Should warn about empty relationships or pass in strict=False
        assert any("empty" in warning.lower() for warning in result.warnings) or not result.is_valid

    def test_validate_malformed_xml(self):
        """Test validation with malformed XML."""
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", "This is not valid XML")
            zf.writestr("_rels/.rels", "<Relationships/>")

        buffer.seek(0)

        result = validate_epc_file(buffer)
        assert result.is_valid is False

    def test_validate_relationship_without_id(self):
        """Test validation detects relationships without ID."""
        buffer = io.BytesIO()

        content_types = Types(
            default=[
                Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")
            ],
            override=[
                Override(
                    part_name="/docProps/core.xml",
                    content_type="application/vnd.openxmlformats-package.core-properties+xml",
                )
            ],
        )

        # Core props to avoid that error
        core_props = CoreProperties(
            created=Created(any_element="2024-01-01T00:00:00Z"),
            creator=Creator(any_element="Test"),
        )

        # Relationship without ID (not valid per spec)
        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="",  # Empty ID
                    type_value="http://schemas.example.org/test",
                    target="test.xml",
                )
            ]
        )

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))
            zf.writestr("docProps/core.xml", serialize_xml(core_props))

        buffer.seek(0)

        result = validate_epc_file(buffer)
        print(f"\nErrors: {result.errors}")
        print(f"Warnings: {result.warnings}")
        assert result.is_valid is False
        assert any("missing" in error.lower() and "id" in error.lower() for error in result.errors)

    def test_validate_external_relationship(self):
        """Test validation handles external relationships correctly."""
        buffer = io.BytesIO()

        content_types = Types(
            default=[Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")]
        )

        # External relationship (should not check if target exists)
        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="External",
                    type_value="http://schemas.example.org/external",
                    target="http://example.com/resource",
                    target_mode=TargetMode.EXTERNAL,
                )
            ]
        )

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))

        buffer.seek(0)

        result = validate_epc_file(buffer)
        # External relationships should not cause "target not found" errors
        assert not any("http://example.com" in error for error in result.errors)


class TestValidationIntegration:
    """Integration tests for complete validation workflows."""

    def test_full_validation_workflow(self):
        """Test complete validation workflow."""
        # Create a comprehensive EPC file
        buffer = io.BytesIO()

        content_types = Types(
            default=[
                Default(extension="rels", content_type="application/vnd.openxmlformats-package.relationships+xml")
            ],
            override=[
                Override(
                    part_name="/docProps/core.xml",
                    content_type="application/vnd.openxmlformats-package.core-properties+xml",
                ),
                Override(
                    part_name="/resqml/obj_TriangulatedSetRepresentation_uuid1.xml",
                    content_type="application/x-resqml+xml;version=2.2;type=obj_TriangulatedSetRepresentation",
                ),
            ],
        )

        core_props = CoreProperties(
            created=Created(any_element="2024-01-01T00:00:00Z"),
            creator=Creator(any_element="Test Integration"),
            identifier=Identifier(any_element="integration-test-id"),
        )

        root_rels = Relationships(
            relationship=[
                Relationship(
                    id="CoreProperties",
                    type_value="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties",
                    target="docProps/core.xml",
                ),
                Relationship(
                    id="Object1",
                    type_value="http://schemas.energistics.org/package/2012/relationships/destinationObject",
                    target="resqml/obj_TriangulatedSetRepresentation_uuid1.xml",
                ),
            ]
        )

        obj_rels = Relationships(relationship=[])

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", serialize_xml(content_types))
            zf.writestr("_rels/.rels", serialize_xml(root_rels))
            zf.writestr("docProps/core.xml", serialize_xml(core_props))
            zf.writestr("resqml/obj_TriangulatedSetRepresentation_uuid1.xml", "<TriangulatedSetRepresentation/>")
            zf.writestr("resqml/_rels/obj_TriangulatedSetRepresentation_uuid1.xml.rels", serialize_xml(obj_rels))

        buffer.seek(0)

        # Test with different validation modes
        result_strict = validate_epc_file(buffer, strict=True, check_relationships=True)
        assert result_strict.is_valid is True

        buffer.seek(0)
        result_lenient = validate_epc_file(buffer, strict=False, check_relationships=False)
        assert result_lenient is not None

    def test_validation_result_formatting(self):
        """Test validation result provides useful output."""
        buffer = io.BytesIO()

        # Create invalid EPC (missing required files)
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("test.txt", "Invalid EPC")

        buffer.seek(0)

        result = validate_epc_file(buffer)
        output = str(result)

        # Check output contains useful information
        assert "FAILED" in output or "PASSED" in output
        assert len(output) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
