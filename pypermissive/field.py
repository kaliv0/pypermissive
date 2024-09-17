from collections.abc import Callable
from typing import Any
from dataclasses import dataclass


@dataclass
class Field:
    type: Any = None
    default: Any = None
    frozen: bool | None = False
    gt: float | int | None = None
    lt: float | int | None = None
    ge: float | int | None = None
    le: float | int | None = None
    length: int | None = None
    max_length: int | None = None
    min_length: int | None = None
    pattern: str | None = None
    default_factory: Callable[..., Any] | None = None
    field_validator: Callable[..., bool] | None = None
