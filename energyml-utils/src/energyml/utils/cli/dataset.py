# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""``csv_to_dataset`` — turn the columns of a CSV / DAT file into HDF5 or Parquet datasets."""

from __future__ import annotations

import argparse
import json
import logging
from typing import Dict, List, Optional

from energyml.utils.cli._common import parse_args
from energyml.utils.data.datasets_io import (
    CSVFileReader,
    DATFileReader,
    HDF5FileWriter,
    ParquetFileWriter,
)

logger = logging.getLogger(__name__)

#: Shape of the ``--mapping`` payload, shown in the help of the command.
_MAPPING_SAMPLE = {
    "FINAL_DATASET_NAME_A": ["CSV_COL_NAME_0", "CSV_COL_NAME_N"],
    "FINAL_DATASET_NAME_B": ["CSV_COL_NAME_X"],
}


def _write_mapped_columns(
    writer,
    target,
    columns: Dict[str, List],
    map_col_name_to_csv_col: Optional[Dict[str, List[str]]],
    datasets_prefix: Optional[str],
    ignore: List[str],
    case_insensitive: bool,
) -> None:
    """Write the datasets described by *map_col_name_to_csv_col*, and mark their columns as used.

    *ignore* is updated in place: a column consumed by the mapping must not be written a second
    time under its own name by the caller.
    """
    if not map_col_name_to_csv_col:
        return

    def key(name: str) -> str:
        return name.lower() if case_insensitive else name

    for dataset_name, col_list in map_col_name_to_csv_col.items():
        col_list = [key(c) for c in col_list] if case_insensitive else col_list
        data: List = []
        if len(col_list) > 1:
            for column in col_list:
                if key(column) not in ignore:
                    try:
                        data = data + [columns[column]]
                    except KeyError:
                        logger.warning("Column '%s' is not in the input file — skipped.", column)
                ignore.append(key(column))
            data = list(map(list, zip(*data)))
        else:
            column = col_list[0] if isinstance(col_list, list) else col_list
            data = columns[column]
            ignore.append(key(column))
        try:
            writer.write_array(target, data, (datasets_prefix or "") + dataset_name)
        except ValueError as e:
            logger.warning("Dataset '%s' could not be written: %s", dataset_name, e)


def _write_remaining_columns(writer, target, columns, datasets_prefix, ignore, case_insensitive) -> None:
    """Write one dataset per column that the mapping did not already consume."""
    for header in columns.keys():
        if (header.lower() if case_insensitive else header) in ignore:
            continue
        try:
            writer.write_array(target, columns[header], (datasets_prefix or "") + header)
        except ValueError as e:
            logger.warning("Column '%s' could not be written: %s", header, e)


def dat_to_h5(
    csv_in,
    h5_out,
    dataset_name: Optional[str] = None,
    datasets_prefix: Optional[str] = None,
    ignore: Optional[List[str]] = None,
    map_col_name_to_csv_col: Optional[Dict[str, List[str]]] = None,
    **csvparams,
):
    """
    Write every column of the DAT file *csv_in* as a dataset of the HDF5 file *h5_out*.

    :param csv_in:
    :param h5_out:
    :param dataset_name: if None, csv headers are used
    :param datasets_prefix: prefix prepended to every dataset path
    :param ignore: column names not to write
    :param map_col_name_to_csv_col: ``{dataset_name: [csv_column, ...]}``
    :param csvparams: forwarded to the reader (e.g. ``delimiter``)
    """
    if dataset_name is not None:
        return
    writer = HDF5FileWriter()
    columns = DATFileReader().read_array(csv_in, **csvparams)
    _ignore = [c.lower() for c in (ignore or [])]
    _write_mapped_columns(writer, h5_out, columns, map_col_name_to_csv_col, datasets_prefix, _ignore, True)
    _write_remaining_columns(writer, h5_out, columns, datasets_prefix, _ignore, True)


