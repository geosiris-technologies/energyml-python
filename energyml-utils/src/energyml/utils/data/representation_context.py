# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
import logging
from typing import Any, Dict, List, Optional, Union
from energyml.opc.opc import Relationship
from energyml.utils.data.crs import CrsInfo
from pydantic import BaseModel, Field, ConfigDict

from energyml.utils.uri import Uri
from energyml.utils.storage_interface import EnergymlStorageInterface
from energyml.utils.epc_utils import extract_uuid_and_version_from_obj_path, get_property_kind_by_title, get_property_kind_uuid_from_property_object
from energyml.utils.introspection import get_obj_uri, get_obj_uuid, get_object_attribute, is_enum, search_attribute_matching_name
from energyml.utils.data.helper import RgbaColor, ScalarRenderingInfo, IndexableElementRenderingInfo, read_color_map, read_graphical_rendering_info
from energyml.utils.data.crs import extract_crs_info

NO_KIND = "NO_KIND"

# ─────────────────────────────────────────────────────────────────────────────
# Element-type keys (RESQML class name suffixes used in ScalarRenderingInfo.elements)
# ─────────────────────────────────────────────────────────────────────────────

_ELEMENT_KEY_FACES = "GraphicalInformationForFaces"
_ELEMENT_KEY_EDGES = "GraphicalInformationForEdges"
_ELEMENT_KEY_NODES = "GraphicalInformationForNodes"
_ELEMENT_KEY_VOLUMES = "GraphicalInformationForVolumes"
_ELEMENT_KEY_WHOLE = "GraphicalInformationForWholeObject"


def _primary_element_key(type_name: str) -> str:
    """Return the dominant element-type key for a RESQML representation class name."""
    t = type_name.lower()
    if any(k in t for k in ("triangulated", "grid2d", "horizon", "surface", "grid")):
        return _ELEMENT_KEY_FACES
    if any(k in t for k in ("polyline", "wellbore", "trajectory", "seismic")):
        return _ELEMENT_KEY_EDGES
    if "point" in t:
        return _ELEMENT_KEY_NODES
    return _ELEMENT_KEY_WHOLE


class CellType(Enum):
    FACE = "face"
    EDGE = "edge"
    NODE = "node"
    VOLUME = "volume"
    WHOLE = "whole"
    
    def __str__(self):
        return self.value
    
    def __eq__(self, value):
        return (isinstance(value, str) and self.value == value.lower()) or (isinstance(value, CellType) and self.value == value.value)

def _primary_cell_type_for_object(type_name: str) -> CellType:
    """Return the dominant element-type key for a RESQML representation class name."""
    if not isinstance(type_name, str):
        type_name = type(type_name).__name__
    t = type_name.lower()
    if any(k in t for k in (_ELEMENT_KEY_VOLUMES.lower(), "ijk", "grid3d")):
        return CellType.VOLUME
    if any(k in t for k in (_ELEMENT_KEY_FACES.lower(), "triangulated", "grid2d", "horizon", "surface", "grid")):
        return CellType.FACE
    if any(k in t for k in (_ELEMENT_KEY_EDGES.lower(), "polyline", "wellbore", "trajectory", "seismic")):
        return CellType.EDGE
    if "point" in t or _ELEMENT_KEY_NODES.lower() in t:
        return CellType.NODE
    return CellType.WHOLE


def _element_constant_color(
    ri: ScalarRenderingInfo, key: str
) -> Optional[RgbaColor]:
    """Return the constant color for *key* element type, falling back to WholeObject."""
    elem = ri.elements.get(key)
    if elem is not None and elem.constant_color is not None:
        return elem.constant_color
    whole = ri.elements.get(_ELEMENT_KEY_WHOLE)
    if whole is not None and whole.constant_color is not None:
        return whole.constant_color
    return None


def collect_graphical_info(obj: Any, workspace: EnergymlStorageInterface) -> Dict[str, List[Any]]:
    rels = workspace.get_obj_rels(obj)
    # print("\tRelationships for object:", rels)
    obj_uuid = get_obj_uuid(obj)
    return collect_graphical_info_from_rels(rels, obj_uuid, workspace)


