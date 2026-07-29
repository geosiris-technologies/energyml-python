# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Lazy, write-buffered EPC handler.

:class:`EpcFile` sits between the two existing implementations of
:class:`~energyml.utils.storage_interface.EnergymlStorageInterface`:

- :class:`~energyml.utils.epc.Epc` deserialises every part when reading and
  re-serialises every part when writing;
- :class:`~energyml.utils.epc_stream.EpcStreamReader` loads objects lazily but
  reads the full XML of every part while indexing, and rebuilds the whole ZIP
  (decompressing and recompressing every entry) on each single modification.

:class:`EpcFile` indexes the archive from its central directory and
``[Content_Types].xml`` only, deserialises a part when it is actually asked for,
buffers modifications in memory, and writes the archive at most once — copying
the compressed payload of untouched parts verbatim (see
:mod:`energyml.utils.zip_raw`).

When ``[Content_Types].xml`` is missing, truncated, or disagrees with the actual
content of the archive, the index falls back to listing the ZIP entries and
sniffing the root element of the undeclared XML parts, so a damaged package
still opens.

Persistence is driven by :class:`EpcAccessMode`::

    with EpcFile("f.epc", mode=EpcAccessMode.READ_ONLY) as epc:   # no write allowed
    with EpcFile("f.epc", mode=EpcAccessMode.IN_MEMORY) as epc:   # edit, never persisted
    with EpcFile("f.epc", mode=EpcAccessMode.MANUAL) as epc:      # persisted on save()
    with EpcFile("f.epc") as epc:                                 # persisted on close()
    with EpcFile("f.epc", mode=EpcAccessMode.IMMEDIATE) as epc:   # persisted on each write

