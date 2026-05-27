# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Comprehensive unit tests for EpcRelsCache class functionality.

Tests cover:
1. Basic relationship computation with forward and reverse relationships
2. Incremental updates (update_cache_for_object)
3. Late-arrival scenario (object referenced before it exists)
4. Parallel vs sequential computation
5. Reverse index functionality
6. Validation (duplicates, orphaned references)
7. Object removal from cache
8. Cache stats and debugging utilities
"""

import pytest
from typing import Set

from energyml.eml.v2_0.commonv2 import Citation as Citation20, EpcExternalPartReference
from energyml.eml.v2_3.commonv2 import Citation
from energyml.resqml.v2_0_1.resqmlv2 import (
    TriangulatedSetRepresentation as TriangulatedSetRepresentation20,
    TrianglePatch as TrianglePatch20,
    PointGeometry as PointGeometry20,
)
from energyml.resqml.v2_2.resqmlv2 import (
    BoundaryFeature,
    HorizonInterpretation,
)

from energyml.utils.epc import (
    EpcRelsCache,
    EnergymlObjectCollection,
    EpcRelsCacheErrorPolicy,
    as_dor,
    EpcExportVersion,
)
from energyml.utils.epc_utils import gen_energyml_object_path, gen_energyml_object_path, relationships_equal
from energyml.utils.introspection import (
    epoch_to_date,
    epoch,
    get_obj_uri,
)
from energyml.utils.constants import EPCRelsRelationshipType


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

    # EpcExternalPartReference
    external_ref = EpcExternalPartReference(
        uuid="25773477-ffee-4cc2-867d-000000000005",
        citation=Citation20(title="An external reference", originator="Test", creation=epoch_to_date(epoch())),
    )

    # TriangulatedSetRepresentation (2.0.1) with references
    trset20 = TriangulatedSetRepresentation20(
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
        "horizon_interp": horizon_interp,
        "external_ref": external_ref,
        "trset20": trset20,
    }


class TestEpcRelsCacheBasics:
    """Test basic EpcRelsCache initialization and functionality."""

    def test_initialization_with_collection(self, sample_objects):
        """Test initializing cache with EnergymlObjectCollection."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC, EpcRelsCacheErrorPolicy.LOG)

        assert cache is not None
        assert len(collection) == 2

    def test_initialization_with_error_policy_string(self, sample_objects):
        """Test backward compatibility with string error policy."""
        collection = EnergymlObjectCollection([sample_objects["bf"]])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC, "log")

        assert cache._error_policy == EpcRelsCacheErrorPolicy.LOG

    def test_uri_from_any_with_object(self, sample_objects):
        """Test _uri_from_any with various input types."""
        collection = EnergymlObjectCollection([sample_objects["bf"]])
        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)

        bf = sample_objects["bf"]
        uri = cache._uri_from_any(bf)

        assert uri == get_obj_uri(bf)

    def test_uri_from_any_with_uri(self, sample_objects):
        """Test _uri_from_any with Uri object."""
        collection = EnergymlObjectCollection([sample_objects["bf"]])
        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)

        bf = sample_objects["bf"]
        expected_uri = get_obj_uri(bf)

        uri = cache._uri_from_any(expected_uri)

        assert uri == expected_uri


