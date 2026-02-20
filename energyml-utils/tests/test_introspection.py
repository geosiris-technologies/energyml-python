# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Test Suite for energyml.utils.introspection module

This module contains comprehensive tests for introspection utilities used to
inspect, manipulate, and extract information from Energyml objects.
"""
from dataclasses import dataclass
from energyml.utils.epc_utils import MimeType, as_dor
import pytest
from typing import Any

import energyml.resqml.v2_0_1.resqmlv2
from energyml.eml.v2_0.commonv2 import Citation as Citation20
from energyml.eml.v2_3.commonv2 import Citation, ExternalDataArrayPart, DataObjectReference
from energyml.resqml.v2_0_1.resqmlv2 import FaultInterpretation
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    TrianglePatch,
    ContactElement,
    IntegerExternalArray,
    ExternalDataArray,
    PointGeometry,
    Point3DExternalArray,
    AbstractPoint3DArray,
)
from energyml.opc.opc import Dcmitype1, Contributor

from src.energyml.utils.constants import (
    date_to_epoch,
    pascal_case,
    epoch,
    epoch_to_date,
    snake_case,
    gen_uuid,
)
from src.energyml.utils.introspection import (
    is_primitive,
    is_enum,
    is_abstract,
    get_class_from_name,
    get_class_from_content_type,
    get_class_from_qualified_type,
    get_object_attribute,
    get_object_attribute_no_verif,
    get_object_attribute_rgx,
    get_object_attribute_advanced,
    set_attribute_from_path,
    copy_attributes,
    get_obj_identifier,
    get_obj_uuid,
    get_obj_version,
    get_obj_title,
    get_obj_pkg_pkgv_type_uuid_version,
    get_obj_uri,
    get_obj_type,
    get_obj_qualified_type,
    get_obj_content_type,
    get_class_methods,
    get_class_fields,
    get_class_attributes,
    get_class_attribute_type,
    get_matching_class_attribute_name,
    search_attribute_matching_name,
    search_attribute_matching_type,
    set_attribute_from_json_str,
    set_attribute_from_dict,
    get_module_name,
    class_match_rgx,
    is_dor,
    get_dor_obj_info,
    get_direct_dor_list,
)


# =============================================================================
# TEST FIXTURES - Reusable test data
# =============================================================================

# Sample nested dictionary for attribute access tests
SAMPLE_NESTED_DICT = {"a": {"b": ["v_x", {"c": "v_test"}]}}

# Sample data for copy_attributes tests
SAMPLE_DATA_IN = {
    "a": {"b": "v_0", "c": "v_1"},
    "uuid": "215f8219-cabd-4e24-9e4f-e371cabc9622",
    "objectVersion": "Resqml 2.0",
    "non_existing": 42,
}

SAMPLE_DATA_OUT_TEMPLATE = {
    "a": None,
    "Uuid": "8291afd6-ae01-49f5-bc96-267e7b27450d",
    "object_version": "Resqml 2.0",
}


@pytest.fixture
def citation_v20():
    """Create a Citation v2.0 object for testing."""
    return Citation20(
        title="Test Citation v2.0",
        originator="Valentin",
        creation=epoch_to_date(epoch()),
        editor="test",
        format="Geosiris",
        last_update=epoch_to_date(epoch()),
    )


@pytest.fixture
def citation_v23():
    """Create a Citation v2.3 object for testing."""
    return Citation(
        title="Test Citation v2.3",
        originator="Valentin",
        creation=epoch_to_date(epoch()),
        editor="test",
        format="Geosiris",
        last_update=epoch_to_date(epoch()),
    )


@pytest.fixture
def fault_interpretation(citation_v20):
    """Create a FaultInterpretation (resqml 2.0.1) object for testing."""
    return FaultInterpretation(
        citation=citation_v20,
        uuid=gen_uuid(),
        object_version="0",
    )


@pytest.fixture
def triangulated_set_no_version(citation_v23, fault_interpretation):
    """Create a TriangulatedSetRepresentation (resqml 2.2) without version."""
    trset_uuid = gen_uuid()
    return TriangulatedSetRepresentation(
        citation=citation_v23,
        uuid=trset_uuid,
        represented_object=as_dor(fault_interpretation),
        triangle_patch=[
            TrianglePatch(
                node_count=3,
                triangles=IntegerExternalArray(
                    values=ExternalDataArray(
                        external_data_array_part=[
                            ExternalDataArrayPart(
                                count=[6],
                                path_in_external_file=f"/RESQML/{trset_uuid}/triangles",
                                uri="samplefile_uri.h5",
                                mime_type=str(MimeType.HDF5),
                            )
                        ]
                    )
                ),
                geometry=PointGeometry(
                    points=Point3DExternalArray(
                        coordinates=ExternalDataArray(
                            external_data_array_part=[
                                ExternalDataArrayPart(
                                    count=[9],
                                    path_in_external_file=f"/RESQML/{trset_uuid}/points",
                                    uri="samplefile_uri.h5",
                                    mime_type=str(MimeType.HDF5),
                                )
                            ]
                        )
                    ),
                ),
            )
        ],
    )


@pytest.fixture
def triangulated_set_versioned(citation_v23, fault_interpretation):
    """Create a TriangulatedSetRepresentation (resqml 2.2) with version."""
    trset_uuid = gen_uuid()
    return TriangulatedSetRepresentation(
        citation=citation_v23,
        uuid=trset_uuid,
        represented_object=as_dor(fault_interpretation),
        object_version="3",
        triangle_patch=[
            TrianglePatch(
                node_count=3,
                triangles=IntegerExternalArray(
                    values=ExternalDataArray(
                        external_data_array_part=[
                            ExternalDataArrayPart(
                                count=[6],
                                path_in_external_file=f"/RESQML/{trset_uuid}/triangles",
                                uri="samplefile_uri.h5",
                                mime_type=str(MimeType.HDF5),
                            )
                        ]
                    )
                ),
                geometry=PointGeometry(
                    points=Point3DExternalArray(
                        coordinates=ExternalDataArray(
                            external_data_array_part=[
                                ExternalDataArrayPart(
                                    count=[9],
                                    path_in_external_file=f"/RESQML/{trset_uuid}/points",
                                    uri="samplefile_uri.h5",
                                    mime_type=str(MimeType.HDF5),
                                )
                            ]
                        )
                    ),
                ),
            )
        ],
    )


# =============================================================================
# TYPE CHECKING TESTS
# =============================================================================


def test_is_primitive():
    """Test identification of primitive types."""
    assert is_primitive(1)
    assert is_primitive(int)
    assert is_primitive(float)
    assert is_primitive(str)
    assert is_primitive(bool)
    assert is_primitive(type(None))
    assert is_primitive(Dcmitype1)  # Enum is given as primitive
    assert not is_primitive(Contributor)


def test_is_enum():
    """Test identification of Enum types."""
    assert is_enum(Dcmitype1)
    assert not is_enum(Contributor)
    assert not is_enum(int)


def test_is_abstract():
    """Test identification of abstract classes."""

    assert is_abstract(AbstractPoint3DArray)
    assert not is_abstract(Point3DExternalArray)
    assert not is_abstract(int)


# =============================================================================
# STRING CASE CONVERSION TESTS
# =============================================================================


def test_snake_case():
    """Test conversion to snake_case."""
    assert snake_case("ThisIsASnakecase") == "this_is_a_snakecase"
    assert snake_case("This_IsASnakecase") == "this_is_a_snakecase"
    assert snake_case("This_isASnakecase") == "this_is_a_snakecase"


def test_pascal_case():
    """Test conversion to PascalCase."""
    assert pascal_case("ThisIsASnakecase") == "ThisIsASnakecase"
    assert pascal_case("This_IsASnakecase") == "ThisIsASnakecase"
    assert pascal_case("This_isASnakecase") == "ThisIsASnakecase"
    assert pascal_case("this_is_a_snakecase") == "ThisIsASnakecase"


def test_epoch():
    """Test epoch time conversion utilities."""
    now = epoch()
    assert date_to_epoch(epoch_to_date(now)) == now


# =============================================================================
# CLASS RESOLUTION TESTS
# =============================================================================


def test_get_class_from_name():
    """Test class resolution from fully qualified name."""
    assert get_class_from_name("energyml.opc.opc.Dcmitype1") == Dcmitype1


def test_get_class_from_content_type():
    """Test class resolution from content type string."""
    found_type = get_class_from_content_type("resqml20.obj_Grid2dRepresentation")
    assert found_type is not None
    assert found_type == energyml.resqml.v2_0_1.resqmlv2.Grid2DRepresentation


def test_get_class_from_qualified_type():
    """Test class resolution from qualified type string.

    According to the docstring: Return a type object matching with the qualified-type.
    This is similar to get_class_from_content_type.
    """
    assert get_class_from_qualified_type("resqml22.TriangulatedSetRepresentation") == TriangulatedSetRepresentation
    assert get_class_from_qualified_type("resqml20.obj_FaultInterpretation") == FaultInterpretation


def test_get_module_name():
    """Test module name generation from domain and version.

    According to the function signature: get_module_name(domain: str, domain_version: str)
    """
    assert get_module_name("resqml", "2.0") == "energyml.resqml.v2_0.resqmlv2"
    assert get_module_name("eml", "2.3") == "energyml.eml.v2_3.commonv2"
    assert get_module_name("eml", "2.0") == "energyml.eml.v2_0.commonv2"
    assert get_module_name("witsml", "1.0") == "energyml.witsml.v1_0.witsmlv2"


# =============================================================================
# CLASS INTROSPECTION TESTS
# =============================================================================


def test_get_class_methods():
    """Test retrieval of class methods.

    According to the docstring: Returns the list of the methods names for a specific class.
    """

    class SampleClass:
        def method_one(self):
            pass

        def method_two(self):
            pass

        def __str__(self):
            return "SampleClass"

    methods = get_class_methods(SampleClass)
    assert isinstance(methods, list)
    # Methods should not include dunder methods or types
    for method in methods:
        assert not method.startswith("__")

    assert len(methods) == 2
    assert "method_one" in methods
    assert "method_two" in methods


def test_get_class_fields():
    """Test retrieval of class fields.

    According to the docstring: Return all class fields names, mapped to their Field value.
    If a dict is given, this function is the identity.
    """
    # Test with dict (identity function)
    test_dict = {"a": 1, "b": 2}
    assert get_class_fields(test_dict) == test_dict

    # Test with actual class
    fields = get_class_fields(Citation)

    official_fields = {
        "title",
        "originator",
        "creation",
        "format",
        "editor",
        "last_update",
        "description",
        "editor_history",
        "descriptive_keywords",
    }

    assert isinstance(fields, dict)
    # Should contain expected fields    assert "title" in fields
    assert len(fields) == len(official_fields)
    assert set(fields.keys()) == official_fields


def test_get_class_attributes():
    """Test retrieval of class attributes.

    According to the docstring: returns a list of attributes (not private ones).
    """

    class SampleClass:
        class_attr = "value"
        _private_attr = "private"

        def __init__(self):
            self.additional_attr = "additional"

        def method_one(self):
            pass

    attributes = get_class_attributes(SampleClass)
    assert isinstance(attributes, list)

    assert len(attributes) == 1
    assert "class_attr" in attributes


def test_get_class_attribute_type():
    """Test retrieval of attribute type from class."""
    citation_title_type = get_class_attribute_type(Citation, "title")
    assert str(citation_title_type) == "Optional[str]"

    citation_editor_history_type = get_class_attribute_type(Citation, "editor_history")
    assert str(citation_editor_history_type) == "List[str]"


def test_get_matching_class_attribute_name(citation_v23):
    """Test finding correct attribute name from class."""
    # Test with case-insensitive matching
    result = get_matching_class_attribute_name(citation_v23, "Title")
    assert result == "title"

    result = get_matching_class_attribute_name(citation_v23, "ORIGINATOR")
    assert result == "originator"


# =============================================================================
# OBJECT ATTRIBUTE ACCESS TESTS
# =============================================================================


def test_get_object_attribute():
    """Test attribute access via dot-notation path."""
    data = SAMPLE_NESTED_DICT.copy()
    assert get_object_attribute(data, "a.b.1.c") == "v_test"


def test_get_object_attribute_no_verif():
    """Test attribute access without verification."""
    data = SAMPLE_NESTED_DICT.copy()

    # Test with dict
    assert get_object_attribute_no_verif(data, "a") is not None

    # Test with list indexing
    assert get_object_attribute_no_verif(data["a"]["b"], "0") == "v_x"

    # Test that non-existent attribute raises exception (no verification)
    with pytest.raises(AttributeError):
        get_object_attribute_no_verif(data, "non_existent")


def test_get_object_attribute_rgx(triangulated_set_versioned):
    """Test attribute access using regex patterns.

    According to the docstring: Search the attribute name using regex for values between dots.
    Example: [Cc]itation.[Tt]it\\.*
    """

    assert get_object_attribute_rgx(triangulated_set_versioned, "Citation.Title") == "Test Citation v2.3"
    assert get_object_attribute_rgx(triangulated_set_versioned, "[Cc]itation.[Tt]it\\.*") == "Test Citation v2.3"
    assert get_object_attribute_rgx(triangulated_set_versioned, "[Cc]itation.[Oo]rigin\\.*") == "Valentin"


def test_get_object_attribute_advanced(triangulated_set_versioned):
    """Test advanced attribute access with matching."""
    assert get_object_attribute_advanced(triangulated_set_versioned, "citation.title") == "Test Citation v2.3"
    assert get_object_attribute_advanced(triangulated_set_versioned, "citation.originator") == "Valentin"


# =============================================================================
# OBJECT ATTRIBUTE MODIFICATION TESTS
# =============================================================================


def test_set_attribute_from_path():
    """Test setting attribute value via dot-notation path."""
    data = SAMPLE_NESTED_DICT.copy()
    assert get_object_attribute(data, "a.b.1.c") == "v_test"
    set_attribute_from_path(data, "a.b.1.c", "v_new")
    assert get_object_attribute(data, "a.b.1.c") == "v_new"
    set_attribute_from_path(data, "a", "v_new")
    assert get_object_attribute(data, "a") == "v_new"


def test_set_attribute_from_json_str():
    """Test setting attributes from JSON string.

    According to signature: set_attribute_from_json_str(obj: Any, json_input: str) -> None
    """
    d_0 = {"a": "v_0", "b": {"c": "v_1"}}
    d_1 = '{"a": "coucou"}'

    set_attribute_from_json_str(d_0, d_1)
    assert d_0["a"] == "coucou"

    d_3 = '{"b": {"c": "v_2"}}'
    set_attribute_from_json_str(d_0, d_3)
    assert d_0["b"]["c"] == "v_2"


def test_set_attribute_from_dict():
    """Test setting attributes from dictionary."""
    d_0 = {"a": "v_0", "b": {"c": "v_1"}}
    d_1 = {"a": "coucou"}

    set_attribute_from_dict(d_0, d_1)
    assert d_0["a"] == "coucou"

    d_3 = {"b": {"c": "v_2"}}
    set_attribute_from_dict(d_0, d_3)
    assert d_0["b"]["c"] == "v_2"


def test_copy_attributes_existing_ignore_case():
    """Test copying only existing attributes with case-insensitive matching."""
    data_in = SAMPLE_DATA_IN.copy()
    data_out = SAMPLE_DATA_OUT_TEMPLATE.copy()

    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=True,
        ignore_case=True,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] == data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert "non_existing" not in data_out


def test_copy_attributes_ignore_case():
    """Test copying all attributes with case-insensitive matching."""
    data_in = SAMPLE_DATA_IN.copy()
    data_out = SAMPLE_DATA_OUT_TEMPLATE.copy()

    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=False,
        ignore_case=True,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] == data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert data_out["non_existing"] == data_in["non_existing"]


def test_copy_attributes_case_sensitive():
    """Test copying attributes with case-sensitive matching."""
    data_in = SAMPLE_DATA_IN.copy()
    data_out = SAMPLE_DATA_OUT_TEMPLATE.copy()

    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=False,
        ignore_case=False,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] != data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert data_out["non_existing"] == data_in["non_existing"]


# =============================================================================
# ATTRIBUTE SEARCH TESTS
# =============================================================================


def test_search_attribute_matching_name(triangulated_set_versioned):
    """Test searching attributes by name pattern."""
    assert len(search_attribute_matching_name(triangulated_set_versioned, "title", search_in_sub_obj=False)) == 0
    title_deep = search_attribute_matching_name(triangulated_set_versioned, "title", search_in_sub_obj=True)
    assert len(title_deep) == 2
    assert triangulated_set_versioned.citation.title in title_deep
    assert triangulated_set_versioned.represented_object.title in title_deep


def test_search_attribute_matching_type(triangulated_set_versioned):
    """Test searching attributes by type pattern."""
    search_results_deep = search_attribute_matching_type(
        triangulated_set_versioned, type_rgx="ExternalDataArrayPart", deep_search=True
    )
    assert len(search_results_deep) == 2

    @dataclass
    class SampleClass:
        ci: ContactElement
        dor: DataObjectReference

    s = SampleClass(
        ci=ContactElement(uuid="007"),
        dor=DataObjectReference(uuid="008"),
    )

    search_result_citation = search_attribute_matching_type(s, type_rgx="DataObjectReference", super_class_search=False)
    assert len(search_result_citation) == 1
    search_result_citation_deep = search_attribute_matching_type(
        s, type_rgx="DataObjectReference", super_class_search=True
    )
    assert len(search_result_citation_deep) == 2

    assert len(search_attribute_matching_type(s, type_rgx="SampleClass", return_self=True)) == 1
    assert len(search_attribute_matching_type(s, type_rgx="SampleClass", return_self=False)) == 0


# =============================================================================
# OBJECT METADATA EXTRACTION TESTS
# =============================================================================


def test_get_obj_uuid(triangulated_set_no_version, fault_interpretation):
    """Test extracting object UUID.

    According to the docstring: Return the object uuid (attribute must match
    the following regex: "[Uu]u?id|UUID").
    """
    assert get_obj_uuid(triangulated_set_no_version) == triangulated_set_no_version.uuid
    assert get_obj_uuid(fault_interpretation) == fault_interpretation.uuid


def test_get_obj_version(triangulated_set_versioned, triangulated_set_no_version, fault_interpretation):
    """Test extracting object version.

    According to the docstring: Return the object version (check for "object_version"
    or "version_string" attribute).
    """
    # Test object with explicit version
    assert get_obj_version(triangulated_set_versioned) == "3"
    assert get_obj_version(fault_interpretation) == "0"

    # Test object without version
    version = get_obj_version(triangulated_set_no_version)
    assert version is None or version == ""


def test_get_obj_version_edge_cases():
    """Test get_obj_version handles missing attributes gracefully."""

    # Create object with only some version attributes
    class MockObjWithVersionString:
        version_string = "1.0"

    class MockObjWithCitationVersion:
        class Citation:
            version_string = "2.0"

        citation = Citation()

    class MockObjNoVersion:
        some_other_attr = "value"

    # Should find version_string
    assert get_obj_version(MockObjWithVersionString()) == "1.0"

    # Should find citation.version_string when object_version missing
    assert get_obj_version(MockObjWithCitationVersion()) == "2.0"

    # Should return None when no version found
    assert get_obj_version(MockObjNoVersion()) is None


def test_get_obj_title(triangulated_set_no_version, fault_interpretation):
    """Test extracting object title."""
    assert get_obj_title(triangulated_set_no_version) == "Test Citation v2.3"
    assert get_obj_title(fault_interpretation) == "Test Citation v2.0"
    assert get_obj_title(as_dor(fault_interpretation)) == "Test Citation v2.0"

    class MockObjWithTitle:
        name = "Mock Title"

    assert get_obj_title(MockObjWithTitle()) == "Mock Title"

    assert get_obj_title({"Title": "Dict Title"}) == "Dict Title"
    assert get_obj_title({"title": "Dict Title Lower"}) == "Dict Title Lower"
    assert get_obj_title({"what": 42}) is None
    assert get_obj_title({"name": "Dict Title Lower"}) == "Dict Title Lower"

    # priority to citation.title
    assert get_obj_title({"name": "Dict Title Lower", "citation": {"title": "Citation Title"}}) == "Citation Title"


def test_get_obj_type(triangulated_set_no_version, fault_interpretation):
    """Test extracting object type name."""
    assert get_obj_type(triangulated_set_no_version) == "TriangulatedSetRepresentation"
    assert get_obj_type(fault_interpretation) == "FaultInterpretation"

    # Test with type itself
    assert get_obj_type(TriangulatedSetRepresentation) == "TriangulatedSetRepresentation"


def test_get_obj_identifier(triangulated_set_no_version, triangulated_set_versioned, fault_interpretation):
    """Test object identifier generation (UUID.VERSION format)."""
    assert get_obj_identifier(triangulated_set_no_version) == triangulated_set_no_version.uuid + "."
    assert get_obj_identifier(fault_interpretation) == fault_interpretation.uuid + ".0"
    assert get_obj_identifier(triangulated_set_versioned) == triangulated_set_versioned.uuid + ".3"


def test_get_obj_pkg_pkgv_type_uuid_version_obj_201(fault_interpretation):
    """Test metadata extraction from resqml20 object."""
    domain, domain_version, object_type, obj_uuid, obj_version = get_obj_pkg_pkgv_type_uuid_version(
        fault_interpretation
    )

    assert domain == "resqml"
    assert domain_version == "20"
    assert object_type == "obj_FaultInterpretation"
    assert obj_uuid == fault_interpretation.uuid
    assert obj_version == fault_interpretation.object_version


def test_get_obj_pkg_pkgv_type_uuid_version_obj_22(triangulated_set_no_version):
    """Test metadata extraction from resqml22 object."""
    domain, domain_version, object_type, obj_uuid, obj_version = get_obj_pkg_pkgv_type_uuid_version(
        triangulated_set_no_version
    )

    assert domain == "resqml"
    assert domain_version == "22"
    assert object_type == "TriangulatedSetRepresentation"
    assert obj_uuid == triangulated_set_no_version.uuid
    assert obj_version == triangulated_set_no_version.object_version


def test_get_obj_qualified_type(triangulated_set_no_version, fault_interpretation):
    """Test qualified type generation.

    According to the docstring: Generates an object qualified type as: 'PKG.PKG_VERSION.OBJ_TYPE'.
    """
    assert "resqml22.TriangulatedSetRepresentation" == get_obj_qualified_type(triangulated_set_no_version)
    assert "resqml20.obj_FaultInterpretation" == get_obj_qualified_type(fault_interpretation)


def test_get_obj_content_type(triangulated_set_no_version, fault_interpretation):
    """Test content type generation from object."""
    expected_content_type = "application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"
    assert get_obj_content_type(triangulated_set_no_version) == expected_content_type

    expected_content_type_fi = "application/x-resqml+xml;version=2.0;type=obj_FaultInterpretation"
    assert get_obj_content_type(fault_interpretation) == expected_content_type_fi


def test_get_obj_uri(triangulated_set_no_version, fault_interpretation):
    """Test URI generation for energyml objects."""
    uri_str = str(get_obj_uri(triangulated_set_no_version))
    assert uri_str == f"eml:///resqml22.TriangulatedSetRepresentation({triangulated_set_no_version.uuid})"
    assert (
        str(get_obj_uri(as_dor(triangulated_set_no_version)))
        == f"eml:///resqml22.TriangulatedSetRepresentation({triangulated_set_no_version.uuid})"
    )

    uri_str_with_dataspace = str(get_obj_uri(triangulated_set_no_version, "/MyDataspace/"))
    assert (
        uri_str_with_dataspace
        == f"eml:///dataspace('/MyDataspace/')/resqml22.TriangulatedSetRepresentation({triangulated_set_no_version.uuid})"
    )

    uri_str_fi = str(get_obj_uri(fault_interpretation))
    assert (
        uri_str_fi
        == f"eml:///resqml20.obj_FaultInterpretation(uuid={fault_interpretation.uuid},version='{fault_interpretation.object_version}')"
    )

    uri_str_fi_dataspace = str(get_obj_uri(fault_interpretation, "/MyDataspace/"))
    assert (
        uri_str_fi_dataspace
        == f"eml:///dataspace('/MyDataspace/')/resqml20.obj_FaultInterpretation(uuid={fault_interpretation.uuid},version='{fault_interpretation.object_version}')"
    )


# =============================================================================
# DATA OBJECT REFERENCE (DOR) TESTS
# =============================================================================


def test_is_dor(triangulated_set_versioned):
    """Test identification of Data Object Reference objects.

    According to the docstring: Returns True if the object is a DataObjectReference or
    has ContentType/QualifiedType attributes.
    """
    assert is_dor(as_dor(triangulated_set_versioned))
    assert not is_dor(triangulated_set_versioned)
    assert is_dor(
        {
            "ContentType": "application/x-resqml+xml;version=2.2;type=RockVolumeFeature",
        }
    )
    assert is_dor(
        {
            "QualifiedType": "resqml22.TriangulatedSetRepresentation",
        }
    )
    assert not is_dor(
        {
            "what": 42,
        }
    )


def test_get_dor_obj_info(triangulated_set_versioned):
    """Test extracting information from DOR objects.

    According to the docstring: From a DOR object, return a tuple
    (uuid, package name, package version, object_type, object_version).
    """
    dor = as_dor(triangulated_set_versioned)
    uuid, pkg_name, pkg_version, obj_type, obj_version = get_dor_obj_info(dor)
    assert uuid == triangulated_set_versioned.uuid
    assert pkg_name == "resqml"
    assert pkg_version == "2.2"
    assert obj_type == type(triangulated_set_versioned)
    assert obj_version == triangulated_set_versioned.object_version


def test_get_direct_dor_list(triangulated_set_no_version):
    """Test finding all DataObjectReference attributes.

    According to the docstring: Search all sub attribute of type "DataObjectReference".
    """
    dor_list = get_direct_dor_list(triangulated_set_no_version)
    assert isinstance(dor_list, list)
    assert len(dor_list) == 1


# =============================================================================
# PATTERN MATCHING TESTS
# =============================================================================


def test_class_match_rgx():
    """Test class name matching with regex.

    According to signature: class_match_rgx(cls, rgx, super_class_search, re_flags)
    Tests if a class name matches a regex pattern.
    """
    # Test simple class name matching
    assert class_match_rgx(Contributor, "Contributor")
    assert class_match_rgx(Contributor, "contrib.*")

    # Test case-insensitive matching (default behavior)
    assert class_match_rgx(Contributor, "contributor")
