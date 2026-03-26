# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import logging
import sys
from typing import Any, Literal, Optional, Callable, List, Tuple, Union

from energyml.utils.storage_interface import EnergymlStorageInterface
import numpy as np

from energyml.utils.data.datasets_io import read_external_dataset_array, get_path_in_external_with_path
from energyml.utils.constants import flatten_concatenation, path_last_attribute, path_parent_attribute
from energyml.utils.exception import ObjectNotFoundNotError
from energyml.utils.introspection import (
    get_obj_uri,
    snake_case,
    get_object_attribute_no_verif,
    search_attribute_matching_name_with_path,
    search_attribute_matching_name,
    search_attribute_matching_type,
    search_attribute_in_upper_matching_name,
    get_obj_uuid,
    get_object_attribute,
    get_object_attribute_rgx,
    get_object_attribute_advanced,
    is_primitive,
    get_obj_title,
)

from energyml.utils.data.crs import CrsInfo, extract_crs_info  # noqa: F401  (re-exported for convenience)

_ARRAY_NAMES_ = [
    "BooleanArrayFromDiscretePropertyArray",
    "BooleanArrayFromIndexArray",
    "BooleanConstantArray",
    "BooleanExternalArray",
    "BooleanHdf5Array",
    "BooleanXmlArray",
    "CompoundExternalArray",
    "DasTimeArray",
    "DoubleConstantArray",
    "DoubleHdf5Array",
    "DoubleLatticeArray",
    "ExternalDataArray",
    "FloatingPointConstantArray",
    "FloatingPointExternalArray",
    "FloatingPointLatticeArray",
    "FloatingPointXmlArray",
    "IntegerArrayFromBooleanMaskArray",
    "IntegerConstantArray",
    "IntegerExternalArray",
    "IntegerHdf5Array",
    "IntegerLatticeArray",
    "IntegerRangeArray",
    "IntegerXmlArray",
    "JaggedArray",
    "ParametricLineArray",
    "ParametricLineFromRepresentationLatticeArray",
    "Point2DHdf5Array",
    "Point3DFromRepresentationLatticeArray",
    "Point3DHdf5Array",
    "Point3DLatticeArray",
    "Point3DParametricArray",
    "Point3DZvalueArray",
    "ResqmlJaggedArray",
    "StringConstantArray",
    "StringExternalArray",
    "StringHdf5Array",
    "StringXmlArray",
]


def _point_as_array(point: Any) -> List:
    """
    Transform a point that has "coordinate1", "coordinate2", "coordinate3" as attributes into a list.
    :param point:
    :return:
    """
    return [
        get_object_attribute_no_verif(point, "coordinate1"),
        get_object_attribute_no_verif(point, "coordinate2"),
        get_object_attribute_no_verif(point, "coordinate3"),
    ]


def is_z_reversed(crs: Optional[Any], workspace: Optional[EnergymlStorageInterface] = None) -> bool:
    """
    Returns True if the Z axis increases downward
    (``ZIncreasingDownward==True`` or ``VerticalAxis.Direction=='down'``).

    Delegates to :func:`extract_crs_info`.

    :param crs: a CRS object
    :return: By default, ``False`` is returned when *crs* is ``None``.
    """
    result = extract_crs_info(crs, workspace).z_increasing_downward
    # logging.debug(f"is_z_reversed: {result}")
    return result


def get_vertical_epsg_code(crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None) -> Optional[int]:
    """Return the EPSG code of the vertical CRS.  Delegates to :func:`extract_crs_info`."""
    return extract_crs_info(crs_object).vertical_epsg_code


def get_projected_epsg_code(crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None) -> Optional[int]:
    """Return the EPSG code of the projected (horizontal) CRS.  Delegates to :func:`extract_crs_info`."""
    return extract_crs_info(crs_object, workspace).projected_epsg_code


def get_projected_uom(crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None) -> Optional[str]:
    """Return the UOM string for the projected (horizontal) CRS.  Delegates to :func:`extract_crs_info`."""
    return extract_crs_info(crs_object, workspace).projected_uom


def get_crs_offsets_and_angle(
    crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None
) -> Tuple[float, float, float, Tuple[float, str]]:
    """
    Return the CRS offsets (X, Y, Z) and the areal rotation angle ``(value, uom)``.

    Delegates to :func:`extract_crs_info` and unpacks the result back into the
    original ``(x, y, z, (angle, uom))`` tuple format for backward compatibility.
    """
    info = extract_crs_info(crs_object, workspace)
    return info.x_offset, info.y_offset, info.z_offset, (info.areal_rotation_value, info.areal_rotation_uom)


def apply_crs_transform(
    well_points: np.ndarray,
    x_offset: float = 0.0,
    y_offset: float = 0.0,
    z_offset: float = 0.0,
    areal_rotation: float = 0.0,
    rotation_uom: str = "rad",
    z_is_up: bool = True,
) -> np.ndarray:
    """
    Transforms interpolated wellbore points from Local CRS to Global/Project coordinates.

    Args:
        well_points: A (N, 3) numpy array of interpolated [X, Y, Z] points.
        x_offset: The X translation value (resqml:XOffset).
        y_offset: The Y translation value (resqml:YOffset).
        z_offset: The Z translation value (resqml:ZOffset).
        areal_rotation: The rotation angle (azimuth of the local CRS grid).
        rotation_uom: The unit of measure for the rotation ('rad' or 'degr').
        z_is_up: If True, converts Z values to 'Up is Positive' (negates RESQML Z).

    Returns:
        A (N, 3) numpy array of transformed coordinates.
    """
    # Create a copy to avoid mutating the original input array
    transformed: np.ndarray = well_points.copy().astype(np.float64)

    # 1. Convert rotation to radians if necessary
    angle_rad: float = areal_rotation
    if rotation_uom == "degr":
        angle_rad = np.radians(areal_rotation)

    # 2. Handle Areal Rotation (Rotation around the Z axis)
    # Applied before translation as per Energistics standards.
    # RESQML ArealRotation / Azimuth is a CLOCKWISE angle (not the standard
    # CCW mathematical convention).  The correct CW rotation matrix is:
    #   x' = x·cos θ + y·sin θ
    #   y' = −x·sin θ + y·cos θ
    if angle_rad != 0.0:
        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)

        x_orig = transformed[:, 0].copy()
        y_orig = transformed[:, 1].copy()

        # Clockwise rotation (RESQML convention)
        transformed[:, 0] = x_orig * cos_theta + y_orig * sin_theta
        transformed[:, 1] = -x_orig * sin_theta + y_orig * cos_theta

    # 3. Apply Translation (Offsets)
    transformed[:, 0] += x_offset
    transformed[:, 1] += y_offset
    transformed[:, 2] += z_offset

    # 4. Final Vertical Orientation
    # Negate Z if the target system is Z-Up (RESQML is natively Z-Down).
    if z_is_up:
        transformed[:, 2] = -transformed[:, 2]

    return transformed


def get_crs_origin_offset(crs_obj: Any) -> np.ndarray:
    """
    Return a ``(3,) float64`` numpy array ``[X, Y, Z]`` corresponding to the
    CRS origin offset (``XOffset``/``OriginProjectedCoordinate1``, …) depending
    on the energyml version.

    Returning an ndarray instead of a plain list avoids the ``np.asarray()``
    call in callers such as :func:`mesh_numpy.crs_displacement_np`.

    :param crs_obj:
    :return:
    """
    tmp_offset_x = get_object_attribute_rgx(crs_obj, "XOffset")
    if tmp_offset_x is None:
        tmp_offset_x = get_object_attribute_rgx(crs_obj, "OriginProjectedCoordinate1")

    tmp_offset_y = get_object_attribute_rgx(crs_obj, "YOffset")
    if tmp_offset_y is None:
        tmp_offset_y = get_object_attribute_rgx(crs_obj, "OriginProjectedCoordinate2")

    tmp_offset_z = get_object_attribute_rgx(crs_obj, "ZOffset")
    if tmp_offset_z is None:
        tmp_offset_z = get_object_attribute_rgx(crs_obj, "OriginProjectedCoordinate3")

    try:
        return np.array(
            [
                float(tmp_offset_x) if tmp_offset_x is not None else 0.0,
                float(tmp_offset_y) if tmp_offset_y is not None else 0.0,
                float(tmp_offset_z) if tmp_offset_z is not None else 0.0,
            ],
            dtype=np.float64,
        )
    except Exception as e:
        logging.info(f"ERR reading crs offset {e}")
        return np.zeros(3, dtype=np.float64)


def get_datum_information(
    datum_obj: Any, workspace: Optional[EnergymlStorageInterface] = None
) -> Tuple[float, float, float, bool, Optional[str], Optional[str], Optional[Any]]:
    "From a ObjMdDatum or a ReferencePointInACrs, return x, y, z, z_increas_downward, projected_epsg_code, vertical_epsg_code, crs object"
    if datum_obj is None:
        return 0.0, 0.0, 0.0, False, None, None, None

    t_lw = type(datum_obj).__name__.lower()

    # resqml20.LocalDepth3dCrs
    if "localdepth3dcrs" in t_lw:
        x = get_object_attribute_rgx(datum_obj, "XOffset.value")
        y = get_object_attribute_rgx(datum_obj, "YOffset.value")
        z = get_object_attribute_rgx(datum_obj, "ZOffset.value")
        z_increasing_downward = get_object_attribute(datum_obj, "ZIncreasingDownward") or False
        projected_epsg_code = get_projected_epsg_code(datum_obj, workspace)
        vertical_epsg_code = get_vertical_epsg_code(datum_obj)
        return (
            float(x) if x is not None else 0.0,
            float(y) if y is not None else 0.0,
            float(z) if z is not None else 0.0,
            z_increasing_downward,
            projected_epsg_code,
            vertical_epsg_code,
            datum_obj,
        )
    elif "referencepointinacrs" in t_lw:
        x = get_object_attribute_rgx(datum_obj, "horizontal_coordinates.coordinate1")
        y = get_object_attribute_rgx(datum_obj, "horizontal_coordinates.coordinate2")
        z = get_object_attribute_rgx(datum_obj, "vertical_coordinate")
        z_increasing_downward = False
        v_crs_dor = get_object_attribute_rgx(datum_obj, "vertical_crs")
        if v_crs_dor is not None and workspace is not None:
            v_crs = workspace.get_object(get_obj_uri(v_crs_dor))
            if v_crs is not None:
                z_increasing_downward = is_z_reversed(v_crs)
        p_crs = get_object_attribute(datum_obj, "horizontal_coordinates.crs")
        projected_epsg_code = (
            get_projected_epsg_code(workspace.get_object(get_obj_uri(p_crs)), workspace)
            if p_crs is not None and workspace is not None
            else None
        )
        v_crs = get_object_attribute(datum_obj, "vertical_crs")
        vertical_epsg_code = get_vertical_epsg_code(v_crs) if v_crs is not None else None
        return (
            float(x) if x is not None else 0.0,
            float(y) if y is not None else 0.0,
            float(z) if z is not None else 0.0,
            z_increasing_downward,
            projected_epsg_code,
            vertical_epsg_code,
            p_crs,
        )
    elif "mddatum" in t_lw:
        x = get_object_attribute_rgx(datum_obj, "location.coordinate1")
        y = get_object_attribute_rgx(datum_obj, "location.coordinate2")
        z = get_object_attribute_rgx(datum_obj, "location.coordinate3")
        crs = get_object_attribute(datum_obj, "LocalCrs")
        _, _, _, z_increasing_downward, projected_epsg_code, vertical_epsg_code, _ = get_datum_information(
            crs, workspace
        )
        return (
            float(x) if x is not None else 0.0,
            float(y) if y is not None else 0.0,
            float(z) if z is not None else 0.0,
            z_increasing_downward,
            projected_epsg_code,
            vertical_epsg_code,
            crs,
        )
    return 0.0, 0.0, 0.0, False, None, None, None


