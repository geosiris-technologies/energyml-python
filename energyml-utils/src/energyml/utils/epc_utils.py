# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0


from io import BytesIO
import json
import logging
import os
import os
from typing import Optional, Set, Tuple, Union, Any, List, Dict, Callable
from pathlib import Path
import zipfile

from energyml.opc.opc import (
    CoreProperties,
    Relationship,
    Relationships,
    TargetMode,
    Created,
    Creator,
    Identifier,
    Types,
    Default,
    Override,
)

from energyml.utils.exception import NotEnoughInformationError

from energyml.utils.constants import (
    CORE_PROPERTIES_FOLDER_NAME,
    EPCRelsRelationshipType,
    EpcExportVersion,
    RELS_FOLDER_NAME,
    epoch,
    epoch_to_date,
    extract_uuid_from_string,
    file_extension_to_mime_type,
    gen_uuid,
    MimeType,
    OptimizedRegex,
    split_identifier,
    content_type_to_qualified_type,
    qualified_type_to_content_type,
    get_property_kind_dict_path_as_dict,
)
from energyml.utils.introspection import (
    get_direct_dor_list,
    get_obj_uri,
    get_dor_obj_info,
    get_object_type_for_file_path_from_class,
    is_dor,
    get_class_pkg_version,
    get_obj_version,
    get_obj_uuid,
    get_obj_identifier,
    get_object_attribute,
    search_attribute_matching_type,
    get_class_from_qualified_type,
    set_attribute_from_path,
    set_attribute_value,
    get_obj_attribute_class,
    copy_attributes,
    get_content_type_from_class,
    get_qualified_type_from_class,
)
from energyml.utils.manager import get_class_pkg
from energyml.utils.serialization import read_energyml_xml_str, serialize_xml, read_energyml_json_str
from energyml.utils.uri import Uri, parse_uri
from energyml.utils.storage_interface import ResourceMetadata

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


def is_core_prop_or_extension_path(path: Union[str, Path]) -> bool:
    """
    Check if the given path is the one for core properties or its rels file in an epc file
    :param path:
    :return:
    """
    _path = Path(path) if not isinstance(path, Path) else path
    return (
        _path.as_posix() == gen_core_props_path()
        or _path.as_posix() == gen_core_props_rels_path()
        or _path.as_posix().startswith(f"/{CORE_PROPERTIES_FOLDER_NAME}/")
        or _path.as_posix().startswith(f"{CORE_PROPERTIES_FOLDER_NAME}/")
    )


