# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

from energyml.opc.opc import (
    Dcmitype1,
    Contributor
)

from src.energyml.utils.introspection import (
    is_primitive, is_enum, get_class_from_name,
    snake_case, pascal_case
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
