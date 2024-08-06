# from pydantic import BaseModel
import types
import typing

from pypermissive.field import Field


class BaseModel:
    def __init__(self, **kwargs):
        valid_attr_types = typing.get_type_hints(self)
        for key, value in kwargs.items():
            if key not in valid_attr_types:
                raise AttributeError(f"unexpected attribute: '{key}'")

            actual_type = type(value)
            expected_type = valid_attr_types[key]
            # primitive types
            if actual_type is expected_type:
                setattr(self, key, value)
                continue

            expected_type_args = typing.get_args(expected_type)
            expected_type_origin = typing.get_origin(expected_type)
            # compare against type hints
            if actual_type is expected_type_origin:
                # validate dict[str, str]
                if actual_type is dict:
                    if tuple(type(v) for v in value) == expected_type_args:
                        setattr(self, key, value)
                        continue
                # validate other collections
                if all([type(v) is expected_type_args[0] for v in value]):
                    setattr(self, key, value)
                    continue
                else:
                    raise ValueError(f"invalid value type: expected '{expected_type}'")

            # union types
            if expected_type_origin is types.UnionType:
                if actual_type in expected_type_args:
                    setattr(self, key, value)
                    continue

                union_message = " | ".join([arg.__name__ for arg in expected_type_args])
                raise ValueError(f"invalid type: '{actual_type.__name__}' not in ({union_message})")

            if type(valid_attr_types.get(key, None)) is Field:
                if expected_type.type is None:
                    raise ValueError("missing value type'")

                if type(value) is not expected_type.type:
                    raise ValueError(
                        f"invalid value type for '{key}', expected: '{expected_type.type}'"
                    )

                if expected_type.gt and not (value > expected_type.gt):
                    raise ValueError(f"invalid value: expected '{value}'>'{expected_type.gt}'")

                setattr(self, key, value)
                continue

            # TODO: move error
            raise ValueError(
                f"invalid type: '{actual_type.__name__}', expected: '{expected_type.__name__}'"
            )
