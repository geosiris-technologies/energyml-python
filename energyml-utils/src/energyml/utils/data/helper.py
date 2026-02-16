# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import inspect
import logging
import sys
from typing import Any, Literal, Optional, Callable, List, Tuple, Union

from energyml.utils.storage_interface import EnergymlStorageInterface
import numpy as np

from .datasets_io import read_external_dataset_array
from ..constants import flatten_concatenation, path_last_attribute, path_parent_attribute
from ..exception import ObjectNotFoundNotError
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

from .datasets_io import get_path_in_external_with_path

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


def is_z_reversed(crs: Optional[Any]) -> bool:
    """
    Returns True if the Z axe is reverse (ZIncreasingDownward=='True' or VerticalAxis.Direction=='down')
    :param crs: a CRS object
    :return: By default, False is returned (if 'crs' is None)
    """
    reverse_z_values = False
    if crs is not None:
        if "VerticalCrs" in type(crs).__name__:
            vert_axis = search_attribute_matching_name(crs, "Direction")
            if len(vert_axis) > 0:
                vert_axis_str = str(vert_axis[0])
                if "." in vert_axis_str:
                    vert_axis_str = vert_axis_str.split(".")[-1]

                reverse_z_values = vert_axis_str.lower() == "down"
        else:
            # resqml 201
            zincreasing_downward = search_attribute_matching_name(crs, "ZIncreasingDownward")
            if len(zincreasing_downward) > 0:
                reverse_z_values = zincreasing_downward[0]

            # resqml >= 22
            vert_axis = search_attribute_matching_name(crs, "VerticalAxis.Direction")
            if len(vert_axis) > 0:
                vert_axis_str = str(vert_axis[0])
                if "." in vert_axis_str:
                    vert_axis_str = vert_axis_str.split(".")[-1]

                reverse_z_values = vert_axis_str.lower() == "down"
    logging.debug(f"is_z_reversed: {reverse_z_values}")
    return reverse_z_values


def get_vertical_epsg_code(crs_object: Any):
    vertical_epsg_code = None
    if crs_object is not None:  # LocalDepth3dCRS
        vertical_epsg_code = get_object_attribute_rgx(crs_object, "VerticalCrs.EpsgCode")
        if vertical_epsg_code is None:  # LocalEngineering2DCrs
            vertical_epsg_code = get_object_attribute_rgx(
                crs_object, "OriginProjectedCrs.AbstractProjectedCrs.EpsgCode"
            )
            if vertical_epsg_code is None:
                vertical_epsg_code = get_object_attribute_rgx(crs_object, "abstract_vertical_crs.epsg_code")
    return vertical_epsg_code


def get_projected_epsg_code(crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None) -> Optional[str]:
    if crs_object is not None:  # LocalDepth3dCRS
        projected_epsg_code = get_object_attribute_rgx(crs_object, "ProjectedCrs.EpsgCode")
        if projected_epsg_code is None:  # LocalEngineering2DCrs
            projected_epsg_code = get_object_attribute_rgx(
                crs_object, "OriginProjectedCrs.AbstractProjectedCrs.EpsgCode"
            )

        if projected_epsg_code is None and workspace is not None:
            return get_projected_epsg_code(
                workspace.get_object_by_uuid(get_object_attribute_rgx(crs_object, "LocalEngineering2[dD]Crs.Uuid"))
            )
        return projected_epsg_code
    return None


def get_projected_uom(crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None):
    if crs_object is not None:
        projected_epsg_uom = get_object_attribute_rgx(crs_object, "ProjectedUom")
        if projected_epsg_uom is None:
            projected_epsg_uom = get_object_attribute_rgx(crs_object, "HorizontalAxes.ProjectedUom")

        if projected_epsg_uom is None and workspace is not None:
            return get_projected_uom(
                workspace.get_object_by_uuid(get_object_attribute_rgx(crs_object, "LocalEngineering2[dD]Crs.Uuid"))
            )
        return projected_epsg_uom
    return None