class TestRelationshipComputation:
    """Test relationship computation with forward and reverse rels."""

    def test_compute_rels_basic(self, sample_objects):
        """Test basic relationship computation."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        rels_dict = cache.compute_rels()

        assert rels_dict is not None
        assert len(rels_dict) >= 2

    def test_trset_has_destination_to_horizon(self, sample_objects):
        """Test that trset has DESTINATION_OBJECT rel to horizonInterp."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)

        # Check for DESTINATION_OBJECT relationship
        dest_rels = [r for r in trset_rels if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT)]
        assert len(dest_rels) >= 1

        # Verify target is horizon_interp
        horizon_path = gen_energyml_object_path(sample_objects["horizon_interp"], EpcExportVersion.CLASSIC)
        assert any(horizon_path in r.target for r in dest_rels)

    def test_trset_has_ml_to_external_part_proxy(self, sample_objects):
        """Test that trset has ML_TO_EXTERNAL_PART_PROXY to external_ref."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["external_ref"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)

        # Check for ML_TO_EXTERNAL_PART_PROXY relationship
        ml_to_proxy_rels = [
            r for r in trset_rels if r.type_value == str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY)
        ]
        assert len(ml_to_proxy_rels) >= 1

        # Verify target is external_ref
        external_path = gen_energyml_object_path(sample_objects["external_ref"], EpcExportVersion.CLASSIC)
        assert any(external_path in r.target for r in ml_to_proxy_rels)

    def test_external_ref_has_proxy_to_ml(self, sample_objects):
        """Test that external_ref has EXTERNAL_PART_PROXY_TO_ML to trset (reverse rel)."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["external_ref"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        external_uri = get_obj_uri(sample_objects["external_ref"])
        external_rels = cache.get_object_rels(external_uri)

        # Check for EXTERNAL_PART_PROXY_TO_ML relationship (reverse rel)
        proxy_to_ml_rels = [
            r for r in external_rels if r.type_value == str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML)
        ]
        assert len(proxy_to_ml_rels) >= 1

        # Verify target is trset20
        trset_path = gen_energyml_object_path(sample_objects["trset20"], EpcExportVersion.CLASSIC)
        assert any(trset_path in r.target for r in proxy_to_ml_rels)

    def test_horizon_has_source_from_trset(self, sample_objects):
        """Test that horizonInterp has SOURCE_OBJECT from trset (reverse rel)."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        horizon_rels = cache.get_object_rels(horizon_uri)

        # Check for SOURCE_OBJECT relationship (reverse rel from trset)
        source_rels = [r for r in horizon_rels if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)]
        assert len(source_rels) >= 1

        # Verify source is trset20
        trset_path = gen_energyml_object_path(sample_objects["trset20"], EpcExportVersion.CLASSIC)
        assert any(trset_path in r.target for r in source_rels)

    def test_compute_rels_parallel(self, sample_objects):
        """Test parallel relationship computation with detailed verification."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["external_ref"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        rels_dict = cache.compute_rels(parallel=True)

        assert rels_dict is not None
        assert len(rels_dict) >= 4

        # Verify trset relationships in detail
        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)
        assert len(trset_rels) >= 2  # At least horizon_interp and external_ref

        # Verify each relationship has correct type and target
        horizon_path = gen_energyml_object_path(sample_objects["horizon_interp"], EpcExportVersion.CLASSIC)
        external_path = gen_energyml_object_path(sample_objects["external_ref"], EpcExportVersion.CLASSIC)

        # Find DESTINATION_OBJECT rel to horizon_interp
        dest_rels = [
            r
            for r in trset_rels
            if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT) and horizon_path in r.target
        ]
        assert len(dest_rels) == 1, f"Expected 1 DESTINATION_OBJECT to horizon, found {len(dest_rels)}"

        # Find ML_TO_EXTERNAL_PART_PROXY rel to external_ref
        ml_to_proxy_rels = [
            r
            for r in trset_rels
            if r.type_value == str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY) and external_path in r.target
        ]
        assert (
            len(ml_to_proxy_rels) == 1
        ), f"Expected 1 ML_TO_EXTERNAL_PART_PROXY to external_ref, found {len(ml_to_proxy_rels)}"

        # Verify horizon_interp has SOURCE_OBJECT from trset (reverse rel)
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        horizon_rels = cache.get_object_rels(horizon_uri)

        trset_path = gen_energyml_object_path(sample_objects["trset20"], EpcExportVersion.CLASSIC)
        source_rels = [
            r
            for r in horizon_rels
            if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT) and trset_path in r.target
        ]
        assert len(source_rels) >= 1, "Expected at least 1 SOURCE_OBJECT from trset to horizon"

        # Verify external_ref has EXTERNAL_PART_PROXY_TO_ML from trset (reverse rel)
        external_uri = get_obj_uri(sample_objects["external_ref"])
        external_rels = cache.get_object_rels(external_uri)

        proxy_to_ml_rels = [
            r
            for r in external_rels
            if r.type_value == str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML) and trset_path in r.target
        ]
        assert len(proxy_to_ml_rels) >= 1, "Expected at least 1 EXTERNAL_PART_PROXY_TO_ML from trset to external_ref"

    def test_compute_rels_sequential_vs_parallel(self, sample_objects):
        """Test that sequential and parallel computation produce identical results."""
        collection1 = EnergymlObjectCollection()
        collection2 = EnergymlObjectCollection()

        for obj in [
            sample_objects["bf"],
            sample_objects["horizon_interp"],
            sample_objects["external_ref"],
            sample_objects["trset20"],
        ]:
            collection1.append(obj)
            collection2.append(obj)

        cache_seq = EpcRelsCache(collection1, EpcExportVersion.CLASSIC)
        cache_par = EpcRelsCache(collection2, EpcExportVersion.CLASSIC)

        rels_seq = cache_seq.compute_rels(parallel=False)
        rels_par = cache_par.compute_rels(parallel=True)

        # Same number of objects should have rels
        assert len(rels_seq) == len(
            rels_par
        ), f"Different number of objects with rels: seq={len(rels_seq)}, par={len(rels_par)}"

        # Verify each object has the same number of relationships
        for obj in [
            sample_objects["bf"],
            sample_objects["horizon_interp"],
            sample_objects["external_ref"],
            sample_objects["trset20"],
        ]:
            obj_uri = get_obj_uri(obj)
            seq_rels = cache_seq.get_object_rels(obj_uri)
            par_rels = cache_par.get_object_rels(obj_uri)

            assert len(seq_rels) == len(par_rels), (
                f"Object {obj_uri} has different number of rels: " f"seq={len(seq_rels)}, par={len(par_rels)}"
            )

            # Verify each relationship from parallel is present in sequential
            for par_rel in par_rels:
                # Check if this relationship exists in sequential results
                matching_rels = [seq_rel for seq_rel in seq_rels if relationships_equal(par_rel, seq_rel)]
                assert len(matching_rels) > 0, (
                    f"Relationship from parallel not found in sequential: "
                    f"target={par_rel.target}, type={par_rel.type_value}"
                )

            # Verify each relationship from sequential is present in parallel
            for seq_rel in seq_rels:
                matching_rels = [par_rel for par_rel in par_rels if relationships_equal(seq_rel, par_rel)]
                assert len(matching_rels) > 0, (
                    f"Relationship from sequential not found in parallel: "
                    f"target={seq_rel.target}, type={seq_rel.type_value}"
                )


