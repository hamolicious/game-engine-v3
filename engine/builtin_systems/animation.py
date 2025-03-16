from enum import _auto_null
from time import time

from engine import builtin_components, internal_components
from engine.ecs import ECSManager

from ..system import system


@system
def animation(ecs: ECSManager) -> None:
    entities_with_animations = ecs.find_entities_with_all_components(
        builtin_components.Animation
    )

    for entity_id in entities_with_animations:
        animation = ecs.fetch_single_component_from_entity(
            entity_id, builtin_components.Animation
        )
        curr_time = time()
        delay = 1.0 / animation.fps

        if curr_time < animation.next_switch:
            continue

        current_animation = animation.current_animation
        if animation.current_frame not in animation.animations[current_animation]:
            current_index = 0
        else:
            current_index = animation.animations[current_animation].index(
                animation.current_frame
            )

        new_index = current_index + 1
        if new_index >= len(animation.animations[current_animation]):
            new_index = 0

        animation.next_switch = curr_time + delay
        animation.current_frame = animation.animations[current_animation][new_index]
