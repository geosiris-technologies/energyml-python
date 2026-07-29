# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
poetry install                      # dev install (pulls every energyml-* data model package)
poetry install --extras crs         # + pyproj, needed for the WGS84 reprojection
poetry install --all-extras         # + parquet / las / segy / geometry (scipy)

poetry run pytest                   # full suite (tests/); addopts deselects the "slow" marker
poetry run pytest tests/test_crs_info.py::TestCrsInfoDto::test_defaults -q   # single test
poetry run pytest --cov=src --cov-report=html

poetry run black .                  # line-length 120, target py39
poetry run flake8 src tests
poetry run pre-commit run --all-files   # black + isort + flake8
```

`[tool.pytest.ini_options]` puts `src` on `pythonpath`, so tests import `energyml.utils.*` without installing.
If a `poetry run <script>` fails on imports, set `$env:PYTHONPATH="src"`.

CLI entry points live in `[tool.poetry.scripts]` and all resolve to functions in [example/tools.py](example/tools.py)
(`extract_3d`, `csv_to_dataset`, `generate_data`, `generate_multiple_data`, `xml_to_json`, `json_to_xml`,
`json_to_epc`, `loadNsave`, `describe_as_csv`, `validate`). Adding a CLI = adding a function there **and** a
line in `[tool.poetry.scripts]`. See README.md for per-script examples.

## Architecture

### Version-neutral by construction

The energyml data models (RESQML 2.0.1/2.2, EML 2.0–2.3, WITSML 2.0/2.1, PRODML 2.0/2.2) are **xsdata-generated
dataclasses shipped as separate packages** (`energyml-resqml2-2`, `energyml-common2-3`, …), declared as dev
dependencies here and published independently. This repository contains no schema classes: it manipulates objects
of classes it does not know at write time. Consequences that shape the whole codebase:

- **Nothing is imported statically from the data models.** Classes are resolved at runtime from a qualified type
  (`resqml22.TriangulatedSetRepresentation`), a content type, or a python path.
- **Attributes are reached by name/regex/path**, never by hard-coded field access, because the same concept sits at
  different paths across versions (e.g. `XOffset` in v2.0.1 vs `OriginProjectedCoordinate1` in v2.2).
- **Dispatch is by naming convention.** `read_array` maps an array class name to a module-level function named
  `read_<snake_case(type_name)>`; same for `read_<snake_case(type)>` in `mesh.py` and `read_numpy_<...>` in
  `mesh_numpy.py`. Supporting a new type = defining a correctly named function, no registry to update.

[introspection.py](src/energyml/utils/introspection.py) is the foundation of all this (attribute lookup, class
resolution, qualified/content type generation, random object generation, `get_object_metadata`). Two subtleties:
`get_class_from_simple_name` builds an explicit namespace for its `exec`/`eval` (PEP 667 broke the previous
implementation on py3.13+), and `is_union_type` must be used instead of `isinstance(cls, typing.Union.__class__)`
(on py3.14 `typing.Union` *is* `types.UnionType`, so that test is true for every class).

### Storage abstraction

[storage_interface.py](src/energyml/utils/storage_interface.py) defines `EnergymlStorageInterface`, implemented by
[`Epc`](src/energyml/utils/epc.py) (everything in memory),
[`EpcStreamReader`](src/energyml/utils/epc_stream.py) (lazy, index-based) and
[`EpcFile`](src/energyml/utils/epc_file.py) (lazy + buffered writes), and extensible to ETP.

**`EpcFile` is the one to prefer for new work.** The other two are kept because external code depends on them.

| | `Epc` | `EpcStreamReader` | `EpcFile` |
|---|---|---|---|
| open | deserialises every part | reads the **full XML** of every part to regex uuid/title | central directory + `[Content_Types].xml`, no part body |
| read | already in memory | lazy, `WeakValueDictionary` | lazy, bounded LRU |
| write | rebuild + `export_file` | full ZIP rewrite (inflate + deflate) **per modification** | in-memory overlay, one rewrite with raw stream copy |

Measured on `rc/epc/SPASS_40+80wells.epc` (2.8 MB, 1678 objects): open 3061 / 199 / 52 ms; 20 `put_object` 11673 /
163 ms (`EpcStreamReader` / `EpcFile` ON_CLOSE). Note `list_objects()` *with titles* is slower on `EpcFile`
(103 ms vs 5 ms) because `EpcStreamReader` already paid that cost at open — pass `resolve_titles=False` when the
titles are not needed.

Two things shape `EpcFile`:

- **Persistence is a policy, not a hard-coded behaviour** — `EpcAccessMode` (READ_ONLY / IN_MEMORY / MANUAL /
  ON_CLOSE / IMMEDIATE) decides when the overlay reaches disk. `has_pending_changes`, `save()`, `save_as()`,
  `discard_changes()` and `compact()` are the explicit controls. In MANUAL, closing without `save()` **discards**
  the modifications (a warning is logged); the same happens when a `with` block exits on an exception.
- **The archive is the source of truth, `[Content_Types].xml` is only a hint.** Overrides pointing at a missing part
  are dropped; parts declared with a non-energyml content type, or not declared at all, are identified by parsing the
  first bytes of their root element (`_content_type_from_head`, built from namespace + `schemaVersion` + `xsi:type`,
  *without* resolving the python class so an uninstalled data model does not break indexing). `rc/epc/testingPackageCpp.epc`
  exercises both defects at once — 5 objects declared twice, once with the wrong path and once with the wrong content
  type. Object paths always come from the archive, never regenerated, so foreign naming survives a round trip.

[zip_raw.py](src/energyml/utils/zip_raw.py) is what makes the writes cheap: `rewrite_zip` copies the already-deflated
payload of untouched entries instead of inflating and re-deflating them (0.030 s vs 0.485 s on the fixture above), and
`append_to_zip` shadows an entry by appending a second one with the same name — `zipfile` resolves a name through the
central directory, where the last one wins. It touches undocumented `zipfile` attributes (`header_offset`, `fp`,
`start_dir`) and falls back to the plain path on any surprise.

Most data functions take `workspace: Optional[EnergymlStorageInterface]`. It is not optional in practice: without
it, DORs cannot be resolved, external arrays cannot be read, and the v2.2 CRS chain cannot be walked. When a
function silently returns partial data, a missing `workspace` is the first thing to check.

### Reading arrays

`helper.read_array` → per-type reader → for external arrays, `workspace.read_array(...)` →
[datasets_io.py](src/energyml/utils/data/datasets_io.py). Backend handlers (HDF5, Parquet, CSV, LAS, SEGY) are
registered in `FileHandlerRegistry`; each is defined inside a `try: import` block with a `Mock*` fallback class so
the package imports fine without the optional dependency. Note that an older `*FileReader` / `*FileWriter` API
coexists with the newer `ExternalArrayHandler` one.

`read_array` returns **either a `list` or an `np.ndarray`** depending on the reader — callers normalise
(`_read_array_np`, `_ensure_float64_points`, `_as_json_ready_list`). Anything that serialises points must handle
both; `json.dumps` on numpy values raises.

### Mesh / export: two parallel stacks

| | legacy | numpy |
|---|---|---|
| reader | `mesh.read_mesh_object` | `mesh_numpy.read_numpy_mesh_object` |
| container | `AbstractMesh` (`point_list`, list-of-lists) | `NumpyMesh` / `NumpyMultiMesh` (`points`, `(N,3)` float64, VTK-flat connectivity) |
| exporters | `mesh.export_obj/export_off/export_geojson_io` (streaming, bytes) | `export.export_obj/geojson/vtk/stl` (dict/text) |

Both are live: `export_multiple_data` (used by `extract_3d`) drives the legacy path; the numpy path feeds PyVista
and the modern exporters. New work should prefer the numpy stack, but the legacy one cannot be deleted yet.

**CRS is applied at read time by the readers, which also keep `crs_object` on the mesh, while
`export._get_export_points` re-applies it when a workspace is reachable.** Feeding a mesh read with
`use_crs_displacement=True` into the modern exporters with a workspace therefore double-transforms it. The numpy
dispatcher guards this with a hard-coded list of type names ([mesh_numpy.py](src/energyml/utils/data/mesh_numpy.py)
`read_numpy_mesh_object`) — a new reader missing from that list gets the wrong treatment.

### CRS pipeline

[crs.py](src/energyml/utils/data/crs.py) is the single place that understands CRS across versions:

1. `extract_crs_info(crs_obj, workspace)` → `CrsInfo`, a version-neutral DTO. It handles v2.0.1
   (`LocalDepth3dCrs`/`LocalTime3dCrs`, data inline) and v2.2/EML 2.3, where the information is spread over a DOR
   chain: `LocalEngineeringCompoundCrs` → `LocalEngineering2dCrs` → `ProjectedCrs` → `ProjectedEpsgCrs.epsg_code`,
   plus `VerticalCrs` → `VerticalEpsgCrs.epsg_code`. Standalone `ProjectedCrs` / `VerticalCrs` are handled too.
   **Never raises** — it logs and returns defaults, so a `CrsInfo` full of `None` usually means a missing workspace
   or an unsupported type, not an absent CRS.
2. `apply_from_crs_info(points, crs_info)` → local → projected (rotation, offsets, Z flip, axis-order swap).
3. `reproject_to_wgs84(points, crs_info, ...)` → projected → WGS84, via pyproj (extra `crs`). Targets EPSG:4979
   (3D) rather than 4326, builds a compound `EPSG:h+EPSG:v` source, flips Z for depth-type vertical CRS, and caches
   transformers keyed on the network flag (PROJ picks its pipeline at build time). Without geoid grids the vertical
   transformation is silently a no-op — hence the warning and the `use_network` flag.

Callers must degrade gracefully when pyproj is absent or no EPSG is found (see `export_geojson`: keep the source
coordinates and advertise the CRS via the `crs` / `coordRefSys` members instead).

### Tests

`tests/` runs against **real EPC fixtures in `rc/epc/`** (`testingPackageCpp.epc` v2.0.1, `testingPackageCpp22.epc`
v2.2, `80wells_surf.epc`, `SPASS_40+80wells.epc`, …) rather than mock dataclasses, so behaviour is validated
against the actual xsdata classes. Fixtures differ in meaningful ways (list vs ndarray points, CRS present or not,
EPSG resolvable or not) — when a bug is version- or file-specific, reproduce it on the right fixture before
concluding. Tests needing an optional dependency skip via a guard (e.g. `is_pyproj_available()`).
