import functools
from enum import Enum
from typing import Any, Callable, Generator, get_type_hints

from .component import Component


def state(handles: Enum):
    def decorator(func: Callable[[Any, Component], Enum]):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        inner._handles_state = handles  # type: ignore
        return inner

    return decorator


class FiniteStateMachine:
    def __init__(self, start_state: Enum) -> None:
        self._current_state = start_state
        self._state_to_func: dict[Enum, Callable] = {}

    def _get_method_state_handler(self, meth_name: str) -> Enum:
        meth = self.__getattribute__(meth_name)
        value = meth.__getattribute__("_handles_state")
        if value is None:
            raise ValueError(f"{meth} is not wrapped")

        return value

    def _is_method_wrapped(self, method_name: str) -> bool:
        if method_name.startswith("__"):
            return False

        meth = self.__getattribute__(method_name)
        return "_handles_state" in dir(meth)

    def _get_all_wrapped_methods(self) -> Generator[str, None, None]:
        funcs = dir(self)

        for func in funcs:
            wrapped = self._is_method_wrapped(func)
            if not wrapped:
                continue

            yield func

    def _build_state_machine(self) -> None:
        state_methods = self._get_all_wrapped_methods()

        for meth_name in state_methods:
            handles = self._get_method_state_handler(meth_name)
            self._state_to_func[handles] = self.__getattribute__(meth_name)

    def get_current_state_arg_types(self) -> dict[str, type]:
        """Basically calls `get_type_hints` on the next state function, and gets rid of `return` key"""
        arg_to_type = get_type_hints(self._state_to_func[self._current_state])

        if "return" in arg_to_type:
            del arg_to_type["return"]

        return arg_to_type

    def advance(self, kwargs: dict[str, Any]) -> None:
        new_state = self._state_to_func[self._current_state](**kwargs)
        self._current_state = new_state
