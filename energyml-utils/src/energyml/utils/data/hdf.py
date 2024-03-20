# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import os
import zipfile
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, List, Tuple, Any, Union

import h5py

from src.energyml.utils.introspection import search_attribute_matching_name_with_path


@dataclass
class DatasetReader:
    def read_array(self, source: str, path_in_external_file: str) -> Optional[List[Any]]:
        return None

    def get_array_dimension(self, source: str, path_in_external_file: str) -> Optional[List[Any]]:
        return None


@dataclass
class ETPReader(DatasetReader):
    def read_array(self, obj_uri: str, path_in_external_file: str) -> Optional[List[Any]]:
        return None

    def get_array_dimension(self, source: str, path_in_external_file: str) -> Optional[List[Any]]:
        return None


@dataclass
class HDF5FileReader(DatasetReader):
    def read_array(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
        with h5py.File(source, "r") as f:
            d_group = f[path_in_external_file]
            return d_group[()].tolist()

    def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
        with h5py.File(source, "r") as f:
            return list(f[path_in_external_file].shape)

    def extract_h5_datasets(
            self, input_h5: Union[BytesIO, str], output_h5: Union[BytesIO, str], h5_datasets_paths: List[str]
    ) -> None:
        if len(h5_datasets_paths) > 0:
            with h5py.File(output_h5, "w") as f_dest:
                with h5py.File(input_h5, "r") as f_src:
                    for dataset in h5_datasets_paths:
                        f_dest.create_dataset(dataset, data=f_src[dataset])


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


def read_triangulated_set_representation(tr_set: Any):
    pass


def read_point_set_representation(point_set: Any):
    pass
