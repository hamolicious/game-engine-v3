from typing import cast

import pygame

from ..builtin_components import Motion, Player, Transform2D
from ..ecs import ECSManager
from ..internal_components import Keyboard, Time
from ..system import system


@system
def simple_wasd(ecs: ECSManager) -> None:
    keyboard = ecs.get_single_component(Keyboard)
    time = ecs.get_single_component(Time)

    player = list(ecs.find_entity_with_components(Player))[0]
    player_transform = cast(
        Transform2D, ecs.fetch_components_from_entity(player, Transform2D)[Transform2D]
    )
    motion = cast(Motion, ecs.fetch_components_from_entity(player, Motion)[Motion])

    vel = pygame.Vector2()
    if keyboard._keys[pygame.K_w]:
        vel += pygame.Vector2(0, -1)

    if keyboard._keys[pygame.K_a]:
        vel += pygame.Vector2(-1, 0)

    if keyboard._keys[pygame.K_s]:
        vel += pygame.Vector2(0, 1)

    if keyboard._keys[pygame.K_d]:
        vel += pygame.Vector2(1, 0)

    if vel == pygame.Vector2():
        return

    vel.normalize_ip()
    player_transform.set_world_position(
        player_transform.world_position + (vel * motion.speed * time.delta_time)
    )
