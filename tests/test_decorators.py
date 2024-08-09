import pytest

from pypermissive import validate_call
from .conftest import Thesis, some_func, TonalMode


def test_computed_field():
    thesis = Thesis()
    assert thesis.foo == [
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (2, 6),
        (2, 7),
        (2, 8),
        (2, 9),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (4, 6),
        (4, 7),
        (4, 8),
        (4, 9),
        (5, 6),
        (5, 7),
        (5, 8),
        (5, 9),
    ]


def test_computed_field_on_none_instance():
    assert Thesis.foo is None


def test_computed_class_field():
    assert Thesis.bar == [
        ("1", "2", "3"),
        ("1", "3", "2"),
        ("2", "1", "3"),
        ("2", "3", "1"),
        ("3", "1", "2"),
        ("3", "2", "1"),
    ]


def test_computed_class_field_called_from_instance():
    thesis = Thesis()
    assert thesis.bar == [
        ("1", "2", "3"),
        ("1", "3", "2"),
        ("2", "1", "3"),
        ("2", "3", "1"),
        ("3", "1", "2"),
        ("3", "2", "1"),
    ]


# ### validate_function_calls ###
def test_validate_call():
    mode = TonalMode(degrees=(1, 2, 3, 5, 6))
    assert some_func("_", 2, mode) == "1__2__3__5__6"


def test_validate_call_invalid_type():
    mode = TonalMode(degrees=(1, 2, 3, 5, 6))
    with pytest.raises(TypeError) as e:
        some_func("*", "2", mode)
    assert str(e.value) == "invalid value type for parameter 'count': expected 'int'"


def test_validate_call_invalid_field_type():
    with pytest.raises(TypeError) as e:
        some_func("*", 2, [1, 2, 3, 4])
    assert str(e.value) == "invalid value type for parameter 'mode': expected 'TonalMode'"


def test_validate_call_invalid_return_type():
    @validate_call
    def foo(x: str, y: str) -> int:
        return x + y

    with pytest.raises(TypeError) as e:
        foo("42", "xxx")
    assert str(e.value) == "invalid return type: expected 'int'"
