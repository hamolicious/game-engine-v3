from typing import Generator

from pygame import Vector2

from engine import Engine, builtin_components, builtin_systems
from engine.entity import Entity
from engine.system import system


class Game(Engine):
    def setup(self) -> Generator[Entity, None, None]:
        yield Entity(
            builtin_components.Name("Background"),
            builtin_components.Transform2D(z=-1),
            builtin_components.Sprite(
                src="./assets/bg.jpg",
                width=1000,
                height=700,
            ),
        )

        yield Entity(
            builtin_components.Player(),
            builtin_components.Transform2D(world_pos=Vector2(200, 200)),
            builtin_components.Motion(),
            builtin_components.Sprite(
                src="./assets/player-single.png",
                width=50,
                height=50,
            ),
            builtin_components.Collision(),
            builtin_components.Health(),
            builtin_components.WASD(),
        )

        yield Entity(
            builtin_components.Name("Log"),
            builtin_components.Transform2D(world_pos=Vector2(300, 500)),
            builtin_components.Motion(),
            builtin_components.Sprite(
                src="./assets/wood log sprite sheet.png",
                width=50,
                height=50,
            ),
            builtin_components.Collision(),
        )

        yield Entity(
            builtin_components.Name("Orb"),
            builtin_components.Transform2D(world_pos=Vector2(150, 150)),
            builtin_components.Motion(),
            builtin_components.Sprite(
                src="./assets/orb.png",
                width=25,
                height=25,
            ),
            builtin_components.Health(),
            builtin_components.FollowPlayer(),
        )