def collect_graphical_info_from_rels(
    rels: List[Relationship], obj_uuid: str, workspace: EnergymlStorageInterface
) -> Dict[str, List[Any]]:
    graphical_info_result = {}
    # Collect graphical information entries whose target matches this representation
    for r in rels:
        if "GraphicalInformationSet" in r.target:
            uuid, version = extract_uuid_and_version_from_obj_path(r.target)
            graphical_info_set = workspace.get_object_by_uuid_versioned(uuid, version)
            if graphical_info_set is None:
                logging.warning(f"GraphicalInformationSet {r.target} not found in workspace")
                continue
            graphical_info_set_uri = get_obj_uri(graphical_info_set)
            for graphical_info in getattr(graphical_info_set, "graphical_information", []):
                target_dors = getattr(graphical_info, "target_object", None)
                if target_dors is not None:
                    if not isinstance(target_dors, list):
                        target_dors = [target_dors]
                    for target_dor in target_dors:
                        target_dor_uuid = get_obj_uuid(target_dor)
                        if target_dor_uuid == obj_uuid:
                            if graphical_info_set_uri not in graphical_info_result:
                                graphical_info_result[graphical_info_set_uri] = []
                            graphical_info_result[graphical_info_set_uri].append(graphical_info)
                            break
    return graphical_info_result


def get_color(cell_type: Union[str, CellType], object_type: str, graphical_info: List[Any], workspace: EnergymlStorageInterface) -> Optional[RgbaColor]:
    """
    Return the color of an object based on its graphical information, or None if not found.
    The function searches for ColorInformation object if found and if the cell_type matches the type of the object_type
    (e.g. "face" for TriangulatedSet or Grid, "edge" for PolylineSet, "node" for PointSet, etc.). 
    If cell_type and object_type do not match, or if no ColorInformation is found, a search is done for DefaultGraphicalInformation 
    that contains an indexable_element_info with the appropriate cell_type. If none found, search for a WholeObject indexable_element_info.
    """
    # test if cell_type and object_type matches
    obj_cell_type = _primary_cell_type_for_object(object_type)
    if cell_type == obj_cell_type:
        # same type, search for ColorInformation
        for gi in graphical_info:
            if "ColorInformation" in type(gi).__name__:
                try:
                    value_vector_index = int(getattr(gi, "value_vector_index", None))
                    cmap_dor = getattr(gi, "color_map", None)
                    if cmap_dor is not None and workspace is not None:
                        cmap_obj = workspace.get_object(get_obj_uri(cmap_dor))
                        if cmap_obj is not None:
                            color_map = read_color_map(cmap_obj)
                            return color_map.entries[value_vector_index].color
                except Exception as exc:
                    logging.debug(f"Error reading ColorInformation: {exc}")
                    
    # Search for DefaultGraphicalInformation with matching cell_type
    info_whole_color = []
    for gi in graphical_info:
        if "DefaultGraphicalInformation" in type(gi).__name__:
            try:
                for elem_info in getattr(gi, "indexable_element_info", []):
                    elem_cell_type = _primary_cell_type_for_object(type(elem_info).__name__)
                    if elem_cell_type == CellType.WHOLE:
                        if elem_info.constant_color is not None:
                            info_whole_color.append(RgbaColor.from_hsv(elem_info.constant_color))
                    if elem_cell_type == cell_type:
                        if elem_info.constant_color is not None:
                            return RgbaColor.from_hsv(elem_info.constant_color)
            except Exception as exc:
                logging.debug(f"Error reading DefaultGraphicalInformation: {exc}")

    if info_whole_color:
        return info_whole_color[0].to_rgb()
    
    return None

def get_color_from_object(obj: Any, cell_type: Union[str, CellType], workspace: EnergymlStorageInterface, target_obj_type: Optional[str]=None) -> Optional[RgbaColor]:
    """
    Return the color of an object based on its graphical information, or None if not found.
    The function searches for ColorInformation object if found and if the cell_type matches the type of the target_obj_type
    (e.g. "face" for TriangulatedSet or Grid, "edge" for PolylineSet, "node" for PointSet, etc.). 
    If cell_type and target_obj_type do not match, or if no ColorInformation is found, a search is done for DefaultGraphicalInformation 
    that contains an indexable_element_info with the appropriate cell_type. If none found, search for a WholeObject indexable_element_info.
    If target_obj_type is not provided, it will be inferred from the type of obj.
    """
    if target_obj_type is None:
        target_obj_type = type(obj).__name__
    graphical_info = collect_graphical_info(obj, workspace)
    return get_color(cell_type, target_obj_type, [gi for gis in graphical_info.values() for gi in gis], workspace)


