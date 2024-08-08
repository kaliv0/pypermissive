# works only on instances
class ComputedField:
    def __init__(self, func):
        self.__func = func
        self.__name__ = func.__name__
        # self.__doc__ == func.__doc__ #??

    def __get__(self, instance, owner):
        if instance is None:
            return None
        result = instance.__dict__[self.__name__] = self.__func(instance)
        return result


class ComputedClassField:
    def __init__(self, func):
        self.__func = func
        self.__name__ = func.__name__
        # self.__doc__ == func.__doc__ #??

    def __get__(self, instance, owner):
        if owner is None:
            return None
        result = self.__func(owner)
        setattr(owner, self.__name__, result)
        return result
