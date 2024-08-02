# from pydantic import BaseModel
import types
import typing


class BaseModel:
    def __init__(self, **kwargs):
        valid_attr_types = typing.get_type_hints(self)
        for key, value in kwargs.items():
            if key not in valid_attr_types:
                raise AttributeError(f"unexpected attribute: '{key}'")

            actual_type = type(value)
            expected_type = valid_attr_types[key]
            if actual_type is not expected_type:
                # compare against type hints
                if actual_type is not typing.get_origin(expected_type):
                    # str == str|None
                    if typing.get_origin(expected_type) is types.UnionType:
                        if actual_type not in typing.get_args(expected_type):
                            raise ValueError(
                                f"invalid type: '{actual_type.__name__}' not in ({expected_type})"
                            )

                    else:
                        # TODO: move error
                        raise ValueError(
                            f"invalid type: '{actual_type.__name__}', expected: '{expected_type.__name__}'"
                        )
            setattr(self, key, value)
