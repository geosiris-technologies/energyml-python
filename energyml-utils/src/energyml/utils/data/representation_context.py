# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import Any, Dict, List, Optional
from energyml.opc.opc import Relationship
from energyml.utils.data.crs import CrsInfo
from pydantic import BaseModel, Field, ConfigDict

from energyml.utils.uri import Uri
from energyml.utils.storage_interface import EnergymlStorageInterface
from energyml.utils.epc_utils import extract_uuid_and_version_from_obj_path, get_property_kind_by_title, get_property_kind_uuid_from_property_object
from energyml.utils.introspection import get_obj_uri, get_obj_uuid, get_object_attribute, is_enum, search_attribute_matching_name
from energyml.utils.data.helper import RgbaColor, ScalarRenderingInfo, read_graphical_rendering_info
from energyml.utils.data.crs import extract_crs_info

NO_KIND = "NO_KIND"


def collect_graphical_info(obj: Any, workspace: EnergymlStorageInterface) -> dict:
    rels = workspace.get_obj_rels(obj)
    obj_uuid = get_obj_uuid(obj)
    return collect_graphical_info_from_rels(rels, obj_uuid, workspace)


def collect_graphical_info_from_rels(
    rels: List[Relationship], obj_uuid: str, workspace: EnergymlStorageInterface
) -> dict:
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


class RepresentationContext(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    obj: Any = Field(...)
    workspace: EnergymlStorageInterface = Field(...)
    uri: Uri = Field(default="")

    crs: List[Any] = Field(default_factory=list)
    crs_infos: List[CrsInfo] = Field(default_factory=list)
    
    rels: List[Relationship] = Field(default_factory=list)

    # Graphical information keyed by GraphicalInformationSet uri → list of entries
    graphical_info: dict = Field(default_factory=dict)

    time_series: list = Field(default_factory=list)
    
    _projected_uom: Optional[str] = None
    _vertical_uom: Optional[str] = None
    
    _interpretation: Optional[Any] = None

    def __init__(self, obj: Any, workspace: EnergymlStorageInterface, **data):
        super().__init__(obj=obj, workspace=workspace, uri=get_obj_uri(obj), **data)
        
        # Properties keyed by object uuid → property object
        self._props = {}
        self._props_by_kind = {}
        self.update()

    def update(self):
        self.rels = self.workspace.get_obj_rels(self.obj)
        self._collect_properties(self.rels)
        self._collect_crs()
        self._collect_graphical_info(self.rels)
        self.collect_time_series()
        
    

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

    def get_default_color(self) -> ScalarRenderingInfo:
        """Search for a default color (first found) for the representation, and return it as an RGBA tuple.  Returns a random color (generated from uuid) if no color information is found."""
        for gis_uri, entries in self.graphical_info.items():
            for entry in entries:
                try:
                    rendering_info = read_graphical_rendering_info(entry, self.uri.uuid, self.workspace)
                    if rendering_info is not None:
                        return rendering_info
                except Exception as exc:
                    logging.debug(f"Error reading graphical rendering info for entry {entry}: {exc}")
        # No color information found, generate a random color from uuid
        return ScalarRenderingInfo(
            target_obj_uuid=self.uri.uuid, constant_color=RgbaColor.random_from_uuid(self.uri.uuid)
        )

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


if __name__ == "__main__":
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
