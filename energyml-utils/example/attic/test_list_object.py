from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from datetime import datetime


def list_epc_classical(epc_file):
    """List contents of an EPC file."""

    if not isinstance(epc_file, list):
        epc_file = [epc_file]

    for f in epc_file:
        print(f"Processing EPC file: {f}")
        epc = EpcStreamReader(f, rels_update_mode=RelsUpdateMode.MANUAL)

        time_start = datetime.now()
        # for obj in epc.list_objects():
        #     print(f"Object: {obj}")
        print(len(epc.list_objects(object_type="resqml22.BoundaryFeature")))

        for obj in sorted(epc.list_objects(object_type="resqml22.BoundaryFeature"), key=lambda o: o.title):
            print(f"BoundaryFeature: {obj}")
        for obj in sorted(epc.list_objects(object_type="resqml22.RockVolumeFeature"), key=lambda o: o.title):
            print(f"RockVolumeFeature: {obj}")
        time_end = datetime.now()
        print(f"Time taken: {time_end - time_start}")


# def list_epc_fast(epc_file):
#     """List contents of an EPC file using fast method."""
#     epc = EpcStreamReader(
#         epc_file,
#         rels_update_mode=RelsUpdateMode.MANUAL,
#     )

#     time_start = datetime.now()
#     # for obj in epc.list_objects_parallel():
#     # print(f"Object: {obj}")
#     print(len(epc.list_objects_parallel()))
#     time_end = datetime.now()
#     print(f"Time taken: {time_end - time_start}")


# def list_epc_seq(epc_file):
#     """List contents of an EPC file using sequential method."""
#     epc = EpcStreamReader(
#         epc_file,
#         rels_update_mode=RelsUpdateMode.MANUAL,
#     )

#     time_start = datetime.now()
#     # for obj in epc.list_objects_seq():
#     # print(f"Object: {obj}")
#     print(len(epc.list_objects_seq()))
#     time_end = datetime.now()
#     print(f"Time taken: {time_end - time_start}")


if __name__ == "__main__":
    epc_file = [
        "D:/Geosiris/Clients/BRGM/git/pointset-extraction/rc/output/full-local/full-local.epc",
        "D:/Geosiris/Clients/BRGM/git/csv-to-energyml/rc/output/full-local/result-out-local-egis-full.epc",
    ]
    # epc_file = "D:/Geosiris/Clients/BRGM/git/pointset-extraction/rc/output/full-local/full-local.epc"
    print("Listing EPC contents (classical method):")
    list_epc_classical(epc_file)

    # print("Listing EPC contents (fast method):")
    # list_epc_fast(epc_file)

    # print("Listing EPC contents (sequential method):")
    # list_epc_seq(epc_file)
