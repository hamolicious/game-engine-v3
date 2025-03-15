import functools
from typing import Callable, Concatenate, ParamSpec, TypeAlias, TypeVar

from engine.ecs import ECSManager


def system(
    func: Callable[[ECSManager], None],
) -> Callable[[ECSManager], None]:

    @functools.wraps(func)
    def wrapper(ecs: ECSManager) -> None:
        # Task before calling the wrapped function
        # print("Before executing function")

        func(ecs)

        # Task after calling the wrapped function
        # print("After executing function")

    return wrapper
