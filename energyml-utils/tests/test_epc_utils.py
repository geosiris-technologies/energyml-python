# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

"""
Comprehensive unit tests for epc_utils module.
Excludes EPC structure validation and property kind functions as per requirements.
"""

import pytest
from pathlib import Path

from energyml.utils.epc_utils import (
    gen_core_props_rels_path,
    gen_core_props_path,
    gen_energyml_object_path,
    gen_rels_path,
    gen_rels_path_from_obj_path,
    get_epc_content_type_path,
    extract_uuid_and_version_from_obj_path,
    create_h5_external_relationship,
    create_default_core_properties,
    create_default_types,
    match_external_proxy_type,
    get_rels_dor_type,
    as_dor,
    create_energyml_object,
    create_external_part_reference,
    get_reverse_dor_list,
    get_file_folder_and_name_from_path,
)
from energyml.utils.constants import EpcExportVersion, EPCRelsRelationshipType, MimeType, gen_uuid
from energyml.opc.opc import Relationship, TargetMode, CoreProperties, Types
from energyml.utils.uri import Uri, parse_uri
from energyml.utils.introspection import get_obj_uuid, get_obj_version
from energyml.eml.v2_3.commonv2 import Citation, DataObjectReference
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    TrianglePatch,
    PointGeometry,
    Point3DExternalArray,
)
from energyml.resqml.v2_0_1.resqmlv2 import ObjTriangulatedSetRepresentation as TriangulatedSetRepresentation201


# =============================================================================
# TEST FIXTURES - Reusable test data
# =============================================================================

TEST_UUID = "12345678-1234-1234-1234-123456789abc"
TEST_UUID_2 = "abcd5678-90ef-1234-5678-abcdef123456"


@pytest.fixture
def sample_citation():
    """Create a sample Citation object for testing."""
    return Citation(
        title="Test Object",
        originator="Test Originator",
        creation="2024-01-01T00:00:00Z",
        format="energyml-utils test",
    )


@pytest.fixture
def sample_triangulated_set_22(sample_citation):
    """Create a sample TriangulatedSetRepresentation (RESQML 2.2) for testing."""
    obj = TriangulatedSetRepresentation(
        uuid=TEST_UUID,
        citation=sample_citation,
        schema_version="2.2",
    )
    return obj


@pytest.fixture
def sample_triangulated_set_201():
    """Create a sample TriangulatedSetRepresentation (RESQML 2.0.1) for testing."""
    citation = Citation(
        title="Test Object 201",
        originator="Test",
        creation="2024-01-01T00:00:00Z",
    )
    obj = TriangulatedSetRepresentation201(
        uuid=TEST_UUID_2,
        citation=citation,
        schema_version="2.0.1",
    )
    return obj


# =============================================================================
# TEST CLASSES
# =============================================================================


