# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""
Readers for energyml *properties* and tables: continuous / discrete / categorical / comment
properties, column-based tables and time series.

Split out of :mod:`energyml.utils.data.mesh`, which re-exports every public name here so existing
imports keep working. They never had anything to do with meshes, and sharing that module had a
concrete consequence: :func:`read_property` dispatches on ``read_<snake_case(type)>`` in its own
module namespace, which used to contain the geometry readers too — so calling it on, say, a
``PointRepresentation`` silently returned meshes instead of raising.
"""

import logging
import sys
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

from energyml.utils.data.helper import read_array
from energyml.utils.exception import NotSupportedError
from energyml.utils.introspection import (
    get_obj_uri,
    get_object_attribute,
    search_attribute_matching_name,
    search_attribute_matching_name_with_path,
    snake_case,
)
from energyml.utils.storage_interface import EnergymlStorageInterface

logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_property_reader_function(property_type_name: str) -> Optional[Callable]:
    """Return the ``read_<snake_case(type)>`` function of this module, or None.

    Only functions defined here are eligible, so an imported helper (``read_array``) can never be
    mistaken for a property reader.
    """
    reader = getattr(sys.modules[__name__], f"read_{snake_case(property_type_name)}", None)
    if not callable(reader) or getattr(reader, "__module__", None) != __name__:
        return None
    return reader


def read_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a property or column-based table from an Energyml object.

    Dispatches to the appropriate reader function based on the object's type name.
    If no specific reader is found, raises a NotSupportedError.

    Args:
        energyml_object: The Energyml object to read from.
        workspace: The storage interface for accessing related objects.

    Returns:
        np.ndarray: The read property or table data.

    Raises:
        NotSupportedError: If the object type is not supported.
    """
    property_type = type(energyml_object).__name__
    reader_func = get_property_reader_function(property_type)
    if reader_func is not None:
        return reader_func(energyml_object=energyml_object, workspace=workspace)
    else:
        # logger.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise NotSupportedError(
            f"Type {property_type} is not supported\n\tfunction read_{snake_case(property_type)} not found"
        )


def read_property_interpreted_with_cbt(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
    _cache_property_arrays: Optional[np.ndarray] = None,
    _return_none_if_no_category_lookup: bool = False,
) -> Optional[np.ndarray]:
    """
    Read a property with category lookup interpretation.

    Reads property arrays and applies category lookup mapping if available.
    Supports both array and dictionary-based category lookups.

    Args:
        energyml_object: The Energyml property object.
        workspace: The storage interface for accessing related objects.
        _cache_property_arrays: Optional cached property arrays to avoid re-reading.
        _return_none_if_no_category_lookup: If True, return None when no category lookup is found.

    Returns:
        Optional[np.ndarray]: The interpreted property values, or None if no lookup and flag is set.
    """

    result = None

    prop_arrays = (
        read_property(energyml_object, workspace) if _cache_property_arrays is None else _cache_property_arrays
    )

    category_lookup_dor = get_object_attribute(energyml_object, "category_lookup")
    if category_lookup_dor is not None:
        category_lookup_obj = workspace.get_object(get_obj_uri(category_lookup_dor))
        if category_lookup_obj is not None:
            category_lookup_data = read_column_based_table(category_lookup_obj, workspace)

            # print(f"category_lookup_array : {category_lookup_data}")
            if isinstance(category_lookup_data, list):
                category_lookup_data = np.array(category_lookup_data)
            if isinstance(category_lookup_data, np.ndarray):
                # map props values to category lookup values using prop value as index in category lookup array
                result = (
                    np.array(
                        [
                            (
                                category_lookup_data[prop]
                                if prop is not None and prop < len(category_lookup_data)
                                else None
                            )
                            for prop in prop_arrays
                        ]
                    )
                    if prop_arrays is not None
                    else None
                )
            elif isinstance(category_lookup_data, dict):
                # Transpose so that each index corresponds to a category (column), not a row.
                # logger.debug(f"category_lookup_data dict : {category_lookup_data}")

                # Guard against inhomogeneous column lengths (e.g. one column is
                # empty while another is not).  Pad all columns with None up to
                # the maximum column length so that np.array() can build a
                # rectangular (n_columns, max_rows) matrix before transposing.
                col_values = [list(v) if not isinstance(v, list) else v for v in category_lookup_data.values()]
                max_len = max((len(c) for c in col_values), default=0)
                if max_len == 0:
                    # All columns empty — nothing to look up.
                    return prop_arrays if not _return_none_if_no_category_lookup else None

                padded = [c + [None] * (max_len - len(c)) for c in col_values]
                category_lookup_matrice = np.array(padded, dtype=object).T
                # logger.debug(f"category_lookup_matrice : {category_lookup_matrice}")
                # return a matrice with the same shape as prop_arrays but with the values from the category lookup array using the prop value as key in the category lookup array
                result = (
                    np.array(
                        [
                            [
                                (
                                    category_lookup_matrice[prop].tolist()
                                    if prop is not None and 0 <= prop < len(category_lookup_matrice)
                                    else None
                                )
                                for prop in prop_row
                            ]
                            for prop_row in prop_arrays
                        ]
                    )
                    if prop_arrays is not None
                    else None
                )
            else:
                # category_lookup_data is what was actually read; the previous message referred to
                # a variable only bound in the dict branch above, which raised NameError instead.
                raise NotSupportedError(
                    f"Category lookup array type {type(category_lookup_data)} is not supported, expected list or dict"
                )

    return prop_arrays if result is None and not _return_none_if_no_category_lookup else result


