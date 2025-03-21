from typing import cast

from .. import ECSManager, system
from ..builtin_components import BaseMotion, FollowPlayer, Player, Transform2D


@system
def follow_player(ecs: ECSManager) -> None:
    player = list(ecs.find_entities_with_all_components(Player))[0]
    player_transform = cast(
        Transform2D, ecs.fetch_components_from_entity(player, Transform2D)[Transform2D]
    )

    for other in ecs.find_entities_with_all_components(Transform2D, FollowPlayer):
        motion = ecs.find_any_variation_on_entity(other, BaseMotion)
        if motion is None:
            continue

        other_transform = cast(
            Transform2D,
            ecs.fetch_components_from_entity(other, Transform2D)[Transform2D],
        )
        follow_player = cast(
            FollowPlayer,
            ecs.fetch_components_from_entity(other, FollowPlayer)[FollowPlayer],
        )

        dist_sqr = other_transform.world_position.distance_squared_to(
            player_transform.world_position
        )

        if dist_sqr < follow_player.distance:
            continue

        motion.move_to_target(other_transform, player_transform)
