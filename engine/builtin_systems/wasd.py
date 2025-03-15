from typing import cast

import pygame

from ..builtin_components import FollowPlayer, Keyboard, Player, Transform2D
from ..ecs import ECSManager
from ..system import system


@system
def simple_wasd(ecs: ECSManager) -> None:
    kid = list(ecs.query_all_exist(Keyboard))[0]
    keyboard = cast(Keyboard, ecs.fetch_components(kid, Keyboard)[Keyboard])

    player = list(ecs.query_all_exist(Player))[0]
    player_transform = cast(
        Transform2D, ecs.fetch_components(player, Transform2D)[Transform2D]
    )

    if keyboard._keys[pygame.K_w]:
        player_transform.set_world_position(
            player_transform.world_position + pygame.Vector2(0, -1)
        )

    if keyboard._keys[pygame.K_a]:
        player_transform.set_world_position(
            player_transform.world_position + pygame.Vector2(-1, 0)
        )

    if keyboard._keys[pygame.K_s]:
        player_transform.set_world_position(
            player_transform.world_position + pygame.Vector2(0, 1)
        )

    if keyboard._keys[pygame.K_d]:
        player_transform.set_world_position(
            player_transform.world_position + pygame.Vector2(1, 0)
        )
