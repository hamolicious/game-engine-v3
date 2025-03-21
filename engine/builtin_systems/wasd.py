import pygame

from engine.builtin_components.animation import Animation

from .. import ECSManager, system
from ..builtin_components import WASD, BaseMotion, Transform2D
from ..internal_components import Keyboard


@system
def simple_wasd(ecs: ECSManager) -> None:
    keyboard = ecs.get_single_component(Keyboard)

    movers = ecs.find_entities_with_all_components(WASD, Transform2D)

    for entity_id in movers:
        motion = ecs.find_any_variation_on_entity(entity_id, BaseMotion)
        if motion is None:
            print("No motion")
            return

        vel = pygame.Vector2()
        dir = ""
        if keyboard.keys[pygame.K_w]:
            vel += pygame.Vector2(0, -1)
            dir = "W"

        if keyboard.keys[pygame.K_s]:
            vel += pygame.Vector2(0, 1)
            dir = "S"

        if keyboard.keys[pygame.K_a]:
            vel += pygame.Vector2(-1, 0)
            dir = "A"

        if keyboard.keys[pygame.K_d]:
            vel += pygame.Vector2(1, 0)
            dir = "D"

        wasd = ecs.fetch_single_component_from_entity(entity_id, WASD)
        if wasd.key_to_animation_map is not None:
            anim = ecs.fetch_single_component_from_entity(entity_id, Animation)
            anim.current_animation = wasd.key_to_animation_map[dir]

        if vel == pygame.Vector2():
            return

        motion.move_in_direction(vel)
