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
                if actual_type is dict and (tuple(type(v) for v in value) != expected_type_args):
                    dict_message = ", ".join([arg.__name__ for arg in expected_type_args])
                    raise ValueError(f"invalid value types inside dict: expected '({dict_message})'")

                # validate other collections
                if any([type(v) is not expected_type_args[0] for v in value]):
                    raise ValueError(f"invalid value type: expected '{expected_type}'")

                setattr(self, key, value)
                continue

            # union types
            if expected_type_origin is types.UnionType:
                if actual_type not in expected_type_args:
                    union_message = " | ".join([arg.__name__ for arg in expected_type_args])
                    raise ValueError(f"invalid type: '{actual_type.__name__}' not in '({union_message})'")

                setattr(self, key, value)
                continue

            # field types
            if type(valid_attr_types.get(key, None)) is Field:
                if expected_type.type is None:
                    raise ValueError("missing value type'")

                if type(value) is not expected_type.type:
                    raise ValueError(f"invalid value type for '{key}', expected: '{expected_type.type}'")
                # TODO: extract expected_type.gt etc
                if expected_type.gt and not (value > expected_type.gt):
                    raise ValueError(f"invalid value: expected '{value}'>'{expected_type.gt}'")

                if expected_type.lt and not (value < expected_type.lt):
                    raise ValueError(f"invalid value: expected '{value}'<'{expected_type.lt}'")

                if expected_type.ge and not (value >= expected_type.ge):
                    raise ValueError(f"invalid value: expected '{value}'>='{expected_type.ge}'")

                if expected_type.le and not (value <= expected_type.le):
                    raise ValueError(f"invalid value: expected '{value}'<='{expected_type.le}'")

                setattr(self, key, value)
                continue

            # TODO: move error
            raise ValueError(f"invalid type: '{actual_type.__name__}', expected: '{expected_type.__name__}'")
