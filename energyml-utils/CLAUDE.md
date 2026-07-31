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
  The same type comes in three spellings and `_mesh_name_mapping` / `_numpy_mesh_name_mapping` must normalise all
  of them: the python class name (`ObjTriangulatedSetRepresentation`), the schema type carried by a content type
  and by `ResourceMetadata.object_type` (`obj_TriangulatedSetRepresentation` — RESQML 2.0.1 keeps that prefix,
  2.2 does not), and the qualified type (`resqml20.obj_…`). Only the first was handled, so `_list_exportable_uuids`
  returned nothing on a 2.0.1 EPC and `extract_3d` exported no file at all.

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
| container | `AbstractMesh` (`point_list`, `(N,3)` ndarray) | `NumpyMesh` / `NumpyMultiMesh` (`points`, VTK-flat connectivity) |

**There is only one implementation left.** `mesh.py`'s geometry readers are adapters: they call the matching
`read_numpy_*` and convert the result back into the legacy containers (`_to_legacy_meshes`), rebuilding the legacy
identifiers from the patch metadata (`"{uri}_patch{n}"`, `"Patch num {n}"` for point sets, the bare URI for
wellbores). Verified against the pre-adapter readers over every representation of every fixture in `rc/epc/` —
1155 objects, 942 meshes, identical down to the index structures and edge/face counts.

Two consequences: `AbstractMesh.point_list` now holds the `(N,3)` float64 array rather than a list of lists (the
field was already annotated for both), and volumetric types (`IjkGridRepresentation`,
`UnstructuredGridRepresentation`) raise `NotSupportedError` from the legacy API since `AbstractMesh` cannot model
them — the numpy stack does. `gen_surface_grid_geometry` is kept for external callers but is no longer used.

**Every mesh carries the `PointFrame` its points are in** (`frame` field on `AbstractMesh` and `NumpyMesh`), and
each dispatcher applies only the pipeline stages the reader did not. That replaced two hard-coded lists of type-name
substrings, where a missing entry transformed the same points twice and an extra one left them raw. Adding a reader
now only requires it to report the frame it produced.

`_ensure_float64_points` takes ownership of the points before any in-place transform: the geometry may come from
`read_array_view`, whose contract forbids mutating it (it can be the memory-mapped file). Connectivity arrays keep
the zero-copy path — they are only read.

**Reader coverage.** Every RESQML representation type has a `read_numpy_*` except `GpGridRepresentation`, which the
schema itself calls "not expected to be used for routine data transfer". Many are one-line delegations
(`WellboreMarkerFrame` / `BlockedWellbore` → the wellbore-frame reader, `NonSealedSurfaceFramework` /
`SealedVolumeFramework` → the representation-set reader, `Seismic2d/3dPostStack` → the lattice or line they
reference) — dispatch is by function name, so the entry point *is* the registration and each still needs one. Two
readers deliberately return a partial geometry and say so: `Truncated*GridRepresentation` reads the base grid
without applying its `TruncationCellPatch`, and an IJK grid whose geometry comes from a `ParentWindow` (an LGR)
returns empty rather than silently producing nothing.

### The IJK grid reader

`rc/epc/80wells_surf_modified_val_color.epc` holds the FESAPI example grids — the same grid shipped left- *and*
right-handed, explicit *and* parametric, faulted and not — which is what pins the four rules below.
`tests/test_mesh_numpy_ijk_spec.py` checks them against values read out of the HDF5, not out of the reader.

- **Cells come out I fastest, then J, then K.** That is the order every cell-indexed array of the grid uses, so a
  property maps onto the cells without permutation. The arrays make the convention explicit: `CellGeometryIsDefined`
  is stored `(NK, NJ, NI)` and `PillarGeometryIsDefined` `(NJ+1, NI+1)`.
- **`GridIsRighthanded` sets the corner winding**, so the emitted hexahedron always has a positive Jacobian. The flag
  is meant in the real-world sense: with a depth-positive-down local CRS a right-handed grid still measures negative
  in the LOCAL frame and only comes out positive after `apply_from_crs_info`. Orientation is therefore correct in
  PROJECTED — the default, and what a viewer renders.
