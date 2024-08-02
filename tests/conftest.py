from enum import Enum
from typing import List

# from pydantic import BaseModel
from pypermissive.validator import BaseModel


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
    hobbies: List[str] = []


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
