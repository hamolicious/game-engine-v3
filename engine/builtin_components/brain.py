import functools
from enum import Enum
from typing import Callable, Generator, Generic, Self, TypeVar, get_type_hints

from ..component import Component

P = TypeVar("P")
T = TypeVar("T", bound=Enum | Enum)

def state(handles: Enum):
    def decorator(func: Callable[[BaseBrain], T]):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        inner._handles_state = handles # type: ignore
        return inner

    return decorator


class BaseBrain(Component):
    def __init__(self, start_state: Enum) -> None:
        self._current_state = start_state
        self._state_to_func: dict[Enum, Callable] = {}

    def _get_method_state_handler(self, meth_name: str) -> Enum:
        meth = self.__getattribute__(meth_name)
        value = meth.__getattribute__('_handles_state')
        if value is None:
            raise ValueError(f'{meth} is not wrapped')

        return value

    def _is_method_wrapped(self, method_name: str) -> bool:
        if method_name.startswith('__'):
            return False

        meth = self.__getattribute__(method_name)
        return '_handles_state' in dir(meth)

    def _get_all_wrapped_methods(self) -> Generator[str]:
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

    def _run_current_state(self) -> None:
        new_state = self._state_to_func[self._current_state]()
        self._current_state = new_state



