"""
Example: Managing .rels files in EPC files using EpcStreamReader

This example demonstrates the new .rels management capabilities:
1. Removing objects without breaking .rels files
2. Cleaning orphaned relationships
3. Rebuilding all .rels files from scratch
"""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from energyml.utils.epc_stream import EpcStreamReader


def example_workflow(epc_path: str):
    """
    Complete workflow example for .rels management.
    """
    print(f"Opening EPC file: {epc_path}")
    reader = EpcStreamReader(epc_path)
    print(f"Loaded {len(reader)} objects\n")

    # ============================================================
    # Scenario 1: Remove objects without breaking .rels
    # ============================================================
    print("=" * 70)
    print("SCENARIO 1: Remove objects (keeps .rels intact)")
    print("=" * 70)

    # Get some objects to remove
    objects_to_remove = list(reader._metadata.keys())[-3:]
    print(f"\nRemoving {len(objects_to_remove)} objects:")

    for obj_id in objects_to_remove:
        print(f"  - {obj_id}")
        reader.remove_object(obj_id)

    print(f"\nRemaining objects: {len(reader)}")
    print("Note: .rels files still reference removed objects (orphaned relationships)")

    # ============================================================
    # Scenario 2: Clean orphaned relationships
    # ============================================================
    print("\n" + "=" * 70)
    print("SCENARIO 2: Clean orphaned relationships")
    print("=" * 70)

    print("\nCalling clean_rels()...")
    clean_stats = reader.clean_rels()

    print("\nCleaning statistics:")
    print(f"  • .rels files scanned: {clean_stats['rels_files_scanned']}")
    print(f"  • Orphaned relationships removed: {clean_stats['relationships_removed']}")
    print(f"  • Empty .rels files deleted: {clean_stats['rels_files_removed']}")

    print("\n✓ Orphaned relationships cleaned!")

    # ============================================================
    # Scenario 3: Rebuild all .rels from scratch
    # ============================================================
    print("\n" + "=" * 70)
    print("SCENARIO 3: Rebuild all .rels from scratch")
    print("=" * 70)

    print("\nCalling rebuild_all_rels()...")
    rebuild_stats = reader.rebuild_all_rels(clean_first=True)

    print("\nRebuild statistics:")
    print(f"  • Objects processed: {rebuild_stats['objects_processed']}")
    print(f"  • .rels files created: {rebuild_stats['rels_files_created']}")
    print(f"  • SOURCE relationships: {rebuild_stats['source_relationships']}")
    print(f"  • DESTINATION relationships: {rebuild_stats['destination_relationships']}")
    print(
        f"  • Total relationships: {rebuild_stats['source_relationships'] + rebuild_stats['destination_relationships']}"
    )

    print("\n✓ All .rels files rebuilt!")

    # ============================================================
    # Best Practices
    # ============================================================
    print("\n" + "=" * 70)
    print("BEST PRACTICES")
    print("=" * 70)

    print(
        """
    1. After removing multiple objects:
       → Call clean_rels() to remove orphaned relationships
       
    2. After modifying many objects or complex operations:
       → Call rebuild_all_rels() to ensure consistency
       
    3. Regular maintenance:
       → Periodically call clean_rels() to keep .rels files tidy
       
    4. When in doubt:
       → Use rebuild_all_rels() to guarantee correct relationships
    """
    )


def quick_clean_example(epc_path: str):
    """
    Quick example: Just clean the .rels files.
    """
    print("\n" + "=" * 70)
    print("QUICK EXAMPLE: Clean .rels in one line")
    print("=" * 70)

    reader = EpcStreamReader(epc_path)
    stats = reader.clean_rels()

    print(f"\n✓ Cleaned! Removed {stats['relationships_removed']} orphaned relationships")


def quick_rebuild_example(epc_path: str):
    """
    Quick example: Rebuild all .rels files.
    """
    print("\n" + "=" * 70)
    print("QUICK EXAMPLE: Rebuild all .rels in one line")
    print("=" * 70)

    reader = EpcStreamReader(epc_path)
    stats = reader.rebuild_all_rels()

    print(
        f"\n✓ Rebuilt! Created {stats['rels_files_created']} .rels files with {stats['source_relationships'] + stats['destination_relationships']} relationships"
    )


if __name__ == "__main__":
    # Use the test EPC file
    test_epc = "wip/BRGM_AVRE_all_march_25.epc"

    if not Path(test_epc).exists():
        print(f"EPC file not found: {test_epc}")
        print("Please provide a valid EPC file path")
        sys.exit(1)

    # Make a temporary copy for the example
    import tempfile
    import shutil

    with tempfile.NamedTemporaryFile(delete=False, suffix=".epc") as tmp:
        tmp_path = tmp.name

    try:
        shutil.copy(test_epc, tmp_path)

        # Run the complete workflow
        example_workflow(tmp_path)

        # Show quick examples
        shutil.copy(test_epc, tmp_path)
        quick_clean_example(tmp_path)

        shutil.copy(test_epc, tmp_path)
        quick_rebuild_example(tmp_path)

        print("\n" + "=" * 70)
        print("Examples completed successfully!")
        print("=" * 70)

    finally:
        # Cleanup
        if Path(tmp_path).exists():
            Path(tmp_path).unlink()
