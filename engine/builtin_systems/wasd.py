from typing import cast

import pygame

from engine import builtin_components

from ..builtin_components import BaseMotion, Player, Transform2D
from ..ecs import ECSManager
from ..internal_components import Keyboard, Time
from ..system import system


@system
def simple_wasd(ecs: ECSManager) -> None:
    keyboard = ecs.get_single_component(Keyboard)
    time = ecs.get_single_component(Time)

    player = list(ecs.find_entities_with_all_components(Player))[0]
    motion = ecs.find_any_variation_on_entity(player, BaseMotion)
    if motion is None:
        print("No motion")
        return

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
    motion.velocity = vel * motion.speed * time.delta_time