# ==================================================


def prod_n_tab(val: Union[float, int, str], tab: List[Union[float, int, str]]):
    """
    Multiply every value of the list 'tab' by the constant 'val'
    :param val:
    :param tab:
    :return:
    """
    if val is None:
        return [None] * len(tab)
    # logging.debug(f"Multiplying list by {val}: {tab}")
    # Convert to numpy array for vectorized operations, handling None values
    arr = np.array(tab, dtype=object)
    # logging.debug(f"arr: {arr}")
    # Create mask for non-None values
    mask = arr != None  # noqa: E711
    # Create result array filled with None
    result = np.full(len(tab), None, dtype=object)
    # logging.debug(f"result before multiplication: {result}")
    # Multiply only non-None values
    result[mask] = arr[mask].astype(float) * val
    # logging.debug(f"result after multiplication: {result}")
    return result.tolist()


def sum_lists(l1: List, l2: List):
    """
    Sums 2 lists values, preserving None values.

    Example:
        [1,1,1] and [2,2,3,6] gives : [3,3,4,6]
        [1,None,3] and [2,2,3] gives : [3,None,6]

    :param l1:
    :param l2:
    :return:
    """
    min_len = min(len(l1), len(l2))

    # Convert to numpy arrays for vectorized operations
    arr1 = np.array(l1[:min_len], dtype=object)
    arr2 = np.array(l2[:min_len], dtype=object)

    # Create result array
    result = np.full(min_len, None, dtype=object)

    # Find indices where both values are not None
    mask = (arr1 != None) & (arr2 != None)  # noqa: E711

    # Sum only where both are not None
    if np.any(mask):
        result[mask] = arr1[mask].astype(float) + arr2[mask].astype(float)

    # Convert back to list and append remaining elements from longer list
    result_list = result.tolist()
    if len(l1) > min_len:
        result_list.extend(l1[min_len:])
    elif len(l2) > min_len:
        result_list.extend(l2[min_len:])

    return result_list


def get_crs_obj(
    context_obj: Any,
    path_in_root: Optional[str] = None,
    root_obj: Optional[Any] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
) -> Optional[Any]:
    """
    Search for the CRS object related to :param:`context_obj` into the :param:`workspace`
    :param context_obj:
    :param path_in_root:
    :param root_obj:
    :param workspace:
    :return:
    """
    if workspace is None:
        logging.error("@get_crs_obj no Epc file given")
    else:
        crs_list = search_attribute_matching_name(context_obj, r"\.*Crs", search_in_sub_obj=True, deep_search=False)
        if crs_list is not None and len(crs_list) > 0 and crs_list[0] is not None:
            # logging.debug(crs_list[0])
            crs = workspace.get_object(get_obj_uri(crs_list[0]))
            # logging.debug(f"CRS found for {get_obj_title(context_obj)} ({type(context_obj).__name__}): {crs}")
            if crs is None:
                # if a wrong version is written in DOR
                # logging.debug(f"CRS {crs_list[0]} not found (or not read correctly)")
                _crs_list = workspace.get_object_by_uuid(get_obj_uuid(crs_list[0]))
                crs = _crs_list[0] if _crs_list is not None and len(_crs_list) > 0 else None
            if crs is None:
                logging.error(f"CRS {crs_list[0]} not found (or not read correctly)")
                raise ObjectNotFoundNotError(get_obj_uri(crs_list[0]))
            if crs is not None:
                return crs
        else:
            logging.debug(f"No CRS found for {get_obj_title(context_obj)} with type {type(context_obj).__name__}")

        if context_obj != root_obj:
            upper_path = path_parent_attribute(path_in_root)
            # upper_path = path_in_root[: path_in_root.rindex(".")]
            if len(upper_path) > 0:
                return get_crs_obj(
                    context_obj=get_object_attribute(root_obj, upper_path),
                    path_in_root=upper_path,
                    root_obj=root_obj,
                    workspace=workspace,
                )

    return None


def linear_interpolation(md_target, md_start, md_end, p_start, p_end):
    """
    Calcule la position 3D par interpolation linéaire simple.
    Utilisé quand Continuity = 0 ou quand les TangentVectors sont absents.
    """
    # Calcul du ratio de progression (0 à 1)
    h = md_end - md_start
    if h == 0:
        return p_start

    t = (md_target - md_start) / h

    # Formule : P = P_start + t * (P_end - p_start)
    p_target = p_start + t * (p_end - p_start)

    return p_target


def hermite_interpolation(md_target, md_start, md_end, p_start, p_end, v_start, v_end):
    """
    Calcule la position 3D d'un point sur une trajectoire de puits via une Spline d'Hermite.

    Cette fonction est particulièrement adaptée aux objets RESQML de type
    'ParametricLineGeometry' avec une continuité C1.

    Args:
        md_target (float): La profondeur mesurée (Measured Depth) cible à interpoler.
        md_start (float): MD du point de contrôle précédent (Knot i).
        md_end (float): MD du point de contrôle suivant (Knot i+1).
        p_start (np.array): Coordonnées [X, Y, Z] au point md_start.
        p_end (np.array): Coordonnées [X, Y, Z] au point md_end.
        v_start (np.array): Vecteur tangente unitaire [dx, dy, dz] au point md_start.
        v_end (np.array): Vecteur tangente unitaire [dx, dy, dz] au point md_end.

    Returns:
        np.array: Un tableau numpy [X, Y, Z] représentant la position interpolée.

    Raises:
        ValueError: Si md_start et md_end sont identiques (division par zéro).
        AssertionError: Si md_target n'est pas compris dans l'intervalle [md_start, md_end].
    """

    # 1. Vérification de l'intervalle
    if not (md_start <= md_target <= md_end):
        # Note : Dans certains cas de forage réel, on peut extrapoler,
        # mais pour un WellboreFrame, on reste normalement dans les clous.
        raise AssertionError("Le MD cible doit être compris entre md_start et md_end.")

    # Distance entre les deux points de contrôle
    h = md_end - md_start
    if h == 0:
        raise ValueError("md_start et md_end ne peuvent pas être identiques.")

    # 2. Normalisation du paramètre t (0 <= t <= 1)
    t = (md_target - md_start) / h
    t2 = t * t
    t3 = t2 * t

    # 3. Mise à l'échelle des vecteurs tangentes (scaling par la distance)
    # En RESQML, les TangentVectors sont souvent unitaires ou normalisés.
    # Pour l'interpolation cubique, ils doivent représenter la dérivée par rapport à t.
    T_start = v_start * h
    T_end = v_end * h

    # 4. Calcul des polynômes de base d'Hermite
    h00 = 2 * t3 - 3 * t2 + 1  # Coefficient pour p_start
    h10 = t3 - 2 * t2 + t  # Coefficient pour T_start
    h01 = -2 * t3 + 3 * t2  # Coefficient pour p_end
    h11 = t3 - t2  # Coefficient pour T_end

    # 5. Combinaison linéaire pour obtenir la position P(t)
    p_target = (h00 * p_start) + (h10 * T_start) + (h01 * p_end) + (h11 * T_end)

    return p_target


# ---------------------------------------------------------------------------
# Point3dParametricArray / ParametricLineArray evaluation
# ---------------------------------------------------------------------------
#
# RESQML line_kind_indices reference:
#   0  → vertical        (control_points store only X,Y; Z = P-value)
#   1  → linear spline   (piecewise-linear)
#   2  → natural cubic spline
#   3  → tangential cubic spline (Hermite, requires tangent_vectors)
#   4  → Z-linear cubic spline   (X,Y natural cubic; Z linear)
#   5  → minimum-curvature spline (requires tangent_vectors)
#  -1  → null / no line
# ---------------------------------------------------------------------------

_PARAMETRIC_KIND_VERTICAL = 0
_PARAMETRIC_KIND_LINEAR = 1
_PARAMETRIC_KIND_NATURAL_CUBIC = 2
_PARAMETRIC_KIND_HERMITE = 3
_PARAMETRIC_KIND_ZLINEAR_CUBIC = 4
_PARAMETRIC_KIND_MIN_CURVATURE = 5
_PARAMETRIC_KIND_NULL = -1


def _interp1d_vectorized(
    ctrl_params: np.ndarray,  # (K,)
    ctrl_pts: np.ndarray,  # (K, d)
    query: np.ndarray,  # (Q,)
) -> np.ndarray:  # (Q, d)
    """Vectorised piecewise-linear interpolation of a 1-D parametric curve."""
    result = np.empty((len(query), ctrl_pts.shape[1]), dtype=np.float64)
    for dim in range(ctrl_pts.shape[1]):
        result[:, dim] = np.interp(query, ctrl_params, ctrl_pts[:, dim])
    return result


def _natural_cubic_spline_eval(
    ctrl_params: np.ndarray,  # (K,)
    ctrl_pts: np.ndarray,  # (K, d)
    query: np.ndarray,  # (Q,)
) -> np.ndarray:  # (Q, d)
    """
    Evaluate a natural cubic spline (second derivatives = 0 at endpoints) via
    ``scipy.interpolate.CubicSpline``.

    Raises ``ImportError`` with an actionable message when scipy is absent —
    install with ``pip install energyml-utils[geometry]`` or
    ``pip install scipy``.
    """
    try:
        from scipy.interpolate import CubicSpline  # lazy import to keep scipy optional
    except ImportError as exc:
        raise ImportError(
            "scipy is required for natural-cubic (kind=2) and Z-linear-cubic (kind=4) "
            "pillar interpolation in IjkGridRepresentation. "
            "Install it with: pip install scipy   or   pip install energyml-utils[geometry]"
        ) from exc

    cs = CubicSpline(ctrl_params, ctrl_pts, bc_type="natural")
    return cs(query)  # shape (Q, d)


def _minimum_curvature_eval(
    ctrl_params: np.ndarray,  # (K,)  P-values (e.g. depth) at knots
    ctrl_pts: np.ndarray,  # (K, 3)  XYZ at knots
    tangents: np.ndarray,  # (K, 3)  unit tangent vectors at knots
    query: np.ndarray,  # (Q,)  query P-values
) -> np.ndarray:  # (Q, 3)
    """
    Minimum-curvature interpolation (RESQML line kind 5).

    Between each pair of knots k and k+1 the trajectory segment is computed
    using the standard directional-drilling minimum-curvature formula:

        DL    = arccos(T_k · T_{k+1})
        RF    = 2/DL * tan(DL/2)   (1.0 when DL==0)
        ΔP    = (ds/2) * (T_k + T_{k+1}) * RF

    Query points within the interval are obtained by re-applying the formula
    with partial-interval tangent blending so that the interpolated position
    depends continuously on the query P-value.
    """
    K = len(ctrl_params)
    Q = len(query)
    result = np.empty((Q, 3), dtype=np.float64)

    # Clamp queries to the valid parametric range.
    q_clamped = np.clip(query, ctrl_params[0], ctrl_params[-1])

    for q_idx in range(Q):
        q = q_clamped[q_idx]
        # Find the enclosing knot interval [k, k+1].
        k = np.searchsorted(ctrl_params, q, side="right") - 1
        k = int(np.clip(k, 0, K - 2))

        p0, p1 = ctrl_params[k], ctrl_params[k + 1]
        ds_full = p1 - p0
        if ds_full == 0.0:
            result[q_idx] = ctrl_pts[k]
            continue

        t = (q - p0) / ds_full  # fractional progress in [0, 1]
        ds = q - p0  # partial arc length from knot k to query

        T0 = tangents[k]
        T1 = tangents[k + 1]
        # Blend tangent at query position using linear interpolation of angle.
        T_q = (1.0 - t) * T0 + t * T1
        nrm = np.linalg.norm(T_q)
        T_q = T_q / nrm if nrm > 1e-12 else T0

        # Minimum-curvature ratio factor for the partial segment T0→T_q.
        cos_dl = np.clip(np.dot(T0, T_q), -1.0, 1.0)
        dl = np.arccos(cos_dl)
        rf = (2.0 / dl) * np.tan(dl / 2.0) if dl > 1e-9 else 1.0

        result[q_idx] = ctrl_pts[k] + (ds / 2.0) * (T0 + T_q) * rf

    return result


