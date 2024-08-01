# from pydantic import BaseModel
from enum import Enum


class BaseModel:
    def __init__(self, **kwargs):
        types = self.__annotations__
        for k, v in kwargs.items():
            if k not in types:
                raise AttributeError(f"unexpected attribute: {k}")

            if type(v) is not types[k]:
                raise ValueError(f"invalid type: {type(v).__name__}, expected: {types[k].__name__}")

            print(f"setting: {k}, type: {type(v).__name__}, value: {v}")
            setattr(self, k, v)


########################################
class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"


class Employee(BaseModel):
    employee_id: int
    name: str
    salary: float
    department: Department
    elected_benefits: bool


if __name__ == "__main__":
    employee = Employee(
        employee_id=1,
        name="Chris DeTuma",
        salary=123_000.00,
        department=Department.IT,
        # department=8,
        elected_benefits=True,
        # foo=str
    )
