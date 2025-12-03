#!/usr/bin/env python
# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Example demonstrating the keep_open feature of EpcStreamReader.

This example shows how using keep_open=True improves performance when
performing multiple operations on an EPC file by keeping the ZIP file
open instead of reopening it for each operation.
"""

import time
from pathlib import Path
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from energyml.utils.epc_stream import EpcStreamReader


def benchmark_without_keep_open(epc_path: str, num_operations: int = 10):
    """Benchmark reading objects without keep_open."""
    print(f"\nBenchmark WITHOUT keep_open ({num_operations} operations):")
    print("=" * 60)

    start = time.time()

    # Create reader without keep_open
    with EpcStreamReader(epc_path, keep_open=False, cache_size=5) as reader:
        metadata_list = reader.list_object_metadata()

        if not metadata_list:
            print("  No objects in EPC file")
            return 0

        # Perform multiple read operations
        for i in range(min(num_operations, len(metadata_list))):
            meta = metadata_list[i % len(metadata_list)]
            if meta.identifier:
                _ = reader.get_object_by_identifier(meta.identifier)
            if i == 0:
                print(f"  First object: {meta.object_type}")

    elapsed = time.time() - start
    print(f"  Time: {elapsed:.4f}s")
    print(f"  Avg per operation: {elapsed / num_operations:.4f}s")

    return elapsed


def benchmark_with_keep_open(epc_path: str, num_operations: int = 10):
    """Benchmark reading objects with keep_open."""
    print(f"\nBenchmark WITH keep_open ({num_operations} operations):")
    print("=" * 60)

    start = time.time()

    # Create reader with keep_open
    with EpcStreamReader(epc_path, keep_open=True, cache_size=5) as reader:
        metadata_list = reader.list_object_metadata()

        if not metadata_list:
            print("  No objects in EPC file")
            return 0

        # Perform multiple read operations
        for i in range(min(num_operations, len(metadata_list))):
            meta = metadata_list[i % len(metadata_list)]
            if meta.identifier:
                _ = reader.get_object_by_identifier(meta.identifier)
            if i == 0:
                print(f"  First object: {meta.object_type}")

    elapsed = time.time() - start
    print(f"  Time: {elapsed:.4f}s")
    print(f"  Avg per operation: {elapsed / num_operations:.4f}s")

    return elapsed


def demonstrate_file_modification_with_keep_open(epc_path: str):
    """Demonstrate that modifications work correctly with keep_open."""
    print("\nDemonstrating file modifications with keep_open:")
    print("=" * 60)

    with EpcStreamReader(epc_path, keep_open=True) as reader:
        metadata_list = reader.list_object_metadata()
        original_count = len(metadata_list)
        print(f"  Original object count: {original_count}")

        if metadata_list:
            # Get first object
            first_obj = reader.get_object_by_identifier(metadata_list[0].identifier)
            print(f"  Retrieved object: {metadata_list[0].object_type}")

            # Update the object (re-add it)
            identifier = reader.update_object(first_obj)
            print(f"  Updated object: {identifier}")

            # Verify we can still read it after update
            updated_obj = reader.get_object_by_identifier(identifier)
            assert updated_obj is not None, "Failed to read object after update"
            print("  ✓ Object successfully read after update")

            # Verify object count is the same
            new_metadata_list = reader.list_object_metadata()
            new_count = len(new_metadata_list)
            print(f"  New object count: {new_count}")

            if new_count == original_count:
                print("  ✓ Object count unchanged (correct)")
            else:
                print(f"  ✗ Object count changed: {original_count} -> {new_count}")


def demonstrate_proper_cleanup():
    """Demonstrate that persistent ZIP file is properly closed."""
    print("\nDemonstrating proper cleanup:")
    print("=" * 60)

    temp_path = "temp_test.epc"

    try:
        # Create a temporary EPC file
        reader = EpcStreamReader(temp_path, keep_open=True)
        print("  Created EpcStreamReader with keep_open=True")

        # Manually close
        reader.close()
        print("  ✓ Manually closed reader")

        # Create another reader and let it go out of scope
        reader2 = EpcStreamReader(temp_path, keep_open=True)
        print("  Created second EpcStreamReader")
        del reader2
        print("  ✓ Reader deleted (automatic cleanup via __del__)")

        # Create reader in context manager
        with EpcStreamReader(temp_path, keep_open=True) as _:
            print("  Created third EpcStreamReader in context manager")
        print("  ✓ Context manager exited (automatic cleanup)")

    finally:
        # Clean up temp file
        if Path(temp_path).exists():
            Path(temp_path).unlink()


def main():
    """Run all examples."""
    print("EpcStreamReader keep_open Feature Demonstration")
    print("=" * 60)

    # You'll need to provide a valid EPC file path
    epc_path = "wip/epc_test.epc"

    if not Path(epc_path).exists():
        print(f"\nError: EPC file not found: {epc_path}")
        print("Please provide a valid EPC file path in the script.")
        print("\nRunning cleanup demonstration only:")
        demonstrate_proper_cleanup()
        return

    try:
        # Run benchmarks
        num_ops = 20

        time_without = benchmark_without_keep_open(epc_path, num_ops)
        time_with = benchmark_with_keep_open(epc_path, num_ops)

        # Show comparison
        print("\n" + "=" * 60)
        print("Performance Comparison:")
        print("=" * 60)
        if time_with > 0 and time_without > 0:
            speedup = time_without / time_with
            improvement = ((time_without - time_with) / time_without) * 100
            print(f"  Speedup: {speedup:.2f}x")
            print(f"  Improvement: {improvement:.1f}%")

            if speedup > 1.1:
                print("\n  ✓ keep_open=True significantly improves performance!")
            elif speedup > 1.0:
                print("\n  ✓ keep_open=True slightly improves performance")
            else:
                print("\n  Note: For this workload, the difference is minimal")
                print("       (cache effects or small file)")

        # Demonstrate modifications
        demonstrate_file_modification_with_keep_open(epc_path)

        # Demonstrate cleanup
        demonstrate_proper_cleanup()

        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
