# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
import energyml.resqml.v2_0_1.resqmlv2
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
)


def test_is_primitive():
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
    found_type = get_class_from_content_type(
        "resqml20.obj_Grid2dRepresentation"
    )
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
