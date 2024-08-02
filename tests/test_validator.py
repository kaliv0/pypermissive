import pytest

from tests.conftest import Department, Employee


def test_basic_validation():
    employee = Employee(
        employee_id=1,
        name="Foo Bar",
        salary=123_000.00,
        department=Department.IT,
        elected_benefits=True,
    )
    assert employee.employee_id == 1
    assert employee.name == "Foo Bar"
    assert employee.salary == 123_000.00
    assert employee.department == Department.IT
    assert employee.elected_benefits is True


def test_invalid_type():
    with pytest.raises(ValueError) as e:
        Employee(
            employee_id="1",
            name="Foo Bar",
            salary=123_000.00,
            department=Department.IT,
            elected_benefits=True,
        )
    assert str(e.value) == "invalid type: 'str', expected: 'int'"


def test_default_values():
    employee = Employee(
        employee_id=1,
        name="Foo Bar",
        salary=123_000.00,
        department=Department.IT,
    )
    assert employee.elected_benefits is False


def test_with_type_hints():
    employee = Employee(
        employee_id=1,
        name="Foo Bar",
        salary=123_000.00,
        department=Department.IT,
        elected_benefits=True,
        hobbies=["Music", "Books"],
    )
    assert employee.employee_id == 1
    assert employee.name == "Foo Bar"
    assert employee.salary == 123_000.00
    assert employee.department == Department.IT
    assert employee.elected_benefits is True
    assert employee.hobbies == ["Music", "Books"]


def test_union_types():
    employee = Employee(
        employee_id=1,
        name=None,
        salary=123_000.00,
        department=Department.IT,
    )
    assert employee.elected_benefits is False


def test_invalid_union_types():
    with pytest.raises(ValueError) as e:
        Employee(
            employee_id=1,
            name=42,
            salary=123_000.00,
            department=Department.IT,
            elected_benefits=True,
        )
    assert str(e.value) == "invalid type: 'int' not in (str | None)"
