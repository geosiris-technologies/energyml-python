# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import logging
import os
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, List, Tuple, Any, Union

import h5py

from ..epc import Epc, get_obj_identifier, EPCRelsRelationshipType
from ..introspection import (
    search_attribute_matching_name_with_path,
    search_attribute_matching_name,
    get_object_attribute,
    get_object_attribute_no_verif,
)


@dataclass
class DatasetReader:
    def read_array(
        self, source: str, path_in_external_file: str
    ) -> Optional[List[Any]]:
        return None

    def get_array_dimension(
        self, source: str, path_in_external_file: str
    ) -> Optional[List[Any]]:
        return None


@dataclass
class ETPReader(DatasetReader):
    def read_array(
        self, obj_uri: str, path_in_external_file: str
    ) -> Optional[List[Any]]:
        return None

    def get_array_dimension(
        self, source: str, path_in_external_file: str
    ) -> Optional[List[Any]]:
        return None


@dataclass
class HDF5FileReader(DatasetReader):
    def read_array(
        self, source: Union[BytesIO, str], path_in_external_file: str
    ) -> Optional[List[Any]]:
        with h5py.File(source, "r") as f:
            d_group = f[path_in_external_file]
            return d_group[()].tolist()

    def get_array_dimension(
        self, source: Union[BytesIO, str], path_in_external_file: str
    ) -> Optional[List[Any]]:
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
    return search_attribute_matching_name_with_path(
        obj, "(PathInHdfFile|PathInExternalFile)"
    )


def get_h5_path_possibilities(value_in_xml: str, epc: Epc) -> List[str]:
    """
    Maybe the path in the epc file objet was given as an absolute one : 'C:/my_file.h5'
    but if the epc has been moved (e.g. in 'D:/a_folder/') it will not work. Thus, the function
    energyml.utils.data.hdf.get_hdf5_path_from_external_path return the value from epc objet concatenate to the
    real epc folder path.
    With our example we will have : 'D:/a_folder/C:/my_file.h5'
    this function returns (following our example):
        [ 'C:/my_file.h5', 'D:/a_folder/my_file.h5', 'my_file.h5']
    :param value_in_xml:
    :param epc:
    :return:
    """
    epc_folder = epc.get_epc_file_folder()
    hdf5_path_respect = value_in_xml
    hdf5_path_rematch = f"{epc_folder+'/' if epc_folder is not None and len(epc_folder) else ''}{os.path.basename(value_in_xml)}"
    hdf5_path_no_folder = f"{os.path.basename(value_in_xml)}"

    return [
        hdf5_path_respect,
        hdf5_path_rematch,
        hdf5_path_no_folder,
        epc.epc_file_path[:-4] + ".h5",
    ]


def get_hdf5_path_from_external_path(
    external_path_obj: Any,
    path_in_root: Optional[str] = None,
    root_obj: Optional[Any] = None,
    epc: Optional[Epc] = None,
) -> Optional[List[str]]:
    """
    Return the hdf5 file path (Searches for "uri" attribute or in :param:`epc` rels files).
    :param external_path_obj: can be an attribute of an ExternalDataArrayPart
    :param path_in_root:
    :param root_obj:
    :param epc:
    :return:
    """
    result = []
    if isinstance(external_path_obj, str):
        # external_path_obj is maybe an attribute of an ExternalDataArrayPart, now search upper in the object
        upper_path = path_in_root[: path_in_root.rindex(".")]
        result = get_hdf5_path_from_external_path(
            external_path_obj=get_object_attribute(root_obj, upper_path),
            path_in_root=upper_path,
            root_obj=root_obj,
            epc=epc,
        )
    elif type(external_path_obj).__name__ == "ExternalDataArrayPart":
        # epc_folder = epc.get_epc_file_folder()
        h5_uri = search_attribute_matching_name(external_path_obj, "uri")
        if h5_uri is not None and len(h5_uri) > 0:
            result = get_h5_path_possibilities(value_in_xml=h5_uri[0], epc=epc)
            # result = f"{epc_folder}/{h5_uri[0]}"

    # epc_folder = epc.get_epc_file_folder()
    hdf_proxy_lst = search_attribute_matching_name(
        external_path_obj, "HdfProxy"
    )
    ext_file_proxy_lst = search_attribute_matching_name(
        external_path_obj, "ExternalFileProxy"
    )

    # resqml 2.0.1
    if hdf_proxy_lst is not None and len(hdf_proxy_lst) > 0:
        hdf_proxy = hdf_proxy_lst
        # logging.debug("h5Proxy", hdf_proxy)
        while isinstance(hdf_proxy, list):
            hdf_proxy = hdf_proxy[0]
        hdf_proxy_obj = epc.get_object_by_identifier(
            get_obj_identifier(hdf_proxy)
        )
        logging.debug("hdf_proxy_obj : ", hdf_proxy_obj, " hdf_proxy : ", hdf_proxy)
        if hdf_proxy_obj is not None:
            for rel in epc.additional_rels.get(
                get_obj_identifier(hdf_proxy_obj), []
            ):
                if (
                    rel.type_value
                    == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type()
                ):
                    result = get_h5_path_possibilities(
                        value_in_xml=rel.target, epc=epc
                    )
                    # result = f"{epc_folder}/{rel.target}"

    # resqml 2.2dev3
    if ext_file_proxy_lst is not None and len(ext_file_proxy_lst) > 0:
        ext_file_proxy = ext_file_proxy_lst
        while isinstance(ext_file_proxy, list):
            ext_file_proxy = ext_file_proxy[0]
        ext_part_ref_obj = epc.get_object_by_identifier(
            get_obj_identifier(
                get_object_attribute_no_verif(
                    ext_file_proxy, "epc_external_part_reference"
                )
            )
        )
        result = get_h5_path_possibilities(
            value_in_xml=ext_part_ref_obj.filename, epc=epc
        )
        # return f"{epc_folder}/{ext_part_ref_obj.filename}"

    result += list(
        filter(
            lambda p: p.lower().endswith(".h5") or p.lower().endswith(".hdf5"),
            epc.external_files_path or [],
        )
    )

    if len(result) == 0:
        result = [epc.epc_file_path[:-4] + ".h5"]

    logging.debug(
        external_path_obj,
        result,
        "\n\t",
        hdf_proxy_lst,
        "\n\t",
        ext_file_proxy_lst,
    )
    return result