class TestLateArrivalScenario:
    """Test the critical late-arrival scenario where object B is added after A references it."""

    def test_add_objects_out_of_order(self, sample_objects):
        """Test adding trset before horizon_interp exists, then adding horizon_interp."""
        collection = EnergymlObjectCollection()

        # Add trset FIRST (references horizon_interp which doesn't exist yet)
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # trset should have forward rel to horizon_interp
        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)
        assert len(trset_rels) >= 2  # To horizon and external_ref

        # NOW add horizon_interp and external_ref
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["external_ref"])

        # Recompute
        cache.compute_rels()

        # horizon_interp should NOW have reverse rel from trset
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        horizon_rels = cache.get_object_rels(horizon_uri)

        source_rels = [r for r in horizon_rels if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)]
        assert len(source_rels) >= 1

        # Verify reverse rel points to trset
        trset_path = gen_energyml_object_path(sample_objects["trset20"], EpcExportVersion.CLASSIC)
        assert any(trset_path in r.target for r in source_rels)

    def test_incremental_update_with_late_arrival(self, sample_objects):
        """Test update_cache_for_object with late-arriving referenced object."""
        collection = EnergymlObjectCollection()

        # Add trset first
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Add horizon_interp later
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        # Use incremental update
        cache.update_cache_for_object(sample_objects["horizon_interp"])

        # horizon_interp should have reverse rel from trset
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        horizon_rels = cache.get_object_rels(horizon_uri)

        source_rels = [r for r in horizon_rels if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)]
        assert len(source_rels) >= 1

    def test_multiple_order_scenarios(self, sample_objects):
        """Test various object addition orders all produce correct results."""
        orders = [
            ["bf", "horizon_interp", "external_ref", "trset20"],  # Normal order
            ["trset20", "external_ref", "horizon_interp", "bf"],  # Reverse order
            ["external_ref", "trset20", "bf", "horizon_interp"],  # Mixed order
        ]

        for order in orders:
            collection = EnergymlObjectCollection()

            for obj_name in order:
                collection.append(sample_objects[obj_name])

            cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
            cache.compute_rels()

            # Verify all relationships are correct regardless of order
            trset_uri = get_obj_uri(sample_objects["trset20"])
            trset_rels = cache.get_object_rels(trset_uri)
            assert len(trset_rels) >= 2

            horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
            horizon_rels = cache.get_object_rels(horizon_uri)
            source_rels = [r for r in horizon_rels if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)]
            assert len(source_rels) >= 1


