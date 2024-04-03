# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import datetime
import re
import zipfile
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import List, Any, Union, Dict, Callable, Optional, Tuple

from energyml.opc.opc import CoreProperties, Relationships, Types, Default, Relationship, Override
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.models.generics import DerivedElement

from .introspection import (
    get_class_from_content_type,
    get_obj_type, search_attribute_matching_type, get_obj_version, get_obj_uuid,
    get_object_type_for_file_path_from_class, get_content_type_from_class, get_direct_dor_list
)
from .manager import get_class_pkg, get_class_pkg_version
from .serialization import (
    serialize_xml, read_energyml_xml_str, read_energyml_xml_bytes, read_energyml_xml_bytes_as_class
)
from .xml import is_energyml_content_type

RELS_CONTENT_TYPE = "application/vnd.openxmlformats-package.core-properties+xml"
RELS_FOLDER_NAME = "_rels"


class NoCrsException(Exception):
    pass


@dataclass
class ObjectNotFoundNotException(Exception):
    obj_id: str = field(
        default=None
    )


class EpcExportVersion(Enum):
    """EPC export version."""
    #: Classical export
    CLASSIC = 1
    #: Export with objet path sorted by package (eml/resqml/witsml/prodml)
    EXPANDED = 2


class EPCRelsRelationshipType(Enum):
    #: The object in Target is the destination of the relationship.
    DESTINATION_OBJECT = "destinationObject"
    #: The current object is the source in the relationship with the target object.
    SOURCE_OBJECT = "sourceObject"
    #: The target object is a proxy object for an external data object (HDF5 file).
    ML_TO_EXTERNAL_PART_PROXY = "mlToExternalPartProxy"
    #: The current object is used as a proxy object by the target object.
    EXTERNAL_PART_PROXY_TO_ML = "externalPartProxyToMl"
    #: The target is a resource outside of the EPC package. Note that TargetMode should be "External"
    #: for this relationship.
    EXTERNAL_RESOURCE = "externalResource"
    #: The object in Target is a media representation for the current object. As a guideline, media files
    #: should be stored in a "media" folder in the ROOT of the package.
    DestinationMedia = "destinationMedia"
    #: The current object is a media representation for the object in Target.
    SOURCE_MEDIA = "sourceMedia"
    #: The target is part of a larger data object that has been chunked into several smaller files
    CHUNKED_PART = "chunkedPart"
    #: /!\ not in the norm
    EXTENDED_CORE_PROPERTIES = "extended-core-properties"

    def get_type(self) -> str:
        match self:
            case EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES:
                return "http://schemas.f2i-consulting.com/package/2014/relationships/" + str(self.value)
            case (
            EPCRelsRelationshipType.CHUNKED_PART
            | EPCRelsRelationshipType.DESTINATION_OBJECT
            | EPCRelsRelationshipType.SOURCE_OBJECT
            | EPCRelsRelationshipType.ML_TO_EXTERNAL_PART_PROXY
            | EPCRelsRelationshipType.EXTERNAL_PART_PROXY_TO_ML
            | EPCRelsRelationshipType.EXTERNAL_RESOURCE
            | EPCRelsRelationshipType.DestinationMedia
            | EPCRelsRelationshipType.SOURCE_MEDIA
            | _
            ):
                return "http://schemas.energistics.org/package/2012/relationships/" + str(self.value)


@dataclass
class RawFile:
    path: str = field(default="_")
    content: BytesIO = field(default=None)


