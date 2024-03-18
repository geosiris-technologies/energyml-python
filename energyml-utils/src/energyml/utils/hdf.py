import os
import zipfile
from io import BytesIO
from typing import Optional

import h5py


def write_h5(
    input_h5: str, output_h5: str, h5_datasets: list, overwrite=False
) -> None:
    if len(h5_datasets) > 0:

        if not overwrite and os.path.exists(output_h5):
            print(f"The output file '{output_h5}'allready exists")
            return

        print(f"writing: {output_h5}: Found datasets: {h5_datasets}")

        with h5py.File(output_h5, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])


def write_h5_memory(input_h5: BytesIO, h5_datasets: list) -> Optional[BytesIO]:
    result = None
    # print(h5_datasets)
    if len(h5_datasets) > 0:
        result = BytesIO()
        with h5py.File(result, "w") as f_dest:
            input_h5.seek(0)
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])
        result.seek(0)
    return result


def write_h5_memory_in_local(input_h5: str, h5_datasets: list) -> Optional[BytesIO]:
    result = None
    if len(h5_datasets) > 0:
        result = BytesIO()
        with h5py.File(result, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    try:
                        f_dest.create_dataset(dataset, data=f_src[dataset])
                    except KeyError:
                        print("unable to find data in h5 : ", dataset)

        result.seek(0)
    return result


def find_data_ref_in_xml(xml_content: bytes):
    tree = etree.ElementTree(etree.fromstring(xml_content))
    root = tree.getroot()
    _uuids = root.xpath("@uuid")
    if len(_uuids) <= 0 :
        _uuids = root.xpath("@UUID")

    data_refs = [
        x.text for x in root.xpath("//*[local-name() = 'PathInHdfFile']")
    ] + [
        x.text for x in root.xpath("//*[local-name() = 'PathInExternalFile']")
    ]
    if len(data_refs) > 0:
        return { _uuids[0]: data_refs }
    return None


def find_data_ref_in_epc_or_xml(file_content: BytesIO):
    result = {}

    try:
        with zipfile.ZipFile(file_content) as epc_as_zip:
            for f_name in epc_as_zip.namelist():
                if not f_name.startswith("_rels/") and re.match(
                    FILE_NAME_REGEX, f_name
                ):
                    with epc_as_zip.open(f_name) as myfile:
                        data_ref = find_data_ref_in_xml(myfile.read())
                        if data_ref is not None:
                            result.update(data_ref)
    except zipfile.BadZipFile:
        file_content.seek(0)
        return find_data_ref_in_xml(file_content.read())
    return result


def find_data_ref_in_energyml_files(files_list: list, file_name=None):
    result = {}

    for file in files_list:
        if type(file) is str:
            result.update(find_data_ref_in_xml(str.encode(file)))
        elif type(file) is BytesIO:
            result.update(find_data_ref_in_epc_or_xml(file))
        elif type(file) is bytes:
            result.update(find_data_ref_in_epc_or_xml(BytesIO(file)))

    return result
