import itertools
import random
from enum import Enum
from uuid import UUID, uuid4

from pypermissive import BaseModel, Field, ComputedField, ComputedClassField, validate_call
from pypermissive.decorators import Interface


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
    hobbies: list[str] = ["Football"]


class Education(BaseModel):
    name: str
    field: str
    institution: str


class Skill(BaseModel):
    name: str


class Worker(BaseModel):
    education: Education
    skill: Skill | str


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


# ### interfaces ###
class MyInterface:
    def bar(self): ...


@Interface(MyInterface)
class Barsome:
    def bar(self):
        return f"{self.__class__.__name__}:bar"


# single inheritance
class Parent:
    val = 1

    def abs(self):
        return f"{self.__class__.__name__}:abs-> {self.val}"


@Interface(MyInterface)
class Child(Parent):
    def bar(self):
        return f"{self.__class__.__name__}:bar"


# multiple inheritance
class Woman:
    const = 1

    def fizz(self):
        return f"{self.__class__.__name__}:fizz-> {self.const}"


class Girl:
    val = 2

    def buzz(self):
        return f"{self.__class__.__name__}:buzz-> {self.val}"


@Interface(MyInterface)
class GrandDaughter(Woman, Girl):
    var = 3

    def total(self):
        return f"{self.__class__.__name__}:total-> {self.const}, {self.val}, {self.var}"

    def bar(self):
        return f"{self.__class__.__name__}:bar"


# multiple interfaces
class OtherInterface:
    def moo(self): ...


@Interface(MyInterface, OtherInterface)
class Frankenstein:
    def __init__(self, val=None):
        self.val = val

    def bar(self):
        return f"{self.__class__.__name__}:bar"

    def moo(self):
        return f"{self.__class__.__name__}:moo"


# interface signature
class SimpleSignature:
    @staticmethod
    def abc(x: int, y: int) -> int: ...


@Interface(SimpleSignature)
class ClassWithSignature:
    @staticmethod
    def abc(x: int, y: int) -> int:
        return x + y
