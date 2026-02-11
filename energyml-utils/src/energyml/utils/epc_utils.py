# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0


from io import BytesIO
import logging
from typing import Optional, Tuple, Union, Any, List, Dict
from pathlib import Path
import zipfile

from energyml.opc.opc import (
    CoreProperties,
    Relationship,
    TargetMode,
    Created,
    Creator,
    Identifier,
    Types,
    Default,
    Override,
)

from energyml.utils.constants import (
    EPCRelsRelationshipType,
    EpcExportVersion,
    RELS_FOLDER_NAME,
    epoch,
    epoch_to_date,
    extract_uuid_from_string,
    gen_uuid,
    MimeType,
)
from energyml.utils.introspection import (
    get_dor_obj_info,
    get_object_type_for_file_path_from_class,
    is_dor,
    get_class_pkg_version,
    get_obj_version,
    get_obj_uuid,
)
from energyml.utils.manager import get_class_pkg
from energyml.utils.serialization import read_energyml_xml_str, serialize_xml
from energyml.utils.uri import Uri, parse_uri


#     ____  ___  ________  __
#    / __ \/   |/_  __/ / / /
#   / /_/ / /| | / / / /_/ /
#  / ____/ ___ |/ / / __  /
# /_/   /_/  |_/_/ /_/ /_/

EXPANDED_EXPORT_FOLDER_PREFIX = "namespace_"
PATH_VERSION_PREFIX = "version_"


def gen_core_props_rels_path() -> str:
    """
    Generate a path to store the core properties rels file into an epc file
    :return:
    """
    core_path = Path(gen_core_props_path())

    return (core_path.parent / RELS_FOLDER_NAME / f"{core_path.name}.rels").as_posix()


