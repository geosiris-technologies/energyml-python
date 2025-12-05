# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import os
import re
import datetime
from pathlib import Path
import traceback

from energyml.utils.data.export import export_obj, export_stl, export_vtk
from energyml.utils.data.mesh import read_mesh_object
from energyml.utils.epc_stream import EpcStreamReader
from energyml.utils.exception import NotSupportedError


def export_all_representation(epc_path: str, output_dir: str, regex_type_filter: str = None):

    epc = EpcStreamReader(epc_path, keep_open=True)
    dt = datetime.datetime.now().strftime("%Hh%M_%d-%m-%Y")
    not_supported_types = set()
    for mdata in epc.list_object_metadata():
        if "Representation" in mdata.object_type and (
            regex_type_filter is None
            or len(regex_type_filter) == 0
            or re.search(regex_type_filter, mdata.object_type, flags=re.IGNORECASE)
        ):
            logging.info(f"Exporting representation: {mdata.object_type} ({mdata.uuid})")
            energyml_obj = epc.get_object_by_uuid(mdata.uuid)[0]
            try:
                mesh_list = read_mesh_object(
                    energyml_object=energyml_obj,
                    workspace=epc,
                    use_crs_displacement=True,
                )

                os.makedirs(output_dir, exist_ok=True)

                path = Path(output_dir) / f"{dt}-{mdata.object_type}{mdata.uuid}_mesh.obj"
                with path.open("wb") as f:
                    export_obj(
                        mesh_list=mesh_list,
                        out=f,
                    )
                    export_stl_path = path.with_suffix(".stl")
                    with export_stl_path.open("wb") as stl_f:
                        export_stl(
                            mesh_list=mesh_list,
                            out=stl_f,
                        )
                    export_vtk_path = path.with_suffix(".vtk")
                    with export_vtk_path.open("wb") as vtk_f:
                        export_vtk(
                            mesh_list=mesh_list,
                            out=vtk_f,
                        )

                logging.info(f"  ✓ Exported to {path.name}")
            except NotSupportedError:
                # print(f"  ✗ Not supported: {e}")
                not_supported_types.add(mdata.object_type)
            except Exception:
                traceback.print_exc()

    logging.info("Export completed.")
    if not_supported_types:
        logging.info("Not supported representation types encountered:")
        for t in not_supported_types:
            logging.info(f" - {t}")


# $env:PYTHONPATH="$(pwd)\src"; poetry run python example/main_test_3D.py
if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    # epc_file = "rc/epc/testingPackageCpp.epc"
    epc_file = "rc/epc/output-val.epc"
    # epc_file = "rc/epc/Volve_Horizons_and_Faults_Depth_originEQN.epc"
    output_directory = Path("exported_meshes") / Path(epc_file).name.replace(".epc", "_3D_export")
    # export_all_representation(epc_file, output_directory)
    # export_all_representation(epc_file, output_directory, regex_type_filter="Wellbore")
    export_all_representation(epc_file, str(output_directory), regex_type_filter="")
