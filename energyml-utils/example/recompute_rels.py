import sys
from energyml.utils.epc import Epc
from energyml.utils.constants import EpcExportVersion



def read_compute_and_write(epc_path: str, output_path: str, export_version: EpcExportVersion = EpcExportVersion.EXPANDED) -> None:
    epc = Epc.read_file(epc_path, recompute_rels=True)
    print("EPC content and files lists before recomputing rels:")

    print("EPC content and files lists after recomputing rels:")
    epc.export_version = export_version
    print(f"Writing modified EPC to {output_path}...")
    epc.export_file(output_path)
    

if __name__ == "__main__":
    if len(sys.argv) == 3:
        epc_path = sys.argv[1]
        output_path = sys.argv[2]
    else:
        # epc_path = "rc/epc/80wells_surf.epc"
        # output_path = "rc/epc/80wells_surf_modified.epc"
        epc_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/BRGM_RESQML_PROJECT_2024/AVRE/exports_brgm/AVRE_COMPLETED_MARCH_2026.epc"
        output_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/BRGM_RESQML_PROJECT_2024/AVRE/exports_brgm/AVRE_COMPLETED_MARCH_2026.epc_modified.epc"

    read_compute_and_write(epc_path, output_path)