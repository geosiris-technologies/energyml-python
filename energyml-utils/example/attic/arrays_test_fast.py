"""
arrays_test_fast.py
===================
Companion to arrays_test.py — but using the mesh_numpy module for zero-copy,
numpy-native geometry reading.

Every function mirrors its counterpart in arrays_test.py and returns
``List[NumpyMesh]``.  The ``__main__`` block at the bottom shows how to
toggle between the different readers and optionally render with PyVista.

Key differences vs. arrays_test.py:
* No list-of-lists — everything is already an ``np.ndarray``.
* VTK flat format for faces / lines — passable directly to PyVista.
* ``use_crs_displacement=True`` applies the CRS offset/scale in-place (no
  extra allocation).
* Optional ``numpy_mesh_to_pyvista()`` helper at the end of each function.
"""

import logging
import os
import sys
import traceback
from pathlib import Path
from typing import List, Optional

import numpy as np


from energyml.utils.data.datasets_io import get_handler_registry
from energyml.utils.data.mesh_numpy import (
    NumpyMesh,
    NumpyPointSetMesh,
    NumpyPolylineMesh,
    NumpySurfaceMesh,
    NumpyVolumeMesh,
    read_numpy_mesh_object,
    numpy_mesh_to_pyvista,
)
from energyml.utils.epc import Epc
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.utils.serialization import read_energyml_xml_str

# ---------------------------------------------------------------------------
# Optional PyVista import — present only when the package is installed.
# ---------------------------------------------------------------------------
try:
    import pyvista as pv

    _PYVISTA_AVAILABLE = True
except ImportError:
    _PYVISTA_AVAILABLE = False

# ---------------------------------------------------------------------------
# Embedded XML fixtures (same as arrays_test.py)
# ---------------------------------------------------------------------------

xml_grid_2d = """<?xml version="1.0" encoding="UTF-8"?>
<resqml:Grid2dRepresentation
  xmlns:eml="http://www.energistics.org/energyml/data/commonv2"
  xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2"
  uuid="4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80" schemaVersion="22">
  <eml:Citation>
    <eml:Title>100x10 grid 2d for continuous color map</eml:Title>
    <eml:Originator>phili</eml:Originator>
    <eml:Creation>2026-02-13T16:55:42Z</eml:Creation>
    <eml:Format>F2I-CONSULTING:FESAPI Example:2.14.1.0</eml:Format>
  </eml:Citation>
  <resqml:RepresentedObject>
    <eml:Uuid>34b69c81-6cfa-4531-be5b-f6bd9b74802f</eml:Uuid>
    <eml:QualifiedType>resqml22.HorizonInterpretation</eml:QualifiedType>
    <eml:Title>Horizon interpretation for continuous color map</eml:Title>
  </resqml:RepresentedObject>
  <resqml:SurfaceRole>map</resqml:SurfaceRole>
  <resqml:FastestAxisCount>50</resqml:FastestAxisCount>
  <resqml:SlowestAxisCount>100</resqml:SlowestAxisCount>
  <resqml:Geometry>
    <resqml:LocalCrs>
      <eml:Uuid>5c0703c5-3806-424e-86cf-8f59c8bb39fa</eml:Uuid>
      <eml:QualifiedType>eml23.LocalEngineeringCompoundCrs</eml:QualifiedType>
      <eml:Title>Default local CRS</eml:Title>
    </resqml:LocalCrs>
    <resqml:Points xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:type="resqml:Point3dLatticeArray">
      <resqml:Origin>
        <resqml:Coordinate1>0.0</resqml:Coordinate1>
        <resqml:Coordinate2>0.0</resqml:Coordinate2>
        <resqml:Coordinate3>0.0</resqml:Coordinate3>
      </resqml:Origin>
      <resqml:Dimension>
        <resqml:Direction>
          <resqml:Coordinate1>0.0</resqml:Coordinate1>
          <resqml:Coordinate2>1.0</resqml:Coordinate2>
          <resqml:Coordinate3>0.0</resqml:Coordinate3>
        </resqml:Direction>
        <resqml:Spacing xsi:type="eml:FloatingPointConstantArray">
          <eml:Value>1.0</eml:Value>
          <eml:Count>99</eml:Count>
        </resqml:Spacing>
      </resqml:Dimension>
      <resqml:Dimension>
        <resqml:Direction>
          <resqml:Coordinate1>1.0</resqml:Coordinate1>
          <resqml:Coordinate2>0.0</resqml:Coordinate2>
          <resqml:Coordinate3>0.0</resqml:Coordinate3>
        </resqml:Direction>
        <resqml:Spacing xsi:type="eml:FloatingPointConstantArray">
          <eml:Value>1.0</eml:Value>
          <eml:Count>49</eml:Count>
        </resqml:Spacing>
      </resqml:Dimension>
    </resqml:Points>
  </resqml:Geometry>
</resqml:Grid2dRepresentation>
"""


