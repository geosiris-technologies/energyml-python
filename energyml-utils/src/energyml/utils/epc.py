# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
This module contains utilities to read/write EPC files.
"""

import datetime
import logging
import os
from pathlib import Path
import random
import re
import traceback
import zipfile
from dataclasses import dataclass, field
from io import BytesIO
from typing import List, Any, Union, Dict, Optional

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
)
from energyml.utils.epc_utils import (
    gen_core_props_path,
    gen_energyml_object_path,
    gen_rels_path,
    get_epc_content_type_path,
    create_h5_external_relationship,
)
from energyml.utils.storage_interface import DataArrayMetadata, EnergymlStorageInterface, ResourceMetadata
import numpy as np
from energyml.utils.uri import Uri, parse_uri
from xsdata.formats.dataclass.models.generics import DerivedElement

from energyml.utils.constants import (
    RELS_CONTENT_TYPE,
    EpcExportVersion,
    RawFile,
    EPCRelsRelationshipType,
)
from energyml.utils.data.datasets_io import (
    get_handler_registry,
    read_external_dataset_array,
)
from energyml.utils.exception import UnparsableFile
from energyml.utils.introspection import (
    get_class_from_content_type,
    get_obj_type,
    get_obj_uri,
    get_obj_usable_class,
    get_obj_version,
    get_obj_uuid,
    get_content_type_from_class,
    get_direct_dor_list,
    epoch_to_date,
    epoch,
    gen_uuid,
    get_obj_identifier,
    get_object_attribute,
    get_qualified_type_from_class,
)
from energyml.utils.serialization import (
    serialize_xml,
    read_energyml_xml_str,
    read_energyml_xml_bytes,
    read_energyml_json_str,
    read_energyml_json_bytes,
    JSON_VERSION,
)
from energyml.utils.xml import is_energyml_content_type


@dataclass
class Epc(EnergymlStorageInterface):
    """
    A class that represent an EPC file content
    """

    # content_type: List[str] = field(
    #     default_factory=list,
    # )

    export_version: EpcExportVersion = field(default=EpcExportVersion.CLASSIC)

    core_props: Optional[CoreProperties] = field(default=None)

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

    force_h5_path: Optional[str] = field(default=None)

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

        # Ensure directory exists
        if path is not None:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
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

    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        """
        Get the relationships for a given energyml object
        :param obj: The object identifier/URI or the object itself
        :return: List of Relationship objects
        """
        # Convert identifier to object if needed
        if isinstance(obj, str) or isinstance(obj, Uri):
            obj = self.get_object_by_identifier(obj)
            if obj is None:
                return []

        rels_path = gen_rels_path(
            energyml_object=obj,
            export_version=self.export_version,
        )
        all_rels = self.compute_rels()
        if rels_path in all_rels:
            return all_rels[rels_path].relationship if all_rels[rels_path].relationship else []
        return []

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
                    type_value=get_rels_dor_type(
                        gen_energyml_object_path(self.get_object(obj_id), self.export_version),
                        in_dor_owner_rels_file=False,
                    ),
                    id=f"_{obj_id}_{get_obj_type(get_obj_usable_class(target_obj))}_{get_obj_identifier(target_obj)}",
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
                            type_value=get_rels_dor_type(
                                gen_energyml_object_path(target_obj, self.export_version), in_dor_owner_rels_file=True
                            ),
                            id=f"_{obj_id}_{get_obj_type(get_obj_usable_class(target_obj))}_{get_obj_identifier(target_obj)}",
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

    def rels_to_h5_file(self, obj: Any, h5_path: str) -> Relationship:
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

        nb_current_file = len(self.get_h5_file_paths(obj))

        rel = create_h5_external_relationship(h5_path=h5_path, current_idx=nb_current_file)
        self.additional_rels[obj_ident].append(rel)
        return rel

    def get_h5_file_paths(self, obj: Any) -> List[str]:
        """
        Get all HDF5 file paths referenced in the EPC file (from rels to external resources)
        :return: list of HDF5 file paths
        """

        if self.force_h5_path is not None:
            return [self.force_h5_path]

        is_uri = (isinstance(obj, str) and parse_uri(obj) is not None) or isinstance(obj, Uri)
        if is_uri:
            obj = self.get_object_by_identifier(obj)

        h5_paths = set()

        if isinstance(obj, str):
            obj = self.get_object_by_identifier(obj)
        for rels in self.additional_rels.get(get_obj_identifier(obj), []):
            if rels.type_value == EPCRelsRelationshipType.EXTERNAL_RESOURCE.get_type():
                h5_paths.add(rels.target)

        if len(h5_paths) == 0:
            # search if an h5 file has the same name than the epc file
            epc_folder = self.get_epc_file_folder()
            if epc_folder is not None and self.epc_file_path is not None:
                epc_file_name = os.path.basename(self.epc_file_path)
                epc_file_base, _ = os.path.splitext(epc_file_name)
                possible_h5_path = os.path.join(epc_folder, epc_file_base + ".h5")
                if os.path.exists(possible_h5_path):
                    h5_paths.add(possible_h5_path)
        return list(h5_paths)

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

    def get_object_by_identifier(self, identifier: Union[str, Uri]) -> Optional[Any]:
        """
        Search an object by its identifier.
        :param identifier: given by the function :func:`get_obj_identifier`, or a URI (or its str representation)
        :return:
        """
        is_uri = isinstance(identifier, Uri) or parse_uri(identifier) is not None
        id_str = str(identifier)
        for o in self.energyml_objects:
            if (get_obj_identifier(o) if not is_uri else str(get_obj_uri(o))) == id_str:
                return o
        return None

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        return self.get_object_by_identifier(identifier)

    def add_object(self, obj: Any) -> bool:
        """
        Add an energyml object to the EPC stream
        :param obj:
        :return:
        """
        self.energyml_objects.append(obj)
        return True

    def remove_object(self, identifier: Union[str, Uri]) -> None:
        """
        Remove an energyml object from the EPC stream by its identifier
        :param identifier:
        :return:
        """
        obj = self.get_object_by_identifier(identifier)
        if obj is not None:
            self.energyml_objects.remove(obj)

    def __len__(self) -> int:
        return len(self.energyml_objects)

    def add_rels_for_object(
        self,
        obj: Any,
        relationships: List[Relationship],
    ) -> None:
        """
        Add relationships to an object in the EPC stream
        :param obj:
        :param relationships:
        :return:
        """

        if isinstance(obj, str) or isinstance(obj, Uri):
            obj = self.get_object_by_identifier(obj)
            obj_ident = get_obj_identifier(obj)
        else:
            obj_ident = get_obj_identifier(obj)
        if obj_ident not in self.additional_rels:
            self.additional_rels[obj_ident] = []

        self.additional_rels[obj_ident] = self.additional_rels[obj_ident] + relationships

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
        """Read an external array from HDF5 files linked to the EPC file.
        :param energyml_array: the energyml array object (e.g. FloatingPointExternalArray)
        :param root_obj: the root object containing the energyml_array
        :param path_in_root: the path in the root object to the energyml_array
        :param use_epc_io_h5: if True, use also the in-memory HDF5 files stored in epc.h5_io_files

        :return: the array read from the external datasets
        """
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

    def read_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        """
        Read a data array from external storage (HDF5, Parquet, CSV, etc.) with optional sub-selection.

        :param proxy: The object identifier/URI or the object itself that references the array
        :param path_in_external: Path within the external file (e.g., 'values/0')
        :param start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
        :param counts: Optional count of elements for each dimension (RESQML v2.2 Count)
        :param external_uri: Optional URI to override default file path (RESQML v2.2 URI)
        :return: The data array as a numpy array, or None if not found
        """
        obj = proxy
        if isinstance(proxy, str) or isinstance(proxy, Uri):
            obj = self.get_object_by_identifier(proxy)

        # Determine which external files to use
        file_paths = [external_uri] if external_uri else self.get_h5_file_paths(obj)
        if not file_paths or len(file_paths) == 0:
            file_paths = self.external_files_path

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return None

        # Get the file handler registry
        handler_registry = get_handler_registry()

        for file_path in file_paths:
            # Get the appropriate handler for this file type
            handler = handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Use handler to read array with sub-selection support
                array = handler.read_array(file_path, path_in_external, start_indices, counts)
                if array is not None:
                    return array
            except Exception as e:
                logging.debug(f"Failed to read dataset from {file_path}: {e}")
                pass

        logging.error(f"Failed to read array from any available file paths: {file_paths}")
        return None

    def write_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        array: np.ndarray,
        start_indices: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """
        Write a data array to external storage (HDF5, Parquet, CSV, etc.) with optional offset.

        :param proxy: The object identifier/URI or the object itself that references the array
        :param path_in_external: Path within the external file (e.g., 'values/0')
        :param array: The numpy array to write
        :param start_indices: Optional start index for each dimension for partial writes
        :param external_uri: Optional URI to override default file path (RESQML v2.2 URI)
        :param kwargs: Additional format-specific parameters (e.g., dtype, column_titles)
        :return: True if successfully written, False otherwise
        """
        obj = proxy
        if isinstance(proxy, str) or isinstance(proxy, Uri):
            obj = self.get_object_by_identifier(proxy)

        # Determine which external files to use
        file_paths = [external_uri] if external_uri else self.get_h5_file_paths(obj)
        if not file_paths or len(file_paths) == 0:
            file_paths = self.external_files_path

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return False

        # Get the file handler registry
        handler_registry = get_handler_registry()

        # Try to write to the first available file
        for file_path in file_paths:
            # Get the appropriate handler for this file type
            handler = handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Use handler to write array with optional partial write support
                success = handler.write_array(file_path, array, path_in_external, start_indices, **kwargs)
                if success:
                    return True
            except Exception as e:
                logging.error(f"Failed to write dataset to {file_path}: {e}")

        logging.error(f"Failed to write array to any available file paths: {file_paths}")
        return False

    # Class methods

    @classmethod
    def read_file(cls, epc_file_path: str) -> "Epc":
        with open(epc_file_path, "rb") as f:
            epc = cls.read_stream(BytesIO(f.read()))
            epc.epc_file_path = epc_file_path
            return epc
        raise IOError(f"Failed to open EPC file {epc_file_path}")

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
                            except Exception:
                                logging.error(traceback.format_exc())
                                logging.error(
                                    f"Epc.@read_stream failed to parse file {ov_path} for content-type: {ov_ct} => {str(get_class_from_content_type(ov_ct))}\n\n",
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
                                except IOError:
                                    logging.error(traceback.format_exc())
                            elif f_info.filename != "_rels/.rels":  # CoreProperties rels file
                                # RELS FILES READING START

                                # logging.debug(f"reading rels {f_info.filename}")
                                rels_path = Path(f_info.filename)
                                obj_folder = (
                                    str(rels_path.parent.parent) + "/" if str(rels_path.parent.parent) != "." else ""
                                )
                                obj_file_name = rels_path.stem  # removing the ".rels"
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

    def list_objects(self, dataspace: str | None = None, object_type: str | None = None) -> List[ResourceMetadata]:
        result = []
        for obj in self.energyml_objects:
            if (dataspace is None or get_obj_type(get_obj_usable_class(obj)) == dataspace) and (
                object_type is None or get_qualified_type_from_class(type(obj)) == object_type
            ):
                res_meta = ResourceMetadata(
                    uri=str(get_obj_uri(obj)),
                    uuid=get_obj_uuid(obj),
                    title=get_object_attribute(obj, "citation.title") or "",
                    object_type=type(obj).__name__,
                    version=get_obj_version(obj),
                    content_type=get_content_type_from_class(type(obj)) or "",
                )
                result.append(res_meta)
        return result

    def put_object(self, obj: Any, dataspace: str | None = None) -> str | None:
        if self.add_object(obj):
            return str(get_obj_uri(obj))
        return None

    def delete_object(self, identifier: Union[str, Any]) -> bool:
        obj = self.get_object_by_identifier(identifier)
        if obj is not None:
            self.remove_object(identifier)
            return True
        return False

    def get_array_metadata(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        """
        Get metadata for data array(s) without loading the full array data.
        Supports RESQML v2.2 sub-array selection metadata.

        :param proxy: The object identifier/URI or the object itself that references the array
        :param path_in_external: Optional specific path. If None, returns all array metadata for the object
        :param start_indices: Optional start index for each dimension (RESQML v2.2 StartIndex)
        :param counts: Optional count of elements for each dimension (RESQML v2.2 Count)
        :return: DataArrayMetadata if path specified, List[DataArrayMetadata] if no path, or None if not found
        """
        obj = proxy
        if isinstance(proxy, str) or isinstance(proxy, Uri):
            obj = self.get_object_by_identifier(proxy)

        # Get possible file paths for this object
        file_paths = self.get_h5_file_paths(obj)
        if not file_paths or len(file_paths) == 0:
            file_paths = self.external_files_path

        if not file_paths:
            logging.warning(f"No external file paths found for proxy: {proxy}")
            return None

        # Get the file handler registry
        handler_registry = get_handler_registry()

        for file_path in file_paths:
            # Get the appropriate handler for this file type
            handler = handler_registry.get_handler_for_file(file_path)
            if handler is None:
                logging.debug(f"No handler found for file: {file_path}")
                continue

            try:
                # Use handler to get metadata without loading full array
                metadata_dict = handler.get_array_metadata(file_path, path_in_external, start_indices, counts)

                if metadata_dict is None:
                    continue

                # Convert dict(s) to DataArrayMetadata
                if isinstance(metadata_dict, list):
                    return [
                        DataArrayMetadata(
                            path_in_resource=m.get("path"),
                            array_type=m.get("dtype", "unknown"),
                            dimensions=m.get("shape", []),
                            start_indices=start_indices,
                            custom_data={"size": m.get("size", 0)},
                        )
                        for m in metadata_dict
                    ]
                else:
                    return DataArrayMetadata(
                        path_in_resource=metadata_dict.get("path"),
                        array_type=metadata_dict.get("dtype", "unknown"),
                        dimensions=metadata_dict.get("shape", []),
                        start_indices=start_indices,
                        custom_data={"size": metadata_dict.get("size", 0)},
                    )
            except Exception as e:
                logging.debug(f"Failed to get metadata from file {file_path}: {e}")

        return None

    def dumps_epc_content_and_files_lists(self) -> str:
        """
        Dumps the EPC content and files lists for debugging purposes.
        :return: A string representation of the EPC content and files lists.
        """
        content_list = [
            f"{get_obj_identifier(obj)} ({get_qualified_type_from_class(type(obj))})" for obj in self.energyml_objects
        ]
        raw_files_list = [raw_file.path for raw_file in self.raw_files]

        return "EPC Content:\n" + "\n".join(content_list) + "\n\nRaw Files:\n" + "\n".join(raw_files_list)

    def close(self) -> None:
        """
        Close the EPC file and release any resources.
        :return:
        """
        pass


#     ______                                      __   ____                 __  _
#    / ____/___  ___  _________ ___  ______ ___  / /  / __/_  ______  _____/ /_(_)___  ____  _____
#   / __/ / __ \/ _ \/ ___/ __ `/ / / / __ `__ \/ /  / /_/ / / / __ \/ ___/ __/ / __ \/ __ \/ ___/
#  / /___/ / / /  __/ /  / /_/ / /_/ / / / / / / /  / __/ /_/ / / / / /__/ /_/ / /_/ / / / (__  )
# /_____/_/ /_/\___/_/   \__, /\__, /_/ /_/ /_/_/  /_/  \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/
#                       /____//____/

# Backward compatibility: re-export functions that were moved to epc_utils
# This allows existing code that imports these functions from epc.py to continue working
from .epc_utils import (
    get_rels_dor_type,
    update_prop_kind_dict_cache,
    get_property_kind_by_uuid,
    get_property_kind_and_parents,
    as_dor,
    create_energyml_object,
    create_external_part_reference,
    get_reverse_dor_list,
    get_file_folder_and_name_from_path,
)

# Also export the cache dict for backward compatibility
from .epc_utils import __CACHE_PROP_KIND_DICT__

__all__ = [
    "Epc",
    "update_prop_kind_dict_cache",
    "get_property_kind_by_uuid",
    "get_property_kind_and_parents",
    "as_dor",
    "create_energyml_object",
    "create_external_part_reference",
    "get_reverse_dor_list",
    "get_file_folder_and_name_from_path",
    "__CACHE_PROP_KIND_DICT__",
]


# def gen_rels_path_from_dor(dor: Any, export_version: EpcExportVersion = EpcExportVersion.CLASSIC) -> str:
