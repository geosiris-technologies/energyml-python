# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from energyml.eml.v2_0.commonv2 import Citation as Citation20
from energyml.eml.v2_0.commonv2 import (
    DataObjectReference as DataObjectReference201,
)
from energyml.eml.v2_3.commonv2 import Citation
from energyml.eml.v2_3.commonv2 import DataObjectReference
from energyml.resqml.v2_0_1.resqmlv2 import FaultInterpretation
from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation

from src.energyml.utils.epc import (
    get_obj_identifier,
    gen_energyml_object_path,
    EpcExportVersion,
)
from src.energyml.utils.introspection import (
    epoch_to_date,
    epoch,
    gen_uuid,
    get_obj_pkg_pkgv_type_uuid_version,
    get_obj_uri,
)

fi_cit = Citation20(
    title="An interpretation",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

fi = FaultInterpretation(
    citation=fi_cit,
    uuid=gen_uuid(),
    object_version="0",
)

tr_cit = Citation(
    title="--",
    # title="test title",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

dor = DataObjectReference(
    uuid=fi.uuid,
    title="a DOR title",
    object_version="0",
    qualified_type="a wrong qualified type",
)

dor_correct20 = DataObjectReference201(
    uuid=fi.uuid,
    title="a DOR title",
    content_type="application/x-resqml+xml;version=2.0;type=obj_FaultInterpretation",
    version_string="0",
)

dor_correct23 = DataObjectReference(
    uuid=fi.uuid,
    title="a DOR title",
    object_version="0",
    qualified_type="resqml20.obj_FaultInterpretation",
)

tr = TriangulatedSetRepresentation(
    citation=tr_cit,
    uuid=gen_uuid(),
    represented_object=dor_correct23,
)


def test_get_obj_identifier():
    assert get_obj_identifier(tr) == tr.uuid + "."
    assert get_obj_identifier(fi) == fi.uuid + ".0"
    assert get_obj_identifier(dor_correct20) == dor_correct20.uuid + ".0"
    assert get_obj_identifier(dor_correct23) == dor_correct23.uuid + ".0"


def test_get_obj_pkg_pkgv_type_uuid_version_obj_201():
    (
        domain,
        domain_version,
        object_type,
        obj_uuid,
        obj_version,
    ) = get_obj_pkg_pkgv_type_uuid_version(fi)
    assert domain == "resqml"
    assert domain_version == "20"
    assert object_type == "obj_FaultInterpretation"
    assert obj_uuid == fi.uuid
    assert obj_version == fi.object_version


def test_get_obj_pkg_pkgv_type_uuid_version_obj_22():
    (
        domain,
        domain_version,
        object_type,
        obj_uuid,
        obj_version,
    ) = get_obj_pkg_pkgv_type_uuid_version(tr)
    assert domain == "resqml"
    assert domain_version == "22"
    assert object_type == "TriangulatedSetRepresentation"
    assert obj_uuid == tr.uuid
    assert obj_version == tr.object_version


def test_get_obj_uri():
    assert str(get_obj_uri(tr)) == f"eml:///resqml22.TriangulatedSetRepresentation({tr.uuid})"
    assert (
        str(get_obj_uri(tr, "/MyDataspace/"))
        == f"eml:///dataspace('/MyDataspace/')/resqml22.TriangulatedSetRepresentation({tr.uuid})"
    )

    assert (
        str(get_obj_uri(fi)) == f"eml:///resqml20.obj_FaultInterpretation(uuid={fi.uuid},version='{fi.object_version}')"
    )
    assert (
        str(get_obj_uri(fi, "/MyDataspace/"))
        == f"eml:///dataspace('/MyDataspace/')/resqml20.obj_FaultInterpretation(uuid={fi.uuid},version='{fi.object_version}')"
    )


def test_gen_energyml_object_path():
    assert gen_energyml_object_path(tr) == f"TriangulatedSetRepresentation_{tr.uuid}.xml"
    assert (
        gen_energyml_object_path(tr, EpcExportVersion.EXPANDED)
        == f"namespace_resqml22/{tr.uuid}/TriangulatedSetRepresentation_{tr.uuid}.xml"
    )
