#!/usr/bin/env python3
# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Example script demonstrating EPC validation.

This script shows how to validate EPC files and generate reports.
"""

import sys
from pathlib import Path

from energyml.utils.epc_validator import validate_epc_file


def validate_single_file(epc_path: str) -> None:
    """Validate a single EPC file and print results."""
    print(f"\n{'=' * 70}")
    print(f"Validating: {epc_path}")
    print(f"{'=' * 70}\n")

    try:
        result = validate_epc_file(epc_path, strict=True, check_relationships=True)

        print(result)

        if result.is_valid:
            print("\n✓ Validation PASSED!")
        else:
            print("\n✗ Validation FAILED!")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error during validation: {e}")
        sys.exit(1)


def validate_directory(directory: str) -> None:
    """Validate all EPC files in a directory."""
    print(f"\n{'=' * 70}")
    print(f"Validating all EPC files in: {directory}")
    print(f"{'=' * 70}\n")

    epc_files = list(Path(directory).glob("**/*.epc"))

    if not epc_files:
        print(f"No EPC files found in {directory}")
        return

    print(f"Found {len(epc_files)} EPC file(s)\n")

    results = {}
    for epc_file in epc_files:
        print(f"Validating {epc_file.name}...", end=" ")
        result = validate_epc_file(str(epc_file))

        if result.is_valid:
            print("✓ PASSED")
        else:
            print("✗ FAILED")
            for error in result.errors[:3]:  # Show first 3 errors
                print(f"    - {error}")
            if len(result.errors) > 3:
                print(f"    ... and {len(result.errors) - 3} more errors")

        results[epc_file.name] = result

    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    passed = sum(1 for r in results.values() if r.is_valid)
    failed = len(results) - passed
    print(f"Total files: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <epc_file>        # Validate a single file")
        print(f"  {sys.argv[0]} <directory>       # Validate all EPC files in directory")
        sys.exit(1)

    path = sys.argv[1]

    if Path(path).is_file():
        validate_single_file(path)
    elif Path(path).is_dir():
        validate_directory(path)
    else:
        print(f"Error: '{path}' is neither a file nor a directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