# ---------------------------------------------------------------------------
# Helper: pretty-print a NumpyMesh
# ---------------------------------------------------------------------------

def print_mesh(mesh: NumpyMesh, *, max_rows: int = 8) -> None:
    """Print a short summary of *mesh* to stdout."""
    sep = "=" * 50
    print(sep)
    print(f"Type       : {type(mesh).__name__}")
    print(f"Identifier : {mesh.identifier!r}")
    print(f"Points     : shape={mesh.points.shape}  dtype={mesh.points.dtype}")

    # Show first max_rows rows so output stays readable.
    head = mesh.points[:max_rows]
    print(head)
    if len(mesh.points) > max_rows:
        print(f"  ... ({len(mesh.points) - max_rows} more rows)")

    if isinstance(mesh, NumpySurfaceMesh):
        print(f"Faces (VTK flat) : len={len(mesh.faces)}  dtype={mesh.faces.dtype}")
        print(mesh.faces[:min(len(mesh.faces), max_rows * 4)])

    elif isinstance(mesh, NumpyPolylineMesh):
        print(f"Lines (VTK flat) : len={len(mesh.lines)}  dtype={mesh.lines.dtype}")
        print(mesh.lines[:min(len(mesh.lines), max_rows * 3)])

    elif isinstance(mesh, NumpyVolumeMesh):
        print(f"Cells (VTK flat)  : len={len(mesh.cells)}   dtype={mesh.cells.dtype}")
        print(f"Cell types        : len={len(mesh.cell_types)} dtype={mesh.cell_types.dtype}")

    print()


# ---------------------------------------------------------------------------
# Reader functions — one per representation type
# ---------------------------------------------------------------------------

