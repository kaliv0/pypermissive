from contextlib import contextmanager

ERROR_MSG = "{error} raised unexpectedly!"


@contextmanager
def not_raises(ExpectedException):
    try:
        yield

    except (ExpectedException, Exception) as error:
        raise AssertionError(ERROR_MSG.format(error=str(error)))
