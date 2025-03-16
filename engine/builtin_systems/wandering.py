import random
from time import time

import pygame

from engine import builtin_components

from ..ecs import ECSManager
from ..system import system


@system
def wandering(ecs: ECSManager) -> None:
    wanderers = ecs.find_entities_with_all_components(
        builtin_components.Wandering, builtin_components.Transform2D
    )

    for wanderer in wanderers:
        motion = ecs.find_any_variation_on_entity(
            wanderer, builtin_components.BaseMotion
        )
        transform = ecs.fetch_single_component_from_entity(
            wanderer, builtin_components.Transform2D
        )

        if motion is None:
            print("No Motion")
            continue

        wc = ecs.fetch_single_component_from_entity(
            wanderer, builtin_components.Wandering
        )

        if (
            transform.world_position.distance_squared_to(wc.current_target)
            < wc.arrival_margin
            and not wc.target_reached
        ):
            wc.target_reached = True
            wc.next_target_at = time() + float(
                random.randint(
                    wc.min_wait_time_sec,
                    wc.max_wait_time_sec,
                )
            )
            return

        if wc.target_reached and time() > (wc.next_target_at or float("inf")):
            new_target = pygame.Vector2()
            new_target.from_polar(
                (
                    random.randint(wc.min_radius, wc.max_radius),
                    random.randint(0, 360),
                )
            )
            new_target += wc.origin

            wc.current_target = new_target
            wc.target_reached = False
            wc.next_target_at = None
            return

        if not wc.target_reached:
            motion.move_to_target(transform, wc.current_target)