def read_numpy_grid(use_crs_displacement: bool = False) -> List[NumpyMesh]:
    """Read a Grid2dRepresentation from an embedded XML string (no EPC needed)."""
    grid_2d = read_energyml_xml_str(xml_grid_2d)
    if "DerivedElement" in str(type(grid_2d)):
        grid_2d = grid_2d.value

    meshes = read_numpy_mesh_object(
        energyml_object=grid_2d,
        workspace=None,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


def read_numpy_polyline(
    epc_path: str = "rc/epc/testingPackageCpp22.epc",
    polyline_uuid: str = "a54b8399-d3ba-4d4b-b215-8d4f8f537e66",
    use_crs_displacement: bool = True,
) -> List[NumpyMesh]:
    """Read a PolylineRepresentation (or PolylineSetRepresentation) by UUID."""
    epc = Epc.read_file(epc_path, read_rels_from_files=False, recompute_rels=False)

    polyline_obj = epc.get_object_by_uuid(polyline_uuid)[0]
    print(f"Object: {type(polyline_obj).__name__}  uuid={polyline_uuid}")

    meshes = read_numpy_mesh_object(
        energyml_object=polyline_obj,
        workspace=epc,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


def read_numpy_trset(
    epc_path: str = "rc/epc/testingPackageCpp22.epc",
    trset_uuid: str = "6e678338-3b53-49b6-8801-faee493e0c42",
    use_crs_displacement: bool = True,
) -> List[NumpyMesh]:
    """Read a TriangulatedSetRepresentation by UUID."""
    epc = Epc.read_file(epc_path, read_rels_from_files=False, recompute_rels=False)

    trset = epc.get_object_by_uuid(trset_uuid)[0]
    print(f"Object: {type(trset).__name__}  uuid={trset_uuid}")

    meshes = read_numpy_mesh_object(
        energyml_object=trset,
        workspace=epc,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


def read_numpy_pointset(
    epc_path: str = "rc/epc/testingPackageCpp22.epc",
    pointset_uuid: str = "fbc5466c-94cd-46ab-8b48-2ae2162b372f",
    use_crs_displacement: bool = True,
) -> List[NumpyMesh]:
    """Read a PointSetRepresentation by UUID.

    Uses EpcStreamReader to exercise the streaming path (same as arrays_test.py).
    """
    epc = EpcStreamReader(
        epc_file_path=epc_path,
        rels_update_mode=RelsUpdateMode.MANUAL,
    )

    pointset = epc.get_object_by_uuid(pointset_uuid)[0]
    print(f"Object: {type(pointset).__name__}  uuid={pointset_uuid}")

    meshes = read_numpy_mesh_object(
        energyml_object=pointset,
        workspace=epc,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


def read_numpy_wellbore_frame_repr(
    epc_path: str = "rc/epc/testingPackageCpp22.epc",
    well_uuid: str = "d873e243-d893-41ab-9a3e-d20b851c099f",
    use_crs_displacement: bool = True,
) -> List[NumpyMesh]:
    """Read a WellboreFrameRepresentation (or WellboreTrajectoryRepresentation)."""
    epc = Epc.read_file(epc_path, read_rels_from_files=False, recompute_rels=False)

    frame_repr = epc.get_object_by_uuid(well_uuid)[0]
    print(f"Object: {type(frame_repr).__name__}  uuid={well_uuid}")

    meshes = read_numpy_mesh_object(
        energyml_object=frame_repr,
        workspace=epc,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


def read_numpy_representation_set(
    epc_path: str = "rc/epc/testingPackageCpp22.epc",
    rep_set_uuid: str = "6b992199-5b47-4624-a62c-b70857133cda",
    use_crs_displacement: bool = True,
) -> List[NumpyMesh]:
    """Read a RepresentationSetRepresentation — returns all member meshes."""
    epc = Epc.read_file(epc_path, read_rels_from_files=False, recompute_rels=False)

    rep_set = epc.get_object_by_uuid(rep_set_uuid)[0]
    print(f"Object: {type(rep_set).__name__}  uuid={rep_set_uuid}")

    meshes = read_numpy_mesh_object(
        energyml_object=rep_set,
        workspace=epc,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


def read_numpy_wellbore_frame_repr_demo_jfr_02_26(
    epc_path: str = r"rc/epc/out-galaxy-12-pts.epc",
    well_uuid: str = "cfad9cb6-99fe-4172-b560-d2feca75dd9f",
    use_crs_displacement: bool = True,
) -> List[NumpyMesh]:
    """Read a wellbore frame from a galaxy EPC file via the streaming reader."""
    epc = EpcStreamReader(epc_path, rels_update_mode=RelsUpdateMode.MANUAL)

    frame_repr = epc.get_object_by_uuid(well_uuid)[0]
    print(f"Object: {type(frame_repr).__name__}  uuid={well_uuid}")

    meshes = read_numpy_mesh_object(
        energyml_object=frame_repr,
        workspace=epc,
        use_crs_displacement=use_crs_displacement,
    )
    return meshes


# ---------------------------------------------------------------------------
# Zero-copy demo: compare read_array vs read_array_view
# ---------------------------------------------------------------------------

def demo_zero_copy(h5_path: str = "rc/epc/testingPackageCpp22.h5") -> None:
    """Show that read_array_view returns a numpy view instead of a copy.

    A view shares memory with the original HDF5 buffer — no extra allocation.
    We confirm this by checking ``np.shares_memory`` and comparing dtype/shape.
    """
    handler_registry = get_handler_registry()
    h5_handler = handler_registry.get_handler_for_file(h5_path)
    if h5_handler is None:
        print(f"[demo_zero_copy] No handler found for {h5_path!r}")
        return

    # Use a dataset that exists in the standard test EPC.
    hdf5_path = "/resqml22/6e678338-3b53-49b6-8801-faee493e0c42/points_patch0"

    eager = h5_handler.read_array(source=h5_path, path_in_external_file=hdf5_path)
    view = h5_handler.read_array_view(source=h5_path, path_in_external_file=hdf5_path)

    print("-" * 50)
    print("demo_zero_copy")
    print(f"  Eager copy  : shape={eager.shape}  dtype={eager.dtype}  id={id(eager)}")
    print(f"  View/array  : shape={view.shape}   dtype={view.dtype}   id={id(view)}")
    print(f"  Same object : {eager is view}")
    # For contiguous HDF5 datasets numpy may or may not share memory depending
    # on the h5py version; we note what actually happened rather than asserting.
    print(f"  Shares memory: {np.shares_memory(eager, view)}")
    print()


# ---------------------------------------------------------------------------
# Optional: write + read-back a test array (from arrays_test.py)
# ---------------------------------------------------------------------------

def test_read_write_array_view(h5_path: str = "test_array_rw_fast.h5") -> None:
    """Write two datasets then read them back via both eager and view paths."""
    handler_registry = get_handler_registry()
    h5_handler = handler_registry.get_handler_for_file(h5_path)
    if h5_handler is None:
        print(f"No handler found for {h5_path}")
        return

    for i, arr in enumerate([np.array([[1, 2, 3], [4, 5, 6]]), np.arange(24, dtype=np.float32).reshape(4, 6)]):
        path = f"/test_dataset_{i}"
        h5_handler.write_array(array=arr, target=h5_path, path_in_external_file=path)
        h5_handler.file_cache.close_all()

        eager = h5_handler.read_array(source=h5_path, path_in_external_file=path)
        view = h5_handler.read_array_view(source=h5_path, path_in_external_file=path)

        print(f"Dataset {path!r}:")
        print(f"  eager : {eager}")
        print(f"  view  : {view}")
        assert np.array_equal(eager, view), "Mismatch between eager and view!"
        print("  [OK] values match\n")


# ---------------------------------------------------------------------------
# Optional: PyVista rendering
# ---------------------------------------------------------------------------

def render_meshes_pyvista(meshes: List[NumpyMesh], title: str = "NumpyMesh viewer") -> None:
    """Render a list of NumpyMesh objects in a PyVista plotter.

    Does nothing if pyvista is not installed.
    """
    if not _PYVISTA_AVAILABLE:
        print("[render_meshes_pyvista] pyvista not installed — skipping render.")
        return

    plotter = pv.Plotter(title=title)
    for mesh in meshes:
        try:
            pv_mesh = numpy_mesh_to_pyvista(mesh)
            plotter.add_mesh(pv_mesh, show_edges=True, label=mesh.identifier or type(mesh).__name__)
        except Exception as e:
            print(f"  [warn] Could not convert {type(mesh).__name__!r}: {e}")

    plotter.add_legend()
    plotter.show()


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    print("=" * 60)
    print("arrays_test_fast.py — NumpyMesh reader demo")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Define which readers to run.
    # Each entry is  (label, callable).
    # Comment / uncomment to control what gets exercised.
    # ------------------------------------------------------------------
    readers = [
        ("Grid2dRepresentation (embedded XML)", read_numpy_grid),
        ("PolylineRepresentation", read_numpy_polyline),
        ("TriangulatedSetRepresentation", read_numpy_trset),
        ("PointSetRepresentation", read_numpy_pointset),
        ("WellboreFrameRepresentation", read_numpy_wellbore_frame_repr),
        ("RepresentationSetRepresentation", read_numpy_representation_set),
        # ("WellboreFrame (galaxy EPC)", read_numpy_wellbore_frame_repr_demo_jfr_02_26),
    ]

    all_meshes: List[NumpyMesh] = []

    for label, reader in readers:
        print(f"\n{'─' * 60}")
        print(f"Running: {label}")
        print(f"{'─' * 60}")
        try:
            result = reader()
            print(f"  → {len(result)} mesh(es) returned")
            all_meshes.extend(result)
            for m in result:
                print_mesh(m)
        except Exception as exc:
            print(f"  [ERROR] {type(exc).__name__}: {exc}")

    # ------------------------------------------------------------------
    # Zero-copy comparison demo (reads directly from the HDF5 file):
    # ------------------------------------------------------------------
    # demo_zero_copy()

    # ------------------------------------------------------------------
    # Round-trip write + read-back test:
    # ------------------------------------------------------------------
    # test_read_write_array_view()

    print(f"\n{'=' * 60}")
    print(f"Total meshes collected: {len(all_meshes)}")
    print(f"{'=' * 60}\n")

    # ------------------------------------------------------------------
    # Optional PyVista render (only if pyvista is installed):
    # ------------------------------------------------------------------
    # render_meshes_pyvista(all_meshes)


if __name__ == "__main__":
    # Run $env:PYTHONPATH="src" if it fails to be executed from the project root.
    print("hello")
    main()
