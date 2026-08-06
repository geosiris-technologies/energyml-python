# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""Format registry and the :func:`export_mesh` dispatcher.

Everything a format needs to be usable — how to write it, what options it takes, how to describe
it in a file dialog, which primitives it supports — is declared **once**, in a :class:`FormatSpec`
registered by the format's own module. Adding a format is therefore a new module plus one
:func:`register_format` call.

Before, the same six formats were enumerated in an ``elif`` chain in ``export_mesh`` and in five
separate dictionaries (``format_description``, ``format_filter_string``, ``get_format_options_class``,
``supports_lines``, ``supports_pointsets``), so a new format meant editing six places and a missing
entry degraded silently to a default.
"""

from __future__ import annotations

import logging
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from energyml.utils.data.export._base import ExportFormat, ExportOptions, drop_empty_patches

if TYPE_CHECKING:
    from energyml.utils.data.crs import PointFrame
    from energyml.utils.data.representation_context import RepresentationContext

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FormatSpec:
    """Everything the export machinery knows about one output format."""

    format: ExportFormat
    """The enum member this spec describes."""

    description: str
    """Human-readable description, shown in UIs."""

    filter_label: str
    """File-dialog filter label, e.g. ``"OBJ Files (*.obj)"``."""

    writer: Callable[..., None]
    """
    The writing function. Called as
    ``writer(mesh_list, out, options=..., contexts=..., use_crs_displacement=..., frame=...,
    origin_shift=...)``.
    """

    binary: bool = True
    """Whether *out* must be a binary stream. GeoJSON is the only text format."""

    options_class: Optional[type] = None
    """Options class accepted by the writer, when it takes one."""

    supports_lines: bool = True
    supports_triangles: bool = True
    supports_pointsets: bool = True

    force_options: Optional[Dict[str, Any]] = None
    """
    Option attributes forced before calling the writer. Used by ``.vtu`` / ``.vtp``, which share
    the VTK writer but pin its sub-format.
    """

    companion_suffix: Optional[str] = None
    """
    Suffix of a side-car file the format writes next to the main one, opened only when *contexts*
    are provided. OBJ uses it for its ``.mtl`` material file.
    """


_REGISTRY: Dict[ExportFormat, FormatSpec] = {}


def register_format(spec: FormatSpec) -> FormatSpec:
    """Register *spec*, replacing any previous entry for the same format."""
    _REGISTRY[spec.format] = spec
    return spec


def get_format_spec(format: Union[str, ExportFormat]) -> FormatSpec:
    """Return the :class:`FormatSpec` of *format*.

    :raises ValueError: when the format is unknown or its module was not imported.
    """
    if isinstance(format, str):
        format = ExportFormat.from_extension(format)
    spec = _REGISTRY.get(format)
    if spec is None:
        raise ValueError(
            f"No writer registered for format {format}. " f"Registered: {sorted(f.value for f in _REGISTRY)}."
        )
    return spec


def registered_formats() -> List[ExportFormat]:
    """Return the registered formats, in registration order."""
    return list(_REGISTRY)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def export_mesh(
    mesh_list: Any,
    output_path: Union[str, Path],
    format: Optional[ExportFormat] = None,
    options: Optional[ExportOptions] = None,
    contexts: Optional[Dict[str, "RepresentationContext"]] = None,
    use_crs_displacement: bool = True,
    frame: Optional["PointFrame"] = None,
    origin_shift: Optional[Any] = None,
) -> None:
    """Export mesh data to a file.

    Format is auto-detected from the file extension when *format* is None.

    :param mesh_list: Meshes to export.
    :param output_path: Destination file path.
    :param format: Explicit format; auto-detected from the extension when None.
    :param options: Format-specific options.
    :param contexts: Color / metadata context dict.
    :param use_crs_displacement: Legacy switch selecting the default target frame
        (``PointFrame.PROJECTED`` when True, ``PointFrame.LOCAL`` when False). Ignored when
        *frame* is given.
    :param frame: Target coordinate frame, e.g. ``PointFrame.WGS84``. Available for **every**
        format, not only GeoJSON.
    :param origin_shift: ``None``, ``"auto"``, or an explicit ``(dx, dy, dz)`` vector subtracted
        from the coordinates. ``"auto"`` recentres on the bounding-box centre of the whole export,
        computed once and applied identically to every patch. Useful for projected coordinates,
        whose 6-7 significant digits lose precision when a viewer reads the file as float32.
    """
    path = Path(output_path)
    if format is None:
        format = ExportFormat.from_extension(path.suffix)

    spec = get_format_spec(format)

    if spec.force_options:
        if spec.options_class is not None and not isinstance(options, spec.options_class):
            options = spec.options_class()
        for attr, value in spec.force_options.items():
            setattr(options, attr, value)

    kwargs: Dict[str, Any] = {
        "obj_name": path.stem,
        "options": options,
        "contexts": contexts,
        "use_crs_displacement": use_crs_displacement,
        "frame": frame,
        "origin_shift": origin_shift,
    }

    mesh_list = drop_empty_patches(mesh_list, raise_when_empty=True)

    with ExitStack() as stack:
        if spec.binary:
            out = stack.enter_context(path.open("wb"))
        else:
            out = stack.enter_context(path.open("w", encoding="utf-8"))
        if spec.companion_suffix and contexts:
            companion_path = path.with_suffix(spec.companion_suffix)
            kwargs["companion"] = stack.enter_context(companion_path.open("wb"))
        spec.writer(mesh_list, out, **kwargs)


# ---------------------------------------------------------------------------
# UI helpers — all derived from the registry
# ---------------------------------------------------------------------------


def supported_formats() -> List[str]:
    """Return all supported export format extensions."""
    return [fmt.value for fmt in _REGISTRY]


def format_description(format: Union[str, ExportFormat]) -> str:
    """Return a human-readable description of *format*."""
    try:
        return get_format_spec(format).description
    except ValueError:
        return "Unknown format"


def format_filter_string(format: Union[str, ExportFormat]) -> str:
    """Return a file-dialog filter string (e.g. ``"VTU Files (*.vtu)"``)."""
    try:
        return get_format_spec(format).filter_label
    except ValueError:
        return "All Files (*.*)"


def all_formats_filter_string() -> str:
    """Return a ``;;``-joined filter string for all supported formats."""
    return ";;".join(spec.filter_label for spec in _REGISTRY.values())


def get_format_options_class(format: Union[str, ExportFormat]) -> Optional[type]:
    """Return the options class for *format*, or None."""
    try:
        return get_format_spec(format).options_class
    except ValueError:
        return None


def supports_lines(format: Union[str, ExportFormat]) -> bool:
    """Return True when *format* can represent polyline primitives."""
    try:
        return get_format_spec(format).supports_lines
    except ValueError:
        return False


def supports_triangles(format: Union[str, ExportFormat]) -> bool:
    """Return True when *format* can represent triangle / polygon primitives."""
    try:
        return get_format_spec(format).supports_triangles
    except ValueError:
        return False


def supports_pointsets(format: Union[str, ExportFormat]) -> bool:
    """Return True when *format* can represent point-cloud primitives."""
    try:
        return get_format_spec(format).supports_pointsets
    except ValueError:
        return False


#: Public API of this module. Declared explicitly so that renaming or removing anything
#: else is not a breaking change, and so `from ... import *` does not leak the imports.
__all__ = [
    "FormatSpec",
    "register_format",
    "get_format_spec",
    "registered_formats",
    "export_mesh",
    "supported_formats",
    "format_description",
    "format_filter_string",
    "all_formats_filter_string",
    "get_format_options_class",
    "supports_lines",
    "supports_triangles",
    "supports_pointsets",
]