def get_crs_offsets_and_angle(
    crs_object: Any, workspace: Optional[EnergymlStorageInterface] = None
) -> Tuple[float, float, float, Tuple[float, str]]:
    """Return the CRS offsets (X, Y, Z) and the areal rotation angle (value and uom) if they exist in the CRS object."""
    if crs_object is None:
        return 0.0, 0.0, 0.0, (0.0, "rad")

    # eml23.LocalEngineering2DCrs
    _tmpx = get_object_attribute_rgx(crs_object, "OriginProjectedCoordinate1")
    _tmpy = get_object_attribute_rgx(crs_object, "OriginProjectedCoordinate2")
    _tmp_azimuth = get_object_attribute_rgx(crs_object, "azimuth.value")
    _tmp_azimuth_uom = str(get_object_attribute_rgx(crs_object, "azimuth.uom") or "")
    if _tmpx is not None and _tmpy is not None:
        try:
            return (
                float(_tmpx),
                float(_tmpy),
                0.0,
                (float(_tmp_azimuth) if _tmp_azimuth is not None else 0.0, _tmp_azimuth_uom),
            )  # Z offset is not defined in 2D CRS, it is defined in eml23.LocalEngineeringCompoundCrs
        except Exception as e:
            logging.info(f"ERR reading crs offset {e}")

    # resqml20.ObjLocalDepth3DCrs
    _tmpx = get_object_attribute_rgx(crs_object, "XOffset")
    _tmpy = get_object_attribute_rgx(crs_object, "YOffset")
    _tmpz = get_object_attribute_rgx(crs_object, "ZOffset")
    _tmp_azimuth = get_object_attribute_rgx(crs_object, "ArealRotation.value")
    _tmp_azimuth_uom = str(get_object_attribute_rgx(crs_object, "ArealRotation.uom") or "")
    if _tmpx is not None and _tmpy is not None:
        try:
            return (
                float(_tmpx),
                float(_tmpy),
                float(_tmpz),
                (float(_tmp_azimuth) if _tmp_azimuth is not None else 0.0, _tmp_azimuth_uom),
            )
        except Exception as e:
            logging.info(f"ERR reading crs offset {e}")

    # eml23.LocalEngineeringCompoundCrs
    _tmp_z = get_object_attribute_rgx(crs_object, "OriginVerticalCoordinate")

    local_engineering2d_crs_dor = get_object_attribute_rgx(crs_object, "localEngineering2DCrs")
    if local_engineering2d_crs_dor is not None and workspace is not None:
        local_engineering2d_crs_uri = get_obj_uri(local_engineering2d_crs_dor)
        _tmp_x, _tmp_y, _, (azimuth, azimuth_uom) = get_crs_offsets_and_angle(
            workspace.get_object(local_engineering2d_crs_uri), workspace
        )
        return _tmp_x, _tmp_y, float(_tmp_z) if _tmp_z is not None else 0.0, (azimuth, azimuth_uom)

    if _tmp_z is not None:
        try:
            return 0.0, 0.0, float(_tmp_z), (0.0, "rad")
        except Exception as e:
            logging.info(f"ERR reading crs offset {e}")

    return 0.0, 0.0, 0.0, (0.0, "rad")


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
    # Note: RESQML rotation is typically clockwise.
    if angle_rad != 0.0:
        cos_theta = np.cos(angle_rad)
        sin_theta = np.sin(angle_rad)

        x_orig = transformed[:, 0].copy()
        y_orig = transformed[:, 1].copy()

        # Standard 2D rotation matrix
        transformed[:, 0] = x_orig * cos_theta - y_orig * sin_theta
        transformed[:, 1] = x_orig * sin_theta + y_orig * cos_theta

    # 3. Apply Translation (Offsets)
    transformed[:, 0] += x_offset
    transformed[:, 1] += y_offset
    transformed[:, 2] += z_offset

    # 4. Final Vertical Orientation
    # Negate Z if the target system is Z-Up (RESQML is natively Z-Down).
    if z_is_up:
        transformed[:, 2] = -transformed[:, 2]

    return transformed


