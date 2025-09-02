# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
This module contains utilities to read/write EPC files.
"""

import datetime
import json
import logging
import os
import random
import re
import traceback
import zipfile
from dataclasses import dataclass, field
from io import BytesIO
from typing import List, Any, Union, Dict, Callable, Optional, Tuple

from energyml.opc.opc import (
    CoreProperties,
    Relationships,
    Types,
    Default,
    Relationship,
    Override,
    Created,
    Creator,
    Identifier,
    Keywords1,
    TargetMode,
)
from .uri import parse_uri
from xsdata.formats.dataclass.models.generics import DerivedElement

from .constants import (
    RELS_CONTENT_TYPE,
    RELS_FOLDER_NAME,
    RGX_DOMAIN_VERSION,
    EpcExportVersion,
    RawFile,
    EPCRelsRelationshipType,
    MimeType,
    content_type_to_qualified_type,
    qualified_type_to_content_type,
    split_identifier,
    get_property_kind_dict_path_as_dict,
)
from .data.datasets_io import (
    read_external_dataset_array,
)
from .exception import UnparsableFile
from .introspection import (
    get_class_from_content_type,
    get_obj_type,
    is_dor,
    search_attribute_matching_type,
    get_obj_version,
    get_obj_uuid,
    get_object_type_for_file_path_from_class,
    get_content_type_from_class,
    get_direct_dor_list,
    epoch_to_date,
    epoch,
    gen_uuid,
    get_obj_identifier,
    get_class_from_qualified_type,
    copy_attributes,
    get_obj_attribute_class,
    set_attribute_from_path,
    set_attribute_value,
    get_object_attribute,
    get_qualified_type_from_class,
    get_class_fields,
)
from .manager import get_class_pkg, get_class_pkg_version
from .serialization import (
    serialize_xml,
    read_energyml_xml_str,
    read_energyml_xml_bytes,
    read_energyml_json_str,
    read_energyml_json_bytes,
    JSON_VERSION,
)
from .workspace import EnergymlWorkspace
from .xml import is_energyml_content_type


@dataclass
class Epc(EnergymlWorkspace):
    """
    A class that represent an EPC file content
    """

    # content_type: List[str] = field(
    #     default_factory=list,
    # )

    export_version: EpcExportVersion = field(default=EpcExportVersion.CLASSIC)

    core_props: CoreProperties = field(default=None)

    """ xml files referred in the [Content_Types].xml  """
    energyml_objects: List = field(
        default_factory=list,
    )

    """ Other files content like pdf etc """
    raw_files: List[RawFile] = field(
        default_factory=list,
    )

    """ A list of external files. It can be used to link hdf5 files """
    external_files_path: List[str] = field(
        default_factory=list,
    )

    """ A list of h5 files stored in memory. (Usefull for Cloud services that doesn't work with local files """
    h5_io_files: List[BytesIO] = field(
        default_factory=list,
    )

    """ 
    Additional rels for objects. Key is the object (same than in @energyml_objects) and value is a list of
    RelationShip. This can be used to link an HDF5 to an ExternalPartReference in resqml 2.0.1
    Key is a value returned by @get_obj_identifier
    """
    additional_rels: Dict[str, List[Relationship]] = field(default_factory=lambda: {})

    """
    Epc file path. Used when loaded from a local file or for export
    """
    epc_file_path: Optional[str] = field(default=None)

    def __str__(self):
        return (
            "EPC file ("
            + str(self.export_version)
            + ") "
            + f"{len(self.energyml_objects)} energyml objects and {len(self.raw_files)} other files {[f.path for f in self.raw_files]}"
            # + f"\n{[serialize_json(ar) for ar in self.additional_rels]}"
        )

    def add_file(self, obj: Union[List, bytes, BytesIO, str, RawFile]):
        """
        Add one ore multiple files to the epc file.
        For non energyml file, it is better to use the RawFile class.
        The input can be a single file content, file path, or a list of them
        :param obj:
        :return:
        """
        if isinstance(obj, list):
            for o in obj:
                self.add_file(o)
        elif isinstance(obj, bytes) or isinstance(obj, BytesIO):
            try:
                xml_obj = read_energyml_xml_bytes(obj)
                self.energyml_objects.append(xml_obj)
            except:
                try:
                    if isinstance(obj, BytesIO):
                        obj.seek(0)
                    json_obj = read_energyml_json_bytes(obj, json_version=JSON_VERSION.OSDU_OFFICIAL)
                    self.add_file(json_obj)
                except:
                    # if isinstance(obj, BytesIO):
                    #     obj.seek(0)
                    # self.add_file(RawFile(path=f"pleaseRenameThisFile_{str(random.random())}", content=obj))
                    raise UnparsableFile()
        elif isinstance(obj, RawFile):
            self.raw_files.append(obj)
        elif isinstance(obj, str):
            # Can be a path or a content
            if os.path.exists(obj):
                with open(obj, "rb") as f:
                    file_content = f.read()
                    f_name = os.path.basename(obj)
                    _, f_ext = os.path.splitext(f_name)
                    if f_ext.lower().endswith(".xml") or f_ext.lower().endswith(".json"):
                        try:
                            self.add_file(file_content)
                        except UnparsableFile:
                            self.add_file(RawFile(f_name, BytesIO(file_content)))
                    elif not f_ext.lower().endswith(".rels"):
                        self.add_file(RawFile(f_name, BytesIO(file_content)))
                    else:
                        logging.error(f"Not supported file extension {f_name}")
            else:
                try:
                    xml_obj = read_energyml_xml_str(obj)
                    self.energyml_objects.append(xml_obj)
                except:
                    try:
                        if isinstance(obj, BytesIO):
                            obj.seek(0)
                        json_obj = read_energyml_json_str(obj, json_version=JSON_VERSION.OSDU_OFFICIAL)
                        self.add_file(json_obj)
                    except:
                        if isinstance(obj, BytesIO):
                            obj.seek(0)
                        self.add_file(RawFile(path=f"pleaseRenameThisFile_{str(random.random())}.txt", content=obj))
        elif str(type(obj).__module__).startswith("energyml."):
            # We should test "energyml.(resqml|witsml|prodml|eml|common)" but I didn't to avoid issues if
            # another specific package comes in the future
            self.energyml_objects.append(obj)
        else:
            logging.error(f"unsupported type {str(type(obj))}")

    # EXPORT functions

    def gen_opc_content_type(self) -> Types:
        """
        Generates a :class:`Types` instance and fill it with energyml objects :class:`Override` values
        :return:
        """
        ct = Types()
        rels_default = Default()
        rels_default.content_type = RELS_CONTENT_TYPE
        rels_default.extension = "rels"

        ct.default = [rels_default]

        ct.override = []
        for e_obj in self.energyml_objects:
            ct.override.append(
                Override(
                    content_type=get_content_type_from_class(type(e_obj)),
                    part_name=gen_energyml_object_path(e_obj, self.export_version),
                )
            )

        if self.core_props is not None:
            ct.override.append(
                Override(
                    content_type=get_content_type_from_class(self.core_props),
                    part_name=gen_core_props_path(self.export_version),
                )
            )

        return ct

    def export_file(self, path: Optional[str] = None) -> None:
        """
        Export the epc file. If :param:`path` is None, the epc 'self.epc_file_path' is used
        :param path:
        :return:
        """
        if path is None:
            path = self.epc_file_path
        epc_io = self.export_io()
        with open(path, "wb") as f:
            f.write(epc_io.getbuffer())

    def export_io(self) -> BytesIO:
        """
        Export the epc file into a :class:`BytesIO` instance. The result is an 'in-memory' zip file.
        :return:
        """
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            # CoreProps
            if self.core_props is None:
                self.core_props = CoreProperties(
                    created=Created(any_element=epoch_to_date(epoch())),
                    creator=Creator(any_element="energyml-utils python module (Geosiris)"),
                    identifier=Identifier(any_element=f"urn:uuid:{gen_uuid()}"),
                    keywords=Keywords1(
                        lang="en",
                        content=["generated;Geosiris;python;energyml-utils"],
                    ),
                    version="1.0",
                )

            zip_info_core = zipfile.ZipInfo(
                filename=gen_core_props_path(self.export_version),
                date_time=datetime.datetime.now().timetuple()[:6],
            )
            data = serialize_xml(self.core_props)
            zip_file.writestr(zip_info_core, data)

            #  Energyml objects
            for e_obj in self.energyml_objects:
                e_path = gen_energyml_object_path(e_obj, self.export_version)
                zip_info = zipfile.ZipInfo(
                    filename=e_path,
                    date_time=datetime.datetime.now().timetuple()[:6],
                )
                data = serialize_xml(e_obj)
                zip_file.writestr(zip_info, data)

            # Rels
            for rels_path, rels in self.compute_rels().items():
                zip_info = zipfile.ZipInfo(
                    filename=rels_path,
                    date_time=datetime.datetime.now().timetuple()[:6],
                )
                data = serialize_xml(rels)
                zip_file.writestr(zip_info, data)

            # Other files:
            for raw in self.raw_files:
                zip_info = zipfile.ZipInfo(
                    filename=raw.path,
                    date_time=datetime.datetime.now().timetuple()[:6],
                )
                zip_file.writestr(zip_info, raw.content.read())

            # ContentType
            zip_info_ct = zipfile.ZipInfo(
                filename=get_epc_content_type_path(),
                date_time=datetime.datetime.now().timetuple()[:6],
            )
            data = serialize_xml(self.gen_opc_content_type())
            zip_file.writestr(zip_info_ct, data)

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
                )
                for target_obj in target_obj_list
            ]
            for obj_id, target_obj_list in dor_relation.items()
        }
        # sourceObject
        for obj in self.energyml_objects:
            obj_id = get_obj_identifier(obj)
            if obj_id not in rels:
                rels[obj_id] = []
            for target_obj in get_direct_dor_list(obj):
                try:
                    rels[obj_id].append(
                        Relationship(
                            target=gen_energyml_object_path(target_obj, self.export_version),
                            type_value=EPCRelsRelationshipType.SOURCE_OBJECT.get_type(),
                            id=f"_{obj_id}_{get_obj_type(target_obj)}_{get_obj_identifier(target_obj)}",
                        )
                    )
                except Exception:
                    logging.error(f'Failed to create rels for "{obj_id}" with target {target_obj}')

        # filtering non-accessible objects from DOR
        rels = {k: v for k, v in rels.items() if self.get_object_by_identifier(k) is not None}

        map_obj_id_to_obj = {get_obj_identifier(obj): obj for obj in self.energyml_objects}

        obj_rels = {
            gen_rels_path(
                energyml_object=map_obj_id_to_obj.get(obj_id),
                export_version=self.export_version,
            ): Relationships(
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
                        type_value=EPCRelsRelationshipType.CORE_PROPERTIES.get_type(),
                        id="CoreProperties",
                    )
                ]
            )

        return obj_rels

    def rels_to_h5_file(self, obj: any, h5_path: str) -> Relationship:
        """
        Creates in the epc file, a Relation (in the object .rels file) to link a h5 external file.
        Usually this function is used to link an ExternalPartReference to a h5 file.
        In practice, the Relation object is added to the "additional_rels" of the current epc file.
        :param obj:
        :param h5_path:
        :return: the Relationship added to the epc.additional_rels dict
        """
        obj_ident = get_obj_identifier(obj)
        if obj_ident not in self.additional_rels:
            self.additional_rels[obj_ident] = []

        rel = Relationship(
            target=h5_path,
            type_value=EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type(),
            id="Hdf5File",
            target_mode=TargetMode.EXTERNAL.value,
        )
        self.additional_rels[obj_ident].append(rel)
        return rel

    # -- Functions inherited from EnergymlWorkspace

    def get_object_as_dor(self, identifier: str, dor_qualified_type) -> Optional[Any]:
        """
        Search an object by its identifier and returns a DOR
        :param identifier:
        :param dor_qualified_type: the qualified type of the DOR (e.g. resqml22.DataObjectReference)
        :return:
        """
        obj = self.get_object_by_identifier(identifier=identifier)
        # if obj is None:

        return as_dor(obj_or_identifier=obj or identifier, dor_qualified_type=dor_qualified_type)

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        """
        Search all objects with the uuid :param:`uuid`.
        :param uuid:
        :return:
        """
        return list(filter(lambda o: get_obj_uuid(o) == uuid, self.energyml_objects))

    def get_object_by_identifier(self, identifier: str) -> Optional[Any]:
        """
        Search an object by its identifier.
        :param identifier: given by the function :func:`get_obj_identifier`
        :return:
        """
        for o in self.energyml_objects:
            if get_obj_identifier(o) == identifier:
                return o
        return None

    def get_object(self, uuid: str, object_version: Optional[str]) -> Optional[Any]:
        return self.get_object_by_identifier(f"{uuid}.{object_version or ''}")

    def get_epc_file_folder(self) -> Optional[str]:
        if self.epc_file_path is not None and len(self.epc_file_path) > 0:
            folders_and_name = re.split(r"[\\/]", self.epc_file_path)
            if len(folders_and_name) > 1:
                return "/".join(folders_and_name[:-1])
            else:
                return ""
        return None

    def read_external_array(
        self,
        energyml_array: Any,
        root_obj: Optional[Any] = None,
        path_in_root: Optional[str] = None,
        use_epc_io_h5: bool = True,
    ) -> List[Any]:
        sources = []
        if self is not None and use_epc_io_h5 and self.h5_io_files is not None and len(self.h5_io_files):
            sources = sources + self.h5_io_files

        return read_external_dataset_array(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
            additional_sources=sources,
            epc=self,
        )

    # Class methods

    @classmethod
    def read_file(cls, epc_file_path: str):
        with open(epc_file_path, "rb") as f:
            epc = cls.read_stream(BytesIO(f.read()))
            epc.epc_file_path = epc_file_path
            return epc

    @classmethod
    def read_stream(cls, epc_file_io: BytesIO):  # returns an Epc instance
        """
        :param epc_file_io:
        :return: an :class:`EPC` instance
        """
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
                    logging.error(f"No {content_type_file_name} file found")
                else:
                    content_type_obj: Types = read_energyml_xml_bytes(epc_file.read(content_type_file_name))
                    path_to_obj = {}
                    for ov in content_type_obj.override:
                        ov_ct = ov.content_type
                        ov_path = ov.part_name
                        # logging.debug(ov_ct)
                        while ov_path.startswith("/") or ov_path.startswith("\\"):
                            ov_path = ov_path[1:]
                        if is_energyml_content_type(ov_ct):
                            _read_files.append(ov_path)
                            try:
                                ov_obj = read_energyml_xml_bytes(
                                    epc_file.read(ov_path),
                                    get_class_from_content_type(ov_ct),
                                )
                                if isinstance(ov_obj, DerivedElement):
                                    ov_obj = ov_obj.value
                                path_to_obj[ov_path] = ov_obj
                                obj_list.append(ov_obj)
                            except Exception as e:
                                logging.error(traceback.format_exc())
                                logging.error(
                                    f"Epc.@read_stream failed to parse file {ov_path} for content-type: {ov_ct} => {get_class_from_content_type(ov_ct)}\n\n",
                                    get_class_from_content_type(ov_ct),
                                )
                                try:
                                    logging.debug(epc_file.read(ov_path))
                                except:
                                    pass
                                # raise e
                        elif get_class_from_content_type(ov_ct) == CoreProperties:
                            _read_files.append(ov_path)
                            core_props = read_energyml_xml_bytes(epc_file.read(ov_path), CoreProperties)
                            path_to_obj[ov_path] = core_props

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
                                    logging.error(traceback.format_exc())
                            elif f_info.filename != "_rels/.rels":  # CoreProperties rels file
                                # RELS FILES READING START

                                # logging.debug(f"reading rels {f_info.filename}")
                                (
                                    rels_folder,
                                    rels_file_name,
                                ) = get_file_folder_and_name_from_path(f_info.filename)
                                while rels_folder.endswith("/"):
                                    rels_folder = rels_folder[:-1]
                                obj_folder = rels_folder[: rels_folder.rindex("/") + 1] if "/" in rels_folder else ""
                                obj_file_name = rels_file_name[:-5]  # removing the ".rels"
                                rels_file: Relationships = read_energyml_xml_bytes(
                                    epc_file.read(f_info.filename),
                                    Relationships,
                                )
                                obj_path = obj_folder + obj_file_name
                                if obj_path in path_to_obj:
                                    try:
                                        additional_rels_key = get_obj_identifier(path_to_obj[obj_path])
                                        for rel in rels_file.relationship:
                                            # logging.debug(f"\t\t{rel.type_value}")
                                            if (
                                                rel.type_value != EPCRelsRelationshipType.DESTINATION_OBJECT.get_type()
                                                and rel.type_value != EPCRelsRelationshipType.SOURCE_OBJECT.get_type()
                                                and rel.type_value
                                                != EPCRelsRelationshipType.EXTENDED_CORE_PROPERTIES.get_type()
                                            ):  # not a computable relation
                                                if additional_rels_key not in additional_rels:
                                                    additional_rels[additional_rels_key] = []
                                                additional_rels[additional_rels_key].append(rel)
                                    except AttributeError:
                                        logging.error(traceback.format_exc())
                                        pass  # 'CoreProperties' object has no attribute 'object_version'
                                    except Exception as e:
                                        logging.error(f"Error with obj path {obj_path} {path_to_obj[obj_path]}")
                                        raise e
                                else:
                                    logging.error(
                                        f"xml file '{f_info.filename}' is not associate to any readable object "
                                        f"(or the object type is not supported because"
                                        f" of a lack of a dependency module) "
                                    )

            return Epc(
                energyml_objects=obj_list,
                raw_files=raw_file_list,
                core_props=core_props,
                additional_rels=additional_rels,
            )
        except zipfile.BadZipFile as error:
            logging.error(error)

        return None


