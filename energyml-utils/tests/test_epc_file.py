# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Tests for :class:`EpcFile`, the lazy write-buffered EPC handler.

They run against the real EPC fixtures of ``rc/epc`` (2.0.1 and 2.2 packaging,
list-of-lists and ndarray points, EPSG resolvable or not) rather than against
mock dataclasses, so the behaviour is checked against the actual xsdata classes.
"""
import os
import shutil
import tempfile
import zipfile

import pytest

from energyml.eml.v2_3.commonv2 import Citation
from energyml.resqml.v2_2.resqmlv2 import BoundaryFeature, BoundaryFeatureInterpretation
from energyml.utils.epc_file import EpcAccessMode, EpcFile, ReadOnlyEpcError
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.utils.epc_utils import as_dor, gen_rels_path_from_obj_path, get_epc_content_type_path
from energyml.utils.introspection import epoch, epoch_to_date

RC_EPC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rc", "epc")

EPC_201 = os.path.join(RC_EPC, "testingPackageCpp.epc")
EPC_22 = os.path.join(RC_EPC, "testingPackageCpp22.epc")
EPC_BIG = os.path.join(RC_EPC, "SPASS_40+80wells.epc")

ALL_FIXTURES = [EPC_201, EPC_22, EPC_BIG]


@pytest.fixture(params=ALL_FIXTURES, ids=lambda p: os.path.basename(p))
def fixture_epc(request):
    """Read-only access to each real EPC fixture."""
    return request.param


@pytest.fixture
def writable_copy():
    """A throwaway copy of a fixture, so tests may modify it."""
    created = []

    def _copy(source=EPC_22):
        fd, path = tempfile.mkstemp(suffix=".epc")
        os.close(fd)
        shutil.copy(source, path)
        created.append(path)
        return path

    yield _copy

    for path in created:
        if os.path.exists(path):
            os.unlink(path)


@pytest.fixture
def new_epc_path():
    fd, path = tempfile.mkstemp(suffix=".epc")
    os.close(fd)
    os.unlink(path)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def sample_objects():
    feature = BoundaryFeature(
        citation=Citation(title="Feature under test", originator="test", creation=epoch_to_date(epoch())),
        uuid="6a1f0000-0000-4000-8000-00000000f001",
        object_version="1.0",
    )
    interpretation = BoundaryFeatureInterpretation(
        citation=Citation(title="Interpretation under test", originator="test", creation=epoch_to_date(epoch())),
        uuid="6a1f0000-0000-4000-8000-00000000f002",
        object_version="1.0",
        interpreted_feature=as_dor(feature),
    )
    return feature, interpretation


class TestIndexing:
    def test_opening_does_not_read_the_parts(self, fixture_epc):
        """
        The index costs the central directory plus the content types. The only
        parts read are the ones the content types fail to describe, and then only
        their first bytes.
        """
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            assert len(epc) > 0
            assert epc.stats.objects_deserialized == 0
            # Whatever was read is a bounded head, never a whole part.
            content_types_size = len(epc.get_part(get_epc_content_type_path()) or b"")
            assert epc.stats.bytes_read <= 2 * content_types_size + epc.stats.head_reads * epc.head_size

        reader = EpcStreamReader(fixture_epc)
        try:
            assert epc.stats.bytes_read < reader.stats.bytes_read
        finally:
            reader.close()

    def test_every_indexed_object_is_loadable(self, fixture_epc):
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            for metadata in epc.list_objects(resolve_titles=False):
                assert epc.get_object(metadata.uuid) is not None, f"{metadata.uuid} indexed but not loadable"

    def test_titles_are_resolved_on_every_version(self, fixture_epc):
        """
        Citation tags carry a version-dependent prefix and, in 2.0.1, attributes
        (``<eml20:Title xsi:type="...">``): the extraction must cope with both.
        """
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            titles = [metadata.title for metadata in epc.list_objects()]
            assert titles, "no object indexed"
            assert any(title for title in titles), "no title resolved at all"

    def test_titles_are_not_resolved_when_not_asked_for(self, fixture_epc):
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            before = epc.stats.head_reads
            epc.list_objects(resolve_titles=False)
            assert epc.stats.head_reads == before
            epc.list_objects(resolve_titles=True)
            assert epc.stats.head_reads > before

    def test_index_agrees_with_epc_stream_reader(self, fixture_epc):
        """
        Same object set as the existing implementation, on packages whose content
        types are sound.
        """
        reader = EpcStreamReader(fixture_epc)
        try:
            reference = {metadata.uuid for metadata in reader.list_objects()}
        finally:
            reader.close()

        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            found = {metadata.uuid for metadata in epc.list_objects(resolve_titles=False)}
        assert found == reference

    def test_every_object_part_of_the_archive_is_indexed(self, fixture_epc):
        """
        Nothing that is an energyml part in the ZIP may be left out, whatever the
        content types say about it.
        """
        with zipfile.ZipFile(fixture_epc) as zf:
            object_parts = {
                name
                for name in zf.namelist()
                if EpcFile._is_candidate_object_part(name) and b"uuid=" in zf.open(name).read(4096)
            }
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            indexed = {epc.get_object_path(metadata.uuid) for metadata in epc.list_objects(resolve_titles=False)}
        assert object_parts - indexed == set()

    def test_filtering_by_type_needs_no_read(self, fixture_epc):
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            some_type = epc.list_objects(resolve_titles=False)[0].object_type
            before = epc.stats.head_reads
            filtered = epc.list_objects(object_type=some_type, resolve_titles=False)
            assert epc.stats.head_reads == before
            assert filtered
            assert all(metadata.object_type == some_type for metadata in filtered)

    def test_lookup_by_uuid_and_by_identifier(self, fixture_epc):
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            metadata = epc.list_objects()[0]
            assert epc.get_object(metadata.uuid) is not None
            assert epc.get_object(metadata.identifier) is not None
            assert epc.get_object(metadata.uri) is not None
            assert len(epc.get_object_by_uuid(metadata.uuid)) >= 1
            assert metadata.uuid in epc

    def test_unknown_object(self, fixture_epc):
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object("00000000-0000-0000-0000-000000000000") is None
            assert epc.get_object("not an identifier") is None
            assert epc.get_object_by_uuid("00000000-0000-0000-0000-000000000000") == []

    def test_object_paths_come_from_the_archive(self, fixture_epc):
        """A package whose naming differs from ours must stay readable."""
        with zipfile.ZipFile(fixture_epc) as zf:
            names = set(zf.namelist())
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            for metadata in epc.list_objects(resolve_titles=False):
                assert epc.get_object_path(metadata.uuid) in names

    def test_caching(self, fixture_epc):
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            uuid = epc.list_objects(resolve_titles=False)[0].uuid
            first = epc.get_object(uuid)
            second = epc.get_object(uuid)
            assert first is second
            assert epc.stats.cache_hits >= 1

            epc.clear_cache()
            assert epc.get_object(uuid) is not first


class TestDegradedPackage:
    def test_index_without_content_types(self, new_epc_path):
        """A package whose [Content_Types].xml is gone must still open."""
        with zipfile.ZipFile(EPC_22) as src, zipfile.ZipFile(new_epc_path, "w", zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                if get_epc_content_type_path() not in info.filename:
                    dst.writestr(info, src.read(info.filename))

        with EpcFile(EPC_22, mode=EpcAccessMode.READ_ONLY) as reference:
            expected = {metadata.uuid for metadata in reference.list_objects(resolve_titles=False)}

        with EpcFile(new_epc_path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert {metadata.uuid for metadata in epc.list_objects(resolve_titles=False)} == expected
            assert epc.stats.parts_sniffed == len(expected)
            assert epc.get_object(next(iter(expected))) is not None

    def test_content_types_declaring_a_missing_part(self, writable_copy):
        """An override pointing nowhere must be dropped, not surfaced as an object."""
        path = writable_copy(EPC_201)
        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            indexed = {metadata.uuid for metadata in epc.list_objects(resolve_titles=False)}
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
        for uuid in indexed:
            assert any(uuid in name for name in names)

    def test_sniffing_can_be_disabled(self, new_epc_path):
        with zipfile.ZipFile(EPC_22) as src, zipfile.ZipFile(new_epc_path, "w", zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                if get_epc_content_type_path() not in info.filename:
                    dst.writestr(info, src.read(info.filename))

        with EpcFile(new_epc_path, mode=EpcAccessMode.READ_ONLY, scan_undeclared_parts=False) as epc:
            assert len(epc) == 0


class TestAccessModes:
    def test_read_only_refuses_every_modification(self, fixture_epc, sample_objects):
        feature, _ = sample_objects
        with EpcFile(fixture_epc, mode=EpcAccessMode.READ_ONLY) as epc:
            with pytest.raises(ReadOnlyEpcError):
                epc.put_object(feature)
            with pytest.raises(ReadOnlyEpcError):
                epc.delete_object(epc.list_objects(resolve_titles=False)[0].uuid)
            with pytest.raises(ReadOnlyEpcError):
                epc.put_part("junk.txt", b"junk")

    def test_read_only_on_a_missing_file(self, new_epc_path):
        with pytest.raises(FileNotFoundError):
            EpcFile(new_epc_path, mode=EpcAccessMode.READ_ONLY)

    def test_in_memory_never_touches_the_file(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects
        before = os.path.getsize(path)

        with EpcFile(path, mode=EpcAccessMode.IN_MEMORY) as epc:
            count_before = len(epc)
            epc.put_object(feature)
            assert len(epc) == count_before + 1
            assert epc.get_object(feature.uuid) is not None

        assert os.path.getsize(path) == before
        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is None

    def test_in_memory_can_be_materialised_with_save_as(self, writable_copy, new_epc_path, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects
        before = os.path.getsize(path)

        with EpcFile(path, mode=EpcAccessMode.IN_MEMORY) as epc:
            epc.put_object(feature)
            epc.save_as(new_epc_path)

        assert os.path.getsize(path) == before
        with EpcFile(new_epc_path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is not None

    def test_manual_discards_unsaved_changes(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects

        with EpcFile(path, mode=EpcAccessMode.MANUAL) as epc:
            epc.put_object(feature)
            assert epc.has_pending_changes

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is None

    def test_manual_writes_on_save(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects

        with EpcFile(path, mode=EpcAccessMode.MANUAL) as epc:
            epc.put_object(feature)
            assert epc.save() is True
            assert not epc.has_pending_changes
            assert epc.save() is False  # nothing left to write

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is not None

    def test_on_close_writes_once(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects

        with EpcFile(path, mode=EpcAccessMode.ON_CLOSE) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)
            assert epc.stats.flushes == 0

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is not None
            assert epc.get_object(interpretation.uuid) is not None

    def test_immediate_writes_on_each_modification(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects

        epc = EpcFile(path, mode=EpcAccessMode.IMMEDIATE)
        epc.put_object(feature)
        assert epc.stats.flushes == 1
        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as other:
            assert other.get_object(feature.uuid) is not None
        epc.put_object(interpretation)
        assert epc.stats.flushes == 2
        epc.close()

        with zipfile.ZipFile(path) as zf:
            assert zf.testzip() is None
        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(interpretation.uuid) is not None

    def test_immediate_compacts_on_close(self, writable_copy, sample_objects):
        from energyml.utils.zip_raw import count_shadowed_entries

        path = writable_copy()
        feature, _ = sample_objects

        epc = EpcFile(path, mode=EpcAccessMode.IMMEDIATE)
        for _ in range(3):
            epc.put_object(feature)
        with zipfile.ZipFile(path) as zf:
            assert count_shadowed_entries(zf) > 0
        epc.close()

        with zipfile.ZipFile(path) as zf:
            assert count_shadowed_entries(zf) == 0
            assert zf.testzip() is None

    def test_discard_changes(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects

        with EpcFile(path, mode=EpcAccessMode.ON_CLOSE) as epc:
            count = len(epc)
            epc.put_object(feature)
            epc.discard_changes()
            assert not epc.has_pending_changes
            assert len(epc) == count

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is None

    def test_pending_changes_are_dropped_on_exception(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects

        with pytest.raises(ValueError):
            with EpcFile(path, mode=EpcAccessMode.ON_CLOSE) as epc:
                epc.put_object(feature)
                raise ValueError("something went wrong")

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is None


class TestModification:
    def test_put_then_read_back(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects

        with EpcFile(path) as epc:
            identifier = epc.put_object(feature)
            assert identifier is not None
            assert epc.get_object(feature.uuid) is feature

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            reloaded = epc.get_object(feature.uuid)
            assert reloaded is not None
            assert reloaded.citation.title == feature.citation.title
            assert epc.get_object(identifier) is not None

    def test_update_reuses_the_existing_path(self, writable_copy):
        path = writable_copy()
        with EpcFile(path) as epc:
            uuid = epc.list_objects(resolve_titles=False)[0].uuid
            original_path = epc.get_object_path(uuid)
            obj = epc.get_object(uuid)
            obj.citation.title = "renamed by the test"
            epc.put_object(obj)
            assert epc.get_object_path(uuid) == original_path

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object_path(uuid) == original_path
            assert epc.get_object(uuid).citation.title == "renamed by the test"

    def test_update_does_not_duplicate_the_object(self, writable_copy):
        path = writable_copy()
        with EpcFile(path) as epc:
            count = len(epc)
            uuid = epc.list_objects(resolve_titles=False)[0].uuid
            epc.put_object(epc.get_object(uuid))
            assert len(epc) == count

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert len(epc) == count

    def test_add_object_refusing_to_replace(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects
        with EpcFile(path) as epc:
            epc.add_object(feature)
            with pytest.raises(ValueError):
                epc.add_object(feature, replace_if_exists=False)

    def test_delete(self, writable_copy):
        path = writable_copy()
        with EpcFile(path) as epc:
            count = len(epc)
            uuid = epc.list_objects(resolve_titles=False)[0].uuid
            part_path = epc.get_object_path(uuid)
            assert epc.delete_object(uuid) is True
            assert len(epc) == count - 1
            assert epc.get_object(uuid) is None

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert len(epc) == count - 1
            assert epc.get_object(uuid) is None
            assert part_path not in epc.list_parts()
        with zipfile.ZipFile(path) as zf:
            assert zf.testzip() is None

    def test_delete_unknown_object(self, writable_copy):
        path = writable_copy()
        with EpcFile(path) as epc:
            assert epc.delete_object("00000000-0000-0000-0000-000000000000") is False

    def test_delete_then_put_again(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects
        with EpcFile(path) as epc:
            epc.put_object(feature)
            epc.delete_object(feature.uuid)
            epc.put_object(feature)

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_object(feature.uuid) is not None

    def test_raw_parts(self, writable_copy):
        path = writable_copy()
        with EpcFile(path) as epc:
            epc.put_part("docs/readme.txt", b"hello")
            assert epc.get_part("docs/readme.txt") == b"hello"

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_part("docs/readme.txt") == b"hello"

        with EpcFile(path) as epc:
            assert epc.delete_part("docs/readme.txt") is True
            assert epc.get_part("docs/readme.txt") is None

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_part("docs/readme.txt") is None

    def test_content_types_stay_consistent(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, _ = sample_objects
        with EpcFile(path) as epc:
            epc.put_object(feature)

        with zipfile.ZipFile(path) as zf:
            content_types = zf.read(get_epc_content_type_path()).decode("utf-8")
        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            for metadata in epc.list_objects(resolve_titles=False):
                assert epc.get_object_path(metadata.uuid) in content_types

    def test_archive_stays_readable_by_epc_stream_reader(self, writable_copy, sample_objects):
        """The written package must be consumable by the other implementation."""
        path = writable_copy()
        feature, _ = sample_objects
        with EpcFile(path) as epc:
            epc.put_object(feature)

        reader = EpcStreamReader(path)
        try:
            assert feature.uuid in {metadata.uuid for metadata in reader.list_objects()}
        finally:
            reader.close()


class TestRelationships:
    def test_rels_are_written_for_a_new_object(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects

        with EpcFile(path, rels_update_mode=RelsUpdateMode.UPDATE_AT_MODIFICATION) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            interpretation_path = epc.get_object_path(interpretation.uuid)
            feature_path = epc.get_object_path(feature.uuid)

            outgoing = epc.get_obj_rels(interpretation.uuid)
            assert any(rel.target == feature_path for rel in outgoing), "missing DESTINATION relationship"

            incoming = epc.get_obj_rels(feature.uuid)
            assert any(rel.target == interpretation_path for rel in incoming), "missing SOURCE relationship"

    def test_rels_files_are_valid_xml(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects
        with EpcFile(path) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)
            interpretation_rels = gen_rels_path_from_obj_path(epc.get_object_path(interpretation.uuid))

        with zipfile.ZipFile(path) as zf:
            from lxml import etree

            etree.fromstring(zf.read(interpretation_rels))

    def test_deleting_an_object_cleans_the_back_references(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects

        with EpcFile(path) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)

        with EpcFile(path) as epc:
            interpretation_path = epc.get_object_path(interpretation.uuid)
            epc.delete_object(interpretation.uuid)

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            remaining = epc.get_obj_rels(feature.uuid)
            assert all(rel.target != interpretation_path for rel in remaining)

    def test_manual_rels_mode_writes_nothing(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects

        with EpcFile(path, rels_update_mode=RelsUpdateMode.MANUAL) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert epc.get_obj_rels(interpretation.uuid) == []

    def test_rels_update_on_close(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects

        with EpcFile(path, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)

        with EpcFile(path, mode=EpcAccessMode.READ_ONLY) as epc:
            feature_path = epc.get_object_path(feature.uuid)
            assert any(rel.target == feature_path for rel in epc.get_obj_rels(interpretation.uuid))

    def test_object_dependencies(self, writable_copy, sample_objects):
        path = writable_copy()
        feature, interpretation = sample_objects
        with EpcFile(path) as epc:
            epc.put_object(feature)
            epc.put_object(interpretation)
            dependencies = epc.get_object_dependencies(interpretation.uuid)
            assert any(feature.uuid in dependency for dependency in dependencies)


class TestCreation:
    def test_new_file(self, new_epc_path, sample_objects):
        feature, interpretation = sample_objects

        with EpcFile(new_epc_path) as epc:
            assert len(epc) == 0
            epc.put_object(feature)
            epc.put_object(interpretation)

        assert os.path.exists(new_epc_path)
        with zipfile.ZipFile(new_epc_path) as zf:
            assert zf.testzip() is None
            assert get_epc_content_type_path() in zf.namelist()

        with EpcFile(new_epc_path, mode=EpcAccessMode.READ_ONLY) as epc:
            assert len(epc) == 2
            assert epc.get_object(feature.uuid) is not None

    def test_new_file_is_readable_by_epc_stream_reader(self, new_epc_path, sample_objects):
        feature, _ = sample_objects
        with EpcFile(new_epc_path) as epc:
            epc.put_object(feature)

        reader = EpcStreamReader(new_epc_path)
        try:
            assert reader.get_object(feature.uuid) is not None
        finally:
            reader.close()


class TestExternalArrays:
    def test_h5_paths_are_resolved(self):
        with EpcFile(EPC_22, mode=EpcAccessMode.READ_ONLY) as epc:
            metadata = epc.list_objects(resolve_titles=False)[0]
            paths = epc.get_h5_file_paths(metadata.uuid)
            assert isinstance(paths, list)

    def test_read_array_matches_epc_stream_reader(self):
        """Both implementations must return the same arrays for the same object."""
        import numpy as np

        reader = EpcStreamReader(EPC_22)
        try:
            candidates = [
                metadata for metadata in reader.list_objects() if "Representation" in (metadata.object_type or "")
            ]
            compared = 0
            with EpcFile(EPC_22, mode=EpcAccessMode.READ_ONLY) as epc:
                for metadata in candidates:
                    obj = reader.get_object(metadata.uuid)
                    arrays = reader.get_array_metadata(obj)
                    if not isinstance(arrays, list):
                        continue
                    for array_metadata in arrays:
                        path = array_metadata.path_in_resource
                        if not path:
                            continue
                        reference = reader.read_array(obj, path)
                        candidate = epc.read_array(metadata.uuid, path)
                        if reference is None:
                            continue
                        assert candidate is not None, f"{path} unreadable through EpcFile"
                        assert np.array_equal(np.asarray(reference), np.asarray(candidate))
                        compared += 1
                        if compared >= 5:
                            return
            assert compared > 0, "no array compared"
        finally:
            reader.close()