def _evaluate_one_pillar(
    kind: int,
    ctrl_params: Optional[np.ndarray],  # (K,) — may be None for kind=0
    ctrl_pts: np.ndarray,  # (K, d) — d=2 for kind=0, d=3 otherwise
    tangents: Optional[np.ndarray],  # (K, 3) — only for kinds 3, 5
    query_params: np.ndarray,  # (Q,) query P-values for this pillar
) -> np.ndarray:  # (Q, 3)
    """
    Evaluate a single parametric pillar at *query_params*, returning `(Q, 3)` XYZ.

    Clamps out-of-range queries to the nearest knot; returns NaN columns for
    null lines (kind==-1).
    """
    Q = len(query_params)

    if kind == _PARAMETRIC_KIND_NULL:
        return np.full((Q, 3), np.nan, dtype=np.float64)

    if kind == _PARAMETRIC_KIND_VERTICAL:
        # Only X, Y stored; Z coordinate = P-value.
        # ctrl_pts shape (K, 2) or (K, 3) — take only first two coords regardless.
        x = float(ctrl_pts[0, 0])
        y = float(ctrl_pts[0, 1])
        out = np.empty((Q, 3), dtype=np.float64)
        out[:, 0] = x
        out[:, 1] = y
        out[:, 2] = query_params
        return out

    if kind == _PARAMETRIC_KIND_LINEAR:
        return _interp1d_vectorized(ctrl_params, ctrl_pts[:, :3], query_params)

    if kind == _PARAMETRIC_KIND_NATURAL_CUBIC:
        return _natural_cubic_spline_eval(ctrl_params, ctrl_pts[:, :3], query_params)

    if kind == _PARAMETRIC_KIND_HERMITE:
        if tangents is None:
            logging.warning(
                "Pillar kind=3 (tangential cubic Hermite) requested but no tangent_vectors "
                "found — falling back to linear interpolation."
            )
            return _interp1d_vectorized(ctrl_params, ctrl_pts[:, :3], query_params)
        # Evaluate piecewise Hermite per query point.
        result = np.empty((Q, 3), dtype=np.float64)
        K = len(ctrl_params)
        q_clamped = np.clip(query_params, ctrl_params[0], ctrl_params[-1])
        for q_idx in range(Q):
            q = q_clamped[q_idx]
            k = int(np.clip(np.searchsorted(ctrl_params, q, side="right") - 1, 0, K - 2))
            result[q_idx] = hermite_interpolation(
                md_target=q,
                md_start=ctrl_params[k],
                md_end=ctrl_params[k + 1],
                p_start=ctrl_pts[k, :3],
                p_end=ctrl_pts[k + 1, :3],
                v_start=tangents[k],
                v_end=tangents[k + 1],
            )
        return result

    if kind == _PARAMETRIC_KIND_ZLINEAR_CUBIC:
        # X, Y: natural cubic spline; Z: linear.
        xy_cubic = _natural_cubic_spline_eval(ctrl_params, ctrl_pts[:, :2], query_params)
        z_linear = np.interp(query_params, ctrl_params, ctrl_pts[:, 2])
        out = np.empty((Q, 3), dtype=np.float64)
        out[:, :2] = xy_cubic
        out[:, 2] = z_linear
        return out

    if kind == _PARAMETRIC_KIND_MIN_CURVATURE:
        if tangents is None:
            logging.warning(
                "Pillar kind=5 (minimum-curvature) requested but no tangent_vectors "
                "found — falling back to linear interpolation."
            )
            return _interp1d_vectorized(ctrl_params, ctrl_pts[:, :3], query_params)
        return _minimum_curvature_eval(ctrl_params, ctrl_pts[:, :3], tangents, query_params)

    # Unknown kind: warn and fall back to linear.
    logging.warning(f"Unknown parametric line kind={kind}; falling back to linear interpolation.")
    return _interp1d_vectorized(ctrl_params, ctrl_pts[:, :3], query_params)


def resolve_parametric_line_array(
    parametric_lines_obj: Any,
    root_obj: Any,
    workspace: Optional[EnergymlStorageInterface],
    n_pillars: int,
) -> Any:
    """
    Resolve `parametric_lines` to a concrete `ParametricLineArray`-like object.

    Two cases:
    * **Direct** ``ParametricLineArray``: returned as-is (most common).
    * **ParametricLineFromRepresentationLatticeArray** (v2.0.1 only): resolves
      the supporting representation, extracts its ``ParametricLineArray`` and
      selects the relevant pillar columns using the embedded
      ``IntegerLatticeArray`` index selection.  Returns a ``SimpleNamespace``
      that duck-types ``ParametricLineArray`` so that
      :func:`evaluate_parametric_line_array` can consume it unchanged.

    :param parametric_lines_obj: Either a ``ParametricLineArray`` or a
        ``ParametricLineFromRepresentationLatticeArray``.
    :param root_obj: Root RESQML object (for array reading context).
    :param workspace: Workspace for resolving external references.
    :param n_pillars: Expected number of pillars in the calling grid.
    :raises ValueError: If the supporting representation or its parametric
        lines cannot be resolved.
    """
    from types import SimpleNamespace

    type_name = type(parametric_lines_obj).__name__
    if "FromRepresentationLattice" not in type_name:
        # Direct ParametricLineArray — nothing to resolve.
        return parametric_lines_obj

    # ParametricLineFromRepresentationLatticeArray path (RESQML v2.0.1).
    supporting_rep_dor = getattr(parametric_lines_obj, "supporting_representation", None)
    if supporting_rep_dor is None:
        raise ValueError("ParametricLineFromRepresentationLatticeArray has no supporting_representation reference.")

    if workspace is None:
        raise ValueError("A workspace is required to resolve ParametricLineFromRepresentationLatticeArray.")

    sup_uri = get_obj_uri(supporting_rep_dor)
    sup_obj = workspace.get_object(sup_uri)
    if sup_obj is None:
        raise ValueError(f"Supporting representation {sup_uri} not found in workspace.")

    # Locate the ParametricLineArray inside the supporting representation.
    pla_results = search_attribute_matching_name_with_path(sup_obj, "ParametricLines")
    if not pla_results:
        pla_results = search_attribute_matching_name_with_path(sup_obj, "parametric_lines")
    if not pla_results:
        raise ValueError(f"Cannot find a ParametricLineArray in supporting representation {sup_uri}.")
    _, sup_pla = pla_results[0]

    # Read the pillar index selection (IntegerLatticeArray).
    idx_obj = getattr(parametric_lines_obj, "line_indices_on_supporting_representation", None)
    if idx_obj is None:
        # No index selection → identity mapping; return parent PLA directly.
        return sup_pla

    from energyml.utils.data.helper import read_array as _read_array_helper  # for local use

    raw_indices = _read_array_helper(energyml_array=idx_obj, root_obj=root_obj, workspace=workspace)
    if not isinstance(raw_indices, np.ndarray):
        raw_indices = np.array(raw_indices, dtype=np.int64)
    raw_indices = raw_indices.flatten().astype(np.int64)

    # Build a SimpleNamespace that selects the relevant pillar columns.
    # We wrap each sub-array lazily using a column-selection proxy so that
    # evaluate_parametric_line_array can call read_array on the underlying
    # arrays and then slice columns.
    return SimpleNamespace(
        _sup_pla=sup_pla,
        _indices=raw_indices,
        knot_count=getattr(sup_pla, "knot_count", None),
        control_points=getattr(sup_pla, "control_points", None),
        control_point_parameters=getattr(sup_pla, "control_point_parameters", None),
        line_kind_indices=getattr(sup_pla, "line_kind_indices", None),
        tangent_vectors=getattr(sup_pla, "tangent_vectors", None),
        parametric_line_intersections=getattr(sup_pla, "parametric_line_intersections", None),
        _column_indices=raw_indices,  # used by evaluate_parametric_line_array to slice columns
    )


