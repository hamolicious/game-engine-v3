from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Callable, Protocol, cast

from engine.component import Component
from engine.ecs import ECSManager


class System(Protocol):
    def __call__(
        self,
        ecs: ECSManager,
    ) -> None: ...

    @property
    def __name__(self) -> str: ...


class SystemsRegister:
    @dataclass
    class Item:
        reads: tuple[type[Component], ...]
        writes: tuple[type[Component], ...]

    _index: list[System] = []
    _register: list[Item] = []

    @classmethod
    def add_system(
        cls,
        system: System,
        reads: tuple[type[Component], ...],
        writes: tuple[type[Component], ...],
    ) -> None:
        if system in cls._index:
            return

        cls._index.append(system)
        cls._register.append(cls.Item(reads, writes))

    @classmethod
    def get_read_writes(cls, system: System) -> Item:
        return cls._register[cls._index.index(system)]

    @classmethod
    def remove_system(cls, system: System) -> None:
        if system not in cls._index:
            return

        cls._register.pop(cls._index.index(system))
        cls._index.remove(system)


def system(
    reads: tuple[type[Component], ...],
    writes: tuple[type[Component], ...],
):
    def decorator(func: Callable[[ECSManager], None]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            func(*args, **kwargs)

        fuck_off_mypy_i_promise_they_are_the_same = cast(System, wrapper)
        SystemsRegister.add_system(
            fuck_off_mypy_i_promise_they_are_the_same, reads or (), writes or ()
        )

        return fuck_off_mypy_i_promise_they_are_the_same

    return decorator