- **`PillarGeometryIsDefined` / `CellGeometryIsDefined` override the coordinates.** Undefined pillars have their nodes
  NaN'd; undefined cells become `VTK_EMPTY_CELL` *in place* rather than being dropped, which is what keeps the 1:1
  match with the cell-indexed properties.
- **A split coordinate line has no parametric line of its own.** `ParametricLineArray` holds only the `(NI+1)(NJ+1)`
  pillars; a split line reuses the line of `ColumnLayerSplitCoordinateLines.PillarIndices[s]` and differs only by its
  P-values — that is how a fault throw is expressed on a parametric geometry, and the doc of
  `Point3dParametricArray.ParametricLineIndices` names it as the reason the explicit index array may be omitted.
  The line count must be taken from `LineKindIndices` ("Size = #Lines"), never derived from the expected pillar
  count: `ControlPoints` is `(KnotCount, #Lines, 3)`, and back-solving a "coordinate dimension" out of it is what
  raised `cannot reshape array of size 18 into shape (1,8,2)` on every faulted parametric grid.

`KnotCount` is the *maximum* knot count over all the lines, so the shorter ones are **NaN-padded** ("if you cannot
provide enough control points for a parametric line, then pad with NaN values"). `_trim_nan_knots` drops that
padding per line before any interpolation; a single NaN reaching `np.interp` / `CubicSpline` / `searchsorted` turns
the whole pillar into NaN silently, since NaN coordinates never raise.

### Grid connection sets

`read_numpy_grid_connection_set_representation` has no geometry of its own: it looks every face up on the grid(s) it
references. RESQML publishes the local face-per-cell index only as a figure, stating just that "the top and bottom
faces always come first, followed by the side faces". `_IJK_LOCAL_FACE_CORNERS` records the rest — the fault sets of
the fixture all pair face **3** on the cell at I with face **5** on its neighbour at I+1, and those faces resolve to
the two walls of the fault plane at X=375, which fixes 3 = I+ and 5 = I- and hence the J-, I+, J+, I- cycle of the
side faces. Both sides of a connection are emitted: across a fault they do not coincide, and drawing one hides the
throw.

### Coordinate frames

[crs.py](src/energyml/utils/data/crs.py) owns the whole pipeline; `PointFrame` names its stages:

```
LOCAL --apply_from_crs_info--> PROJECTED --reproject_to_wgs84--> WGS84
```

They are **successive**, not alternatives: skipping the local stage hands pyproj coordinates still offset by the
local origin. `to_frame(points, crs_info, target, current)` is the only entry point that knows the ordering, so no
caller has to remember it and a transform cannot run twice. It degrades rather than raising — a WGS84 request with
no EPSG code, or without pyproj, comes back as `PROJECTED` with `degraded_reason` set, which is what the GeoJSON
writer uses to decide whether to advertise a `crs` member.

`compute_origin_shift` / the `origin_shift` option recentre projected coordinates (6-7 significant digits, which
lose precision once a viewer reads the file as float32). It must be resolved **once per export** — a per-patch
centre would pull the patches apart.

`reproject_to_wgs84` transforms in blocks of `_REPROJECT_CHUNK` points: the columns of a C-order `(N,3)` array are
strided, so pyproj needs one contiguous buffer per axis, and blocking makes that scratch constant (6 MiB) instead
of proportional to N.

### Export package

[data/export/](src/energyml/utils/data/export/) is one module per format (`obj`, `off`, `geojson`, `vtk`, `stl`)
over a shared `_base.py`, plus `_registry.py`. Each module declares a `FormatSpec` — writer, options class,
description, filter label, supported primitives, side-car suffix — and `export_mesh` plus every UI helper reads
that registry. Adding a format is a module and one `register_format` call, not six places to edit.
`__init__.py` re-exports the old flat API, so `from energyml.utils.data.export import export_obj` still resolves.

Every writer takes `frame=` and `origin_shift=`, not just GeoJSON. `use_crs_displacement` is kept and simply
selects the default frame (`PROJECTED` / `LOCAL`).

GeoJSON has **one** geometry implementation: the streaming writer (bounded memory). `to_geojson_feature` and
`export_geojson_dict` serialise through it and parse the result back. Note `export_geojson_dict` now reprojects to
WGS84 by default, where it used to emit non-RFC-7946 output silently; pass `to_wgs84=False` for the old behaviour.

### Properties

[properties.py](src/energyml/utils/data/properties.py) holds `read_property`, `read_column_based_table`,
`read_time_series` and the per-kind property readers, re-exported from `mesh.py` for compatibility. They dispatch
on `read_<snake_case(type)>` **in their own module namespace**; while they lived in `mesh.py` that namespace also
held the geometry readers, so `read_property` on a `PointRepresentation` returned meshes instead of raising.

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

Two things a real file breaks, both handled rather than raised:

- **The vertical EPSG code can be unusable.** Files write a *datum* code where a CRS code belongs (the Volve
  export declares `EPSG:6230`, the ED50 datum). The compound source then fails to build; giving up would leave the
  points in their projected CRS although the horizontal part is perfectly reprojectable. So
  `_build_transformer_with_vertical_fallback` retries with the horizontal CRS alone and passes Z through untouched
  — longitude/latitude are correct, Z stays in its source vertical frame, and a warning says so.
- **The EPSG codes have to survive deserialisation first.** They hang off a polymorphic `xsi:type`, and energyml
  files usually write it *unprefixed* (`xsi:type="VerticalCrsEpsgCode"`), which resolves against the document's
  default namespace — `commonv2`, exactly where those types live. xsdata reads that default namespace as
  `ns_map[None]`, so `FallbackNamespaceXmlParser` must keep the `None` key when it merges its fallback namespaces:
  rewriting it to `""` built the element as its abstract base and dropped both EPSG codes, making the reprojection
  impossible on a large share of RESQML 2.0.1 files. Covered by `tests/test_xsi_type_resolution.py`.

### Tests

`tests/` runs against **real EPC fixtures in `rc/epc/`** (`testingPackageCpp.epc` v2.0.1, `testingPackageCpp22.epc`
v2.2, `80wells_surf.epc`, `SPASS_40+80wells.epc`, …) rather than mock dataclasses, so behaviour is validated
against the actual xsdata classes. Fixtures differ in meaningful ways (list vs ndarray points, CRS present or not,
EPSG resolvable or not) — when a bug is version- or file-specific, reproduce it on the right fixture before
concluding. Tests needing an optional dependency skip via a guard (e.g. `is_pyproj_available()`).

**Only `testingPackageCpp.epc` / `testingPackageCpp22.epc` (+ their `.h5`) are committed** — every other EPC of
`rc/epc/` is field data that stays local, and `.gitignore` re-allows exactly those four. A test that needs one of
the others must *skip* when it is absent, never fail; on a fresh clone the suite is green with 28 skips. See
[rc/epc/README.md](rc/epc/README.md), which also lists what the testing packages do **not** cover (no vertical EPSG
code, no standalone `ProjectedCrs`, no rotation, HDF5 only, small packages).

For grid work the 2.2 testing package is the fixture: it carries the whole FESAPI grid example set (22 IJK grids
covering explicit and parametric geometry, both handedness values, K-gaps, split coordinate lines, undefined cells
and an LGR, plus 6 grid connection sets). Read the expected values out of `testingPackageCpp22.h5` — the shape of a
dataset is often the answer on its own, e.g. `CellGeometryIsDefined` being `(NK, NJ, NI)`.

`pytest` deselects the `slow` marker through `addopts`; CI runs `pytest -m ""` to get everything. Mark a test slow
when it builds an `EpcStreamReader` over a large package — that inflates every part (~50 s on
`SPASS_40+80wells.epc`). `EpcStreamReader` also **rewrites the archive when it closes**, even after a read-only
session, so never point one at a committed fixture: use the `writable_copy` fixture, which copies the EPC under its
original basename into a temp directory together with its sibling `.h5`.
