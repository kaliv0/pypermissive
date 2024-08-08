from typing import Any, Callable
from dataclasses import dataclass


@dataclass  # or simple class with __slots__?
class Field:
    type: Any = None  # rename to value_type
    default: Any = None
    gt: float | int = None
    lt: float | int = None
    ge: float | int = None
    le: float | int = None
    length: int = None
    max_length: int = None
    min_length: int = None
    pattern: str = None
    default_factory: Callable = None
    frozen: bool = False
