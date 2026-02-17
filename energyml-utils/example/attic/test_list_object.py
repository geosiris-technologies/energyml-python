from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from datetime import datetime


def list_epc_classical(epc_file):
    """List contents of an EPC file."""
    epc = EpcStreamReader(epc_file, rels_update_mode=RelsUpdateMode.MANUAL)

    time_start = datetime.now()
    for obj in epc.list_objects():
        print(f"Object: {obj}")
    print(len(epc.list_objects()))
    time_end = datetime.now()
    print(f"Time taken: {time_end - time_start}")


def list_epc_fast(epc_file):
    """List contents of an EPC file using fast method."""
    epc = EpcStreamReader(
        epc_file,
        rels_update_mode=RelsUpdateMode.MANUAL,
    )

    time_start = datetime.now()
    # for obj in epc.list_objects_parallel():
    # print(f"Object: {obj}")
    print(len(epc.list_objects_parallel()))
    time_end = datetime.now()
    print(f"Time taken: {time_end - time_start}")


def list_epc_seq(epc_file):
    """List contents of an EPC file using sequential method."""
    epc = EpcStreamReader(
        epc_file,
        rels_update_mode=RelsUpdateMode.MANUAL,
    )

    time_start = datetime.now()
    # for obj in epc.list_objects_seq():
    # print(f"Object: {obj}")
    print(len(epc.list_objects_seq()))
    time_end = datetime.now()
    print(f"Time taken: {time_end - time_start}")


if __name__ == "__main__":
    epc_file = "D:/Geosiris/Clients/BRGM/git/pointset-extraction/rc/output/full-local/full-local.epc"
    print("Listing EPC contents (classical method):")
    list_epc_classical(epc_file)

    # print("\nListing EPC contents (fast method):")
    # list_epc_fast(epc_file)

    # print("\nListing EPC contents (sequential method):")
    # list_epc_seq(epc_file)
