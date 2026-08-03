# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Mesh export to various file formats.

One module per format — :mod:`obj`, :mod:`off`, :mod:`geojson`, :mod:`vtk`, :mod:`stl` — each
declaring what it can do through a :class:`~._registry.FormatSpec`. The dispatcher
:func:`export_mesh` and the UI helpers (``format_description``, ``format_filter_string``,
``supports_lines``, …) all read that registry, so adding a format means adding a module and one
registration, not editing six places.

Both mesh hierarchies are accepted by every export function: the legacy
:class:`~energyml.utils.data.mesh.AbstractMesh` and the numpy
:class:`~energyml.utils.data.mesh_numpy.NumpyMesh` / ``NumpyMultiMesh``.

Coordinate frames
-----------------
Every writer takes ``frame=`` and ``origin_shift=``, not just the GeoJSON one:

* ``frame`` — :class:`~energyml.utils.data.crs.PointFrame`: ``LOCAL``, ``PROJECTED`` (default for
  the 3-D formats) or ``WGS84`` (default for GeoJSON, as RFC 7946 requires). Each mesh records the
  frame it is already in, so only the missing stages are applied and no transform runs twice.
* ``origin_shift`` — ``None``, ``"auto"`` or an explicit ``(dx, dy, dz)``. Projected coordinates
  carry 6-7 significant digits, which loses precision once a viewer reads the file as float32;
  recentring restores it. ``"auto"`` is resolved **once** over the whole export so the patches keep
  their relative positions.

The legacy ``use_crs_displacement`` flag is still accepted and simply selects the default frame
(``PROJECTED`` when True, ``LOCAL`` when False).
"""

from energyml.utils.data.export._base import (
    ExportFormat,
    ExportOptions,
    GeoJSONExportOptions,
    EmptyMeshError,
    drop_empty_patches,
    STLExportOptions,
    VTKExportOptions,
    VTKFormat,
    resolve_origin_shift,
)
from energyml.utils.data.export._registry import (
    FormatSpec,
    all_formats_filter_string,
    export_mesh,
    format_description,
    format_filter_string,
    get_format_options_class,
    get_format_spec,
    register_format,
    registered_formats,
    supported_formats,
    supports_lines,
    supports_pointsets,
    supports_triangles,
)

# Importing the format modules is what populates the registry.
# The private helpers are re-exported on purpose: they were importable from the old
# `export` module and external code (and mesh.py) still reaches for them.
from energyml.utils.data.export.geojson import (  # noqa: E402,F401
    _feature_id,
    _geojson_bbox,
    _geojson_crs_members,
    _prepare_geojson_points,
    export_geojson,
)
from energyml.utils.data.export.obj import export_obj  # noqa: E402
from energyml.utils.data.export.off import export_off, export_off_part  # noqa: E402
from energyml.utils.data.export.stl import export_stl  # noqa: E402
from energyml.utils.data.export.vtk import export_vtk  # noqa: E402

__all__ = [
    # Formats / options
    "ExportFormat",
    "ExportOptions",
    "GeoJSONExportOptions",
    "EmptyMeshError",
    "drop_empty_patches",
    "STLExportOptions",
    "VTKExportOptions",
    "VTKFormat",
    # Registry
    "FormatSpec",
    "register_format",
    "get_format_spec",
    "registered_formats",
    # Writers
    "export_mesh",
    "export_obj",
    "export_off",
    "export_off_part",
    "export_geojson",
    "export_vtk",
    "export_stl",
    # Frame helpers
    "resolve_origin_shift",
    # UI helpers
    "supported_formats",
    "format_description",
    "format_filter_string",
    "all_formats_filter_string",
    "get_format_options_class",
    "supports_lines",
    "supports_triangles",
    "supports_pointsets",
]
