# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import json
import sys
from pathlib import Path
import logging

import numpy as np


src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from energyml.utils.introspection import get_obj_uri
from energyml.utils.constants import EpcExportVersion
from energyml.utils.epc_stream import read_epc_stream
from energyml.utils.epc import (
    Epc,
    create_energyml_object,
    as_dor,
    create_h5_external_relationship,
    gen_energyml_object_path,
)
from energyml.utils.serialization import serialize_json


def test_epc_stream_main():
    logging.basicConfig(level=logging.DEBUG)

    from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation, ContactElement
    from energyml.eml.v2_3.commonv2 import DataObjectReference

    # Use the test EPC file
    test_epc = "wip/my_stream_file.epc"

    if Path(test_epc).exists():
        # delete this file to start fresh
        Path(test_epc).unlink()

    epc_stream = read_epc_stream(test_epc, export_version=EpcExportVersion.EXPANDED)
    print(f"EPC Stream has {len(epc_stream)} objects:")

    assert len(epc_stream) == 0
    print("✓ EPC Stream is empty as expected.")
    print(json.dumps(epc_stream.dumps_epc_content_and_files_lists(), indent=2))
    # Now we will create some objects

    trset: TriangulatedSetRepresentation = create_energyml_object("resqml22.TriangulatedSetRepresentation")
    bfi = create_energyml_object("resqml22.BoundaryFeatureInterpretation")
    bfi.object_version = "1.0"
    bf = create_energyml_object("resqml22.BoundaryFeature")

    trset.represented_object = as_dor(bfi)
    bfi.interpreted_feature = as_dor(bf)

    # print(get_dor_obj_info(trset.represented_object))
    # print(get_dor_obj_info(as_dor(bfi, "eml20.DataObjectReference")))
    print(gen_energyml_object_path(trset.represented_object))

    print("\nCreated objects:")
    print(serialize_json(trset))
    print(serialize_json(bfi))
    print(serialize_json(bf))

    print("=" * 70)

    print("=) Adding TriangulatedSetRepresentation to EPC Stream...")
    epc_stream.add_object(trset)
    print("Epc dumps after adding TriangulatedSetRepresentation:")
    print(json.dumps(epc_stream.dumps_epc_content_and_files_lists(), indent=2))

    print("=) Adding BoundaryFeatureInterpretation to EPC Stream...")
    epc_stream.add_object(bfi)
    print("Epc dumps after adding BoundaryFeatureInterpretation:")
    print(json.dumps(epc_stream.dumps_epc_content_and_files_lists(), indent=2))

    print("=) Adding BoundaryFeature to EPC Stream...")
    epc_stream.add_object(bf)
    print("Epc dumps after adding BoundaryFeature:")
    print(json.dumps(epc_stream.dumps_epc_content_and_files_lists(), indent=2))

    print("=) Removing BoundaryFeature to EPC Stream...")
    epc_stream.remove_object(get_obj_uri(bf))
    print("Epc dumps after removing BoundaryFeature:")
    print(json.dumps(epc_stream.dumps_epc_content_and_files_lists(), indent=2))

    print("=" * 70, " ARRAYS")
    print("HDF5 file paths for TriangulatedSetRepresentation (before adding external rels):")
    print(epc_stream.get_h5_file_paths(get_obj_uri(trset)))

    #  Now adding rels to external HDF5 file
    external_hdf5_path = "wip/external_data.h5"
    epc_stream.add_rels_for_object(
        trset,
        relationships=[create_h5_external_relationship(h5_path=external_hdf5_path)],
    )
    epc_stream.add_rels_for_object(
        trset,
        relationships=[create_h5_external_relationship(h5_path=external_hdf5_path + "_bis.h5")],
    )

    print(epc_stream.get_obj_rels(trset))

    print("=" * 70, " ARRAYS")
    print("HDF5 file paths for TriangulatedSetRepresentation (after adding external rels):")
    print(epc_stream.get_h5_file_paths(get_obj_uri(trset)))

    written = epc_stream.write_array(trset, "/MyDataset", array=np.arange(12).reshape((3, 4)))
    print(f"Array write successful: {written}")
    print("Reading back the written arrays:")
    array_read = epc_stream.read_array(trset, "/MyDataset")
    print(array_read)


