import typing
from dataclasses import dataclass


@dataclass(frozen=True)  # or simple class with __slots__?
class Field:
    type: typing.Any = None  # rename to value_type
    # default: typing.Any = None  # TODO: set outside of validation block
    gt: float | int = None
    lt: float | int = None
    ge: float | int = None
    le: float | int = None
    # max_length: int = None
    # min_length: int = None
    # pattern: str = None
    # default_factory: Callable = None
    # frozen: bool = False
