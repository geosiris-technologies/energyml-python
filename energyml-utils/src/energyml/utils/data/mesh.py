# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass, field
from io import BytesIO
from typing import List, Optional, Any

_FILE_HEADER: bytes = b"# file exported by energyml-utils python module (Geosiris)\n"


@dataclass
class AbstractMesh:
    energyml_object: Any = field(
        default=None
    )

    crs_object: Any = field(
        default=None
    )


def export_off(off_file: BytesIO, points: List[List[float]], indices: List[List[int]], colors: Optional[List[List[int]]] = None) -> BytesIO:
    nb_edges = sum(list(map(lambda x: len(x), indices)))

    off_file.write(b"OFF\n")
    off_file.write(_FILE_HEADER)
    off_file.write(f"{len(points)} {len(indices)} {nb_edges}\n".encode('utf-8'))

    for p in points:
        for pi in p:
            off_file.write(f"{pi} ".encode('utf-8'))
        off_file.write(b"\n")

    cpt = 0
    for face in indices:
        if len(face) > 1:
            off_file.write(f"{len(face)} ".encode('utf-8'))
            for pi in face:
                off_file.write(f"{pi} ".encode('utf-8'))

            if colors is not None and len(colors) > cpt and colors[cpt] is not None and len(colors[cpt]) > 0:
                for col in colors[cpt]:
                    off_file.write(f"{col} ".encode('utf-8'))

            off_file.write(b"\n")
    return off_file