class TestPathGenerationFunctions:
    """Test suite for EPC path generation utility functions."""

    def test_gen_core_props_rels_path(self):
        """Test generation of core properties rels file path."""
        result = gen_core_props_rels_path()
        assert isinstance(result, str)
        assert result == "docProps/_rels/core.xml.rels"

    def test_gen_core_props_path_classic(self):
        """Test core properties path generation for classic export."""
        result = gen_core_props_path(EpcExportVersion.CLASSIC)
        assert result == "docProps/core.xml"

    def test_gen_core_props_path_expanded(self):
        """Test core properties path generation for expanded export."""
        result = gen_core_props_path(EpcExportVersion.EXPANDED)
        assert result == "docProps/core.xml"

    def test_gen_core_props_path_default(self):
        """Test core properties path generation with default export version."""
        result = gen_core_props_path()
        assert result == "docProps/core.xml"

    def test_get_epc_content_type_path(self):
        """Test content types file path generation."""
        result = get_epc_content_type_path()
        assert result == "[Content_Types].xml"

    def test_gen_rels_path_from_obj_path_simple(self):
        """Test rels path generation from simple object path."""
        obj_path = "ObjType_12345678-1234-1234-1234-123456789abc.xml"
        result = gen_rels_path_from_obj_path(obj_path)
        assert result == "_rels/ObjType_12345678-1234-1234-1234-123456789abc.xml.rels"

    def test_gen_rels_path_from_obj_path_with_folder(self):
        """Test rels path generation from path with folders."""
        obj_path = "namespace_resqml22/version_1.0/Grid2dRepresentation_abc-123.xml"
        result = gen_rels_path_from_obj_path(obj_path)
        assert result == "namespace_resqml22/version_1.0/_rels/Grid2dRepresentation_abc-123.xml.rels"

    def test_gen_rels_path_from_obj_path_with_path_object(self):
        """Test rels path generation with Path object input."""
        obj_path = Path("folder/subfolder/Object_uuid.xml")
        result = gen_rels_path_from_obj_path(obj_path)
        assert result == "folder/subfolder/_rels/Object_uuid.xml.rels"

    def test_gen_rels_path_from_obj_path_raises_error_for_rels_folder(self):
        """Test that error is raised when object path is in _rels folder."""
        obj_path = "_rels/Object_uuid.xml.rels"
        with pytest.raises(ValueError, match="cannot be in the '_rels' folder"):
            gen_rels_path_from_obj_path(obj_path)

    def test_extract_uuid_and_version_from_obj_path_simple(self):
        """Test UUID and version extraction from simple path."""
        obj_path = "Grid2dRepresentation_12345678-1234-1234-1234-123456789abc.xml"
        uuid, version = extract_uuid_and_version_from_obj_path(obj_path)
        assert uuid == "12345678-1234-1234-1234-123456789abc"
        assert version is None

    def test_extract_uuid_and_version_from_obj_path_with_version(self):
        """Test UUID and version extraction from versioned path."""
        obj_path = "namespace_resqml22/version_2.5/Grid_abcd1234-5678-90ab-cdef-123456789012.xml"
        uuid, version = extract_uuid_and_version_from_obj_path(obj_path)
        assert uuid == "abcd1234-5678-90ab-cdef-123456789012"
        assert version == "2.5"

    def test_extract_uuid_and_version_from_obj_path_invalid(self):
        """Test error when no UUID found in path."""
        obj_path = "invalid_path_without_uuid.xml"
        with pytest.raises(ValueError, match="Cannot extract uuid"):
            extract_uuid_and_version_from_obj_path(obj_path)

    def test_get_file_folder_and_name_from_path_with_folder(self):
        """Test folder and filename extraction from path with folder."""
        path = "folder/subfolder/file.xml"
        folder, filename = get_file_folder_and_name_from_path(path)
        assert folder == "folder/subfolder/"
        assert filename == "file.xml"

    def test_get_file_folder_and_name_from_path_without_folder(self):
        """Test folder and filename extraction from path without folder."""
        path = "file.xml"
        folder, filename = get_file_folder_and_name_from_path(path)
        assert folder == ""
        assert filename == "file.xml"

    def test_get_file_folder_and_name_from_path_multiple_levels(self):
        """Test folder and filename extraction from deeply nested path."""
        path = "level1/level2/level3/level4/data.xml"
        folder, filename = get_file_folder_and_name_from_path(path)
        assert folder == "level1/level2/level3/level4/"
        assert filename == "data.xml"


