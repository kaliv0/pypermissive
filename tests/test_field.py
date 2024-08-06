import typing
import pytest

from tests.conftest import Teenager


def test_value_type():
    teen = Teenager(name="John Doe")
    assert teen.name == "John Doe"
    assert typing.get_type_hints(Teenager).get("name").type is str


def test_invalid_type():
    with pytest.raises(ValueError) as e:
        Teenager(name=1234)
    assert str(e.value) == "invalid value type for 'name', expected: '<class 'str'>'"


def test_default_value():
    teen = Teenager()
    assert teen.name == "Jimmie"
    assert typing.get_type_hints(Teenager).get("name").type is str


def test_gt():
    teen = Teenager(name="John Doe", age=12)
    assert teen.age == 12


def test_invalid_gt():
    with pytest.raises(ValueError) as e:
        Teenager(name="John Doe", age=8)
    assert str(e.value) == "invalid value: expected '8'>'9'"