#     ______                                      __   ____                 __  _
#    / ____/___  ___  _________ ___  ______ ___  / /  / __/_  ______  _____/ /_(_)___  ____  _____
#   / __/ / __ \/ _ \/ ___/ __ `/ / / / __ `__ \/ /  / /_/ / / / __ \/ ___/ __/ / __ \/ __ \/ ___/
#  / /___/ / / /  __/ /  / /_/ / /_/ / / / / / / /  / __/ /_/ / / / / /__/ /_/ / /_/ / / / (__  )
# /_____/_/ /_/\___/_/   \__, /\__, /_/ /_/ /_/_/  /_/  \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/
#                       /____//____/

"""
PropertyKind list: a list of Pre-defined properties
"""
__CACHE_PROP_KIND_DICT__ = {}


def update_prop_kind_dict_cache():
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


def as_dor(obj_or_identifier: Any, dor_qualified_type: str = "eml23.DataObjectReference"):
    """
    Create an DOR from an object to target the latter.
    :param obj_or_identifier:
    :param dor_qualified_type: the qualified type of the DOR (e.g. "eml23.DataObjectReference" is the default value)
    :return:
    """
    dor = None
    if obj_or_identifier is not None:
        cls = get_class_from_qualified_type(dor_qualified_type)
        dor = cls()
        if isinstance(obj_or_identifier, str):  # is an identifier or uri
            parsed_uri = parse_uri(obj_or_identifier)
            if parsed_uri is not None:
                if hasattr(dor, "qualified_type"):
                    set_attribute_from_path(dor, "qualified_type", parsed_uri.get_qualified_type())
                if hasattr(dor, "content_type"):
                    set_attribute_from_path(
                        dor, "content_type", qualified_type_to_content_type(parsed_uri.get_qualified_type())
                    )
                set_attribute_from_path(dor, "uuid", parsed_uri.uuid)
                if hasattr(dor, "object_version"):
                    set_attribute_from_path(dor, "version_string", parsed_uri.version)
                if hasattr(dor, "version_string"):
                    set_attribute_from_path(dor, "version_string", parsed_uri.version)

            else:  # identifier
                if len(__CACHE_PROP_KIND_DICT__) == 0:
                    # update the cache to check if it is a
                    try:
                        update_prop_kind_dict_cache()
                    except FileNotFoundError as e:
                        logging.error(f"Failed to parse propertykind dict {e}")
                try:
                    uuid, version = split_identifier(obj_or_identifier)
                    if uuid in __CACHE_PROP_KIND_DICT__:
                        return as_dor(__CACHE_PROP_KIND_DICT__[uuid])
                    else:
                        set_attribute_from_path(dor, "uuid", uuid)
                        set_attribute_from_path(dor, "ObjectVersion", version)
                except AttributeError:
                    logging.error(f"Failed to parse identifier {obj_or_identifier}. DOR will be empty")
        else:
            if is_dor(obj_or_identifier):
                # If it is a dor, we create a dor conversionif hasattr(dor, "qualified_type"):
                if hasattr(dor, "qualified_type"):
                    if hasattr(obj_or_identifier, "qualified_type"):
                        dor.qualified_type = get_object_attribute(obj_or_identifier, "qualified_type")
                    elif hasattr(obj_or_identifier, "content_type"):
                        dor.qualified_type = content_type_to_qualified_type(
                            get_object_attribute(obj_or_identifier, "content_type")
                        )

                if hasattr(dor, "content_type"):
                    if hasattr(obj_or_identifier, "qualified_type"):
                        dor.content_type = qualified_type_to_content_type(
                            get_object_attribute(obj_or_identifier, "qualified_type")
                        )
                    elif hasattr(obj_or_identifier, "content_type"):
                        dor.content_type = get_object_attribute(obj_or_identifier, "content_type")

                set_attribute_from_path(dor, "title", get_object_attribute(obj_or_identifier, "Title"))

            else:
                if hasattr(dor, "qualified_type"):
                    set_attribute_from_path(dor, "qualified_type", get_qualified_type_from_class(obj_or_identifier))
                if hasattr(dor, "content_type"):
                    set_attribute_from_path(dor, "content_type", get_content_type_from_class(obj_or_identifier))

                set_attribute_from_path(dor, "title", get_object_attribute(obj_or_identifier, "Citation.Title"))

            set_attribute_from_path(dor, "uuid", get_obj_uuid(obj_or_identifier))

            if hasattr(dor, "object_version"):
                set_attribute_from_path(dor, "object_version", get_obj_version(obj_or_identifier))
            if hasattr(dor, "version_string"):
                set_attribute_from_path(dor, "version_string", get_obj_version(obj_or_identifier))

    return dor


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
    version_flat = re.findall(RGX_DOMAIN_VERSION, eml_version)[0][0].replace(".", "").replace("_", "")
    obj = create_energyml_object(
        content_or_qualified_type="eml" + version_flat + ".EpcExternalPartReference",
        citation=citation,
        uuid=uuid,
    )
    set_attribute_value(obj, "MimeType", MimeType.HDF5.value)
    set_attribute_value(obj, "ExistenceKind", "Actual")
    set_attribute_value(obj, "Filename", h5_file_path)

    return obj


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