def read_abstract_values_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read abstract values property from patches.

    Extracts and concatenates arrays from all 'values_for_patch' attributes.

    Args:
        energyml_object: The Energyml object containing the property.
        workspace: The storage interface for accessing arrays.

    Returns:
        np.ndarray: The concatenated array of property values.
    """
    arrays = []
    for values_for_patch in search_attribute_matching_name_with_path(energyml_object, "values_for_patch"):
        array = read_array(
            energyml_array=values_for_patch[1],
            root_obj=energyml_object,
            path_in_root=".",
            workspace=workspace,
        )
        if isinstance(array, list):
            array = np.array(array)
        arrays.append(array)
    if len(arrays) == 1:
        return arrays[0]
    else:
        return np.concatenate(arrays)


def read_discrete_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a discrete property.

    Delegates to read_abstract_values_property for implementation.

    Args:
        energyml_object: The discrete property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The property values.
    """

    return read_abstract_values_property(energyml_object, workspace)


def read_continuous_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a continuous property.

    Delegates to read_abstract_values_property for implementation.

    Args:
        energyml_object: The continuous property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The property values.
    """

    return read_abstract_values_property(energyml_object, workspace)


def read_categorical_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a categorical property.

    Note: Categorical values are returned as integers. Use the property's
    'code_list' attribute to map to string values.

    Args:
        energyml_object: The categorical property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The integer-coded property values.
    """
    # TODO: the categorical values should be converted to strings using the code list of the property, but for now we keep the integer values and let the user manage the conversion if needed.
    logger.warning(
        "CategoricalProperty is read as a continuous property, the categorical values are not converted to strings but kept as integers. Use the 'code_list' attribute of the property to get the list of possible string values corresponding to the integer values in the array"
    )
    return read_abstract_values_property(energyml_object, workspace)


def read_comment_property(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> np.ndarray:
    """
    Read a comment property.

    Delegates to read_abstract_values_property for implementation.

    Args:
        energyml_object: The comment property object.
        workspace: The storage interface.

    Returns:
        np.ndarray: The comment values.
    """
    return read_abstract_values_property(energyml_object, workspace)


def read_column_based_table(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> Dict[str, np.ndarray]:
    """
    Read a column-based table.

    Extracts column data into a dictionary keyed by column titles.

    Args:
        energyml_object: The table object with 'column' attributes.
        workspace: The storage interface for accessing arrays.

    Returns:
        Dict[str, np.ndarray]: Dictionary of column names to arrays.
    """
    columns = {}
    for column in get_object_attribute(energyml_object, "column"):
        column_name = getattr(column, "title", "_")
        # print(f"Reading column: {column_name} : {column}")
        # print(f"getattr(column_array, 'values', None): {getattr(column, 'values', None)}")
        array = read_array(
            energyml_array=getattr(column, "values", None),
            root_obj=energyml_object,
            path_in_root=".",
            workspace=workspace,
        )
        if isinstance(array, list):
            array = np.array(array)
        columns[column_name] = array
    return columns


def read_time_series(
    energyml_object: Any,
    workspace: EnergymlStorageInterface,
) -> List[Tuple[str, int]]:
    """
    Read a time series from an Energyml object.

    Extracts date-time values and time step indices, constructing a normalized
    list of (step_index, datetime) tuples for each time step.

    Args:
        energyml_object: The Energyml time series object.
        workspace: The storage interface for accessing related objects.

    Returns:
        List[Tuple[str, int]]: List of tuples containing (step_index, datetime_string).
    """

    # 1. Extraction des DateTime
    times_iso = search_attribute_matching_name(energyml_object, "date_time")

    # 2. Extraction des TimeSteps (v2.2+)
    steps_indices = []
    time_step_obj = get_object_attribute(energyml_object, "time_step")
    if time_step_obj is not None:
        steps_indices = read_array(time_step_obj, energyml_object, ".", workspace, sub_indices=None)
    else:
        # Fallback : on utilise l'index de la liste
        steps_indices = list(range(len(times_iso)))

    # 3. Construction de la structure normalisée
    steps_data = []
    for i in range(len(times_iso)):
        steps_data.append(
            (steps_indices[i], times_iso[i])
            # {"index": i, "datetime": times_iso[i], "step_val": steps_indices[i]}  # L'index utilisé par les propriétés
        )

    return steps_data


#: Public API of this module. Declared explicitly so that renaming or removing anything
#: else is not a breaking change, and so `from ... import *` does not leak the imports.
__all__ = [
    "get_property_reader_function",
    "read_property",
    "read_property_interpreted_with_cbt",
    "read_abstract_values_property",
    "read_discrete_property",
    "read_continuous_property",
    "read_categorical_property",
    "read_comment_property",
    "read_column_based_table",
    "read_time_series",
]
