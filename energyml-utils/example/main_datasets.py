# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from src.energyml.utils.data.datasets_io import (
    ParquetFileReader,
    ParquetFileWriter,
    CSVFileReader,
    CSVFileWriter,
    read_dataset,
)
from utils.data.helper import read_array
from utils.introspection import search_attribute_matching_name_with_path
from utils.serialization import read_energyml_xml_file


def local_parquet():
    pr = ParquetFileReader()
    pw = ParquetFileWriter()

    print(pr.read_array("../wip/sample1.parquet", "column0"))
    print(pr.read_array("../wip/sample1.parquet", "column0")[0])
    print(len(pr.read_array("../wip/sample1.parquet", "column0")))
    print(pr.get_array_dimension("../wip/sample1.parquet", "column0"))

    print(pw.write_array("../wip/export.parquet", [[1, 2, 3], [2, 2, 2]]))
    print(pr.read_array("../wip/export.parquet"))
    print(pw.write_array("../wip/export_matrice.parquet", [[[1, 6, 6], [2, 9, 9], [3, 10, 10]], [2, 2, 2]]))
    print(pr.read_array("../wip/export_matrice.parquet"))


def local_csv():
    csvr = CSVFileReader()
    csvw = CSVFileWriter()
    csv_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/Export_of_database.csv"
    print(csvr.read_array(csv_path, "0"))
    print(csvr.read_array(csv_path, "Line", has_headers=True))
    print(csvr.read_array(csv_path, None, has_headers=True))

    with open(csv_path, "r") as csv_file:
        print(csvr.read_array(csv_file, "Line", has_headers=True))
    with open(csv_path, "rb") as csv_file:
        print(csvr.read_array(csv_file, "Line", has_headers=True))
    with open(csv_path, "rb") as csv_file:
        print(csvr.read_array(csv_file, "1", has_headers=False))

    csv_test_path = "../wip/data/export.csv"
    csvw.write_array(csv_test_path, [[1, 2, 3], [2, 2, 2]])
    print(csvr.read_array(csv_test_path))

    print("# DAT")
    dat_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/NT66-AGG-DAtA.truncated.dat"
    with open(dat_path, "r") as dat_file:
        print(csvr.read_array(dat_file, None, delimiter=" ", has_headers=False, skipinitialspace=True)[0])
        dat_file.seek(0)
        print(csvr.read_array(dat_file, "1", delimiter=" ", has_headers=False, skipinitialspace=True))

    print("# DAT shetland-horizon_Truncated")
    dat_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/test_ColumnBaseTable_parquet_hdf5/shetland-horizon_Truncated.dat"
    with open(dat_path, "r") as dat_file:
        print(csvr.read_array(dat_file, None, delimiter=",", has_headers=False)[0])
        dat_file.seek(0)
        print(csvr.read_array(dat_file, "1", delimiter=",", has_headers=False))

    print("# Global function call")
    print(read_dataset(dat_path, "0", None))
    print(read_dataset(dat_path, None, None))

    print(csvr.read_array_as_panda_dict(csv_path))
    print(csvr.read_array_as_panda_dict(csv_path)["Line"])
    print(csvr.read_array_as_panda_dict(dat_path, has_header=False))


def local_cs_in_polyline_rep():
    poly = read_energyml_xml_file("../rc/polyline_set_for_array_tests_with_csv.xml")
    for array_path, array_value in search_attribute_matching_name_with_path(
        poly, r"LinePatch.\d+.NodeCountPerPolyline"
    ):
        if array_value is not None:
            print(f"{array_path}\n\t{array_value}")
            try:
                val = read_array(
                    energyml_array=array_value,
                    root_obj=poly,
                    path_in_root=array_path,
                    workspace=None,
                )
                print(f"{type(array_value)} \n\t{val}")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    # local_parquet()
    local_csv()
    # local_cs_in_polyline_rep()