@dataclass
class Epc:
    """
    A class that represent an EPC file content
    """
    # content_type: List[str] = field(
    #     default_factory=list,
    # )

    export_version: EpcExportVersion = field(
        default=EpcExportVersion.CLASSIC
    )

    core_props: CoreProperties = field(default=None)

    """ xml files refered in the [Content_Types].xml  """
    energyml_objects: List = field(
        default_factory=list,
    )

    """ Other files content like pdf etc """
    raw_files: List[RawFile] = field(
        default_factory=list,
    )

    """ A list of external files. It ca be used to link hdf5 files """
    external_files_path: List[str] = field(
        default_factory=list,
    )

    """ 
    Additional rels for objects. Key is the object (same than in @energyml_objects) and value is a list of
    RelationShip. This can be used to link an HDF5 to an ExternalPartReference in resqml 2.0.1
    Key is a value returned by @get_obj_identifier
    """
    additional_rels: Dict[str, List[Relationship]] = field(
        default_factory=lambda: {}
    )

    """
    Epc file path. Used when loaded from a local file or for export
    """
    epc_file_path: Optional[str] = field(
        default=None
    )

    def __str__(self):
        return (
                "EPC file (" + str(self.export_version) + ") "
                + f"{len(self.energyml_objects)} energyml objects and {len(self.raw_files)} other files {[f.path for f in self.raw_files]}"
                # + f"\n{[serialize_json(ar) for ar in self.additional_rels]}"
        )

    # EXPORT functions

    def gen_opc_content_type(self) -> Types:
        ct = Types()
        rels_default = Default()
        rels_default.content_type = RELS_CONTENT_TYPE
        rels_default.extension = "rels"

        ct.default = [rels_default]

        ct.override = []
        for e_obj in self.energyml_objects:
            ct.override.append(Override(
                content_type=get_content_type_from_class(type(e_obj)),
                part_name=gen_energyml_object_path(e_obj, self.export_version),
            ))

        if self.core_props is not None:
            ct.override.append(Override(
                content_type=get_content_type_from_class(self.core_props),
                part_name=gen_core_props_path(self.export_version),
            ))

        return ct

    def export_file(self, path: Optional[str] = None) -> None:
        """
        Export the epc file. If :param path is None, the epc 'self.epc_file_path' is used
        :param path:
        :return:
        """
        if path is None:
            path = self.epc_file_path
        epc_io = self.export_io()
        with open(path, "wb") as f:
            f.write(epc_io.getbuffer())

    def export_io(self) -> BytesIO:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            #  Energyml objects
            for e_obj in self.energyml_objects:
                e_path = gen_energyml_object_path(e_obj, self.export_version)
                zip_info = zipfile.ZipInfo(filename=e_path, date_time=datetime.datetime.now().timetuple()[:6])
                data = serialize_xml(e_obj)
                zip_file.writestr(zip_info, data)

            # Rels
            for rels_path, rels in self.compute_rels().items():
                zip_info = zipfile.ZipInfo(filename=rels_path, date_time=datetime.datetime.now().timetuple()[:6])
                data = serialize_xml(rels)
                zip_file.writestr(zip_info, data)

            # CoreProps
            if self.core_props is not None:
                zip_info = zipfile.ZipInfo(filename=gen_core_props_path(self.export_version),
                                           date_time=datetime.datetime.now().timetuple()[:6])
                data = serialize_xml(self.core_props)
                zip_file.writestr(zip_info, data)

            # ContentType
            zip_info = zipfile.ZipInfo(filename=get_epc_content_type_path(),
                                       date_time=datetime.datetime.now().timetuple()[:6])
            data = serialize_xml(self.gen_opc_content_type())
            zip_file.writestr(zip_info, data)

        return zip_buffer

    def compute_rels(self) -> Dict[str, Relationships]:
        """
        Returns a dict containing for each objet, the rels xml file path as key and the RelationShips object as value
        :return:
        """
        dor_relation = get_reverse_dor_list(self.energyml_objects)

        # destObject
        rels = {
            obj_id: [
                Relationship(
                    target=gen_energyml_object_path(target_obj, self.export_version),
                    type_value=EPCRelsRelationshipType.DESTINATION_OBJECT.get_type(),
                    id=f"_{obj_id}_{get_obj_type(target_obj)}_{get_obj_identifier(target_obj)}",
                ) for target_obj in target_obj_list
            ]
            for obj_id, target_obj_list in dor_relation.items()
        }
        # sourceObject
        for obj in self.energyml_objects:
            obj_id = get_obj_identifier(obj)
            if obj_id not in rels:
                rels[obj_id] = []
            for target_obj in get_direct_dor_list(obj):
                rels[obj_id].append(Relationship(
                    target=gen_energyml_object_path(target_obj, self.export_version),
                    type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                    id=f"_{obj_id}_{get_obj_type(target_obj)}_{get_obj_identifier(target_obj)}",
                ))

        map_obj_id_to_obj = {
            get_obj_identifier(obj): obj
            for obj in self.energyml_objects
        }

        obj_rels = {
            gen_rels_path(map_obj_id_to_obj.get(obj_id), export_version=self.export_version): Relationships(
                relationship=obj_rels + (self.additional_rels[obj_id] if obj_id in self.additional_rels else []),

            )
            for obj_id, obj_rels in rels.items()
        }

        # CoreProps
        if self.core_props is not None:
            obj_rels[gen_rels_path(self.core_props)] = Relationships(
                relationship=[
                    Relationship(
                        target=gen_core_props_path(),
                        type_value=EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES.get_type(),
                        id="CoreProperties"
                    )
                ]
            )

        return obj_rels

    # -----------

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        return list(filter(lambda o: get_obj_uuid(o) == uuid, self.energyml_objects))

    def get_object_by_identifier(self, identifier: str) -> Optional[Any]:
        """
        :param identifier: given by the function @get_obj_identifier
        :return:
        """
        for o in self.energyml_objects:
            if get_obj_identifier(o) == identifier:
                return o
        return None

    def get_epc_file_foler(self) -> Optional[str]:
        if self.epc_file_path is not None and len(self.epc_file_path) > 0:
            folders_and_name = re.split(r"[\\/]", self.epc_file_path)
            if len(folders_and_name) > 1:
                return "/".join(folders_and_name[:-1])
            else:
                return ""
        return None

    # Class methods

    @classmethod
    def read_file(cls, epc_file_path: str):
        with open(epc_file_path, "rb") as f:
            epc = cls.read_stream(BytesIO(f.read()))
            epc.epc_file_path = epc_file_path
            return epc

    @classmethod
    def read_stream(cls, epc_file_io: BytesIO):  # returns an Epc instance
        try:
            _read_files = []
            obj_list = []
            raw_file_list = []
            additional_rels = {}
            core_props = None
            with zipfile.ZipFile(epc_file_io, "r", zipfile.ZIP_DEFLATED) as epc_file:
                content_type_file_name = get_epc_content_type_path()
                content_type_info = None
                try:
                    content_type_info = epc_file.getinfo(content_type_file_name)
                except KeyError:
                    for info in epc_file.infolist():
                        if info.filename.lower() == content_type_file_name.lower():
                            content_type_info = info
                            break

                _read_files.append(content_type_file_name)

                if content_type_info is None:
                    print(f"No {content_type_file_name} file found")
                else:
                    content_type_obj: Types = read_energyml_xml_bytes(epc_file.read(content_type_file_name))
                    path_to_obj = {}
                    for ov in content_type_obj.override:
                        ov_ct = ov.content_type
                        ov_path = ov.part_name
                        # print(ov_ct)
                        while ov_path.startswith("/") or ov_path.startswith("\\"):
                            ov_path = ov_path[1:]
                        if is_energyml_content_type(ov_ct):
                            _read_files.append(ov_path)
                            try:
                                ov_obj = read_energyml_xml_bytes_as_class(
                                    epc_file.read(ov_path),
                                    get_class_from_content_type(ov_ct)
                                )
                                if isinstance(ov_obj, DerivedElement):
                                    ov_obj = ov_obj.value
                                path_to_obj[ov_path] = ov_obj
                                obj_list.append(ov_obj)
                            except ParserError as e:
                                print(f"Epc.@read_stream failed to parse file {ov_path} for content-type: {ov_ct} => {get_class_from_content_type(ov_ct)}")
                                raise e
                        elif get_class_from_content_type(ov_ct) == CoreProperties:
                            _read_files.append(ov_path)
                            core_props = read_energyml_xml_bytes_as_class(epc_file.read(ov_path), CoreProperties)

                    for f_info in epc_file.infolist():
                        if f_info.filename not in _read_files:
                            _read_files.append(f_info.filename)
                            if not f_info.filename.lower().endswith(".rels"):
                                try:
                                    raw_file_list.append(
                                        RawFile(
                                            path=f_info.filename,
                                            content=BytesIO(epc_file.read(f_info.filename)),
                                        )
                                    )
                                except IOError as e:
                                    print(e)
                            else:  # rels
                                # print(f"reading rels {f_info.filename}")
                                rels_folder, rels_file_name = get_file_folder_and_name_from_path(f_info.filename)
                                while rels_folder.endswith("/"):
                                    rels_folder = rels_folder[:-1]
                                obj_folder = rels_folder[:rels_folder.rindex("/") + 1] if "/" in rels_folder else ""
                                obj_file_name = rels_file_name[:-5]  # removing the ".rels"
                                rels_file: Relationships = read_energyml_xml_bytes_as_class(
                                    epc_file.read(f_info.filename),
                                    Relationships
                                )
                                obj_path = obj_folder + obj_file_name
                                if obj_path in path_to_obj:
                                    try:
                                        additional_rels_key = get_obj_identifier(path_to_obj[obj_path])
                                        for rel in rels_file.relationship:
                                            # print(f"\t\t{rel.type_value}")
                                            if (rel.type_value != EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()
                                                    and rel.type_value != EPCRelsRelationshipType.SOURCE_OBJECT.get_type()
                                                    and rel.type_value != EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES.get_type()
                                            ):  # not a computable relation
                                                if additional_rels_key not in additional_rels:
                                                    additional_rels[additional_rels_key] = []
                                                additional_rels[additional_rels_key].append(rel)
                                    except Exception as e:
                                        print(f"Error with obj path {obj_path} {path_to_obj[obj_path]}")
                                        raise e
                                else:
                                    print(f"xml file {obj_path} not found in EPC (rels is not associate to any object)")

            return Epc(energyml_objects=obj_list,
                       raw_files=raw_file_list,
                       core_props=core_props,
                       additional_rels=additional_rels
                       )
        except zipfile.BadZipFile as error:
            print(error)

        return None