class RepresentationContext(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    obj: Any = Field(...)
    workspace: EnergymlStorageInterface = Field(...)
    uri: Uri = Field(default="")

    crs: List[Any] = Field(default_factory=list)
    crs_infos: List[CrsInfo] = Field(default_factory=list)
    
    rels: List[Relationship] = Field(default_factory=list)

    # Graphical information keyed by GraphicalInformationSet uri → list of entries
    graphical_info: Dict[str, List[Any]] = Field(default_factory=dict)

    time_series: List[Any] = Field(default_factory=list)
    
    _projected_uom: Optional[str] = None
    _vertical_uom: Optional[str] = None
    
    _interpretation: Optional[Any] = None
    _interpretation_context: Optional["RepresentationContext"] = None

    def __init__(self, obj: Any, workspace: EnergymlStorageInterface, **data):
        super().__init__(obj=obj, workspace=workspace, uri=get_obj_uri(obj), **data)
        
        # Properties keyed by object uuid → property object
        self._props = {}
        self._props_by_kind = {}
        self._rendering_info = None
        self.update()

    def update(self):
        self.rels = self.workspace.get_obj_rels(self.obj)
        self._collect_properties(self.rels)
        self._collect_crs()
        self._collect_graphical_info(self.rels)
        self.collect_time_series()
        self._rendering_info = None  # invalidate lazy cache
        
    

    def collect_time_series(self):
        self.time_series = []
        time_series_dors = search_attribute_matching_name(self.obj, r"time_series")
        if time_series_dors is not None:
            for ts_dor in time_series_dors:
                ts_obj = self.workspace.get_object(get_obj_uri(ts_dor))
                if ts_obj is not None:
                    self.time_series.append(ts_obj)
                else:
                    logging.warning(f"TimeSeries {get_obj_uri(ts_dor)} not found in workspace")

    def _collect_properties(self, rels: List[Relationship]):
        # Collect related properties keyed by property uuid
        self._props = {}
        self._props_by_kind = {}
        for r in self.rels:
            if "Property" in r.target:
                uuid, version = extract_uuid_and_version_from_obj_path(r.target)
                prop = self.workspace.get_object_by_uuid_versioned(uuid, version)
                if prop is None:
                    logging.warning(f"Property {r.target} not found in workspace")
                    continue
                prop_uuid = getattr(prop, "uuid", NO_KIND)
                self._props[prop_uuid] = prop
                prop_kind_uuid = get_property_kind_uuid_from_property_object(prop) or NO_KIND
                if prop_kind_uuid not in self._props_by_kind:
                    self._props_by_kind[prop_kind_uuid] = []
                    
                if prop_kind_uuid != NO_KIND:
                    self._props_by_kind[prop_kind_uuid].append(prop)
                else:
                    # Search if a standard name is given (in resqml 201)
                    title = get_object_attribute(prop, "propertyKind.kind")
                    if title is not None:
                        if is_enum(title):
                            title = title.value
                        pk = get_property_kind_by_title(title)
                        if pk is not None:
                            self._props_by_kind[pk.uuid].append(prop)
                        else:
                            self._props_by_kind[NO_KIND].append(prop)
                    else:
                        self._props_by_kind[NO_KIND].append(prop)

    def _collect_crs(self):
        # Collect related CRS objects referenced by the representation
        self.crs = []
        self.crs_infos = []
        crs_uuids = set()
        crs_dors = search_attribute_matching_name(self.obj, r"\.*Crs", search_in_sub_obj=True, deep_search=False)
        if crs_dors is not None and len(crs_dors) > 0:
            for crs_ref in crs_dors:
                if crs_ref is not None:
                    crs = self.workspace.get_object(get_obj_uri(crs_ref))
                    if crs is not None:
                        self.crs.append(crs) # always add to keep crs for each patch
                        crs_uuid = getattr(crs, "uuid", None)
                        if crs_uuid is not None and crs_uuid not in crs_uuids:
                            crs_uuids.add(crs_uuid)
                            self.crs_infos.append(extract_crs_info(crs, self.workspace))
                    else:
                        logging.warning(f"CRS {get_obj_uri(crs_ref)} not found in workspace")

    def _collect_graphical_info(self, rels: List[Relationship]):
        # Collect graphical information entries whose target matches this representation
        self.graphical_info = collect_graphical_info_from_rels(rels, self.uri.uuid, self.workspace)

    @property
    def rendering_info(self) -> Optional[ScalarRenderingInfo]:
        """Lazily accumulate and cache all graphical rendering info for this representation."""
        if self._rendering_info is None:
            accumulated: Optional[ScalarRenderingInfo] = None
            for _gis_uri, entries in self.graphical_info.items():
                for entry in entries:
                    try:
                        ri = read_graphical_rendering_info(entry, self.uri.uuid, self.workspace)
                        if ri is None:
                            continue
                        if accumulated is None:
                            accumulated = ri
                        else:
                            # Merge elements dict (later entries overwrite earlier for same key)
                            accumulated.elements.update(ri.elements)
                            if ri.color_map is not None:
                                accumulated.color_map = ri.color_map
                            if ri.color_min_max is not None:
                                accumulated.color_min_max = ri.color_min_max
                            if ri.contour_major_line_info is not None:
                                accumulated.contour_major_line_info = ri.contour_major_line_info
                            if ri.contour_minor_line_info is not None:
                                accumulated.contour_minor_line_info = ri.contour_minor_line_info
                    except Exception as exc:
                        logging.debug(f"Error reading graphical rendering info: {exc}")
            self._rendering_info = accumulated
        return self._rendering_info
    
    
    def get_related_color(self, cell_type: Union[str, CellType]) -> Optional[RgbaColor]:
        """Return the color of an object based on its graphical information, or None if not found. Search is done for the given cell_type first, then fallback to WholeObject."""
        obj_type = type(self.obj).__name__
        color = None
        # Fallback on interpretation
        if self.interpretation_as_context is not None:
            color = get_color(cell_type, obj_type, [gi for gis in self.interpretation_as_context.graphical_info.values() for gi in gis], self.workspace)
        if color is None:
            # search for units in rels or interpretation rels
            cached_uuids = set()
            for r in self.rels + (self.interpretation_as_context.rels if self.interpretation_as_context is not None else []):
                if "Unit" in r.target:
                    uuid, version = extract_uuid_and_version_from_obj_path(r.target)
                    print(f"Found Unit reference in relationship: {r.target} (uuid={uuid}, version={version})")
                    if uuid not in cached_uuids:
                        cached_uuids.add(uuid)
                        unit_obj = self.workspace.get_object_by_uuid_versioned(uuid, version)
                        if unit_obj is not None:
                            col = get_color_from_object(unit_obj, cell_type, self.workspace, target_obj_type=obj_type)
                            if col is not None:
                                return col
        return color

    @property
    def mesh_color(self) -> Optional[RgbaColor]:
        """Constant color for mesh elements (faces or volumes), or None if not set."""
        cell_type = _primary_cell_type_for_object(self.obj)
        obj_type = type(self.obj).__name__
        color = get_color(cell_type, obj_type, [gi for gis in self.graphical_info.values() for gi in gis], self.workspace)
        
        return color or self.get_related_color(cell_type)
            

    @property
    def face_color(self) -> Optional[RgbaColor]:
        """Constant color for face elements, or None if not set."""
        color = get_color(CellType.FACE, type(self.obj).__name__, [gi for gis in self.graphical_info.values() for gi in gis], self.workspace)
        return color or self.get_related_color(CellType.FACE)

    @property
    def edge_color(self) -> Optional[RgbaColor]:
        """Constant color for edge elements, or None if not set."""
        color = get_color(CellType.EDGE, type(self.obj).__name__, [gi for gis in self.graphical_info.values() for gi in gis], self.workspace)
        return color or self.get_related_color(CellType.EDGE)
            
    @property
    def node_color(self) -> Optional[RgbaColor]:
        """Constant color for node/point elements, or None if not set."""
        color = get_color(CellType.NODE, type(self.obj).__name__, [gi for gis in self.graphical_info.values() for gi in gis], self.workspace)
        return color or self.get_related_color(CellType.NODE)
            
    @property
    def primary_color(self) -> RgbaColor:
        """Best constant color for this representation type, falling back to a UUID-seeded random color."""
        ri = self.rendering_info
        if ri is not None:
            key = _primary_element_key(type(self.obj).__name__)
            color = _element_constant_color(ri, key)
            if color is not None:
                return color
        return RgbaColor.random_from_uuid(self.uri.uuid)

    def get_property(self, property_uuid: str) -> Optional[Any]:
        """Return the property object with the given uuid, or None."""
        return self._props.get(property_uuid)
    
    @property
    def vertical_is_time(self) -> bool:
        """Return True if the vertical axis of the representation is time, based on interpretation domain or CRS info."""
        # Check interpretation domain first
        domain = self.domain
        if domain is not None and "time" in domain.lower():
            return True
        
        return False
    
    @property
    def domain(self) -> Optional[str]:
        """Return the domain of the representation (e.g. "depth", "time", "depth/time", etc.) if available from interpretation, or None."""
        interp = self.interpretation
        if interp is not None:
            try:
                return interp.domain.value
            except Exception as e:
                print(f"Error accessing interpretation domain: {e}")
                pass
        return None
    
    @property
    def interpretation(self) -> Optional[Any]:
        """Return the interpretation object related to this representation, or None if not found."""
        if self._interpretation is not None:
            return self._interpretation
        interpretation_dor = None
        try:
            interpretation_dor = self.obj.represented_interpretation
        except Exception as exc:
            try:
                interpretation_dor = self.obj.represented_object
            except Exception as exc:
                pass
        if interpretation_dor is not None:
            interpretation_obj = self.workspace.get_object(get_obj_uri(interpretation_dor))
            if interpretation_obj is not None:
                self._interpretation = interpretation_obj
                return interpretation_obj
            
        return None
    
    @property
    def interpretation_as_context(self) -> Optional["RepresentationContext"]:
        """Return the interpretation as a RepresentationContext, or None if not found."""
        if self._interpretation_context is not None:
            return self._interpretation_context
        
        interp = self.interpretation
        if interp is not None:
            self._interpretation_context = RepresentationContext(interp, self.workspace)
            return self._interpretation_context
        return None
    
    @property
    def projected_uom(self) -> Optional[str]:
        """Return the projected unit of measure (e.g. "m") if available from CRS info, or None."""
        for ci in self.crs_infos:
            if ci.projected_uom is not None:
                return ci.projected_uom
        return None

    @property
    def vertical_uom(self) -> Optional[str]:
        """Return the vertical unit of measure (e.g. "m") if available from CRS info, or None."""
        if self.vertical_is_time:
            # For time-based representations, return the time unit of measure if available
            for ci in self.crs_infos:
                if ci.time_uom is not None:
                    return ci.time_uom
            # If timeUom not found, fall back to vertical_uom (for VerticalCRS, istime doesn't exists and istime is defined in CompoundCRS with vertical_axis)
                
        for ci in self.crs_infos:
            if ci.vertical_uom is not None:
                return ci.vertical_uom
        return None
    
    @property
    def properties(self) -> Dict[str, Any]:
        """Return a dict of all properties keyed by property uuid."""
        return self._props
    
    @property
    def properties_by_kind(self) -> Dict[str, List[Any]]:
        """Return a dict of properties grouped by property kind uuid."""
        return self._props_by_kind

    def get_properties_time_series(self, property_uuid: str) -> Dict[str, List[Any]]:
        """
        Return a time-indexed dict {time_step_str: [property_values, ...]} for
        the given property uuid.  Returns an empty dict when the property has no
        time series reference.
        """
        from energyml.utils.data.mesh import read_time_series, read_property

        prop = self.get_property(property_uuid)
        if prop is None:
            logging.warning(f"Property {property_uuid} not found in context")
            return {}

        time_series_dor = search_attribute_matching_name(prop, r"TimeSeries")
        if not time_series_dor:
            return {}

        ts_obj = self.workspace.get_object(get_obj_uri(time_series_dor[0]))
        if ts_obj is None:
            return {}

        steps = read_time_series(ts_obj, self.workspace)
        values = read_property(prop, self.workspace)

        result: Dict[str, List[Any]] = {}
        for step_idx, dt in steps:
            result[str(dt)] = values[step_idx] if step_idx < len(values) else []
        return result

    def seach_same_representation_in_other_time_step(self) -> List[Uri]:
        """Search for another representation that has the same interpretation, and same TimeSeries reference (if any), but different time step."""
        if self.time_series is None or len(self.time_series) == 0:
            logging.debug(
                f"Representation {self.uri} has no TimeSeries reference, skipping search for same representation in other time step"
            )
            return []
        interpretation_dor = getattr(self.obj, "represented_interpretation", None)
        if interpretation_dor is None:
            return None

        obj_time_series_uuids = {get_obj_uuid(ts) for ts in self.time_series}

        similar_representations = []

        interp_rels = self.workspace.get_obj_rels(get_obj_uri(interpretation_dor))
        for r in interp_rels:
            if self.uri.object_type in r.target and self.uri.uuid not in r.target:
                candidate_uuid, candidate_version = extract_uuid_and_version_from_obj_path(r.target)
                candidate = self.workspace.get_object_by_uuid_versioned(candidate_uuid, candidate_version)

                if candidate is not None:
                    candidate_time_series_dor = search_attribute_matching_name(candidate, r"time_series")
                    candidate_time_series_uuids = (
                        {get_obj_uuid(ts) for ts in candidate_time_series_dor} if candidate_time_series_dor else set()
                    )
                    # search if at least one of the TimeSeries references is the same between the candidate and the current representation
                    if len(obj_time_series_uuids.intersection(candidate_time_series_uuids)) > 0:
                        similar_representations.append(get_obj_uri(candidate))

        return similar_representations

    def dump(self) -> str:
        """Return a human-readable summary of the context for debugging."""
        lines: List[str] = []
        lines.append("=" * 60)
        lines.append(f"RepresentationContext")
        lines.append(f"  URI     : {self.uri}")
        lines.append(f"  Type    : {type(self.obj).__name__}")
        lines.append("")

        lines.append(f"  CRS ({len(self.crs)}):")
        for c in self.crs:
            lines.append(f"    - {type(c).__name__}  {get_obj_uri(c)}")
            
        # UOMs
        lines.append("  UOM:")
        lines.append(f"    - vertical_uom from CRS info: {self.vertical_uom}")
        lines.append(f"    - projected_uom from CRS info: {self.projected_uom}")
        lines.append(f"    - vertical_is_time: {self.vertical_is_time}")
        lines.append(f"    - interpretation domain: {self.domain}")
        
        
        # Interpretation
        lines.append("  Interpretation:")
        lines.append(f"    - represented_interpretation: {get_obj_uri(getattr(self.obj, 'represented_interpretation', None))}")

        lines.append("")
        lines.append(f"  Relationships ({len(self.rels)}):")
        for r in self.rels:
            lines.append(f"    - [{r.type_ if hasattr(r, 'type_') else getattr(r, 'type', '?')}]  {r.target}")

        lines.append("")
        lines.append(f"  Properties ({len(self.properties_by_kind)}):")
        for kind, props in self.properties_by_kind.items():
            lines.append(f"    - Kind {kind} ({len(props)} properties)")
            for prop in props:
                lines.append(f"      - {type(prop).__name__}  uuid={get_obj_uuid(prop)}")

        lines.append("")
        lines.append(f"  Graphical info ({len(self.graphical_info)} set(s)):")
        for uri, entries in self.graphical_info.items():
            lines.append(f"    - Set {uri}  ({len(entries)} entr{'y' if len(entries)==1 else 'ies'})")

        lines.append("=" * 60)
        return "\n".join(lines)


if __name__ == "__main__2":
    import sys

    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

    epc_path = "rc/epc/testingPackageCpp22.epc"
    representation_uri = "df2103a0-fa3d-11e5-b8d4-0002a5d5c51b."
    # representation_uri = "eml:///resqml20.obj_Grid2dRepresentation(030a82f6-10a7-4ecf-af03-54749e098624)"

    from energyml.utils.epc import Epc

    epc = Epc.read_file(epc_path)
    workspace = epc  # Epc extends EnergymlStorageInterface directly

    repr_obj = workspace.get_object(representation_uri)
    if repr_obj is None:
        print(f"ERROR: object not found for URI {representation_uri}")
        sys.exit(1)

    repr_ctx = RepresentationContext(repr_obj, workspace)

    # --- dump of values ---
    print(repr_ctx.dump())

    # Detail: CRS info
    if repr_ctx.crs:
        from energyml.utils.data.crs import extract_crs_info

        print("\nCRS details:")
        for c in repr_ctx.crs:
            info = extract_crs_info(c, workspace)
            print(f"  {type(c).__name__}:")
            print(f"    x_offset={info.x_offset}, y_offset={info.y_offset}, z_offset={info.z_offset}")
            print(f"    z_increasing_downward={info.z_increasing_downward}")
            print(f"    projected_epsg={info.projected_epsg_code}, vertical_epsg={info.vertical_epsg_code}")
            print(f"    areal_rotation={info.areal_rotation_value} {info.areal_rotation_uom}")
            print(f"    axis_order={info.projected_axis_order}")

    # Detail: property arrays (truncated)
    if repr_ctx._props:
        from energyml.utils.data.mesh import read_property

        print("\nProperty arrays (first 10 values):")
        for uuid, prop in repr_ctx._props.items():
            try:
                arr = read_property(prop, workspace)
                print(f"  {type(prop).__name__} [{uuid}]: shape={getattr(arr, 'shape', len(arr))}  sample={arr[:10]}")
            except Exception as exc:
                print(f"  {type(prop).__name__} [{uuid}]: ERROR reading — {exc}")

    # print property time series values
    if repr_ctx._props:
        print("\nProperty time series values:")
        for uuid, prop in repr_ctx._props.items():
            try:
                ts_values = repr_ctx.get_properties_time_series(uuid)
                if ts_values:
                    print(f"  {type(prop).__name__} [{uuid}]:")
                    for time_step, values in ts_values.items():
                        print(f"    - Time {time_step}: sample={values[:10]}")
            except Exception as exc:
                print(f"  {type(prop).__name__} [{uuid}]: ERROR reading time series — {exc}")



if __name__ == "__main__3":
    # Run $env:PYTHONPATH="src" if it fails to be executed from the project root.
    # poetry run python .\src\energyml\utils\data\representation_context.py
    import sys

    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

    epc_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/BRGM_RESQML_PROJECT_2024/AVRE/exports_brgm/AVRE_COMPLETED_APRIL_SURF/AVRE_COLORED_valentin.epc"
    representation_uri = "eml:///resqml22.StratigraphicUnitInterpretation(feefb8d2-785e-4173-8315-69b57e022c53)"

    from energyml.utils.epc import Epc

    epc = Epc.read_file(epc_path)
    workspace = epc  # Epc extends EnergymlStorageInterface directly

    repr_obj = workspace.get_object(representation_uri)
    if repr_obj is None:
        print(f"ERROR: object not found for URI {representation_uri}")
        sys.exit(1)
        
    print("GI : ", collect_graphical_info(repr_obj, workspace))

    


if __name__ == "__main__":
    # Run $env:PYTHONPATH="src" if it fails to be executed from the project root.
    # poetry run python .\src\energyml\utils\data\representation_context.py
    import sys

    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

    epc_path = "D:/Geosiris/Cloud/Geo-Workflow/BRGM/BRGM_RESQML_PROJECT_2024/AVRE/exports_brgm/AVRE_COMPLETED_APRIL_SURF/AVRE_COLORED_valentin.epc"
    # representation_uri = "eml:///resqml22.TriangulatedSetRepresentation(b1fd87b4-17f7-4730-a37b-7829e59add4b)"  # SENO
    # representation_uri = "eml:///resqml22.TriangulatedSetRepresentation(13b8bf5d-af9e-4b23-9ef0-5be693afd617)"  # PERC
    # representation_uri = "eml:///resqml22.StratigraphicUnitInterpretation(feefb8d2-785e-4173-8315-69b57e022c53)"
    representation_uri = "eml:///resqml22.StratigraphicUnitInterpretation(ff7a469b-606a-4fb8-969c-f136269de1a5)"  # PERC

    from energyml.utils.epc import Epc

    epc = Epc.read_file(epc_path)
    workspace = epc  # Epc extends EnergymlStorageInterface directly

    repr_obj = workspace.get_object(representation_uri)
    if repr_obj is None:
        print(f"ERROR: object not found for URI {representation_uri}")
        sys.exit(1)
        
    gi_list = []
    for gi in collect_graphical_info(repr_obj, workspace).values():
        gi_list.extend(gi)
        # for entry in gi:
        #     try:
        #         rendering_info = read_graphical_rendering_info(entry, get_obj_uuid(repr_obj), workspace)
        #         print(f"Rendering info for entry {type(entry)}")
        #         print(f"\t{rendering_info}")
        #     except Exception as exc:
        #         print(f"Error reading graphical rendering info for entry {entry}: {exc}")
                
                
    # print(get_color(CellType.FACE, type(repr_obj).__name__, gi_list, workspace))
    # print(get_color(CellType.EDGE, type(repr_obj).__name__, gi_list, workspace))
    repr_ctx = RepresentationContext(repr_obj, workspace)
    print(repr_ctx.face_color)
    print(repr_ctx.edge_color)
    print(repr_ctx.node_color)

    