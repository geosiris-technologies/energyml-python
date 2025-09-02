# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
This module is a work in progress
"""  # pylint: disable=W0105

import logging
import os
import re
from dataclasses import dataclass
from io import BytesIO, TextIOWrapper, StringIO, BufferedReader
from typing import Optional, List, Tuple, Any, Union, TextIO, BinaryIO, Dict

import numpy as np

from .model import DatasetReader
from ..constants import EPCRelsRelationshipType, mime_type_to_file_extension
from ..exception import MissingExtraInstallation
from ..introspection import (
    search_attribute_matching_name_with_path,
    get_object_attribute,
    search_attribute_matching_name,
    get_obj_identifier,
    get_object_attribute_no_verif,
)

try:
    import h5py

    __H5PY_MODULE_EXISTS__ = True
except Exception as e:
    __H5PY_MODULE_EXISTS__ = False

try:
    import csv

    __CSV_MODULE_EXISTS__ = True
except Exception as e:
    __CSV_MODULE_EXISTS__ = False

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    from pandas import DataFrame

    # import pyarrow.feather as feather
    __PARQUET_MODULE_EXISTS__ = True
except Exception as e:
    __PARQUET_MODULE_EXISTS__ = False

# HDF5
if __H5PY_MODULE_EXISTS__:

    def h5_list_datasets(h5_file_path: Union[BytesIO, str]) -> List[str]:
        """
        List all datasets in an HDF5 file.
        :param h5_file_path: Path to the HDF5 file
        :return: List of dataset names in the HDF5 file
        """
        res = []
        with h5py.File(h5_file_path, "r") as f:
            # Function to print the names of all datasets
            def list_datasets(name, obj):
                if isinstance(obj, h5py.Dataset):  # Check if the object is a dataset
                    res.append(name)

            # Visit all items in the HDF5 file and apply the list function
            f.visititems(list_datasets)
        return res

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
            if h5_datasets_paths is None:
                h5_datasets_paths = h5_list_datasets(input_h5)
            if len(h5_datasets_paths) > 0:
                with h5py.File(output_h5, "a") as f_dest:
                    with h5py.File(input_h5, "r") as f_src:
                        for dataset in h5_datasets_paths:
                            f_dest.create_dataset(dataset, data=f_src[dataset])

    @dataclass
    class HDF5FileWriter:

        def write_array(
            self,
            target: Union[str, BytesIO, bytes],
            array: Union[list, np.ndarray],
            path_in_external_file: str,
            dtype: Optional[np.dtype] = None,
        ):
            if isinstance(array, list):
                array = np.asarray(array)
            print("writing array", target)
            with h5py.File(target, "a") as f:
                # print(array.dtype, h5py.string_dtype(), array.dtype == 'O')
                # print("\t", dtype or (h5py.string_dtype() if array.dtype == '0' else array.dtype))
                if isinstance(array, np.ndarray) and array.dtype == "O":
                    array = np.asarray([s.encode() if isinstance(s, str) else s for s in array])
                    np.void(array)
                dset = f.create_dataset(path_in_external_file, array.shape, dtype or array.dtype)
                dset[()] = array

else:

    class HDF5FileReader:
        def read_array(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def extract_h5_datasets(
            self,
            input_h5: Union[BytesIO, str],
            output_h5: Union[BytesIO, str],
            h5_datasets_paths: List[str],
        ) -> None:
            raise MissingExtraInstallation(extra_name="hdf5")


# APACHE PARQUET
if __PARQUET_MODULE_EXISTS__:

    @dataclass
    class ParquetFileReader:
        def read_array(
            self, source: Union[BytesIO, str], path_in_external_file: Optional[str] = None
        ) -> Optional[List[Any]]:
            """
            :param source: the parquet file path or memory file
            :param path_in_external_file: the column name in the parquet file, if None, the entire table is returned
                (with a name for each column, not as a simple matrix)
            :return:
            """
            if isinstance(source, bytes):
                source = pa.BufferReader(source)
            array = pq.read_table(source)
            if path_in_external_file is not None:
                return array[path_in_external_file]
            else:
                return array
            # return pq.read_table(source).to_pandas()
            # return pq.read_table(source).to_pandas()[path_in_external_file]

        def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
            if isinstance(source, bytes):
                source = pa.BufferReader(source)
            return pq.read_metadata(source)

    @dataclass
    class ParquetFileWriter:
        def write_array(
            self, target: Union[str, BytesIO, bytes], array: list, column_titles: Optional[List[str]] = None
        ) -> None:
            if (
                not isinstance(array[0], list)
                and not isinstance(array[0], np.ndarray)
                and not isinstance(array[0], pd.Series)
            ):
                # print(f"dtype : {type(array[0])}")
                array = [array]

            array_as_pd_df = pd.DataFrame({k: array[idx] for idx, k in enumerate(column_titles or range(len(array)))})

            pq.write_table(
                pa.Table.from_pandas(array_as_pd_df),
                target,
                version="2.6",
                compression="snappy",
            )

else:

    @dataclass
    class ParquetFileReader:
        def read_array(self, source: Union[BytesIO, str], path_in_external_file: Optional[str] = None) -> None:
            raise MissingExtraInstallation(extra_name="parquet")

        def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
            raise MissingExtraInstallation(extra_name="parquet")

    @dataclass
    class ParquetFileWriter:
        def write_array(
            self, target: Union[BytesIO, str], array: list, column_titles: Optional[List[str]] = None
        ) -> None:
            raise MissingExtraInstallation(extra_name="parquet")


# DAT
@dataclass
class DATFileReader:
    def read_array(
        self,
        source: Union[BytesIO, TextIO, str],
        path_in_external_file: Optional[Union[int, str]] = None,
        delimiter: Optional[str] = ",",
        has_headers: bool = False,
        encoding: Optional[str] = "utf-8",
        **fmtparams,
    ) -> Optional[Dict]:
        """
        :param source: the dat file path or memory file
        :param path_in_external_file: the column name (or number) in the dat file, if None, the entire table is returned
            as it is in the file
        :param delimiter: the column delimiter
        :param has_headers: set it to True if the file contains column titles
        :param encoding:
        :return:
        """
        if isinstance(source, str):
            with open(source, "r", newline="") as datFile:
                return self.read_array(datFile, path_in_external_file, delimiter, has_headers, encoding, **fmtparams)
        else:
            comments = ""
            s_pos = 0
            c = source.readline()
            while c.startswith("#"):
                s_pos = source.tell()
                comments += c
                c = source.readline()

            source.seek(s_pos)

            logging.debug(comments)

            items = []

            if len(comments) > 0:
                _delim = re.search(r'Default\s+delimiter:\s*"(?P<delim>[^"])"', comments, re.IGNORECASE)
                logging.debug("delim", _delim, _delim.group("delim"))
                if _delim is not None:
                    _delim = _delim.group("delim")
                    logging.debug(_delim, "<==")
                    if len(_delim) > 0:
                        delimiter = _delim

                items = re.findall(
                    r"Item\s*:\s*(?P<itemName>[\w]+)\s+line\s+number\s*:\s*(?P<lnum>\d+)\s+delimiter\s+field\s+number\s*:\s*(?P<idx>\d+)",
                    comments,
                    re.IGNORECASE,
                )
                logging.debug("items", items)

                items = list(map(lambda it: (it[0], int(it[1]), int(it[2])), items))

                _cst = re.findall(
                    r"Item\s*:\s*(?P<itemName>[\w]+)\s+constant\s*:\s*(?P<value>\w+)", comments, re.IGNORECASE
                )
                logging.debug("cst", _cst)

                max_line_number = 0
                for _, n, _ in items:
                    if n > max_line_number:
                        max_line_number = n

                for i in range(max_line_number - 1):
                    source.readline()  # on skip les values des autres items, on ne garde que le tableau de valeurs
                logging.debug(max_line_number)
                logging.debug(items)
                # removing items not related to the columns titles items
                items = list(filter(lambda it: it[1] == max_line_number, items))
                logging.debug(items)

            if isinstance(source, BytesIO) or isinstance(source, BinaryIO) or isinstance(source, BufferedReader):
                source = TextIOWrapper(source, encoding=encoding)
            elif isinstance(source, bytes):
                source = StringIO(source.decode(encoding=encoding))

            if items is not None and len(items) > 0:
                return pd.read_csv(source, delimiter=delimiter, names=list(map(lambda it: it[0], items)), **fmtparams)
            else:
                array = csv.reader(source, delimiter=delimiter, **fmtparams)
                if path_in_external_file is not None and array is not None:
                    idx = int(path_in_external_file)
                    return [row[idx] for row in list(filter(lambda l: len(l) > 0, list(array)))]
                else:
                    return list(array)

    def read_array_as_panda_dict(
        self, source: Union[BytesIO, TextIO, str], delimiter: Optional[str] = ",", has_header: bool = True, **fmtparams
    ) -> Optional[Any]:
        if isinstance(source, str):
            with open(source, "r", newline="") as datFile:
                return self.read_array_as_panda_dict(datFile, delimiter, has_header=has_header, **fmtparams)
        else:
            return pd.read_csv(source, delimiter=delimiter, header=0 if has_header else None, **fmtparams)


# CSV
@dataclass
class CSVFileReader:
    def read_array(
        self,
        source: Union[BytesIO, TextIO, str],
        path_in_external_file: Optional[Union[int, str]] = None,
        delimiter: Optional[str] = ",",
        has_headers: bool = False,
        encoding: Optional[str] = "utf-8",
        **fmtparams,
    ) -> Optional[List[Any]]:
        """
        :param source: the csv file path or memory file
        :param path_in_external_file: the column name (or number) in the csv file, if None, the entire table is returned
            as it is in the file
        :param delimiter: the column delimiter
        :param has_headers: set it to True if the file contains column titles
        :return:
        """
        if isinstance(source, str):
            with open(source, "r", newline="") as csvFile:
                return self.read_array(csvFile, path_in_external_file, delimiter, has_headers, encoding, **fmtparams)
        else:
            if isinstance(source, BytesIO) or isinstance(source, BinaryIO) or isinstance(source, BufferedReader):
                source = TextIOWrapper(source, encoding=encoding)
            elif isinstance(source, bytes):
                source = StringIO(source.decode(encoding=encoding))

            if has_headers:
                if path_in_external_file is not None:
                    dictionary = csv.DictReader(source, delimiter=delimiter, **fmtparams)
                    if dictionary is not None:
                        return [row[path_in_external_file] for row in dictionary]
                else:
                    # array = pd.read_csv(source, delimiter=delimiter, **fmtparams)
                    # return [array.keys().tolist()] + array.values.tolist()
                    array = csv.reader(source, delimiter=delimiter, **fmtparams)
                    return list(array)
            else:
                array = csv.reader(source, delimiter=delimiter, **fmtparams)
                if path_in_external_file is not None and array is not None:
                    idx = int(path_in_external_file)
                    # for row in list(array):
                    #     print(len(row))
                    return [row[idx] for row in list(filter(lambda l: len(l) > 0, list(array)))]
                else:
                    return list(array)

    def read_array_as_panda_dict(
        self, source: Union[BytesIO, TextIO, str], delimiter: Optional[str] = ",", has_header: bool = True, **fmtparams
    ) -> Optional[Any]:
        if isinstance(source, str):
            with open(source, "r", newline="") as csvFile:
                return self.read_array_as_panda_dict(csvFile, delimiter, has_header=has_header, **fmtparams)
        else:
            return pd.read_csv(source, delimiter=delimiter, header=0 if has_header else None, **fmtparams)


@dataclass
class CSVFileWriter:
    def write_array(
        self,
        target: Union[BytesIO, TextIO, bytes, str],
        array: list,
        column_titles: Optional[List[str]] = None,
        delimiter: str = ",",
        **fmtparams,
    ) -> Optional[List[Any]]:
        if not isinstance(array[0], list):
            array = [array]

        if isinstance(target, str):
            with open(target, "w", newline="") as csvFile:
                return self.write_array(csvFile, array, column_titles, delimiter, **fmtparams)
        else:
            csvwriter = csv.writer(target, delimiter=delimiter, **fmtparams)
            csvwriter.writerows(array)


##############
def get_external_file_path_possibilities(
    value_in_xml: str, epc: Any, file_extension: Optional[str] = "h5"
) -> List[str]:
    """
    Maybe the path in the epc file objet was given as an absolute one : 'C:/my_file.h5'
    but if the epc has been moved (e.g. in 'D:/a_folder/') it will not work. Thus, the function
    energyml.utils.data.hdf.get_hdf5_path_from_external_path return the value from epc objet concatenate to the
    real epc folder path.
    With our example we will have : 'D:/a_folder/C:/my_file.h5'
    this function returns (following our example):
        [ 'C:/my_file.h5', 'D:/a_folder/my_file.h5', 'my_file.h5' ]
    :param value_in_xml:
    :param epc:
    :param file_extension: the external file extension (usually "h5" for "YOUR_HDF_FILE.h5")
    :return:
    """
    if epc is not None:
        epc_folder = epc.get_epc_file_folder()
        return get_external_file_path_possibilities_from_folder(file_raw_path=value_in_xml, folder_path=epc_folder) + [
            epc.epc_file_path[:-4] + f".{file_extension}",
        ]
    else:
        return get_external_file_path_possibilities_from_folder(file_raw_path=value_in_xml, folder_path=".")


def get_external_file_path_from_external_path(
    external_path_obj: Any,
    path_in_root: Optional[str] = None,
    root_obj: Optional[Any] = None,
    epc: Optional[Any] = None,
) -> Optional[List[str]]:
    """
    Return the hdf5 (or other type) file path (Searches for "uri" attribute or in :param:`epc` rels files).
    :param external_path_obj: can be an attribute of an ExternalDataArrayPart
    :param path_in_root:
    :param root_obj:
    :param epc: an EPC instance
    :return:
    """
    result = []
    if isinstance(external_path_obj, str):
        # external_path_obj is maybe an attribute of an ExternalDataArrayPart, now search upper in the object
        upper_path = path_in_root[: path_in_root.rindex(".")]
        result = get_external_file_path_from_external_path(
            external_path_obj=get_object_attribute(root_obj, upper_path),
            path_in_root=upper_path,
            root_obj=root_obj,
            epc=epc,
        )
    elif type(external_path_obj).__name__ == "ExternalDataArrayPart":
        # epc_folder = epc.get_epc_file_folder()
        external_file_uri = search_attribute_matching_name(external_path_obj, "uri")
        mimetype = next(iter(search_attribute_matching_name(external_path_obj, "MimeType")), None)
        if external_file_uri is not None and len(external_file_uri) > 0:
            result = get_external_file_path_possibilities(
                value_in_xml=external_file_uri[0], epc=epc, file_extension=mime_type_to_file_extension(mimetype) or "h5"
            )
            # result = f"{epc_folder}/{h5_uri[0]}"

    # epc_folder = epc.get_epc_file_folder()
    hdf_proxy_lst = search_attribute_matching_name(external_path_obj, "HdfProxy")
    ext_file_proxy_lst = search_attribute_matching_name(external_path_obj, "ExternalFileProxy")

    # resqml 2.0.1
    if hdf_proxy_lst is not None and len(hdf_proxy_lst) > 0:
        hdf_proxy = hdf_proxy_lst
        # logging.debug("h5Proxy", hdf_proxy)
        while isinstance(hdf_proxy, list):
            hdf_proxy = hdf_proxy[0]
        hdf_proxy_obj = epc.get_object_by_identifier(get_obj_identifier(hdf_proxy))
        try:
            logging.debug(f"hdf_proxy_obj : {hdf_proxy_obj} {hdf_proxy} : {hdf_proxy}")
        except:
            pass
        if hdf_proxy_obj is not None:
            for rel in epc.additional_rels.get(get_obj_identifier(hdf_proxy_obj), []):
                if rel.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
                    result = get_external_file_path_possibilities(value_in_xml=rel.target, epc=epc)
                    # result = f"{epc_folder}/{rel.target}"

    # resqml 2.2dev3
    if ext_file_proxy_lst is not None and len(ext_file_proxy_lst) > 0:
        ext_file_proxy = ext_file_proxy_lst
        while isinstance(ext_file_proxy, list):
            ext_file_proxy = ext_file_proxy[0]
        ext_part_ref_obj = epc.get_object_by_identifier(
            get_obj_identifier(get_object_attribute_no_verif(ext_file_proxy, "epc_external_part_reference"))
        )
        result = get_external_file_path_possibilities(value_in_xml=ext_part_ref_obj.filename, epc=epc)
        # return f"{epc_folder}/{ext_part_ref_obj.filename}"

    # result += list(
    #     filter(
    #         lambda p: p.lower().endswith(".h5") or p.lower().endswith(".hdf5"),
    #         epc.external_files_path or [],
    #     )
    # )

    if epc is not None and len(result) == 0:
        result = [epc.epc_file_path[:-4] + ".h5"]

    try:
        logging.debug(f"{external_path_obj} {result} \n\t{hdf_proxy_lst}\n\t{ext_file_proxy_lst}")
    except:
        pass
    return result


def get_external_file_path_possibilities_from_folder(file_raw_path: str, folder_path: str) -> List[str]:
    external_path_respect = file_raw_path
    external_path_rematch = f"{folder_path + '/' if folder_path is not None and len(folder_path) else ''}{os.path.basename(file_raw_path or '')}"
    external_path_no_folder = f"{os.path.basename(file_raw_path)}" if file_raw_path is not None else ""

    return [
        external_path_respect,
        external_path_rematch,
        external_path_no_folder,
    ]


def read_dataset(
    source: Union[BytesIO, str],
    path_in_external_file: Optional[str] = None,
    mimetype: Optional[str] = "application/x-hdf5",
) -> Any:
    mimetype = (mimetype or "").lower()
    file_reader = HDF5FileReader()  # default is hdf5
    if "parquet" in mimetype or (
        isinstance(source, str) and (source.lower().endswith(".parquet") or source.lower().endswith(".pqt"))
    ):
        file_reader = ParquetFileReader()
    elif "csv" in mimetype or (
        isinstance(source, str) and (source.lower().endswith(".csv") or source.lower().endswith(".dat"))
    ):
        file_reader = CSVFileReader()
    return file_reader.read_array(source, path_in_external_file)


def read_external_dataset_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    additional_sources: Optional[List[Union[str, BytesIO, BufferedReader]]] = None,
    epc: Optional[any] = None,
):
    if additional_sources is None:
        additional_sources = []
    result_array = []

    for path_in_obj, path_in_external in get_path_in_external_with_path(energyml_array):
        succeed = False
        external_array_obj_path = ".".join(path_in_obj.split(".")[:-1])
        external_path_obj = get_object_attribute(obj=energyml_array, attr_dot_path=external_array_obj_path)
        mimetype = next(iter(search_attribute_matching_name(external_path_obj, "MimeType")), "application/x-hdf5")

        sources = additional_sources
        sources = sources + get_external_file_path_from_external_path(
            external_path_obj=external_path_obj, path_in_root=path_in_root, root_obj=root_obj, epc=epc
        )
        for s in sources:
            try:
                # TODO: take care of the "Counts" and "Starts" list in ExternalDataArrayPart to fill array correctly
                result_array = result_array + read_dataset(
                    source=s, path_in_external_file=path_in_external, mimetype=mimetype
                )
                succeed = True
                break  # stop after the first read success
            except MissingExtraInstallation as mei:
                raise mei
            except Exception as e:
                logging.debug(f"Failed to read external file {s} for {path_in_obj} with path {path_in_external} : {e}")
                pass
        if not succeed:
            raise Exception(f"Failed to read external file. Paths tried : {sources}")

    return result_array


def get_path_in_external(obj) -> List[Any]:
    """
    See :func:`get_path_in_external_with_path`. Only the value is returned, not the dot path into the object
    :param obj:
    :return:
    """
    return [val for path, val in get_path_in_external_with_path(obj=obj)]


def get_path_in_external_with_path(obj: any) -> List[Tuple[str, Any]]:
    """
    See :func:`search_attribute_matching_name_with_path`. Search an attribute with type matching regex
    "(PathInHdfFile|PathInExternalFile)".

    :param obj:
    :return: [ (Dot_Path_In_Obj, value), ...]
    """
    return search_attribute_matching_name_with_path(obj, "(PathInHdfFile|PathInExternalFile)")
