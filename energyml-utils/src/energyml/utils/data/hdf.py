# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, List, Tuple, Any, Union

import h5py

from ..introspection import (
    search_attribute_matching_name_with_path,
)


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
        self,
        input_h5: Union[BytesIO, str],
        output_h5: Union[BytesIO, str],
        h5_datasets_paths: List[str],
    ) -> None:
        """
        Copy all dataset from :param input_h5 matching with paths in :param h5_datasets_paths into the :param output
        :param input_h5:
        :param output_h5:
        :param h5_datasets_paths:
        :return:
        """
        if len(h5_datasets_paths) > 0:
            with h5py.File(output_h5, "w") as f_dest:
                with h5py.File(input_h5, "r") as f_src:
                    for dataset in h5_datasets_paths:
                        f_dest.create_dataset(dataset, data=f_src[dataset])


def get_hdf_reference(obj) -> List[Any]:
    """
    See :func:`get_hdf_reference_with_path`. Only the value is returned, not the dot path into the object
    :param obj:
    :return:
    """
    return [val for path, val in get_hdf_reference_with_path(obj=obj)]


def get_hdf_reference_with_path(obj: any) -> List[Tuple[str, Any]]:
    """
    See :func:`search_attribute_matching_name_with_path`. Search an attribute with type matching regex
    "(PathInHdfFile|PathInExternalFile)".

    :param obj:
    :return: [ (Dot_Path_In_Obj, value), ...]
    """
    return search_attribute_matching_name_with_path(obj, "(PathInHdfFile|PathInExternalFile)")
