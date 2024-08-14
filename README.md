<p align="center">
  <img src="https://github.com/kaliv0/pypermissive/blob/main/permissive.jpg?raw=true" alt="Permissive Path">
</p>

---

# PyPermissive

[![tests](https://img.shields.io/github/actions/workflow/status/kaliv0/pypermissive/ci.yml)](https://github.com/kaliv0/pypermissive/actions/workflows/ci.yml)
![Python 3.x](https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=Python&logoColor=white)
[![PyPI](https://img.shields.io/pypi/v/pypermissive.svg)](https://pypi.org/project/pypermissive/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/kaliv0/pypermissive/blob/main/LICENSE)

Validation library in Python, modeled after Pydantic

## Example

Inherit from BaseModel and describe required types.<br>
<i>PyPermissive</i> supports validation for primitive types:
```python
class Employee(BaseModel):
    employee_id: int
    name: str
    salary: float
    elected_benefits: bool = False
    
employee = Employee(
    employee_id=1,
    name="Foo Bar",
    salary=123_000.00,
    elected_benefits=True,
)
```

collections:
```python
class Book(BaseModel):
    characters: dict[str, str]
    chapters: list[str]
    
book = Book(
    characters={"Pelleas": "he", "Melisande": "she"},
    chapters=["Beginning", "Middle", "End"]
)
```

unions, classes and fields.<br>
<br>Fields are similar to <i>pydantic</i> with one caveat: you need to give value type explicitly:

```python
class User(BaseModel):
    name: Field(type=str, default="Jimmie", frozen=True)
    age: Field(type=int, gt=18, lt=35)
    id: Field(type=UUID, default_factory=uuid4)
    email: Field(type=str, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[.][a-zA-Z0-9-.]+$")
    nickname: Field(type=str, min_length=6, max_length=12)
    PIN: Field(type=str, field_validator=lambda x: x.isdigit())

```

You can also use decorators:<br>
@ComputedField (invoke only from instances) and @ComputedClassField (invoke both on class and instance level)
```python
class Thesis:
    BAZZ = ["1", "2", "3"]

    def __init__(self):
        self.fizz = [1, 2, 3, 4, 5]
        self.buzz = [6, 7, 8, 9]

    @ComputedField
    def foo(self):
        return [val for val in itertools.product(self.fizz, self.buzz)]

    @ComputedClassField
    def bar(self):
        return list(itertools.permutations(self.BAZZ))

    
```

The library supports @validate_call that checks both argument and return types:
```python
@validate_call
def some_func(delimiter: str, count: int, numbers: list[int]) -> str:
    return (delimiter * count).join([str(d) for d in numbers])
```