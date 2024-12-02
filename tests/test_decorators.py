import pytest

from pypermissive import validate_call
from pypermissive.decorators import InterfaceError, Interface
from .conftest import (
    Thesis,
    TonalMode,
    some_func,
    Barsome,
    MyInterface,
    Child,
    Parent,
    Girl,
    GrandDaughter,
    Woman,
    Frankenstein,
)
from .util import not_raises


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
        some_func("*", "2", mode)  # noqa
    assert str(e.value) == "invalid value type for parameter 'count': expected 'int'"


def test_validate_call_invalid_field_type():
    with pytest.raises(TypeError) as e:
        some_func("*", 2, [1, 2, 3, 4])  # noqa
    assert str(e.value) == "invalid value type for parameter 'mode': expected 'TonalMode'"


def test_validate_call_invalid_return_type():
    @validate_call
    def foo(x: str, y: str) -> int:
        return x + y  # noqa

    with pytest.raises(TypeError) as e:
        foo("42", "xxx")
    assert str(e.value) == "invalid return type: expected 'int'"


# ### interfaces ###
def test_interface():
    with not_raises(InterfaceError):
        b = Barsome()
    b.bar()  # TODO: assert


def test_interface_raises():
    with pytest.raises(InterfaceError, match="Missing required methods: 'bar'"):

        @Interface(MyInterface)
        class Barless:
            def baz(self): ...


def test_interface_correct_type():
    bar = Barsome()
    assert isinstance(bar, Barsome)
    assert isinstance(bar, MyInterface) is False
    assert type(bar) is Barsome  # TODO: ??
    assert type(bar) is not MyInterface


def test_interface_inheritance():
    concrete = Child()
    assert isinstance(concrete, Child)
    assert isinstance(concrete, Parent)
    assert not isinstance(concrete, MyInterface)

    assert issubclass(Child, Parent)
    assert not issubclass(Child, MyInterface)
    assert type(Child) is not MyInterface


def test_interface_multiple_inheritance():
    joujou = GrandDaughter()
    assert isinstance(joujou, GrandDaughter)
    assert isinstance(joujou, Girl)
    assert isinstance(joujou, Woman)
    assert not isinstance(joujou, MyInterface)

    assert issubclass(GrandDaughter, Girl)
    assert not issubclass(Girl, MyInterface)
    assert type(Girl) is not MyInterface
    # TODO: test actual methods
    # joujou.fizz()
    # joujou.buzz()
    # joujou.bar()


def test_stacking_interfaces():
    with not_raises(InterfaceError):
        f = Frankenstein()
    f.bar()  # TODO: not showing by the LSP
    f.moo()
