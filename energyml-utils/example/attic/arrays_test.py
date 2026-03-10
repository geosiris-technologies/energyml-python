import logging
import traceback
from typing import List, Optional
from energyml.utils.data.datasets_io import get_handler_registry
import numpy as np
from energyml.utils.data.helper import _ARRAY_NAMES_, read_array
from energyml.utils.data.mesh import (
    AbstractMesh,
    SurfaceMesh,
    PolylineSetMesh,
    read_column_based_table,
    read_mesh_object,
    read_property_interpreted_with_cbt,
    read_property,
    read_time_series,
)
from energyml.utils.storage_interface import EnergymlStorageInterface
from energyml.utils.epc import Epc
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.utils.introspection import (
    get_obj_title,
    search_attribute_matching_name,
    get_object_attribute,
    search_attribute_matching_name_with_path,
)
# from energyml.resqml.v2_2.resqmlv2 import VerticalCRS
# from energyml.resqml.v2_0_1.resqmlv2 import DiscreteProperty as DiscreteProperty201, ContinuousProperty as ContinuousProperty201
# from energyml.eml.v2_3.commonv2 import TimeSeries, ColumnBasedTable
# from energyml.eml.v2_1.commonv2 import TimeSeries as TimeSeries21

from energyml.utils.serialization import read_energyml_xml_str, serialize_json


xml_Point3DLatticeArray = """
<resqml:Point3dLatticeArray  xmlns:eml="http://www.energistics.org/energyml/data/commonv2" xmlns:prodml="http://www.energistics.org/energyml/data/prodmlv2" xmlns:witsml="http://www.energistics.org/energyml/data/witsmlv2" xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2"  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="resqml:Point3dLatticeArray">
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
</resqml:Point3dLatticeArray>
"""


grid_2D = """<?xml version="1.0" encoding="UTF-8"?>
<resqml:Grid2dRepresentation xmlns:eml="http://www.energistics.org/energyml/data/commonv2" xmlns:prodml="http://www.energistics.org/energyml/data/prodmlv2" xmlns:witsml="http://www.energistics.org/energyml/data/witsmlv2" xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2" uuid="4e56b0e4-2cd1-4efa-97dd-95f72bcf9f80" schemaVersion="22">
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
    <resqml:Points xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="resqml:Point3dLatticeArray">
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

polyline_rep = """<?xml version="1.0" encoding="UTF-8"?>
<resqml:PolylineRepresentation xmlns:eml="http://www.energistics.org/energyml/data/commonv2" xmlns:prodml="http://www.energistics.org/energyml/data/prodmlv2" xmlns:witsml="http://www.energistics.org/energyml/data/witsmlv2" xmlns:resqml="http://www.energistics.org/energyml/data/resqmlv2" uuid="47f86668-27c4-4b28-a19e-bd0355321ecc" schemaVersion="22">
  <eml:Citation>
    <eml:Title>Horizon1 Interp1 SinglePolylineRep</eml:Title>
    <eml:Originator>phili</eml:Originator>
    <eml:Creation>2026-02-13T16:55:39Z</eml:Creation>
    <eml:Format>F2I-CONSULTING:FESAPI Example:2.14.1.0</eml:Format>
  </eml:Citation>
  <resqml:RepresentedObject>
    <eml:Uuid>ac12dc12-4951-459b-b585-90f48aa88a5a</eml:Uuid>
    <eml:QualifiedType>resqml22.HorizonInterpretation</eml:QualifiedType>
    <eml:Title>Horizon1 Interp1</eml:Title>
  </resqml:RepresentedObject>
  <resqml:IsClosed>false</resqml:IsClosed>
  <resqml:NodePatchGeometry>
    <resqml:LocalCrs>
      <eml:Uuid>5c0703c5-3806-424e-86cf-8f59c8bb39fa</eml:Uuid>
      <eml:QualifiedType>eml23.LocalEngineeringCompoundCrs</eml:QualifiedType>
      <eml:Title>Default local CRS</eml:Title>
    </resqml:LocalCrs>
    <resqml:Points xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="resqml:Point3dExternalArray">
      <resqml:Coordinates>
        <eml:ExternalDataArrayPart>
          <eml:Count>12</eml:Count>
          <eml:PathInExternalFile>/resqml22/47f86668-27c4-4b28-a19e-bd0355321ecc/points_patch0</eml:PathInExternalFile>
          <eml:StartIndex>0</eml:StartIndex>
          <eml:URI>testingPackageCpp22.h5</eml:URI>
          <eml:MimeType>application/x-hdf5</eml:MimeType>
        </eml:ExternalDataArrayPart>
      </resqml:Coordinates>
    </resqml:Points>
    <resqml:SeismicCoordinates xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="resqml:Seismic2dCoordinates">
      <resqml:SeismicSupport>
        <eml:Uuid>5a371b9e-7202-42de-83a0-1b996d20586b</eml:Uuid>
        <eml:QualifiedType>resqml22.PolylineRepresentation</eml:QualifiedType>
        <eml:Title>Seismic line Rep</eml:Title>
      </resqml:SeismicSupport>
      <resqml:LineAbscissa xsi:type="eml:FloatingPointExternalArray">
        <eml:ArrayFloatingPointType>arrayOfFloat32LE</eml:ArrayFloatingPointType>
        <eml:CountPerValue>1</eml:CountPerValue>
        <eml:Values>
          <eml:ExternalDataArrayPart>
            <eml:Count>4</eml:Count>
            <eml:PathInExternalFile>/resqml22/47f86668-27c4-4b28-a19e-bd0355321ecc/lineAbscissa_patch0</eml:PathInExternalFile>
            <eml:StartIndex>0</eml:StartIndex>
            <eml:URI>testingPackageCpp22.h5</eml:URI>
            <eml:MimeType>application/x-hdf5</eml:MimeType>
          </eml:ExternalDataArrayPart>
        </eml:Values>
      </resqml:LineAbscissa>
    </resqml:SeismicCoordinates>
  </resqml:NodePatchGeometry>
