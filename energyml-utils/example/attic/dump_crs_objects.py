"""
Dump the raw JSON for every CRS (and Grid2D) object referenced by
``crs_info_from_epc.py``, so you can cross-check the expected values
in the integration script against what is actually stored in the EPC files.

Run from the workspace root::

    poetry run python example/attic/dump_crs_objects.py
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from energyml.utils.epc import Epc
from energyml.utils.serialization import serialize_json

logging.basicConfig(level=logging.ERROR)

_ROOT = Path(__file__).parent.parent.parent
EPC20_PATH = str(_ROOT / "rc" / "epc" / "testingPackageCpp.epc")
EPC22_PATH = str(_ROOT / "rc" / "epc" / "testingPackageCpp22.epc")

# ---------------------------------------------------------------------------
# Objects to dump
# (epc_key, uuid, label)
# ---------------------------------------------------------------------------
OBJECTS_EPC20 = [
    ("dbd637d5-4528-4145-908b-5f7136824f6d", "LocalTime3DCrs"),
    ("0ae56ef3-fc79-405b-8deb-6942e0f2e77c", "LocalDepth3DCrs"),
    ("95330cec-164c-4165-9fb9-c56477ae7f8a", "LocalEngineeringCompoundCrs (v2.0.1 EPC)"),
    ("811f8e68-c0e4-5f90-b9cf-03f7e3d53ca4", "LocalEngineering2DCrs (v2.0.1 EPC)"),
    ("1f6cf904-336c-5202-a13d-7c9b142cd406", "VerticalCrs (v2.0.1 EPC)"),
    ("030a82f6-10a7-4ecf-af03-54749e098624", "Grid2DRepresentation → LocalTime3DCrs"),
    ("aa5b90f1-2eab-4fa6-8720-69dd4fd51a4d", "Grid2DRepresentation → LocalDepth3DCrs"),
    ("4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80", "Grid2DRepresentation (v2.0.1)"),
]

OBJECTS_EPC22 = [
    ("997796f5-da9d-5175-9fb7-e592957b73fb", "LocalEngineering2DCrs (no EPSG)"),
    ("671ffdeb-f25c-513a-a4a2-1774d3ac20c6", "LocalEngineering2DCrs (EPSG 23031)"),
    ("f0e9f421-b902-4392-87d8-6495c02f2fbe", "LocalEngineeringCompoundCrs (no EPSG)"),
    ("6a18c177-93be-41ac-9084-f84bbb31f46d", "LocalEngineeringCompoundCrs (EPSG 23031)"),
    ("65cd199f-156b-5112-ad3e-b4f54a2aa77b", "VerticalCrs-A  — Direction=down → z_down=True"),
    ("355174db-6226-57ae-a5a6-92f33825fed4", "VerticalCrs-B  — Direction=down → z_down=True"),
    ("4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80", "Grid2DRepresentation (v2.2)"),
    ("1a4112fa-c4ef-4c8d-aed0-47d9273bebc5", "TriangulatedSetRepresentation (v2.2)"),
]

# ---------------------------------------------------------------------------

def _sep(title: str) -> None:
    print(f"\n{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}")


def _dump(epc: Epc, uuid: str, label: str) -> None:
    print(f"\n── {label}  [{uuid}]")
    candidates = epc.get_object_by_uuid(uuid)
    if not candidates:
        print("  *** NOT FOUND ***")
        return
    obj = candidates[0]
    print(f"  type : {type(obj).__module__}.{type(obj).__name__}")
    try:
        raw = json.loads(serialize_json(obj))
        # Pretty-print, indented 4 spaces relative to the bullet
        text = json.dumps(raw, indent=2, ensure_ascii=False)
        for line in text.splitlines():
            print(f"    {line}")
    except Exception as exc:
        print(f"  *** serialization error: {exc} ***")


def main() -> None:
    _sep(f"EPC 2.0.1 — {EPC20_PATH}")
    epc20 = Epc.read_file(EPC20_PATH)
    print(f"  Loaded {len(epc20.energyml_objects)} objects.")
    for uuid, label in OBJECTS_EPC20:
        _dump(epc20, uuid, label)

    _sep(f"EPC 2.2 — {EPC22_PATH}")
    epc22 = Epc.read_file(EPC22_PATH)
    print(f"  Loaded {len(epc22.energyml_objects)} objects.")
    for uuid, label in OBJECTS_EPC22:
        _dump(epc22, uuid, label)


if __name__ == "__main__":
    main()
