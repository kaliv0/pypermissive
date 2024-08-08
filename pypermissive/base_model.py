import re
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
                    raise ValueError("missing value type")
                if type(value) is not expected_type.type:
                    raise ValueError(f"invalid value type for '{key}', expected: '{expected_type.type}'")

                # validate numbers
                # TODO: extract expected_type.gt etc
                if expected_type.gt and not (value > expected_type.gt):
                    raise ValueError(f"invalid value: expected '{value}'>'{expected_type.gt}'")

                if expected_type.lt and not (value < expected_type.lt):
                    raise ValueError(f"invalid value: expected '{value}'<'{expected_type.lt}'")

                if expected_type.ge and not (value >= expected_type.ge):
                    raise ValueError(f"invalid value: expected '{value}'>='{expected_type.ge}'")

                if expected_type.le and not (value <= expected_type.le):
                    raise ValueError(f"invalid value: expected '{value}'<='{expected_type.le}'")

                # validate strings
                # length
                if expected_type.length and (len(value) != expected_type.length):
                    # TODO: change error messages
                    raise ValueError(
                        f"invalid value length '{len(value)}': expected '{expected_type.length}' characters"
                    )
                elif expected_type.min_length and (len(value) < expected_type.min_length):
                    raise ValueError(
                        f"invalid value length '{len(value)}': expected no less than '{expected_type.min_length}' characters"
                    )
                elif expected_type.max_length and (len(value) > expected_type.max_length):
                    raise ValueError(
                        f"invalid value length '{len(value)}': expected up to '{expected_type.max_length}' characters"
                    )

                # pattern
                if expected_type.pattern and re.match(expected_type.pattern, value) is None:
                    raise ValueError(
                        f"invalid value '{value}': does not match given pattern '{expected_type.pattern}'"
                    )

                setattr(self, key, value)
                continue
            else:
                # TODO: move error
                raise ValueError(f"invalid type: '{actual_type.__name__}', expected: '{expected_type.__name__}'")

        # set default attributes for fields
        for key, value in valid_attr_types.items():
            if (type(value) is Field) and (value.default is not None) and (hasattr(self, key) is False):
                if type(value.default) is not value.type:
                    # TODO: fix error message?
                    raise TypeError(f"invalid type for default '{key}' value")
                setattr(self, key, value.default)

    ##############################################
    def __setattr__(self, key, value):
        attr_data = typing.get_type_hints(self)[key]
        if type(attr_data) is Field and hasattr(self, key) and attr_data.frozen:
            raise AttributeError(f"field '{key}' is readonly")
        super().__setattr__(key, value)
