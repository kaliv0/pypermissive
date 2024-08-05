import typing
import pytest

from tests.conftest import Child


def test_value_type():
    child = Child(name="John Doe")
    assert child.name == "John Doe"
    assert typing.get_type_hints(Child).get("name").value_type is str


def test_invalid_type():
    with pytest.raises(ValueError) as e:
        Child(name=1234)
    assert str(e.value) == "invalid field: expected 'Field(value_type=<class 'str'>)'"
