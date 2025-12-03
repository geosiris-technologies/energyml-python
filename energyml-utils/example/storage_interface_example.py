#!/usr/bin/env python
# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Example usage of the unified storage interface.

This example demonstrates how to use the EnergymlStorageInterface to work
with EPC files in both regular and streaming modes, using the same API.
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from energyml.utils.storage_interface import create_storage


def example_regular_epc():
    """Example using regular EPC storage (loads everything into memory)"""
    print("=" * 60)
    print("Example 1: Regular EPC Storage")
    print("=" * 60)

    # Create storage from file path
    with create_storage("example.epc", stream_mode=False) as storage:
        # List all objects
        print("\nListing all objects:")
        for metadata in storage.list_objects():
            print(f"  - {metadata.title} ({metadata.object_type})")
            print(f"    UUID: {metadata.uuid}")
            print(f"    URI: {metadata.uri}")

        # Get a specific object
        objects = storage.list_objects()
        if objects:
            first_obj = storage.get_object(objects[0].identifier)
            print(f"\nRetrieved object: {objects[0].title}")

            # Try to read an array
            try:
                array = storage.read_array(first_obj, "values/0")
                if array is not None:
                    print(f"  Array shape: {array.shape}")
                    print(f"  Array dtype: {array.dtype}")
            except Exception as e:
                print(f"  No array data or error: {e}")


def example_streaming_epc():
    """Example using streaming EPC storage (memory efficient for large files)"""
    print("\n" + "=" * 60)
    print("Example 2: Streaming EPC Storage (Memory Efficient)")
    print("=" * 60)

    # Create storage in streaming mode
    with create_storage("example.epc", stream_mode=True, cache_size=50) as storage:
        # List all objects (metadata loaded, objects loaded on-demand)
        print("\nListing all objects (lazy loading):")
        all_metadata = storage.list_objects()
        print(f"Total objects: {len(all_metadata)}")

        for metadata in all_metadata[:5]:  # Show first 5
            print(f"  - {metadata.title} ({metadata.object_type})")

        if len(all_metadata) > 5:
            print(f"  ... and {len(all_metadata) - 5} more")

        # Get statistics (only available in streaming mode)
        if hasattr(storage, "get_statistics"):
            stats = storage.get_statistics()
            print("\nCache statistics:")
            print(f"  Total objects: {stats['total_objects']}")
            print(f"  Loaded objects: {stats['loaded_objects']}")
            print(f"  Cache hits: {stats['cache_hits']}")
            print(f"  Cache misses: {stats['cache_misses']}")
            if stats["cache_hit_ratio"] is not None:
                print(f"  Cache hit ratio: {stats['cache_hit_ratio']:.2%}")


def example_filtering():
    """Example of filtering objects by type"""
    print("\n" + "=" * 60)
    print("Example 3: Filtering Objects by Type")
    print("=" * 60)

    with create_storage("example.epc") as storage:
        # List only specific object types
        print("\nListing Grid2dRepresentation objects:")
        grid_objects = storage.list_objects(object_type="resqml20.obj_Grid2dRepresentation")

        for metadata in grid_objects:
            print(f"  - {metadata.title}")
            print(f"    UUID: {metadata.uuid}")


def example_crud_operations():
    """Example of Create, Read, Update, Delete operations"""
    print("\n" + "=" * 60)
    print("Example 4: CRUD Operations")
    print("=" * 60)

    with create_storage("example.epc") as storage:
        # Get an object
        objects = storage.list_objects()
        if not objects:
            print("No objects in EPC file")
            return

        print(f"\nTotal objects: {len(objects)}")

        # Read
        first_metadata = objects[0]
        obj = storage.get_object(first_metadata.identifier)
        print(f"\nRead object: {first_metadata.title}")
        print(f"Object type: {type(obj).__name__}")

        # Get by UUID (may return multiple versions)
        uuid_objects = storage.get_object_by_uuid(first_metadata.uuid)
        print(f"Objects with UUID {first_metadata.uuid}: {len(uuid_objects)}")

        # Update would be: modify obj, then storage.put_object(obj)
        # Delete would be: storage.delete_object(identifier)

        # Save changes (if using EPCStorage)
        if hasattr(storage, "save"):
            # storage.save("modified_example.epc")
            print("\nChanges can be saved with storage.save()")


def example_array_operations():
    """Example of working with data arrays"""
    print("\n" + "=" * 60)
    print("Example 5: Array Operations")
    print("=" * 60)

    with create_storage("example.epc") as storage:
        objects = storage.list_objects()

        for metadata in objects:
            obj = storage.get_object(metadata.identifier)

            # Try to get array metadata
            try:
                array_meta = storage.get_array_metadata(obj, "values/0")
                if array_meta:
                    print(f"\nObject: {metadata.title}")
                    print(f"  Array path: {array_meta.path_in_resource}")
                    print(f"  Array type: {array_meta.array_type}")
                    print(f"  Dimensions: {array_meta.dimensions}")
                    print(f"  Total elements: {array_meta.size}")

                    # Read the array
                    array = storage.read_array(obj, "values/0")
                    if array is not None:
                        print(f"  Actual shape: {array.shape}")
                        print(f"  Min/Max: {array.min():.2f} / {array.max():.2f}")

                    break  # Only show first array
            except Exception:
                continue


def example_comparison():
    """Compare regular vs streaming mode"""
    print("\n" + "=" * 60)
    print("Example 6: Regular vs Streaming Comparison")
    print("=" * 60)

    import time

    file_path = "example.epc"

    # Regular mode
    start = time.time()
    with create_storage(file_path, stream_mode=False) as storage:
        metadata_list = storage.list_objects()
        regular_count = len(metadata_list)
    regular_time = time.time() - start

    # Streaming mode
    start = time.time()
    with create_storage(file_path, stream_mode=True, cache_size=10) as storage:
        metadata_list = storage.list_objects()
        stream_count = len(metadata_list)
    stream_time = time.time() - start

    print("\nRegular mode:")
    print(f"  Objects: {regular_count}")
    print(f"  Load time: {regular_time:.4f}s")

    print("\nStreaming mode:")
    print(f"  Objects: {stream_count}")
    print(f"  Load time: {stream_time:.4f}s")

    if stream_time < regular_time:
        speedup = regular_time / stream_time
        print(f"\nStreaming mode is {speedup:.2f}x faster for metadata loading!")
    else:
        print("\nRegular mode was faster (small file, overhead dominates)")


if __name__ == "__main__":
    print("Unified Storage Interface Examples")
    print("=" * 60)
    print("\nNote: These examples require an 'example.epc' file to exist.")
    print("Modify the file paths as needed for your environment.\n")

    try:
        example_regular_epc()
        example_streaming_epc()
        example_filtering()
        example_crud_operations()
        example_array_operations()
        example_comparison()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please provide a valid EPC file path.")
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback

        traceback.print_exc()