def gen_core_props_path(
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the core properties file into an epc file (depending on the :param:`export_version`)
    :param export_version: the version of the EPC export to use (classic or expanded)
    :return:
    """
    return "docProps/core.xml"


def gen_energyml_object_path(
    energyml_object: Union[str, Uri, Any],
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the :param:`energyml_object` into an epc file (depending on the :param:`export_version`)
    :param energyml_object: can be either an EnergyML object or a string containing the XML representation of an EnergyML object, or a string containing the URI of an EnergyML object, or a Uri object representing an EnergyML object
    :param export_version: the version of the EPC export to use (classic or expanded)
    :return:
    """
    if isinstance(energyml_object, str):
        if energyml_object.startswith("eml:///"):
            energyml_object = parse_uri(energyml_object.strip())
        else:
            energyml_object = read_energyml_xml_str(energyml_object)
    if isinstance(energyml_object, Uri):
        obj_type = energyml_object.object_type
        uuid = energyml_object.uuid
        pkg = energyml_object.domain
        pkg_version = energyml_object.domain_version
        object_version = energyml_object.version
    elif is_dor(energyml_object):
        uuid, pkg, pkg_version, obj_cls, object_version = get_dor_obj_info(energyml_object)
        obj_type = get_object_type_for_file_path_from_class(obj_cls)
    elif isinstance(energyml_object, CoreProperties):
        return gen_core_props_path(export_version)
    else:
        obj_type = get_object_type_for_file_path_from_class(energyml_object.__class__)
        # logging.debug("is_dor: ", str(is_dor(energyml_object)), "object type : " + str(obj_type))
        pkg = get_class_pkg(energyml_object)
        pkg_version = get_class_pkg_version(energyml_object)
        object_version = get_obj_version(energyml_object)
        uuid = get_obj_uuid(energyml_object)

    if not uuid or len(uuid) == 0:
        raise ValueError(f"The object must have a valid uuid to be stored in an epc file - {energyml_object}")
    if not obj_type or len(obj_type) == 0:
        raise ValueError(f"The object must have a valid type to be stored in an epc file - {energyml_object}")
    if not pkg or len(pkg) == 0:
        raise ValueError(f"The object must have a valid package to be stored in an epc file - {energyml_object}")
    if not pkg_version or len(pkg_version) == 0:
        raise ValueError(
            f"The object must have a valid package version to be stored in an epc file - {energyml_object}"
        )

    if export_version == EpcExportVersion.EXPANDED:
        # TODO: verify if we need to add a "/" at the begining of the path or not
        return f"{EXPANDED_EXPORT_FOLDER_PREFIX}{pkg}{pkg_version.replace('.', '')}/{(PATH_VERSION_PREFIX + object_version + '/') if object_version is not None and len(object_version) > 0 else ''}{obj_type}_{uuid}.xml"
    else:
        return obj_type + "_" + uuid + ".xml"


def gen_rels_path(
    energyml_object: Any,
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the :param:`energyml_object` rels file into an epc file
    (depending on the :param:`export_version`)
    :param energyml_object:
    :param export_version:
    :return:
    """
    if isinstance(energyml_object, CoreProperties):
        return gen_core_props_rels_path()
    else:
        obj_path = Path(gen_energyml_object_path(energyml_object, export_version))
        return gen_rels_path_from_obj_path(obj_path=obj_path)


def gen_rels_path_from_obj_path(obj_path: Union[str, Path]) -> str:
    """
    Generate a path to store the rels file into an epc file from the object path
    :param obj_path: the path of the object file (e.g. "namespace_pkg1.0/version_1.0/ObjType_uuid.xml" or "ObjType_uuid.xml")
    :return: the path to store the rels file (e.g. "namespace_pkg1.0/version_1.0/_rels/ObjType_uuid.xml.rels" or "_rels/ObjType_uuid.xml.rels")
    """
    _obj_path = Path(obj_path) if not isinstance(obj_path, Path) else obj_path
    if _obj_path.parent.name == RELS_FOLDER_NAME:
        raise ValueError(f"The object path cannot be in the '{RELS_FOLDER_NAME}' folder")
    return (_obj_path.parent / RELS_FOLDER_NAME / f"{_obj_path.name}.rels").as_posix()


def get_epc_content_type_path(
    # export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the "[Content_Types].xml" file into an epc file
    :return:
    """
    return "[Content_Types].xml"


def extract_uuid_and_version_from_obj_path(obj_path: Union[str, Path]) -> Tuple[str, Optional[str]]:
    """
    Extract the uuid and version of an object from its path in the epc file
    :param obj_path: the path of the object file (e.g. "namespace_pkg1.0/version_1.0/ObjType_uuid.xml" or "ObjType_uuid.xml")
    :return: a tuple containing the uuid and version of the object
    """
    _obj_path = Path(obj_path) if not isinstance(obj_path, Path) else obj_path

    uuid_match = extract_uuid_from_string(str(_obj_path))
    if uuid_match is None:
        raise ValueError(f"Cannot extract uuid from object path: {obj_path}")

    # If this data object is versioned, the unique path should contain a directory called 'version_id' (where id is the identifier for the data object version).
    version = None
    for part in _obj_path.parts:
        if part.startswith(PATH_VERSION_PREFIX):
            version = part[len(PATH_VERSION_PREFIX) :]

    return uuid_match, version


#     __  ____________ ______
#    /  |/  /  _/ ___// ____/
#   / /|_/ // / \__ \/ /
#  / /  / // / ___/ / /___
# /_/  /_/___//____/\____/


def create_h5_external_relationship(h5_path: str, current_idx: int = 0) -> Relationship:
    """
    Create a Relationship object to link an external HDF5 file.
    :param h5_path:
    :return:
    """
    return Relationship(
        target=h5_path,
        type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
        id=f"Hdf5File{current_idx + 1 if current_idx > 0 else ''}",
        target_mode=TargetMode.EXTERNAL,
    )


def create_default_core_properties(creator: Optional[str] = None) -> CoreProperties:
    """Create default Core Properties object."""
    return CoreProperties(
        created=Created(any_element=epoch_to_date(epoch())),
        creator=Creator(any_element=creator or "energyml-utils python module (Geosiris)"),
        identifier=Identifier(any_element=f"urn:uuid:{gen_uuid()}"),
        version="1.0",
    )


def create_default_types() -> Types:
    """Create default Types object."""
    return Types(
        default=[Default(extension="rels", content_type=str(MimeType.RELS))],
        override=[Override(content_type=str(MimeType.CORE_PROPERTIES), part_name=gen_core_props_path())],
    )


#  _    __      ___     __      __  _
# | |  / /___ _/ (_)___/ /___ _/ /_(_)___  ____
# | | / / __ `/ / / __  / __ `/ __/ / __ \/ __ \
# | |/ / /_/ / / / /_/ / /_/ / /_/ / /_/ / / / /
# |___/\__,_/_/_/\__,_/\__,_/\__/_/\____/_/ /_/


def valdiate_basic_epc_structure(epc: Union[str, Path, zipfile.ZipFile, BytesIO]) -> bool:
    should_close = False
    if isinstance(epc, (str, Path)):
        epc_io = zipfile.ZipFile(epc, "r")
        should_close = True
    elif isinstance(epc, BytesIO):
        epc_io = zipfile.ZipFile(epc, "r")
        should_close = True
    elif isinstance(epc, zipfile.ZipFile):
        epc_io = epc
    else:
        raise ValueError("The epc parameter must be a string, a Path, a ZipFile or a BytesIO object")

    # Check if the EPC file contains the required files: [Content_Types].xml, _rels/.rels and docProps/core.xml
    required_files = {
        get_epc_content_type_path(),
        gen_core_props_rels_path(),
        gen_core_props_path(),
    }

    try:
        epc_files = set(epc_io.namelist())
        missing_files = required_files - epc_files
        if missing_files:
            logging.warning(f"The EPC file is missing the following required files: {missing_files}")
            return False
    finally:
        if should_close:
            epc_io.close()

    return True


def create_mandatory_structure_epc(epc: Union[str, Path, zipfile.ZipFile, BytesIO]) -> None:
    # Create a zip file with the minimal structure of an EPC file, including [Content_Types].xml and _rels/.rels and core properties
    should_close = False
    if isinstance(epc, (str, Path)):
        epc_io = zipfile.ZipFile(epc, "a", zipfile.ZIP_DEFLATED)
        should_close = True
    elif isinstance(epc, BytesIO):
        epc_io = zipfile.ZipFile(epc, "a", zipfile.ZIP_DEFLATED)
        should_close = True
    elif isinstance(epc, zipfile.ZipFile):
        if epc.mode == "r":
            raise ValueError("Cannot write to a read-only ZipFile. Open it in 'a' or 'w' mode.")
        epc_io = epc
    else:
        raise ValueError("The epc parameter must be a string, a Path, a ZipFile or a BytesIO object")

    core_props = create_default_core_properties()
    empty_epc_structure = {
        get_epc_content_type_path(): serialize_xml(Types()),
        gen_core_props_rels_path(): serialize_xml(Relationship()),
        gen_core_props_path(): serialize_xml(core_props),
    }

    # print(f"Current files in the EPC: {epc_io.namelist()}")
    # print(f"Potential created files: {list(empty_epc_structure.keys())}")
    try:
        for path, content in empty_epc_structure.items():
            if path not in epc_io.namelist():
                epc_io.writestr(path, content)
    finally:
        if should_close:
            epc_io.close()


def repair_epc_structure_if_not_valid(epc: Union[str, Path, zipfile.ZipFile, BytesIO]) -> None:
    if not valdiate_basic_epc_structure(epc):
        logging.warning("EPC structure validation failed. Attempting auto-repair.")
        create_mandatory_structure_epc(epc)
