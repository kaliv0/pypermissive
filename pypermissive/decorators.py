class ComputedClassField:
    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__

    def __get__(self, instance, owner):
        if owner is None:
            return None
        result = self._func(owner)
        setattr(owner, self.__name__, result)
        return result


class ComputedField(ComputedClassField):
    def __get__(self, instance, owner):
        if instance is None:
            return None
        result = self._func(instance)
        setattr(instance, self.__name__, result)
        return result


##############################################
def validate_call(func):
    from functools import wraps
    import inspect

    @wraps(func)
    def wrapper(*args, **kwargs):
        signature_args = inspect.get_annotations(func)
        return_type = signature_args.pop("return", None)
        call_params = inspect.getcallargs(func, *args, **kwargs)
        for name, value_type in signature_args.items():
            if type(call_params[name]) is not value_type:
                raise TypeError(f"invalid value type for parameter '{name}': expected '{value_type.__name__}'")

        result = func(*args, **kwargs)
        if return_type and type(result) is not return_type:
            raise TypeError(f"invalid return type: expected '{return_type.__name__}'")
        return result

    return wrapper
