from typing import TypeAlias

from engine.component import Component

EntityId: TypeAlias = str


class Entity:
    def __init__(self, *components: Component) -> None:
        self._components = list(components)