class TestEnergyMLObjectPathGeneration:
    """Test suite for EnergyML object path generation."""

    def test_gen_energyml_object_path_classic_resqml22(self, sample_triangulated_set_22):
        """Test classic EPC path generation for RESQML 2.2 object."""
        result = gen_energyml_object_path(sample_triangulated_set_22, EpcExportVersion.CLASSIC)
        assert result == f"TriangulatedSetRepresentation_{TEST_UUID}.xml"

    def test_gen_energyml_object_path_classic_resqml201(self, sample_triangulated_set_201):
        """Test classic EPC path generation for RESQML 2.0.1 object."""
        result = gen_energyml_object_path(sample_triangulated_set_201, EpcExportVersion.CLASSIC)
        assert result == f"obj_TriangulatedSetRepresentation_{TEST_UUID_2}.xml"

    def test_gen_energyml_object_path_expanded_without_version(self, sample_triangulated_set_22):
        """Test expanded EPC path generation without object version."""
        result = gen_energyml_object_path(sample_triangulated_set_22, EpcExportVersion.EXPANDED)
        assert f"namespace_resqml22/TriangulatedSetRepresentation_{TEST_UUID}.xml" == result

    def test_gen_energyml_object_path_expanded_with_version(self, sample_triangulated_set_22):
        """Test expanded EPC path generation with object version."""
        sample_triangulated_set_22.object_version = "3.1"
        result = gen_energyml_object_path(sample_triangulated_set_22, EpcExportVersion.EXPANDED)
        assert (
            f"namespace_resqml22/version_{sample_triangulated_set_22.object_version}/TriangulatedSetRepresentation_{TEST_UUID}.xml"
            == result
        )

    def test_gen_energyml_object_path_from_uri_string(self):
        """Test path generation from URI string."""
        uri_str = f"eml:///resqml22.TriangulatedSetRepresentation({TEST_UUID})"
        result = gen_energyml_object_path(uri_str, EpcExportVersion.CLASSIC)
        assert f"TriangulatedSetRepresentation_{TEST_UUID}.xml" in result

    def test_gen_energyml_object_path_from_uri_object(self):
        """Test path generation from Uri object."""
        uri = Uri(
            domain="resqml",
            domain_version="22",
            object_type="TriangulatedSetRepresentation",
            uuid=TEST_UUID,
        )
        result = gen_energyml_object_path(uri, EpcExportVersion.CLASSIC)
        assert f"TriangulatedSetRepresentation_{TEST_UUID}.xml" in result

    def test_gen_energyml_object_path_raises_error_no_uuid(self, sample_citation):
        """Test error is raised when object has no UUID."""
        obj = TriangulatedSetRepresentation(
            citation=sample_citation,
            schema_version="2.2",
        )
        # Don't set UUID
        with pytest.raises(ValueError, match="must have a valid uuid"):
            gen_energyml_object_path(obj, EpcExportVersion.CLASSIC)

    def test_gen_energyml_object_path_types(self):
        """Test path generation for Types object."""
        types_ = Types()
        result = gen_energyml_object_path(types_)
        assert result == "[Content_Types].xml"

    def test_gen_rels_path_with_types(self):
        """Test rels path generation for Types object."""
        types_ = Types()
        result = gen_rels_path(types_)
        assert result == "_rels/.rels"

    def test_gen_energyml_object_path_core_properties(self):
        """Test path generation for CoreProperties object."""
        core_props = CoreProperties()
        result = gen_energyml_object_path(core_props)
        assert result == "docProps/core.xml"

    def test_gen_rels_path_with_core_properties(self):
        """Test rels path generation for CoreProperties object."""
        core_props = CoreProperties()
        result = gen_rels_path(core_props)
        assert result == "docProps/_rels/core.xml.rels"

    def test_gen_rels_path_with_energyml_object_classic(self, sample_triangulated_set_22):
        """Test rels path generation for EnergyML object in classic mode."""
        result = gen_rels_path(sample_triangulated_set_22, EpcExportVersion.CLASSIC)
        assert result == f"_rels/TriangulatedSetRepresentation_{TEST_UUID}.xml.rels"

    def test_gen_rels_path_with_energyml_object_expanded(self, sample_triangulated_set_22):
        """Test rels path generation for EnergyML object in expanded mode."""
        result = gen_rels_path(sample_triangulated_set_22, EpcExportVersion.EXPANDED)
        assert "_rels/" in result
        assert f"TriangulatedSetRepresentation_{TEST_UUID}.xml.rels" in result