def test_epc_im_main():
    logging.basicConfig(level=logging.DEBUG)

    from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation, ContactElement
    from energyml.eml.v2_3.commonv2 import DataObjectReference

    # Use the test EPC file
    test_epc = "wip/my_stream_file.epc"

    if Path(test_epc).exists():
        # delete this file to start fresh
        Path(test_epc).unlink()

    epc_im = Epc(epc_file_path=test_epc, export_version=EpcExportVersion.EXPANDED)
    print(f"EPC Stream has {len(epc_im)} objects:")

    assert len(epc_im) == 0
    print("✓ EPC Stream is empty as expected.")
    print(json.dumps(epc_im.dumps_epc_content_and_files_lists(), indent=2))
    # Now we will create some objects

    trset: TriangulatedSetRepresentation = create_energyml_object("resqml22.TriangulatedSetRepresentation")
    bfi = create_energyml_object("resqml22.BoundaryFeatureInterpretation")
    bfi.object_version = "1.0"
    bf = create_energyml_object("resqml22.BoundaryFeature")

    trset.represented_object = as_dor(bfi)
    bfi.interpreted_feature = as_dor(bf)

    # print(get_dor_obj_info(trset.represented_object))
    # print(get_dor_obj_info(as_dor(bfi, "eml20.DataObjectReference")))
    print(gen_energyml_object_path(trset.represented_object))

    print("\nCreated objects:")
    print(serialize_json(trset))
    print(serialize_json(bfi))
    print(serialize_json(bf))

    print("=" * 70)

    print("=) Adding TriangulatedSetRepresentation to EPC Stream...")
    epc_im.add_object(trset)
    print("Epc dumps after adding TriangulatedSetRepresentation:")
    print(json.dumps(epc_im.dumps_epc_content_and_files_lists(), indent=2))

    print("=) Adding BoundaryFeatureInterpretation to EPC Stream...")
    epc_im.add_object(bfi)
    print("Epc dumps after adding BoundaryFeatureInterpretation:")
    print(json.dumps(epc_im.dumps_epc_content_and_files_lists(), indent=2))

    print("=) Adding BoundaryFeature to EPC Stream...")
    epc_im.add_object(bf)
    print("Epc dumps after adding BoundaryFeature:")
    print(json.dumps(epc_im.dumps_epc_content_and_files_lists(), indent=2))

    print("=) Removing BoundaryFeature to EPC Stream...")
    epc_im.remove_object(get_obj_uri(bf))
    print("Epc dumps after removing BoundaryFeature:")
    print(json.dumps(epc_im.dumps_epc_content_and_files_lists(), indent=2))

    print("=" * 70, " ARRAYS")
    print("HDF5 file paths for TriangulatedSetRepresentation (before adding external rels):")
    print(epc_im.get_h5_file_paths(get_obj_uri(trset)))

    #  Now adding rels to external HDF5 file
    external_hdf5_path = "wip/external_data.h5"
    epc_im.add_rels_for_object(
        trset,
        relationships=[create_h5_external_relationship(h5_path=external_hdf5_path)],
    )
    epc_im.add_rels_for_object(
        trset,
        relationships=[create_h5_external_relationship(h5_path=external_hdf5_path + "_bis.h5")],
    )

    print(epc_im.get_obj_rels(trset))

    print("=" * 70, " ARRAYS")
    print("HDF5 file paths for TriangulatedSetRepresentation (after adding external rels):")
    print(epc_im.get_h5_file_paths(get_obj_uri(trset)))

    written = epc_im.write_array(trset, "/MyDataset", array=np.arange(12).reshape((3, 4)))
    print(f"Array write successful: {written}")
    print("Reading back the written arrays:")
    array_read = epc_im.read_array(trset, "/MyDataset")
    print(array_read)


if __name__ == "__main__":

    print("Testing EPC Stream main...")
    test_epc_stream_main()

    print("\n✓ EPC Stream main test completed.")

    print("\n" + "=" * 70)
    print("Testing in memory EPC...")
    test_epc_im_main()

    print("FIN")
