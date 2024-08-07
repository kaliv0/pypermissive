from enum import Enum
from typing import List

# from pydantic import BaseModel
from pypermissive.base_model import BaseModel
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


#########################
class Teenager(BaseModel):
    name: Field(
        type=str,
    ) = "Jimmie"  # TODO: refactor

    age: Field(type=int, gt=9, lt=20)
    school_grade: Field(type=int, ge=5, le=12)
