# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for the raw ZIP stream copy used to rewrite EPC files cheaply.

The point of these tests is that a raw-copied archive must be indistinguishable
from a decompress/recompress one for any reader: same names, same content, same
CRC, and ``testzip()`` clean.
"""
import os
import tempfile
import zipfile

import pytest

from energyml.utils.zip_raw import (
    append_to_zip,
    count_shadowed_entries,
    iter_effective_infos,
    rewrite_zip,
)

SAMPLE_PARTS = {
    "[Content_Types].xml": b"<?xml version='1.0'?><Types/>",
    "a.xml": b"<a>" + b"x" * 5000 + b"</a>",
    "folder/b.xml": "<b>accentué € ☃</b>".encode("utf-8"),
    "_rels/.rels": b"<Relationships/>",
    "binary.bin": bytes(range(256)) * 40,
    "empty.txt": b"",
}


@pytest.fixture
def sample_zip():
    fd, path = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in SAMPLE_PARTS.items():
            zf.writestr(name, data)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def out_path():
    fd, path = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    os.unlink(path)
    yield path
    if os.path.exists(path):
        os.unlink(path)


def read_all(path):
    with zipfile.ZipFile(path) as zf:
        assert zf.testzip() is None
        return {name: zf.read(name) for name in zf.namelist()}


class TestRewriteZip:
    def test_pure_copy_preserves_everything(self, sample_zip, out_path):
        raw_copied, recompressed = rewrite_zip(sample_zip, out_path)

        assert raw_copied == len(SAMPLE_PARTS)
        assert recompressed == 0
        assert read_all(out_path) == SAMPLE_PARTS

    def test_raw_copy_matches_the_recompressed_result(self, sample_zip, out_path):
        fd, slow_path = tempfile.mkstemp(suffix=".zip")
        os.close(fd)
        os.unlink(slow_path)
        try:
            rewrite_zip(sample_zip, out_path, allow_raw_copy=True)
            rewrite_zip(sample_zip, slow_path, allow_raw_copy=False)
            assert read_all(out_path) == read_all(slow_path)

            with zipfile.ZipFile(out_path) as fast, zipfile.ZipFile(slow_path) as slow:
                assert {i.filename: i.CRC for i in fast.infolist()} == {i.filename: i.CRC for i in slow.infolist()}
        finally:
            if os.path.exists(slow_path):
                os.unlink(slow_path)

    def test_update_and_delete(self, sample_zip, out_path):
        rewrite_zip(
            sample_zip,
            out_path,
            updates={"a.xml": b"<a>new</a>", "added.xml": b"<added/>"},
            deleted={"binary.bin"},
        )

        content = read_all(out_path)
        assert content["a.xml"] == b"<a>new</a>"
        assert content["added.xml"] == b"<added/>"
        assert "binary.bin" not in content
        assert content["folder/b.xml"] == SAMPLE_PARTS["folder/b.xml"]

    def test_in_place_rewrite(self, sample_zip):
        rewrite_zip(sample_zip, sample_zip, updates={"a.xml": b"<a>in place</a>"})

        content = read_all(sample_zip)
        assert content["a.xml"] == b"<a>in place</a>"
        assert len(content) == len(SAMPLE_PARTS)

    def test_creation_without_source(self, out_path):
        rewrite_zip(None, out_path, updates={"only.xml": b"<only/>"})
        assert read_all(out_path) == {"only.xml": b"<only/>"}

    def test_deleting_everything_yields_a_valid_empty_archive(self, sample_zip, out_path):
        rewrite_zip(sample_zip, out_path, deleted=set(SAMPLE_PARTS))
        assert read_all(out_path) == {}

    def test_shadowed_entries_are_dropped(self, sample_zip, out_path):
        append_to_zip(sample_zip, {"a.xml": b"<a>shadowing</a>"})
        with zipfile.ZipFile(sample_zip) as zf:
            assert count_shadowed_entries(zf) == 1

        rewrite_zip(sample_zip, out_path)

        content = read_all(out_path)
        assert content["a.xml"] == b"<a>shadowing</a>"
        with zipfile.ZipFile(out_path) as zf:
            assert count_shadowed_entries(zf) == 0
            assert len(zf.infolist()) == len(SAMPLE_PARTS)

    def test_source_is_left_untouched_when_the_write_fails(self, sample_zip, out_path):
        before = read_all(sample_zip)

        class Unwritable:
            def __len__(self):
                raise RuntimeError("boom")

        with pytest.raises(Exception):
            rewrite_zip(sample_zip, sample_zip, updates={"a.xml": Unwritable()})

        assert read_all(sample_zip) == before


class TestAppendToZip:
    def test_appended_entry_is_readable(self, sample_zip):
        append_to_zip(sample_zip, {"new.xml": b"<new/>"})
        assert read_all(sample_zip)["new.xml"] == b"<new/>"

    def test_appending_an_existing_name_shadows_it(self, sample_zip):
        append_to_zip(sample_zip, {"a.xml": b"<a>v2</a>"})

        with zipfile.ZipFile(sample_zip) as zf:
            assert zf.read("a.xml") == b"<a>v2</a>"
            assert zf.namelist().count("a.xml") == 2
            assert [i.filename for i in iter_effective_infos(zf)].count("a.xml") == 1

    def test_empty_update_is_a_noop(self, sample_zip):
        before = os.path.getsize(sample_zip)
        append_to_zip(sample_zip, {})
        assert os.path.getsize(sample_zip) == before
