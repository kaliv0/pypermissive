import pytest

from tests.conftest import (
    Department,
    Employee,
    Book,
    Monograph,
    Boy,
    TonalMode,
    Worker,
    Skill,
    Education,
)


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


def test_unexpected_attribute():
    with pytest.raises(AttributeError) as e:
        Employee(foo="bar")
    assert str(e.value) == "unexpected attribute: 'foo'"


def test_default_values():
    employee = Employee(
        employee_id=1,
        name="Foo Bar",
        salary=123_000.00,
        department=Department.IT,
    )
    assert employee.elected_benefits is False


# ### type hints ###
def test_with_type_hints_list():
    boy = Boy(hobbies=["Music", "Books"])
    assert boy.hobbies == ["Music", "Books"]


def test_type_hints_dict():
    book = Book(characters={"good guy": "he", "bad guys": "them"})
    assert book.characters == {"good guy": "he", "bad guys": "them"}


def test_type_hints_set():
    monograph = Monograph(sources={"Wikipedia", "Old books"})
    assert monograph.sources == {"Wikipedia", "Old books"}


def test_type_hints_tuple():
    mode = TonalMode(degrees=(1, 2, 3, 5, 6))
    assert mode.degrees == (1, 2, 3, 5, 6)


def test_invalid_type_hints_type():
    with pytest.raises(ValueError) as e:
        Book(characters=[1, 2, 3, 4])
    assert str(e.value) == "invalid type: 'list', expected: 'dict'"


def test_invalid_type_hints_value_types():
    with pytest.raises(ValueError) as e:
        TonalMode(degrees=("I", "II", "III", "V", "VI"))
    assert str(e.value) == "invalid value type: expected 'tuple[int]'"


# ### union types ###
def test_union_types():
    employee = Employee(
        employee_id=1,
        name="Foo Bar",
        salary=123_000.00,
        department="Sales",
    )
    assert employee.department == "Sales"


def test_invalid_union_types():
    with pytest.raises(ValueError) as e:
        Employee(
            employee_id=1,
            name="Foo Bar",
            salary=123_000.00,
            department=8,
            elected_benefits=True,
        )
    assert str(e.value) == "invalid type: 'int' not in (Department | str)"


# def test_optional():
#     person = Person(name="John Doe")
#     assert person.name == "John Doe"
#     assert person.age is None


# ### nested classes ###
def test_nested_classes():
    worker = Worker(
        skill=Skill(name="Data Science"),
        education=Education(name="PhD", field="AI", institution="MIT"),
    )
    assert worker.skill.name == "Data Science"
    assert worker.education.name == "PhD"
    assert worker.education.field == "AI"
    assert worker.education.institution == "MIT"


def test_nested_classes_union_type():
    worker = Worker(
        skill="Data Science", education=Education(name="PhD", field="AI", institution="MIT")
    )
    assert worker.skill == "Data Science"
    assert worker.education.name == "PhD"
    assert worker.education.field == "AI"
    assert worker.education.institution == "MIT"


def test_nested_classes_invalid_type():
    with pytest.raises(ValueError) as e:
        Worker(skill="Data Science", education=42)
    assert str(e.value) == "invalid type: 'int', expected: 'Education'"
