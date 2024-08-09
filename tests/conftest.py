import itertools
import random
from enum import Enum
from typing import List
from uuid import UUID, uuid4

# from pydantic import BaseModel
from pypermissive.base_model import BaseModel
from pypermissive.decorators import ComputedField, ComputedClassField, validate_call
from pypermissive.field import Field


class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"


class Employee(BaseModel):
    employee_id: int
    name: str
    salary: float
    department: Department | str
    elected_benefits: bool = False


class Boy(BaseModel):
    hobbies: List[str] = ["Football"]


class Education(BaseModel):
    name: str
    field: str
    institution: str


class Skill(BaseModel):
    name: str


class Worker(BaseModel):
    education: Education
    skill: Skill | str


# class Person(BaseModel):
#     name: str
#     # age: Optional[int]
#     # age: Union[int, None]


class Book(BaseModel):
    characters: dict[str, str]


class Monograph(BaseModel):
    sources: set[str]


class TonalMode(BaseModel):
    degrees: tuple[int]


# ### Fields ###
class Teenager(BaseModel):
    name: Field(type=str, default="Jimmie")

    age: Field(type=int, gt=9, lt=20)
    school_grade: Field(type=int, ge=5, le=12)


class Foo(BaseModel):
    bar: Field()


class Fizz(BaseModel):
    buzz: Field(type=int, default="bazz")


class Profile(BaseModel):
    nickname: Field(type=str, min_length=3, max_length=15, frozen=True)
    PIN: Field(type=str, length=6)
    email: Field(type=str, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[.][a-zA-Z0-9-.]+$")


class User(BaseModel):
    id: Field(type=UUID, default_factory=uuid4)


class ShadyUser(BaseModel):
    id: Field(type=UUID, default_factory=random.random)


class StrictUser(BaseModel):
    PIN: Field(type=str, field_validator=lambda x: x.isdigit())


# ### ComputedFields ###
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


# ### validate_call ###
@validate_call
def some_func(delimiter: str, count: int, mode: TonalMode) -> str:
    return (delimiter * count).join([str(d) for d in mode.degrees])
