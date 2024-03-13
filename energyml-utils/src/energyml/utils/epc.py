import datetime
import re
import uuid as uuid_mod
import zipfile
from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from typing import List, Any, Union, Dict, Callable

from energyml.opc.opc import CoreProperties, Relationships, Types, Default, Relationship, Override

from .introspection import (
    get_object_attribute_rgx,
    get_class_from_content_type,
    get_obj_type, search_attribute_matching_type
)
from .manager import get_class_pkg, get_class_pkg_version
from .serialization import (
    serialize_xml, read_energyml_xml_str, read_energyml_xml_bytes, read_energyml_xml_bytes_as_class
)
from .xml import is_energyml_content_type

RELS_CONTENT_TYPE = "application/vnd.openxmlformats-package.core-properties+xml"


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

    def __str__(self):
        return (
                "EPC file (" + str(self.export_version) + ") "
                + f"{len(self.energyml_objects)} energyml objects and {len(self.raw_files)} other files {[f.path for f in self.raw_files]}"
        )

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

    def export_file(self, path: str) -> None:
        epc_io = self.export_io()
        with open(path, "wb") as f:
            f.write(epc_io.getbuffer())

    def export_io(self) -> BytesIO:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            #  Energyml objects
            for e_obj in self.energyml_objects:
                e_path = gen_energyml_object_path(e_obj)
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
                zip_info = zipfile.ZipInfo(filename=gen_core_props_path(self.export_version), date_time=datetime.datetime.now().timetuple()[:6])
                data = serialize_xml(self.core_props)
                zip_file.writestr(zip_info, data)

            # ContentType
            zip_info = zipfile.ZipInfo(filename=get_epc_content_type_path(), date_time=datetime.datetime.now().timetuple()[:6])
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
            gen_rels_path(map_obj_id_to_obj.get(obj_id)): Relationships(
                relationship=obj_rels + (self.additional_rels[obj_id] if obj_id in self.additional_rels else [])
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

    @classmethod
    def read_file(cls, epc_file_path: str):
        with open(epc_file_path, "rb") as f:
            return cls.read_stream(BytesIO(f.read()))

    @classmethod
    def read_stream(cls, epc_file_io: BytesIO):  # returns an Epc instance
        try:
            _read_files = []
            obj_list = []
            raw_file_list = []
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
                    for ov in content_type_obj.override:
                        ov_ct = ov.content_type
                        ov_path = ov.part_name
                        while ov_path.startswith("/") or ov_path.startswith("\\"):
                            ov_path = ov_path[1:]
                        if is_energyml_content_type(ov_ct):
                            _read_files.append(ov_path)
                            obj_list.append(
                                read_energyml_xml_bytes_as_class(
                                    epc_file.read(ov_path),
                                    get_class_from_content_type(ov_ct)
                                )
                            )
                        elif get_class_from_content_type(ov_ct) == CoreProperties:
                            _read_files.append(ov_path)
                            core_props = read_energyml_xml_bytes_as_class(epc_file.read(ov_path), CoreProperties)

                    for f_info in epc_file.infolist():
                        if f_info.filename not in _read_files and not f_info.filename.lower().endswith(".rels"):
                            _read_files.append(f_info.filename)
                            try:
                                raw_file_list.append(
                                    RawFile(
                                        path=f_info.filename,
                                        content=BytesIO(epc_file.read(f_info.filename)),
                                    )
                                )
                            except IOError as e:
                                print(e)

            return Epc(energyml_objects=obj_list, raw_files=raw_file_list, core_props=core_props)
        except zipfile.BadZipFile as error:
            print(error)

        return None


#     ______                                      __   ____                 __  _
#    / ____/___  ___  _________ ___  ______ ___  / /  / __/_  ______  _____/ /_(_)___  ____  _____
#   / __/ / __ \/ _ \/ ___/ __ `/ / / / __ `__ \/ /  / /_/ / / / __ \/ ___/ __/ / __ \/ __ \/ ___/
#  / /___/ / / /  __/ /  / /_/ / /_/ / / / / / / /  / __/ /_/ / / / / /__/ /_/ / /_/ / / / (__  )
# /_____/_/ /_/\___/_/   \__, /\__, /_/ /_/ /_/_/  /_/  \__,_/_/ /_/\___/\__/_/\____/_/ /_/____/
#                       /____//____/


def get_data_object_type(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    return get_class_pkg(cls) + "." + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits)


def get_qualified_type_from_class(cls: Union[type, Any], print_dev_version=True):
    return (
            get_data_object_type(cls, print_dev_version, 2)
            .replace(".", "") + "." + get_object_type_for_file_path_from_class(cls)
            )


def get_content_type_from_class(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    if not isinstance(cls, type):
        cls = type(cls)

    if ".opc." in cls.__module__:
        if cls.__name__.lower() == "coreproperties":
            return "application/vnd.openxmlformats-package.core-properties+xml"
    else:
        return ("application/x-" + get_class_pkg(cls)
                + "+xml;version=" + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits) + ";type="
                + get_object_type_for_file_path_from_class(cls))

    print(f"@get_content_type_from_class not supported type : {cls}")
    return None


def get_object_type_for_file_path_from_class(cls) -> str:
    obj_type = get_obj_type(cls)
    pkg = get_class_pkg(cls)
    if re.match(r"Obj[A-Z].*", obj_type) is not None and pkg == "resqml":
        return "obj_" + obj_type[3:]
    return obj_type


def now(time_zone=datetime.timezone(datetime.timedelta(hours=1), "UTC")) -> int:
    return int(datetime.datetime.timestamp(datetime.datetime.now(time_zone)))


def epoch(time_zone=datetime.timezone(datetime.timedelta(hours=1), "UTC")) -> int:
    return int(now(time_zone))


def date_to_epoch(date: str) -> int:
    """
    Transform a energyml date into an epoch datetime
    :return: int
    """
    return int(datetime.datetime.fromisoformat(date).timestamp())


def epoch_to_date(epoch_value: int, time_zone=datetime.timezone(datetime.timedelta(hours=1), "UTC")) -> str:
    date = datetime.datetime.fromtimestamp(epoch_value / 1e3, time_zone)
    return date.strftime("%Y-%m-%dT%H:%M:%S%z")


def gen_uuid() -> str:
    return str(uuid_mod.uuid4())


def get_obj_uuid(obj: Any) -> str:
    return get_object_attribute_rgx(obj, "[Uu]u?id|UUID")


def get_obj_version(obj: Any) -> str:
    return get_object_attribute_rgx(obj, "object_version")


def get_direct_dor_list(obj: Any) -> List[Any]:
    return search_attribute_matching_type(obj, "DataObjectreference")


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

    if object_version is None:
        object_version = "0"

    if export_version == EpcExportVersion.EXPANDED:
        return f"namespace_{pkg}{pkg_version.replace('.', '')}/{uuid}{('/version_' + object_version) if object_version is not None else ''}/{obj_type}_{uuid}.xml"
    else:
        return obj_type + "_" + uuid + ".xml"


def gen_rels_path(obj: Any) -> str:
    if isinstance(obj, CoreProperties):
        return ".rels/.rels"
    else:
        return f".rels/{gen_energyml_object_path(obj, EpcExportVersion.CLASSIC)}.rels"


def get_epc_content_type_path() -> str:
    return "[Content_Types].xml"
