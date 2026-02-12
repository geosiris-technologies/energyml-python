import os
import sys
import logging
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.eml.v2_3.commonv2 import Citation, ExternalDataArrayPart
from energyml.resqml.v2_2.resqmlv2 import (
    TriangulatedSetRepresentation,
    BoundaryFeatureInterpretation,
    BoundaryFeature,
    HorizonInterpretation,
    TrianglePatch,
    IntegerExternalArray,
    ExternalDataArray,
    PointGeometry,
    Point3DExternalArray,
)

from energyml.resqml.v2_0_1.resqmlv2 import TrianglePatch as TrianglePatchV2_0_1
from energyml.utils.introspection import epoch_to_date, epoch
from energyml.utils.epc import as_dor, gen_uuid, get_obj_identifier
from energyml.utils.constants import EPCRelsRelationshipType, MimeType

from energyml.opc.opc import Relationship
from energyml.utils.data.datasets_io import get_handler_registry
import numpy as np


CONST_H5_PATH = "external_data.h5"
CONST_CSV_PATH = "external_data.csv"
CONST_PARQUET_PATH = "external_data.parquet"
CONST_LAS_PATH = "external_data.las"
CONST_SEGY_PATH = "external_data.sgy"


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
    trset_uuid = "25773477-ffee-4cc2-867d-000000000004"
    trset = TriangulatedSetRepresentation(
        citation=Citation(
            title="Test TriangulatedSetRepresentation",
            originator="Test",
            creation=epoch_to_date(epoch()),
        ),
        uuid="25773477-ffee-4cc2-867d-000000000004",
        object_version="1.0",
        represented_object=as_dor(horizon_interp),
        triangle_patch=[
            TrianglePatch(
                node_count=3,
                triangles=IntegerExternalArray(
                    values=ExternalDataArray(
                        external_data_array_part=[
                            ExternalDataArrayPart(
                                count=[6],
                                path_in_external_file=f"/RESQML/{trset_uuid}/triangles",
                                uri=CONST_H5_PATH,
                                mime_type=str(MimeType.HDF5),
                            )
                        ]
                    )
                ),
                geometry=PointGeometry(
                    points=Point3DExternalArray(
                        coordinates=ExternalDataArray(
                            external_data_array_part=[
                                ExternalDataArrayPart(
                                    count=[9],
                                    path_in_external_file=f"/RESQML/{trset_uuid}/points",
                                    uri=CONST_CSV_PATH,
                                    mime_type=str(MimeType.CSV),
                                )
                            ]
                        )
                    ),
                ),
            )
        ],
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

    # Calculate the EPC directory for cleanup
    epc_dir = os.path.dirname(path) if os.path.dirname(path) else "."

    # Clean up old external files if they exist (to avoid stale data)
    for old_file in [
        os.path.join(epc_dir, CONST_H5_PATH),
        os.path.join(epc_dir, CONST_CSV_PATH),
        os.path.join(epc_dir, CONST_PARQUET_PATH),
        os.path.join(epc_dir, CONST_LAS_PATH),
        os.path.join(epc_dir, CONST_SEGY_PATH),
    ]:
        if os.path.exists(old_file):
            os.remove(old_file)
            logging.info(f"Cleaned up old external file: {old_file}")

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


def test_create_epc_v3_with_different_external_files(path: str):
    # Define interesting test arrays with edge cases: 2D arrays with null values, zeros, negatives, special values
    # HDF5 test array: Integer triangles with zeros and varied values (2D: 3 triangles x 3 vertices)
    h5_triangles = np.array([[0, 1, 2], [2, 3, 0], [-1, 4, 5]], dtype=np.int32)  # Including negative value and zero

    # CSV test array: 3D coordinates with NaN values (2D: 5 points x 3 coords)
    csv_points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, np.nan, 0.0],  # NaN value
            [1.0, 1.0, 0.0],
            [0.0, 1.0, np.nan],  # Another NaN
            [0.5, 0.5, -1.5],  # Negative value
        ],
        dtype=np.float32,
    )

    # Parquet test array: Normals with special float values (2D: 4 points x 3 components)
    parquet_normals = np.array(
        [
            [0.0, 0.0, 1.0],
            [np.inf, 0.0, 0.0],  # Positive infinity
            [-np.inf, 0.0, 0.0],  # Negative infinity
            [0.0, np.nan, 1.0],  # NaN value
        ],
        dtype=np.float32,
    )

    # LAS test array: Well log data with null values (2D: 10 depth points x 3 curves)
    las_well_log = np.array(
        [
            [1000.0, 75.5, 2.35],
            [1001.0, 80.2, 2.40],
            [1002.0, np.nan, 2.38],  # Missing GR value
            [1003.0, 85.1, np.nan],  # Missing RHOB value
            [1004.0, 90.0, 2.42],
            [1005.0, 0.0, 2.45],  # Zero GR (valid but unusual)
            [1006.0, 95.5, 2.50],
            [1007.0, np.nan, np.nan],  # Multiple nulls
            [1008.0, 100.0, 2.55],
            [1009.0, -10.5, 2.60],  # Negative value (calibration artifact)
        ],
        dtype=np.float32,
    )

    # SEG-Y test array: Seismic traces with various edge cases (2D: 5 traces x 8 samples)
    segy_seismic = np.array(
        [
            [0.0, 0.5, 1.0, 0.5, 0.0, -0.5, -1.0, -0.5],
            [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, -0.2, -0.4],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Silent trace (all zeros)
            [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4],
            [np.nan, 0.1, 0.2, 0.3, np.nan, 0.5, 0.6, np.nan],  # Traces with NaN (dead traces)
        ],
        dtype=np.float32,
    )

    if os.path.exists(path):
        os.remove(path)

    # Calculate the EPC directory
    epc_dir = os.path.dirname(path) if os.path.dirname(path) else "."

    # Clean up old external files if they exist (to avoid stale data)
    for old_file in [
        os.path.join(epc_dir, CONST_H5_PATH),
        os.path.join(epc_dir, CONST_CSV_PATH),
        os.path.join(epc_dir, CONST_PARQUET_PATH),
        os.path.join(epc_dir, CONST_LAS_PATH),
        os.path.join(epc_dir, CONST_SEGY_PATH),
    ]:
        if os.path.exists(old_file):
            os.remove(old_file)
            logging.info(f"Cleaned up old external file: {old_file}")

    logging.info(f"==> Creating new EPC at {path}...")
    epc = EpcStreamReader(epc_file_path=path, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION)

    data = sample_objects()

    epc.add_object(data["bf"])
    epc.add_object(data["horizon_interp"])
    tr_set_id = epc.add_object(data["trset"])

    hi_rels = epc.get_obj_rels(data["horizon_interp"])
    logging.info(f"Horizon interpretation rels: {hi_rels}")

    # ========== HDF5 Test ==========
    logging.info("\n" + "=" * 60)
    logging.info("==> Testing HDF5 format...")
    h5_file_path = "wip/notARealFile.h5"
    h5_path_in_external = f"/RESQML/{tr_set_id}/triangles"
    epc.add_rels_for_object(
        tr_set_id,
        relationships=[Relationship(type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE), target=h5_file_path)],
    )
    epc.write_array(
        proxy=tr_set_id,
        path_in_external=h5_path_in_external,
        array=h5_triangles,
        external_uri=CONST_H5_PATH,
    )
    logging.info(f"Written HDF5 array shape: {h5_triangles.shape}, dtype: {h5_triangles.dtype}")
    logging.info(f"HDF5 test array content:\n{h5_triangles}")

    # ========== CSV Test ==========
    logging.info("\n" + "=" * 60)
    logging.info("==> Testing CSV format...")
    csv_path_in_external = f"/RESQML/{tr_set_id}/points"
    epc.write_array(
        proxy=tr_set_id,
        path_in_external=csv_path_in_external,
        array=csv_points,
        external_uri=CONST_CSV_PATH,
    )
    logging.info(f"Written CSV array shape: {csv_points.shape}, dtype: {csv_points.dtype}")
    logging.info(f"CSV test array content:\n{csv_points}")

    # ========== Parquet Test ==========
    logging.info("\n" + "=" * 60)
    logging.info("==> Testing Parquet format...")
    parquet_file_path = "wip/test_data.parquet"
    parquet_path_in_external = f"/RESQML/{tr_set_id}/normals"
    epc.add_rels_for_object(
        tr_set_id,
        relationships=[
            Relationship(type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE), target=parquet_file_path)
        ],
    )
    epc.write_array(
        proxy=tr_set_id,
        path_in_external=parquet_path_in_external,
        array=parquet_normals,
        external_uri=CONST_PARQUET_PATH,
    )
    logging.info(f"Written Parquet array shape: {parquet_normals.shape}, dtype: {parquet_normals.dtype}")
    logging.info(f"Parquet test array content:\n{parquet_normals}")

    # ========== LAS Test ==========
    logging.info("\n" + "=" * 60)
    logging.info("==> Testing LAS format...")
    las_file_path = "wip/test_well_log.las"
    las_path_in_external = "DEPTH,GR,RHOB"  # LAS mnemonics
    epc.add_rels_for_object(
        tr_set_id,
        relationships=[Relationship(type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE), target=las_file_path)],
    )
    epc.write_array(
        proxy=tr_set_id,
        path_in_external=las_path_in_external,
        array=las_well_log,
        external_uri=CONST_LAS_PATH,
    )
    logging.info(f"Written LAS array shape: {las_well_log.shape}, dtype: {las_well_log.dtype}")
    logging.info(f"LAS test array content:\n{las_well_log}")

    # ========== SEG-Y Test ==========
    logging.info("\n" + "=" * 60)
    logging.info("==> Testing SEG-Y format...")
    segy_file_path = "wip/test_seismic.sgy"
    segy_path_in_external = "traces"  # SEG-Y standard path
    epc.add_rels_for_object(
        tr_set_id,
        relationships=[Relationship(type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE), target=segy_file_path)],
    )
    epc.write_array(
        proxy=tr_set_id,
        path_in_external=segy_path_in_external,
        array=segy_seismic,
        external_uri=CONST_SEGY_PATH,
    )
    logging.info(f"Written SEG-Y array shape: {segy_seismic.shape}, dtype: {segy_seismic.dtype}")
    logging.info(f"SEG-Y test array content:\n{segy_seismic}")

    logging.info("\n" + "=" * 60)
    logging.info("==> Successfully wrote data to all supported file formats:")
    logging.info(f"    - HDF5: {CONST_H5_PATH}")
    logging.info(f"    - CSV: {CONST_CSV_PATH}")
    logging.info(f"    - Parquet: {CONST_PARQUET_PATH}")
    logging.info(f"    - LAS: {CONST_LAS_PATH}")
    logging.info(f"    - SEG-Y: {CONST_SEGY_PATH}")

    # ========== Read Back and Verify ==========
    logging.info("\n" + "#" * 60)
    logging.info("### VERIFICATION: Reading back arrays and comparing ###")
    logging.info("#" * 60)

    registry = get_handler_registry()
    verification_passed = True

    # Construct full paths to external files (relative to EPC location)
    h5_full_path = os.path.join(epc_dir, CONST_H5_PATH)
    csv_full_path = os.path.join(epc_dir, CONST_CSV_PATH)
    parquet_full_path = os.path.join(epc_dir, CONST_PARQUET_PATH)
    las_full_path = os.path.join(epc_dir, CONST_LAS_PATH)
    segy_full_path = os.path.join(epc_dir, CONST_SEGY_PATH)

    logging.info(f"Reading files from EPC directory: {epc_dir}")
    logging.info(f"  - HDF5: {h5_full_path}")
    logging.info(f"  - CSV: {csv_full_path}")
    logging.info(f"  - Parquet: {parquet_full_path}")
    logging.info(f"  - LAS: {las_full_path}")
    logging.info(f"  - SEG-Y: {segy_full_path}")

    def arrays_equal(arr1, arr2, name):
        """Compare two arrays handling NaN, inf, and other special values."""
        try:
            # Check shapes first
            if arr1.shape != arr2.shape:
                logging.error(f"[{name}] Shape mismatch: {arr1.shape} != {arr2.shape}")
                # Try to reshape if total size matches
                if arr1.size == arr2.size:
                    logging.warning(f"[{name}] Arrays have same total size ({arr1.size}), attempting reshape...")
                    try:
                        arr2_reshaped = arr2.reshape(arr1.shape)
                        logging.info(f"[{name}] Reshape successful, comparing reshaped arrays...")
                        return arrays_equal(arr1, arr2_reshaped, name + " (reshaped)")
                    except Exception as reshape_err:
                        logging.error(f"[{name}] Reshape failed: {reshape_err}")
                return False

            # Check dtypes
            if arr1.dtype != arr2.dtype:
                logging.warning(
                    f"[{name}] Dtype difference: {arr1.dtype} != {arr2.dtype} (attempting comparison anyway)"
                )

            # Use numpy's array_equal which handles NaN properly with equal_nan=True
            are_equal = np.array_equal(arr1, arr2, equal_nan=True)

            if not are_equal:
                # Provide detailed difference information
                try:
                    diff_mask = ~np.isclose(arr1, arr2, equal_nan=True, rtol=1e-5, atol=1e-8)
                    n_diff = np.sum(diff_mask)

                    if n_diff == 0:
                        # Arrays are actually equal (dtype conversion issue)
                        logging.info(f"[{name}] Arrays are equal (dtype conversion handled)")
                        return True

                    logging.error(f"[{name}] Arrays differ in {n_diff} elements")
                    if n_diff < 20:  # Only show details if not too many differences
                        logging.error(
                            f"[{name}] Differences:\nExpected:\n{arr1[diff_mask]}\nActual:\n{arr2[diff_mask]}"
                        )
                except Exception as diff_err:
                    logging.error(f"[{name}] Could not compute differences: {diff_err}")
                return False

            return True
        except Exception as e:
            logging.error(f"[{name}] Comparison error: {e}")
            return False

    # --- HDF5 Verification ---
    logging.info("\n" + "=" * 60)
    logging.info("==> Verifying HDF5 format...")
    h5_handler = registry.get_handler_for_file(h5_full_path)
    if h5_handler:
        # Get metadata
        h5_metadata = h5_handler.get_array_metadata(h5_full_path, h5_path_in_external)
        logging.info(f"HDF5 Metadata: {h5_metadata}")

        # Read back
        h5_read_back = h5_handler.read_array(h5_full_path, h5_path_in_external)
        if h5_read_back is not None:
            logging.info(f"Read back HDF5 array shape: {h5_read_back.shape}, dtype: {h5_read_back.dtype}")
            logging.info(f"Read back HDF5 content:\n{h5_read_back}")

            # Verify
            if arrays_equal(h5_triangles, h5_read_back, "HDF5"):
                logging.info("✓ HDF5 verification PASSED")
            else:
                logging.error("✗ HDF5 verification FAILED")
                verification_passed = False
        else:
            logging.error("✗ HDF5 read returned None")
            verification_passed = False
    else:
        logging.error("✗ HDF5 handler not available")
        verification_passed = False

    # --- CSV Verification ---
    logging.info("\n" + "=" * 60)
    logging.info("==> Verifying CSV format...")
    csv_handler = registry.get_handler_for_file(csv_full_path)
    if csv_handler:
        # Get metadata
        csv_metadata = csv_handler.get_array_metadata(csv_full_path)
        logging.info(f"CSV Metadata: {csv_metadata}")

        # Read back
        csv_read_back = csv_handler.read_array(csv_full_path)
        if csv_read_back is not None:
            logging.info(f"Read back CSV array shape: {csv_read_back.shape}, dtype: {csv_read_back.dtype}")
            logging.info(f"Read back CSV content:\n{csv_read_back}")

            # Verify
            if arrays_equal(csv_points, csv_read_back, "CSV"):
                logging.info("✓ CSV verification PASSED")
            else:
                logging.error("✗ CSV verification FAILED")
                verification_passed = False
        else:
            logging.error("✗ CSV read returned None")
            verification_passed = False
    else:
        logging.error("✗ CSV handler not available")
        verification_passed = False

    # --- Parquet Verification ---
    logging.info("\n" + "=" * 60)
    logging.info("==> Verifying Parquet format...")
    parquet_handler = registry.get_handler_for_file(parquet_full_path)
    if parquet_handler:
        # Get metadata
        parquet_metadata = parquet_handler.get_array_metadata(parquet_full_path)
        logging.info(f"Parquet Metadata: {parquet_metadata}")

        # Read back
        parquet_read_back = parquet_handler.read_array(parquet_full_path)
        if parquet_read_back is not None:
            logging.info(f"Read back Parquet array shape: {parquet_read_back.shape}, dtype: {parquet_read_back.dtype}")
            logging.info(f"Read back Parquet content:\n{parquet_read_back}")

            # Verify
            if arrays_equal(parquet_normals, parquet_read_back, "Parquet"):
                logging.info("✓ Parquet verification PASSED")
            else:
                logging.error("✗ Parquet verification FAILED")
                verification_passed = False
        else:
            logging.error("✗ Parquet read returned None")
            verification_passed = False
    else:
        logging.error("✗ Parquet handler not available")
        verification_passed = False

    # --- LAS Verification ---
    logging.info("\n" + "=" * 60)
    logging.info("==> Verifying LAS format...")
    las_handler = registry.get_handler_for_file(las_full_path)
    if las_handler:
        # Get metadata
        las_metadata = las_handler.get_array_metadata(las_full_path)
        logging.info(f"LAS Metadata: {las_metadata}")

        # Read back
        las_read_back = las_handler.read_array(las_full_path, las_path_in_external)
        if las_read_back is not None:
            logging.info(f"Read back LAS array shape: {las_read_back.shape}, dtype: {las_read_back.dtype}")
            logging.info(f"Read back LAS content:\n{las_read_back}")

            # Verify
            if arrays_equal(las_well_log, las_read_back, "LAS"):
                logging.info("✓ LAS verification PASSED")
            else:
                logging.error("✗ LAS verification FAILED")
                verification_passed = False
        else:
            logging.error("✗ LAS read returned None")
            verification_passed = False
    else:
        logging.error("✗ LAS handler not available")
        verification_passed = False

    # --- SEG-Y Verification ---
    logging.info("\n" + "=" * 60)
    logging.info("==> Verifying SEG-Y format...")
    segy_handler = registry.get_handler_for_file(segy_full_path)
    if segy_handler:
        # Get metadata
        segy_metadata = segy_handler.get_array_metadata(segy_full_path)
        logging.info(f"SEG-Y Metadata: {segy_metadata}")

        # Read back
        segy_read_back = segy_handler.read_array(segy_full_path, segy_path_in_external)
        if segy_read_back is not None:
            logging.info(f"Read back SEG-Y array shape: {segy_read_back.shape}, dtype: {segy_read_back.dtype}")
            logging.info(f"Read back SEG-Y content:\n{segy_read_back}")

            # Verify
            if arrays_equal(segy_seismic, segy_read_back, "SEG-Y"):
                logging.info("✓ SEG-Y verification PASSED")
            else:
                logging.error("✗ SEG-Y verification FAILED")
                verification_passed = False
        else:
            logging.error("✗ SEG-Y read returned None")
            verification_passed = False
    else:
        logging.error("✗ SEG-Y handler not available")
        verification_passed = False

    # Final summary
    logging.info("\n" + "#" * 60)
    if verification_passed:
        logging.info("### ✓✓✓ ALL VERIFICATIONS PASSED ✓✓✓ ###")
    else:
        logging.error("### ✗✗✗ SOME VERIFICATIONS FAILED ✗✗✗ ###")
    logging.info("#" * 60)

    # Close and verify
    epc.close()
    logging.info("==> EPC file closed successfully")


def recompute_rels(path: str):
    EpcStreamReader(epc_file_path=path, enable_parallel_rels=True, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # main((sys.argv[1] if len(sys.argv) > 1 else None) or "wip/80wells_surf.epc")

    # test_create_epc("wip/test_create.epc")
    # test_create_epc_v2("wip/test_create.epc")
    # test_create_epc_v3_with_different_external_files("wip/test_create_v3.epc")

    recompute_rels(sys.argv[1] if len(sys.argv) > 1 else "wip/failingData/fix/S-PASS-1-EARTHMODEL_ONLY.epc")
    recompute_rels(sys.argv[1] if len(sys.argv) > 1 else "wip/failingData/fix/S-PASS-1-GEOMODEL.epc")
