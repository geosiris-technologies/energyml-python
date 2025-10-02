#!/usr/bin/env python3
import sys

print("Python executable:", sys.executable)
print("Python path:")
for p in sys.path:
    print(f"  {p}")

try:
    import energyml.utils

    print("✓ energyml.utils imported successfully")
except ImportError as e:
    print(f"✗ Failed to import energyml.utils: {e}")

try:
    from energyml.utils.validation import validate_epc

    print("✓ validate_epc imported successfully")
except ImportError as e:
    print(f"✗ Failed to import validate_epc: {e}")
