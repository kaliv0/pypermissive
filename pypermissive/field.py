from dataclasses import dataclass


@dataclass(frozen=True)  # ???
class Field:
    value_type: type = None
    # default: value_type = None
    # gt: float | int = None
    # lt: float | int = None
    # ge: float | int = None
    # le: float | int = None
    # max_length: float | int = None
    # min_length: float | int = None
    # pattern: str = None
    # default_factory: Callable = None
    # frozen: bool = False
    # allow_inf_nan: bool = True #???
