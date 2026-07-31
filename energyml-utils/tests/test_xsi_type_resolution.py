# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
"""An ``xsi:type`` with no prefix must resolve against the default namespace of the document.

That is the common spelling in the wild: energyml files usually declare ``commonv2`` as their
default namespace, and the polymorphic CRS types (``VerticalCrsEpsgCode``, ``ProjectedCrsEpsgCode``)
are declared there — so ``xsi:type="VerticalCrsEpsgCode"`` is valid and unambiguous.

``FallbackNamespaceXmlParser`` used to rewrite the default-namespace key from ``None`` to ``""``
while merging its fallback namespaces. :meth:`xsdata.formats.converter.QNameConverter.resolve`
reads it as ``ns_map[None]`` (an unprefixed value splits to a ``None`` prefix), so the type was
lost, the element was built as its abstract base and every child became an unknown property.
Concretely: a RESQML 2.0.1 ``LocalDepth3dCrs`` lost both of its EPSG codes, which is enough to
make any WGS84 reprojection impossible.
"""

import pytest

from energyml.utils.data.crs import extract_crs_info
from energyml.utils.serialization import read_energyml_xml_bytes

_CRS_TEMPLATE = """<ns2:LocalDepth3dCrs xmlns="http://www.energistics.org/energyml/data/commonv2"
 {extra_ns}xmlns:ns2="http://www.energistics.org/energyml/data/resqmlv2"
 schemaVersion="2.0" uuid="716f6472-18a3-4f19-a57c-d4f5642ccc53">
    <Citation>
        <Title>Default</Title>
        <Originator>tests</Originator>
        <Creation>2019-03-22T10:29:55Z</Creation>
        <Format>tests</Format>
    </Citation>
    <ns2:YOffset>6470000.0</ns2:YOffset>
    <ns2:ZOffset>-0.0</ns2:ZOffset>
    <ns2:ArealRotation uom="rad">0.0</ns2:ArealRotation>
    <ns2:ProjectedAxisOrder>easting northing</ns2:ProjectedAxisOrder>
    <ns2:ProjectedUom>m</ns2:ProjectedUom>
    <ns2:VerticalUom>m</ns2:VerticalUom>
    <ns2:XOffset>420000.0</ns2:XOffset>
    <ns2:ZIncreasingDownward>true</ns2:ZIncreasingDownward>
    <ns2:VerticalCrs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="{vertical}">
        <EpsgCode>5715</EpsgCode>
    </ns2:VerticalCrs>
    <ns2:ProjectedCrs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="{projected}">
        <EpsgCode>23031</EpsgCode>
    </ns2:ProjectedCrs>
</ns2:LocalDepth3dCrs>
"""

_EML_NS = 'xmlns:eml="http://www.energistics.org/energyml/data/commonv2" '


def _crs_document(vertical: str, projected: str, extra_ns: str = "") -> bytes:
    return _CRS_TEMPLATE.format(vertical=vertical, projected=projected, extra_ns=extra_ns).encode("utf-8")


@pytest.mark.parametrize(
    "vertical,projected,extra_ns",
    [
        # what SKUA-GOCAD and most exporters write: no prefix, default namespace applies
        ("VerticalCrsEpsgCode", "ProjectedCrsEpsgCode", ""),
        # explicitly prefixed, the spelling that already worked
        ("eml:VerticalCrsEpsgCode", "eml:ProjectedCrsEpsgCode", _EML_NS),
    ],
    ids=["unprefixed", "prefixed"],
)
def test_polymorphic_crs_type_is_resolved(vertical, projected, extra_ns):
    crs = read_energyml_xml_bytes(_crs_document(vertical, projected, extra_ns))

    assert type(crs.vertical_crs).__name__ == "VerticalCrsEpsgCode"
    assert type(crs.projected_crs).__name__ == "ProjectedCrsEpsgCode"
    assert crs.vertical_crs.epsg_code == 5715
    assert crs.projected_crs.epsg_code == 23031


def test_undeclared_prefix_still_falls_back():
    # The fallback namespaces are the point of the custom parser: a prefix the document never
    # declares must still resolve when it is a well-known energyml one.
    crs = read_energyml_xml_bytes(_crs_document("eml:VerticalCrsEpsgCode", "eml:ProjectedCrsEpsgCode"))
    assert crs.projected_crs.epsg_code == 23031


def test_epsg_codes_reach_the_crs_info():
    # The reason it matters: without them `to_frame` cannot reach PointFrame.WGS84.
    info = extract_crs_info(read_energyml_xml_bytes(_crs_document("VerticalCrsEpsgCode", "ProjectedCrsEpsgCode")))

    assert info.projected_epsg_code == 23031
    assert info.vertical_epsg_code == 5715
    assert info.x_offset == 420000.0
    assert info.y_offset == 6470000.0
