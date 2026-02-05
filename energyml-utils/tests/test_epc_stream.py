# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Comprehensive unit tests for EpcStreamReader functionality.

Tests cover:
1. Relationship update modes (UPDATE_AT_MODIFICATION, UPDATE_ON_CLOSE, MANUAL)
2. Object lifecycle (add, update, remove)
3. Relationship consistency
4. Performance and caching
5. Edge cases and error handling
"""
import os
import tempfile
import zipfile
from pathlib import Path

import pytest
import numpy as np

from energyml.eml.v2_3.commonv2 import Citation, DataObjectReference
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    BoundaryFeatureInterpretation,
    BoundaryFeature,
    HorizonInterpretation,
)
from energyml.opc.opc import Relationships

from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.utils.epc import create_energyml_object, as_dor, get_obj_identifier
from energyml.utils.introspection import (
    epoch_to_date,
    epoch,
    gen_uuid,
    get_direct_dor_list,
)
from energyml.utils.constants import EPCRelsRelationshipType
from energyml.utils.serialization import read_energyml_xml_bytes


@pytest.fixture
def temp_epc_file():
    """Create a temporary EPC file path for testing."""
    # Create temp file path but don't create the file itself
    # Let EpcStreamReader create it
    fd, temp_path = tempfile.mkstemp(suffix=".epc")
    os.close(fd)  # Close the file descriptor
    os.unlink(temp_path)  # Remove the empty file

    yield temp_path

    # Cleanup
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
        uuid=gen_uuid(),
        object_version="1.0",
    )

    # Create a BoundaryFeatureInterpretation
    bfi = BoundaryFeatureInterpretation(
        citation=Citation(
            title="Test Boundary Feature Interpretation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid=gen_uuid(),
        object_version="1.0",
        interpreted_feature=as_dor(bf),
    )

    # Create a TriangulatedSetRepresentation
    trset = TriangulatedSetRepresentation(
        citation=Citation(
            title="Test TriangulatedSetRepresentation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid=gen_uuid(),
        object_version="1.0",
        represented_object=as_dor(bfi),
    )

    # Create a HorizonInterpretation (independent object)
    horizon_interp = HorizonInterpretation(
        citation=Citation(
            title="Test HorizonInterpretation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid=gen_uuid(),
        object_version="1.0",
        domain="depth",
    )

    return {
        "bf": bf,
        "bfi": bfi,
        "trset": trset,
        "horizon_interp": horizon_interp,
    }


class TestRelsUpdateModes:
    """Test different relationship update modes."""

    def test_manual_mode_no_auto_rebuild(self, temp_epc_file, sample_objects):
        """Test that MANUAL mode does not automatically rebuild relationships on close."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.MANUAL)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        # Add objects in MANUAL mode
        reader.add_object(bf)
        reader.add_object(bfi)

        # Close without rebuild (MANUAL mode should not call rebuild_all_rels)
        reader.close()

        # Reopen and check - rels should exist from _add_object_to_file
        # but they won't be "rebuilt" from scratch
        reader2 = EpcStreamReader(temp_epc_file)

        # Objects should be there
        assert len(reader2) == 2

        # Basic rels should exist (from _add_object_to_file)
        bfi_rels = reader2.get_obj_rels(get_obj_identifier(bfi))
        assert len(bfi_rels) > 0  # Should have SOURCE rels

        reader2.close()

    def test_update_on_close_mode(self, temp_epc_file, sample_objects):
        """Test that UPDATE_ON_CLOSE mode rebuilds rels on close."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]
        trset = sample_objects["trset"]

        # Add objects
        reader.add_object(bf)
        reader.add_object(bfi)
        reader.add_object(trset)

        # Before closing, rels may not be complete
        reader.close()

        # Reopen and verify relationships were built
        reader2 = EpcStreamReader(temp_epc_file)

        # Check that bfi has a SOURCE relationship to bf
        bfi_rels = reader2.get_obj_rels(get_obj_identifier(bfi))
        source_rels = [r for r in bfi_rels if r.type_value == EPCRelsRelationshipType.SOURCE_OBJECT.get_type()]
        assert len(source_rels) >= 1, "Expected SOURCE relationship from bfi to bf"

        # Check that bf has a DESTINATION relationship from bfi
        bf_rels = reader2.get_obj_rels(get_obj_identifier(bf))
        dest_rels = [r for r in bf_rels if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()]
        assert len(dest_rels) >= 1, "Expected DESTINATION relationship from bfi to bf"

        reader2.close()

    def test_update_at_modification_mode_add(self, temp_epc_file, sample_objects):
        """Test that UPDATE_AT_MODIFICATION mode updates rels immediately on add."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        # Add objects
        reader.add_object(bf)
        reader.add_object(bfi)

        # Check relationships immediately (without closing)
        bfi_rels = reader.get_obj_rels(get_obj_identifier(bfi))
        source_rels = [r for r in bfi_rels if r.type_value == EPCRelsRelationshipType.SOURCE_OBJECT.get_type()]
        assert len(source_rels) >= 1, "Expected immediate SOURCE relationship from bfi to bf"

        bf_rels = reader.get_obj_rels(get_obj_identifier(bf))
        dest_rels = [r for r in bf_rels if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()]
        assert len(dest_rels) >= 1, "Expected immediate DESTINATION relationship from bfi to bf"

        reader.close()

    def test_update_at_modification_mode_remove(self, temp_epc_file, sample_objects):
        """Test that UPDATE_AT_MODIFICATION mode cleans up rels on remove."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        # Add objects
        reader.add_object(bf)
        reader.add_object(bfi)

        # Verify relationships exist
        bf_rels_before = reader.get_obj_rels(get_obj_identifier(bf))
        assert len(bf_rels_before) > 0, "Expected relationships before removal"

        # Remove bfi
        reader.remove_object(get_obj_identifier(bfi))

        # Check that bf's rels no longer has references to bfi
        bf_rels_after = reader.get_obj_rels(get_obj_identifier(bf))
        bfi_refs = [r for r in bf_rels_after if get_obj_identifier(bfi) in r.id]
        assert len(bfi_refs) == 0, "Expected no references to removed object"

        reader.close()

    def test_update_at_modification_mode_update(self, temp_epc_file, sample_objects):
        """Test that UPDATE_AT_MODIFICATION mode updates rels on object modification."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]
        trset = sample_objects["trset"]

        # Add initial objects
        reader.add_object(bf)
        reader.add_object(bfi)
        reader.add_object(trset)

        # Modify bfi to reference a different feature (create new one)
        bf2 = BoundaryFeature(
            citation=Citation(
                title="Test Boundary Feature 2",
                originator="Test",
                creation=epoch_to_date(epoch()),
            ),
            uuid=gen_uuid(),
            object_version="1.0",
        )
        reader.add_object(bf2)

        # Update bfi to reference bf2 instead of bf
        bfi_modified = BoundaryFeatureInterpretation(
            citation=bfi.citation,
            uuid=bfi.uuid,
            object_version=bfi.object_version,
            interpreted_feature=as_dor(bf2),
        )

        reader.update_object(bfi_modified)

        # Check that bf no longer has DESTINATION relationship from bfi
        bf_rels = reader.get_obj_rels(get_obj_identifier(bf))
        bfi_dest_rels = [
            r
            for r in bf_rels
            if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type() and get_obj_identifier(bfi) in r.id
        ]
        assert len(bfi_dest_rels) == 0, "Expected old DESTINATION relationship to be removed"

        # Check that bf2 now has DESTINATION relationship from bfi
        bf2_rels = reader.get_obj_rels(get_obj_identifier(bf2))
        bfi_dest_rels2 = [
            r
            for r in bf2_rels
            if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type() and get_obj_identifier(bfi) in r.id
        ]
        assert len(bfi_dest_rels2) >= 1, "Expected new DESTINATION relationship to be added"

        reader.close()


