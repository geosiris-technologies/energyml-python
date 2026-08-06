# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
The console scripts declared in ``[tool.poetry.scripts]``.

The ten scripts used to point at ``example.tools``, a module the wheel does not ship: every one
of them was installed and every one of them died at import with ``ModuleNotFoundError``. Nothing
caught it because the repository root is on ``sys.path`` in development.

These tests read the declarations out of ``pyproject.toml`` and resolve each of them the way
``pip`` does — import the module, get the attribute — then run ``--help`` on it. A CLI moved,
renamed or mistyped fails here rather than at the user's first ``pip install``.
"""

from __future__ import annotations

import importlib
import json
import re
from pathlib import Path

import pytest

_PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def _declared_scripts() -> dict:
    """``{script_name: "module:function"}`` read from ``[tool.poetry.scripts]``."""
    try:
        import tomllib  # python >= 3.11
    except ModuleNotFoundError:  # pragma: no cover — python 3.9 / 3.10
        tomllib = None

    if tomllib is not None:
        with open(_PYPROJECT, "rb") as f:
            return tomllib.load(f).get("tool", {}).get("poetry", {}).get("scripts", {})

    # minimal fallback parser, enough for the flat `name = "value"` table we declare
    text = _PYPROJECT.read_text(encoding="utf-8")
    section = text.split("[tool.poetry.scripts]", 1)[-1].split("\n[", 1)[0]
    return dict(re.findall(r'^\s*([\w-]+)\s*=\s*"([^"]+)"\s*$', section, re.M))


SCRIPTS = _declared_scripts()


def test_scripts_are_declared():
    assert SCRIPTS, "no console script declared in [tool.poetry.scripts]"


@pytest.mark.parametrize("name", sorted(SCRIPTS))
def test_entry_point_target_is_importable(name):
    """Resolve `module:function` exactly like the generated console script does."""
    module_path, _, attribute = SCRIPTS[name].partition(":")
    assert module_path.startswith("energyml."), (
        f"'{name}' points at '{module_path}', which is outside the distributed package: "
        "the wheel only ships 'energyml/'"
    )
    module = importlib.import_module(module_path)
    target = getattr(module, attribute, None)
    assert callable(target), f"'{name}' -> {SCRIPTS[name]} is not callable"


@pytest.mark.parametrize("name", sorted(SCRIPTS))
def test_entry_point_help(name, capsys):
    """``--help`` must build the parser and exit with code 0."""
    module_path, _, attribute = SCRIPTS[name].partition(":")
    target = getattr(importlib.import_module(module_path), attribute)
    with pytest.raises(SystemExit) as exit_info:
        target(["--help"])
    assert exit_info.value.code == 0
    assert "usage:" in capsys.readouterr().out


class TestRoundTrip:
    """One end-to-end run of the conversion commands, on a fixture that is published."""

    @staticmethod
    def _fixture() -> Path:
        path = Path(__file__).parent.parent / "rc" / "epc" / "testingPackageCpp.epc"
        if not path.is_file():
            pytest.skip(f"fixture {path.name} not present in rc/epc/")
        return path

    def test_xml_to_json(self, tmp_path):
        from energyml.utils.cli import xml_to_json

        json_path = tmp_path / "objects.json"
        xml_to_json(["-f", str(self._fixture()), "-o", str(json_path)])
        assert json_path.is_file()
        objects = json.loads(json_path.read_text(encoding="utf-8"))
        assert isinstance(objects, list) and len(objects) > 0
        assert all("$type" in o for o in objects)

    def test_json_to_xml_then_json_to_epc(self, tmp_path):
        """JSON in, one XML per object out, then the same JSON packaged in an EPC.

        Built from a single hand-made object rather than from the EPC fixture: the JSON
        round trip of that fixture is not stable (a handful of its objects fail to serialize
        back to XML, and *which* ones changes from run to run — a pre-existing defect of the
        serializer, unrelated to the CLI).
        """
        from energyml.utils.cli import json_to_epc, json_to_xml
        from energyml.utils.epc import Epc
        from energyml.utils.serialization import JSON_VERSION, serialize_json

        from energyml.resqml.v2_2.resqmlv2 import BoundaryFeature
        from energyml.eml.v2_3.commonv2 import Citation

        obj = BoundaryFeature(
            uuid="0c1b2f30-4e5a-4a1b-9b6d-2f0d5a7c8e91",
            schema_version="2.2",
            citation=Citation(
                title="a boundary",
                originator="test",
                creation="2024-01-01T00:00:00Z",
                format="energyml-utils",
                last_update="2024-01-01T00:00:00Z",
            ),
        )
        json_path = tmp_path / "objects.json"
        json_path.write_text("[" + serialize_json(obj, JSON_VERSION.OSDU_OFFICIAL) + "]", encoding="utf-8")

        xml_out = tmp_path / "xml"
        xml_out.mkdir()
        json_to_xml(["-f", str(json_path), "-o", str(xml_out / "ignored")])
        assert list(xml_out.glob("*.xml")), "json_to_xml wrote no file"

        epc_path = tmp_path / "rebuilt.epc"
        json_to_epc(["-f", str(json_path), "-o", str(epc_path)])
        assert epc_path.is_file()
        assert len(Epc.read_file(str(epc_path)).energyml_objects) == 1

    def test_load_n_save(self, tmp_path):
        from energyml.utils.cli import load_n_save
        from energyml.utils.epc import Epc

        out = tmp_path / "out.epc"
        load_n_save(["-f", str(self._fixture()), "-o", str(out)])
        assert out.is_file()
        assert len(Epc.read_file(str(out)).energyml_objects) > 0

    def test_describe_as_csv(self, tmp_path):
        from energyml.utils.cli import describe_as_csv

        # describe_as_csv writes its output next to the objects it read
        folder = tmp_path / "objects"
        folder.mkdir()
        (folder / self._fixture().name).write_bytes(self._fixture().read_bytes())

        describe_as_csv(["-f", str(folder)])
        csv_path = folder / "describe.csv"
        assert csv_path.is_file()
        lines = csv_path.read_text(encoding="utf-8").strip().split("\n")
        assert lines[0].startswith("Title;QualifiedType;")
        assert len(lines) > 1, "no object described"

    def test_validate(self, tmp_path, capsys):
        from energyml.utils.cli import validate_files

        validate_files(["-f", str(self._fixture())])
        # the command prints a JSON list (or a dict when grouped) on stdout
        assert isinstance(json.loads(capsys.readouterr().out), list)

    def test_extract_3d_geojson(self, tmp_path):
        from energyml.utils.cli import extract_representation_in_3d_file

        out = tmp_path / "meshes"
        out.mkdir()
        extract_representation_in_3d_file(["-f", str(self._fixture()), "-o", str(out), "-ff", "geojson"])
        written = list(out.glob("*.geojson"))
        assert written, "extract_3d wrote no geojson file"
        for path in written:
            document = json.loads(path.read_text(encoding="utf-8"))
            assert document["type"] == "FeatureCollection"


class TestGenerate:
    def test_generate_data_prints_an_object(self, capsys):
        from energyml.utils.cli import generate_data

        generate_data(["-t", "resqml22.TriangulatedSetRepresentation", "-ff", "json"])
        assert "TriangulatedSetRepresentation" in capsys.readouterr().out

    def test_unknown_type_is_reported(self, capsys):
        from energyml.utils.cli import generate_data

        generate_data(["-t", "resqml22.NotAType"])
        assert "Class not found" in capsys.readouterr().out

    def test_generate_multiple_data_writes_files(self, tmp_path):
        from energyml.utils.cli import generate_multiple_data

        generate_multiple_data(
            ["-t", "resqml22.TriangulatedSetRepresentation", "resqml22.PointSetRepresentation", "-o", str(tmp_path)]
        )
        assert len(list(tmp_path.glob("*.json"))) == 2
