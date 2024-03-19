# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import os
import zipfile
from io import BytesIO
from typing import Optional, List, Tuple, Any

import h5py

from src.energyml.utils.introspection import search_attribute_matching_name_with_path


def write_h5(
    input_h5: str, output_h5: str, h5_datasets: list, overwrite=False
) -> None:
    if len(h5_datasets) > 0:

        if not overwrite and os.path.exists(output_h5):
            print(f"The output file '{output_h5}'allready exists")
            return

        print(f"writing: {output_h5}: Found datasets: {h5_datasets}")

        with h5py.File(output_h5, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])


def write_h5_memory(input_h5: BytesIO, h5_datasets: list) -> Optional[BytesIO]:
    result = None
    # print(h5_datasets)
    if len(h5_datasets) > 0:
        result = BytesIO()
        with h5py.File(result, "w") as f_dest:
            input_h5.seek(0)
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])
        result.seek(0)
    return result


def write_h5_memory_in_local(input_h5: str, h5_datasets: list) -> Optional[BytesIO]:
    result = None
    if len(h5_datasets) > 0:
        result = BytesIO()
        with h5py.File(result, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    try:
                        f_dest.create_dataset(dataset, data=f_src[dataset])
                    except KeyError:
                        print("unable to find data in h5 : ", dataset)

        result.seek(0)
    return result


def get_hdf_reference(obj, param) -> List[Any]:
    return [
        val
        for path, val in get_hdf_reference_with_path(obj=obj)
    ]


def get_hdf_reference_with_path(obj: any) -> List[Tuple[str, Any]]:
    return search_attribute_matching_name_with_path(
        obj,
        "(PathInHdfFile|PathInExternalFile)"
    )
