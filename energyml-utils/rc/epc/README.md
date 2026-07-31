# EPC test fixtures

## What may be published

Only the **FESAPI testing packages** are committed:

| file | provenance |
|---|---|
| `testingPackageCpp.epc` + `.h5` | FESAPI example package, RESQML 2.0.1 — <https://github.com/F2I-Consulting/fesapi> |
| `testingPackageCpp22.epc` + `.h5` | same example package, RESQML 2.2 / EML 2.3 |

Everything else in this directory is **field or customer data and stays local**: the 80-well
surveys, `SPASS_40+80wells`, the Volve exports, `out-galaxy-*`, `output-val`, `result_pse`.
`.gitignore` ignores `rc/**/*.epc` and `rc/**/*.h5` and re-allows only the four files above —
do not add to that allow list without checking the data may be published.

A test that needs a local-only EPC **must skip when the file is absent**, never fail: see the
`fixture_epc` fixture of `tests/test_epc_file.py` and the `epc` fixture of
`tests/test_geojson_export.py`. On a fresh clone the suite is green with 28 skips.

> `80wells_surf_modified_val_color.epc` is misleadingly named: all 165 of its objects come from
> the testing packages (same UUIDs, same `F2I-CONSULTING:FESAPI Example` format) with colour
> maps added, and it shares nothing with `80wells_surf.epc`. It is still not committed — the
> testing packages already cover everything it was used for.

## What the testing packages cover

Enough for almost the whole suite, and in particular the grid work
(`tests/test_mesh_numpy_ijk_spec.py` runs entirely on `testingPackageCpp22.epc`):

- 22 `IjkGridRepresentation`: explicit **and** parametric geometry, left- **and** right-handed,
  faulted (split coordinate lines) and unfaulted, K-gaps, `CellGeometryIsDefined=false` cells,
  a `ParentWindow` LGR, and a grid whose pillars mix vertical, linear and Z-linear-cubic lines
  with NaN-padded knots.
- 6 `GridConnectionSetRepresentation`, with and without `ConnectionInterpretations`.
- `UnstructuredGridRepresentation`, `Grid2dRepresentation`, `TriangulatedSetRepresentation`,
  `PolylineSetRepresentation`, `PointSetRepresentation`, `PlaneSetRepresentation`,
  `SealedSurfaceFrameworkRepresentation`, `RepresentationSetRepresentation`, `SubRepresentation`,
  the wellbore family (trajectory, frame, marker frame, seismic frame), properties, colour maps,
  `GraphicalInformationSet`, `ColumnBasedTable`, `TimeSeries`, `PropertyKind`/`PropertySet`.
- Both CRS shapes: `LocalDepth3dCrs` / `LocalTime3dCrs` (2.0.1) and the 2.2 DOR chain
  `LocalEngineeringCompoundCrs` → `LocalEngineering2dCrs` → `ProjectedCrs`.
- A resolvable **projected** EPSG code (23031, ED50 / UTM 31N), so local → projected → WGS84 runs.
- Deliberately malformed packaging in `testingPackageCpp.epc` (objects declared twice, wrong
  path, wrong content type) — what the `EpcFile` indexing tests rely on.

## What they do NOT cover

This is the shopping list for a publishable replacement EPC.

### CRS / reprojection — the biggest gap

1. **No vertical EPSG code at all.** Every CRS resolves `vertical_epsg_code = None`, so the
   compound `EPSG:h+EPSG:v` source of `reproject_to_wgs84`, the Z flip for a depth-type vertical
   CRS, and the geoid-grid warning are never exercised. The local files carry 5714/5715.
2. **No standalone `ProjectedCrs`** — the shape where a representation references a `ProjectedCrs`
   directly instead of going through `LocalEngineeringCompoundCrs`. That is what
   `tests/test_geojson_export.py` needs, and why its 8 tests skip.
3. **No unusable vertical code**, i.e. a *datum* code written where a CRS code belongs
   (Volve declares `EPSG:6230`). `_build_transformer_with_vertical_fallback` exists only for that
   case and is currently covered by unit tests, not by a file.
4. **No non-zero areal rotation and no northing-first axis order**, so the full local → projected
   transform is only ever exercised on synthetic data (see `TestGrid2dGetsTheFullTransform`).

### Scale

5. **Small packages** (165/168 objects, ~300 kB). The `EpcFile` indexing and
   `EpcStreamReader`-comparison tests parametrised on `SPASS_40+80wells.epc` (1678 objects,
   2.8 MB) skip — 12 tests. The assertions still run on the small packages; what is lost is the
   behaviour at scale, which is the whole point of the lazy index.

### Object types

6. Absent from the testing packages, present in the local files: `ProjectedCrs` (standalone),
   `ReferencePointInACrs`, `CommentProperty`, `DataobjectCollection`,
   `CollectionsToDataobjectsAssociationSet`, `GeologicUnitOccurrenceInterpretation`.

### External array backends

7. **HDF5 only.** No Parquet, CSV, LAS or SEGY external array is referenced anywhere, so those
   `FileHandlerRegistry` handlers are only covered by synthetic tests.

### Representation types with no fixture anywhere

Not a gap of the testing packages specifically — no EPC in `rc/epc/` contains them, so these
readers are written from the specification and unvalidated against a real file:
`DeviationSurveyRepresentation`, `StreamlinesRepresentation`, `Graph2dRepresentation`,
`UnstructuredColumnLayerGridRepresentation` (and its truncated variant),
`TruncatedIjkGridRepresentation`, `Seismic2d/3dPostStackRepresentation`,
`RedefinedGeometryRepresentation`, `GpGridRepresentation`.