def evaluate_parametric_line_array(
    pla: Any,
    root_obj: Any,
    workspace: Optional[EnergymlStorageInterface],
    query_parameters: np.ndarray,  # shape (NKL, n_pillars)
    ni: int,
    nj: int,
) -> np.ndarray:  # shape (NKL, n_pillars, 3) float64
    """
    Evaluate a ``ParametricLineArray`` at the given query P-values and return
    3-D Cartesian coordinates for every grid node.

    This is the core of the ``Point3dParametricArray`` reader for
    :func:`read_numpy_ijk_grid_representation`.

    :param pla: A ``ParametricLineArray`` instance (or duck-typed
        ``SimpleNamespace`` from :func:`resolve_parametric_line_array`).
    :param root_obj: Root RESQML object — passed to :func:`read_array` for
        external-dataset resolution.
    :param workspace: Workspace used for HDF5 reads.
    :param query_parameters: ``(NKL, n_pillars)`` array of parametric
        P-values (usually depth) at which to evaluate each pillar.
    :param ni: Grid cell count in the I direction (``NI``).
    :param nj: Grid cell count in the J direction (``NJ``).
    :return: ``(NKL, n_pillars, 3)`` float64 array of evaluated XYZ positions.
    :raises ValueError: If mandatory arrays (control_points, line_kind_indices)
        cannot be read.
    :raises ImportError: Propagated from :func:`_natural_cubic_spline_eval`
        when scipy is missing and kind-2 / kind-4 pillars are present.
    """
    nkl, n_pillars = query_parameters.shape

    knot_count: int = getattr(pla, "knot_count", None)

    # --- 1. Read control_points ---
    cp_obj = getattr(pla, "control_points", None)
    if cp_obj is None:
        raise ValueError("ParametricLineArray.control_points is required but absent.")
    raw_cp = read_array(energyml_array=cp_obj, root_obj=root_obj, workspace=workspace)
    if not isinstance(raw_cp, np.ndarray):
        raw_cp = np.array(raw_cp, dtype=np.float64)
    raw_cp = raw_cp.astype(np.float64)

    # Determine coordinate dimension (2 for vertical-only, 3 otherwise).
    # The flat array has K*P*d values; we disambiguate using knot_count and n_pillars.
    n_pillars_base = (ni + 1) * (nj + 1)
    coord_dim = raw_cp.size // (knot_count * n_pillars) if knot_count and knot_count * n_pillars > 0 else 3
    if coord_dim not in (2, 3):
        # Fallback: try 4-D layout (knot, NJ+1, NI+1, d)
        if raw_cp.size == knot_count * (nj + 1) * (ni + 1) * 3:
            raw_cp = raw_cp.reshape(knot_count, nj + 1, ni + 1, 3)
            raw_cp = raw_cp.reshape(knot_count, n_pillars_base, 3)
            coord_dim = 3
        else:
            coord_dim = 3  # safe default
    ctrl_pts = raw_cp.reshape(knot_count, n_pillars, coord_dim)

    # Optional column selection for ParametricLineFromRepresentationLatticeArray.
    col_indices: Optional[np.ndarray] = getattr(pla, "_column_indices", None)
    if col_indices is not None:
        ctrl_pts = ctrl_pts[:, col_indices, :]

    # --- 2. Read control_point_parameters (may be None for all-vertical) ---
    cpp_obj = getattr(pla, "control_point_parameters", None)
    ctrl_params: Optional[np.ndarray] = None
    if cpp_obj is not None:
        raw_cpp = read_array(energyml_array=cpp_obj, root_obj=root_obj, workspace=workspace)
        if not isinstance(raw_cpp, np.ndarray):
            raw_cpp = np.array(raw_cpp, dtype=np.float64)
        raw_cpp = raw_cpp.astype(np.float64).flatten()
        # Layout: (K * P,) ordered knot-major → reshape to (K, P).
        if raw_cpp.size == knot_count * n_pillars:
            ctrl_params = raw_cpp.reshape(knot_count, n_pillars)
        elif raw_cpp.size == knot_count:
            # Same parameters for all pillars (broadcast).
            ctrl_params = np.tile(raw_cpp[:, np.newaxis], (1, n_pillars))
        else:
            logging.warning(
                f"control_point_parameters size {raw_cpp.size} does not match "
                f"knot_count={knot_count} × n_pillars={n_pillars}. "
                "Attempting best-effort reshape."
            )
            ctrl_params = raw_cpp[: knot_count * n_pillars].reshape(knot_count, n_pillars)
        if col_indices is not None:
            ctrl_params = ctrl_params[:, col_indices]

    # --- 3. Read line_kind_indices ---
    lki_obj = getattr(pla, "line_kind_indices", None)
    if lki_obj is None:
        raise ValueError("ParametricLineArray.line_kind_indices is required but absent.")
    raw_lki = read_array(energyml_array=lki_obj, root_obj=root_obj, workspace=workspace)
    if not isinstance(raw_lki, np.ndarray):
        raw_lki = np.array(raw_lki, dtype=np.int32)
    kinds: np.ndarray = raw_lki.astype(np.int32).flatten()
    if col_indices is not None:
        kinds = kinds[col_indices]
    if len(kinds) != n_pillars:
        logging.warning(
            f"line_kind_indices length {len(kinds)} ≠ n_pillars {n_pillars}. "
            "Broadcasting first kind value to all pillars."
        )
        kinds = np.full(n_pillars, kinds[0] if len(kinds) > 0 else _PARAMETRIC_KIND_LINEAR, dtype=np.int32)

    # --- 4. Read tangent_vectors (optional, only for kinds 3 and 5) ---
    tv_obj = getattr(pla, "tangent_vectors", None)
    tangent_vecs: Optional[np.ndarray] = None
    unique_kinds = np.unique(kinds)
    needs_tangents = any(k in unique_kinds for k in (_PARAMETRIC_KIND_HERMITE, _PARAMETRIC_KIND_MIN_CURVATURE))
    if tv_obj is not None and needs_tangents:
        raw_tv = read_array(energyml_array=tv_obj, root_obj=root_obj, workspace=workspace)
        if not isinstance(raw_tv, np.ndarray):
            raw_tv = np.array(raw_tv, dtype=np.float64)
        tangent_vecs = raw_tv.astype(np.float64).reshape(knot_count, n_pillars, 3)
        if col_indices is not None:
            tangent_vecs = tangent_vecs[:, col_indices, :]

    # --- 5. Evaluate each pillar ---
    result = np.empty((nkl, n_pillars, 3), dtype=np.float64)

    for p_idx in range(n_pillars):
        kind = int(kinds[p_idx])
        q_p = query_parameters[:, p_idx]  # (NKL,) P-values for this pillar
        cp_p = ctrl_pts[:, p_idx, :]  # (K, d)

        # ctrl_params_p: (K,) — derived from global or pillar-specific params.
        # For kind=0, ctrl_params is None (vertical) and we pass None.
        if ctrl_params is not None:
            cpp_p = ctrl_params[:, p_idx]  # (K,)
        else:
            cpp_p = None

        tv_p = tangent_vecs[:, p_idx, :] if tangent_vecs is not None else None  # (K, 3) or None

        result[:, p_idx, :] = _evaluate_one_pillar(
            kind=kind,
            ctrl_params=cpp_p,
            ctrl_pts=cp_p,
            tangents=tv_p,
            query_params=q_p,
        )

    return result


def get_wellbore_points(
    mds: Optional[np.ndarray],
    traj_mds: Optional[np.ndarray],
    traj_points: Optional[np.ndarray],
    traj_tangents: Optional[np.ndarray],
    step_meters: float = 5.0,
) -> np.ndarray:
    """
    mds : MDs du WellboreFrame
    traj_mds : MDs de la trajectoire (ControlPointParameters)
    traj_points : Points XYZ de la trajectoire
    traj_tangents : Tangentes XYZ (Optionnel)
    step_meters : Distance entre chaque point de la trajectoire lisse (Optionnel)
    """
    if mds is None or len(mds) == 0:
        if traj_mds is None or traj_points is None or traj_tangents is None:
            raise ValueError(
                "To generate a smooth trajectory, traj_mds, traj_points and traj_tangents must be provided."
            )
        return generate_smooth_trajectory(
            traj_mds=traj_mds, traj_points=traj_points, traj_tangents=traj_tangents, step_meters=step_meters
        )

    results = []

    for m in mds:
        # 1. Trouver l'intervalle
        idx = np.searchsorted(traj_mds, m) - 1

        # Gestion des bords
        if idx < 0:
            results.append(traj_points[0])
            continue
        if idx >= len(traj_mds) - 1:
            results.append(traj_points[-1])
            continue

        # 2. Extraire les bornes
        p_s, p_e = traj_points[idx], traj_points[idx + 1]
        m_s, m_e = traj_mds[idx], traj_mds[idx + 1]

        # 3. Choisir la méthode
        if traj_tangents is not None:
            # Cas ParametricLineGeometry C1+
            v_s, v_e = traj_tangents[idx], traj_tangents[idx + 1]
            p_3d = hermite_interpolation(m, m_s, m_e, p_s, p_e, v_s, v_e)
        else:
            # Cas Linear ou PointGeometry
            p_3d = linear_interpolation(m, m_s, m_e, p_s, p_e)

        results.append(p_3d)

    return np.array(results)


def generate_smooth_trajectory(
    traj_mds: np.ndarray, traj_points: np.ndarray, traj_tangents: np.ndarray, step_meters: float = 5.0
) -> np.ndarray:
    """
    Generates a high-resolution polyline for the trajectory by sampling
    it at a regular interval.

    Args:
        traj_mds: MDs of control points from HDF5.
        traj_points: Control points (N, 3) from HDF5.
        traj_tangents: Tangent vectors (N, 3) from HDF5.
        step_meters: Desired distance between each point of the final polyline.

    Returns:
        A (M, 3) numpy array representing the smooth 3D polyline.
    """
    # 1. Create a regular MD sampling from min to max MD
    md_min, md_max = traj_mds[0], traj_mds[-1]
    # We create a new set of MDs every 'step_meters'
    sampled_mds = np.arange(md_min, md_max, step_meters)

    # Ensure the last point of the trajectory is included
    if sampled_mds[-1] < md_max:
        sampled_mds = np.append(sampled_mds, md_max)

    # 2. Reuse our interpolation logic
    smooth_points = []
    for m in sampled_mds:
        # Find the interval in the original control points
        idx = np.searchsorted(traj_mds, m) - 1
        idx = max(0, min(idx, len(traj_mds) - 2))

        p_3d = hermite_interpolation(
            m,
            traj_mds[idx],
            traj_mds[idx + 1],
            traj_points[idx],
            traj_points[idx + 1],
            traj_tangents[idx],
            traj_tangents[idx + 1],
        )
        smooth_points.append(p_3d)

    return np.array(smooth_points)


def generate_vertical_well_points(
    wellbore_mds: np.ndarray, head_x: float, head_y: float, head_z: float, z_increasing_downward: bool = False
) -> np.ndarray:
    """
    Generates local 3D coordinates for a perfectly vertical wellbore.

    Args:
        wellbore_mds: (N,) array of Measured Depths from the WellboreFrame.
        head_x: The X coordinate of the MdDatum (well head) in Local CRS.
        head_y: The Y coordinate of the MdDatum (well head) in Local CRS.
        head_z: The Z coordinate of the MdDatum (well head) in Local CRS.

    Returns:
        (N, 3) numpy array of points [X, Y, Z] in Local CRS.
    """
    num_points = len(wellbore_mds)
    # Initialize the array with (N, 3)
    local_points = np.zeros((num_points, 3))

    # In a vertical well, X and Y are constant and equal to the head position
    local_points[:, 0] = head_x
    local_points[:, 1] = head_y

    # The MD (Measured Depth) represents the distance traveled from MD 0.
    # In a vertical well, Z_point = Z_datum + (MD_point - MD_datum_at_0)
    # Most of the time, MD at head is 0.
    # If wellbore_mds start at 0, Z starts at head_z.
    # if z_increasing_downward is False, we add the MD to head_z, otherwise we subtract it.
    md_start = wellbore_mds[0]
    if z_increasing_downward:
        local_points[:, 2] = head_z - (wellbore_mds - md_start)
    else:
        local_points[:, 2] = head_z + (wellbore_mds - md_start)

    return local_points