def gen_core_props_path(
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the core properties file into an epc file (depending on the :param:`export_version`)
    :param export_version: the version of the EPC export to use (classic or expanded)
    :return:
    """
    return f"{CORE_PROPERTIES_FOLDER_NAME}/core.xml"


def gen_energyml_object_path(
    energyml_object: Union[str, Uri, Any],
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the :param:`energyml_object` into an epc file (depending on the :param:`export_version`)
    :param energyml_object: can be either an EnergyML object or a string containing the XML representation of an EnergyML object, or a string containing the URI of an EnergyML object, or a Uri object representing an EnergyML object, or even a DOR object.
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
    elif isinstance(energyml_object, Types):
        return get_epc_content_type_path()
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
    elif isinstance(energyml_object, Types):
        return get_epc_content_type_rels_path()
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


def get_epc_content_type_rels_path() -> str:
    """Generate a path to store the rels file for "[Content_Types].xml" into an epc file :return:"""
    return f"{RELS_FOLDER_NAME}/.rels"


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


def in_epc_file_path_to_mime_type(path: str) -> Optional[str]:
    """Infer MIME type from in-EPC file path"""
    if not path:
        return None

    # Check for specific EPC file types first
    if path.endswith("rels"):
        return MimeType.RELS.value
    elif path in (gen_core_props_path(), f"/{gen_core_props_path()}"):
        return MimeType.CORE_PROPERTIES.value
    elif path.startswith((f"/{CORE_PROPERTIES_FOLDER_NAME}/", f"{CORE_PROPERTIES_FOLDER_NAME}/")):
        return MimeType.EXTENDED_CORE_PROPERTIES.value

    # Fallback to inferring from file extension
    ext = path.split(".")[-1]
    return file_extension_to_mime_type(ext)


def get_file_folder(path) -> Optional[str]:
    """Get the folder path from a given file path."""
    if path is None:
        return None
    _path = Path(path) if not isinstance(path, Path) else path
    return _path.parent.as_posix() if _path.parent != Path(".") else ""


def make_path_relative_to_other_file(path: str, ref_path: Optional[Union[str, Path]]) -> str:
    # make the relative path absolute regarding to the epc file path
    if ref_path is not None:
        if isinstance(ref_path, (str, Path)):
            epc_folder = get_file_folder(ref_path) or ""
            if not os.path.isabs(path):
                return os.path.normpath(os.path.join(epc_folder, path))
            else:
                return path
    else:
        return path


def make_path_relative_to_filepath_list(paths: List[str], ref_path: Optional[Union[str, Path]] = None) -> List[str]:
    return [make_path_relative_to_other_file(path, ref_path) for path in paths]


#     __  ____________ ______
#    /  |/  /  _/ ___// ____/
#   / /|_/ // / \__ \/ /
#  / /  / // / ___/ / /___
# /_/  /_/___//____/\____/


def as_identifier(identifier: Union[str, Uri, Any]) -> Optional[str]:
    if identifier is None:
        return None
    elif isinstance(identifier, str):
        if identifier.startswith("eml:///"):
            return as_identifier(parse_uri(identifier))
        if OptimizedRegex.UUID.fullmatch(identifier) is not None:
            raise NotEnoughInformationError(
                "Simple uuid is not enough to be used as an identifier, please provide a full URI or an object with a valid URI or identifier that contains the version : 'UUID.VERSION' even if VERSION can be an empty string"
            )
        else:
            return identifier
    elif isinstance(identifier, Uri):
        return identifier.as_identifier()
    elif isinstance(identifier, ResourceMetadata):
        return as_identifier(identifier.identifier)
    elif hasattr(identifier, "uri"):  # EpcObjectMetadata
        return as_identifier(identifier.uri)
    else:
        # Try to get URI from object
        obj_uri = get_obj_uri(obj=identifier, dataspace=None)
        if obj_uri is not None:
            return obj_uri.as_identifier()
        return str(identifier)


def create_external_relationship(path: str, _id: Optional[str] = None) -> Relationship:
    return Relationship(
        target=path,
        type_value=str(EPCRelsRelationshipType.EXTERNAL_RESOURCE),
        target_mode=TargetMode.EXTERNAL,
        id=_id or f"_ext_{gen_uuid()}",
    )


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


def relationships_equal(rel1: Relationship, rel2: Relationship) -> bool:
    """
    Compare two Relationship objects for equality based on their target and type_value.

    Two relationships are considered equal if they have:
    - The same target (destination path)
    - The same type_value (relationship type)

    Note: The id field is NOT compared as it's typically auto-generated and
    doesn't affect the semantic meaning of the relationship.

    :param rel1: First Relationship object
    :param rel2: Second Relationship object
    :return: True if relationships are semantically equal, False otherwise

    Example:
        >>> rel1 = Relationship(target="obj.xml", type_value="destinationObject", id="_1")
        >>> rel2 = Relationship(target="obj.xml", type_value="destinationObject", id="_2")
        >>> relationships_equal(rel1, rel2)  # True (different IDs don't matter)
    """
    return rel1.target == rel2.target and rel1.type_value == rel2.type_value


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
        override=[
            Override(content_type=str(MimeType.CORE_PROPERTIES), part_name=gen_core_props_path()),
        ],
    )


def match_external_proxy_type(obj_or_path_or_type: Union[str, Uri, Any]) -> bool:
    """Check if the given object, path or type string matches the pattern of an external proxy reference."""
    if isinstance(obj_or_path_or_type, str):
        # for a classname, a filepath or a content-type, we check if it contains "external" and "reference"
        obj_or_path_or_type_lw = obj_or_path_or_type.lower()
        return "external" in obj_or_path_or_type_lw and "reference" in obj_or_path_or_type_lw
    elif isinstance(obj_or_path_or_type, Uri):
        return match_external_proxy_type(obj_or_path_or_type.get_qualified_type())
    else:
        return match_external_proxy_type(str(type(obj_or_path_or_type)))


def get_rels_dor_type(dor_target: Union[str, Uri, Any], in_dor_owner_rels_file: bool) -> str:
    """
    Determine the appropriate EPC relationship type for a DOR based on its target and rels file context.

    :param dor_target: The target object/type that the DOR references. Can be a string (qualified type),
                       a Uri object, or an EnergyML object. Used to determine if it's an external proxy.
    :param in_dor_owner_rels_file: Boolean indicating which rels file perspective:
                                    - True: We're in the rels file of the object that OWNS/CONTAINS the DOR
                                    - False: We're in the rels file of the object that is TARGETED by the DOR
    :return: The appropriate EPCRelsRelationshipType as a string for the relationship

    The function handles four scenarios:
    - External proxy from owner's perspective -> ML_TO_EXTERNAL_PART_PROXY
    - External proxy from target's perspective -> EXTERNAL_PART_PROXY_TO_ML
    - Regular object from owner's perspective -> DESTINATION_OBJECT
    - Regular object from target's perspective -> SOURCE_OBJECT
    """
    if match_external_proxy_type(dor_target):
        if in_dor_owner_rels_file:
            # in the rels file of the Representation that points to the proxy
            return str(EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY)
        else:
            # in the EpcExternalPartReference rels file
            return str(EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML)
    else:
        if in_dor_owner_rels_file:
            # in the rels file of the object that contains the DOR
            return str(EPCRelsRelationshipType.DESTINATION_OBJECT)
        else:
            # in the DOR target rels file
            return str(EPCRelsRelationshipType.SOURCE_OBJECT)


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
        get_epc_content_type_rels_path(),
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
        gen_core_props_rels_path(): serialize_xml(Relationships()),
        gen_core_props_path(): serialize_xml(core_props),
        get_epc_content_type_rels_path(): serialize_xml(
            Relationships(
                relationship=[
                    Relationship(
                        id="CoreProperties",
                        type_value=str(EPCRelsRelationshipType.CORE_PROPERTIES),
                        target=gen_core_props_path(),
                    )
                ]
            )
        ),
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


#     ____                            __          __ __ _           __
#    / __ \_________  ____  ___  ____/ /___  __   / //_/(_)___  ____/ /____
#   / /_/ / ___/ __ \/ __ \/ _ \/ __  / __ \/ /  / ,<  / / __ \/ __  / ___/
#  / ____/ /  / /_/ / /_/ /  __/ /_/ / /_/ / /  / /| |/ / / / / /_/ (__  )
# /_/   /_/   \____/ .___/\___/\__,_/\__, /_/  /_/ |_/_/_/ /_/\__,_/____/
#                 /_/                /____/

"""
PropertyKind list: a list of Pre-defined properties
"""
__CACHE_PROP_KIND_DICT__ = {}


def update_prop_kind_dict_cache():
    """Update the property kind dictionary cache from the standard property kinds file."""
    prop_kind = get_property_kind_dict_path_as_dict()

    for prop in prop_kind["PropertyKind"]:
        __CACHE_PROP_KIND_DICT__[prop["Uuid"]] = read_energyml_json_str(json.dumps(prop))[0]


def get_property_kind_by_uuid(uuid: str) -> Optional[Any]:
    """
    Get a property kind by its uuid.
    :param uuid: the uuid of the property kind
    :return: the property kind or None if not found
    """
    if len(__CACHE_PROP_KIND_DICT__) == 0:
        # update the cache to check if it is a
        try:
            update_prop_kind_dict_cache()
        except FileNotFoundError as e:
            logging.error(f"Failed to parse propertykind dict {e}")
    return __CACHE_PROP_KIND_DICT__.get(uuid, None)


def get_property_kind_and_parents(uuids: list) -> Dict[str, Any]:
    """Get PropertyKind objects and their parents from a list of UUIDs.

    Args:
        uuids (list): List of PropertyKind UUIDs.

    Returns:
        Dict[str, Any]: A dictionary mapping UUIDs to PropertyKind objects and their parents.
    """
    dict_props: Dict[str, Any] = {}

    for prop_uuid in uuids:
        prop = get_property_kind_by_uuid(prop_uuid)
        if prop is not None:
            dict_props[prop_uuid] = prop
            parent_uuid = get_object_attribute(prop, "parent.uuid")
            if parent_uuid is not None and parent_uuid not in dict_props:
                dict_props = get_property_kind_and_parents([parent_uuid]) | dict_props
        else:
            logging.warning(f"PropertyKind with UUID {prop_uuid} not found.")
            continue
    return dict_props


#     ____  ____  ____     ______                 __  _
#    / __ \/ __ \/ __ \   / ____/_______  ____ _/ /_(_)___  ____
#   / / / / / / / /_/ /  / /   / ___/ _ \/ __ `/ __/ / __ \/ __ \
#  / /_/ / /_/ / _, _/  / /___/ /  /  __/ /_/ / /_/ / /_/ / / / /
# /_____/\____/_/ |_|   \____/_/   \___/\__,_/\__/_/\____/_/ /_/


def as_dor(obj_or_identifier: Union[str, Uri, Any], dor_qualified_type: str = "eml23.DataObjectReference"):
    """
    Create a DOR (Data Object Reference) from an object to target the latter.
    :param obj_or_identifier: an energyml object, identifier string, or URI
    :param dor_qualified_type: the qualified type of the DOR (e.g. "eml23.DataObjectReference" is the default value)
    :return: a DOR object
    """
    if obj_or_identifier is None:
        return None

    cls = get_class_from_qualified_type(dor_qualified_type)
    dor = cls()

    # Variables to collect data from different sources
    dor_uuid = None
    dor_title = None
    dor_version = None
    dor_qualified_type_str = None
    dor_content_type_str = None
    dor_energistics_uri = None

    if isinstance(obj_or_identifier, str) or isinstance(obj_or_identifier, Uri):  # is an identifier or uri
        parsed_uri = obj_or_identifier if isinstance(obj_or_identifier, Uri) else parse_uri(obj_or_identifier)
        if parsed_uri is not None:
            # From URI
            logging.debug(f"====> parsed uri {parsed_uri} : uuid is {parsed_uri.uuid}")
            dor_uuid = parsed_uri.uuid
            dor_version = parsed_uri.version
            dor_qualified_type_str = parsed_uri.get_qualified_type()
            dor_content_type_str = qualified_type_to_content_type(parsed_uri.get_qualified_type())
            dor_energistics_uri = str(obj_or_identifier)
        elif isinstance(obj_or_identifier, str):  # identifier
            if len(__CACHE_PROP_KIND_DICT__) == 0:
                try:
                    update_prop_kind_dict_cache()
                except FileNotFoundError as e:
                    logging.error(f"Failed to parse propertykind dict {e}")
            try:
                uuid, version = split_identifier(obj_or_identifier)
                if uuid in __CACHE_PROP_KIND_DICT__:
                    return as_dor(__CACHE_PROP_KIND_DICT__[uuid], dor_qualified_type)
                else:
                    dor_uuid = uuid
                    dor_version = version
            except AttributeError:
                logging.error(f"Failed to parse identifier {obj_or_identifier}. DOR will be empty")
    else:
        if is_dor(obj_or_identifier):
            # DOR conversion
            if hasattr(obj_or_identifier, "qualified_type"):
                dor_qualified_type_str = get_object_attribute(obj_or_identifier, "qualified_type")
            elif hasattr(obj_or_identifier, "content_type"):
                dor_qualified_type_str = content_type_to_qualified_type(
                    get_object_attribute(obj_or_identifier, "content_type")
                )

            if hasattr(obj_or_identifier, "qualified_type"):
                dor_content_type_str = qualified_type_to_content_type(
                    get_object_attribute(obj_or_identifier, "qualified_type")
                )
            elif hasattr(obj_or_identifier, "content_type"):
                dor_content_type_str = get_object_attribute(obj_or_identifier, "content_type")

            dor_title = get_object_attribute(obj_or_identifier, "Title")
            dor_uuid = get_obj_uuid(obj_or_identifier)
            dor_version = get_obj_version(obj_or_identifier)
        else:
            # For etp Resource object
            if hasattr(obj_or_identifier, "uri"):
                dor = as_dor(obj_or_identifier.uri, dor_qualified_type)
                if hasattr(obj_or_identifier, "name") and hasattr(dor, "title"):
                    setattr(dor, "title", getattr(obj_or_identifier, "name"))
                return dor
            else:
                # Regular EnergyML object
                try:
                    dor_qualified_type_str = get_qualified_type_from_class(obj_or_identifier)
                except Exception as e:
                    logging.error(f"Failed to set qualified_type for DOR {e}")

                try:
                    dor_content_type_str = get_content_type_from_class(obj_or_identifier)
                except Exception as e:
                    logging.error(f"Failed to set content_type for DOR {e}")

                dor_title = get_object_attribute(obj_or_identifier, "Citation.Title")
                dor_uuid = get_obj_uuid(obj_or_identifier)
                dor_version = get_obj_version(obj_or_identifier)

    # Unified attribute setting section - applies collected data to DOR
    if dor_qualified_type_str and hasattr(dor, "qualified_type"):
        dor.qualified_type = dor_qualified_type_str

    if dor_content_type_str and hasattr(dor, "content_type"):
        dor.content_type = dor_content_type_str

    if dor_title and hasattr(dor, "title"):
        setattr(dor, "title", dor_title)

    if dor_uuid:
        if hasattr(dor, "uuid"):
            setattr(dor, "uuid", dor_uuid)
        if hasattr(dor, "uid"):
            setattr(dor, "uid", dor_uuid)

    if dor_version:
        if hasattr(dor, "object_version"):
            setattr(dor, "object_version", dor_version)
        if hasattr(dor, "version_string"):
            setattr(dor, "version_string", dor_version)

    if dor_energistics_uri and hasattr(dor, "energistics_uri"):
        setattr(dor, "energistics_uri", dor_energistics_uri)

    return dor


#     ____  __     _           __     ______                 __  _
#    / __ \/ /_   (_)__  _____/ /_   / ____/_______  ____ _/ /_(_)___  ____
#   / / / / __ \ / / _ \/ ___/ __/  / /   / ___/ _ \/ __ `/ __/ / __ \/ __ \
#  / /_/ / /_/ // /  __/ /__/ /_   / /___/ /  /  __/ /_/ / /_/ / /_/ / / / /
#  \____/_.___// /\___/\___/\__/   \____/_/   \___/\__,_/\__/_/\____/_/ /_/
#            /___/


def create_energyml_object(
    content_or_qualified_type: str,
    citation: Optional[Any] = None,
    uuid: Optional[str] = None,
):
    """
    Create an energyml object instance depending on the content-type or qualified-type given in parameter.
    The SchemaVersion is automatically assigned.
    If no citation is given default one will be used.
    If no uuid is given, a random uuid will be used.
    :param content_or_qualified_type:
    :param citation:
    :param uuid:
    :return:
    """
    if citation is None:
        citation = {
            "title": "New_Object",
            "Creation": epoch_to_date(epoch()),
            "LastUpdate": epoch_to_date(epoch()),
            "Format": "energyml-utils",
            "Originator": "energyml-utils python module",
        }
    cls = get_class_from_qualified_type(content_or_qualified_type)
    obj = cls()
    cit = get_obj_attribute_class(cls, "citation")()
    copy_attributes(
        obj_in=citation,
        obj_out=cit,
        only_existing_attributes=True,
        ignore_case=True,
    )
    set_attribute_from_path(obj, "citation", cit)
    set_attribute_value(obj, "uuid", uuid or gen_uuid())
    set_attribute_value(obj, "SchemaVersion", get_class_pkg_version(obj))

    return obj


def create_external_part_reference(
    eml_version: str,
    h5_file_path: str,
    citation: Optional[Any] = None,
    uuid: Optional[str] = None,
):
    """
    Create an EpcExternalPartReference depending on the energyml version (should be ["2.0", "2.1", "2.2"]).
    The MimeType, ExistenceKind and Filename will be automatically filled.
    :param eml_version:
    :param h5_file_path:
    :param citation:
    :param uuid:
    :return:
    """
    version_flat = OptimizedRegex.DOMAIN_VERSION.findall(eml_version)[0][0].replace(".", "").replace("_", "")
    obj = create_energyml_object(
        content_or_qualified_type="eml" + version_flat + ".EpcExternalPartReference",
        citation=citation,
        uuid=uuid,
    )
    set_attribute_value(obj, "MimeType", MimeType.HDF5.value)
    set_attribute_value(obj, "ExistenceKind", "Actual")
    set_attribute_value(obj, "Filename", h5_file_path)

    return obj


#     ____       __      __  _                __    _
#    / __ \___  / /___ _/ /_(_)___  ____  ___/ /_  (_)___  _____
#   / /_/ / _ \/ / __ `/ __/ / __ \/ __ \/ __  / / / / __ \/ ___/
#  / _, _/  __/ / /_/ / /_/ / /_/ / / / / /_/ / /_/ / /_/ (__  )
# /_/ |_|\___/_/\__,_/\__/_/\____/_/ /_/\__,_/\__,_/ .___/____/
#                                                  /_/


def get_reverse_dor_list(obj_list: List[Any], key_func: Callable = get_obj_identifier) -> Dict[str, List[Any]]:
    """
    Compute a dict with 'OBJ_UUID.OBJ_VERSION' as Key, and list of DOR that reference it.
    If the object version is None, key is 'OBJ_UUID.'
    :param obj_list:
    :param key_func: a callable to create the key of the dict from the object instance
    :return: str
    """
    rels = {}
    for obj in obj_list:
        for dor in search_attribute_matching_type(obj, "DataObjectReference", return_self=False):
            key = key_func(dor)
            if key not in rels:
                rels[key] = []
            rels[key] = rels.get(key, []) + [obj]
    return rels


def get_dor_uris_from_obj(obj: Any) -> Set[Uri]:
    """Get uri of all Data Object References (DORs) directly referenced by the given object."""
    uri_set = set()
    try:
        dor_list = get_direct_dor_list(obj)
        for dor in dor_list:
            try:
                uri = get_obj_uri(dor)
                if uri and uri.is_object_uri():
                    uri_set.add(uri)
            except Exception as e:
                logging.warning(f"Failed to extract uri from DOR: {e}")
    except Exception as e:
        logging.warning(f"Failed to get DOR list from object: {e}")
    return uri_set


def get_dor_or_external_uris_from_obj(obj: Any) -> Tuple[Set[Uri], Set[Tuple[str, str]]]:
    """
    Extract all URIs from Data Object References (DORs) and external data references in an EnergyML object.

    This function performs a comprehensive scan of an EnergyML object to find:
    1. **Data Object References (DORs)**: Internal references to other EnergyML objects within the EPC
       (e.g., a TriangulatedSetRepresentation pointing to a HorizonInterpretation)
    2. **External Data References**: References to external data files, typically HDF5 arrays
       (e.g., ExternalDataArrayPart.uri for array storage outside the EPC)

    Unlike `get_dor_uris_from_obj()` which only returns DORs, this function captures both internal
    object references AND external file references, making it suitable for complete dependency analysis.

    :param obj: Any EnergyML object (e.g., Representation, Property, Interpretation, etc.)
                The function will recursively search all attributes matching DOR or external reference patterns.

    :return: A tuple containing:
             - A set of URIs for all DORs found (internal references to other EnergyML objects)
             - A set of tuples for external references, where each tuple contains (external URI, MIME type)

    :raises: Does not raise exceptions. Logs warnings for any extraction failures and continues processing.

    Example:
        >>> from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation
        >>> trset = load_triangulated_set()  # Has DOR to interpretation + external HDF5 arrays
        >>> dor_uris, external_uris = get_dor_or_external_uris_from_obj(trset)
        >>> for uri in dor_uris:
        ...     print(f"Internal reference: {uri}")
        >>> for ext_uri, mime_type in external_uris:
        ...     print(f"External file: {ext_uri} (type: {mime_type})")

        ...         print(f"Internal reference: {uri}")
        ...     else:
        ...         print(f"External file: {uri[0]} (type: {uri[1]})")
        Internal reference: eml:///resqml22.HorizonInterpretation(abc-123-def)
        External file: my_hdf5_file.h5 (type: application/x-hdf5)

    Note:
        - The search pattern matches both 'DataObjectReference' and 'ExternalDataArrayPart' types
        - DORs are identified by having 'uid' or 'uuid' attributes
        - External references are identified by having 'uri' and optionally 'mime_type' attributes
        - For complete relationship analysis including reverse relationships, use EpcRelsCache instead

    See Also:
        - `get_dor_uris_from_obj()`: Similar function but only returns internal DOR references
        - `get_direct_dor_list()`: Returns the actual DOR objects rather than their URIs
    """
    dor_uris = set()
    external_uris = set()
    try:
        dor_list = search_attribute_matching_type(obj, "DataObjectReference|ExternalDataArrayPart")
        for dor_or_ext in dor_list:
            if hasattr(dor_or_ext, "uid") or hasattr(dor_or_ext, "uuid"):
                # DOR case
                try:
                    uri = get_obj_uri(dor_or_ext)
                    if uri and uri.is_object_uri():
                        dor_uris.add(uri)
                except Exception as e:
                    logging.warning(f"Failed to extract uri from DOR: {e}")
            else:
                # External reference case (e.g. ExternalDataArrayPart)
                try:
                    ext_uri = getattr(dor_or_ext, "uri", None)
                    ext_mime_type = getattr(dor_or_ext, "mime_type", None)
                    if ext_uri:
                        external_uris.add((ext_uri, ext_mime_type))
                except Exception as e:
                    logging.warning(f"Failed to extract uri from external reference: {e}")
    except Exception as e:
        logging.warning(f"Failed to get DOR list from object: {e}")
    return dor_uris, external_uris


#     ____  ___  ________  ______
#    / __ \/   |/_  __/ / / / ___/
#   / /_/ / /| | / / / /_/ /\__ \
#  / ____/ ___ |/ / / __  /___/ /
# /_/   /_/  |_/_/ /_/ /_//____/


def get_file_folder_and_name_from_path(path: str) -> Tuple[str, str]:
    """
    Returns a tuple (FOLDER_PATH, FILE_NAME)
    :param path:
    :return:
    """
    obj_folder = path[: path.rindex("/") + 1] if "/" in path else ""
    obj_file_name = path[path.rindex("/") + 1 :] if "/" in path else path
    return obj_folder, obj_file_name