class TestObjectLifecycle:
    """Test object lifecycle operations."""

    def test_add_object(self, temp_epc_file, sample_objects):
        """Test adding objects to EPC."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        assert identifier == get_obj_identifier(bf)
        assert identifier in reader._metadata
        assert reader.get_object_by_identifier(identifier) is not None

        reader.close()

    def test_remove_object(self, temp_epc_file, sample_objects):
        """Test removing objects from EPC."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        result = reader.remove_object(identifier)
        assert result is True
        assert identifier not in reader._metadata
        assert reader.get_object_by_identifier(identifier) is None

        reader.close()

    def test_update_object(self, temp_epc_file, sample_objects):
        """Test updating existing objects."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        # Modify the object
        bf_modified = BoundaryFeature(
            citation=Citation(
                title="Modified Title",
                originator="Test",
                creation=epoch_to_date(epoch()),
            ),
            uuid=bf.uuid,
            object_version=bf.object_version,
        )

        new_identifier = reader.update_object(bf_modified)
        assert new_identifier == identifier

        # Verify the object was updated
        obj = reader.get_object_by_identifier(identifier)
        assert obj.citation.title == "Modified Title"

        reader.close()

    def test_replace_if_exists(self, temp_epc_file, sample_objects):
        """Test replace_if_exists parameter."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        # Try to add same object again with replace_if_exists=False
        with pytest.raises((ValueError, RuntimeError)) as exc_info:
            reader.add_object(bf, replace_if_exists=False)
        # The error message should mention the object already exists
        assert "already exists" in str(exc_info.value).lower()

        # Should work with replace_if_exists=True (default)
        identifier2 = reader.add_object(bf, replace_if_exists=True)
        assert identifier == identifier2

        reader.close()


