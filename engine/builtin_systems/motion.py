from typing import cast

from .. import builtin_components, internal_components
from ..ecs import ECSManager
from ..system import system


@system
def motion(ecs: ECSManager) -> None:
    time = ecs.get_single_component(internal_components.Time)
    entities = ecs.find_entities_with_any_of_components(
        *builtin_components.BaseMotion.all_variations()
    )

    for entity_id in entities:
        motion = ecs.find_any_variation_on_entity(
            entity_id, builtin_components.BaseMotion
        )
        if motion is None:
            continue

        transform = ecs.fetch_single_component_from_entity(
            entity_id, builtin_components.Transform2D
        )

        motion.apply(transform, time.delta_time)
