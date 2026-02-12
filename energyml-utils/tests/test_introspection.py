# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import energyml.resqml.v2_0_1.resqmlv2
from energyml.eml.v2_0.commonv2 import Citation as Citation20
from energyml.eml.v2_3.commonv2 import Citation
from energyml.resqml.v2_0_1.resqmlv2 import FaultInterpretation
from energyml.resqml.v2_2.resqmlv2 import TriangulatedSetRepresentation
from energyml.opc.opc import Dcmitype1, Contributor

from src.energyml.utils.constants import (
    date_to_epoch,
    pascal_case,
    epoch,
    epoch_to_date,
    snake_case,
)
from src.energyml.utils.introspection import (
    is_primitive,
    is_enum,
    get_class_from_name,
    get_class_from_content_type,
    get_object_attribute,
    set_attribute_from_path,
    copy_attributes,
    get_obj_identifier,
    get_obj_pkg_pkgv_type_uuid_version,
    get_obj_uri,
    gen_uuid,
)


def test_is_primitive():
    assert is_primitive(1)
    assert is_primitive(int)
    assert is_primitive(float)
    assert is_primitive(str)
    assert is_primitive(bool)
    assert is_primitive(type(None))
    assert is_primitive(Dcmitype1)  # Enum is given as primitive
    assert not is_primitive(Contributor)


def test_is_enum():
    assert is_enum(Dcmitype1)
    assert not is_enum(Contributor)
    assert not is_enum(int)


def test_get_class_from_name():
    assert get_class_from_name("energyml.opc.opc.Dcmitype1") == Dcmitype1


def test_snake_case():
    assert snake_case("ThisIsASnakecase") == "this_is_a_snakecase"
    assert snake_case("This_IsASnakecase") == "this_is_a_snakecase"
    assert snake_case("This_isASnakecase") == "this_is_a_snakecase"


def test_pascal_case():
    assert pascal_case("ThisIsASnakecase") == "ThisIsASnakecase"
    assert pascal_case("This_IsASnakecase") == "ThisIsASnakecase"
    assert pascal_case("This_isASnakecase") == "ThisIsASnakecase"
    assert pascal_case("this_is_a_snakecase") == "ThisIsASnakecase"


def test_epoch():
    now = epoch()
    assert date_to_epoch(epoch_to_date(now)) == now


def test_get_class_from_content_type():
    found_type = get_class_from_content_type("resqml20.obj_Grid2dRepresentation")
    assert found_type is not None
    assert found_type == energyml.resqml.v2_0_1.resqmlv2.Grid2DRepresentation


def test_get_object_attribute():
    data = {"a": {"b": ["v_x", {"c": "v_test"}]}}
    assert get_object_attribute(data, "a.b.1.c") == "v_test"


def test_set_attribute_from_path():
    data = {"a": {"b": ["v_x", {"c": "v_test"}]}}
    assert get_object_attribute(data, "a.b.1.c") == "v_test"
    set_attribute_from_path(data, "a.b.1.c", "v_new")
    assert get_object_attribute(data, "a.b.1.c") == "v_new"
    set_attribute_from_path(data, "a", "v_new")
    assert get_object_attribute(data, "a") == "v_new"


def test_copy_attributes_existing_ignore_case():
    data_in = {
        "a": {"b": "v_0", "c": "v_1"},
        "uuid": "215f8219-cabd-4e24-9e4f-e371cabc9622",
        "objectVersion": "Resqml 2.0",
        "non_existing": 42,
    }
    data_out = {
        "a": None,
        "Uuid": "8291afd6-ae01-49f5-bc96-267e7b27450d",
        "object_version": "Resqml 2.0",
    }
    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=True,
        ignore_case=True,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] == data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert "non_existing" not in data_out


def test_copy_attributes_ignore_case():
    data_in = {
        "a": {"b": "v_0", "c": "v_1"},
        "uuid": "215f8219-cabd-4e24-9e4f-e371cabc9622",
        "objectVersion": "Resqml 2.0",
        "non_existing": 42,
    }
    data_out = {
        "a": None,
        "Uuid": "8291afd6-ae01-49f5-bc96-267e7b27450d",
        "object_version": "Resqml 2.0",
    }
    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=False,
        ignore_case=True,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] == data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert data_out["non_existing"] == data_in["non_existing"]


def test_copy_attributes_case_sensitive():
    data_in = {
        "a": {"b": "v_0", "c": "v_1"},
        "uuid": "215f8219-cabd-4e24-9e4f-e371cabc9622",
        "objectVersion": "Resqml 2.0",
        "non_existing": 42,
    }
    data_out = {
        "a": None,
        "Uuid": "8291afd6-ae01-49f5-bc96-267e7b27450d",
        "object_version": "Resqml 2.0",
    }
    copy_attributes(
        obj_in=data_in,
        obj_out=data_out,
        only_existing_attributes=False,
        ignore_case=False,
    )
    assert data_out["a"] == data_in["a"]
    assert data_out["Uuid"] != data_in["uuid"]
    assert data_out["object_version"] == data_in["objectVersion"]
    assert data_out["non_existing"] == data_in["non_existing"]


# Test fixtures for object identifiers and URIs
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
    title="Test TriSet",
    originator="Valentin",
    creation=epoch_to_date(epoch()),
    editor="test",
    format="Geosiris",
    last_update=epoch_to_date(epoch()),
)

tr = TriangulatedSetRepresentation(
    citation=tr_cit,
    uuid=gen_uuid(),
)

tr_versioned = TriangulatedSetRepresentation(
    citation=tr_cit,
    uuid=gen_uuid(),
    object_version="3",
)


def test_get_obj_identifier():
    """Test object identifier generation."""
    assert get_obj_identifier(tr) == tr.uuid + "."
    assert get_obj_identifier(fi) == fi.uuid + ".0"
    assert get_obj_identifier(tr_versioned) == tr_versioned.uuid + ".3"


def test_get_obj_pkg_pkgv_type_uuid_version_obj_201():
    """Test extracting package, version, type, uuid, and version from resqml20 object."""
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
    """Test extracting package, version, type, uuid, and version from resqml22 object."""
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
    """Test URI generation for energyml objects."""
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