#     ______                                      __   ____                 __  _
#    / ____/___  ___  _________ ___  ______ ___  / /  / __/_  ______  _____/ /_(_)___  ____  _____
#   / __/ / __ \/ _ \/ ___/ __ `/ / / / __ `__ \/ /  / /_/ / / / __ \/ ___/ __/ / __ \/ __ \/ ___/
#  / /___/ / / /  __/ /  / /_/ / /_/ / / / / / / /  / __/ /_/ / / / / /__/ /_/ / /_/ / / / (__  )
# /_____/_/ /_/\___/_/   \__, /\__, /_/ /_/ /_/_/  /_/  \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/
#                       /____//____/


def get_obj_identifier(obj: Any) -> str:
    """
    Generate an objet identifier as : 'OBJ_UUID.OBJ_VERSION'
    If the object version is None, the result is 'OBJ_UUID.'
    :param obj:
    :return: str
    """
    obj_obj_version = get_obj_version(obj)
    if obj_obj_version is None:
        obj_obj_version = ""
    obj_uuid = get_obj_uuid(obj)
    return f"{obj_uuid}.{obj_obj_version}"


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


# PATHS


def gen_core_props_path(export_version: EpcExportVersion = EpcExportVersion.CLASSIC):
    return "docProps/core.xml"


