import datetime
import re
import uuid
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from io import BytesIO
from typing import List, Any, Union, Dict

from energyml.opc.opc import CoreProperties, Relationships, Types, Default, Relationship, Override

from .manager import get_class_pkg, get_class_pkg_version
from .xml import is_energyml_content_type

try:
    from introspection import get_object_attribute_rgx, get_class_from_content_type
except ImportError:
    from utils.introspection import get_object_attribute_rgx, get_class_from_content_type

from .serialization import (
    serialize_xml, read_energyml_xml_str, read_energyml_xml_bytes, read_energyml_xml_bytes_as_class
)


RELS_CONTENT_TYPE = "application/vnd.openxmlformats-package.core-properties+xml"


class EpcExportVersion(Enum):
    """EPC export version."""

    #: Classical export
    CLASSIC = 1

    #: Export with objet path sorted by package (eml/resqml/witsml/prodml)
    EXPANDED = 2


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

    """ Additional rels for objects. Key is the object (same than in @energyml_objects) and value is a list of
        RelationShip. This can be used to link an HDF5 to an ExternalPartReference in resqml 2.0.1 
    """
    additional_rels: Dict[Any, List[Relationship]] = field(
        default_factory=lambda: {}
    )

    def __str__(self):
        return (
                "EPC file (" + str(self.export_version) + ") "
                + f"{len(self.energyml_objects)} energyml objects and {len(self.raw_files)} other files"
        )

    def gen_opc_content_type(self) -> Types:
        ct = Types()
        rels_default = Default()
        rels_default.content_type = RELS_CONTENT_TYPE
        rels_default.extension = "rels"

        ct.default = [rels_default]

        ct.override = []
        for e_obj in self.energyml_objects:
            ct.override.append(Override(content_type=get_content_type_from_class(e_obj), part_name=gen_energyml_object_path(e_obj, self.export_version)))

        return ct

    def gen_content_type_file(self) -> Types:
        content_type = Types()

        for obj in self.energyml_objects:
            content_type.override.append(Override(
                content_type=get_content_type_from_class(type(obj)),
                part_name=gen_energyml_object_path(obj, self.export_version),
            ))
        return content_type

    def export_file(self, path: str) -> None:
        epc_io = self.export_io()

        with open(path, "wb") as f:
            f.write(epc_io.getbuffer())

    def export_io(self) -> BytesIO:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for e_obj in self.energyml_objects:
                e_path = gen_energyml_object_path(e_obj)
                zip_info = zipfile.ZipInfo(filename=e_path, date_time=datetime.datetime.now().timetuple()[:6])
                data = serialize_xml(e_obj)
                zip_file.writestr(zip_info, data)

        return zip_buffer

    def _export_rels(self, output: BytesIO) -> None:
        pass

    def _export_energyml_objects(self, output: BytesIO) -> None:
        # TODO
        pass

    def _export_content_type(self, output: BytesIO) -> None:
        # TODO
        pass

    def _export_raw_files(self, output: BytesIO) -> None:
        # TODO
        pass

    def compute_rels(self) -> Dict[Any, Relationships]:
        # TODO
        return None

    @classmethod
    def read_file(cls, epc_file_path: str):
        with open(epc_file_path, "rb") as f:
            return cls.read_stream(BytesIO(f.read()))

    @classmethod
    def read_stream(cls, input: BytesIO):  # returns an Epc instance

        try:
            obj_list = []
            raw_file_list = []
            core_props = None
            with zipfile.ZipFile(input, "r", zipfile.ZIP_DEFLATED) as epc_file:
                content_type_file_name = "[Content_Types].xml"
                content_type_info = None
                try:
                    content_type_info = epc_file.getinfo(content_type_file_name)
                except KeyError:
                    for info in epc_file.infolist():
                        if info.filename.lower() == content_type_file_name.lower():
                            content_type_info = info
                            break

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

                            obj_list.append(
                                read_energyml_xml_bytes_as_class(epc_file.read(ov_path),
                                                                 get_class_from_content_type(ov_ct)
                                                                 )
                            )
                        elif get_class_from_content_type(ov_ct) == CoreProperties:
                            core_props = read_energyml_xml_bytes_as_class(epc_file.read(ov_path), CoreProperties)

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


def get_qualified_type_from_class(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    return get_data_object_type(cls, print_dev_version, nb_max_version_digits) + "." + get_object_type_for_file_path_from_class(cls);


def get_content_type_from_class(cls: Union[type, Any], print_dev_version=True, nb_max_version_digits=2):
    return ("application/x-" + get_class_pkg(cls)
            + "+xml;version=" + get_class_pkg_version(cls, print_dev_version, nb_max_version_digits) + ";type="
            + get_object_type_for_file_path_from_class(cls))


def get_object_type_for_file_path_from_class(cls) -> str:
    obj_type = get_obj_type(cls)
    pkg = get_class_pkg(cls)
    if re.match(r"Obj[A-Z].*", obj_type) is not None and pkg == "resqml":
        return "obj_" + obj_type[3:]
    return obj_type


def gen_energyml_object_path(energyml_object: Union[str, Any], export_version: EpcExportVersion = EpcExportVersion.CLASSIC):
    if isinstance(energyml_object, str):
        energyml_object = read_energyml_xml_str(energyml_object)

    obj_type = get_object_type_for_file_path_from_class(energyml_object.__class__)

    pkg = get_class_pkg(energyml_object)
    pkg_version = get_class_pkg_version(energyml_object)
    object_version = get_obj_version(energyml_object)
    if object_version is None:
        object_version = "0"

    if export_version == EpcExportVersion.EXPANDED:
        return pkg + "/" + get_obj_uuid(energyml_object) + pkg_version + "/" + object_version + ".xml"
    else:
        return obj_type + "_" + get_obj_uuid(energyml_object) + ".xml"


def now(time_zone=timezone(timedelta(hours=1), "UTC")) -> int:
    return int(datetime.timestamp(datetime.now(time_zone)))


def epoch(time_zone=timezone(timedelta(hours=1), "UTC")) -> int:
    return int(now(time_zone))


def date_to_epoch(date: str) -> int:
    """
    Transform a energyml date into an epoch datetime
    :return: int
    """
    return int(datetime.fromisoformat(date).timestamp())


def epoch_to_date(epoch: int, time_zone=timezone(timedelta(hours=1), "UTC")) -> str:
    date = datetime.fromtimestamp(epoch / 1e3, time_zone)
    return date.strftime("%Y-%m-%dT%H:%M:%S%z")


def gen_uuid() -> str:
    return str(uuid.uuid4())


def get_obj_type(obj: Any) -> str:
    if isinstance(obj, type):
        return str(obj.__name__)
    return get_obj_type(type(obj))


def get_obj_uuid(obj: Any) -> str:
    return get_object_attribute_rgx(obj, "[Uu]u?id|UUID")


def get_obj_version(obj: Any) -> str:
    return get_object_attribute_rgx(obj, "ObjectVersion")
