from enum import Enum
from typing import List

from pypermissive.validator import BaseModel


class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"


class Hobby:
    name: str


class Employee(BaseModel):
    employee_id: int
    name: str | None
    salary: float
    department: Department
    elected_benefits: bool = False
    hobbies: List[Hobby] = []
