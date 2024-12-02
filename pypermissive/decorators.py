import inspect  # TODO: top level?


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


##############################################
class InterfaceError(Exception):
    pass


# TODO:
#  Support dunder methods??
#  Enforce method signatures
#  Require interface methods to be empty/abstract/pass-only


class Interface:
    def __init__(self, *klass):
        self.required_methods = self.get_methods(*klass)

    # TODO: fails at class-definition level long before any instantiation
    def __call__(self, klass):
        missing_methods = [func for func in self.required_methods if func not in self.get_methods(klass)]
        if missing_methods:
            raise InterfaceError(f"Missing required methods: '{', '.join(func for func in missing_methods)}'")

        class DuckType(*klass.__bases__):
            def __init__(self, *args, **kwargs) -> None:
                self._origin = klass(*args, **kwargs)

            def __getattribute__(self, attr):
                try:
                    return super().__getattribute__(attr)
                except AttributeError:
                    return self._origin.__getattribute__(attr)

        return DuckType

    @staticmethod
    def get_methods(*klass):
        # TODO: extracting only function names for now
        return [
            func[0]
            for kl in klass
            for func in inspect.getmembers(kl, inspect.isfunction)
            if not func[0].startswith("__")
        ]

    # TODO: NB: if you put decorator on a parent and same decorator on a child that inherits from the parent you get an error
