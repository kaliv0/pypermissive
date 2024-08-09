import re
import types
import typing

from pypermissive import Field


class BaseModel:
    def __init__(self, **kwargs):
        valid_attr_types = typing.get_type_hints(self)
        self._validate_and_set_attributes(valid_attr_types, **kwargs)
        self._set_default_field_attributes(valid_attr_types)

    ##############################################
    def _validate_and_set_attributes(self, valid_attr_types, **kwargs):
        for key, value in kwargs.items():
            if key not in valid_attr_types:
                raise AttributeError(f"unexpected attribute: '{key}'")

            actual_type = type(value)
            expected_type = valid_attr_types[key]
            expected_type_args = typing.get_args(expected_type)
            expected_type_origin = typing.get_origin(expected_type)
            if (
                self._is_valid_primitive_type(actual_type, expected_type)
                or self._is_valid_collection(
                    value, actual_type, expected_type, expected_type_args, expected_type_origin
                )
                or self._is_valid_union_type(actual_type, expected_type_args, expected_type_origin)
                or self._is_valid_field_type(key, value, expected_type, valid_attr_types)
            ):
                setattr(self, key, value)
                continue
            raise TypeError(f"invalid type: '{actual_type.__name__}', expected: '{expected_type.__name__}'")

    @staticmethod
    def _is_valid_primitive_type(actual_type, expected_type):
        return actual_type is expected_type

    @staticmethod
    def _is_valid_collection(value, actual_type, expected_type, expected_type_args, expected_type_origin):
        if actual_type is not expected_type_origin:
            return False

        if actual_type is dict and (tuple(type(v) for v in value) != expected_type_args):
            dict_message = ", ".join([arg.__name__ for arg in expected_type_args])
            raise TypeError(f"invalid value types inside dict: expected '({dict_message})'")
        # validate other collections
        if any([type(v) is not expected_type_args[0] for v in value]):
            raise TypeError(f"invalid value type: expected '{expected_type}'")
        return True

    @staticmethod
    def _is_valid_union_type(actual_type, expected_type_args, expected_type_origin):
        if expected_type_origin is not types.UnionType:
            return False

        if actual_type not in expected_type_args:
            union_message = " | ".join([arg.__name__ for arg in expected_type_args])
            raise TypeError(f"invalid type: '{actual_type.__name__}' not in '({union_message})'")
        return True

    def _is_valid_field_type(self, key, value, expected_type, valid_attr_types):
        if type(valid_attr_types.get(key, None)) is not Field:
            return False

        self._validate_type(key, value, expected_type)
        if self._is_valid_against_user_defined_function(key, value, expected_type):
            return True

        self._validate_number(value, expected_type)
        self._validate_string(value, expected_type)
        return True

    @staticmethod
    def _validate_type(key, value, expected_type):
        if expected_type.type is None:
            raise TypeError("missing value type")
        if type(value) is not expected_type.type:
            raise TypeError(f"invalid value type for '{key}', expected: '{expected_type.type.__name__}'")

    @staticmethod
    def _is_valid_against_user_defined_function(key, value, expected_type):
        if expected_type.field_validator is None:
            return False

        if expected_type.field_validator(value) is False:
            raise ValueError(f"invalid value '{value}' for '{key}'")
        return True

    @staticmethod
    def _validate_number(value, expected_type):
        if expected_type.gt and not (value > expected_type.gt):
            raise ValueError(f"invalid value: expected '{value}'>'{expected_type.gt}'")
        if expected_type.lt and not (value < expected_type.lt):
            raise ValueError(f"invalid value: expected '{value}'<'{expected_type.lt}'")
        if expected_type.ge and not (value >= expected_type.ge):
            raise ValueError(f"invalid value: expected '{value}'>='{expected_type.ge}'")
        if expected_type.le and not (value <= expected_type.le):
            raise ValueError(f"invalid value: expected '{value}'<='{expected_type.le}'")

    def _validate_string(self, value, expected_type):
        self._validate_string_length(value, expected_type)
        self._validate_string_pattern(value, expected_type)

    @staticmethod
    def _validate_string_length(value, expected_type):
        if expected_type.length and (len(value) != expected_type.length):
            raise ValueError(f"invalid value length '{len(value)}': expected '{expected_type.length}' characters")
        if expected_type.min_length and (len(value) < expected_type.min_length):
            raise ValueError(
                f"invalid value length '{len(value)}': expected no less than '{expected_type.min_length}' characters"
            )
        if expected_type.max_length and (len(value) > expected_type.max_length):
            raise ValueError(
                f"invalid value length '{len(value)}': expected up to '{expected_type.max_length}' characters"
            )

    @staticmethod
    def _validate_string_pattern(value, expected_type):
        if expected_type.pattern and re.match(expected_type.pattern, value) is None:
            raise ValueError(f"invalid value '{value}': does not match given pattern '{expected_type.pattern}'")

    def _set_default_field_attributes(self, valid_attr_types):
        for key, value in valid_attr_types.items():
            if type(value) is Field and hasattr(self, key) is False:
                self._set_value(key, value)

    def _set_value(self, key, value):
        if value.default:
            if type(value.default) is not value.type:
                raise TypeError(f"invalid type for default '{key}' value: expected: '{value.type.__name__}'")
            return setattr(self, key, value.default)
        if value.default_factory:
            created_value = value.default_factory()
            if type(created_value) is not value.type:
                raise TypeError(f"invalid type for created '{key}' value")
            return setattr(self, key, created_value)

    ##############################################
    def __setattr__(self, key, value):
        attr_data = typing.get_type_hints(self)[key]
        if type(attr_data) is Field and hasattr(self, key) and attr_data.frozen:
            raise AttributeError(f"field '{key}' is readonly")
        super().__setattr__(key, value)
