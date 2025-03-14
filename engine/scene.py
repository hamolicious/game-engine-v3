from typing import Generator

from .entity import Entity


class Scene:
    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}

    def add_entity(self, ent: Entity) -> None:
        self._entities[ent.id] = ent

    def get_entity(self, id: str) -> Entity | None:
        return self._entities.get(id, None)

    def get_all_entities(self) -> Generator[Entity, None, None]:
        for ent in self._entities.values():
            yield ent
