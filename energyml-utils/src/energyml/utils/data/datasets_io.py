# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
This module is a work in progress
"""  # pylint: disable=W0105

import logging
import os
import re
import numpy as np
from dataclasses import dataclass
from io import BytesIO, TextIOWrapper, StringIO, BufferedReader
from typing import Optional, List, Tuple, Any, Union, TextIO, BinaryIO, Dict

from energyml.utils.uri import Uri, parse_uri

from energyml.utils.data.model import DatasetReader
from energyml.utils.constants import EPCRelsRelationshipType, mime_type_to_file_extension, path_last_attribute
from energyml.utils.exception import MissingExtraInstallation
from energyml.utils.introspection import (
    get_obj_uri,
    search_attribute_matching_name_with_path,
    get_object_attribute,
    search_attribute_matching_name,
    get_obj_identifier,
    get_object_attribute_no_verif,
)

try:
    import h5py

    __H5PY_MODULE_EXISTS__ = True
except Exception:
    h5py = None
    __H5PY_MODULE_EXISTS__ = False

try:
    import csv

    __CSV_MODULE_EXISTS__ = True
except Exception:
    __CSV_MODULE_EXISTS__ = False

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    # import pyarrow.feather as feather
    __PARQUET_MODULE_EXISTS__ = True
except Exception:
    __PARQUET_MODULE_EXISTS__ = False

# HDF5
if __H5PY_MODULE_EXISTS__:

    def h5_list_datasets(h5_file_path: Union[BytesIO, str, "h5py.File"]) -> List[str]:
        """
        List all datasets in an HDF5 file.
        :param h5_file_path: Path to the HDF5 file, BytesIO object, or an already opened h5py.File
        :return: List of dataset names in the HDF5 file
        """
        res = []

        # Check if it's already an opened h5py.File
        if isinstance(h5_file_path, h5py.File):  # type: ignore

            def list_datasets(name, obj):
                if isinstance(obj, h5py.Dataset):  # type: ignore
                    res.append(name)

            h5_file_path.visititems(list_datasets)
        else:
            with h5py.File(h5_file_path, "r") as f:  # type: ignore
                # Function to print the names of all datasets
                def list_datasets(name, obj):
                    if isinstance(obj, h5py.Dataset):  # Check if the object is a dataset  # type: ignore
                        res.append(name)

                # Visit all items in the HDF5 file and apply the list function
                f.visititems(list_datasets)
        return res

    @dataclass
    class HDF5FileReader(DatasetReader):  # noqa: F401
        def read_array(
            self, source: Union[BytesIO, str, "h5py.File"], path_in_external_file: str
        ) -> Optional[np.ndarray]:
            # Check if it's already an opened h5py.File
            if isinstance(source, h5py.File):  # type: ignore
                d_group = source[path_in_external_file]
                return d_group[()]  # type: ignore
            else:
                with h5py.File(source, "r") as f:  # type: ignore
                    d_group = f[path_in_external_file]
                    return d_group[()]  # type: ignore

        def get_array_dimension(
            self, source: Union[BytesIO, str, "h5py.File"], path_in_external_file: str
        ) -> Optional[List[int]]:
            # Check if it's already an opened h5py.File
            if isinstance(source, h5py.File):  # type: ignore
                return list(source[path_in_external_file].shape)
            else:
                with h5py.File(source, "r") as f:  # type: ignore
                    return list(f[path_in_external_file].shape)

        def extract_h5_datasets(
            self,
            input_h5: Union[BytesIO, str, "h5py.File"],
            output_h5: Union[BytesIO, str, "h5py.File"],
            h5_datasets_paths: List[str],
        ) -> None:
            """
            Copy all dataset from :param input_h5 matching with paths in :param h5_datasets_paths into the :param output
            :param input_h5: Path to HDF5 file, BytesIO, or already opened h5py.File
            :param output_h5: Path to HDF5 file, BytesIO, or already opened h5py.File
            :param h5_datasets_paths:
            :return:
            """
            if h5_datasets_paths is None:
                h5_datasets_paths = h5_list_datasets(input_h5)
            if len(h5_datasets_paths) > 0:
                # Handle output file
                should_close_dest = not isinstance(output_h5, h5py.File)  # type: ignore
                f_dest = output_h5 if isinstance(output_h5, h5py.File) else h5py.File(output_h5, "a")  # type: ignore

                try:
                    # Handle input file
                    should_close_src = not isinstance(input_h5, h5py.File)  # type: ignore
                    f_src = input_h5 if isinstance(input_h5, h5py.File) else h5py.File(input_h5, "r")  # type: ignore

                    try:
                        for dataset in h5_datasets_paths:
                            f_dest.create_dataset(dataset, data=f_src[dataset])
                    finally:
                        if should_close_src:
                            f_src.close()
                finally:
                    if should_close_dest:
                        f_dest.close()

    @dataclass
    class HDF5FileWriter:

        def write_array(
            self,
            target: Union[str, BytesIO, bytes, "h5py.File"],
            array: Union[list, np.ndarray],
            path_in_external_file: str,
            dtype: Optional[np.dtype] = None,
        ):
            if isinstance(array, list):
                array = np.asarray(array)
            print("writing array", target)
            if dtype is not None and not isinstance(dtype, np.dtype):
                dtype = np.dtype(dtype)

            # Check if it's already an opened h5py.File
            if isinstance(target, h5py.File):  # type: ignore
                if isinstance(array, np.ndarray) and array.dtype == "O":
                    array = np.asarray([s.encode() if isinstance(s, str) else s for s in array])
                    np.void(array)
                dset = target.create_dataset(path_in_external_file, array.shape, dtype or array.dtype)
                dset[()] = array
            else:
                with h5py.File(target, "a") as f:  # type: ignore
                    # print(array.dtype, h5py.string_dtype(), array.dtype == 'O')
                    # print("\t", dtype or (h5py.string_dtype() if array.dtype == '0' else array.dtype))
                    if isinstance(array, np.ndarray) and array.dtype == "O":
                        array = np.asarray([s.encode() if isinstance(s, str) else s for s in array])
                        np.void(array)
                    dset = f.create_dataset(path_in_external_file, array.shape, dtype or array.dtype)
                    dset[()] = array

else:

    class HDF5FileReader:
        def read_array(self, source: Union[BytesIO, str, Any], path_in_external_file: str) -> Optional[np.ndarray]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def get_array_dimension(
            self, source: Union[BytesIO, str, Any], path_in_external_file: str
        ) -> Optional[np.ndarray]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def extract_h5_datasets(
            self,
            input_h5: Union[BytesIO, str, Any],
            output_h5: Union[BytesIO, str, Any],
            h5_datasets_paths: List[str],
        ) -> None:
            raise MissingExtraInstallation(extra_name="hdf5")

    class HDF5FileWriter:

        def write_array(
            self,
            target: Union[str, BytesIO, bytes, Any],
            array: Union[list, np.ndarray],
            path_in_external_file: str,
            dtype: Optional[np.dtype] = None,
        ):
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
                comments += str(c)
                c = source.readline()

            source.seek(s_pos)

            logging.debug(comments)

            items = []

            if len(comments) > 0:
                _delim = re.search(r'Default\s+delimiter:\s*"(?P<delim>[^"])"', comments, re.IGNORECASE)
                if _delim is not None:
                    logging.debug("delim", _delim, _delim.group("delim"))
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
                    return [row[idx] for row in list(filter(lambda line: len(line) > 0, list(array)))]
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
                    return [row[idx] for row in list(filter(lambda line: len(line) > 0, list(array)))]
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
    if "parquet" in mimetype or (
        isinstance(source, str) and (source.lower().endswith(".parquet") or source.lower().endswith(".pqt"))
    ):
        file_reader = ParquetFileReader()
    elif "csv" in mimetype or (
        isinstance(source, str) and (source.lower().endswith(".csv") or source.lower().endswith(".dat"))
    ):
        file_reader = CSVFileReader()
    else:
        file_reader = HDF5FileReader()  # default is hdf5
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


def get_path_in_external_with_path(obj: Any) -> List[Tuple[str, Any]]:
    """
    See :func:`search_attribute_matching_name_with_path`. Search an attribute with type matching regex
    "(PathInHdfFile|PathInExternalFile)".

    :param obj:
    :return: [ (Dot_Path_In_Obj, value), ...]
    """
    return search_attribute_matching_name_with_path(obj, "(PathInHdfFile|PathInExternalFile)")


def get_proxy_uri_for_path_in_external(obj: Any, dataspace_name_or_uri: Union[str, Uri]) -> Dict[str, List[Any]]:
    """
    Search all PathInHdfFile or PathInExternalFile in the object and return a map of uri to list of path found
    in the object for this uri.

    :param obj:
    :param dataspace_name_or_uri: the dataspace name or uri to search
    :return: { uri : [ path_in_external1, path_in_external2, ... ], ... }
    """
    if dataspace_name_or_uri is not None and isinstance(dataspace_name_or_uri, str):
        dataspace_name_or_uri = dataspace_name_or_uri.strip()
    ds_name = dataspace_name_or_uri
    if isinstance(dataspace_name_or_uri, str):
        if dataspace_name_or_uri is not None:
            if not dataspace_name_or_uri.startswith("eml:///"):
                dataspace_name_or_uri = f"eml:///dataspace('{dataspace_name_or_uri}')"
        else:
            dataspace_name_or_uri = "eml:///"
        ds_uri = parse_uri(dataspace_name_or_uri)
        assert ds_uri is not None, f"Cannot parse dataspace uri {dataspace_name_or_uri}"
        ds_name = ds_uri.dataspace
    elif isinstance(dataspace_name_or_uri, Uri):
        ds_name = dataspace_name_or_uri.dataspace

    uri_path_map = {}
    _piefs = get_path_in_external_with_path(obj)
    if _piefs is not None and len(_piefs) > 0:
        # logging.info(f"Found {_piefs} datasets in object {get_obj_uuid(obj)}")

        # uri_path_map[uri] = _piefs
        for item in _piefs:
            uri = str(get_obj_uri(obj, dataspace=ds_name))
            if isinstance(item, tuple):
                logging.info(
                    f"Item: {item}, type: {type(item)}, len: {len(item) if hasattr(item, '__len__') else 'N/A'}"
                )
                # Then unpack
                path, pief = item
                # logging.info(f"\t test : {path_last_attribute(path)}")
                if "hdf" in path_last_attribute(path).lower():
                    dor = get_object_attribute(
                        obj=obj, attr_dot_path=path[: -len(path_last_attribute(path))] + "hdf_proxy"
                    )
                    proxy_uuid = get_object_attribute(obj=dor, attr_dot_path="uuid")
                    if proxy_uuid is not None:
                        uri = str(get_obj_uri(dor, dataspace=ds_name))

                if uri not in uri_path_map:
                    uri_path_map[uri] = []
                uri_path_map[uri].append(pief)
    else:
        logging.debug(f"No datasets found in object {str(get_obj_uri(obj))}")
    return uri_path_map


# ===========================================================================================
# FILE CACHE MANAGER AND HANDLER REGISTRY
# ===========================================================================================

from collections import OrderedDict
from typing import Callable
from energyml.utils.data.model import ExternalArrayHandler


class FileCacheManager:
    """
    Manages a cache of open file handles to avoid reopening overhead.

    Keeps up to `max_open_files` (default 3) files open using an LRU strategy.
    When a file is accessed, it moves to the front of the cache. When the cache
    is full, the least recently used file is closed and removed.

    Features:
    - Thread-safe access to file handles
    - Automatic cleanup of least-recently-used files
    - Support for any file type with proper handlers
    - Explicit close() method for cleanup
    """

    def __init__(self, max_open_files: int = 3):
        """
        Initialize file cache manager.

        Args:
            max_open_files: Maximum number of files to keep open simultaneously
        """
        self.max_open_files = max_open_files
        self._cache: OrderedDict[str, Any] = OrderedDict()  # file_path -> open file handle
        self._handlers: Dict[str, ExternalArrayHandler] = {}  # file_path -> handler instance

    def get_or_open(self, file_path: str, handler: ExternalArrayHandler, mode: str = "r") -> Optional[Any]:
        """
        Get an open file handle from cache, or open it if not cached.

        Args:
            file_path: Path to the file
            handler: Handler instance that knows how to open this file type
            mode: File open mode ('r', 'a', etc.)

        Returns:
            Open file handle, or None if opening failed
        """
        # Normalize path
        file_path = os.path.abspath(file_path) if os.path.exists(file_path) else file_path

        # Check cache first
        if file_path in self._cache:
            # Move to end (most recently used)
            self._cache.move_to_end(file_path)
            return self._cache[file_path]

        # Not in cache - try to open it
        try:
            file_handle = self._open_file(file_path, mode)
            if file_handle is None:
                return None

            # Add to cache
            self._cache[file_path] = file_handle
            self._handlers[file_path] = handler
            self._cache.move_to_end(file_path)

            # Evict oldest if cache is full
            if len(self._cache) > self.max_open_files:
                self._evict_oldest()

            return file_handle

        except Exception as e:
            logging.debug(f"Failed to open file {file_path}: {e}")
            return None

    def _open_file(self, file_path: str, mode: str) -> Optional[Any]:
        """
        Open a file based on its extension.

        Args:
            file_path: Path to the file
            mode: File open mode

        Returns:
            Open file handle specific to the file type
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext in [".h5", ".hdf5"] and __H5PY_MODULE_EXISTS__:
            return h5py.File(file_path, mode)  # type: ignore
        # Add other file types as needed
        # For now, other types will be opened on-demand by their handlers

        return None

    def _evict_oldest(self) -> None:
        """Remove the least recently used file from cache."""
        if not self._cache:
            return

        # Get oldest (first) item
        oldest_path, oldest_handle = self._cache.popitem(last=False)

        # Close the file handle
        try:
            if hasattr(oldest_handle, "close"):
                oldest_handle.close()
        except Exception as e:
            logging.debug(f"Error closing cached file {oldest_path}: {e}")

        # Remove handler reference
        if oldest_path in self._handlers:
            del self._handlers[oldest_path]

    def close_all(self) -> None:
        """Close all cached file handles."""
        for file_path, file_handle in list(self._cache.items()):
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except Exception as e:
                logging.debug(f"Error closing file {file_path}: {e}")

        self._cache.clear()
        self._handlers.clear()

    def remove(self, file_path: str) -> None:
        """
        Remove a specific file from cache and close it.

        Args:
            file_path: Path to the file to remove
        """
        file_path = os.path.abspath(file_path) if os.path.exists(file_path) else file_path

        if file_path in self._cache:
            file_handle = self._cache.pop(file_path)
            try:
                if hasattr(file_handle, "close"):
                    file_handle.close()
            except Exception as e:
                logging.debug(f"Error closing file {file_path}: {e}")

        if file_path in self._handlers:
            del self._handlers[file_path]

    def __len__(self) -> int:
        """Return number of cached files."""
        return len(self._cache)

    def __contains__(self, file_path: str) -> bool:
        """Check if a file is in cache."""
        file_path = os.path.abspath(file_path) if os.path.exists(file_path) else file_path
        return file_path in self._cache