class TestRelationshipFunctions:
    """Test suite for relationship creation and management."""

    def test_create_h5_external_relationship_default_index(self):
        """Test HDF5 external relationship creation with default index."""
        h5_path = "external_data.h5"
        result = create_h5_external_relationship(h5_path)

        assert isinstance(result, Relationship)
        assert result.target == h5_path
        assert result.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type()
        assert result.id == "Hdf5File"
        assert result.target_mode == TargetMode.EXTERNAL

    def test_create_h5_external_relationship_custom_index(self):
        """Test HDF5 external relationship creation with custom index."""
        h5_path = "data/measurements.h5"
        result = create_h5_external_relationship(h5_path, current_idx=2)

        assert result.target == h5_path
        assert result.id == "Hdf5File3"
        assert result.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type()

    def test_create_h5_external_relationship_zero_index(self):
        """Test HDF5 external relationship creation with zero index."""
        h5_path = "test.h5"
        result = create_h5_external_relationship(h5_path, current_idx=0)

        assert result.id == "Hdf5File"

    def test_get_reverse_dor_list_empty(self):
        """Test reverse DOR list with empty object list."""
        result = get_reverse_dor_list([])
        assert result == {}

    def test_get_reverse_dor_list_with_objects(self, sample_triangulated_set_22, sample_citation):
        """Test reverse DOR list with objects containing DORs."""
        # Create object with DOR
        dor = as_dor(create_energyml_object("eml23.ProjectedCrs"))

        # Create triangulated set with patches that might have DORs
        obj_with_dor = TriangulatedSetRepresentation(
            uuid=gen_uuid(),
            citation=sample_citation,
            schema_version="2.2",
        )
        # Adding a patch with contact element that has DOR
        patch = TrianglePatch(
            geometry=PointGeometry(points=Point3DExternalArray(), local_crs=dor)
        )  # Reference to another object
        obj_with_dor.triangle_patch = [patch]

        result = get_reverse_dor_list([obj_with_dor])

        # Verify the result format - should have entries
        assert isinstance(result, dict)


class TestDefaultObjectCreation:
    """Test suite for default object creation functions."""

    def test_create_default_core_properties_no_creator(self):
        """Test default core properties creation without custom creator."""
        result = create_default_core_properties()

        assert isinstance(result, CoreProperties)
        assert result.created is not None
        assert result.creator is not None
        assert "energyml-utils" in result.creator.any_element
        assert result.identifier is not None
        assert result.version == "1.0"
        # Verify the identifier is a valid UUID format
        assert "urn:uuid:" in result.identifier.any_element

    def test_create_default_core_properties_custom_creator(self):
        """Test default core properties creation with custom creator."""
        custom_creator = "TestOrganization"
        result = create_default_core_properties(creator=custom_creator)

        assert result.creator.any_element == custom_creator
        assert result.version == "1.0"
        assert result.created is not None

    def test_create_default_types(self):
        """Test default Types object creation."""
        result = create_default_types()

        assert isinstance(result, Types)
        assert len(result.default) == 1
        assert result.default[0].extension == "rels"
        assert result.default[0].content_type == str(MimeType.RELS)
        assert len(result.override) == 1
        assert result.override[0].content_type == str(MimeType.CORE_PROPERTIES)
        assert result.override[0].part_name == "docProps/core.xml"


class TestExternalProxyMatching:
    """Test suite for external proxy type matching."""

    def test_match_external_proxy_type_with_valid_strings(self):
        """Test matching external proxy type with valid strings."""
        assert match_external_proxy_type("EpcExternalPartReference") is True
        assert match_external_proxy_type("eml23.EpcExternalPartReference") is True
        assert match_external_proxy_type("external_reference") is True
        assert match_external_proxy_type("EXTERNAL_REFERENCE") is True

    def test_match_external_proxy_type_with_invalid_strings(self):
        """Test matching external proxy type with invalid strings."""
        assert match_external_proxy_type("Grid2dRepresentation") is False
        assert match_external_proxy_type("WellboreTrajectory") is False
        assert match_external_proxy_type("random_type") is False
        assert match_external_proxy_type("TriangulatedSetRepresentation") is False

    def test_match_external_proxy_type_case_insensitive(self):
        """Test that matching is case-insensitive."""
        assert match_external_proxy_type("External_Reference") is True
        assert match_external_proxy_type("EXTERNAL_PART_REFERENCE") is True

    def test_match_external_proxy_type_with_path(self):
        """Test matching external proxy type from file path."""
        assert match_external_proxy_type("path/to/obj_EpcExternalPartReference_uuid.xml") is True


