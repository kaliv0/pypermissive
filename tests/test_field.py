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


def test_lt():
    teen = Teenager(name="John Doe", age=12)
    assert teen.age == 12


def test_invalid_lt():
    with pytest.raises(ValueError) as e:
        Teenager(name="John Doe", age=23)
    assert str(e.value) == "invalid value: expected '23'<'20'"


def test_ge():
    teen_1 = Teenager(name="John Doe", age=10, school_grade=5)
    teen_2 = Teenager(name="Joe Dow", age=15, school_grade=9)
    assert teen_1.school_grade == 5
    assert teen_2.school_grade == 9


def test_invalid_ge():
    with pytest.raises(ValueError) as e:
        Teenager(name="John Doe", age=11, school_grade=2)
    assert str(e.value) == "invalid value: expected '2'>='5'"


def test_le():
    teen_1 = Teenager(name="John Doe", age=15, school_grade=9)
    teen_2 = Teenager(name="Joe Dow", age=18, school_grade=12)
    assert teen_1.school_grade == 9
    assert teen_2.school_grade == 12


def test_invalid_le():
    with pytest.raises(ValueError) as e:
        Teenager(name="John Doe", age=19, school_grade=13)
    assert str(e.value) == "invalid value: expected '13'<='12'"