def gen_energyml_object_path(energyml_object: Union[str, Any],
                             export_version: EpcExportVersion = EpcExportVersion.CLASSIC):
    if isinstance(energyml_object, str):
        energyml_object = read_energyml_xml_str(energyml_object)

    obj_type = get_object_type_for_file_path_from_class(energyml_object.__class__)

    pkg = get_class_pkg(energyml_object)
    pkg_version = get_class_pkg_version(energyml_object)
    object_version = get_obj_version(energyml_object)
    uuid = get_obj_uuid(energyml_object)

    # if object_version is None:
    #     object_version = "0"

    if export_version == EpcExportVersion.EXPANDED:
        return f"namespace_{pkg}{pkg_version.replace('.', '')}/{uuid}{('/version_' + object_version) if object_version is not None else ''}/{obj_type}_{uuid}.xml"
    else:
        return obj_type + "_" + uuid + ".xml"


def get_file_folder_and_name_from_path(path: str) -> Tuple[str, str]:
    obj_folder = path[:path.rindex("/") + 1] if "/" in path else ""
    obj_file_name = path[path.rindex("/") + 1:] if "/" in path else path
    return obj_folder, obj_file_name


def gen_rels_path(obj: Any,
                  export_version: EpcExportVersion = EpcExportVersion.CLASSIC
                  ) -> str:
    if isinstance(obj, CoreProperties):
        return f"{RELS_FOLDER_NAME}/.rels"
    else:
        obj_path = gen_energyml_object_path(obj, export_version)
        obj_folder, obj_file_name = get_file_folder_and_name_from_path(obj_path, )
        return f"{obj_folder}{RELS_FOLDER_NAME}/{obj_file_name}.rels"


def get_epc_content_type_path() -> str:
    return "[Content_Types].xml"