</resqml:PolylineRepresentation>
"""


def read_grid() -> List[AbstractMesh]:
    point3d_lattice_array = read_energyml_xml_str(xml_Point3DLatticeArray)
    # print(point3d_lattice_array)
    # point3d_lattice_array.value
    if "DerivedElement" in str(type(point3d_lattice_array)):
        point3d_lattice_array = point3d_lattice_array.value
    print(serialize_json(point3d_lattice_array, check_obj_prefixed_classes=False))

    print(np.array(read_array(point3d_lattice_array, None)))

    grid_2d = read_energyml_xml_str(grid_2D)
    if "DerivedElement" in str(type(grid_2d)):
        grid_2d = grid_2d.value

    meshes = read_mesh_object(grid_2d)
    return meshes


def read_polyline() -> List[AbstractMesh]:
    # polyline_representation = read_energyml_xml_str(polyline_rep)
    # if "DerivedElement" in str(type(polyline_representation)):
    #     polyline_representation = polyline_representation.value

    # meshes = read_mesh_object(polyline_representation)
    # return meshes

    epc = Epc.read_file("rc/epc/testingPackageCpp22.epc", read_rels_from_files=False, recompute_rels=False)

    polyline0 = epc.get_object_by_uuid("a54b8399-d3ba-4d4b-b215-8d4f8f537e66")[0]
    # polyline0 = epc.get_object_by_uuid("65c59595-bf48-451e-94aa-120ebdf28d8b")[0]
    # polyline0 = epc.get_object_by_uuid("47f86668-27c4-4b28-a19e-bd0355321ecc")[0]
    print(polyline0)
    print(epc.get_h5_file_paths(polyline0))

    meshes = read_mesh_object(energyml_object=polyline0, workspace=epc)

    return meshes


def read_wellbore_frame_repr(
    epc_path: str = "rc/epc/testingPackageCpp22.epc",
    well_uuid: str = "d873e243-d893-41ab-9a3e-d20b851c099f",
) -> List[AbstractMesh]:
    epc = Epc.read_file(f"{epc_path}", read_rels_from_files=False, recompute_rels=False)

    frame_repr = epc.get_object_by_uuid(well_uuid)[0]
    # print(frame_repr)
    # print(epc.get_h5_file_paths(frame_repr))

    meshes = read_mesh_object(energyml_object=frame_repr, workspace=epc)

    # Previous result :
    # points:
    #     [[   0.    0.    0.]
    #     [   0.    0.  250.]
    #     [   0.    0.  500.]
    #     [   0.    0.  750.]
    #     [   0.    0. 1000.]]
    # line indices:
    #     [[0 1]
    #     [1 2]
    #     [2 3]
    #     [3 4]]

    return meshes


def read_representation_set_representation() -> List[AbstractMesh]:
    epc = Epc.read_file("rc/epc/testingPackageCpp22.epc", read_rels_from_files=False, recompute_rels=False)

    rep_set_rep = epc.get_object_by_uuid("6b992199-5b47-4624-a62c-b70857133cda")[0]
    # print(rep_set_rep)
    print(epc.get_h5_file_paths(rep_set_rep))

    return read_mesh_object(energyml_object=rep_set_rep, workspace=epc)


def read_props_and_cbt(
    epc_path: List[str] = [
        "rc/epc/testingPackageCpp22.epc",
        "D:/Geosiris/Clients/BRGM/git/csv-to-energyml/rc/output/full-local/attic/result-out-EpcStream-egis-full.epc",
    ],
    p_or_cbt_uuids: List = [
        "1c5a3e99-e997-4bd7-a94d-c45d7b7405ce",
        "be17c053-9189-4bc0-9db1-75aa51a026cd",
        "da73937c-2c60-4e10-8917-5154fde4ded5",
        "6561b499-82ed-4233-8a83-ea5d5aaf56a9",
        "0d6aba60-b37e-498c-aedc-334561eb0749",
        "d64d0ed0-72fa-4495-8e3a-a01175194e25",
        "5abecfe6-b951-4802-9002-e597169a9923",
        "49207072-563b-404a-9707-9a9b70168d33",
    ],
) -> None:

    epcs = []
    for path in epc_path:
        epc = Epc.read_file(
            epc_file_path=path,
            # rels_update_mode=RelsUpdateMode.MANUAL,
        )
        # epc = EpcStreamReader(
        #     epc_file_path=path,
        #     rels_update_mode=RelsUpdateMode.MANUAL,
        # )
        # epc = Epc.read_file(f"{path}", read_rels_from_files=False, recompute_rels=False)
        epcs.append(epc)

    for uuid in p_or_cbt_uuids:
        read = False
        prop_or_cbt = None
        for epc in epcs:
            try:
                prop_or_cbt_lst = epc.get_object_by_uuid(uuid)
                if not prop_or_cbt_lst:
                    continue
                prop_or_cbt = prop_or_cbt_lst[0]
                array = None
                reshaped_array = None
                if "column" in str(type(prop_or_cbt)).lower():
                    array = read_column_based_table(prop_or_cbt, workspace=epc)
                elif "time" in str(type(prop_or_cbt)).lower():
                    array = read_time_series(prop_or_cbt, workspace=epc)
                else:
                    array = read_property(
                        prop_or_cbt,
                        workspace=epc,
                    )
                    reshaped_array = read_property_interpreted_with_cbt(
                        prop_or_cbt,
                        workspace=epc,
                        _cache_property_arrays=array,
                        _return_none_if_no_category_lookup=True,
                    )
                print("=" * 40)
                # print("TS: ", search_attribute_matching_name(prop_or_cbt, "\\w*.time_series"))
                # print(f"\t {get_object_attribute(prop_or_cbt, 'time_or_interval_series.time_series')}")
                print(f"{type(prop_or_cbt)} : {get_obj_title(prop_or_cbt)} - uuid: {uuid}")
                print(array)

                if reshaped_array is not None:
                    print(" # => interpreted array:")
                    print(reshaped_array)

                print("\n")
                read = True
                break
            # except NotSupportedError as e:
            #     print(f"Object with uuid {uuid} found but not supported: {e}")
            except Exception as e:
                traceback.print_exc()
                print(f"Error reading object with uuid {uuid}: {e}")
                pass
        if not read:
            print("[E]" + "=" * 40)
            if prop_or_cbt is not None:
                print(f"Object with uuid {get_obj_title(prop_or_cbt)} found but could not be read.")
            else:
                print(f"Object with uuid {uuid} not found in any EPC file.")
            print("\n")


def read_trset(
    epc_path: str = "rc/epc/testingPackageCpp22.epc", trset_uuid: str = "6e678338-3b53-49b6-8801-faee493e0c42"
) -> List[AbstractMesh]:
    epc = Epc.read_file(f"{epc_path}", read_rels_from_files=False, recompute_rels=False)

    trset = epc.get_object_by_uuid(trset_uuid)[0]
    # print(trset)
    # print(epc.get_h5_file_paths(trset))

    meshes = read_mesh_object(energyml_object=trset, workspace=epc)

    return meshes


def print_tuple_list(tuple_list: List[tuple]) -> None:
    for t in tuple_list:
        print(t)


def read_pointset(
    epc_path: str = "rc/epc/testingPackageCpp22.epc", pointset_uuid: str = "fbc5466c-94cd-46ab-8b48-2ae2162b372f"
) -> List[AbstractMesh]:
    # epc = Epc.read_file(f"{epc_path}", read_rels_from_files=False, recompute_rels=False)
    epc = EpcStreamReader(
        epc_file_path=epc_path,
        rels_update_mode=RelsUpdateMode.MANUAL,
    )

    pointset = epc.get_object_by_uuid(pointset_uuid)[0]
    # print(pointset)
    # print(epc.get_h5_file_paths(pointset))
    # meshes = []
    meshes = read_mesh_object(energyml_object=pointset, workspace=epc)

    print(epc.get_obj_rels(pointset))

    # logging.debug("=" * 40)
    # print_tuple_list(search_attribute_matching_name_with_path(pointset, r"NodePatch.[\d]+.Geometry.Points"))
    # logging.debug("=" * 40)
    # print_tuple_list(
    #     search_attribute_matching_name_with_path(pointset, r"NodePatchGeometry.[\d]+.Points")
    # )  # resqml 2.0.1
    # logging.debug("=" * 40)

    return meshes


def read_wellbore_frame_repr_demo_jfr_02_26(
    epc_path: str = r"rc/epc/out-galaxy-12-pts.epc",
    well_uuid: str = "cfad9cb6-99fe-4172-b560-d2feca75dd9f",
) -> List[AbstractMesh]:
    # epc = Epc.read_file(f"{epc_path}", read_rels_from_files=False, recompute_rels=False)
    epc = EpcStreamReader(f"{epc_path}", rels_update_mode=RelsUpdateMode.MANUAL)

    frame_repr = epc.get_object_by_uuid(well_uuid)[0]
    # print(frame_repr)
    # print(epc.get_h5_file_paths(frame_repr))

    print(epc.get_h5_file_paths())

    print(epc.get_h5_file_paths(frame_repr))

    print("Object type: ", type(frame_repr))

    meshes = read_mesh_object(energyml_object=frame_repr, workspace=epc)

    # Previous result :
    # points:
    #     [[   0.    0.    0.]
    #     [   0.    0.  250.]
    #     [   0.    0.  500.]
    #     [   0.    0.  750.]
    #     [   0.    0. 1000.]]
    # line indices:
    #     [[0 1]
    #     [1 2]
    #     [2 3]
    #     [3 4]]

    return meshes


def test_read_write_array(h5_path):

    handler_registry = get_handler_registry()

    h5_handler = handler_registry.get_handler_for_file(h5_path)
    if h5_handler is None:
        print(f"No handler found for file {h5_path}")
        return
    h5_handler.write_array(
        array=np.array([[1, 2, 3], [4, 5, 6]]),
        target=h5_path,
        path_in_external_file="/test_array",
    )

    h5_handler.file_cache.close_all()

    print(
        h5_handler.read_array(
            source=h5_path,
            path_in_external_file="/test_array",
        )
    )

    success = h5_handler.write_array(
        array=np.array([[7, 8, 9], [10, 11, 12]]),
        target=h5_path,
        path_in_external_file="/test_array2",
    )
    print(f"Write success: {success}")

    cached = h5_handler.file_cache.get_or_open(h5_path, h5_handler, "a")
    # print if file is still opened :
    print(f"File still opened after write: {cached} is open: {hasattr(cached, 'id') and cached.id.valid}")

    success = h5_handler.write_array(
        array=np.array([[13, 14, 15], [16, 17, 18]]),
        target=h5_path,
        path_in_external_file="/test_array3",
    )
    print(f"Write success: {success}")

    print(
        h5_handler.read_array(
            source=h5_path,
            path_in_external_file="/test_array2",
        )
    )


if __name__ == "__main__":
    # Run $env:PYTHONPATH="src" if it fails to be executed from the project root.
    logging.basicConfig(level=logging.DEBUG)
    meshes = []
    # meshes = read_grid()
    # meshes = read_polyline()
    # meshes = read_wellbore_frame_repr()
    # meshes = read_representation_set_representation()
    # meshes = read_trset()
    # meshes = read_pointset()
    # meshes = read_wellbore_frame_repr_demo_jfr_02_26()

    print(f"Number of meshes read: {len(meshes)}")

    if meshes:
        for m in meshes:
            print("=" * 40)
            print(f"Mesh identifier: {m.identifier}")
            print("points:")
            print(np.array(m.point_list))

            if isinstance(m, SurfaceMesh):
                print("face indices:")
                print(np.array(m.faces_indices))
            elif isinstance(m, PolylineSetMesh):
                print("line indices:")
                try:
                    print(np.array(m.line_indices))
                except Exception as e:
                    print(m.line_indices)
                    raise e

    # read_props_and_cbt()
    read_props_and_cbt(epc_path=["D:/Geosiris/Gitlab/clients/brgm/csv-to-energyml/rc/output/result.epc"], 
                       p_or_cbt_uuids=["a9d7a549-1a21-4659-b85e-2b2d3ba3a7ca"])
    # read_props_and_cbt(epc_path=["D:/Geosiris/Gitlab/clients/brgm/csv-to-energyml/rc/output/result.epc"], 
    #                    p_or_cbt_uuids=["deaa96db-9cd0-456c-beb1-dc19607fcfb9", "399678cf-6fe6-4522-9fba-710115c546cf"])
    
    # from energyml.eml.v2_3.commonv2 import IntegerLatticeArray, IntegerConstantArray
    # print(read_array(IntegerLatticeArray(
    #             start_value=1,
    #             offset=[IntegerConstantArray(value=2, count=5)],
    #         )))
    # test_read_write_array("test_array_rw.h5")
