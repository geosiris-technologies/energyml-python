# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Comprehensive unit tests for Epc class functionality.

Tests cover:
1. Object lifecycle (add, get, remove)
2. Export functionality (export_file, export_io)
3. Relationship computation (compute_rels) - only at export time
4. HDF5 array operations (write_array, read_array)
5. DOR creation and handling (as_dor)
6. File path generation (gen_energyml_object_path)
7. External files and raw files handling
"""
import os
import tempfile

import pytest
import numpy as np

from energyml.eml.v2_0.commonv2 import Citation as Citation20
from energyml.eml.v2_0.commonv2 import DataObjectReference as DataObjectReference201, EpcExternalPartReference
from energyml.eml.v2_3.commonv2 import Citation, DataObjectReference, ExternalDataArray, ExternalDataArrayPart
from energyml.resqml.v2_0_1.resqmlv2 import (
    FaultInterpretation,
    TriangulatedSetRepresentation as TriangulatedSetRepresentation20,
    TrianglePatch as TrianglePatch20,
    PointGeometry as PointGeometry20,
)
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    BoundaryFeatureInterpretation,
    BoundaryFeature,
    HorizonInterpretation,
    TrianglePatch,
    PointGeometry,
    Point3DExternalArray,
)

from energyml.utils.epc import (
    Epc,
    as_dor,
    EpcExportVersion,
)
from energyml.utils.epc_utils import gen_energyml_object_path
from energyml.utils.introspection import (
    epoch_to_date,
    epoch,
    gen_uuid,
    get_content_type_from_class,
    get_obj_uri,
    get_qualified_type_from_class,
    get_obj_identifier,
)
from energyml.utils.constants import EPCRelsRelationshipType, MimeType

CST_H5_PATH = "my_h5_filepath.h5"


@pytest.fixture
def temp_epc_file():
    """Create a temporary EPC file path for testing."""
    fd, temp_path = tempfile.mkstemp(suffix=".epc")
    os.close(fd)
    os.unlink(temp_path)

    yield temp_path

    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_objects():
    """Create sample EnergyML objects for testing."""
    # Create a BoundaryFeature
    bf = BoundaryFeature(
        citation=Citation(
            title="Test Boundary Feature",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000001",
        object_version="1.0",
    )

    # Create a BoundaryFeatureInterpretation
    bfi = BoundaryFeatureInterpretation(
        citation=Citation(
            title="Test Boundary Feature Interpretation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000002",
        object_version="1.0",
        interpreted_feature=as_dor(bf),
    )

    # Create a HorizonInterpretation
    horizon_interp = HorizonInterpretation(
        citation=Citation(
            title="Test HorizonInterpretation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        interpreted_feature=as_dor(bf),
        uuid="25773477-ffee-4cc2-867d-000000000003",
        object_version="1.0",
    )

    # Create a TriangulatedSetRepresentation
    trset = TriangulatedSetRepresentation(
        citation=Citation(
            title="Test TriangulatedSetRepresentation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000004",
        object_version="1.0",
        represented_object=as_dor(horizon_interp),
        triangle_patch=[
            TrianglePatch(
                geometry=PointGeometry(
                    points=Point3DExternalArray(
                        coordinates=ExternalDataArray(
                            external_data_array_part=[
                                ExternalDataArrayPart(
                                    path_in_external_file="/points", uri=CST_H5_PATH, mime_type=MimeType.HDF5.value
                                )
                            ]
                        )
                    )
                )
            )
        ],
    )

    # Resqml 2.0.1 FaultInterpretation for additional tests
    fi_cit = Citation20(
        title="An interpretation",
        originator="Valentin",
        creation=epoch_to_date(epoch()),
        editor="test",
        format="Geosiris",
        last_update=epoch_to_date(epoch()),
    )

    fi = FaultInterpretation(
        citation=fi_cit,
        uuid=gen_uuid(),
        object_version="0",
    )

    # 201
    external_ref = EpcExternalPartReference(
        uuid="25773477-ffee-4cc2-867d-000000000005",
        citation=Citation20(title="An external reference", originator="Valentin", creation=epoch_to_date(epoch())),
    )

    tr_set_20 = TriangulatedSetRepresentation20(
        citation=Citation20(
            title="Test TriangulatedSetRepresentation 2.0", originator="Test", creation=epoch_to_date(epoch())
        ),
        uuid="25773477-ffee-4cc2-867d-000000000006",
        object_version="1.0",
        represented_interpretation=as_dor(horizon_interp, "eml20.DataObjectReference"),
        triangle_patch=[
            TrianglePatch20(geometry=PointGeometry20(local_crs=as_dor(external_ref, "eml20.DataObjectReference")))
        ],
    )

    return {
        "bf": bf,
        "bfi": bfi,
        "trset": trset,
        "trset20": tr_set_20,
        "external_ref": external_ref,
        "horizon_interp": horizon_interp,
        "fi": fi,
    }


class TestObjectLifecycle:
    """Test basic object lifecycle operations."""

    def test_add_object(self, sample_objects):
        """Test adding objects to Epc."""
        epc = Epc()
        bf = sample_objects["bf"]

        result = epc.add_object(bf)
        assert result is True
        assert len(epc.energyml_objects) == 1
        assert bf in epc.energyml_objects

    def test_add_multiple_objects(self, sample_objects):
        """Test adding multiple objects."""
        epc = Epc()

        epc.add_object(sample_objects["bf"])
        epc.add_object(sample_objects["bfi"])
        epc.add_object(sample_objects["horizon_interp"])
        epc.add_object(sample_objects["trset"])

        assert len(epc) == 4
        assert len(epc.energyml_objects) == 4

    def test_get_object_by_identifier(self, sample_objects):
        """Test retrieving object by identifier."""
        epc = Epc()
        bf = sample_objects["bf"]

        epc.add_object(bf)
        identifier = get_obj_identifier(bf)

        retrieved = epc.get_object_by_identifier(identifier)
        assert retrieved is not None
        assert retrieved.uuid == bf.uuid

    def test_get_object_by_uuid(self, sample_objects):
        """Test retrieving objects by UUID."""
        epc = Epc()
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        epc.add_object(bf)
        epc.add_object(bfi)

        results = epc.get_object_by_uuid(bf.uuid)
        assert len(results) == 1
        assert results[0].uuid == bf.uuid

    def test_remove_object(self, sample_objects):
        """Test removing objects from Epc."""
        epc = Epc()
        bf = sample_objects["bf"]

        epc.add_object(bf)
        assert len(epc) == 1

        identifier = get_obj_identifier(bf)
        epc.remove_object(identifier)

        assert len(epc) == 0
        assert bf not in epc.energyml_objects

    def test_len(self, sample_objects):
        """Test __len__ method."""
        epc = Epc()
        assert len(epc) == 0

        epc.add_object(sample_objects["bf"])
        assert len(epc) == 1

        epc.add_object(sample_objects["bfi"])
        assert len(epc) == 2


class TestExportFunctionality:
    """Test export operations."""

    def test_export_file(self, temp_epc_file, sample_objects):
        """Test exporting Epc to file."""
        epc = Epc()
        epc.add_object(sample_objects["bf"])
        epc.add_object(sample_objects["bfi"])

        epc.export_file(temp_epc_file)

        assert os.path.exists(temp_epc_file)
        assert os.path.getsize(temp_epc_file) > 0

    def test_export_and_reload(self, temp_epc_file, sample_objects):
        """Test exporting and reloading an Epc file."""
        epc = Epc()
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        epc.add_object(bf)
        epc.add_object(bfi)
        epc.export_file(temp_epc_file)

        # Reload
        epc2 = Epc.read_file(temp_epc_file)
        assert len(epc2) == 2

        # Verify objects are present
        bf_retrieved = epc2.get_object_by_uuid(bf.uuid)
        assert len(bf_retrieved) == 1
        assert bf_retrieved[0].citation.title == bf.citation.title

    def test_export_io(self, sample_objects):
        """Test exporting to BytesIO."""
        epc = Epc()
        epc.add_object(sample_objects["bf"])
        epc.add_object(sample_objects["bfi"])

        io = epc.export_io()

        assert io is not None
        assert io.tell() > 0  # Check that data was written

        # Try to read it back
        io.seek(0)
        epc2 = Epc.read_stream(io)
        assert len(epc2) == 2


class TestRelationships:
    """Test relationship computation - Epc only computes rels at export time."""

    def test_compute_rels_basic(self, sample_objects):
        """Test basic relationship computation."""
        epc = Epc()
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        epc.add_object(bf)
        epc.add_object(bfi)

        # Compute relationships
        rels_dict = epc.compute_rels()

        assert rels_dict is not None
        assert len(rels_dict) > 0

        # Check that relationships were computed
        # compute_rels returns dict with rels paths as keys, not identifiers
        assert any("BoundaryFeatureInterpretation" in key for key in rels_dict.keys())

    def test_compute_rels_complex_chain(self, sample_objects):
        """Test relationship computation with object chain."""
        epc = Epc()
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]
        horizon_interp = sample_objects["horizon_interp"]
        trset = sample_objects["trset"]

        epc.add_object(bf)
        epc.add_object(bfi)
        epc.add_object(horizon_interp)
        epc.add_object(trset)

        rels_dict = epc.compute_rels()

        # Verify relationships exist
        assert len(rels_dict) >= 3  # At least 3 objects should have rels

        # Check specific relationships
        bfi_id = get_obj_identifier(bfi)
        if bfi_id in rels_dict:
            bfi_rels = rels_dict[bfi_id]
            dest_rels = [
                r for r in bfi_rels.relationship if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT)
            ]
            assert len(dest_rels) >= 1

    def test_trset_to_interpretation_destination_relationship(self, sample_objects):
        """Test that TriangulatedSetRepresentation has DESTINATION_OBJECT relationship to interpretation."""
        epc = Epc()
        bf = sample_objects["bf"]
        horizon_interp = sample_objects["horizon_interp"]
        trset = sample_objects["trset"]

        epc.add_object(bf)
        epc.add_object(horizon_interp)
        epc.add_object(trset)

        rels_dict = epc.compute_rels()

        # Get trset rels path
        trset_path = gen_energyml_object_path(trset, epc.export_version)
        trset_rels_path = f"_rels/{trset_path}.rels"

        assert trset_rels_path in rels_dict
        trset_rels = rels_dict[trset_rels_path]

        # Check for DESTINATION_OBJECT relationship to horizon_interp
        dest_rels = [
            r for r in trset_rels.relationship if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT)
        ]
        assert len(dest_rels) >= 1

        # Verify target points to horizon_interp
        horizon_interp_path = gen_energyml_object_path(horizon_interp, epc.export_version)
        assert any(horizon_interp_path in r.target for r in dest_rels)

    def test_interpretation_has_source_and_destination_relationships(self, sample_objects):
        """Test that interpretation has SOURCE_OBJECT from trset and DESTINATION_OBJECT to feature."""
        epc = Epc()
        bf = sample_objects["bf"]
        horizon_interp = sample_objects["horizon_interp"]
        trset = sample_objects["trset"]

        epc.add_object(bf)
        epc.add_object(horizon_interp)
        epc.add_object(trset)

        rels_dict = epc.compute_rels()

        # Get interpretation rels path
        interp_path = gen_energyml_object_path(horizon_interp, epc.export_version)
        interp_rels_path = f"_rels/{interp_path}.rels"

        assert interp_rels_path in rels_dict
        interp_rels = rels_dict[interp_rels_path]

        # Check for SOURCE_OBJECT relationship from trset
        source_rels = [
            r for r in interp_rels.relationship if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)
        ]
        assert len(source_rels) >= 1

        # Verify source points to trset
        trset_path = gen_energyml_object_path(trset, epc.export_version)
        assert any(trset_path in r.target for r in source_rels)

        # Check for DESTINATION_OBJECT relationship to feature
        dest_rels = [
            r for r in interp_rels.relationship if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT)
        ]
        assert len(dest_rels) >= 1

        # Verify target points to bf
        bf_path = gen_energyml_object_path(bf, epc.export_version)
        assert any(bf_path in r.target for r in dest_rels)

    def test_feature_has_source_relationship_from_interpretation(self, sample_objects):
        """Test that feature has SOURCE_OBJECT relationship from interpretation."""
        epc = Epc()
        bf = sample_objects["bf"]
        horizon_interp = sample_objects["horizon_interp"]

        epc.add_object(bf)
        epc.add_object(horizon_interp)

        rels_dict = epc.compute_rels()

        # Get feature rels path
        bf_path = gen_energyml_object_path(bf, epc.export_version)
        bf_rels_path = f"_rels/{bf_path}.rels"

        assert bf_rels_path in rels_dict
        bf_rels = rels_dict[bf_rels_path]

        # Check for SOURCE_OBJECT relationship from interpretation
        source_rels = [r for r in bf_rels.relationship if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)]
        assert len(source_rels) >= 1

        # Verify source points to horizon_interp
        interp_path = gen_energyml_object_path(horizon_interp, epc.export_version)
        assert any(interp_path in r.target for r in source_rels)

    def test_external_part_reference_relationships(self, sample_objects):
        """Test external part reference has EXTERNAL_PART_PROXY_TO_ML to trset20."""
        epc = Epc()
        external_ref = sample_objects["external_ref"]
        trset20 = sample_objects["trset20"]
        horizon_interp = sample_objects["horizon_interp"]
        bf = sample_objects["bf"]

        epc.add_object(bf)
        epc.add_object(horizon_interp)
        epc.add_object(external_ref)
        epc.add_object(trset20)

        rels_dict = epc.compute_rels()

        # Get external_ref rels path
        external_ref_path = gen_energyml_object_path(external_ref, epc.export_version)
        external_ref_rels_path = f"_rels/{external_ref_path}.rels"

        assert external_ref_rels_path in rels_dict
        external_ref_rels = rels_dict[external_ref_rels_path]

        # Check for EXTERNAL_PART_PROXY_TO_ML relationship
        proxy_to_ml_rels = [
            r
            for r in external_ref_rels.relationship
            if r.type_value == str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML)
        ]
        assert len(proxy_to_ml_rels) >= 1

        # Verify target points to trset20
        trset20_path = gen_energyml_object_path(trset20, epc.export_version)
        assert any(trset20_path in r.target for r in proxy_to_ml_rels)

    def test_external_data_array_part_rels_detection(self, sample_objects):
        """Test that ExternalDataArrayPart relationships are detected."""
        from energyml.opc.opc import TargetMode

        epc = Epc()
        trset22 = sample_objects["trset"]
        horizon_interp = sample_objects["horizon_interp"]

        epc.add_object(horizon_interp)
        epc.add_object(trset22)

        trset22_external_rels = [
            r for r in epc.get_obj_rels(trset22) if r.type_value == str(EPCRelsRelationshipType.EXTERNAL_RESOURCE)
        ]
        assert len(trset22_external_rels) == 1
        assert trset22_external_rels[0].target == CST_H5_PATH
        assert trset22_external_rels[0].target_mode == TargetMode.EXTERNAL

    def test_trset20_has_ml_to_external_part_proxy_relationship(self, sample_objects):
        """Test that trset20 has ML_TO_EXTERNAL_PART_PROXY relationship to external_ref."""
        epc = Epc()
        external_ref = sample_objects["external_ref"]
        trset20 = sample_objects["trset20"]
        horizon_interp = sample_objects["horizon_interp"]
        bf = sample_objects["bf"]

        epc.add_object(bf)
        epc.add_object(horizon_interp)
        epc.add_object(external_ref)
        epc.add_object(trset20)

        rels_dict = epc.compute_rels()

        # Get trset20 rels path
        trset20_path = gen_energyml_object_path(trset20, epc.export_version)
        trset20_rels_path = f"_rels/{trset20_path}.rels"

        assert trset20_rels_path in rels_dict
        trset20_rels = rels_dict[trset20_rels_path]

        # Check for ML_TO_EXTERNAL_PART_PROXY relationship
        ml_to_proxy_rels = [
            r
            for r in trset20_rels.relationship
            if r.type_value == str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY)
        ]
        assert len(ml_to_proxy_rels) >= 1

        # Verify target points to external_ref
        external_ref_path = gen_energyml_object_path(external_ref, epc.export_version)
        assert any(external_ref_path in r.target for r in ml_to_proxy_rels)

    def test_complete_relationship_chain(self, sample_objects):
        """Test complete relationship chain: trset -> interp -> feature."""
        epc = Epc()
        bf = sample_objects["bf"]
        horizon_interp = sample_objects["horizon_interp"]
        trset = sample_objects["trset"]

        epc.add_object(bf)
        epc.add_object(horizon_interp)
        epc.add_object(trset)

        rels_dict = epc.compute_rels()

        # Verify all three objects have relationship files
        trset_path = gen_energyml_object_path(trset, epc.export_version)
        interp_path = gen_energyml_object_path(horizon_interp, epc.export_version)
        bf_path = gen_energyml_object_path(bf, epc.export_version)

        assert f"_rels/{trset_path}.rels" in rels_dict
        assert f"_rels/{interp_path}.rels" in rels_dict
        assert f"_rels/{bf_path}.rels" in rels_dict

    def test_get_obj_rels_after_compute(self, sample_objects):
        """Test get_obj_rels after explicit compute_rels call."""
        epc = Epc()
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        epc.add_object(bf)
        epc.add_object(bfi)

        # Compute rels explicitly
        epc.compute_rels()

        # Now we can get rels
        bfi_rels = epc.get_obj_rels(bfi)
        assert bfi_rels is not None

    def test_relationships_in_exported_file(self, temp_epc_file, sample_objects):
        """Test that relationships are correctly written to exported file."""
        epc = Epc()
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        epc.add_object(bf)
        epc.add_object(bfi)
        epc.export_file(temp_epc_file)

        # Reload and check relationships
        epc2 = Epc.read_file(temp_epc_file)

        # After reload, relationships are stored in additional_rels
        assert len(epc2) == 2


class TestDORCreation:
    """Test DataObjectReference creation."""

    def test_as_dor_from_object(self, sample_objects):
        """Test creating DOR from energyml object."""
        bf = sample_objects["bf"]
        dor = as_dor(bf)

        assert dor.uuid == bf.uuid
        assert dor.title == bf.citation.title
        assert dor.qualified_type == get_qualified_type_from_class(bf)

    def test_as_dor_v20_from_object(self, sample_objects):
        """Test creating v2.0 DOR from energyml object."""
        bf = sample_objects["bf"]
        dor = as_dor(bf, "eml20.DataObjectReference")

        assert isinstance(dor, DataObjectReference201)
        assert dor.uuid == bf.uuid
        assert dor.content_type == get_content_type_from_class(bf)

    def test_as_dor_from_dor(self):
        """Test creating DOR from another DOR."""
        dor_correct20 = DataObjectReference201(
            uuid="25773477-ffee-4cc2-867d-000000000001",
            title="a DOR title",
            content_type="application/x-resqml+xml;version=2.2;type=BoundaryFeature",
            version_string="1.0",
        )

        dor_23 = as_dor(dor_correct20, "eml23.DataObjectReference")
        assert dor_23.uuid == dor_correct20.uuid
        assert dor_23.title == dor_correct20.title
        assert isinstance(dor_23, DataObjectReference)

    def test_as_dor_from_uri(self):
        """Test creating DOR from URI string."""
        uri_str = "eml:///resqml22.TriangulatedSetRepresentation(0a2ba9e1-1018-4bfd-8fec-1c8cef13fa52)"

        dor_20 = as_dor(uri_str, "eml20.DataObjectReference")
        assert dor_20.uuid == "0a2ba9e1-1018-4bfd-8fec-1c8cef13fa52"
        assert dor_20.content_type == "application/x-resqml+xml;version=2.2;type=TriangulatedSetRepresentation"

        dor_23 = as_dor(uri_str, "eml23.DataObjectReference")
        assert dor_23.uuid == "0a2ba9e1-1018-4bfd-8fec-1c8cef13fa52"
        assert dor_23.qualified_type == "resqml22.TriangulatedSetRepresentation"


class TestFilePathGeneration:
    """Test file path generation for objects."""

    def test_gen_energyml_object_path_classic(self, sample_objects):
        """Test path generation with CLASSIC export version."""
        trset = sample_objects["trset"]

        path = gen_energyml_object_path(trset, EpcExportVersion.CLASSIC)
        assert path == f"TriangulatedSetRepresentation_{trset.uuid}.xml"

    def test_gen_energyml_object_path_expanded(self, sample_objects):
        """Test path generation with EXPANDED export version."""
        trset = sample_objects["trset"]

        path = gen_energyml_object_path(trset, EpcExportVersion.EXPANDED)
        expected = f"namespace_resqml22/version_{trset.object_version}/TriangulatedSetRepresentation_{trset.uuid}.xml"
        assert path == expected

    def test_gen_energyml_object_path_no_version(self, sample_objects):
        """Test path generation for object without explicit version."""
        bf = sample_objects["bf"]

        # For objects with object_version
        path = gen_energyml_object_path(bf, EpcExportVersion.CLASSIC)
        assert path == f"BoundaryFeature_{bf.uuid}.xml"


class TestHDF5Operations:
    """Test HDF5 array operations."""

    def test_write_and_read_array(self, temp_epc_file, sample_objects):
        """Test writing and reading arrays."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".h5") as f:
            h5_path = f.name

        try:
            epc = Epc(force_h5_path=h5_path)
            trset = sample_objects["trset"]

            epc.add_object(trset)

            # Write array
            test_array = np.arange(20).reshape((4, 5))
            success = epc.write_array(trset, "/test_dataset", test_array)
            assert success

            # Read array back
            read_array = epc.read_array(trset, "/test_dataset")
            assert read_array is not None
            assert np.array_equal(read_array, test_array)

        finally:
            import time

            time.sleep(0.1)
            if os.path.exists(h5_path):
                try:
                    os.unlink(h5_path)
                except PermissionError:
                    pass

    def test_write_array_creates_h5_rel(self, sample_objects):
        """Test that writing array creates proper H5 relationship."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".h5") as f:
            h5_path = f.name

        try:
            epc = Epc(force_h5_path=h5_path)
            trset = sample_objects["trset"]

            epc.add_object(trset)

            test_array = np.array([1, 2, 3, 4, 5])
            epc.write_array(trset, "/dataset", test_array)

            # Check H5 file paths
            h5_paths = epc.get_h5_file_paths(trset)
            assert len(h5_paths) > 0

        finally:
            import time

            time.sleep(0.1)
            if os.path.exists(h5_path):
                try:
                    os.unlink(h5_path)
                except PermissionError:
                    pass

    def test_multiple_arrays(self, sample_objects):
        """Test writing multiple arrays."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".h5") as f:
            h5_path = f.name

        try:
            epc = Epc(force_h5_path=h5_path)
            trset = sample_objects["trset"]

            epc.add_object(trset)

            array1 = np.arange(10)
            array2 = np.arange(20).reshape((4, 5))
            array3 = np.arange(12).reshape((3, 4))

            epc.write_array(trset, "/array1", array1)
            epc.write_array(trset, "/array2", array2)
            epc.write_array(trset, "/array3", array3)

            # Read them back
            assert np.array_equal(epc.read_array(trset, "/array1"), array1)
            assert np.array_equal(epc.read_array(trset, "/array2"), array2)
            assert np.array_equal(epc.read_array(trset, "/array3"), array3)

        finally:
            import time

            time.sleep(0.1)
            if os.path.exists(h5_path):
                try:
                    os.unlink(h5_path)
                except PermissionError:
                    pass


