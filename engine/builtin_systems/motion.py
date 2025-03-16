from typing import cast

from .. import builtin_components
from ..ecs import ECSManager
from ..system import system


@system
def motion(ecs: ECSManager) -> None:
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

        motion.apply(transform)
