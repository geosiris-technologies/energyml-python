import os
import sys
import logging
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.eml.v2_3.commonv2 import Citation
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    BoundaryFeatureInterpretation,
    BoundaryFeature,
    HorizonInterpretation,
)
from energyml.utils.introspection import epoch_to_date, epoch
from energyml.utils.epc import as_dor, gen_uuid, get_obj_identifier
from energyml.utils.constants import EPCRelsRelationshipType


def sample_objects():
    """Create sample EnergyML objects for testing."""
    # Create a BoundaryFeature
    bf = BoundaryFeature(
        citation=Citation(
            title="Test Boundary Feature",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000001",
        object_version="1.0",
    )

    # Create a BoundaryFeatureInterpretation
    bfi = BoundaryFeatureInterpretation(
        citation=Citation(
            title="Test Boundary Feature Interpretation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000002",
        object_version="1.0",
        interpreted_feature=as_dor(bf),
    )

    # Create a HorizonInterpretation (independent object)
    horizon_interp = HorizonInterpretation(
        citation=Citation(
            title="Test HorizonInterpretation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        interpreted_feature=as_dor(bf),
        uuid="25773477-ffee-4cc2-867d-000000000003",
        object_version="1.0",
        domain="depth",
    )

    # Create a TriangulatedSetRepresentation
    trset = TriangulatedSetRepresentation(
        citation=Citation(
            title="Test TriangulatedSetRepresentation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000004",
        object_version="1.0",
        represented_object=as_dor(horizon_interp),
    )

    return {
        "bf": bf,
        "bfi": bfi,
        "trset": trset,
        "horizon_interp": horizon_interp,
    }


def main(epc_file_path: str):
    epc = EpcStreamReader(
        epc_file_path=epc_file_path, enable_parallel_rels=True, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION
    )

    # logging.info(epc.get_statistics())

    for obj in epc.list_objects():
        logging.info(f"Object: {obj}")


def test_create_epc(path: str):
    # delete file if exists
    if os.path.exists(path):
        os.remove(path)
    logging.info(f"==> Creating new EPC at {path}...")
    epc = EpcStreamReader(epc_file_path=path, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

    data = sample_objects()

    logging.info("==> Creating sample objects and adding to EPC...")

    logging.info("==> Adding horizon interpretation")
    epc.add_object(data["horizon_interp"])
    logging.info(f"horizon rels : {epc.get_obj_rels(data['horizon_interp'])}")

    logging.info("==> Adding boundary feature")
    epc.add_object(data["bf"])
    logging.info(f"boundary feature rels : {epc.get_obj_rels(data['bf'])}")

    logging.info("==> Adding boundary feature interpretation")
    epc.add_object(data["bfi"])
    logging.info("==> Adding triangulated set representation")
    epc.add_object(data["trset"])

    # Debug: Print all metadata identifiers
    logging.info(f"==> All metadata identifiers: {list(epc._metadata_mgr._metadata.keys())}")

    logging.info("==> All objects added. Closing EPC to write to disk.")

    horizon_id = get_obj_identifier(data["horizon_interp"])
    logging.info(f"==> Horizon identifier: {horizon_id}")
    logging.info(f"==> Horizon in metadata: {horizon_id in epc._metadata_mgr._metadata}")

    # Debug: Test _id_from_uri_or_identifier
    resolved_id = epc._id_from_uri_or_identifier(data["horizon_interp"])
    logging.info(f"==> Resolved ID from object: {resolved_id}")
    logging.info(
        f"==> Resolved ID in metadata: {resolved_id in epc._metadata_mgr._metadata if resolved_id else 'ID is None'}"
    )

    horizon_rels = epc.get_obj_rels(data["horizon_interp"])
    assert (
        len(horizon_rels) == 2
    ), f"Expected 2 relationships in horizon rels since both bfi and trset should refer to horizon as interpreted feature {horizon_rels}"
    epc.close()

    epc_reopen = EpcStreamReader(epc_file_path=path, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

    horizon_rels = epc_reopen.get_obj_rels(data["horizon_interp"])
    assert (
        len(horizon_rels) == 2
    ), f"Expected 2 relationships in horizon rels since both bfi and trset should refer to horizon as interpreted feature {horizon_rels}"

    logging.info("==> Reopened EPC, listing objects:")
    for obj in epc_reopen.list_objects():
        logging.info(f"Object: {obj}")
        obj_rels = epc_reopen.get_obj_rels(obj)
        logging.info(f"\tObject rels: {obj_rels}")
        dest_rels = [r for r in obj_rels if r.type_value == str(EPCRelsRelationshipType.DESTINATION_OBJECT)]
        logging.info(f"\tObject DESTINATION rels: {dest_rels}")

    # remove trset to check if horizon has no more source rels
    epc_reopen.remove_object(data["trset"])

    horizon_rels_after_removal = epc_reopen.get_obj_rels(data["horizon_interp"])
    logging.info(f"Horizon interpretation rels after removing trset: {horizon_rels_after_removal}")
    source_rels_after_removal = [
        r for r in horizon_rels_after_removal if r.type_value == str(EPCRelsRelationshipType.SOURCE_OBJECT)
    ]
    logging.info(f"Horizon interpretation SOURCE rels after removing trset: {source_rels_after_removal}")
    assert (
        len(source_rels_after_removal) == 0
    ), "Expected no SOURCE relationships in horizon rels after removing trset since trset was the only destination referring to horizon"

    assert (
        len(horizon_rels_after_removal) == 1
    ), "Expected 1 relationship in horizon rels after removing trset since bfi should still refer to horizon as interpreted feature"

    epc_reopen.close()


def test_create_epc_v2(path: str):

    if os.path.exists(path):
        os.remove(path)
    logging.info(f"==> Creating new EPC at {path}...")
    epc = EpcStreamReader(epc_file_path=path, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

    data = sample_objects()

    epc.add_object(data["bf"])
    # epc.add_object(data["bfi"])
    epc.add_object(data["horizon_interp"])
    epc.add_object(data["trset"])

    hi_rels = epc.get_obj_rels(data["horizon_interp"])

    logging.info(f"Horizon interpretation rels: {hi_rels}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # main((sys.argv[1] if len(sys.argv) > 1 else None) or "wip/80wells_surf.epc")

    # test_create_epc("wip/test_create.epc")
    test_create_epc_v2("wip/test_create.epc")
