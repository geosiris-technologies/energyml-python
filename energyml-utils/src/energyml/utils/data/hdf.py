# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, List, Tuple, Any, Union

import h5py

from src.energyml.utils.epc import Epc, get_obj_identifier, ObjectNotFoundNotException, \
    EPCRelsRelationshipType
from src.energyml.utils.introspection import search_attribute_matching_name_with_path, search_attribute_matching_name, \
    get_obj_uuid, get_object_attribute


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
    return [
        val
        for path, val in get_hdf_reference_with_path(obj=obj)
    ]


def get_hdf_reference_with_path(obj: any) -> List[Tuple[str, Any]]:
    """
    See :func:`search_attribute_matching_name_with_path`. Search an attribute with type matching regex
    "(PathInHdfFile|PathInExternalFile)".

    :param obj:
    :return: [ (Dot_Path_In_Obj, value), ...]
    """
    return search_attribute_matching_name_with_path(
        obj,
        "(PathInHdfFile|PathInExternalFile)"
    )


def get_crs_obj(
        context_obj: Any,
        path_in_root: Optional[str] = None,
        root_obj: Optional[Any] = None,
        epc: Optional[Epc] = None
) -> Optional[Any]:
    """
    Search for the CRS object related to :param:`context_obj` into the :param:`epc`
    :param context_obj:
    :param path_in_root:
    :param root_obj:
    :param epc:
    :return:
    """
    crs_list = search_attribute_matching_name(context_obj, r"\.*Crs", search_in_sub_obj=True, deep_search=False)
    if crs_list is not None and len(crs_list) > 0:
        crs = epc.get_object_by_identifier(get_obj_identifier(crs_list[0]))
        if crs is None:
            crs = epc.get_object_by_uuid(get_obj_uuid(crs_list[0]))
        if crs is None:
            raise ObjectNotFoundNotException(get_obj_identifier(crs_list[0]))
        if crs is not None:
            return crs

    if context_obj != root_obj:
        upper_path = path_in_root[:path_in_root.rindex(".")]
        if len(upper_path) > 0:
            return get_crs_obj(
                context_obj=get_object_attribute(root_obj, upper_path),
                path_in_root=upper_path,
                root_obj=root_obj,
                epc=epc,
            )

    return None


def get_hdf5_path_from_external_path(
        external_path_obj: Any,
        path_in_root: Optional[str] = None,
        root_obj: Optional[Any] = None,
        epc: Optional[Epc] = None
) -> Optional[str]:
    """
    Return the hdf5 file path (Searches for "uri" attribute or in :param:`epc` rels files).
    :param external_path_obj: can be an attribute of an ExternalDataArrayPart
    :param path_in_root:
    :param root_obj:
    :param epc:
    :return:
    """
    if isinstance(external_path_obj, str):
        # external_path_obj is maybe an attribute of an ExternalDataArrayPart, now search upper in the object
        upper_path = path_in_root[:path_in_root.rindex(".")]
        return get_hdf5_path_from_external_path(
            external_path_obj=get_object_attribute(root_obj, upper_path),
            path_in_root=upper_path,
            root_obj=root_obj,
            epc=epc,
        )
    elif type(external_path_obj).__name__ == "ExternalDataArrayPart":
        epc_folder = epc.get_epc_file_folder()
        h5_uri = search_attribute_matching_name(external_path_obj, "uri")
        if h5_uri is not None and len(h5_uri) > 0:
            return f"{epc_folder}/{h5_uri[0]}"
    else:
        epc_folder = epc.get_epc_file_folder()
        hdf_proxy = search_attribute_matching_name(external_path_obj, "HdfProxy")[0]
        if hdf_proxy is not None:
            hdf_proxy_obj = epc.get_object_by_identifier(get_obj_identifier(hdf_proxy))
            if hdf_proxy_obj is not None:
                for rel in epc.additional_rels.get(get_obj_identifier(hdf_proxy_obj), []):
                    # print(f"\trel : {rel}")
                    if rel.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
                        return f"{epc_folder}/{rel.target}"
    return None