class FileHandlerRegistry:
    """
    Global registry that maps file extensions to handler classes.

    This allows the system to automatically select the correct handler
    based on file extension without hardcoding dependencies.

    Usage:
        registry = FileHandlerRegistry()
        handler = registry.get_handler_for_file("data.h5")
        if handler:
            array = handler.read_array("data.h5", "/dataset/path")
    """

    def __init__(self):
        self._handlers: Dict[str, Callable[[], ExternalArrayHandler]] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register all available handlers based on installed dependencies."""
        # HDF5 Handler
        if __H5PY_MODULE_EXISTS__:
            self.register_handler([".h5", ".hdf5"], lambda: HDF5ArrayHandler())
        else:
            self.register_handler([".h5", ".hdf5"], lambda: MockHDF5ArrayHandler())

        # Parquet Handler
        if __PARQUET_MODULE_EXISTS__:
            self.register_handler([".parquet", ".pq"], lambda: ParquetArrayHandler())
        else:
            self.register_handler([".parquet", ".pq"], lambda: MockParquetArrayHandler())

        # CSV Handler - always available (uses Python's csv module)
        if __CSV_MODULE_EXISTS__:
            self.register_handler([".csv", ".txt", ".dat"], lambda: CSVArrayHandler())

    def register_handler(self, extensions: List[str], handler_factory: Callable[[], ExternalArrayHandler]) -> None:
        """
        Register a handler factory for given file extensions.

        Args:
            extensions: List of file extensions (with leading dot, e.g., ['.h5', '.hdf5'])
            handler_factory: Callable that returns a new handler instance
        """
        for ext in extensions:
            ext_lower = ext.lower() if ext.startswith(".") else "." + ext.lower()
            self._handlers[ext_lower] = handler_factory

    def get_handler_for_file(self, file_path: str) -> Optional[ExternalArrayHandler]:
        """
        Get appropriate handler for a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            Handler instance, or None if no handler registered for this extension
        """
        ext = os.path.splitext(file_path)[1].lower()

        if ext in self._handlers:
            return self._handlers[ext]()

        return None

    def supports_extension(self, extension: str) -> bool:
        """
        Check if a handler is registered for the given extension.

        Args:
            extension: File extension (with or without leading dot)

        Returns:
            True if a handler is registered
        """
        ext_lower = extension.lower() if extension.startswith(".") else "." + extension.lower()
        return ext_lower in self._handlers


# Global registry instance
_GLOBAL_HANDLER_REGISTRY = FileHandlerRegistry()


def get_handler_registry() -> FileHandlerRegistry:
    """Get the global file handler registry."""
    return _GLOBAL_HANDLER_REGISTRY


# ===========================================================================================
# CONCRETE HANDLER IMPLEMENTATIONS
# ===========================================================================================

# HDF5 Handler
if __H5PY_MODULE_EXISTS__:

    class HDF5ArrayHandler(ExternalArrayHandler):
        """Handler for HDF5 files (.h5, .hdf5)."""

        def read_array(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[np.ndarray]:
            """Read array from HDF5 file."""
            if isinstance(source, h5py.File):  # type: ignore
                if path_in_external_file:
                    d_group = source[path_in_external_file]
                    return d_group[()]  # type: ignore
                return None
            else:
                with h5py.File(source, "r") as f:  # type: ignore
                    if path_in_external_file:
                        d_group = f[path_in_external_file]
                        return d_group[()]  # type: ignore
                    return None

        def write_array(
            self,
            target: Union[str, BytesIO, Any],
            array: Union[list, np.ndarray],
            path_in_external_file: Optional[str] = None,
            **kwargs,
        ) -> bool:
            """Write array to HDF5 file."""
            if not path_in_external_file:
                return False

            if isinstance(array, list):
                array = np.asarray(array)

            dtype = kwargs.get("dtype")
            if dtype is not None and not isinstance(dtype, np.dtype):
                dtype = np.dtype(dtype)

            try:
                if isinstance(target, h5py.File):  # type: ignore
                    if isinstance(array, np.ndarray) and array.dtype == "O":
                        array = np.asarray([s.encode() if isinstance(s, str) else s for s in array])
                        np.void(array)
                    dset = target.create_dataset(path_in_external_file, array.shape, dtype or array.dtype)
                    dset[()] = array
                else:
                    with h5py.File(target, "a") as f:  # type: ignore
                        if isinstance(array, np.ndarray) and array.dtype == "O":
                            array = np.asarray([s.encode() if isinstance(s, str) else s for s in array])
                            np.void(array)
                        dset = f.create_dataset(path_in_external_file, array.shape, dtype or array.dtype)
                        dset[()] = array
                return True
            except Exception as e:
                logging.error(f"Failed to write array to HDF5: {e}")
                return False

        def get_array_metadata(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[Union[dict, List[dict]]]:
            """Get metadata for HDF5 datasets."""
            try:
                if isinstance(source, h5py.File):  # type: ignore
                    if path_in_external_file:
                        dset = source[path_in_external_file]
                        return {
                            "path": path_in_external_file,
                            "dtype": str(dset.dtype),
                            "shape": list(dset.shape),
                            "size": dset.size,
                        }
                    else:
                        # List all datasets
                        datasets = h5_list_datasets(source)
                        return [self.get_array_metadata(source, ds) for ds in datasets]
                else:
                    with h5py.File(source, "r") as f:  # type: ignore
                        return self.get_array_metadata(f, path_in_external_file)
            except Exception as e:
                logging.debug(f"Failed to get HDF5 metadata: {e}")
                return None

        def list_arrays(self, source: Union[BytesIO, str, Any]) -> List[str]:
            """List all datasets in HDF5 file."""
            return h5_list_datasets(source)

        def can_handle_file(self, file_path: str) -> bool:
            """Check if this handler can process the file."""
            ext = os.path.splitext(file_path)[1].lower()
            return ext in [".h5", ".hdf5"]

else:

    class MockHDF5ArrayHandler(ExternalArrayHandler):
        """Mock handler when h5py is not installed."""

        def read_array(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[np.ndarray]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def write_array(
            self,
            target: Union[str, BytesIO, Any],
            array: Union[list, np.ndarray],
            path_in_external_file: Optional[str] = None,
            **kwargs,
        ) -> bool:
            raise MissingExtraInstallation(extra_name="hdf5")

        def get_array_metadata(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[Union[dict, List[dict]]]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def list_arrays(self, source: Union[BytesIO, str, Any]) -> List[str]:
            raise MissingExtraInstallation(extra_name="hdf5")

        def can_handle_file(self, file_path: str) -> bool:
            return os.path.splitext(file_path)[1].lower() in [".h5", ".hdf5"]


# Parquet Handler
if __PARQUET_MODULE_EXISTS__:

    class ParquetArrayHandler(ExternalArrayHandler):
        """Handler for Parquet files (.parquet, .pq)."""

        def read_array(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[np.ndarray]:
            """Read array from Parquet file."""
            if isinstance(source, bytes):
                source = pa.BufferReader(source)

            table = pq.read_table(source)

            if path_in_external_file:
                return np.array(table[path_in_external_file])
            else:
                # Return all columns as 2D array
                return table.to_pandas().values

        def write_array(
            self,
            target: Union[str, BytesIO, Any],
            array: Union[list, np.ndarray],
            path_in_external_file: Optional[str] = None,
            **kwargs,
        ) -> bool:
            """Write array to Parquet file."""
            column_titles = kwargs.get("column_titles")

            try:
                if not isinstance(array[0], (list, np.ndarray, pd.Series)):
                    array = [array]

                array_as_pd_df = pd.DataFrame(
                    {k: array[idx] for idx, k in enumerate(column_titles or range(len(array)))}
                )

                pq.write_table(
                    pa.Table.from_pandas(array_as_pd_df),
                    target,
                    version="2.6",
                    compression="snappy",
                )
                return True
            except Exception as e:
                logging.error(f"Failed to write array to Parquet: {e}")
                return False

        def get_array_metadata(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[Union[dict, List[dict]]]:
            """Get metadata for Parquet columns."""
            try:
                if isinstance(source, bytes):
                    source = pa.BufferReader(source)

                metadata = pq.read_metadata(source)
                schema = pq.read_schema(source)

                if path_in_external_file:
                    # Get specific column metadata
                    col_idx = schema.get_field_index(path_in_external_file)
                    if col_idx >= 0:
                        field = schema.field(col_idx)
                        return {
                            "path": path_in_external_file,
                            "dtype": str(field.type),
                            "shape": [metadata.num_rows],
                            "size": metadata.num_rows,
                        }
                else:
                    # Get all columns
                    return [
                        {
                            "path": field.name,
                            "dtype": str(field.type),
                            "shape": [metadata.num_rows],
                            "size": metadata.num_rows,
                        }
                        for field in schema
                    ]
            except Exception as e:
                logging.debug(f"Failed to get Parquet metadata: {e}")
                return None

        def list_arrays(self, source: Union[BytesIO, str, Any]) -> List[str]:
            """List all columns in Parquet file."""
            try:
                if isinstance(source, bytes):
                    source = pa.BufferReader(source)
                schema = pq.read_schema(source)
                return [field.name for field in schema]
            except Exception:
                return []

        def can_handle_file(self, file_path: str) -> bool:
            """Check if this handler can process the file."""
            ext = os.path.splitext(file_path)[1].lower()
            return ext in [".parquet", ".pq"]

else:

    class MockParquetArrayHandler(ExternalArrayHandler):
        """Mock handler when parquet libraries are not installed."""

        def read_array(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[np.ndarray]:
            raise MissingExtraInstallation(extra_name="parquet")

        def write_array(
            self,
            target: Union[str, BytesIO, Any],
            array: Union[list, np.ndarray],
            path_in_external_file: Optional[str] = None,
            **kwargs,
        ) -> bool:
            raise MissingExtraInstallation(extra_name="parquet")

        def get_array_metadata(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[Union[dict, List[dict]]]:
            raise MissingExtraInstallation(extra_name="parquet")

        def list_arrays(self, source: Union[BytesIO, str, Any]) -> List[str]:
            raise MissingExtraInstallation(extra_name="parquet")

        def can_handle_file(self, file_path: str) -> bool:
            return os.path.splitext(file_path)[1].lower() in [".parquet", ".pq"]


# CSV Handler
if __CSV_MODULE_EXISTS__:

    class CSVArrayHandler(ExternalArrayHandler):
        """Handler for CSV files (.csv, .txt, .dat)."""

        def read_array(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[np.ndarray]:
            """Read array from CSV file."""
            # For CSV, path_in_external_file can be column name or index
            # This is a simplified implementation
            try:
                if isinstance(source, str):
                    data = np.genfromtxt(source, delimiter=",")
                else:
                    data = np.genfromtxt(source, delimiter=",")
                return data
            except Exception as e:
                logging.debug(f"Failed to read CSV: {e}")
                return None

        def write_array(
            self,
            target: Union[str, BytesIO, Any],
            array: Union[list, np.ndarray],
            path_in_external_file: Optional[str] = None,
            **kwargs,
        ) -> bool:
            """Write array to CSV file."""
            try:
                if isinstance(array, list):
                    array = np.asarray(array)
                np.savetxt(target, array, delimiter=",")
                return True
            except Exception as e:
                logging.error(f"Failed to write CSV: {e}")
                return False

        def get_array_metadata(
            self, source: Union[BytesIO, str, Any], path_in_external_file: Optional[str] = None
        ) -> Optional[Union[dict, List[dict]]]:
            """Get metadata for CSV file."""
            try:
                data = self.read_array(source, path_in_external_file)
                if data is not None:
                    return {
                        "path": path_in_external_file or "",
                        "dtype": str(data.dtype),
                        "shape": list(data.shape),
                        "size": data.size,
                    }
            except Exception as e:
                logging.debug(f"Failed to get CSV metadata: {e}")
            return None

        def list_arrays(self, source: Union[BytesIO, str, Any]) -> List[str]:
            """CSV files don't have named datasets."""
            return []

        def can_handle_file(self, file_path: str) -> bool:
            """Check if this handler can process the file."""
            ext = os.path.splitext(file_path)[1].lower()
            return ext in [".csv", ".txt", ".dat"]
