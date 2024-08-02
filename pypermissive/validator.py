# from pydantic import BaseModel
import typing
from enum import Enum
from typing import List


class BaseModel:
    def __init__(self, **kwargs):
        # valid_attr_types = self.__annotations__  # TODO: rename
        valid_attr_types = typing.get_type_hints(self)
        for key, value in kwargs.items():
            if key not in valid_attr_types:
                raise AttributeError(f"unexpected attribute: {key}")

            actual_type = type(value)
            expected_type = valid_attr_types[key]
            if actual_type is not expected_type:
                # compare list == typing.List
                if actual_type is not typing.get_origin(expected_type):
                    raise ValueError(
                        f"invalid type: {actual_type.__name__}, expected: {expected_type.__name__}"
                    )

            print(f"setting: {key}, type: {actual_type.__name__}, value: {value}")
            setattr(self, key, value)


########################################
class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"


class Hobby:
    name: str


class Employee(BaseModel):
    employee_id: int
    name: str
    salary: float
    department: Department
    elected_benefits: bool = False
    hobbies: List[Hobby]


if __name__ == "__main__":
    employee = Employee(
        employee_id=1,
        name="Chris DeTuma",
        salary=123_000.00,
        department=Department.IT,
        # department=8,
        elected_benefits=True,
        hobbies=["Music", "Cinema"],
        # hobbies=["Music", "Cinema", 3]
        # foo=str
    )

    print(employee.elected_benefits)