def read_parametric_geometry(
    geometry: Any, workspace: Optional[EnergymlStorageInterface] = None
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """Read a ParametricLineGeometry and return the controle point parameters, control points, and tangents."""
    if geometry is None:
        raise ValueError("Geometry object is None")

    knot_count = getattr(geometry, "knot_count", None)

    traj_mds = read_array(
        energyml_array=getattr(geometry, "control_point_parameters"),
        root_obj=geometry,
        workspace=workspace,
    )
    if not isinstance(traj_mds, np.ndarray):
        traj_mds = np.array(traj_mds)

    traj_points = read_array(
        energyml_array=getattr(geometry, "control_points"),
        root_obj=geometry,
        workspace=workspace,
    )
    if not isinstance(traj_points, np.ndarray):
        traj_points = np.array(traj_points)
    traj_points = traj_points.reshape(-1, 3)

    traj_tangents = None
    try:
        traj_tangents = read_array(
            energyml_array=getattr(geometry, "tangent_vectors"),
            root_obj=geometry,
            workspace=workspace,
        )
    except Exception as e:
        logging.debug(f"No tangent vectors found for {geometry}, fallback to linear interpolation: {e}")

    if traj_tangents is not None:
        if not isinstance(traj_tangents, np.ndarray):
            traj_tangents = np.array(traj_tangents)
        traj_tangents = traj_tangents.reshape(-1, 3)

    # verif with knot_count if exists
    if knot_count is not None:
        if (
            len(traj_mds) != knot_count
            or len(traj_points) != knot_count
            or (traj_tangents is not None and len(traj_tangents) != knot_count)
        ):
            logging.warning(
                f"Mismatch between knot_count ({knot_count}) and actual control points count (mds: {len(traj_mds)}, points: {len(traj_points)}, tangents: {len(traj_tangents) if traj_tangents is not None else 'N/A'})"
            )

    return traj_mds, traj_points, traj_tangents


#     ___
#    /   |  ______________ ___  _______
#   / /| | / ___/ ___/ __ `/ / / / ___/
#  / ___ |/ /  / /  / /_/ / /_/ (__  )
# /_/  |_/_/  /_/   \__,_/\__, /____/
#                        /____/


def _array_name_mapping(array_type_name: str) -> str:
    """
    Transform the type name to match existing reader function
    :param array_type_name:
    :return:
    """
    array_type_name = array_type_name.replace("3D", "3d").replace("2D", "2d")
    if array_type_name.endswith("ConstantArray"):
        return "ConstantArray"
    elif "External" in array_type_name or "Hdf5" in array_type_name:
        return "ExternalArray"
    elif "Xml" in array_type_name:
        return "XmlArray"
    elif "Jagged" in array_type_name:
        return "JaggedArray"
    elif "Lattice" in array_type_name:
        if "Integer" in array_type_name or "Double" in array_type_name or "Floating" in array_type_name:
            return "int_double_lattice_array"
    return array_type_name


def get_supported_array() -> List[str]:
    """
    Return a list of the supported arrays for the use of :py:func:`energyml.utils.data.helper.read_array` function.
    :return:
    """
    return [x for x in _ARRAY_NAMES_ if get_array_reader_function(_array_name_mapping(x)) is not None]


def get_not_supported_array():
    """
    Return a list of the NOT supported arrays for the use of :py:func:`energyml.utils.data.helper.read_array` function.
    :return:
    """
    return [x for x in _ARRAY_NAMES_ if get_array_reader_function(_array_name_mapping(x)) is None]


def _extract_external_data_array_part_params(
    obj: Any,
) -> tuple[Optional[List[int]], Optional[List[int]], Optional[str]]:
    """
    Extract array parameters (Count, StartIndex, URI) from an object.
    Uses regex to match various attribute name formats (snake_case, PascalCase).

    Args:
        obj: The object to extract parameters from (ExternalDataArrayPart or parent object)

    Returns:
        Tuple of (start_indices, counts, external_uri)
    """
    start_indices = None
    counts = None
    external_uri = None

    # Extract StartIndex using regex (matches: StartIndex, start_index, startIndex)
    start_attr = get_object_attribute_rgx(obj, "[Ss]tart[_]?[Ii]ndex")
    if start_attr is not None:
        if isinstance(start_attr, list):
            start_indices = start_attr
        elif isinstance(start_attr, (int, float)):
            start_indices = [int(start_attr)]
        elif hasattr(start_attr, "value"):
            if isinstance(start_attr.value, list):
                start_indices = start_attr.value
            elif isinstance(start_attr.value, (int, float)):
                start_indices = [int(start_attr.value)]

    # Extract Count using regex (matches: Count, count, NodeCount, node_count)
    count_attr = get_object_attribute_rgx(obj, "([Nn]ode[_]?)?[Cc]ount")
    if count_attr is not None:
        if isinstance(count_attr, list):
            counts = count_attr
        elif isinstance(count_attr, (int, float)):
            counts = [int(count_attr)]
        elif hasattr(count_attr, "value"):
            if isinstance(count_attr.value, list):
                counts = count_attr.value
            elif isinstance(count_attr.value, (int, float)):
                counts = [int(count_attr.value)]

    # Extract URI using regex (matches: URI, uri)
    uri_attr = get_object_attribute_rgx(obj, "[Uu][Rr][Ii]")
    if uri_attr is not None:
        if isinstance(uri_attr, str):
            external_uri = uri_attr
        elif hasattr(uri_attr, "value") and isinstance(uri_attr.value, str):
            external_uri = uri_attr.value

    return start_indices, counts, external_uri


def read_external_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> Optional[Union[List[Any], np.ndarray]]:
    """
    Read an external array (BooleanExternalArray, BooleanHdf5Array, DoubleHdf5Array, IntegerHdf5Array, StringExternalArray ...)
    Automatically handles RESQML v2.2 (multiple ExternalDataArrayPart with individual parameters)
    and RESQML v2.0.1 (count from parent object).

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    array = None
    if workspace is not None:
        crs = None
        try:
            get_crs_obj(
                context_obj=root_obj,
                root_obj=root_obj,
                path_in_root=path_in_root,
                workspace=workspace,
            )
        except ObjectNotFoundNotError as e:
            logging.debug(f"CRS not found for {get_obj_title(root_obj)}: {e}")

        # Search for ExternalDataArrayPart type objects (RESQML v2.2)
        external_parts = search_attribute_matching_type(
            energyml_array, "ExternalDataArrayPart", return_self=False, deep_search=True
        )

        if external_parts and len(external_parts) > 0:
            # RESQML v2.2: Loop over each ExternalDataArrayPart
            # Each part has its own start/count/uri and path_in_external
            for ext_part in external_parts:
                start_indices, counts, external_uri = _extract_external_data_array_part_params(ext_part)
                pief_list = get_path_in_external_with_path(obj=ext_part)
                # logging.debug(f"Pief : {pief_list}")
                for pief_path_in_obj, pief in pief_list:
                    arr = workspace.read_array(
                        proxy=crs or root_obj,
                        path_in_external=pief,
                        start_indices=start_indices,
                        counts=counts,
                        external_uri=external_uri,
                    )
                    if arr is not None:
                        array = arr if array is None else np.concatenate((array, arr))
                    # logging.debug(f"\t ExternalDataArrayPart read successfully. arr : {arr} : array : {array}")
        else:
            # RESQML v2.0.1: Extract count from parent object, no StartIndex or URI
            counts = None
            if path_in_root and root_obj:
                last_attr = path_last_attribute(path_in_root)
                if last_attr:
                    parent_path = path_in_root[: path_in_root.rfind("." + last_attr)]
                    if parent_path:
                        try:
                            parent_obj = get_object_attribute_advanced(root_obj, parent_path)
                            if parent_obj:
                                # Extract count from parent using simplified function
                                _, counts, _ = _extract_external_data_array_part_params(parent_obj)
                        except Exception as e:
                            logging.debug(f"Failed to extract count from parent: {e}")

            # Read array using path_in_external from the array object itself
            pief_list = get_path_in_external_with_path(obj=energyml_array)
            for pief_path_in_obj, pief in pief_list:
                arr = workspace.read_array(
                    proxy=crs or root_obj,
                    path_in_external=pief,
                    start_indices=None,
                    counts=counts,
                    external_uri=None,
                )
                if arr is not None:
                    array = arr if array is None else np.concatenate((array, arr))

    else:
        array = read_external_dataset_array(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
        )

    if sub_indices is not None and len(sub_indices) > 0:
        if isinstance(array, np.ndarray):
            array = array[sub_indices]
        elif isinstance(array, list):
            # Fallback for non-numpy arrays
            array = [array[idx] for idx in sub_indices]

    # logging.debug(f"External array read successfully. => {array}")
    return array


def get_array_reader_function(array_type_name: str) -> Optional[Callable]:
    """
    Returns the name of the potential appropriate function to read an object with type is named :param array_type_name
    :param array_type_name: the initial type name
    :return:
    """
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if name == f"read_{snake_case(array_type_name)}":
            return obj
    return None


def read_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> Union[List[Any], np.ndarray]:
    """
    Read an array and return a list. The array is read depending on its type. see. :py:func:`energyml.utils.data.helper.get_supported_array`
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices: for SubRepresentation
    :return:
    """
    if isinstance(energyml_array, np.ndarray):
        # if isinstance(energyml_array, list):
        return energyml_array
    elif isinstance(energyml_array, list):
        # logging.debug("Warning: the array is a list, not a numpy array, be careful with the performance !")
        # logging.debug(energyml_array)
        if len(energyml_array) > 0 and is_primitive(energyml_array[0]):
            return energyml_array
        else:
            return [
                read_array(
                    energyml_array=elem,
                    root_obj=root_obj,
                    path_in_root=path_in_root,
                    workspace=workspace,
                    sub_indices=sub_indices,
                )
                for elem in energyml_array
                if elem is not None
            ]
    array_type_name = _array_name_mapping(type(energyml_array).__name__)

    reader_func = get_array_reader_function(array_type_name)
    if reader_func is not None:
        return reader_func(
            energyml_array=energyml_array,
            root_obj=root_obj,
            path_in_root=path_in_root,
            workspace=workspace,
            sub_indices=sub_indices,
        )
    else:
        logging.error(f"Type {array_type_name} is not supported: function read_{snake_case(array_type_name)} not found")
        raise Exception(
            f"Type {array_type_name} is not supported\n\t{energyml_array}: \n\tfunction read_{snake_case(array_type_name)} not found"
        )


def read_constant_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> Union[np.ndarray, List[Any]]:
    """
    Read a constant array (BooleanConstantArray, DoubleConstantArray,
    FloatingPointConstantArray, IntegerConstantArray …).

    For numeric (int / float / bool) values a ``numpy.ndarray`` is returned
    via :func:`numpy.full`, avoiding a Python-list allocation.  String values
    fall back to a plain list because numpy object arrays add no benefit.

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    value = get_object_attribute_no_verif(energyml_array, "value")
    count = (
        len(sub_indices)
        if sub_indices is not None and len(sub_indices) > 0
        else get_object_attribute_no_verif(energyml_array, "count")
    )

    if isinstance(value, (int, float, bool, np.integer, np.floating)):
        return np.full(int(count), value)
    # Non-numeric (e.g. string) — keep as Python list.
    return [value] * int(count)


def read_xml_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> Union[List[Any], np.ndarray]:
    """
    Read a xml array ( BooleanXmlArray, FloatingPointXmlArray, IntegerXmlArray, StringXmlArray ...)
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """

    values = get_object_attribute_no_verif(energyml_array, "values")
    # count = get_object_attribute_no_verif(energyml_array, "count_per_value")
    # logging.debug("values: ", values)

    if sub_indices is not None and len(sub_indices) > 0:
        if isinstance(values, np.ndarray):
            values = values[sub_indices]
        elif isinstance(values, list):
            # Use list comprehension for efficiency
            values = [values[idx] for idx in sub_indices]
    return values


def read_jagged_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List[Any]:
    """
    Read a jagged array
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    elements = read_array(
        energyml_array=get_object_attribute_no_verif(energyml_array, "elements"),
        root_obj=root_obj,
        path_in_root=(path_in_root or "") + ".elements",
        workspace=workspace,
    )
    cumulative_length = read_array(
        energyml_array=read_array(get_object_attribute_no_verif(energyml_array, "cumulative_length")),
        root_obj=root_obj,
        path_in_root=(path_in_root or "") + ".cumulative_length",
        workspace=workspace,
    )

    # Use list comprehension for better performance
    array = [
        elements[cumulative_length[i - 1] if i > 0 else 0 : cumulative_length[i]] for i in range(len(cumulative_length))
    ]

    if sub_indices is not None and len(sub_indices) > 0:
        array = [array[idx] for idx in sub_indices]
    return array


def read_int_double_lattice_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
):
    """
    Read DoubleLatticeArray or IntegerLatticeArray.
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    start_value = int(get_object_attribute_no_verif(energyml_array, "start_value"))
    offset = get_object_attribute_no_verif(energyml_array, "offset")

    if len(offset) == 0:
        raise Exception(f"{type(energyml_array)} has no offset — cannot generate indices")

    if len(offset) == 1:
        # 1D lattice: start_value, start_value+v, start_value+2v, …  (count+1 values)
        offset_obj = offset[0]
        offset_value = get_object_attribute_no_verif(offset_obj, "value")
        count = int(get_object_attribute_no_verif(offset_obj, "count"))
        result = [start_value + i * offset_value for i in range(count + 1)]
    else:
        # N-D lattice (N ≥ 2) — used for NodeIndicesOnSupportingRepresentation.
        #
        # Each Offset[k] is an IntegerConstantArray with:
        #   Count  = number of *steps* along axis k  →  grid size = Count+1
        #   Value  = stride multiplier for axis k
        #
        # Flat index formula (C/row-major order):
        #   flat_idx(i0, i1, …) = StartValue
        #                        + i0 * Value[0] * (Count[1]+1) * (Count[2]+1) * …
        #                        + i1 * Value[1] * (Count[2]+1) * …
        #                        + …
        #                        + iN-1 * Value[N-1]
        #
        # i.e.  stride[k] = Value[k] * prod(Count[m]+1 for m in range(k+1, N))
        N = len(offset)
        counts = [int(get_object_attribute_no_verif(off, "count")) for off in offset]
        values = [int(get_object_attribute_no_verif(off, "value")) for off in offset]

        strides = []
        for k in range(N):
            s = values[k]
            for m in range(k + 1, N):
                s *= counts[m] + 1
            strides.append(s)

        # np.indices gives shape (N, d0, d1, …)
        shape = tuple(c + 1 for c in counts)
        idx_grids = np.indices(shape)  # (N, *shape)
        flat_indices = start_value + sum(idx_grids[k] * strides[k] for k in range(N))
        result = flat_indices.ravel().tolist()

    return result


def read_point3d_zvalue_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
):
    """
    Read a Point3D2ValueArray
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    supporting_geometry = get_object_attribute_no_verif(energyml_array, "supporting_geometry")
    sup_geom_array = read_array(
        energyml_array=supporting_geometry,
        root_obj=root_obj,
        path_in_root=(path_in_root or "") + ".SupportingGeometry",
        workspace=workspace,
        sub_indices=sub_indices,
    )

    zvalues = get_object_attribute_no_verif(energyml_array, "zvalues")
    zvalues_array = flatten_concatenation(
        read_array(
            energyml_array=zvalues,
            root_obj=root_obj,
            path_in_root=(path_in_root or "") + ".ZValues",
            workspace=workspace,
            sub_indices=sub_indices,
        )
    )

    # Use NumPy for vectorized operation if possible
    error_logged = False

    if isinstance(sup_geom_array, np.ndarray) and isinstance(zvalues_array, np.ndarray):
        # Vectorized assignment for NumPy arrays
        min_len = min(len(sup_geom_array), len(zvalues_array))
        if min_len < len(sup_geom_array):
            logging.warning(
                f"Z-values array ({len(zvalues_array)}) is shorter than geometry array ({len(sup_geom_array)}), only updating first {min_len} values"
            )
        sup_geom_array[:min_len, 2] = zvalues_array[:min_len]
    else:
        # Fallback for list-based arrays
        for i in range(len(sup_geom_array)):
            try:
                sup_geom_array[i][2] = zvalues_array[i]
            except (IndexError, TypeError) as e:
                if not error_logged:
                    logging.error(f"{type(e).__name__}: index {i} is out of bound of {len(zvalues_array)}")
                    error_logged = True

    return sup_geom_array


def read_point3d_from_representation_lattice_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
):
    """
    Read a ``Point3DFromRepresentationLatticeArray``.

    The XY(Z) positions are borrowed from a *supporting* ``Grid2DRepresentation``
    by selecting its nodes via the flat indices described in
    ``NodeIndicesOnSupportingRepresentation`` (an ``IntegerLatticeArray``).

    The index formula for an N-dimensional ``IntegerLatticeArray`` is row-major:

        stride[k] = Value[k] * prod(Count[m]+1 for m in range(k+1, N))
        flat_idx(i, j, …) = StartValue + i*stride[0] + j*stride[1] + …

    Example — supporting rep 2×4, ``Offset[0]={Count=1, Value=1}``,
    ``Offset[1]={Count=3, Value=1}``:
        stride[0] = 1 * 4 = 4,  stride[1] = 1
        flat_idx(i, j) = 4i + j  →  [0,1,2,3,4,5,6,7]

    Note: Only ``Grid2DRepresentation`` supporting reps are currently supported.

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    supporting_rep_dor = get_object_attribute_no_verif(energyml_array, "supporting_representation")
    supporting_rep_identifier = get_obj_uri(supporting_rep_dor)
    supporting_rep = workspace.get_object(supporting_rep_identifier) if workspace is not None else None

    if supporting_rep is None and workspace is not None:
        from energyml.utils.introspection import get_obj_uuid

        candidates = workspace.get_object(get_obj_uri(supporting_rep_dor))
        supporting_rep = candidates[0] if candidates else None

    if supporting_rep is None:
        raise Exception(f"Supporting representation {supporting_rep_identifier} not found in workspace")

    if "grid2d" not in str(type(supporting_rep)).lower():
        raise Exception(
            f"Unsupported supporting rep type {type(supporting_rep).__name__} " f"for {type(energyml_array).__name__}"
        )

    # ── 1. Read ALL points from the supporting representation ────────────────
    # RESQML 2.0.1 uses Grid2dPatch; RESQML 2.2 stores geometry directly.
    all_sup_points: Optional[np.ndarray] = None

    patch_matches = search_attribute_matching_name_with_path(supporting_rep, "Grid2dPatch")
    if patch_matches:
        patch_path, patch = patch_matches[0]
        all_sup_points = read_grid2d_patch(
            patch=patch,
            grid2d=supporting_rep,
            path_in_root=patch_path,
            workspace=workspace,
        )
    else:
        # RESQML 2.2: geometry is directly on the representation
        geom_points_matches = search_attribute_matching_name_with_path(supporting_rep, "Geometry.Points")
        if not geom_points_matches:
            raise Exception(f"Cannot find points in supporting rep {type(supporting_rep).__name__}")
        geom_path, geom_points_obj = geom_points_matches[0]
        all_sup_points = read_array(
            energyml_array=geom_points_obj,
            root_obj=supporting_rep,
            path_in_root=geom_path,
            workspace=workspace,
        )

    if not isinstance(all_sup_points, np.ndarray):
        all_sup_points = np.array(all_sup_points, dtype=float)
    all_sup_points = all_sup_points.reshape(-1, 3)

    # ── 2. Generate the node index list from the IntegerLatticeArray ─────────
    node_idx_arr = get_object_attribute_no_verif(energyml_array, "node_indices_on_supporting_representation")
    if node_idx_arr is None:
        node_idx_arr = get_object_attribute_rgx(energyml_array, "NodeIndices")

    if node_idx_arr is not None:
        node_indices = read_array(
            energyml_array=node_idx_arr,
            root_obj=root_obj,
            path_in_root=path_in_root,
            workspace=workspace,
        )
        node_indices = np.asarray(node_indices, dtype=np.int64)
        result = all_sup_points[node_indices]
    else:
        # No index array: use all points in order (identity mapping)
        logging.debug(
            "Point3DFromRepresentationLatticeArray: no NodeIndices found, " "using all supporting rep points in order"
        )
        result = all_sup_points

    # ── 3. Optional sub-selection (SubRepresentation) ────────────────────────
    if sub_indices is not None and len(sub_indices) > 0:
        result = result[np.asarray(sub_indices, dtype=np.int64)]

    return result


