from typing import cast

from engine.component import Component

from ..builtin_components.brain import Brain
from ..ecs import ECSManager
from ..fsm import get_state_disable_components
from ..system import system


@system
def brain(ecs: ECSManager) -> None:
    big_brein = ecs.find_entities_with_all_components(Brain)

    for entity_id in big_brein:
        brain = ecs.fetch_single_component_from_entity(entity_id, Brain)

        component_types = cast(
            dict[str, type[Component]], brain.fsm.get_current_state_arg_types()
        )

        components = ecs.fetch_components_from_entity(
            entity_id, *tuple(component_types.values())
        )

        arg_name_to_component_instance = {
            an: components[ct] for an, ct in component_types.items()
        }

        if brain.fsm.is_initial_transition:
            disable_components = get_state_disable_components(
                brain.fsm.get_current_state_func()
            )
            comps = tuple(
                ecs.fetch_components_from_entity(
                    entity_id, *disable_components
                ).values()
            )
            brain.remember(*comps)
            ecs.remove_component_from_entity(entity_id, *map(type, comps))
            brain.fsm.is_initial_transition = False

        has_transitioned = brain.fsm.advance(arg_name_to_component_instance)

        if has_transitioned:
            disable_components = get_state_disable_components(
                brain.fsm.get_current_state_func()
            )
            comps = tuple(
                ecs.fetch_components_from_entity(
                    entity_id, *disable_components
                ).values()
            )
            ecs.add_component_to_entity(entity_id, *brain.forget())

            disable_components = get_state_disable_components(
                brain.fsm.get_current_state_func()
            )
            comps = tuple(
                ecs.fetch_components_from_entity(
                    entity_id, *disable_components
                ).values()
            )
            brain.remember(*comps)
            ecs.remove_component_from_entity(entity_id, *map(type, comps))