Instances are not thread-safe.
"""

import logging
import os
import re
import zipfile
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

import numpy as np
from lxml import etree as ETREE

from energyml.opc.opc import (
    CoreProperties,
    Default,
    Override,
    Relationship,
    Relationships,
    Types,
)
from energyml.utils.constants import (
    EPCRelsRelationshipType,
    EpcExportVersion,
    MimeType,
    OptimizedRegex,
    date_to_datetime,
)
from energyml.utils.data.datasets_io import get_handler_registry
from energyml.utils.epc_stream import RelsUpdateMode
from energyml.utils.epc_utils import (
    EXPANDED_EXPORT_FOLDER_PREFIX,
    create_default_core_properties,
    create_default_types,
    create_external_relationship,
    gen_core_props_path,
    gen_core_props_rels_path,
    gen_energyml_object_path,
    gen_rels_path_from_obj_path,
    get_dor_or_external_uris_from_obj,
    get_epc_content_type_path,
    get_epc_content_type_rels_path,
    get_file_folder,
    get_rels_dor_type,
    in_epc_file_path_to_mime_type,
    is_core_prop_or_extension_path,
    make_path_relative_to_filepath_list,
    make_path_relative_to_other_file,
    relationships_equal,
)
from energyml.utils.introspection import (
    gen_uuid,
    get_class_from_content_type,
    get_content_type_from_class,
    get_obj_title,
    get_obj_uri,
    get_object_attribute_advanced,
)
from energyml.utils.manager import reshape_version
from energyml.utils.serialization import read_energyml_xml_bytes, serialize_xml
from energyml.utils.storage_interface import (
    DataArrayMetadata,
    EnergymlStorageInterface,
    ResourceMetadata,
    create_resource_metadata_from_uri,
)
from energyml.utils.uri import Uri, create_uri_from_content_type_or_qualified_type, parse_uri
from energyml.utils.xml_utils import (
    find_schema_version_in_element,
    get_pkg_from_namespace,
    get_root_namespace,
    is_energyml_content_type,
)
from energyml.utils.zip_raw import append_to_zip, count_shadowed_entries, rewrite_zip

__all__ = [
    "EpcAccessMode",
    "EpcFile",
    "EpcFileStats",
    "ReadOnlyEpcError",
]

_DEFAULT_HEAD_SIZE = 8192
"""Bytes read from the head of a part when resolving its citation lazily."""

# Deliberately tolerant: the namespace prefix differs between versions (`eml:`,
# `eml20:`, `eml23:`, none at all) and the tags carry attributes in 2.0.1
# (`<eml20:Title xsi:type="eml20:DescriptionString">`).
_RE_OBJECT_VERSION = re.compile(rb'\bobjectVersion\s*=\s*"([^"]*)"')
_RE_UUID_ATTR = re.compile(rb'\buuid\s*=\s*"([^"]*)"', re.IGNORECASE)
_RE_TITLE = re.compile(rb"<(?:[\w.\-]+:)?Title\b[^>]*>(.*?)</", re.DOTALL)
_RE_LAST_UPDATE = re.compile(rb"<(?:[\w.\-]+:)?LastUpdate\b[^>]*>(.*?)</", re.DOTALL)


class ReadOnlyEpcError(RuntimeError):
    """Raised when a modification is attempted on an EPC opened read-only."""


class EpcAccessMode(Enum):
    """
    How modifications made through an :class:`EpcFile` reach the disk.

    READ_ONLY  Any modification raises :class:`ReadOnlyEpcError`. Cheapest mode:
               nothing is ever buffered nor written.
    IN_MEMORY  Modifications are kept in an in-memory overlay and never written
               to the source file, not even on close. Use
               :meth:`EpcFile.save_as` to materialise them elsewhere.
    MANUAL     Modifications are buffered until :meth:`EpcFile.save` is called.
               Closing with pending modifications logs a warning and discards them.
    ON_CLOSE   Modifications are buffered and written once, on :meth:`EpcFile.close`
               (or when leaving the ``with`` block). Default: one archive rewrite
               per session instead of one per modification.
    IMMEDIATE  Every modification is written straight away. Additions and updates
               are appended to the archive, which is O(what changed) rather than
               O(archive); deletions still force a rewrite. The archive is
               compacted on close to drop the shadowed entries.
    """

    READ_ONLY = "read_only"
    IN_MEMORY = "in_memory"
    MANUAL = "manual"
    ON_CLOSE = "on_close"
    IMMEDIATE = "immediate"

    @property
    def allows_write(self) -> bool:
        """True when the mode accepts modifications at all."""
        return self is not EpcAccessMode.READ_ONLY

    @property
    def persists(self) -> bool:
        """True when modifications can reach the source file."""
        return self in (EpcAccessMode.MANUAL, EpcAccessMode.ON_CLOSE, EpcAccessMode.IMMEDIATE)


@dataclass
class EpcFileStats:
    """Counters describing what an :class:`EpcFile` actually had to do."""

    parts_indexed: int = 0
    objects_indexed: int = 0
    parts_sniffed: int = 0
    """Parts whose type had to be guessed because [Content_Types].xml did not declare them."""
    head_reads: int = 0
    """Bounded reads done to resolve a citation (title / version / last update)."""
    objects_deserialized: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    bytes_read: int = 0
    flushes: int = 0
    parts_raw_copied: int = 0
    parts_recompressed: int = 0

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total else 0.0


@dataclass
class _ObjectEntry:
    """
    Index entry for one energyml part. Everything past the path and the content
    type is resolved on demand.
    """

    path: str
    content_type: str
    uuid: str
    declared: bool = True
    """False when the part was not declared in [Content_Types].xml."""

    version: Optional[str] = None
    title: Optional[str] = None
    last_changed: Optional[datetime] = None
    head_resolved: bool = False
    """True once the citation has been read (or filled in from a put_object)."""

    _uri: Optional[Uri] = field(default=None, repr=False)

    @property
    def uri(self) -> Uri:
        if self._uri is None or self._uri.version != self.version:
            self._uri = create_uri_from_content_type_or_qualified_type(self.content_type, self.uuid, self.version)
        return self._uri

    @property
    def identifier(self) -> str:
        return self.uri.as_identifier()

    @property
    def qualified_type(self) -> str:
        return self.uri.get_qualified_type()

    def to_resource_metadata(self) -> ResourceMetadata:
        return create_resource_metadata_from_uri(self.uri, title=self.title, last_changed=self.last_changed)


def _sniff_root_element(head: bytes) -> Optional[Any]:
    """
    Parse just enough of ``head`` to get the root element with its attributes.

    Works on a truncated document, which is the point: identifying a part must
    not require reading it whole.
    """
    try:
        parser = ETREE.XMLPullParser(events=("start",), recover=True)
        parser.feed(head)
        for _, element in parser.read_events():
            return element
    except Exception as e:
        logging.debug(f"Failed to sniff XML head: {e}")
    return None


def _content_type_from_head(head: bytes) -> Optional[str]:
    """
    Derive the content type of an energyml part from the first bytes of its XML.

    Built from the XML alone — root namespace, ``schemaVersion`` and root type —
    rather than by resolving the python class: indexing a package must not
    require its data model package to be installed, exactly like indexing from
    ``[Content_Types].xml`` does not.

    The object type is taken from the ``xsi:type`` attribute when present, since
    that is where 2.0.1 carries the ``obj_`` prefixed form the content type uses
    (``<resqml20:PointSetRepresentation xsi:type="resqml20:obj_PointSetRepresentation">``).
    """
    root = _sniff_root_element(head)
    if root is None:
        return None
    try:
        package = get_pkg_from_namespace(get_root_namespace(root))
        if package is None or package == "opc":
            return None
        schema_version = find_schema_version_in_element(root)
        if not schema_version:
            return None
        version = reshape_version(schema_version, 2)

        xsi_type = root.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        object_type = xsi_type.split(":")[-1] if xsi_type else ETREE.QName(root).localname
        if not object_type:
            return None
        return f"application/x-{package}+xml;version={version};type={object_type}"
    except Exception as e:
        logging.debug(f"Failed to derive the content type from the XML head: {e}")
        return None


def _decode(value: Optional[bytes]) -> Optional[str]:
    if value is None:
        return None
    return value.decode("utf-8", errors="ignore").strip() or None


def _serialize(obj: Any) -> bytes:
    """
    Serialise to bytes.

    ``serialize_xml`` returns ``str``; the overlay stores bytes so that a part
    read back from it behaves exactly like one read from the archive.
    """
    data = serialize_xml(obj)
    return data.encode("utf-8") if isinstance(data, str) else data


class EpcFile(EnergymlStorageInterface):
    """
    Lazy EPC reader/writer with buffered writes.

    :param epc_file_path: path of the EPC. Created empty when missing and the mode
                          allows writing.
    :param mode: persistence policy, see :class:`EpcAccessMode`.
    :param export_version: packaging used for *new* parts. Detected from the
                           archive when it already contains parts.
    :param rels_update_mode: when relationships are recomputed for modified objects.
    :param cache_size: number of deserialised objects kept in the LRU cache.
    :param scan_undeclared_parts: sniff the XML parts that ``[Content_Types].xml``
                                  does not declare. Disable to trust it blindly.
    :param compact_on_close: in IMMEDIATE mode, rewrite the archive on close to
                             drop the entries shadowed by appends.
    :param force_h5_path: bypass relationship resolution for external arrays.
    """

    def __init__(
        self,
        epc_file_path: Union[str, Path],
        mode: EpcAccessMode = EpcAccessMode.ON_CLOSE,
        export_version: EpcExportVersion = EpcExportVersion.CLASSIC,
        rels_update_mode: RelsUpdateMode = RelsUpdateMode.UPDATE_AT_MODIFICATION,
        cache_size: int = 128,
        scan_undeclared_parts: bool = True,
        compact_on_close: bool = True,
        force_h5_path: Optional[str] = None,
        compression: int = zipfile.ZIP_DEFLATED,
        head_size: int = _DEFAULT_HEAD_SIZE,
    ):
        self.epc_file_path = Path(epc_file_path)
        self.mode = mode
        self.rels_update_mode = rels_update_mode
        self.cache_size = max(1, cache_size)
        self.scan_undeclared_parts = scan_undeclared_parts
        self.compact_on_close = compact_on_close
        self.force_h5_path = force_h5_path
        self.compression = compression
        self.head_size = head_size
        self.stats = EpcFileStats()

        self.export_version = export_version

        # --- index (built at open, never holds a part body) ---
        self._zip_entries: Dict[str, zipfile.ZipInfo] = {}
        self._by_path: Dict[str, _ObjectEntry] = {}
        self._by_uuid: Dict[str, List[_ObjectEntry]] = {}
        self._core_props_path: Optional[str] = None

        # --- write overlay ---
        self._pending: Dict[str, bytes] = {}
        self._deleted: Set[str] = set()
        self._content_types_dirty = False
        self._pending_rels_rebuild: Set[str] = set()

        # --- caches ---
        self._object_cache: "OrderedDict[str, Any]" = OrderedDict()
        self._zip: Optional[zipfile.ZipFile] = None
        self._closed = False

        if not self.epc_file_path.exists():
            if not mode.allows_write:
                raise FileNotFoundError(f"EPC file not found: {self.epc_file_path}")
            self._create_empty_epc()
        elif not zipfile.is_zipfile(self.epc_file_path):
            raise ValueError(f"File is not a valid ZIP/EPC file: {self.epc_file_path}")

        self._build_index()

    # ------------------------------------------------------------------
    # Index
    # ------------------------------------------------------------------

    def _create_empty_epc(self) -> None:
        """Create the minimal valid EPC structure for a file that does not exist yet."""
        core_props = create_default_core_properties()
        parts = {
            get_epc_content_type_path(): _serialize(create_default_types()),
            gen_core_props_path(): _serialize(core_props),
            gen_core_props_rels_path(): _serialize(Relationships()),
            get_epc_content_type_rels_path(): _serialize(
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
        self.epc_file_path.parent.mkdir(parents=True, exist_ok=True)
        rewrite_zip(None, self.epc_file_path, updates=parts, compression=self.compression)

    def _open_zip(self) -> zipfile.ZipFile:
        if self._zip is None:
            self._zip = zipfile.ZipFile(self.epc_file_path, "r")
        return self._zip

    def _close_zip(self) -> None:
        if self._zip is not None:
            try:
                self._zip.close()
            except Exception as e:  # pragma: no cover - defensive
                logging.debug(f"Error closing ZIP handle: {e}")
            self._zip = None

    def _build_index(self) -> None:
        """
        Build the object index from the central directory and ``[Content_Types].xml``.

        No part body is read, except for the XML parts the content types fail to
        describe correctly (and only when ``scan_undeclared_parts`` is set).
        """
        self._by_path.clear()
        self._by_uuid.clear()

        zf = self._open_zip()
        self._zip_entries = {info.filename: info for info in zf.infolist()}
        self.stats.parts_indexed = len(self._zip_entries)

        # Packaging is readable from the paths alone.
        if any(name.lstrip("/").startswith(EXPANDED_EXPORT_FOLDER_PREFIX) for name in self._zip_entries):
            self.export_version = EpcExportVersion.EXPANDED

        for part_name, content_type in self._read_declared_content_types().items():
            if content_type == MimeType.CORE_PROPERTIES.value:
                # Only believe it when the path agrees: real packages exist where
                # object parts are declared with the core properties content type.
                if is_core_prop_or_extension_path(part_name):
                    self._core_props_path = part_name
                continue
            try:
                if not is_energyml_content_type(content_type):
                    continue
            except Exception:
                continue
            self._register_part(part_name, content_type, declared=True)

        if self.scan_undeclared_parts:
            # Anything that looks like an object part and did not come out of the
            # content types is identified from its own root element. That covers a
            # missing [Content_Types].xml as well as one declaring a part with the
            # wrong content type.
            for part_name in self._zip_entries:
                if part_name in self._by_path or not self._is_candidate_object_part(part_name):
                    continue
                self._sniff_and_register(part_name)

        if self._core_props_path is None and gen_core_props_path() in self._zip_entries:
            self._core_props_path = gen_core_props_path()

        if self.stats.parts_sniffed:
            logging.info(
                f"{self.epc_file_path}: {self.stats.parts_sniffed} part(s) identified by reading their root element "
                f"because {get_epc_content_type_path()} does not describe them usably"
            )

        self.stats.objects_indexed = len(self._by_path)

    def _read_declared_content_types(self) -> Dict[str, str]:
        """
        Read ``[Content_Types].xml`` and keep only the overrides that match a part
        actually present in the archive.

        An override pointing at a missing part is dropped rather than trusted: it
        is the usual symptom of a package edited by a tool that forgot to update
        the content types, and keeping it would surface objects that cannot be read.
        """
        data = self._read_part(get_epc_content_type_path())
        if data is None:
            for name in self._zip_entries:
                if name.lower() == get_epc_content_type_path().lower():
                    data = self._read_part(name)
                    break
        if data is None:
            logging.warning(f"No {get_epc_content_type_path()} in {self.epc_file_path}, indexing from the ZIP listing")
            return {}

        try:
            types = read_energyml_xml_bytes(data, Types)
        except Exception as e:
            logging.warning(f"Unreadable {get_epc_content_type_path()} ({e}), indexing from the ZIP listing")
            return {}

        result: Dict[str, str] = {}
        for override in types.override or []:
            if not override.part_name or not override.content_type:
                continue
            part_name = override.part_name.lstrip("/\\")
            if part_name not in self._zip_entries:
                logging.debug(f"Content type declares a missing part, ignored: {part_name}")
                continue
            result[part_name] = override.content_type
        return result

    @staticmethod
    def _is_candidate_object_part(part_name: str) -> bool:
        """True for the parts that could hold an energyml object."""
        lowered = part_name.lower()
        if not lowered.endswith(".xml"):
            return False
        if lowered.startswith("[content_types]") or "/_rels/" in lowered or lowered.startswith("_rels/"):
            return False
        if part_name in (gen_core_props_path(), f"/{gen_core_props_path()}"):
            return False
        return True

    def _sniff_and_register(self, part_name: str) -> None:
        """Identify an undeclared XML part from its root element."""
        head = self._read_part_head(part_name, self.head_size)
        if not head:
            return
        content_type = _content_type_from_head(head)
        if content_type is None:
            logging.debug(f"Undeclared part not recognised as energyml, ignored: {part_name}")
            return
        entry = self._register_part(part_name, content_type, declared=False, head=head)
        if entry is not None:
            self.stats.parts_sniffed += 1
            logging.debug(f"Part not usable from the content types, recovered by sniffing: {part_name}")

    def _register_part(
        self, part_name: str, content_type: str, declared: bool, head: Optional[bytes] = None
    ) -> Optional[_ObjectEntry]:
        """Add an energyml part to the index, deriving its uuid from the path or the head."""
        uuid = self._uuid_from_path(part_name)
        if uuid is None:
            head = head if head is not None else self._read_part_head(part_name, self.head_size)
            match = _RE_UUID_ATTR.search(head or b"")
            uuid = _decode(match.group(1)) if match else None
        if not uuid:
            logging.warning(f"Cannot determine the uuid of part {part_name}, ignored")
            return None

        entry = _ObjectEntry(path=part_name, content_type=content_type, uuid=uuid, declared=declared)
        if head is not None:
            self._fill_from_head(entry, head)
        self._by_path[part_name] = entry
        self._by_uuid.setdefault(uuid, []).append(entry)
        return entry

    @staticmethod
    def _uuid_from_path(part_name: str) -> Optional[str]:
        match = OptimizedRegex.UUID_NO_GRP.search(part_name)
        return match.group(0) if match is not None else None

    # ------------------------------------------------------------------
    # Lazy citation resolution
    # ------------------------------------------------------------------

    def _read_part_head(self, part_name: str, size: int) -> Optional[bytes]:
        """Read at most ``size`` bytes of a part, honouring the write overlay."""
        if part_name in self._deleted:
            return None
        if part_name in self._pending:
            return self._pending[part_name][:size]
        if part_name not in self._zip_entries:
            return None
        try:
            with self._open_zip().open(part_name) as f:
                data = f.read(size)
            self.stats.bytes_read += len(data)
            self.stats.head_reads += 1
            return data
        except Exception as e:
            logging.debug(f"Failed to read the head of {part_name}: {e}")
            return None

    def _fill_from_head(self, entry: _ObjectEntry, head: bytes) -> None:
        version = _RE_OBJECT_VERSION.search(head)
        if version is not None:
            entry.version = _decode(version.group(1))
        title = _RE_TITLE.search(head)
        if title is not None:
            entry.title = _decode(title.group(1))
        last_update = _RE_LAST_UPDATE.search(head)
        if last_update is not None:
            raw = _decode(last_update.group(1))
            try:
                entry.last_changed = date_to_datetime(raw) if raw else None
            except Exception:
                entry.last_changed = None
        entry.head_resolved = title is not None

    def _resolve_entry(self, entry: _ObjectEntry) -> _ObjectEntry:
        """
        Resolve the citation of an entry (object version, title, last update).

        Reads a bounded head first and only falls back to the whole part when the
        citation is further in. Idempotent.
        """
        if entry.head_resolved:
            return entry
        head = self._read_part_head(entry.path, self.head_size)
        if head:
            self._fill_from_head(entry, head)
        if not entry.head_resolved:
            info = self._zip_entries.get(entry.path)
            bigger = entry.path in self._pending or (info is not None and info.file_size > self.head_size)
            if bigger:
                whole = self._read_part(entry.path)
                if whole:
                    self._fill_from_head(entry, whole)
        entry.head_resolved = True
        return entry

    def resolve_all(self) -> None:
        """
        Resolve the citation of every indexed object.

        Only useful when titles are needed for the whole package; this is the one
        operation whose cost is proportional to the size of the EPC.
        """
        for entry in list(self._by_path.values()):
            self._resolve_entry(entry)

    # ------------------------------------------------------------------
    # Parts
    # ------------------------------------------------------------------

    def _read_part(self, part_name: str) -> Optional[bytes]:
        """Read a whole part, honouring the write overlay."""
        if part_name in self._deleted:
            return None
        if part_name in self._pending:
            return self._pending[part_name]
        if part_name not in self._zip_entries:
            return None
        try:
            data = self._open_zip().read(part_name)
        except KeyError:
            return None
        self.stats.bytes_read += len(data)
        return data

    def _part_exists(self, part_name: str) -> bool:
        if part_name in self._deleted:
            return False
        return part_name in self._pending or part_name in self._zip_entries

    def list_parts(self) -> List[str]:
        """All part paths currently in the package, overlay included."""
        names = set(self._zip_entries) - self._deleted
        names.update(self._pending)
        return sorted(names)

    def get_part(self, part_name: str) -> Optional[bytes]:
        """Raw content of any part (energyml or not)."""
        return self._read_part(part_name)

    def put_part(self, part_name: str, data: bytes) -> None:
        """
        Add or replace a non-energyml part (a PDF, an image, ...).

        Use :meth:`put_object` for energyml objects.
        """
        self._check_writable()
        self._pending[part_name] = data
        self._deleted.discard(part_name)
        self._content_types_dirty = True
        self._after_write()

    def delete_part(self, part_name: str) -> bool:
        """Remove any part from the package."""
        self._check_writable()
        if not self._part_exists(part_name):
            return False
        self._pending.pop(part_name, None)
        if part_name in self._zip_entries:
            self._deleted.add(part_name)
        self._content_types_dirty = True
        self._after_write()
        return True

    # ------------------------------------------------------------------
    # Object lookup
    # ------------------------------------------------------------------

    @staticmethod
    def _split_identifier(identifier: Union[str, Uri, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Split an identifier into (uuid, version).

        A version of ``None`` means "any", which is what a bare uuid or a trailing
        dot (``uuid.``) asks for.
        """
        if identifier is None:
            return None, None
        if isinstance(identifier, Uri):
            return identifier.uuid, identifier.version or None
        if isinstance(identifier, str):
            text = identifier.strip()
            if text.startswith("eml:///"):
                try:
                    uri = parse_uri(text)
                    return uri.uuid, uri.version or None
                except Exception:
                    return None, None
            match = OptimizedRegex.UUID_NO_GRP.search(text)
            if match is None:
                return None, None
            uuid = match.group(0)
            rest = text[match.end() :]
            if rest.startswith("."):
                rest = rest[1:]
            return uuid, rest or None
        uri = get_obj_uri(obj=identifier, dataspace=None)
        if uri is not None:
            return uri.uuid, uri.version or None
        return None, None

    def _find_entries(self, identifier: Union[str, Uri, Any]) -> List[_ObjectEntry]:
        """Entries matching an identifier, resolving versions only when needed."""
        uuid, version = self._split_identifier(identifier)
        if uuid is None:
            return []
        candidates = list(self._by_uuid.get(uuid, ()))
        if not candidates or version is None:
            return candidates
        # A version was requested: resolving it costs one bounded head read per
        # candidate, and there is normally exactly one.
        return [entry for entry in candidates if self._resolve_entry(entry).version == version]

    def get_object(self, identifier: Union[str, Uri]) -> Optional[Any]:
        entries = self._find_entries(identifier)
        if not entries:
            logging.debug(f"No object found for identifier {identifier}")
            return None
        if len(entries) > 1:
            logging.debug(f"{len(entries)} objects share the uuid of {identifier}, returning the first one")
        return self._load(entries[0])

    def get_object_by_uuid(self, uuid: str) -> List[Any]:
        objects = [self._load(entry) for entry in self._by_uuid.get(uuid, ())]
        return [obj for obj in objects if obj is not None]

    def _load(self, entry: _ObjectEntry) -> Optional[Any]:
        """Deserialise a part, through the LRU cache."""
        cached = self._object_cache.get(entry.path)
        if cached is not None:
            self._object_cache.move_to_end(entry.path)
            self.stats.cache_hits += 1
            return cached
        self.stats.cache_misses += 1

        data = self._read_part(entry.path)
        if data is None:
            logging.warning(f"Part {entry.path} is indexed but unreadable")
            return None
        try:
            cls = get_class_from_content_type(entry.content_type)
            obj = read_energyml_xml_bytes(data, cls)
        except Exception as e:
            logging.error(f"Failed to deserialise {entry.path}: {e}")
            return None

        self.stats.objects_deserialized += 1
        self._cache_object(entry.path, obj)
        return obj

    def _cache_object(self, part_name: str, obj: Any) -> None:
        self._object_cache[part_name] = obj
        self._object_cache.move_to_end(part_name)
        while len(self._object_cache) > self.cache_size:
            self._object_cache.popitem(last=False)

    def clear_cache(self) -> None:
        """Drop the deserialised objects. Pending modifications are unaffected."""
        self._object_cache.clear()

    def list_objects(
        self,
        dataspace: Optional[str] = None,
        object_type: Optional[str] = None,
        resolve_titles: bool = True,
    ) -> List[ResourceMetadata]:
        """
        Metadata of the indexed objects.

        ``object_type`` accepts a qualified type (``resqml22.TriangulatedSetRepresentation``)
        as well as a bare type (``TriangulatedSetRepresentation``), the latter
        being what :attr:`ResourceMetadata.object_type` carries. The filter is
        applied on the index, so it never triggers a read. Pass
        ``resolve_titles=False`` to skip the citation resolution entirely.
        """
        entries = list(self._by_path.values())
        if object_type:
            entries = [entry for entry in entries if object_type in (entry.qualified_type, entry.uri.object_type)]
        if resolve_titles:
            entries = [self._resolve_entry(entry) for entry in entries]
        return [entry.to_resource_metadata() for entry in entries]

    def get_object_path(self, identifier: Union[str, Uri, Any]) -> Optional[str]:
        """
        In-package path of an object.

        Always the path found in the archive, never one regenerated from the
        metadata, so a package whose naming does not match what this library would
        produce stays readable.
        """
        entries = self._find_entries(identifier)
        return entries[0].path if entries else None

    @property
    def core_properties(self) -> Optional[CoreProperties]:
        if self._core_props_path is None:
            return None
        data = self._read_part(self._core_props_path)
        if data is None:
            return None
        try:
            return read_energyml_xml_bytes(data, CoreProperties)
        except Exception as e:
            logging.warning(f"Failed to read the core properties: {e}")
            return None

    @core_properties.setter
    def core_properties(self, core_props: CoreProperties) -> None:
        self._check_writable()
        path = self._core_props_path or gen_core_props_path()
        self._core_props_path = path
        self._pending[path] = _serialize(core_props)
        self._deleted.discard(path)
        self._content_types_dirty = True
        self._after_write()

    # ------------------------------------------------------------------
    # Object modification
    # ------------------------------------------------------------------

    def _check_writable(self) -> None:
        if self._closed:
            raise RuntimeError("This EpcFile is closed")
        if not self.mode.allows_write:
            raise ReadOnlyEpcError(
                f"{self.epc_file_path} is opened in {self.mode.name} mode; reopen it with a writable EpcAccessMode"
            )

    def _after_write(self) -> None:
        """Persist right away in IMMEDIATE mode, otherwise let the overlay grow."""
        if self.mode is EpcAccessMode.IMMEDIATE:
            self.flush()

    @property
    def has_pending_changes(self) -> bool:
        """True when modifications are buffered and not yet written."""
        return bool(self._pending or self._deleted or self._content_types_dirty)

    def put_object(self, obj: Any, dataspace: Optional[str] = None) -> Optional[str]:
        self._check_writable()

        uri = get_obj_uri(obj=obj, dataspace=None)
        if uri is None:
            raise ValueError("Failed to build a URI for the object, cannot store it in the EPC")

        existing = self._find_entries(uri)
        # Reuse the path already in the package when updating, so the naming of a
        # foreign package is preserved.
        path = existing[0].path if existing else gen_energyml_object_path(obj, self.export_version)
        content_type = get_content_type_from_class(obj)

        self._pending[path] = _serialize(obj)
        self._deleted.discard(path)

        entry = self._by_path.get(path)
        if entry is None:
            entry = _ObjectEntry(path=path, content_type=content_type, uuid=uri.uuid)
            self._by_path[path] = entry
            self._by_uuid.setdefault(uri.uuid, []).append(entry)
            self._content_types_dirty = True
        entry.content_type = content_type
        entry.version = uri.version or None
        entry.title = get_obj_title(obj)
        entry.last_changed = self._object_last_update(obj)
        entry.head_resolved = True

        self._cache_object(path, obj)

        if self.rels_update_mode is RelsUpdateMode.UPDATE_AT_MODIFICATION:
            self._stage_rels_for(obj, entry)
        elif self.rels_update_mode is RelsUpdateMode.UPDATE_ON_CLOSE:
            self._pending_rels_rebuild.add(path)

        self._after_write()
        return entry.identifier

    def add_object(self, obj: Any, replace_if_exists: bool = True) -> Optional[str]:
        """Store an object, optionally refusing to overwrite an existing one."""
        if not replace_if_exists:
            uri = get_obj_uri(obj=obj, dataspace=None)
            if uri is not None and self._find_entries(uri):
                raise ValueError(f"Object {uri.as_identifier()} already exists and replace_if_exists is False")
        return self.put_object(obj)

    def delete_object(self, identifier: Union[str, Uri, Any]) -> bool:
        self._check_writable()

        entries = self._find_entries(identifier)
        if not entries:
            logging.warning(f"No object to delete for identifier {identifier}")
            return False

        for entry in entries:
            rels_path = gen_rels_path_from_obj_path(entry.path)
            # Read the .rels before dropping it: it is what tells us which other
            # objects have to be fixed up.
            own_rels = self._read_rels(rels_path)
            for path in (entry.path, rels_path):
                self._pending.pop(path, None)
                if path in self._zip_entries:
                    self._deleted.add(path)
            self._object_cache.pop(entry.path, None)
            self._by_path.pop(entry.path, None)
            siblings = self._by_uuid.get(entry.uuid, [])
            if entry in siblings:
                siblings.remove(entry)
            if not siblings:
                self._by_uuid.pop(entry.uuid, None)
            self._pending_rels_rebuild.discard(entry.path)
            self._drop_incoming_rels(entry.path, own_rels)

        self._content_types_dirty = True
        self._after_write()
        return True

    def remove_object(self, identifier: Union[str, Uri, Any]) -> bool:
        """Alias of :meth:`delete_object`."""
        return self.delete_object(identifier)

    @staticmethod
    def _object_last_update(obj: Any) -> Optional[datetime]:
        raw = get_object_attribute_advanced(obj, "citation.lastUpdate")
        if isinstance(raw, datetime):
            return raw
        if isinstance(raw, str):
            try:
                return date_to_datetime(raw)
            except Exception:
                return None
        return None

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def _read_rels(self, rels_path: str) -> List[Relationship]:
        data = self._read_part(rels_path)
        if not data:
            return []
        try:
            return list(read_energyml_xml_bytes(data, Relationships).relationship or [])
        except Exception as e:
            logging.warning(f"Failed to read {rels_path}: {e}")
            return []

    def _write_rels(self, rels_path: str, rels: List[Relationship]) -> None:
        self._pending[rels_path] = _serialize(Relationships(relationship=rels))
        self._deleted.discard(rels_path)

    @staticmethod
    def _merge_rels(existing: List[Relationship], additions: List[Relationship]) -> List[Relationship]:
        merged = list(existing)
        for addition in additions:
            if not any(relationships_equal(addition, current) for current in merged):
                merged.append(addition)
        return merged

    def get_obj_rels(self, obj: Union[str, Uri, Any]) -> List[Relationship]:
        path = self.get_object_path(obj)
        if path is None:
            return []
        return self._read_rels(gen_rels_path_from_obj_path(path))

    def _stage_rels_for(self, obj: Any, entry: _ObjectEntry) -> None:
        """
        Recompute the relationships touched by storing ``obj``.

        Only the ``.rels`` of the object and of the objects it points at are read
        and rewritten; everything else in the package is left alone.
        """
        try:
            dor_uris, external_uris = get_dor_or_external_uris_from_obj(obj)
        except Exception as e:
            logging.warning(f"Failed to extract the references of {entry.path}: {e}")
            return

        own_path = entry.path
        own_rels_path = gen_rels_path_from_obj_path(own_path)
        additions: List[Relationship] = []

        for dor_uri in dor_uris:
            target_entries = self._find_entries(dor_uri)
            if not target_entries:
                logging.debug(f"{own_path} references {dor_uri}, absent from the package")
                continue
            target_path = target_entries[0].path
            additions.append(
                Relationship(
                    target=target_path,
                    type_value=get_rels_dor_type(dor_uri, in_dor_owner_rels_file=True),
                    id=f"_{gen_uuid()}",
                )
            )
            # Mirror the SOURCE relationship in the target's own .rels.
            target_rels_path = gen_rels_path_from_obj_path(target_path)
            back = Relationship(
                target=own_path,
                type_value=get_rels_dor_type(dor_uri, in_dor_owner_rels_file=False),
                id=f"_{gen_uuid()}",
            )
            self._write_rels(target_rels_path, self._merge_rels(self._read_rels(target_rels_path), [back]))

        for external_uri, _mime_type in external_uris:
            if external_uri:
                additions.append(create_external_relationship(external_uri))

        existing = [rel for rel in self._read_rels(own_rels_path) if rel.target not in (None, own_path)]
        self._write_rels(own_rels_path, self._merge_rels(existing, additions))

    def _drop_incoming_rels(self, removed_path: str, own_rels: List[Relationship]) -> None:
        """
        Remove the relationships pointing at a part that has just been removed.

        Only the ``.rels`` of the neighbours are touched: an object's own ``.rels``
        lists both the objects it points at and the ones pointing at it, so the
        number of files to fix is its degree in the reference graph, not the size
        of the package.
        """
        for rel in own_rels:
            target = rel.target
            if not target or target not in self._by_path:
                continue
            neighbour_rels_path = gen_rels_path_from_obj_path(target)
            existing = self._read_rels(neighbour_rels_path)
            kept = [candidate for candidate in existing if candidate.target != removed_path]
            if len(kept) != len(existing):
                self._write_rels(neighbour_rels_path, kept)

    def rebuild_all_rels(self) -> int:
        """
        Recompute every ``.rels`` from the references found in the objects.

        Unlike the rest of this class, this loads every object. Returns the number
        of ``.rels`` parts written.
        """
        self._check_writable()
        for rels_path in [name for name in self.list_parts() if name.endswith(".rels")]:
            if rels_path not in (get_epc_content_type_rels_path(), gen_core_props_rels_path()):
                self._pending[rels_path] = _serialize(Relationships())
                self._deleted.discard(rels_path)

        written_before = len(self._pending)
        for entry in list(self._by_path.values()):
            obj = self._load(entry)
            if obj is not None:
                self._stage_rels_for(obj, entry)
        self._pending_rels_rebuild.clear()
        self._after_write()
        return len(self._pending) - written_before

    # ------------------------------------------------------------------
    # Content types
    # ------------------------------------------------------------------

    def _gen_content_types(self) -> Types:
        """Regenerate ``[Content_Types].xml`` from the index and the part listing."""
        types = Types(default=[Default(extension="rels", content_type=str(MimeType.RELS))], override=[])

        core_path = self._core_props_path or gen_core_props_path()
        if self._part_exists(core_path):
            types.override.append(Override(content_type=str(MimeType.CORE_PROPERTIES), part_name=f"/{core_path}"))

        for entry in self._by_path.values():
            types.override.append(Override(content_type=entry.content_type, part_name=f"/{entry.path}"))

        known = set(self._by_path) | {core_path, get_epc_content_type_path()}
        for part_name in self.list_parts():
            if part_name in known or part_name.endswith(".rels"):
                continue
            mime_type = in_epc_file_path_to_mime_type(part_name)
            if mime_type:
                types.override.append(Override(content_type=mime_type, part_name=f"/{part_name}"))

        return types

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _build_flush_payload(self) -> Dict[str, bytes]:
        """
        Parts to write out.

        ``[Content_Types].xml`` is only regenerated when the set of parts changed:
        updating an object in place leaves the content types untouched, and
        rebuilding them means re-serialising one override per object in the
        package, which dominates the cost of an otherwise tiny append.
        """
        payload = dict(self._pending)
        if self._content_types_dirty:
            payload[get_epc_content_type_path()] = _serialize(self._gen_content_types())
        return payload

    def flush(self) -> bool:
        """
        Write the buffered modifications to the source file.

        Appends when the mode is IMMEDIATE and nothing has to be removed;
        rewrites the archive otherwise, copying the compressed payload of the
        untouched parts verbatim.

        :return: True when something was written.
        """
        if not self.has_pending_changes:
            return False
        if self.mode is EpcAccessMode.IN_MEMORY:
            logging.warning(
                f"{self.epc_file_path} is opened in IN_MEMORY mode: modifications are not written. Use save_as()."
            )
            return False
        if not self.mode.allows_write:
            raise ReadOnlyEpcError(f"{self.epc_file_path} is opened read-only")

        if self.rels_update_mode is RelsUpdateMode.UPDATE_ON_CLOSE and self._pending_rels_rebuild:
            for path in list(self._pending_rels_rebuild):
                entry = self._by_path.get(path)
                if entry is not None:
                    obj = self._load(entry)
                    if obj is not None:
                        self._stage_rels_for(obj, entry)
            self._pending_rels_rebuild.clear()

        payload = self._build_flush_payload()
        can_append = self.mode is EpcAccessMode.IMMEDIATE and not self._deleted

        self._close_zip()
        if can_append:
            append_to_zip(self.epc_file_path, payload, compression=self.compression)
        else:
            raw_copied, recompressed = rewrite_zip(
                self.epc_file_path,
                self.epc_file_path,
                updates=payload,
                deleted=self._deleted,
                compression=self.compression,
            )
            self.stats.parts_raw_copied += raw_copied
            self.stats.parts_recompressed += recompressed

        self.stats.flushes += 1
        self._pending.clear()
        self._deleted.clear()
        self._content_types_dirty = False

        self._zip_entries = {info.filename: info for info in self._open_zip().infolist()}
        return True

    def save(self) -> bool:
        """Alias of :meth:`flush`, for symmetry with :meth:`save_as`."""
        return self.flush()

    def save_as(self, target: Union[str, Path]) -> Path:
        """
        Write the package, modifications included, to another file.

        The current instance keeps pointing at its original file; this is the way
        to materialise an EPC edited in IN_MEMORY mode.
        """
        target_path = Path(target)
        if target_path.exists() and os.path.samefile(target_path, self.epc_file_path):
            self.flush()
            return self.epc_file_path

        target_path.parent.mkdir(parents=True, exist_ok=True)
        raw_copied, recompressed = rewrite_zip(
            self.epc_file_path,
            target_path,
            updates=self._build_flush_payload(),
            deleted=self._deleted,
            compression=self.compression,
        )
        self.stats.parts_raw_copied += raw_copied
        self.stats.parts_recompressed += recompressed
        return target_path

    def discard_changes(self) -> None:
        """Drop the buffered modifications and rebuild the index from the file."""
        self._pending.clear()
        self._deleted.clear()
        self._content_types_dirty = False
        self._pending_rels_rebuild.clear()
        self._object_cache.clear()
        self._build_index()

    def compact(self) -> bool:
        """
        Rewrite the archive to drop the entries shadowed by IMMEDIATE-mode appends.

        No-op when there is nothing to reclaim.
        """
        if not self.mode.persists:
            return False
        self.flush()
        if count_shadowed_entries(self._open_zip()) == 0:
            return False
        self._close_zip()
        raw_copied, recompressed = rewrite_zip(self.epc_file_path, self.epc_file_path, compression=self.compression)
        self.stats.parts_raw_copied += raw_copied
        self.stats.parts_recompressed += recompressed
        self._zip_entries = {info.filename: info for info in self._open_zip().infolist()}
        return True

    def close(self) -> None:
        if self._closed:
            return
        try:
            if self.mode is EpcAccessMode.ON_CLOSE and self.has_pending_changes:
                self.flush()
            elif self.mode is EpcAccessMode.MANUAL and self.has_pending_changes:
                logging.warning(
                    f"{self.epc_file_path} is closed with unsaved modifications "
                    f"({len(self._pending)} parts written, {len(self._deleted)} removed): "
                    f"they are discarded. Call save() to keep them."
                )
            elif self.mode is EpcAccessMode.IMMEDIATE and self.compact_on_close:
                self.compact()
        finally:
            self._close_zip()
            self._object_cache.clear()
            self._closed = True

    # ------------------------------------------------------------------
    # External arrays
    # ------------------------------------------------------------------

    def get_h5_file_paths(
        self, obj_or_id: Union[str, Uri, Any] = None, make_path_absolute_from_epc_path: bool = True
    ) -> List[str]:
        """External file paths reachable from an object's relationships, plus the EPC folder content."""
        if self.force_h5_path is not None:
            return [self.force_h5_path]

        paths: Set[str] = set()
        part_path = self.get_object_path(obj_or_id) if obj_or_id is not None else None
        if part_path is not None:
            for rel in self._read_rels(gen_rels_path_from_obj_path(part_path)):
                if rel.type_value == str(EPCRelsRelationshipType.EXTERNAL_RESOURCE) and rel.target:
                    paths.add(rel.target)

        if make_path_absolute_from_epc_path:
            paths = set(make_path_relative_to_filepath_list(list(paths), str(self.epc_file_path)))

        folder = get_file_folder(str(self.epc_file_path))
        if folder is not None and os.path.isdir(folder):
            for name in os.listdir(folder):
                if name.lower().endswith(".h5"):
                    paths.add(os.path.join(folder, name))

        return list(paths)

    def _candidate_array_files(self, proxy: Any, external_uri: Optional[str]) -> List[str]:
        paths = self.get_h5_file_paths(proxy)
        if external_uri:
            paths.insert(0, make_path_relative_to_other_file(external_uri, str(self.epc_file_path)))
        return paths

    def read_array(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        file_paths = self._candidate_array_files(proxy, external_uri)
        if not file_paths:
            logging.warning(f"No external file found for proxy: {proxy}")
            return None

        registry = get_handler_registry()
        for file_path in file_paths:
            handler = registry.get_handler_for_file(file_path)
            if handler is None:
                continue
            try:
                array = handler.read_array(file_path, path_in_external, start_indices, counts)
                if array is not None:
                    return array
            except Exception as e:
                logging.debug(f"Failed to read {path_in_external} from {file_path}: {e}")
        logging.error(f"Failed to read {path_in_external} from any of: {file_paths}")
        return None

    def read_array_view(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: str,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
        external_uri: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        file_paths = self._candidate_array_files(proxy, external_uri)
        if not file_paths:
            return None

        registry = get_handler_registry()
        for file_path in file_paths:
            handler = registry.get_handler_for_file(file_path)
            if handler is None:
                continue
            try:
                read_view = getattr(handler, "read_array_view", None)
                array = (
                    read_view(file_path, path_in_external, start_indices, counts)
                    if read_view is not None
                    else handler.read_array(file_path, path_in_external, start_indices, counts)
                )
                if array is not None:
                    return array
            except Exception as e:
                logging.debug(f"Failed to read_array_view from {file_path}: {e}")
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
        if external_uri is not None:
            folder = os.path.dirname(str(self.epc_file_path)) or "."
            file_paths = (
                [external_uri] if os.path.isabs(external_uri) else [os.path.join(folder, external_uri), external_uri]
            )
        elif self.force_h5_path is not None:
            file_paths = [self.force_h5_path]
        else:
            file_paths = self.get_h5_file_paths(proxy)

        if not file_paths:
            logging.warning(f"No external file found for proxy: {proxy}")
            return False

        registry = get_handler_registry()
        for file_path in file_paths:
            handler = registry.get_handler_for_file(file_path)
            if handler is None:
                continue
            try:
                if handler.write_array(file_path, array, path_in_external, start_indices, **kwargs):
                    return True
            except Exception as e:
                logging.error(f"Failed to write {path_in_external} to {file_path}: {e}")
        return False

    def get_array_metadata(
        self,
        proxy: Union[str, Uri, Any],
        path_in_external: Optional[str] = None,
        start_indices: Optional[List[int]] = None,
        counts: Optional[List[int]] = None,
    ) -> Union[DataArrayMetadata, List[DataArrayMetadata], None]:
        file_paths = [self.force_h5_path] if self.force_h5_path is not None else self.get_h5_file_paths(proxy)
        if not file_paths:
            logging.warning(f"No external file found for proxy: {proxy}")
            return None

        registry = get_handler_registry()
        for file_path in file_paths:
            handler = registry.get_handler_for_file(file_path)
            if handler is None:
                continue
            try:
                raw = handler.get_array_metadata(file_path, path_in_external, start_indices, counts)
            except Exception as e:
                logging.debug(f"Failed to read the array metadata of {file_path}: {e}")
                continue
            if raw is None:
                continue
            if isinstance(raw, list):
                return [self._to_array_metadata(item, start_indices) for item in raw]
            return self._to_array_metadata(raw, start_indices)
        return None

    @staticmethod
    def _to_array_metadata(raw: Dict[str, Any], start_indices: Optional[List[int]]) -> DataArrayMetadata:
        return DataArrayMetadata(
            path_in_resource=raw.get("path"),
            array_type=raw.get("dtype", "unknown"),
            dimensions=raw.get("shape", []),
            start_indices=start_indices,
            custom_data={"size": raw.get("size", 0)},
        )

    # ------------------------------------------------------------------
    # Dunder / misc
    # ------------------------------------------------------------------

    def get_object_dependencies(self, identifier: Union[str, Uri]) -> List[str]:
        """Identifiers of the objects referenced by this one."""
        obj = self.get_object(identifier)
        if obj is None:
            return []
        dor_uris, _ = get_dor_or_external_uris_from_obj(obj)
        return [uri.as_identifier() for uri in dor_uris]

    def __len__(self) -> int:
        return len(self._by_path)

    def __iter__(self) -> Iterator[str]:
        return iter(entry.identifier for entry in self._by_path.values())

    def __contains__(self, identifier: Union[str, Uri, Any]) -> bool:
        return bool(self._find_entries(identifier))

    def __enter__(self) -> "EpcFile":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None and self.mode is EpcAccessMode.ON_CLOSE and self.has_pending_changes:
            logging.warning(
                f"Leaving the context of {self.epc_file_path} on {exc_type.__name__}: "
                f"the pending modifications are discarded rather than written."
            )
            self._pending.clear()
            self._deleted.clear()
            self._content_types_dirty = False
        self.close()
        return False

    def __del__(self):
        try:
            if not self._closed:
                self._close_zip()
        except Exception:  # pragma: no cover - interpreter shutdown
            pass

    def __str__(self) -> str:
        return (
            f"EpcFile({self.epc_file_path}, {self.export_version.name}, mode={self.mode.name}) "
            f"{len(self._by_path)} objects / {len(self._zip_entries)} parts"
            + (f" [+{len(self._pending)} pending, -{len(self._deleted)} removed]" if self.has_pending_changes else "")
        )