def gen_core_props_path(
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
):
    return "docProps/core.xml"


def gen_energyml_object_path(
    energyml_object: Union[str, Any],
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
):
    """
    Generate a path to store the :param:`energyml_object` into an epc file (depending on the :param:`export_version`)
    :param energyml_object:
    :param export_version:
    :return:
    """
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
        return f"namespace_{pkg}{pkg_version.replace('.', '')}/{uuid}{(('/version_' + object_version) if object_version is not None else '')}/{obj_type}_{uuid}.xml"
    else:
        return obj_type + "_" + uuid + ".xml"


def get_file_folder_and_name_from_path(path: str) -> Tuple[str, str]:
    """
    Returns a tuple (FOLDER_PATH, FILE_NAME)
    :param path:
    :return:
    """
    obj_folder = path[: path.rindex("/") + 1] if "/" in path else ""
    obj_file_name = path[path.rindex("/") + 1 :] if "/" in path else path
    return obj_folder, obj_file_name


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
        return f"{RELS_FOLDER_NAME}/.rels"
    else:
        obj_path = gen_energyml_object_path(energyml_object, export_version)
        obj_folder, obj_file_name = get_file_folder_and_name_from_path(obj_path)
        return f"{obj_folder}{RELS_FOLDER_NAME}/{obj_file_name}.rels"


def get_epc_content_type_path(
    export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
) -> str:
    """
    Generate a path to store the "[Content_Types].xml" file into an epc file
    (depending on the :param:`export_version`)
    :return:
    """
    return "[Content_Types].xml"
