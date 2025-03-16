import functools
from enum import Enum
from typing import Callable, Generic, Self, TypeVar

T = TypeVar("T", bound=Enum)


class BaseBrain(Generic[T]): ...


def state(handles: Enum):
    def decorator(func: Callable[[], T]):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        inner._handles_state = handles
        return inner

    return decorator


class Brain:
    def __init__(self, brain: type[BaseBrain]) -> None:
        super().__init__()
        self.brain = brain()
