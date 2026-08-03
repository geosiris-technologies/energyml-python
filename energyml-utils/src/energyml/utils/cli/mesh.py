# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""``extract_3d`` — export the representations of an EPC as 3-D / GIS files."""

from __future__ import annotations

import argparse
import logging
from typing import List, Optional

from energyml.utils.cli._common import parse_args
from energyml.utils.data.mesh import MeshFileFormat, export_multiple_data

logger = logging.getLogger(__name__)


def extract_representation_in_3d_file(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``extract_3d`` command."""
    formats = [e.value for e in MeshFileFormat]
    parser = argparse.ArgumentParser(
        prog="extract_3d",
        description="Export the representations of an EPC into 3-D or GIS files "
        f"(one of : {formats}), one file per representation.",
    )
    parser.add_argument("--epc", "-f", type=str, required=True, help="Epc file path")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output folder path")
    # store_true, not store_false: with store_false the flag defaulted to True, so
    # `use_crs_displacement=not args.no_crs` was False unless --no-crs was passed — the switch
    # was inverted and the export was written in local coordinates by default.
    parser.add_argument("--no-crs", action="store_true", help="Disable crs displacement")
    parser.add_argument(
        "--file-format",
        "-ff",
        type=MeshFileFormat,
        choices=list(MeshFileFormat),
        default=MeshFileFormat.OBJ,
        help=f"Type of the output files (one of : {formats}). Default is 'obj'",
    )
    parser.add_argument("--uuid", "-u", type=str, help="The uuids of representations to extract", nargs="+")
    parser.add_argument(
        "--no-wgs84",
        action="store_true",
        help="GeoJSON only : keep the coordinates in their source CRS instead of reprojecting them to WGS84",
    )
    parser.add_argument(
        "--proj-network",
        action="store_true",
        help="GeoJSON only : allow PROJ to download the geoid grids needed by the vertical datum transformation",
    )

    args = parse_args(parser, argv)

    export_multiple_data(
        epc_path=args.epc,
        uuid_list=args.uuid,
        output_folder_path=args.output,
        file_format=args.file_format,
        use_crs_displacement=not args.no_crs,
        to_wgs84=not args.no_wgs84,
        use_network=args.proj_network,
    )
    print(f"Representations of {args.epc} exported in {args.output}")


__all__ = ["extract_representation_in_3d_file"]
