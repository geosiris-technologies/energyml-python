import os

from src.energyml.utils.data.mesh import *
from src.energyml.utils.data.hdf import *


def test_off():
    print("hello")
    indices = [
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3],
    ]

    print(sum(list(map(lambda x: len(x), indices))))

    points = [
        [0., 0., 0.],
        [1., 0., 0.],
        [0., 1., 0.],
        [1., 1., 0.],
    ]

    indices = [
        [0, 1, 3],
        [0, 3, 2],
    ]

    off_file = export_off(points, indices)

    print(off_file.getvalue())

    tmp_folder = "../../../#data/tmp"
    print(os.listdir(tmp_folder))

    try:
        os.mkdir(tmp_folder)
    except Exception as e:
        print(e)

    with open(f"{tmp_folder}/hdf-test0.off", "wb") as f:
        f.write(off_file.getvalue())


if __name__ == "__main__":
    # test_off()

    hdf5filereader = HDF5FileReader()

    hdf5filereader.read_array("../../../#data/Volve_Horizons_and_Faults_Depth_originEQN_Plus.h5", "/RESQML/d9b95bb5-019d-4341-bcf6-df392338187f/points_patch0")
    print(hdf5filereader.get_array_dimension("../../../#data/Volve_Horizons_and_Faults_Depth_originEQN_Plus.h5", "/RESQML/d9b95bb5-019d-4341-bcf6-df392338187f/points_patch0"))
    # print(hdf5filereader.read_array("../../../#data/Volve_Horizons_and_Faults_Depth_originEQN_Plus.h5", "/RESQML/d9b95bb5-019d-4341-bcf6-df392338187f/points_patch0"))