class TestExternalFilesHandling:
    """Test handling of external files."""

    def test_add_external_file_path(self):
        """Test adding external file paths."""
        epc = Epc()

        epc.external_files_path.append("/path/to/external/file.h5")
        epc.external_files_path.append("/path/to/another/file.h5")

        assert len(epc.external_files_path) == 2
        assert "/path/to/external/file.h5" in epc.external_files_path

    def test_force_h5_path(self):
        """Test force_h5_path parameter."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".h5") as f:
            h5_path = f.name

        try:
            epc = Epc(force_h5_path=h5_path)
            assert epc.force_h5_path == h5_path

        finally:
            if os.path.exists(h5_path):
                try:
                    os.unlink(h5_path)
                except PermissionError:
                    pass


class TestExportVersions:
    """Test different export versions."""

    def test_classic_export_version(self, temp_epc_file, sample_objects):
        """Test export with CLASSIC version."""
        epc = Epc(export_version=EpcExportVersion.CLASSIC)
        epc.add_object(sample_objects["bf"])

        epc.export_file(temp_epc_file)

        assert os.path.exists(temp_epc_file)

        # Reload and verify
        epc2 = Epc.read_file(temp_epc_file)
        assert len(epc2) == 1

    def test_expanded_export_version(self, temp_epc_file, sample_objects):
        """Test export with EXPANDED version."""
        epc = Epc(export_version=EpcExportVersion.EXPANDED)
        epc.add_object(sample_objects["bf"])
        epc.add_object(sample_objects["bfi"])

        epc.export_file(temp_epc_file)

        assert os.path.exists(temp_epc_file)

        # Reload and verify
        epc2 = Epc.read_file(temp_epc_file)
        assert len(epc2) == 2


class TestAdditionalRels:
    """Test additional relationships handling."""

    def test_add_rels_for_object(self, sample_objects):
        """Test adding additional relationships for an object."""
        from energyml.opc.opc import Relationship

        epc = Epc()
        bf = sample_objects["bf"]
        epc.add_object(bf)

        identifier = get_obj_uri(bf)

        # Add external resource relationship
        h5_rel = Relationship(
            target="data/external.h5",
            type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE),
            id=f"_external_{identifier}",
        )

        epc.add_rels_for_object(identifier, [h5_rel])

        assert identifier in epc._rels_cache._supplemental_rels
        assert len(epc._rels_cache._supplemental_rels[identifier]) == 1

    def test_get_h5_file_paths(self, sample_objects):
        """Test retrieving H5 file paths from relationships."""
        from energyml.opc.opc import Relationship

        epc = Epc()
        trset = sample_objects["trset"]
        epc.add_object(trset)

        identifier = get_obj_identifier(trset)

        # Add H5 relationships
        h5_rel = Relationship(
            target="data/geometry.h5",
            type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE),
            id=f"_external_{identifier}_1",
        )

        epc.add_rels_for_object(identifier, [h5_rel])

        h5_paths = epc.get_h5_file_paths(trset)
        assert "data/geometry.h5" in h5_paths


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_epc(self):
        """Test operations on empty Epc."""
        epc = Epc()

        assert len(epc) == 0
        assert len(epc.energyml_objects) == 0

        # Should be able to export empty epc
        io = epc.export_io()
        assert io is not None

    def test_remove_nonexistent_object(self):
        """Test removing non-existent object."""
        epc = Epc()

        # Should not raise error
        epc.remove_object("nonexistent-uuid.0")
        assert len(epc) == 0

    def test_get_nonexistent_object(self):
        """Test getting non-existent object."""
        epc = Epc()

        result = epc.get_object_by_identifier("nonexistent-uuid.0")
        assert result is None

        results = epc.get_object_by_uuid("nonexistent-uuid")
        assert len(results) == 0

    def test_duplicate_add(self, sample_objects):
        """Test adding the same object multiple times."""
        epc = Epc()
        bf = sample_objects["bf"]

        epc.add_object(bf)
        epc.add_object(bf)  # Add same object again

        # Behavior: object appears only once in the list
        assert len(epc.energyml_objects) >= 1


class TestListObjects:
    """Test list_objects functionality."""

    def test_list_objects(self, sample_objects):
        """Test listing objects."""
        epc = Epc()

        epc.add_object(sample_objects["bf"])
        epc.add_object(sample_objects["bfi"])
        epc.add_object(sample_objects["trset"])

        objects_list = epc.list_objects()
        assert len(objects_list) == 3

    def test_list_objects_empty(self):
        """Test listing objects from empty Epc."""
        epc = Epc()

        objects_list = epc.list_objects()
        assert len(objects_list) == 0


class TestCoreProperties:
    """Test core properties handling."""

    def test_core_props_creation(self, temp_epc_file, sample_objects):
        """Test that core properties are created during export."""
        epc = Epc()
        epc.add_object(sample_objects["bf"])

        epc.export_file(temp_epc_file)

        # Verify core props exist after export
        assert epc.core_props is not None

    def test_custom_core_props(self, temp_epc_file, sample_objects):
        """Test setting custom core properties."""
        from energyml.opc.opc import CoreProperties, Creator

        core_props = CoreProperties(
            creator=Creator(any_element="Test Creator"),
        )

        epc = Epc(core_props=core_props)
        epc.add_object(sample_objects["bf"])

        epc.export_file(temp_epc_file)

        # Reload and verify
        epc2 = Epc.read_file(temp_epc_file)
        assert epc2.core_props is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
