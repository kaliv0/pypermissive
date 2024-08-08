from tests.conftest import Thesis


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
