"""
Performance benchmarking tests for parallel rebuild_all_rels implementation.

This module compares sequential vs parallel relationship rebuilding performance
on real EPC files.
"""

import os
import time
import tempfile
import shutil
from pathlib import Path
import pytest

from energyml.utils.epc_stream_old import EpcStreamReader


# Default test file path - can be overridden via environment variable
DEFAULT_TEST_FILE = r"C:\Users\Cryptaro\Downloads\80wells_surf.epc"
TEST_EPC_PATH = os.environ.get("TEST_EPC_PATH", DEFAULT_TEST_FILE)


def create_test_copy(source_path: str) -> str:
    """Create a temporary copy of the EPC file for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "test.epc")
    shutil.copy(source_path, temp_path)
    return temp_path


@pytest.mark.slow
@pytest.mark.skipif(not os.path.exists(TEST_EPC_PATH), reason=f"Test EPC file not found: {TEST_EPC_PATH}")
class TestParallelRelsPerformance:
    """Performance comparison tests for sequential vs parallel rebuild_all_rels.

    These tests are marked as 'slow' and skipped by default.
    Run with: pytest -m slow
    """

    def test_sequential_rebuild_performance(self):
        """Benchmark sequential rebuild_all_rels implementation."""
        # Create test copy
        test_file = create_test_copy(TEST_EPC_PATH)

        try:
            # Open with sequential mode
            reader = EpcStreamReader(test_file, enable_parallel_rels=False, keep_open=True)

            # Measure rebuild time
            start_time = time.time()
            stats = reader.rebuild_all_rels(clean_first=True)
            end_time = time.time()

            execution_time = end_time - start_time

            # Verify stats
            assert stats["objects_processed"] > 0, "Should process some objects"
            assert stats["source_relationships"] > 0, "Should create SOURCE relationships"
            assert stats["rels_files_created"] > 0, "Should create .rels files"

            # Print results
            print(f"\n{'='*70}")
            print(f"SEQUENTIAL MODE PERFORMANCE")
            print(f"{'='*70}")
            print(f"Objects processed:        {stats['objects_processed']}")
            print(f"SOURCE relationships:     {stats['source_relationships']}")
            print(f"DESTINATION relationships: {stats['destination_relationships']}")
            print(f"Rels files created:       {stats['rels_files_created']}")
            print(f"Execution time:           {execution_time:.3f}s")
            print(f"Objects per second:       {stats['objects_processed']/execution_time:.2f}")
            print(f"{'='*70}\n")

            # Close reader before cleanup
            reader.close()

            # Allow time for file handles to be released
            import time as time_module

            time_module.sleep(0.5)

            # Store for comparison
            return {"mode": "sequential", "execution_time": execution_time, "stats": stats}

        finally:
            # Cleanup
            try:
                # Ensure directory is cleaned up
                temp_dir = os.path.dirname(test_file)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"Warning: Cleanup failed: {e}")

    def test_parallel_rebuild_performance(self):
        """Benchmark parallel rebuild_all_rels implementation."""
        # Create test copy
        test_file = create_test_copy(TEST_EPC_PATH)

        try:
            # Open with parallel mode
            reader = EpcStreamReader(test_file, enable_parallel_rels=True, keep_open=True)

            # Measure rebuild time
            start_time = time.time()
            stats = reader.rebuild_all_rels(clean_first=True)
            end_time = time.time()

            execution_time = end_time - start_time

            # Verify stats
            assert stats["objects_processed"] > 0, "Should process some objects"
            assert stats["source_relationships"] > 0, "Should create SOURCE relationships"
            assert stats["rels_files_created"] > 0, "Should create .rels files"
            assert stats["parallel_mode"] is True, "Should indicate parallel mode"

            # Print results
            print(f"\n{'='*70}")
            print(f"PARALLEL MODE PERFORMANCE")
            print(f"{'='*70}")
            print(f"Objects processed:        {stats['objects_processed']}")
            print(f"SOURCE relationships:     {stats['source_relationships']}")
            print(f"DESTINATION relationships: {stats['destination_relationships']}")
            print(f"Rels files created:       {stats['rels_files_created']}")
            print(f"Execution time:           {execution_time:.3f}s")
            print(f"Objects per second:       {stats['objects_processed']/execution_time:.2f}")
            print(f"{'='*70}\n")

            # Close reader before cleanup
            reader.close()

            # Allow time for file handles to be released
            import time as time_module

            time_module.sleep(0.5)

            return {"mode": "parallel", "execution_time": execution_time, "stats": stats}

        finally:
            # Cleanup
            try:
                temp_dir = os.path.dirname(test_file)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"Warning: Cleanup failed: {e}")

    def test_compare_sequential_vs_parallel(self):
        """Direct comparison of sequential vs parallel performance."""
        # Run sequential
        test_file_seq = create_test_copy(TEST_EPC_PATH)

        try:
            reader_seq = EpcStreamReader(test_file_seq, enable_parallel_rels=False, keep_open=True)
            start_seq = time.time()
            stats_seq = reader_seq.rebuild_all_rels(clean_first=True)
            time_seq = time.time() - start_seq
            reader_seq.close()
        finally:
            if os.path.exists(test_file_seq):
                os.unlink(test_file_seq)
            if os.path.exists(os.path.dirname(test_file_seq)):
                shutil.rmtree(os.path.dirname(test_file_seq))

        # Run parallel
        test_file_par = create_test_copy(TEST_EPC_PATH)

        try:
            reader_par = EpcStreamReader(test_file_par, enable_parallel_rels=True, keep_open=True)
            start_par = time.time()
            stats_par = reader_par.rebuild_all_rels(clean_first=True)
            time_par = time.time() - start_par
            reader_par.close()
        finally:
            if os.path.exists(test_file_par):
                os.unlink(test_file_par)
            if os.path.exists(os.path.dirname(test_file_par)):
                shutil.rmtree(os.path.dirname(test_file_par))

        # Verify consistency
        assert stats_seq["objects_processed"] == stats_par["objects_processed"], "Should process same number of objects"
        assert (
            stats_seq["source_relationships"] == stats_par["source_relationships"]
        ), "Should create same SOURCE relationships"
        assert (
            stats_seq["destination_relationships"] == stats_par["destination_relationships"]
        ), "Should create same DESTINATION relationships"

        # Calculate speedup
        speedup = time_seq / time_par
        speedup_percent = (time_seq - time_par) / time_seq * 100

        # Print comparison
        print(f"\n{'='*70}")
        print(f"PERFORMANCE COMPARISON")
        print(f"{'='*70}")
        print(f"Test file: {os.path.basename(TEST_EPC_PATH)}")
        print(f"Objects processed: {stats_seq['objects_processed']}")
        print(f"-" * 70)
        print(f"Sequential time:   {time_seq:.3f}s")
        print(f"Parallel time:     {time_par:.3f}s")
        print(f"-" * 70)
        print(f"Speedup:           {speedup:.2f}x")
        print(f"Time saved:        {speedup_percent:.1f}%")
        print(f"Absolute savings:  {time_seq - time_par:.3f}s")
        print(f"{'='*70}\n")

        # Assert some improvement (parallel should be faster or at least not much slower)
        # For small EPCs, overhead might make parallel slightly slower
        # For large EPCs (80+ objects), parallel should be significantly faster
        if stats_seq["objects_processed"] >= 50:
            assert (
                time_par < time_seq * 1.2
            ), f"Parallel mode should not be >20% slower for {stats_seq['objects_processed']} objects"

    def test_correctness_parallel_vs_sequential(self):
        """Verify that parallel and sequential produce identical results."""
        # Test with sequential
        test_file_seq = create_test_copy(TEST_EPC_PATH)

        try:
            reader_seq = EpcStreamReader(test_file_seq, enable_parallel_rels=False)
            stats_seq = reader_seq.rebuild_all_rels(clean_first=True)

            # Read back relationships
            rels_seq = {}
            for identifier in reader_seq._metadata:
                try:
                    obj_rels = reader_seq.get_obj_rels(identifier)
                    rels_seq[identifier] = sorted([(r.target, r.type_value) for r in obj_rels])
                except Exception:
                    rels_seq[identifier] = []

            reader_seq.close()
        finally:
            if os.path.exists(test_file_seq):
                os.unlink(test_file_seq)
            if os.path.exists(os.path.dirname(test_file_seq)):
                shutil.rmtree(os.path.dirname(test_file_seq))

        # Test with parallel
        test_file_par = create_test_copy(TEST_EPC_PATH)

        try:
            reader_par = EpcStreamReader(test_file_par, enable_parallel_rels=True)
            stats_par = reader_par.rebuild_all_rels(clean_first=True)

            # Read back relationships
            rels_par = {}
            for identifier in reader_par._metadata:
                try:
                    obj_rels = reader_par.get_obj_rels(identifier)
                    rels_par[identifier] = sorted([(r.target, r.type_value) for r in obj_rels])
                except Exception:
                    rels_par[identifier] = []

            reader_par.close()
        finally:
            if os.path.exists(test_file_par):
                os.unlink(test_file_par)
            if os.path.exists(os.path.dirname(test_file_par)):
                shutil.rmtree(os.path.dirname(test_file_par))

        # Compare results
        assert stats_seq["objects_processed"] == stats_par["objects_processed"]
        assert stats_seq["source_relationships"] == stats_par["source_relationships"]
        assert stats_seq["destination_relationships"] == stats_par["destination_relationships"]

        # Compare actual relationships (order-independent)
        assert set(rels_seq.keys()) == set(rels_par.keys()), "Should have same objects"

        for identifier in rels_seq:
            assert (
                rels_seq[identifier] == rels_par[identifier]
            ), f"Relationships for {identifier} should match between sequential and parallel modes"

        print(f"\n✓ Correctness verified: Sequential and parallel modes produce identical results")


if __name__ == "__main__":
    """Run performance tests directly."""
    import sys

    if len(sys.argv) > 1:
        TEST_EPC_PATH = sys.argv[1]

    if not os.path.exists(TEST_EPC_PATH):
        print(f"Error: Test file not found: {TEST_EPC_PATH}")
        print(f"Usage: python {__file__} [path/to/test.epc]")
        sys.exit(1)

    print(f"Running performance tests with: {TEST_EPC_PATH}\n")

    # Run tests
    test = TestParallelRelsPerformance()

    try:
        test.test_sequential_rebuild_performance()
        test.test_parallel_rebuild_performance()
        test.test_compare_sequential_vs_parallel()
        test.test_correctness_parallel_vs_sequential()

        print("\n✓ All performance tests passed!")

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