def get_crs_origin_offset(crs_obj: Any) -> List[float | int]:
    """
    Return a list [X,Y,Z] corresponding to the crs Offset [XOffset/OriginProjectedCoordinate1, ... ] depending on the
    crs energyml version.
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

    crs_point_offset = [0.0, 0.0, 0.0]
    try:
        crs_point_offset = [
            float(tmp_offset_x) if tmp_offset_x is not None else 0.0,
            float(tmp_offset_y) if tmp_offset_y is not None else 0.0,
            float(tmp_offset_z) if tmp_offset_z is not None else 0.0,
        ]
    except Exception as e:
        logging.info(f"ERR reading crs offset {e}")

    return crs_point_offset


def get_datum_information(datum_obj: Any, workspace: Optional[EnergymlStorageInterface] = None):
    "From a ObjMdDatum or a ReferencePointInACrs, return x, y, z, z_increas_downward, projected_epsg_code, vertical_epsg_code"
    if datum_obj is None:
        return 0.0, 0.0, 0.0, False, None, None

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
        )
    elif "referencepointinacrs" in t_lw:
        x = get_object_attribute_rgx(datum_obj, "horizontal_coordinates.coordinate1")
        y = get_object_attribute_rgx(datum_obj, "horizontal_coordinates.coordinate2")
        z = get_object_attribute_rgx(datum_obj, "vertical_coordinate")
        z_increasing_downward = get_object_attribute(datum_obj, "ZIncreasingDownward") or False
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
        )
    elif "mddatum" in t_lw:
        x = get_object_attribute_rgx(datum_obj, "location.coordinate1")
        y = get_object_attribute_rgx(datum_obj, "location.coordinate2")
        z = get_object_attribute_rgx(datum_obj, "location.coordinate3")
        crs = get_object_attribute(datum_obj, "LocalCrs")
        _, _, _, z_increasing_downward, projected_epsg_code, vertical_epsg_code = get_datum_information(crs, workspace)
        return (
            float(x) if x is not None else 0.0,
            float(y) if y is not None else 0.0,
            float(z) if z is not None else 0.0,
            z_increasing_downward,
            projected_epsg_code,
            vertical_epsg_code,
        )
    return 0.0, 0.0, 0.0, False, None, None


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
            # logging.debug(f"CRS found for {get_obj_title(context_obj)} : {crs_list[0]}")
            crs = workspace.get_object(get_obj_uri(crs_list[0]))
            if crs is None:
                # logging.debug(f"CRS {crs_list[0]} not found (or not read correctly)")
                crs = workspace.get_object_by_uuid(get_obj_uuid(crs_list[0]))
            if crs is None:
                logging.error(f"CRS {crs_list[0]} not found (or not read correctly)")
                raise ObjectNotFoundNotError(get_obj_uri(crs_list[0]))
            if crs is not None:
                return crs

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


def generate_vertical_well_points(wellbore_mds: np.ndarray, head_x: float, head_y: float, head_z: float) -> np.ndarray:
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
    md_start = wellbore_mds[0]
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
        crs = get_crs_obj(
            context_obj=root_obj,
            root_obj=root_obj,
            path_in_root=path_in_root,
            workspace=workspace,
        )

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
) -> List[Any]:
    """
    Read a constant array ( BooleanConstantArray, DoubleConstantArray, FloatingPointConstantArray, IntegerConstantArray ...)
    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    # logging.debug(f"Reading constant array\n\t{energyml_array}")

    value = get_object_attribute_no_verif(energyml_array, "value")
    count = (
        len(sub_indices)
        if sub_indices is not None and len(sub_indices) > 0
        else get_object_attribute_no_verif(energyml_array, "count")
    )

    # logging.debug(f"\tValue : {[value for i in range(0, count)]}")

    return [value] * count


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
    start_value = get_object_attribute_no_verif(energyml_array, "start_value")
    offset = get_object_attribute_no_verif(energyml_array, "offset")

    result = []

    if len(offset) == 1:
        # 1D lattice array: offset is a single DoubleConstantArray or IntegerConstantArray
        offset_obj = offset[0]

        # Get the offset value and count from the ConstantArray
        offset_value = get_object_attribute_no_verif(offset_obj, "value")
        count = get_object_attribute_no_verif(offset_obj, "count")

        # Generate the 1D array: start_value + i * offset_value for i in range(count)
        result = [start_value + i * offset_value for i in range(count)]
    else:
        raise Exception(f"{type(energyml_array)} read with an offset of length {len(offset)} is not supported")

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
    Read a Point3DFromRepresentationLatticeArray.

    Note: Only works for Grid2DRepresentation.

    :param energyml_array:
    :param root_obj:
    :param path_in_root:
    :param workspace:
    :param sub_indices:
    :return:
    """
    supporting_rep_identifier = get_obj_uri(get_object_attribute_no_verif(energyml_array, "supporting_representation"))
    # logging.debug(f"energyml_array : {energyml_array}\n\t{supporting_rep_identifier}")
    supporting_rep = workspace.get_object(supporting_rep_identifier) if workspace is not None else None

    # TODO chercher un pattern \.*patch\.*.[d]+ pour trouver le numero du patch dans le path_in_root puis lire le patch
    # logging.debug(f"path_in_root {path_in_root}")

    result = []
    if "grid2d" in str(type(supporting_rep)).lower():
        patch_path, patch = search_attribute_matching_name_with_path(supporting_rep, "Grid2dPatch")[0]
        points = read_grid2d_patch(
            patch=patch, grid2d=supporting_rep, path_in_root=patch_path, workspace=workspace, sub_indices=sub_indices
        )
        # TODO: take the points by there indices from the NodeIndicesOnSupportingRepresentation
        result = points

    else:
        raise Exception(f"Not supported type {type(energyml_array)} for object {type(root_obj)}")
    # pour trouver les infos qu'il faut
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

    Note: If a CRS is found and its 'ZIncreasingDownward' is set to true or its

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

        crs = None
        try:
            crs = get_crs_obj(
                context_obj=energyml_array,
                path_in_root=path_in_root,
                root_obj=root_obj,
                workspace=workspace,
            )
        except ObjectNotFoundNotError:
            logging.error("No CRS found, not able to check zIncreasingDownward")

        zincreasing_downward = is_z_reversed(crs)

        slowest_vec = _point_as_array(get_object_attribute_rgx(slowest, "offset|direction"))
        slowest_spacing = read_array(get_object_attribute_no_verif(slowest, "spacing"))
        slowest_table = list(map(lambda x: prod_n_tab(x, slowest_vec), slowest_spacing))

        fastest_vec = _point_as_array(get_object_attribute_rgx(fastest, "offset|direction"))
        fastest_spacing = read_array(get_object_attribute_no_verif(fastest, "spacing"))
        fastest_table = list(map(lambda x: prod_n_tab(x, fastest_vec), fastest_spacing))

        slowest_size = len(slowest_table)
        fastest_size = len(fastest_table)

        logging.debug(f"slowest vector: {slowest_vec}, spacing: {slowest_spacing}, size: {slowest_size}")
        logging.debug(f"fastest vector: {fastest_vec}, spacing: {fastest_spacing}, size: {fastest_size}")
        logging.debug(f"origin: {origin}, zincreasing_downward: {zincreasing_downward}")

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
            slowest_arr = np.array(slowest_table, dtype=float)  # shape: (slowest_size, 3)
            fastest_arr = np.array(fastest_table, dtype=float)  # shape: (fastest_size, 3)

            # Compute cumulative sums
            slowest_cumsum = np.cumsum(slowest_arr, axis=0)  # cumulative offset along slowest axis
            fastest_cumsum = np.cumsum(fastest_arr, axis=0)  # cumulative offset along fastest axis

            # Create meshgrid indices
            i_indices, j_indices = np.meshgrid(np.arange(slowest_size), np.arange(fastest_size), indexing="ij")

            # Initialize result array
            result_arr = np.zeros((slowest_size, fastest_size, 3), dtype=float)
            result_arr[:, :, :] = origin_arr  # broadcast origin to all positions

            # Add offsets based on zincreasing_downward
            if zincreasing_downward:
                # Add slowest offsets where i > 0
                result_arr[1:, :, :] += slowest_cumsum[:-1, np.newaxis, :]
                # Add fastest offsets where j > 0
                result_arr[:, 1:, :] += fastest_cumsum[np.newaxis, :-1, :]
            else:
                # Add fastest offsets where j > 0
                result_arr[:, 1:, :] += fastest_cumsum[np.newaxis, :-1, :]
                # Add slowest offsets where i > 0
                result_arr[1:, :, :] += slowest_cumsum[:-1, np.newaxis, :]

            # Flatten to list of points
            result = result_arr.reshape(-1, 3).tolist()

        except (ValueError, TypeError) as e:
            # Fallback to original implementation if NumPy conversion fails
            logging.warning(f"NumPy vectorization failed ({e}), falling back to iterative approach")
            for i in range(slowest_size):
                for j in range(fastest_size):
                    previous_value = origin

                    if j > 0:
                        if i > 0:
                            line_idx = i * fastest_size
                            previous_value = result[line_idx + j - 1]
                        else:
                            previous_value = result[j - 1]
                        if zincreasing_downward:
                            result.append(sum_lists(previous_value, slowest_table[i - 1]))
                        else:
                            result.append(sum_lists(previous_value, fastest_table[j - 1]))
                    else:
                        if i > 0:
                            prev_line_idx = (i - 1) * fastest_size
                            previous_value = result[prev_line_idx]
                            if zincreasing_downward:
                                result.append(sum_lists(previous_value, fastest_table[j - 1]))
                            else:
                                result.append(sum_lists(previous_value, slowest_table[i - 1]))
                        else:
                            result.append(previous_value)
    else:
        raise Exception(f"{type(energyml_array)} read with an offset of length {len(offset)} is not supported")

    if sub_indices is not None and len(sub_indices) > 0:
        if isinstance(result, np.ndarray):
            result = result[sub_indices].tolist()
        else:
            result = [result[idx] for idx in sub_indices]

    return result


# def read_boolean_constant_array(
#         energyml_array: Any,
#         root_obj: Optional[Any] = None,
#         path_in_root: Optional[str] = None,
#         workspace: Optional[EnergymlStorageInterface] = None
# ):
#     logging.debug(energyml_array)