class TestRelsDorType:
    """Test suite for get_rels_dor_type function."""

    def test_external_proxy_in_owner_rels_file(self):
        """Test external proxy reference from the owner's rels file perspective."""
        # When we're in the rels file of an object that references an external proxy
        result = get_rels_dor_type("EpcExternalPartReference", in_dor_owner_rels_file=True)
        assert result == str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY)

    def test_external_proxy_in_target_rels_file(self):
        """Test external proxy reference from the target's rels file perspective."""
        # When we're in the rels file of the external proxy itself
        result = get_rels_dor_type("eml23.EpcExternalPartReference", in_dor_owner_rels_file=False)
        assert result == str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML)

    def test_regular_object_in_owner_rels_file(self):
        """Test regular object reference from the owner's rels file perspective."""
        # When we're in the rels file of an object that references a regular EnergyML object
        result = get_rels_dor_type("resqml22.TriangulatedSetRepresentation", in_dor_owner_rels_file=True)
        assert result == str(EPCRelsRelationshipType.DESTINATION_OBJECT)

    def test_regular_object_in_target_rels_file(self):
        """Test regular object reference from the target's rels file perspective."""
        # When we're in the rels file of the referenced object
        result = get_rels_dor_type("resqml22.Grid2dRepresentation", in_dor_owner_rels_file=False)
        assert result == str(EPCRelsRelationshipType.SOURCE_OBJECT)

    def test_with_uri_object_external_proxy(self):
        """Test with Uri object pointing to external proxy."""
        uri = Uri(
            domain="eml",
            domain_version="23",
            object_type="EpcExternalPartReference",
            uuid=TEST_UUID,
        )
        result = get_rels_dor_type(uri, in_dor_owner_rels_file=True)
        assert result == str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY)

    def test_with_uri_object_regular_object(self):
        """Test with Uri object pointing to regular EnergyML object."""
        uri = Uri(
            domain="resqml",
            domain_version="22",
            object_type="TriangulatedSetRepresentation",
            uuid=TEST_UUID,
        )
        result = get_rels_dor_type(uri, in_dor_owner_rels_file=False)
        assert result == str(EPCRelsRelationshipType.SOURCE_OBJECT)

    def test_with_energyml_object(self, sample_triangulated_set_22):
        """Test with actual EnergyML object."""
        # Regular EnergyML object from owner perspective
        result = get_rels_dor_type(sample_triangulated_set_22, in_dor_owner_rels_file=True)
        assert result == str(EPCRelsRelationshipType.DESTINATION_OBJECT)

    def test_all_four_scenarios(self):
        """Test all four possible combinations of external/regular × owner/target."""
        # Scenario 1: External proxy, owner's perspective
        result1 = get_rels_dor_type("external_reference", True)
        assert result1 == str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY)

        # Scenario 2: External proxy, target's perspective
        result2 = get_rels_dor_type("external_reference", False)
        assert result2 == str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML)

        # Scenario 3: Regular object, owner's perspective
        result3 = get_rels_dor_type("WellboreTrajectory", True)
        assert result3 == str(EPCRelsRelationshipType.DESTINATION_OBJECT)

        # Scenario 4: Regular object, target's perspective
        result4 = get_rels_dor_type("WellboreTrajectory", False)
        assert result4 == str(EPCRelsRelationshipType.SOURCE_OBJECT)


