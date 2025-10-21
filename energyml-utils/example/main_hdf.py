# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from energyml.utils.data.datasets_io import get_path_in_external_with_path
from energyml.utils.introspection import get_obj_uri


if __name__ == "__main__":
    from energyml.utils.epc import Epc

    # Create an EPC file
    epc = Epc.read_file("wip/BRGM_AVRE_all_march_25.epc")

    print("\n".join(map(lambda o: str(get_obj_uri(o)), epc.energyml_objects)))

    print(epc.get_h5_file_paths("eml:///resqml22.PolylineSetRepresentation(e75db94d-a251-4f31-8a24-23b9573fbf39)"))

    print(
        get_path_in_external_with_path(
            epc.get_object_by_identifier(
                "eml:///resqml22.PolylineSetRepresentation(e75db94d-a251-4f31-8a24-23b9573fbf39)"
            )
        )
    )

    print(
        epc.read_h5_dataset(
            "eml:///resqml22.PolylineSetRepresentation(e75db94d-a251-4f31-8a24-23b9573fbf39)",
            "/RESQML/e75db94d-a251-4f31-8a24-23b9573fbf39/points_patch0",
        )
    )
