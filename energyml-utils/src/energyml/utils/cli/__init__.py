# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Command line entry points of energyml-utils.

Every console script declared in ``[tool.poetry.scripts]`` points into this package. They used
to live in ``example/tools.py``, which is **not** part of the distribution — the wheel only ships
``energyml/`` — so all ten executables were created by ``pip install`` and every one of them
failed at import with ``ModuleNotFoundError: No module named 'example'``. It went unnoticed in
development because the repository root happens to be on ``sys.path`` there.

============================ ==========================================================
Console script               Function
============================ ==========================================================
``extract_3d``               :func:`~energyml.utils.cli.mesh.extract_representation_in_3d_file`
``csv_to_dataset``           :func:`~energyml.utils.cli.dataset.csv_to_dataset`
``generate_data``            :func:`~energyml.utils.cli.generate.generate_data`
``generate_multiple_data``   :func:`~energyml.utils.cli.generate.generate_multiple_data`
``xml_to_json``              :func:`~energyml.utils.cli.convert.xml_to_json`
``json_to_xml``              :func:`~energyml.utils.cli.convert.json_to_xml`
``json_to_epc``              :func:`~energyml.utils.cli.convert.json_to_epc`
``loadNsave``                :func:`~energyml.utils.cli.convert.load_n_save`
``describe_as_csv``          :func:`~energyml.utils.cli.describe.describe_as_csv`
``validate``                 :func:`~energyml.utils.cli.validate.validate_files`
============================ ==========================================================

Each entry point takes an optional ``argv`` list, so it can be driven from a test or from
another program without going through ``sys.argv``.
"""

from energyml.utils.cli.convert import (
    json_to_epc,
    json_to_xml,
    load_n_save,
    osdu_schema_to_energyml,
    prop_kind_to_json,
    xml_to_json,
)
from energyml.utils.cli.dataset import csv_to_dataset, csv_to_h5, csv_to_parquet, dat_to_h5
from energyml.utils.cli.describe import describe_as_csv
from energyml.utils.cli.generate import generate_data, generate_multiple_data
from energyml.utils.cli.mesh import extract_representation_in_3d_file
from energyml.utils.cli.validate import validate_files

__all__ = [
    # 3-D / GIS export
    "extract_representation_in_3d_file",
    # datasets
    "csv_to_dataset",
    "csv_to_h5",
    "csv_to_parquet",
    "dat_to_h5",
    # generation
    "generate_data",
    "generate_multiple_data",
    # conversions
    "xml_to_json",
    "json_to_xml",
    "json_to_epc",
    "load_n_save",
    "prop_kind_to_json",
    "osdu_schema_to_energyml",
    # description / validation
    "describe_as_csv",
    "validate_files",
]