class TestDORCreation:
    """Test suite for Data Object Reference (DOR) creation."""

    def test_as_dor_with_none(self):
        """Test DOR creation with None input returns None."""
        result = as_dor(None)
        assert result is None

    def test_as_dor_from_uri_string(self):
        """Test DOR creation from URI string."""
        uri_string = f"eml:///resqml22.TriangulatedSetRepresentation({TEST_UUID})"
        result = as_dor(uri_string, dor_qualified_type="eml23.DataObjectReference")

        assert isinstance(result, DataObjectReference)
        assert get_obj_uuid(result) == TEST_UUID

    def test_as_dor_from_energyml_object(self, sample_triangulated_set_22):
        """Test DOR creation from EnergyML object."""
        result = as_dor(sample_triangulated_set_22, dor_qualified_type="eml23.DataObjectReference")

        assert isinstance(result, DataObjectReference)
        assert get_obj_uuid(result) == TEST_UUID
        assert result.title == "Test Object"

    def test_as_dor_from_existing_dor(self):
        """Test DOR conversion from one DOR type to another."""
        source_dor = DataObjectReference(
            uuid=TEST_UUID,
            title="Original DOR",
            qualified_type="resqml22.TriangulatedSetRepresentation",
        )

        result = as_dor(source_dor, dor_qualified_type="eml23.DataObjectReference")

        assert isinstance(result, DataObjectReference)
        assert get_obj_uuid(result) == TEST_UUID
        assert result.qualified_type == "resqml22.TriangulatedSetRepresentation"
        assert result.title == "Original DOR"

    def test_as_dor_with_version(self, sample_triangulated_set_22):
        """Test DOR creation preserves object version."""
        sample_triangulated_set_22.object_version = "2.5"
        result = as_dor(sample_triangulated_set_22, dor_qualified_type="eml23.DataObjectReference")

        assert get_obj_version(result) == "2.5"

    def test_as_dor_from_uri_object(self):
        """Test DOR creation from Uri object."""
        uri = Uri(
            domain="resqml",
            domain_version="22",
            object_type="TriangulatedSetRepresentation",
            uuid=TEST_UUID,
            version="1.0",
        )

        result = as_dor(uri, dor_qualified_type="eml23.DataObjectReference")

        assert isinstance(result, DataObjectReference)
        assert get_obj_uuid(result) == TEST_UUID
        assert get_obj_version(result) == "1.0"


class TestObjectCreation:
    """Test suite for EnergyML object creation functions."""

    def test_create_energyml_object_with_defaults(self):
        """Test EnergyML object creation with default parameters."""
        result = create_energyml_object("resqml22.TriangulatedSetRepresentation")

        assert isinstance(result, TriangulatedSetRepresentation)
        assert result.citation is not None
        assert result.citation.title == "New_Object"
        assert get_obj_uuid(result) is not None
        assert result.schema_version == "2.2"

    def test_create_energyml_object_with_custom_citation(self):
        """Test EnergyML object creation with custom citation."""
        custom_citation = {
            "title": "Custom Test Object",
            "originator": "Test Organization",
        }

        result = create_energyml_object(
            "resqml22.TriangulatedSetRepresentation",
            citation=custom_citation,
        )

        assert result.citation.title == "Custom Test Object"
        assert result.citation.originator == "Test Organization"

    def test_create_energyml_object_with_custom_uuid(self):
        """Test EnergyML object creation with custom UUID."""
        custom_uuid = TEST_UUID

        result = create_energyml_object(
            "resqml22.TriangulatedSetRepresentation",
            uuid=custom_uuid,
        )

        assert get_obj_uuid(result) == custom_uuid

    def test_create_energyml_object_resqml201(self):
        """Test EnergyML object creation for RESQML 2.0.1."""
        result = create_energyml_object("resqml20.obj_TriangulatedSetRepresentation")

        assert isinstance(result, TriangulatedSetRepresentation201)
        assert result.schema_version == "2.0"

    def test_create_external_part_reference_22(self):
        """Test external part reference creation for EML 2.2."""
        h5_path = "data/external.h5"
        result = create_external_part_reference("2.2", h5_path)

        assert result is not None
        assert get_obj_uuid(result) is not None
        # Note: The actual attributes depend on the EpcExternalPartReference schema

    def test_create_external_part_reference_20(self):
        """Test external part reference creation for EML 2.0."""
        h5_path = "test.h5"
        result = create_external_part_reference("2.0", h5_path)

        assert result is not None
        assert get_obj_uuid(result) is not None

    def test_create_external_part_reference_with_custom_params(self):
        """Test external part reference creation with custom citation and UUID."""
        custom_citation = {"title": "External Data Reference"}
        custom_uuid = TEST_UUID_2

        result = create_external_part_reference(
            "2.1",
            "external.h5",
            citation=custom_citation,
            uuid=custom_uuid,
        )

        assert get_obj_uuid(result) == custom_uuid

    def test_create_external_part_reference_version_formats(self):
        """Test external part reference creation with different version formats."""
        # Test with dotted version
        result1 = create_external_part_reference("2.2", "test1.h5")
        assert result1 is not None

        # Test with underscore version
        result2 = create_external_part_reference("2_1", "test2.h5")
        assert result2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
