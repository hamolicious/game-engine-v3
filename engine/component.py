from __future__ import annotations
from time import time


class Component:
    def __init__(self) -> None:
        self._mount_time: float = 0

    @property
    def mounted_at(self) -> float:
        return self._mount_time


    @property
    def mounted_time_sec(self) -> float:
        return time() - self._mount_time


class ComponentTemplate(Component):
    @classmethod
    def all_variations(cls) -> tuple[type[ComponentTemplate], ...]:
        return tuple(cls.__subclasses__())
