import functools
from typing import Callable

from engine.component import Component


# TODO: check how to type arbitrary amount of args
def system(original_function: Callable[[Component], None] | None = None):
    def _decorate(function):
        @functools.wraps(function)
        def wrapped_function(*args, **kwargs):
            # TODO: should't this yield?
            return original_function(*args, **kwargs)

        return wrapped_function

    if original_function:
        return _decorate(original_function)

    return _decorate