class TestRelationshipConsistency:
    """Test relationship consistency and correctness."""

    def test_bidirectional_relationships(self, temp_epc_file, sample_objects):
        """Test that SOURCE and DESTINATION relationships are bidirectional."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        reader.add_object(bf)
        reader.add_object(bfi)

        # Check bfi -> bf (SOURCE)
        bfi_rels = reader.get_obj_rels(get_obj_identifier(bfi))
        bfi_source_to_bf = [
            r
            for r in bfi_rels
            if r.type_value == EPCRelsRelationshipType.SOURCE_OBJECT.get_type() and get_obj_identifier(bf) in r.id
        ]
        assert len(bfi_source_to_bf) >= 1

        # Check bf -> bfi (DESTINATION)
        bf_rels = reader.get_obj_rels(get_obj_identifier(bf))
        bf_dest_from_bfi = [
            r
            for r in bf_rels
            if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type() and get_obj_identifier(bfi) in r.id
        ]
        assert len(bf_dest_from_bfi) >= 1

        reader.close()

    def test_cascade_relationships(self, temp_epc_file, sample_objects):
        """Test relationships in a chain: trset -> bfi -> bf."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]
        trset = sample_objects["trset"]

        reader.add_object(bf)
        reader.add_object(bfi)
        reader.add_object(trset)

        # Check trset -> bfi
        trset_rels = reader.get_obj_rels(get_obj_identifier(trset))
        trset_to_bfi = [
            r
            for r in trset_rels
            if r.type_value == EPCRelsRelationshipType.SOURCE_OBJECT.get_type() and get_obj_identifier(bfi) in r.id
        ]
        assert len(trset_to_bfi) >= 1

        # Check bfi -> bf
        bfi_rels = reader.get_obj_rels(get_obj_identifier(bfi))
        bfi_to_bf = [
            r
            for r in bfi_rels
            if r.type_value == EPCRelsRelationshipType.SOURCE_OBJECT.get_type() and get_obj_identifier(bf) in r.id
        ]
        assert len(bfi_to_bf) >= 1

        # Check bf has 2 DESTINATION relationships (from bfi and indirectly from trset)
        bf_rels = reader.get_obj_rels(get_obj_identifier(bf))
        bf_dest_rels = [r for r in bf_rels if r.type_value == EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()]
        assert len(bf_dest_rels) >= 1

        reader.close()

    def test_independent_objects_no_rels(self, temp_epc_file, sample_objects):
        """Test that independent objects don't have relationships between two boundary features."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        # Use two boundary features with no references to each other
        bf1 = sample_objects["bf"]
        bf2 = BoundaryFeature(
            uuid="00000000-0000-0000-0000-000000000099",
            citation=Citation(title="Second Boundary Feature", originator="Test", creation="2026-01-01T00:00:00Z"),
        )

        reader.add_object(bf1)
        reader.add_object(bf2)

        # Check that bf2 has no relationships to bf1
        bf2_rels = reader.get_obj_rels(get_obj_identifier(bf2))
        bf1_refs = [r for r in bf2_rels if get_obj_identifier(bf1) in r.id]
        assert len(bf1_refs) == 0

        reader.close()


class TestCachingAndPerformance:
    """Test caching functionality and performance optimizations."""

    def test_cache_hit_rate(self, temp_epc_file, sample_objects):
        """Test that cache is working properly."""
        reader = EpcStreamReader(temp_epc_file, cache_size=10)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        # First access - cache miss
        obj1 = reader.get_object_by_identifier(identifier)
        stats1 = reader.get_statistics()

        # Second access - cache hit
        obj2 = reader.get_object_by_identifier(identifier)
        stats2 = reader.get_statistics()

        assert stats2.cache_hits >= stats1.cache_hits
        assert obj1 is obj2  # Should be same object reference

        reader.close()

    def test_metadata_access_without_loading(self, temp_epc_file, sample_objects):
        """Test that metadata can be accessed without loading full objects."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        reader.add_object(bf)
        reader.add_object(bfi)

        reader.close()

        # Reopen and access metadata
        reader2 = EpcStreamReader(temp_epc_file, preload_metadata=True)

        # Check that we can list objects without loading them
        metadata_list = reader2.list_object_metadata()
        assert len(metadata_list) == 2
        assert reader2.stats.loaded_objects == 0, "Expected no objects loaded when accessing metadata"

        reader2.close()

    def test_lazy_loading(self, temp_epc_file, sample_objects):
        """Test that objects are loaded on-demand."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]
        trset = sample_objects["trset"]

        reader.add_object(bf)
        reader.add_object(bfi)
        reader.add_object(trset)

        reader.close()

        # Reopen
        reader2 = EpcStreamReader(temp_epc_file)
        assert len(reader2) == 3
        assert reader2.stats.loaded_objects == 0, "Expected no objects loaded initially"

        # Load one object
        reader2.get_object_by_identifier(get_obj_identifier(bf))
        assert reader2.stats.loaded_objects == 1, "Expected exactly 1 object loaded"

        reader2.close()


class TestHelperMethods:
    """Test helper methods for rels path generation."""

    def test_gen_rels_path_from_metadata(self, temp_epc_file, sample_objects):
        """Test generating rels path from metadata."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        metadata = reader._metadata[identifier]
        rels_path = reader._gen_rels_path_from_metadata(metadata)

        assert rels_path is not None
        assert "_rels/" in rels_path
        assert ".rels" in rels_path

        reader.close()

    def test_gen_rels_path_from_identifier(self, temp_epc_file, sample_objects):
        """Test generating rels path from identifier."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]
        identifier = reader.add_object(bf)

        rels_path = reader._gen_rels_path_from_identifier(identifier)

        assert rels_path is not None
        assert "_rels/" in rels_path
        assert ".rels" in rels_path

        reader.close()


class TestModeManagement:
    """Test mode switching and management."""

    def test_set_rels_update_mode(self, temp_epc_file):
        """Test changing the relationship update mode."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.MANUAL)

        assert reader.get_rels_update_mode() == RelsUpdateMode.MANUAL

        reader.set_rels_update_mode(RelsUpdateMode.UPDATE_AT_MODIFICATION)
        assert reader.get_rels_update_mode() == RelsUpdateMode.UPDATE_AT_MODIFICATION

        reader.close()

    def test_invalid_mode_raises_error(self, temp_epc_file):
        """Test that invalid mode raises error."""
        reader = EpcStreamReader(temp_epc_file)

        with pytest.raises(ValueError):
            reader.set_rels_update_mode("invalid_mode")

        reader.close()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_remove_nonexistent_object(self, temp_epc_file):
        """Test removing an object that doesn't exist."""
        reader = EpcStreamReader(temp_epc_file)

        result = reader.remove_object("nonexistent-uuid.0")
        assert result is False

        reader.close()

    def test_update_nonexistent_object(self, temp_epc_file, sample_objects):
        """Test updating an object that doesn't exist."""
        reader = EpcStreamReader(temp_epc_file)

        bf = sample_objects["bf"]

        with pytest.raises(ValueError):
            reader.update_object(bf)

        reader.close()

    def test_empty_epc_operations(self, temp_epc_file):
        """Test operations on empty EPC."""
        reader = EpcStreamReader(temp_epc_file)

        assert len(reader) == 0
        assert len(reader.list_object_metadata()) == 0

        reader.close()

    def test_multiple_add_remove_cycles(self, temp_epc_file, sample_objects):
        """Test multiple add/remove cycles."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        bf = sample_objects["bf"]

        for _ in range(3):
            identifier = reader.add_object(bf)
            assert identifier in reader._metadata

            reader.remove_object(identifier)
            assert identifier not in reader._metadata

        reader.close()


class TestRebuildAllRels:
    """Test the rebuild_all_rels functionality."""

    def test_rebuild_all_rels_manual_mode(self, temp_epc_file, sample_objects):
        """Test manually rebuilding relationships in MANUAL mode."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.MANUAL)

        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        reader.add_object(bf)
        reader.add_object(bfi)

        # Manually rebuild relationships
        stats = reader.rebuild_all_rels(clean_first=True)

        assert stats["objects_processed"] == 2
        assert stats["source_relationships"] >= 1
        assert stats["destination_relationships"] >= 1

        # Verify relationships exist now
        bfi_rels = reader.get_obj_rels(get_obj_identifier(bfi))
        assert len(bfi_rels) > 0

        reader.close()