def read_grid2d_patch(
    patch: Any,
    grid2d: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> Union[List, np.ndarray]:
    points_path, points_obj = search_attribute_matching_name_with_path(patch, "Geometry.Points")[0]

    return read_array(
        energyml_array=points_obj,
        root_obj=grid2d,
        path_in_root=path_in_root + "." + points_path if path_in_root else points_path,
        workspace=workspace,
        sub_indices=sub_indices,
    )


def read_point3d_lattice_array(
    energyml_array: Any,
    root_obj: Optional[Any] = None,
    path_in_root: Optional[str] = None,
    workspace: Optional[EnergymlStorageInterface] = None,
    sub_indices: Optional[Union[List[int], np.ndarray]] = None,
) -> List:
    """
    Read a Point3DLatticeArray.

    Accumulates origin + cumulative slowest/fastest offset vectors into an
    (N, 3) float64 array.  CRS transforms (z-flip, offsets, rotation) are the
    responsibility of the caller — this function is CRS-neutral.

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    result = []
    origin = _point_as_array(get_object_attribute_no_verif(energyml_array, "origin"))
    offset = get_object_attribute_rgx(energyml_array, "offset|dimension")

    if len(offset) == 2:
        slowest = offset[0]
        fastest = offset[1]

        crs_sa_count = search_attribute_in_upper_matching_name(
            obj=energyml_array,
            name_rgx="slowestAxisCount",
            root_obj=root_obj,
            current_path=path_in_root or "",
        )

        crs_fa_count = search_attribute_in_upper_matching_name(
            obj=energyml_array,
            name_rgx="fastestAxisCount",
            root_obj=root_obj,
            current_path=path_in_root or "",
        )

        slowest_vec = _point_as_array(get_object_attribute_rgx(slowest, "offset|direction"))
        slowest_spacing = read_array(get_object_attribute_no_verif(slowest, "spacing"))
        slowest_table = list(map(lambda x: prod_n_tab(x, slowest_vec), slowest_spacing))

        fastest_vec = _point_as_array(get_object_attribute_rgx(fastest, "offset|direction"))
        fastest_spacing = read_array(get_object_attribute_no_verif(fastest, "spacing"))
        fastest_table = list(map(lambda x: prod_n_tab(x, fastest_vec), fastest_spacing))

        slowest_size = len(slowest_table)
        fastest_size = len(fastest_table)

        # logging.debug(f"slowest vector: {slowest_vec}, spacing: {slowest_spacing}, size: {slowest_size}")
        # logging.debug(f"fastest vector: {fastest_vec}, spacing: {fastest_spacing}, size: {fastest_size}")
        # logging.debug(f"origin: {origin}")

        if crs_sa_count is not None and len(crs_sa_count) > 0 and crs_fa_count is not None and len(crs_fa_count) > 0:
            if (crs_sa_count[0] == fastest_size and crs_fa_count[0] == slowest_size) or (
                crs_sa_count[0] == fastest_size - 1 and crs_fa_count[0] == slowest_size - 1
            ):
                logging.debug("reversing order")
                # if offset were given in the wrong order
                tmp_table = slowest_table
                slowest_table = fastest_table
                fastest_table = tmp_table

                tmp_size = slowest_size
                slowest_size = fastest_size
                fastest_size = tmp_size
            else:
                slowest_size = crs_sa_count[0]
                fastest_size = crs_fa_count[0]

        # Vectorized approach using NumPy for massive performance improvement
        try:
            # Convert tables to NumPy arrays
            origin_arr = np.array(origin, dtype=float)
            slowest_arr = np.array(slowest_table, dtype=float)  # shape: (slowest_size-1, 3)
            fastest_arr = np.array(fastest_table, dtype=float)  # shape: (fastest_size-1, 3)

            # Sanity: spacing arrays must have exactly (size-1) rows.
            # For well-formed RESQML data this is always true; bail out to the
            # iterative fallback if someone passes malformed data.
            if slowest_arr.shape[0] != slowest_size - 1 or fastest_arr.shape[0] != fastest_size - 1:
                raise ValueError(
                    f"Spacing array length mismatch: "
                    f"slowest={slowest_arr.shape[0]} expected {slowest_size - 1}, "
                    f"fastest={fastest_arr.shape[0]} expected {fastest_size - 1}"
                )

            # Compute cumulative sums (shape: (size-1, 3))
            slowest_cumsum = np.cumsum(slowest_arr, axis=0)
            fastest_cumsum = np.cumsum(fastest_arr, axis=0)

            # Initialize result array
            result_arr = np.zeros((slowest_size, fastest_size, 3), dtype=float)
            result_arr[:, :, :] = origin_arr  # broadcast origin to all positions

            # Accumulate offsets:
            #   result_arr[:, j, :] += fastest_cumsum[j-1]  for j in 1..fastest_size-1
            #   result_arr[i, :, :] += slowest_cumsum[i-1]  for i in 1..slowest_size-1
            result_arr[:, 1:, :] += fastest_cumsum[np.newaxis, :, :]  # (1, fast-1, 3)
            result_arr[1:, :, :] += slowest_cumsum[:, np.newaxis, :]  # (slow-1, 1, 3)

            # Return the (N, 3) float64 numpy array directly — no .tolist().
            result = result_arr.reshape(-1, 3)

        except (ValueError, TypeError) as e:
            # Fallback to original implementation if NumPy conversion fails.
            logging.warning(f"NumPy vectorization failed ({e}), falling back to iterative approach")
            fallback: List = []
            for i in range(slowest_size):
                for j in range(fastest_size):
                    previous_value = origin

                    if j > 0:
                        if i > 0:
                            line_idx = i * fastest_size
                            previous_value = fallback[line_idx + j - 1]
                        else:
                            previous_value = fallback[j - 1]
                        fallback.append(sum_lists(previous_value, fastest_table[j - 1]))
                    else:
                        if i > 0:
                            prev_line_idx = (i - 1) * fastest_size
                            previous_value = fallback[prev_line_idx]
                            fallback.append(sum_lists(previous_value, slowest_table[i - 1]))
                        else:
                            fallback.append(previous_value)
            # Convert fallback list to ndarray to keep the return type consistent.
            result = np.array(fallback, dtype=np.float64).reshape(-1, 3)
    else:
        raise Exception(f"{type(energyml_array)} read with an offset of length {len(offset)} is not supported")

    if sub_indices is not None and len(sub_indices) > 0:
        # result is always an ndarray here; index directly without .tolist().
        result = result[np.asarray(sub_indices, dtype=np.int64)]

    return result


# def read_boolean_constant_array(
#         energyml_array: Any,
#         root_obj: Optional[Any] = None,
#         path_in_root: Optional[str] = None,
#         workspace: Optional[EnergymlStorageInterface] = None
# ):
#     logging.debug(energyml_array)


#    ______                 __    _            __              __
#   / ____/________ _____  / /_  (_)________ _/ /  _________  / /___  __________
#  / / __/ ___/ __ `/ __ \/ __ \/ / ___/ __ `/ /  / ___/ __ \/ / __ \/ ___/ ___/
# / /_/ / /  / /_/ / /_/ / / / / / /__/ /_/ / /  / /__/ /_/ / / /_/ / /  (__  )
# \____/_/   \__,_/ .___/_/ /_/_/\___/\__,_/_/   \___/\____/_/\____/_/  /____/
#                /_/

# ===========================
# PyVista integration snippet
# ===========================

# from energyml.utils.data.helper import (
#     read_graphical_rendering_info, read_property
# )

# # 1. Load objects
# gis   = workspace.get_object(gis_uri)
# prop  = workspace.get_object(prop_uri)
# prop_uuid = get_obj_uuid(prop)

# # 2. Extract rendering info
# info = read_graphical_rendering_info(gis, prop_uuid, workspace)

# # 3. Read scalar values
# scalars = read_array(prop.values_for_patch[0], root_obj=prop, workspace=workspace)

# # 4. Build PyVista LUT
# import pyvista as pv
# if info and info.color_map:
#     lut = pv.LookupTable()
#     lut.values = info.color_map.to_vtk_lut()              # (256,4) RGBA
#     if info.color_min_max:
#         lut.scalar_range = info.color_min_max
#     mesh.plot(scalars=scalars, cmap=lut)
# elif info and info.constant_color:
#     c = info.constant_color
#     mesh.plot(color=(c.r, c.g, c.b), opacity=c.a)
# HsvColor: hue [0,360], saturation [0,1], value [0,1], alpha [0,1], title
# MinMax:   minimum: float, maximum: float

import colorsys
from dataclasses import dataclass, field as dc_field


# ─────────────────────────────────────────────────────────────────────────────
# Unified output data structures
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class RgbaColor:
    """RGBA colour with channels in [0.0, 1.0]."""

    r: float
    g: float
    b: float
    a: float = 1.0

    def to_uint8(self) -> Tuple[int, int, int, int]:
        """Return (R, G, B, A) in [0, 255] - ready for VTK / PyVista."""
        return (
            int(round(self.r * 255)),
            int(round(self.g * 255)),
            int(round(self.b * 255)),
            int(round(self.a * 255)),
        )
        
    def to_hex(self) -> str:
        """Return color as a hex string, e.g. '#RRGGBBAA'."""
        return "#{:02X}{:02X}{:02X}{:02X}".format(*self.to_uint8())
    
    def to_hex_argb(self) -> str:
        """Return color as a hex string in ARGB order, e.g. '#AARRGGBB'."""
        r, g, b, a = self.to_uint8()
        return "#{:02X}{:02X}{:02X}{:02X}".format(a, r, g, b)

    @staticmethod
    def from_hsv(hsv_obj: Any) -> "RgbaColor":
        """Convert a RESQML ``HsvColor`` to :class:`RgbaColor`."""
        h = (hsv_obj.hue or 0.0) / 360.0  # RESQML hue is [0, 360]
        s = hsv_obj.saturation or 0.0
        v = hsv_obj.value or 0.0
        a = hsv_obj.alpha if hsv_obj.alpha is not None else 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return RgbaColor(r, g, b, a)

    @staticmethod
    def random() -> "RgbaColor":
        """Generate a random RGBA color (for testing)."""
        import random

        return RgbaColor(
            r=random.random(),
            g=random.random(),
            b=random.random(),
            a=1.0,
        )

    @staticmethod
    def random_from_uuid(uuid_str: str) -> "RgbaColor":
        """Generate a random RGBA color based on a UUID string (for consistent testing)."""
        import random
        import hashlib

        # Create a hash of the UUID string to seed the random generator
        hash_bytes = hashlib.sha256(uuid_str.encode()).digest()
        seed = int.from_bytes(hash_bytes, "big")
        random.seed(seed)

        return RgbaColor(
            r=random.random(),
            g=random.random(),
            b=random.random(),
            a=1.0,
        )


@dataclass
class ColorMapEntry:
    """One control point: a scalar index mapped to an RGBA colour."""

    index: float  # float for both continuous and discrete (int index cast to float)
    color: RgbaColor


@dataclass
class ColorMapInfo:
    """
    Unified representation of a RESQML color map, directly usable by PyVista/VTK.

    Covers both :class:`ContinuousColorMap` and :class:`DiscreteColorMap`.

    PyVista usage example::

        info = read_color_map(my_continuous_color_map)
        lut = pv.LookupTable()
        lut.values = info.to_vtk_lut()          # (256, 4) uint8 RGBA array
        lut.scalar_range = (info.entries[0].index, info.entries[-1].index)
        mesh.plot(scalars="my_property", cmap=lut)
    """

    is_continuous: bool
    entries: List[ColorMapEntry]  # sorted by ascending index
    null_color: Optional[RgbaColor] = None
    above_max_color: Optional[RgbaColor] = None
    below_min_color: Optional[RgbaColor] = None

    def to_vtk_lut(self, n_colors: int = 256) -> np.ndarray:
        """
        Return an ``(N, 4)`` uint8 RGBA array for use as a PyVista / VTK LUT.

        - For **continuous** maps:  linearly interpolates the control-point
          HSV colors over *n_colors* levels.
        - For **discrete** maps:    returns one row per entry (``n_colors``
          is ignored) so each integer index gets an exact color.

        :param n_colors: Number of samples for continuous maps (default 256).
        :return: ``np.ndarray`` of shape ``(N, 4)``, dtype ``uint8``.
        """
        if not self.entries:
            return np.zeros((1, 4), dtype=np.uint8)

        sorted_entries = sorted(self.entries, key=lambda e: e.index)

        if not self.is_continuous:
            # One exact row per integer entry - no interpolation needed.
            return np.array([e.color.to_uint8() for e in sorted_entries], dtype=np.uint8)

        # Continuous: sample n_colors levels with linear interpolation in RGBA.
        indices = np.array([e.index for e in sorted_entries], dtype=np.float64)
        float_colors = np.array(
            [[e.color.r, e.color.g, e.color.b, e.color.a] for e in sorted_entries],
            dtype=np.float64,
        )
        t = np.linspace(indices[0], indices[-1], n_colors)
        result = np.zeros((n_colors, 4), dtype=np.uint8)
        for ch in range(4):
            result[:, ch] = np.clip(np.interp(t, indices, float_colors[:, ch]) * 255, 0, 255).round().astype(np.uint8)
        return result

    def scalar_range(self) -> Tuple[float, float]:
        """Return ``(min_index, max_index)`` of the stored entries."""
        if not self.entries:
            return (0.0, 1.0)
        indices = [e.index for e in self.entries]
        return (min(indices), max(indices))


@dataclass
class ScalarRenderingInfo:
    """
    All graphical rendering parameters needed to display a RESQML property or
    representation in a 3D viewer (PyVista, VTK, etc.).

    Produced by :func:`read_graphical_rendering_info`.

    Typical PyVista workflow::

        info = read_graphical_rendering_info(gis, prop_uuid, workspace)
        scalars = read_property(prop, workspace)           # np.ndarray
        if info and info.color_map:
            lut = pv.LookupTable()
            lut.values = info.color_map.to_vtk_lut()
            if info.color_min_max:
                lut.scalar_range = info.color_min_max
            mesh.plot(scalars=scalars, cmap=lut)
    """

    target_obj_uuid: str

    # ── Colour mapping (from ColorInformation → ColorMap) ────────────────────
    color_map: Optional[ColorMapInfo] = None
    color_min_max: Optional[Tuple[float, float]] = None  # clamp range for the LUT
    color_use_log: bool = False
    color_use_reverse: bool = False
    color_value_vector_index: Optional[int] = None  # component for vector props

    # ── Alpha / opacity mapping (from AlphaInformation) ──────────────────────
    # Piecewise: list of (property_value, opacity [0..1]) control points
    alpha_control_points: Optional[List[Tuple[float, float]]] = None
    alpha_min_max: Optional[Tuple[float, float]] = None
    alpha_use_log: bool = False
    alpha_overwrite_color_alpha: bool = False

    # ── Size mapping (from SizeInformation) ──────────────────────────────────
    size_min_max: Optional[Tuple[float, float]] = None  # (min_size, max_size)
    size_use_log: bool = False
    size_value_vector_index: Optional[int] = None

    # ── Visibility / constant style (from DefaultGraphicalInformation) ────────
    is_visible: bool = True
    constant_color: Optional[RgbaColor] = None
    constant_alpha: Optional[float] = None  # [0..1] global opacity override

    # ── Contour lines (from ContourLineSetInformation) ────────────────────────
    contour_increment: Optional[float] = None
    contour_show_major_every: Optional[int] = None


# ─────────────────────────────────────────────────────────────────────────────
# Color-map readers  (Group 1 - both return ColorMapInfo)
# ─────────────────────────────────────────────────────────────────────────────


def _optional_rgba(hsv_obj: Optional[Any]) -> Optional[RgbaColor]:
    """Convert an optional ``HsvColor`` to :class:`RgbaColor`, or ``None``."""
    return RgbaColor.from_hsv(hsv_obj) if hsv_obj is not None else None


def read_continuous_color_map(color_map_obj: Any) -> ColorMapInfo:
    """
    Read a RESQML ``ContinuousColorMap`` into a :class:`ColorMapInfo`.

    **Input**: a ``ContinuousColorMap`` xsdata dataclass instance (e.g. from
    ``workspace.get_object(uri)``).

    **Output**: :class:`ColorMapInfo` with ``is_continuous=True`` and entries
    sorted ascending by ``index`` (a ``float``).  The ``to_vtk_lut()`` method
    produces a ``(256, 4)`` uint8 RGBA array directly usable by PyVista.
    """
    entries = sorted(
        [
            ColorMapEntry(index=float(e.index), color=RgbaColor.from_hsv(e.hsv))
            for e in (color_map_obj.entry or [])
            if e.index is not None and e.hsv is not None
        ],
        key=lambda ce: ce.index,
    )
    return ColorMapInfo(
        is_continuous=True,
        entries=entries,
        null_color=_optional_rgba(getattr(color_map_obj, "null_color", None)),
        above_max_color=_optional_rgba(getattr(color_map_obj, "above_max_color", None)),
        below_min_color=_optional_rgba(getattr(color_map_obj, "below_min_color", None)),
    )


def read_discrete_color_map(color_map_obj: Any) -> ColorMapInfo:
    """
    Read a RESQML ``DiscreteColorMap`` into a :class:`ColorMapInfo`.

    **Input**: a ``DiscreteColorMap`` xsdata dataclass instance.

    **Output**: :class:`ColorMapInfo` with ``is_continuous=False`` and one
    entry per integer code.  ``to_vtk_lut()`` returns exactly one RGBA row per
    entry - suitable for VTK's categorical lookup table
    (``vtkLookupTable.SetAnnotation`` workflow).
    """
    entries = sorted(
        [
            ColorMapEntry(index=float(e.index), color=RgbaColor.from_hsv(e.hsv))
            for e in (color_map_obj.entry or [])
            if e.index is not None and e.hsv is not None
        ],
        key=lambda ce: ce.index,
    )
    return ColorMapInfo(
        is_continuous=False,
        entries=entries,
        null_color=_optional_rgba(getattr(color_map_obj, "null_color", None)),
        above_max_color=_optional_rgba(getattr(color_map_obj, "above_max_color", None)),
        below_min_color=_optional_rgba(getattr(color_map_obj, "below_min_color", None)),
    )


def read_color_map(color_map_obj: Any) -> Optional[ColorMapInfo]:
    """
    Dispatch to :func:`read_continuous_color_map` or :func:`read_discrete_color_map`
    based on the runtime type of *color_map_obj*.

    :param color_map_obj: Any RESQML color-map object (``ContinuousColorMap``
        or ``DiscreteColorMap`` from any EML/RESQML version).
    :return: :class:`ColorMapInfo`, or ``None`` if the type is unrecognised.
    """
    type_name = type(color_map_obj).__name__.lower()
    if "continuous" in type_name:
        return read_continuous_color_map(color_map_obj)
    if "discrete" in type_name:
        return read_discrete_color_map(color_map_obj)
    logging.warning(f"read_color_map: unsupported color-map type '{type(color_map_obj).__name__}'")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point  (Group 2)
# ─────────────────────────────────────────────────────────────────────────────


def read_graphical_rendering_info(
    graphical_information_set: Any,
    target_uuid: str,
    workspace: Optional[EnergymlStorageInterface] = None,
) -> Optional[ScalarRenderingInfo]:
    """
    Extract all rendering parameters for a target object from a
    ``GraphicalInformationSet``.

    **Input**:

    - *graphical_information_set*: a RESQML/EML ``GraphicalInformationSet``
      object (from ``workspace.get_object(uri)`` or similar), or directly a GraphicalObject (e.g. DefaultGraphicalInformation).
       The function will search for all graphical information entries in the set that target the specified UUID, and accumulate their parameters into a single :class:`ScalarRenderingInfo` output.
    - *target_uuid*: the UUID (string) of the property, representation,
      feature or interpretation you want to render.
    - *workspace*: an :class:`EnergymlStorageInterface` used to resolve the
      ``ColorMap`` DOR inside ``ColorInformation``.  Pass ``None`` if the
      color map is not needed.

    **Output**: :class:`ScalarRenderingInfo`, or ``None`` if the GIS contains
    no graphical information targeting *target_uuid*.

    Covers all standard RESQML v2.2 ``AbstractGraphicalInformation`` subtypes:

    +-------------------------------+-----------------------------------+
    | RESQML class                  | Populated fields                  |
    +===============================+===================================+
    | ``ColorInformation``          | ``color_map``, ``color_min_max``, |
    |                               | ``color_use_log``, ``color_use_`` |
    |                               | ``reverse``,                      |
    |                               | ``color_value_vector_index``      |
    +-------------------------------+-----------------------------------+
    | ``AlphaInformation``          | ``alpha_control_points``,         |
    |                               | ``alpha_min_max``,                |
    |                               | ``alpha_use_log``,                |
    |                               | ``alpha_overwrite_color_alpha``   |
    +-------------------------------+-----------------------------------+
    | ``SizeInformation``           | ``size_min_max``,                 |
    |                               | ``size_use_log``,                 |
    |                               | ``size_value_vector_index``       |
    +-------------------------------+-----------------------------------+
    | ``DefaultGraphicalInform…``   | ``is_visible``,                   |
    |                               | ``constant_color``,               |
    |                               | ``constant_alpha``                |
    +-------------------------------+-----------------------------------+
    | ``ContourLineSetInform…``     | ``contour_increment``,            |
    |                               | ``contour_show_major_every``      |
    +-------------------------------+-----------------------------------+
    """

    result = ScalarRenderingInfo(target_obj_uuid=target_uuid)
    found = False

    gis_infos: List[Any] = getattr(graphical_information_set, "graphical_information", []) or (
        [graphical_information_set] if not isinstance(graphical_information_set, list) else graphical_information_set
    )

    for info in gis_infos:
        # Each AbstractGraphicalInformation targets ≥1 objects via target_object[].
        targets: List[Any] = getattr(info, "target_object", []) or []
        if not any(get_obj_uuid(t) == target_uuid for t in targets):
            continue
        found = True

        type_name = type(info).__name__

        if "ColorInformation" in type_name:
            result.color_use_log = bool(getattr(info, "use_logarithmic_mapping", False))
            result.color_use_reverse = bool(getattr(info, "use_reverse_mapping", False))
            result.color_value_vector_index = getattr(info, "value_vector_index", None)
            mm = getattr(info, "min_max", None)
            if mm is not None:
                result.color_min_max = (mm.minimum, mm.maximum)
            cmap_dor = getattr(info, "color_map", None)
            if cmap_dor is not None and workspace is not None:
                cmap_obj = workspace.get_object(get_obj_uri(cmap_dor))
                if cmap_obj is None:
                    candidates = workspace.get_object(get_obj_uri(cmap_dor))
                    cmap_obj = candidates[0] if candidates else None
                if cmap_obj is not None:
                    result.color_map = read_color_map(cmap_obj)

        elif "AlphaInformation" in type_name:
            result.alpha_use_log = bool(getattr(info, "use_logarithmic_mapping", False))
            result.alpha_overwrite_color_alpha = bool(getattr(info, "overwrite_color_alpha", False))
            mm = getattr(info, "min_max", None)
            if mm is not None:
                result.alpha_min_max = (mm.minimum, mm.maximum)
            raw_indices = getattr(info, "index", []) or []
            raw_alphas = getattr(info, "alpha", []) or []
            if raw_indices and raw_alphas:
                try:
                    result.alpha_control_points = [(float(idx), float(a)) for idx, a in zip(raw_indices, raw_alphas)]
                except (TypeError, ValueError) as exc:
                    logging.warning(f"read_graphical_rendering_info: cannot parse AlphaInformation indices: {exc}")

        elif "SizeInformation" in type_name:
            result.size_use_log = bool(getattr(info, "use_logarithmic_mapping", False))
            result.size_value_vector_index = getattr(info, "value_vector_index", None)
            mm = getattr(info, "min_max", None)
            if mm is not None:
                result.size_min_max = (mm.minimum, mm.maximum)

        elif "DefaultGraphicalInformation" in type_name:
            for elem_info in getattr(info, "indexable_element_info", []) or []:
                if (getattr(elem_info, "is_visible", None)) is False:
                    result.is_visible = False
                const_col = getattr(elem_info, "constant_color", None)
                if const_col is not None:
                    result.constant_color = RgbaColor.from_hsv(const_col)
                const_alpha = getattr(elem_info, "constant_alpha", None)
                if const_alpha is not None:
                    result.constant_alpha = float(const_alpha)

        elif "ContourLineSetInformation" in type_name:
            result.contour_increment = getattr(info, "increment", None)
            result.contour_show_major_every = getattr(info, "show_major_line_every", None)

        # AnnotationInformation is intentionally not mapped to ScalarRenderingInfo
        # because it drives label text, not colour/size - handle separately if needed.

    return result if found else None

# def numpy_dtype_to_resqml_22_type(dtype: np.dtype, is_external: bool = True) -> Optional[str]:
#     import energyml.resqml.v2_2.resqmlv2
#     # ======== resqml22
#     # BooleanXmlArrayList
#     # FloatingPointXmlArrayList
#     # IntegerXmlArrayList
#     # BooleanXmlArray
#     # StringXmlArray
#     # FloatingPointXmlArray
#     # IntegerXmlArray
#     # ======= common23
#     # BooleanExternalArray
#     # StringExternalArray
#     # FloatingPointExternalArray
#     # IntegerExternalArray
#     # ======= common21
#     # Point2DHdf5Array
#     # Point2dHdf5Array
#     # Point3DHdf5Array
#     # Point3dHdf5Array
#     # StringHdf5Array
#     # BooleanHdf5Array
#     # DoubleHdf5Array
#     # IntegerHdf5Array
    
#     suffix = "ExternalArray" if is_external else "XmlArray"
#     if np.issubdtype(dtype, np.bool_):




# def numpy_to_resqml_array(np_array: np.ndarray, resqlm_version: str = "2.2") -> Any:
#     """
#     Convert a NumPy array to a RESQML array object (e.g. RealArray, IntegerArray).

#     :param np_array: The input NumPy array to convert.
#     :param resqlm_version: The target RESQML version (default "2.2").
#     :return: A RESQML array object containing the data from the NumPy array.
#     """
#     dtype = np_array.dtype
    
