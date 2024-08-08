import typing
from uuid import UUID

import pytest

from .conftest import Teenager, Foo, Profile, Fizz, User, ShadyUser


def test_value_type():
    teen = Teenager(name="John Doe")
    assert teen.name == "John Doe"
    assert typing.get_type_hints(Teenager).get("name").type is str


def test_invalid_type():
    with pytest.raises(ValueError) as e:
        Teenager(name=1234)
    assert str(e.value) == "invalid value type for 'name', expected: 'str'"


def test_missing_value_type():
    with pytest.raises(ValueError) as e:
        Foo(bar=42)
    assert str(e.value) == "missing value type"


def test_default_value():
    teen = Teenager()
    assert teen.name == "Jimmie"
    assert typing.get_type_hints(Teenager).get("name").type is str


def test_invalid_default_value_type():
    with pytest.raises(TypeError) as e:
        Fizz()
    assert str(e.value) == "invalid type for default 'buzz' value: expected: 'int'"


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


def test_min_length():
    profile = Profile(nickname="HIM")
    assert profile.nickname == "HIM"


def test_invalid_min_length():
    with pytest.raises(ValueError) as e:
        Profile(nickname="XY")
    assert str(e.value) == "invalid value length '2': expected no less than '3' characters"


def test_max_length():
    profile = Profile(nickname="Rambhadracharya")
    assert profile.nickname == "Rambhadracharya"


def test_invalid_max_length():
    with pytest.raises(ValueError) as e:
        Profile(nickname="Rambhadracharyakurukshetraindrarashtra")
    assert str(e.value) == "invalid value length '38': expected up to '15' characters"


def test_length():
    profile = Profile(nickname="Him", PIN="123456")
    assert profile.PIN == "123456"


def test_invalid_length():
    with pytest.raises(ValueError) as e:
        Profile(nickname="Sinbad", PIN="1234")
    assert str(e.value) == "invalid value length '4': expected '6' characters"


def test_frozen_field():
    profile = Profile(nickname="Foo")
    with pytest.raises(AttributeError) as e:
        profile.nickname = "Bar"
    assert str(e.value) == "field 'nickname' is readonly"


def test_regex_pattern():
    profile = Profile(nickname="Fat Joe", PIN="123456", email="fat-joe82@gmail.com")
    assert profile.email == "fat-joe82@gmail.com"


def test_invalid_pattern():
    with pytest.raises(ValueError) as e:
        Profile(nickname="Fat Joe", PIN="123456", email="fat-joe82@gmail")
    assert (
        str(e.value)
        == "invalid value 'fat-joe82@gmail': does not match given pattern '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[.][a-zA-Z0-9-.]+$'"
    )


def test_default_factory():
    user = User()
    assert type(user.id) is UUID


def test_invalid_default_factory_result_type():
    with pytest.raises(TypeError) as e:
        ShadyUser()
    assert str(e.value) == "invalid type for created 'id' value"