class TestArrayOperations:
    """Test HDF5 array operations."""

    def test_write_read_array(self, temp_epc_file, sample_objects):
        """Test writing and reading arrays."""
        # Create temp HDF5 file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".h5") as f:
            h5_path = f.name

        try:
            reader = EpcStreamReader(temp_epc_file, force_h5_path=h5_path)

            trset = sample_objects["trset"]
            reader.add_object(trset)

            # Write array
            test_array = np.arange(12).reshape((3, 4))
            success = reader.write_array(trset, "/test_dataset", test_array)
            assert success

            # Read array back
            read_array = reader.read_array(trset, "/test_dataset")
            assert read_array is not None
            assert np.array_equal(read_array, test_array)

            # Close reader before deleting files
            reader.close()
        finally:
            # Give time for file handles to be released
            import time

            time.sleep(0.1)
            if os.path.exists(h5_path):
                try:
                    os.unlink(h5_path)
                except PermissionError:
                    pass  # File still locked, skip cleanup


class TestAdditionalRelsPreservation:
    """Test that manually added relationships (like EXTERNAL_RESOURCE) are preserved during updates."""

    def test_external_resource_preserved_on_object_update(self, temp_epc_file, sample_objects):
        """Test that EXTERNAL_RESOURCE relationships are preserved when the object is updated."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        # Add initial object
        trset = sample_objects["trset"]
        identifier = reader.add_object(trset)

        # Add EXTERNAL_RESOURCE relationship manually
        from energyml.opc.opc import Relationship

        h5_rel = Relationship(
            target="data/test_data.h5",
            type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
            id=f"_external_{identifier}_h5",
        )
        reader.add_rels_for_object(identifier, [h5_rel], write_immediately=True)

        # Verify the HDF5 path is returned
        h5_paths_before = reader.get_h5_file_paths(identifier)
        assert "data/test_data.h5" in h5_paths_before

        # Update the object (modify its title)
        trset.citation.title = "Updated Triangulated Set"
        reader.update_object(trset)

        # Verify EXTERNAL_RESOURCE relationship is still present
        h5_paths_after = reader.get_h5_file_paths(identifier)
        assert "data/test_data.h5" in h5_paths_after, "EXTERNAL_RESOURCE relationship was lost after update"

        # Also verify by checking rels directly
        rels = reader.get_obj_rels(identifier)
        external_rels = [r for r in rels if r.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type()]
        assert len(external_rels) > 0, "EXTERNAL_RESOURCE relationship not found in rels"
        assert any("test_data.h5" in r.target for r in external_rels)

        reader.close()

    def test_external_resource_preserved_when_referenced_by_other(self, temp_epc_file, sample_objects):
        """Test that EXTERNAL_RESOURCE relationships are preserved when another object references this one."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        # Add BoundaryFeature with EXTERNAL_RESOURCE
        bf = sample_objects["bf"]
        bf_id = reader.add_object(bf)

        # Add EXTERNAL_RESOURCE relationship to BoundaryFeature
        from energyml.opc.opc import Relationship

        h5_rel = Relationship(
            target="data/boundary_data.h5",
            type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
            id=f"_external_{bf_id}_h5",
        )
        reader.add_rels_for_object(bf_id, [h5_rel], write_immediately=True)

        # Verify initial state
        h5_paths_initial = reader.get_h5_file_paths(bf_id)
        assert "data/boundary_data.h5" in h5_paths_initial

        # Add BoundaryFeatureInterpretation that references the BoundaryFeature
        # This will create DESTINATION_OBJECT relationship in bf's rels file
        bfi = sample_objects["bfi"]
        reader.add_object(bfi)

        # Verify EXTERNAL_RESOURCE is still present after adding referencing object
        h5_paths_after = reader.get_h5_file_paths(bf_id)
        assert "data/boundary_data.h5" in h5_paths_after, "EXTERNAL_RESOURCE lost after adding referencing object"

        # Verify rels directly
        rels = reader.get_obj_rels(bf_id)
        external_rels = [r for r in rels if r.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type()]
        assert len(external_rels) > 0
        assert any("boundary_data.h5" in r.target for r in external_rels)

        reader.close()

    def test_external_resource_preserved_update_on_close_mode(self, temp_epc_file, sample_objects):
        """Test EXTERNAL_RESOURCE preservation in UPDATE_ON_CLOSE mode."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE)

        # Add object
        trset = sample_objects["trset"]
        identifier = reader.add_object(trset)

        # Add EXTERNAL_RESOURCE relationship
        from energyml.opc.opc import Relationship

        h5_rel = Relationship(
            target="data/test_data.h5",
            type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
            id=f"_external_{identifier}_h5",
        )
        reader.add_rels_for_object(identifier, [h5_rel], write_immediately=True)

        # Update object
        trset.citation.title = "Modified in UPDATE_ON_CLOSE mode"
        reader.update_object(trset)

        # Close (triggers rebuild_all_rels in UPDATE_ON_CLOSE mode)
        reader.close()

        # Reopen and verify
        reader2 = EpcStreamReader(temp_epc_file)
        h5_paths = reader2.get_h5_file_paths(identifier)
        assert "data/test_data.h5" in h5_paths, "EXTERNAL_RESOURCE lost after close in UPDATE_ON_CLOSE mode"
        reader2.close()

    def test_multiple_external_resources_preserved(self, temp_epc_file, sample_objects):
        """Test that multiple EXTERNAL_RESOURCE relationships are all preserved."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        # Add object
        trset = sample_objects["trset"]
        identifier = reader.add_object(trset)

        # Add multiple EXTERNAL_RESOURCE relationships
        from energyml.opc.opc import Relationship

        h5_rels = [
            Relationship(
                target="data/geometry.h5",
                type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
                id=f"_external_{identifier}_geometry",
            ),
            Relationship(
                target="data/properties.h5",
                type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
                id=f"_external_{identifier}_properties",
            ),
            Relationship(
                target="data/metadata.h5",
                type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
                id=f"_external_{identifier}_metadata",
            ),
        ]
        reader.add_rels_for_object(identifier, h5_rels, write_immediately=True)

        # Verify all are present
        h5_paths_before = reader.get_h5_file_paths(identifier)
        assert "data/geometry.h5" in h5_paths_before
        assert "data/properties.h5" in h5_paths_before
        assert "data/metadata.h5" in h5_paths_before

        # Update object
        trset.citation.title = "Updated with Multiple H5 Files"
        reader.update_object(trset)

        # Verify all EXTERNAL_RESOURCE relationships are still present
        h5_paths_after = reader.get_h5_file_paths(identifier)
        assert "data/geometry.h5" in h5_paths_after
        assert "data/properties.h5" in h5_paths_after
        assert "data/metadata.h5" in h5_paths_after

        reader.close()

    def test_external_resource_preserved_cascade_updates(self, temp_epc_file, sample_objects):
        """Test EXTERNAL_RESOURCE preserved through cascade of object updates."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        # Create chain: bf <- bfi <- trset
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]
        trset = sample_objects["trset"]

        # Add all objects
        bf_id = reader.add_object(bf)
        bfi_id = reader.add_object(bfi)
        trset_id = reader.add_object(trset)

        # Add EXTERNAL_RESOURCE to bf (bottom of chain)
        from energyml.opc.opc import Relationship

        h5_rel = Relationship(
            target="data/bf_data.h5",
            type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
            id=f"_external_{bf_id}_h5",
        )
        reader.add_rels_for_object(bf_id, [h5_rel], write_immediately=True)

        # Verify initial state
        h5_paths = reader.get_h5_file_paths(bf_id)
        assert "data/bf_data.h5" in h5_paths

        # Update intermediate object (bfi)
        bfi.citation.title = "Modified BFI"
        reader.update_object(bfi)

        # Update top object (trset)
        trset.citation.title = "Modified TriSet"
        reader.update_object(trset)

        # Verify EXTERNAL_RESOURCE still present after cascade of updates
        h5_paths_final = reader.get_h5_file_paths(bf_id)
        assert "data/bf_data.h5" in h5_paths_final, "EXTERNAL_RESOURCE lost after cascade updates"

        reader.close()

    def test_external_resource_with_object_removal(self, temp_epc_file, sample_objects):
        """Test that EXTERNAL_RESOURCE is properly handled when referenced object is removed."""
        reader = EpcStreamReader(temp_epc_file, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

        # Create bf and bfi (bfi references bf)
        bf = sample_objects["bf"]
        bfi = sample_objects["bfi"]

        bf_id = reader.add_object(bf)
        bfi_id = reader.add_object(bfi)

        # Add EXTERNAL_RESOURCE to bfi
        from energyml.opc.opc import Relationship

        h5_rel = Relationship(
            target="data/bfi_data.h5",
            type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
            id=f"_external_{bfi_id}_h5",
        )
        reader.add_rels_for_object(bfi_id, [h5_rel], write_immediately=True)

        # Verify it exists
        h5_paths = reader.get_h5_file_paths(bfi_id)
        assert "data/bfi_data.h5" in h5_paths

        # Remove bf (which bfi references)
        reader.remove_object(bf_id)

        # Update bfi (now its reference to bf is broken, but EXTERNAL_RESOURCE should remain)
        bfi.citation.title = "Modified after BF removed"
        reader.update_object(bfi)

        # Verify EXTERNAL_RESOURCE is still there
        h5_paths_after = reader.get_h5_file_paths(bfi_id)
        assert "data/bfi_data.h5" in h5_paths_after, "EXTERNAL_RESOURCE lost after referenced object removal"

        reader.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
