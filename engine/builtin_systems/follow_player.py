from typing import cast

from ..builtin_components import BaseMotion, FollowPlayer, Player, Transform2D
from ..ecs import ECSManager
from ..internal_components import Time
from ..system import system


@system
def follow_player(ecs: ECSManager) -> None:
    time = ecs.get_single_component(Time)
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

        motion.velocity = (
            (
                other_transform.world_position - player_transform.world_position
            ).normalize()
            * -motion.speed
            * time.delta_time
        )
