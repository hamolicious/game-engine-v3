from __future__ import annotations
from engine.metrics import Metric, Metrics

from hashlib import md5
from time import time
from typing import Callable, Generator, Type, TypeVar, cast

from engine.component import Component, ComponentTemplate
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

    def add_component(self, entity_id: EntityId, component: Type[Component]) -> None:
        if self._map.get(entity_id) is None:
            self._map[entity_id] = set()

        self._map[entity_id].add(component)


T = TypeVar("T", bound=Component)
R = TypeVar("R", bound=ComponentTemplate)


class ECSManager:
    def __init__(self) -> None:
        self.entities: dict[EntityId, Entity] = {}
        self.components: dict[type[Component], set[EntityId]] = {}
        self.has_map = _HasComponentMap()

        self.systems: dict[Stages, list[Callable[[ECSManager], None]]] = {
            Stages.SETUP: [],
            Stages.UPDATE: [],
            Stages.DRAW: [],
        }

    @staticmethod
    def _generate_entity_id() -> EntityId:
        return md5(str(time()).encode()).hexdigest()

    def create_entity(self, entity: Entity) -> EntityId:
        new_id = self._generate_entity_id()
        self.entities[new_id] = entity

        for comp in entity._components[::-1]:
            self.add_component_to_entity(new_id, comp)

        return new_id

    def remove_entity(self, entity_id: EntityId) -> bool:
        if entity_id not in self.entities:
            return False

        del self.entities[entity_id]
        self.has_map.remove_entity(entity_id)

        for comp in self.entities[entity_id]._components:
            self.components[type(comp)].remove(entity_id)

        return True

    def find_entities_with_all_components(
        self, *all_of: type[Component]
    ) -> Generator[EntityId, None, None]:
        yield from set.intersection(*[self.components[type_] for type_ in all_of])

    def find_entities_with_any_of_components(
        self, *component_types: type[Component]
    ) -> Generator[EntityId, None, None]:
        any_of = list(component_types)

        for type_ in any_of:
            yield from self.components.get(type_, set())

    def find_any_variation_on_entity(
        self, entity_id: EntityId, component_template: type[R]
    ) -> R | None:
        for type_ in component_template.all_variations():
            if (
                self.components.get(type_) is not None
                and entity_id in self.components[type_]
            ):
                return cast(
                    R, self.fetch_single_component_from_entity(entity_id, type_)
                )
        return None

    def get_single_component(self, component: Type[T]) -> T:
        ids = list(self.find_entities_with_all_components(component))
        assert len(ids) == 1, f"Found more than 1 instance! {component=}"
        return cast(T, self.fetch_components_from_entity(ids[0], component)[component])

    def fetch_components_from_entity(
        self, entity_id: EntityId, *components: Type[Component]
    ) -> dict[Type[Component], Component]:
        if entity_id not in self.entities:
            return {}

        ent = self.entities[entity_id]
        return {type(k): k for k in ent._components if type(k) in set(components)}

    def fetch_single_component_from_entity(
        self, entity_id: EntityId, component: Type[T]
    ) -> T:
        return cast(
            T, self.fetch_components_from_entity(entity_id, component)[component]
        )

    def add_component_to_entity(
        self, entity_id: EntityId, *components: Component
    ) -> None:
        for component in components:
            ct = type(component)
            if ct not in self.components:
                self.components[ct] = set()

            self.components[ct].add(entity_id)
            self.has_map.add_component(entity_id, type(component))
            self.entities[entity_id]._components.append(component)
            component._mount_time = time()

    def remove_component_from_entity(
        self, entity_id: EntityId, *component_types: Type[Component]
    ) -> bool:
        components = self.fetch_components_from_entity(
            entity_id, *component_types
        ).values()
        for component in components:
            self.entities[entity_id]._components.remove(component)
            self.has_map.remove_components(entity_id, type(component))
            self.components[type(component)].remove(entity_id)

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
            if Metrics.TOTAL_SYSTEM_TIMES.get(system.__name__) is None:
                Metrics.TOTAL_SYSTEM_TIMES[system.__name__] = Metric(name=f'system__{system.__name__}')

            Metrics.TOTAL_SYSTEM_TIMES[system.__name__].start_timer()
            system(self)
            Metrics.TOTAL_SYSTEM_TIMES[system.__name__].end_timer()