class TestIncrementalUpdates:
    """Test incremental cache updates."""

    def test_update_cache_for_single_object(self, sample_objects):
        """Test updating cache for a single object."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Add new object and update incrementally
        collection.append(sample_objects["trset20"])
        cache.update_cache_for_object(sample_objects["trset20"])

        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)

        assert len(trset_rels) >= 1  # At least horizon_interp

    def test_update_propagates_reverse_rels(self, sample_objects):
        """Test that updating an object propagates reverse rels to targets."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Get initial horizon rels count
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        initial_rels = cache.get_object_rels(horizon_uri)
        initial_count = len(initial_rels)

        # Add trset and update
        collection.append(sample_objects["trset20"])
        cache.update_cache_for_object(sample_objects["trset20"])

        # horizon should now have reverse rel from trset
        updated_rels = cache.get_object_rels(horizon_uri)
        assert len(updated_rels) > initial_count

    def test_clear_cache(self, sample_objects):
        """Test clearing the cache."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Verify cache has data
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        assert len(cache.get_object_rels(horizon_uri)) > 0

        # Clear cache
        cache.clear_cache()

        # Cache should be empty
        assert len(cache.get_object_rels(horizon_uri)) == 0

    def test_recompute_cache(self, sample_objects):
        """Test recomputing the entire cache."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Add new object
        collection.append(sample_objects["trset20"])

        # Recompute entire cache
        cache.recompute_cache()

        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)
        assert len(trset_rels) >= 1


