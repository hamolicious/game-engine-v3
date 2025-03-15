from __future__ import annotations

from hashlib import md5
from time import time
from typing import Callable, Generator, Type, TypeVar, TypeVarTuple, cast

from engine.component import Component
from engine.entity import Entity, EntityId
from engine.types import Stages


class _HasComponentMap:
    def __init__(self) -> None:
        self._map: dict[EntityId, set[Type[Component]]] = {}

    def has(self, entity_id: EntityId, *components: Type[Component]) -> bool:
        return all([comp in self._map[entity_id] for comp in components])

    def remove_entity(self, entity_id: EntityId) -> bool:
        if entity_id not in self._map:
            return False

        del self._map[entity_id]
        return True

    def remove_components(
        self, entity_id: EntityId, *components: Type[Component]
    ) -> None:
        curr_map = self._map[entity_id]
        self._map[entity_id] = curr_map ^ set(components)

    def set_components(self, entity_id: EntityId, *components: Type[Component]) -> None:
        curr_map = self._map.get(entity_id, set())
        self._map[entity_id] = curr_map | set(components)
        return


T = TypeVar("T", bound=Component)


class ECSManager:
    def __init__(self) -> None:
        self.entities: dict[EntityId, Entity] = {}
        self.components: dict[type[Component], set[EntityId]] = {}
        self.has_map = _HasComponentMap()

        self.systems: dict[Stages, list[Callable[[ECSManager], None]]] = {
            Stages.SETUP: [],
            Stages.UPDATE: [],
            Stages.RENDER: [],
        }

    @staticmethod
    def _generate_entity_id() -> EntityId:
        return md5(str(time()).encode()).hexdigest()

    def create_entity(self, entity: Entity) -> EntityId:
        new_id = self._generate_entity_id()
        self.entities[new_id] = entity
        self.has_map.set_components(new_id, *map(lambda i: type(i), entity._components))

        for comp in entity._components:
            ct = type(comp)
            if ct not in self.components:
                self.components[ct] = set()

            self.components[ct].add(new_id)

        return new_id

    def remove_entity(self, entity_id: EntityId) -> bool:
        if entity_id not in self.entities:
            return False

        del self.entities[entity_id]
        self.has_map.remove_entity(entity_id)

        for comp in self.entities[entity_id]._components:
            self.components[type(comp)].remove(entity_id)

        return True

    def query_all_exist(
        self, *component_types: type[Component]
    ) -> Generator[EntityId, None, None]:
        comp_list = list(component_types)
        for entity_id in self.components.get(comp_list[0], set()):
            if self.has_map.has(entity_id, *comp_list):
                yield entity_id

    def fetch_only_one(self, component: Type[T]) -> T:
        ids = list(self.query_all_exist(component))
        assert len(ids) == 1, f"Found more than 1 instance! {component=}"
        return cast(T, self.fetch_components(ids[0], component)[component])

    def fetch_components(
        self, entity_id: EntityId, *components: Type[Component]
    ) -> dict[Type[Component], Component]:
        if entity_id not in self.entities:
            return {}

        ent = self.entities[entity_id]
        comp_set = set(components)
        return {type(k): k for k in ent._components if type(k) in comp_set}

    def add_component(self, entity_id: EntityId, component: Component) -> None:
        self.entities[entity_id]._components.append(component)

    def remove_component(
        self, entity_id: EntityId, component_type: Type[Component]
    ) -> bool:
        value = list(
            filter(
                lambda c: type[c] == component_type,
                self.entities[entity_id]._components,
            )
        )

        value_len = len(value)
        if value_len == 0:
            return False
        elif value_len > 1:
            raise RuntimeError(f"wtf? {component_type=}")

        self.entities[entity_id]._components.remove(value[0])

        return True

    def register_system(
        self, system: Callable[[ECSManager], None], stage: Stages = Stages.UPDATE
    ) -> None:
        self.systems[stage].append(system)

    def unregister_system(
        self, system: Callable[[ECSManager], None], stage: Stages = Stages.UPDATE
    ) -> bool:
        if system in self.systems[stage]:
            self.systems[stage].remove(system)
            return True
        return False

    def run_systems(self, stage: Stages) -> None:
        for system in self.systems[stage]:
            system(self)
