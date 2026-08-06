# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Low level ZIP helpers used to rewrite an archive without paying for the
decompression/recompression of the entries that did not change.

The :mod:`zipfile` module cannot modify an existing archive in place: updating a
single part means rebuilding the whole file. The naive way to do that
(``dst.writestr(info, src.read(name))``) inflates and re-deflates *every* entry,
which dominates the cost by an order of magnitude on a real EPC:

    rewrite of a 2.8 MB / 3360 parts EPC, decompress + recompress : 0.485 s
    same rewrite, raw stream copy                                 : 0.030 s

:func:`rewrite_zip` copies the already-deflated bytes of the untouched entries
straight from the source file, and only compresses what actually changed.

Implementation note: this reaches into a few ``zipfile`` attributes that are not
part of the documented API (``ZipInfo.header_offset``, ``ZipFile.fp`` and
``ZipFile.start_dir``). Every raw copy is guarded and falls back to the plain
decompress/recompress path when anything looks unexpected, so a change in the
standard library degrades performance but never correctness.

The extra field of copied entries is dropped: it only carries optional metadata
(extended timestamps, unix uid/gid) that has no meaning in an EPC, and dropping
it avoids having to reconcile a stale Zip64 extra with the one ``zipfile``
regenerates for large entries.
"""

import logging
import os
import shutil
import struct
import tempfile
import warnings
import zipfile
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)

_LOCAL_HEADER_SIGNATURE = b"PK\x03\x04"
_LOCAL_HEADER_SIZE = 30

__all__ = [
    "iter_effective_infos",
    "rewrite_zip",
    "append_to_zip",
    "count_shadowed_entries",
]


def iter_effective_infos(zf: zipfile.ZipFile) -> Iterator[zipfile.ZipInfo]:
    """
    Iterate over the entries of ``zf`` that are actually reachable by name.

    A ZIP archive may contain several entries sharing the same name (that is what
    makes append-based updates possible). ``zipfile`` resolves a name to the
    **last** matching entry of the central directory; this generator yields
    exactly those, in file order, so that a rewrite drops the shadowed ones.
    """
    for info in zf.infolist():
        if zf.NameToInfo.get(info.filename) is info:
            yield info


def count_shadowed_entries(zf: zipfile.ZipFile) -> int:
    """Number of entries kept in the archive but shadowed by a later one of the same name."""
    return len(zf.infolist()) - len(zf.NameToInfo)


def _read_raw_entry(src_fp, info: zipfile.ZipInfo) -> Optional[bytes]:
    """
    Read the compressed payload of ``info`` straight from the source file object.

    Returns ``None`` when the local header cannot be trusted, which tells the
    caller to fall back to the decompress/recompress path.
    """
    try:
        src_fp.seek(info.header_offset)
        header = src_fp.read(_LOCAL_HEADER_SIZE)
        if len(header) != _LOCAL_HEADER_SIZE or not header.startswith(_LOCAL_HEADER_SIGNATURE):
            return None
        name_len, extra_len = struct.unpack("<HH", header[26:_LOCAL_HEADER_SIZE])
        src_fp.seek(info.header_offset + _LOCAL_HEADER_SIZE + name_len + extra_len)
        data = src_fp.read(info.compress_size)
        if len(data) != info.compress_size:
            return None
        return data
    except Exception as e:  # pragma: no cover - defensive
        logger.debug(f"Raw read failed for {info.filename}: {e}")
        return None


def _copy_entry_raw(src_fp, info: zipfile.ZipInfo, dst: zipfile.ZipFile) -> bool:
    """
    Append ``info`` to ``dst`` without touching its compressed payload.

    Returns True on success, False when the caller must fall back to a regular
    (decompress + recompress) copy.
    """
    data = _read_raw_entry(src_fp, info)
    if data is None:
        return False

    try:
        copy = zipfile.ZipInfo(info.filename, info.date_time)
        copy.compress_type = info.compress_type
        copy.comment = info.comment
        copy.extra = b""
        copy.create_system = info.create_system
        copy.create_version = info.create_version
        copy.extract_version = info.extract_version
        # bit 3 marks a trailing data descriptor: we write the real sizes in the
        # local header, so it must be cleared.
        copy.flag_bits = info.flag_bits & ~0x08
        copy.internal_attr = info.internal_attr
        copy.external_attr = info.external_attr
        copy.CRC = info.CRC
        copy.compress_size = info.compress_size
        copy.file_size = info.file_size

        fp = dst.fp
        copy.header_offset = fp.tell()
        fp.write(copy.FileHeader(zip64=None))
        fp.write(data)

        dst.filelist.append(copy)
        dst.NameToInfo[copy.filename] = copy
        dst.start_dir = fp.tell()
        dst._didModify = True
        return True
    except Exception as e:  # pragma: no cover - defensive
        logger.debug(f"Raw copy failed for {info.filename}, falling back: {e}")
        return False


def rewrite_zip(
    source: Optional[Union[str, Path]],
    target: Union[str, Path],
    updates: Optional[Dict[str, bytes]] = None,
    deleted: Optional[Union[Set[str], Iterable[str]]] = None,
    compression: int = zipfile.ZIP_DEFLATED,
    allow_raw_copy: bool = True,
) -> Tuple[int, int]:
    """
    Write ``target`` from ``source`` applying ``updates`` and ``deleted``.

    Entries of ``source`` that are neither updated nor deleted are copied with
    their compressed payload untouched when possible.

    :param source: archive to copy from, or None to create ``target`` from scratch
    :param target: path of the archive to write; may be the same file as ``source``
                   (the write then goes through a temporary file)
    :param updates: part path -> new content, written (and compressed) as-is
    :param deleted: part paths to drop
    :param compression: compression used for the entries of ``updates``
    :param allow_raw_copy: set to False to force the decompress/recompress path
    :return: (number of entries raw-copied, number of entries re-compressed)
    """
    updates = updates or {}
    deleted = set(deleted or ())
    source_path = Path(source) if source is not None else None
    target_path = Path(target)

    in_place = (
        source_path is not None
        and source_path.exists()
        and target_path.exists()
        and os.path.samefile(source_path, target_path)
    )

    if in_place:
        fd, tmp_name = tempfile.mkstemp(suffix=".epc", dir=str(target_path.parent))
        os.close(fd)
        write_to = Path(tmp_name)
    else:
        write_to = target_path

    raw_copied = 0
    recompressed = 0
    skipped = deleted | set(updates.keys())

    try:
        with zipfile.ZipFile(write_to, "w", compression, allowZip64=True) as dst:
            if source_path is not None and source_path.exists():
                with zipfile.ZipFile(source_path, "r") as src, open(source_path, "rb") as src_fp:
                    for info in iter_effective_infos(src):
                        if info.filename in skipped:
                            continue
                        if allow_raw_copy and _copy_entry_raw(src_fp, info, dst):
                            raw_copied += 1
                        else:
                            dst.writestr(info, src.read(info.filename))
                            recompressed += 1

            for path, data in updates.items():
                dst.writestr(path, data)
                recompressed += 1

        if in_place:
            shutil.move(str(write_to), str(target_path))
    except Exception:
        if in_place and write_to.exists():
            try:
                os.unlink(write_to)
            except OSError:  # pragma: no cover - defensive
                pass
        raise

    return raw_copied, recompressed


def append_to_zip(
    target: Union[str, Path],
    updates: Dict[str, bytes],
    compression: int = zipfile.ZIP_DEFLATED,
) -> None:
    """
    Append parts to an existing archive without rewriting it.

    An appended entry whose name already exists shadows the previous one: readers
    resolve a name through the central directory, where the appended entry comes
    last. The shadowed bytes stay in the file until it is rewritten, which is what
    :func:`rewrite_zip` does when compacting.

    Note that this cannot express a deletion.
    """
    if not updates:
        return
    with warnings.catch_warnings():
        # zipfile warns on duplicate names; here it is the intended mechanism.
        warnings.filterwarnings("ignore", message="Duplicate name", category=UserWarning)
        with zipfile.ZipFile(target, "a", compression, allowZip64=True) as zf:
            for path, data in updates.items():
                zf.writestr(path, data)
