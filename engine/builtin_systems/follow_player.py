from typing import cast

from ..builtin_components import FollowPlayer, Player, Transform2D
from ..ecs import ECSManager
from ..internal_components import Time
from ..system import system


@system
def follow_player(ecs: ECSManager) -> None:
    time = ecs.get_single_component(Time)
    player = list(ecs.find_entity_with_components(Player))[0]
    player_transform = cast(
        Transform2D, ecs.fetch_components_from_entity(player, Transform2D)[Transform2D]
    )

    for other in ecs.find_entity_with_components(Transform2D, FollowPlayer):
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

        new_pos = other_transform.world_position + (
            (
                other_transform.world_position - player_transform.world_position
            ).normalize()
            * -follow_player.speed
            * time.delta_time
        )

        other_transform.set_world_position(new_pos)
