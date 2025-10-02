#!/usr/bin/env python3
import sys
import os

print("=== ENVIRONMENT DIAGNOSTICS ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"PYTHONPATH environment variable: {os.environ.get('PYTHONPATH', 'Not set')}")

print("\n=== PYTHON PATH ===")
for i, p in enumerate(sys.path):
    print(f"  {i}: {p}")

print("\n=== IMPORT TEST ===")
try:
    import energyml.utils

    print("✓ energyml.utils imported successfully")
    print(f"  Module path: {energyml.utils.__file__ if hasattr(energyml.utils, '__file__') else 'No __file__ attr'}")
    print(f"  Module path list: {getattr(energyml.utils, '__path__', 'No __path__ attr')}")
except ImportError as e:
    print(f"✗ Failed to import energyml.utils: {e}")

# Check if src directory exists in Python path
src_path = os.path.join(os.getcwd(), "src")
print(f"\n=== SRC DIRECTORY CHECK ===")
print(f"Expected src path: {src_path}")
print(f"Src path exists: {os.path.exists(src_path)}")
print(f"Src path in sys.path: {src_path in sys.path}")

# Check what's in the src directory
if os.path.exists(src_path):
    print(f"Contents of src: {os.listdir(src_path)}")
    energyml_path = os.path.join(src_path, "energyml")
    if os.path.exists(energyml_path):
        print(f"Contents of src/energyml: {os.listdir(energyml_path)}")
