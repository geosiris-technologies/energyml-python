# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Example: export NumpyMultiMesh objects from an EPC file to all supported formats.

Demonstrates:
 - Reading meshes via read_numpy_mesh_object (NumpyMultiMesh)
 - Building RepresentationContext per object for colour metadata
 - Exporting to OBJ (+.mtl), GeoJSON, VTK Legacy ASCII, VTK Legacy Binary,
   VTK XML UnstructuredGrid (.vtu), VTK XML PolyData (.vtp), STL
 - Two passes: with and without CRS displacement

Usage::

    # from the workspace root
    poetry run python example/main_test_numpy_export.py <path/to/file.epc> <output_dir>

    # defaults (uses bundled test EPC files when no args are given)
    poetry run python example/main_test_numpy_export.py
"""

import datetime
import logging
import os
import re
import sys
import traceback
from pathlib import Path
from typing import Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy import guards — pyvista is strictly optional
# ---------------------------------------------------------------------------
try:
    from energyml.utils.data.mesh_numpy import read_numpy_mesh_object
    from energyml.utils.data.representation_context import RepresentationContext
    from energyml.utils.data.export import (
        ExportFormat,
        VTKExportOptions,
        VTKFormat,
        STLExportOptions,
        GeoJSONExportOptions,
        export_mesh,
    )
    from energyml.utils.epc_stream import EpcStreamReader
    from energyml.utils.epc import Epc
    from energyml.utils.exception import NotSupportedError
    from energyml.utils.introspection import get_obj_uuid
except ImportError as exc:
    log.error("Could not import energyml-utils modules: %s", exc)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Core export routine
# ---------------------------------------------------------------------------


def export_all_numpy(
    epc_path: str,
    output_dir: str,
    regex_type_filter: Optional[str] = None,
    use_crs_displacement: bool = True,
) -> None:
    """Read every Representation in *epc_path* via the numpy pipeline and
    export it to all supported formats.

    :param epc_path: Path to the ``.epc`` file.
    :param output_dir: Directory where output files are written (created if absent).
    :param regex_type_filter: Optional regex; only objects whose type name matches
        are exported (case-insensitive).
    :param use_crs_displacement: When True, CRS origin/axis offsets are applied to
        the exported coordinates.  Two passes are run by the top-level script: one
        with True and one with False.
    """
    tag = "crs" if use_crs_displacement else "nocrs"
    # storage = EpcStreamReader(epc_path, keep_open=True)
    storage = Epc.read_file(epc_path)
    dt = datetime.datetime.now().strftime("%Hh%M_%d-%m-%Y")

    not_supported_types: set = set()
    exported_count = 0

    for mdata in storage.list_objects():
        if "Representation" not in mdata.object_type:
            continue
        if regex_type_filter and not re.search(regex_type_filter, mdata.object_type, flags=re.IGNORECASE):
            continue

        log.info("Processing %s  (%s)", mdata.object_type, mdata.uuid)
        energyml_obj = storage.get_object_by_uuid(mdata.uuid)[0]

        try:
            # ---- 1. Read as NumpyMultiMesh --------------------------------
            multi_mesh = read_numpy_mesh_object(
                energyml_object=energyml_obj,
                workspace=storage,
                # Read with displacement=False so the exporter controls it.
                use_crs_displacement=False,
            )

            if multi_mesh is None or multi_mesh.patch_count() == 0:
                log.info("  → no patches, skipping.")
                continue

            # ---- 2. Build RepresentationContext for colour metadata --------
            ctx = RepresentationContext(energyml_obj, storage)
            source_uuid = get_obj_uuid(energyml_obj)
            contexts: Dict[str, RepresentationContext] = {source_uuid: ctx}

            # Also index children by their source_uuid for colour lookup
            for patch in multi_mesh.flat_patches():
                patch_uuid = patch.source_uuid
                if patch_uuid and patch_uuid not in contexts:
                    patch_obj = storage.get_object_by_uuid(patch_uuid)
                    if patch_obj:
                        contexts[patch_uuid] = RepresentationContext(patch_obj[0], storage)

            # ---- 3. Prepare output directory / base filename ---------------
            os.makedirs(output_dir, exist_ok=True)
            stem = f"{dt}-{mdata.object_type}_{mdata.uuid}_{tag}"
            base = Path(output_dir) / stem

            # ---- 4. Export to every format ---------------------------------
            formats_to_export = [
                (f"{base}.obj", ExportFormat.OBJ, None),
                (f"{base}.geojson", ExportFormat.GEOJSON, GeoJSONExportOptions(indent=None)),
                (f"{base}.vtk", ExportFormat.VTK, VTKExportOptions(vtk_format=VTKFormat.LEGACY_ASCII)),
                (f"{base}_binary.vtk", ExportFormat.VTK, VTKExportOptions(vtk_format=VTKFormat.LEGACY_BINARY)),
                (f"{base}.vtu", ExportFormat.VTU, VTKExportOptions(vtk_format=VTKFormat.VTU)),
                (f"{base}.vtp", ExportFormat.VTP, VTKExportOptions(vtk_format=VTKFormat.VTP)),
                (f"{base}_binary.stl", ExportFormat.STL, STLExportOptions(binary=True)),
                (f"{base}_ascii.stl", ExportFormat.STL, STLExportOptions(binary=False)),
            ]

            for path_str, fmt, opts in formats_to_export:
                try:
                    export_mesh(
                        mesh_list=multi_mesh,
                        output_path=path_str,
                        format=fmt,
                        options=opts,
                        contexts=contexts,
                        use_crs_displacement=use_crs_displacement,
                    )
                    log.info("  ✓ %s", Path(path_str).name)
                except Exception:  # noqa: BLE001
                    log.warning("  ✗ %s — export failed:", Path(path_str).name)
                    traceback.print_exc()

            exported_count += 1

        except NotSupportedError as e:
            not_supported_types.add(mdata.object_type)
            log.debug("  Not supported: %s", e)
        except Exception:
            traceback.print_exc()

    log.info("")
    log.info("Done.  Exported %d objects -> %s", exported_count, output_dir)
    if not_supported_types:
        log.info("Unsupported representation types skipped:")
        for t in sorted(not_supported_types):
            log.info("  - %s", t)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Allow: main_test_numpy_export.py [epc_path] [output_dir]
    args = sys.argv[1:]

    if len(args) >= 1:
        epc_file = args[0]
    else:
        # Fall back to the bundled test EPC in the workspace
        candidates = [
            "rc/epc/testingPackageCpp22.epc",
            "rc/epc/testingPackageCpp.epc",
        ]
        epc_file = next((p for p in candidates if Path(p).exists()), None)
        if epc_file is None:
            log.error(
                "No EPC file found.  Pass a path as the first argument or place a "
                ".epc file at rc/epc/testingPackageCpp22.epc"
            )
            sys.exit(1)

    base_output = args[1] if len(args) >= 2 else "exported_meshes/numpy_export"

    log.info("=" * 60)
    log.info("EPC  : %s", epc_file)
    log.info("OUT  : %s", base_output)
    log.info("=" * 60)

    # Pass 1 — with CRS displacement
    log.info("\n--- Pass 1: use_crs_displacement=True ---\n")
    export_all_numpy(
        epc_path=epc_file,
        output_dir=f"{base_output}/with_crs",
        use_crs_displacement=True,
    )

    # Pass 2 — raw coordinates (no CRS displacement)
    log.info("\n--- Pass 2: use_crs_displacement=False ---\n")
    export_all_numpy(
        epc_path=epc_file,
        output_dir=f"{base_output}/no_crs",
        use_crs_displacement=False,
    )