class TestReverseIndex:
    """Test reverse reference index functionality."""

    def test_reverse_index_built_during_compute(self, sample_objects):
        """Test that reverse index is built during compute_rels."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Check reverse index exists
        assert cache._reverse_index is not None
        assert len(cache._reverse_index) > 0

        # horizon_interp should be in reverse index (referenced by trset)
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        assert horizon_uri in cache._reverse_index

        # trset should be in the sources for horizon
        trset_uri = get_obj_uri(sample_objects["trset20"])
        assert trset_uri in cache._reverse_index[horizon_uri]

    def test_reverse_index_stats(self, sample_objects):
        """Test get_reverse_index_stats method."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["external_ref"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        stats = cache.get_reverse_index_stats()

        assert stats is not None
        assert "total_targets" in stats
        assert "total_references" in stats
        assert "max_references_to_single_target" in stats
        assert stats["total_targets"] > 0
        assert stats["total_references"] > 0

    def test_reverse_index_cleared(self, sample_objects):
        """Test that reverse index is cleared with cache."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        assert len(cache._reverse_index) > 0

        cache.clear_cache()

        assert len(cache._reverse_index) == 0


class TestSupplementalRels:
    """Test supplemental relationships functionality."""

    def test_add_supplemental_rels(self, sample_objects):
        """Test adding supplemental relationships."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Create and add supplemental rel
        from energyml.opc.opc import Relationship

        supplemental_rel = Relationship(target="test_target.xml", type_value="test_type", id="test_id")

        bf_uri = get_obj_uri(sample_objects["bf"])
        cache.add_supplemental_rels(sample_objects["bf"], supplemental_rel)

        # Get rels should include supplemental
        rels = cache.get_object_rels(bf_uri)
        assert any(r.target == "test_target.xml" for r in rels)

    def test_supplemental_rels_persist_across_clear(self, sample_objects):
        """Test that supplemental rels persist across clear_cache."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Add supplemental rel
        from energyml.opc.opc import Relationship

        supplemental_rel = Relationship(target="test_target.xml", type_value="test_type", id="test_id")

        cache.add_supplemental_rels(sample_objects["bf"], supplemental_rel)

        # Clear computed rels
        cache.clear_cache()

        # Supplemental should still be there
        bf_uri = get_obj_uri(sample_objects["bf"])
        rels = cache.get_object_rels(bf_uri)
        assert any(r.target == "test_target.xml" for r in rels)


class TestValidation:
    """Test validation functionality."""

    def test_validate_rels_no_issues(self, sample_objects):
        """Test validation with no issues."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        report = cache.validate_rels()

        assert report is not None
        assert "duplicates" in report
        assert "orphaned_references" in report
        assert len(report["duplicates"]) == 0

    def test_validate_detects_orphaned_references(self, sample_objects):
        """Test that validation detects orphaned references."""
        collection = EnergymlObjectCollection()
        # Only add trset (references horizon which doesn't exist)
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        report = cache.validate_rels()

        # Should detect orphaned references to horizon_interp and external_ref
        assert len(report["orphaned_references"]) > 0

    def test_clean_rels_removes_duplicates(self, sample_objects):
        """Test that clean_rels removes duplicate relationships."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)

        # Manually add duplicate rels
        bf_uri = get_obj_uri(sample_objects["bf"])
        from energyml.opc.opc import Relationship

        cache._computed_rels[bf_uri] = [
            Relationship(target="test.xml", type_value="type1", id="id1"),
            Relationship(target="test.xml", type_value="type1", id="id2"),  # Duplicate
        ]

        # Clean should remove duplicate
        cache.clean_rels(sample_objects["bf"])

        rels = cache.get_object_rels(bf_uri)
        assert len(rels) == 1


class TestObjectRemoval:
    """Test object removal from cache."""

    def test_remove_object_from_cache(self, sample_objects):
        """Test _remove_object_from_cache method."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Verify horizon has rels
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        assert len(cache.get_object_rels(horizon_uri)) > 0

        # Remove horizon from cache
        cache._remove_object_from_cache(sample_objects["horizon_interp"])

        # horizon should have no rels
        assert len(cache.get_object_rels(horizon_uri)) == 0

        # Reverse index should not have horizon
        assert horizon_uri not in cache._reverse_index

    def test_remove_cleans_reverse_index(self, sample_objects):
        """Test that removal cleans up reverse index entries."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])
        collection.append(sample_objects["trset20"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # trset should be in reverse index for horizon
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        trset_uri = get_obj_uri(sample_objects["trset20"])
        assert trset_uri in cache._reverse_index.get(horizon_uri, set())

        # Remove trset
        cache._remove_object_from_cache(sample_objects["trset20"])

        # trset should no longer be in reverse index for horizon
        if horizon_uri in cache._reverse_index:
            assert trset_uri not in cache._reverse_index[horizon_uri]


class TestErrorHandling:
    """Test error handling with different policies."""

    def test_error_policy_log(self, sample_objects):
        """Test LOG error policy (should not raise)."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC, EpcRelsCacheErrorPolicy.LOG)

        # This should not raise even with invalid input
        try:
            cache._handle_error("Test error")
            # Should not raise
        except:
            pytest.fail("LOG policy should not raise exceptions")

    def test_error_policy_raise(self, sample_objects):
        """Test RAISE error policy (should raise)."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC, EpcRelsCacheErrorPolicy.RAISE)

        # This should raise
        with pytest.raises(RuntimeError):
            cache._handle_error("Test error")

    def test_error_policy_skip(self, sample_objects):
        """Test SKIP error policy (should do nothing)."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC, EpcRelsCacheErrorPolicy.SKIP)

        # This should do nothing
        try:
            cache._handle_error("Test error")
            # Should not raise
        except:
            pytest.fail("SKIP policy should not raise exceptions")


