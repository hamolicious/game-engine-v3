from typing import cast

from ..builtin_components import FollowPlayer, Player, Transform2D
from ..ecs import ECSManager
from ..system import system


@system
def follow_player(ecs: ECSManager) -> None:
    player = list(ecs.query_all_exist(Player))[0]
    player_transform = cast(
        Transform2D, ecs.fetch_components(player, Transform2D)[Transform2D]
    )
    for other in ecs.query_all_exist(Transform2D, FollowPlayer):
        other_transform = cast(
            Transform2D, ecs.fetch_components(other, Transform2D)[Transform2D]
        )

        other_transform.set_world_position(player_transform.world_position)