def csv_to_h5(
    csv_in,
    h5_out,
    dataset_name: Optional[str] = None,
    datasets_prefix: Optional[str] = None,
    ignore: Optional[List[str]] = None,
    map_col_name_to_csv_col: Optional[Dict[str, List[str]]] = None,
    **csvparams,
):
    """
    Write every column of the CSV file *csv_in* as a dataset of the HDF5 file *h5_out*.

    See :func:`dat_to_h5` for the parameters.
    """
    if dataset_name is not None:
        return
    writer = HDF5FileWriter()
    columns = CSVFileReader().read_array_as_panda_dict(csv_in, **csvparams)
    _ignore = list(ignore or [])
    _write_mapped_columns(writer, h5_out, columns, map_col_name_to_csv_col, datasets_prefix, _ignore, False)
    _write_remaining_columns(writer, h5_out, columns, datasets_prefix, _ignore, False)


def csv_to_parquet(
    csv_in,
    parquet_out,
    dataset_name: Optional[str] = None,
    datasets_prefix: Optional[str] = None,
    ignore: Optional[List[str]] = None,
    map_col_name_to_csv_col: Optional[Dict[str, List[str]]] = None,
    **csvparams,
):
    """
    Write every column of the CSV file *csv_in* as a column of the Parquet file *parquet_out*.

    See :func:`dat_to_h5` for the parameters.
    """
    if dataset_name is not None:
        return
    columns = CSVFileReader().read_array_as_panda_dict(csv_in, **csvparams)
    _ignore = list(ignore or [])
    datadict: Dict[str, List] = {}

    # a dict is not a writer, but it exposes what _write_mapped_columns needs
    class _DictWriter:
        @staticmethod
        def write_array(_target, array, path):
            datadict[path] = array

    _write_mapped_columns(_DictWriter, None, columns, map_col_name_to_csv_col, datasets_prefix, _ignore, False)
    _write_remaining_columns(_DictWriter, None, columns, datasets_prefix, _ignore, False)

    keys = list(datadict.keys())
    ParquetFileWriter().write_array(parquet_out, [datadict[k] for k in keys], keys)


def csv_to_dataset(argv: Optional[List[str]] = None) -> None:
    """Entry point of the ``csv_to_dataset`` command."""
    parser = argparse.ArgumentParser(
        prog="csv_to_dataset",
        description="Convert the columns of a CSV file into HDF5 or Parquet datasets. "
        "The output format is chosen from the extension of --output ('.parquet' / '.pqt' for "
        "Parquet, HDF5 otherwise).",
    )
    parser.add_argument("--csv", "-f", type=str, required=True, help="Csv file path")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output file path")
    parser.add_argument("--prefix", "-p", type=str, default="", help="Dataset path prefix")
    parser.add_argument("--csv-delimiter", "-d", type=str, default=",", help="CSV delimiter")
    parser.add_argument(
        "--mapping",
        "-m",
        type=str,
        help=f"Json file path. The json content should look like this : {json.dumps(_MAPPING_SAMPLE)}",
    )
    parser.add_argument(
        "--mapping-line",
        "-ml",
        type=str,
        help=f"A json dict that should look like this : {json.dumps(_MAPPING_SAMPLE)}",
    )
    parser.add_argument("--ignore", "-i", type=str, help="A csv column name to ignore", nargs="+")

    args = parse_args(parser, argv)

    mapping = args.mapping_line or args.mapping
    if mapping is not None:
        mapping = json.loads(mapping)
    logger.debug("delimiter=%r mapping=%s", args.csv_delimiter, mapping)

    output_file_path = args.output
    convert = csv_to_parquet if output_file_path.lower().endswith((".parquet", ".pqt")) else csv_to_h5
    convert(
        args.csv,
        output_file_path,
        datasets_prefix=args.prefix,
        ignore=args.ignore,
        map_col_name_to_csv_col=mapping,
        delimiter=args.csv_delimiter,
    )
    print(f"Datasets written in {output_file_path}")


__all__ = [
    "dat_to_h5",
    "csv_to_h5",
    "csv_to_parquet",
    "csv_to_dataset",
]