class TestDeduplication:
    """Test relationship deduplication."""

    def test_deduplicate_rels(self, sample_objects):
        """Test _deduplicate_rels method."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)

        from energyml.opc.opc import Relationship

        rels = [
            Relationship(target="test1.xml", type_value="type1", id="id1"),
            Relationship(target="test1.xml", type_value="type1", id="id2"),  # Duplicate
            Relationship(target="test2.xml", type_value="type2", id="id3"),
        ]

        deduped = cache._deduplicate_rels(rels)

        assert len(deduped) == 2  # Only 2 unique rels

    def test_get_object_rels_returns_deduplicated(self, sample_objects):
        """Test that get_object_rels returns deduplicated results."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])
        rels = cache.get_object_rels(horizon_uri)

        # Check no duplicates
        seen = set()
        for rel in rels:
            key = (rel.target, rel.type_value)
            assert key not in seen, "Found duplicate relationship"
            seen.add(key)


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def test_full_workflow(self, sample_objects):
        """Test complete workflow: add, compute, update, validate."""
        collection = EnergymlObjectCollection()

        # Step 1: Add initial objects
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)

        # Step 2: Compute rels
        cache.compute_rels()

        # Step 3: Add more objects incrementally
        collection.append(sample_objects["external_ref"])
        cache.update_cache_for_object(sample_objects["external_ref"])

        collection.append(sample_objects["trset20"])
        cache.update_cache_for_object(sample_objects["trset20"])

        # Step 4: Validate
        report = cache.validate_rels()
        assert len(report["duplicates"]) == 0

        # Step 5: Get stats
        stats = cache.get_reverse_index_stats()
        assert stats["total_targets"] > 0

        # Step 6: Verify all relationships are correct
        trset_uri = get_obj_uri(sample_objects["trset20"])
        trset_rels = cache.get_object_rels(trset_uri)
        assert len(trset_rels) >= 2

    def test_parallel_then_incremental(self, sample_objects):
        """Test parallel compute followed by incremental updates."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])
        collection.append(sample_objects["horizon_interp"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)

        # Parallel compute
        cache.compute_rels(parallel=True)

        # Add object and update incrementally
        collection.append(sample_objects["trset20"])
        cache.update_cache_for_object(sample_objects["trset20"])

        # Verify correct
        trset_uri = get_obj_uri(sample_objects["trset20"])
        horizon_uri = get_obj_uri(sample_objects["horizon_interp"])

        trset_rels = cache.get_object_rels(trset_uri)
        horizon_rels = cache.get_object_rels(horizon_uri)

        assert len(trset_rels) >= 1
        assert len(horizon_rels) >= 1

    def test_recompute_after_many_updates(self, sample_objects):
        """Test full recompute after many incremental updates."""
        collection = EnergymlObjectCollection()
        collection.append(sample_objects["bf"])

        cache = EpcRelsCache(collection, EpcExportVersion.CLASSIC)
        cache.compute_rels()

        # Many incremental updates
        collection.append(sample_objects["horizon_interp"])
        cache.update_cache_for_object(sample_objects["horizon_interp"])

        collection.append(sample_objects["external_ref"])
        cache.update_cache_for_object(sample_objects["external_ref"])

        collection.append(sample_objects["trset20"])
        cache.update_cache_for_object(sample_objects["trset20"])

        # Full recompute
        cache.recompute_cache(parallel=False)

        # Verify still correct
        report = cache.validate_rels()
        assert len(report["duplicates"]) == 0

        stats = cache.get_reverse_index_stats()
        assert stats["total_targets"] > 0
