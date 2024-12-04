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
#  Enforce method signatures -> more tests, check subtypes
#  Require interface methods to be empty/abstract/pass-only


class Interface:
    def __init__(self, *klass):
        self.required_methods = self.get_methods(*klass)

    # NB: fails at class-definition level
    def __call__(self, klass):
        missing_methods = []
        invalid_signature_methods = []
        klass_methods = self.get_methods(klass)
        for name, func in self.required_methods.items():
            if name not in klass_methods.keys():
                missing_methods.append(name)
            if not (curr_method := klass_methods.get(name, None)) or inspect.signature(func) != inspect.signature(
                curr_method
            ):
                invalid_signature_methods.append(name)

        if missing_methods:
            raise InterfaceError(f"Missing required methods: '{', '.join(name for name in missing_methods)}'")
        if invalid_signature_methods:
            raise InterfaceError(
                f"Methods with invalid signature: '{', '.join(name for name in invalid_signature_methods)}'"
            )

        class DuckType(*klass.__bases__):
            def __init__(self, *args, **kwargs) -> None:
                self._origin = klass(*args, **kwargs)

            # TODO: getattribute or getattr?
            def __getattribute__(self, attr):
                try:
                    return super().__getattribute__(attr)
                except AttributeError:
                    return self._origin.__getattribute__(attr)

            # TODO: refactor
            def __setattr__(self, attr, value):
                try:
                    return super().__setattr__(attr, value)
                except AttributeError:
                    return self._origin.__setattr__(attr, value)

            # TODO: can we doo any magic with repr, str etc to keep the original class name (when using inheritance)?
            def __repr__(self):
                return self._origin.__repr__()

            def __str__(self):
                return self._origin.__str__()  # TODO: do we need this?

        return DuckType

    @staticmethod
    def get_methods(*klass):
        return {
            func[0]: func[1]
            for kl in klass
            for func in inspect.getmembers(kl, inspect.isfunction)
            if not func[0].startswith("_")  # TODO: support public methods only (?)
        }

    # TODO: NB: if you put decorator on a parent and same decorator on a child that inherits from the parent you get an error
