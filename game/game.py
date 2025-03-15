import math
import time as os_time
from typing import Generator, cast

from pygame import Vector2

from engine import Engine, builtin_components, builtin_systems
from engine.builtin_components.transform import Transform2D
from engine.component import Component
from engine.ecs import ECSManager
from engine.entity import Entity
from engine.internal_components.time import Time
from engine.system import system


class BopUpandDown(Component):
    def __init__(
        self,
        amplitude: float = 5,
        frequency: float = 0.5,
    ) -> None:
        super().__init__()

        self.amplitude = amplitude
        self.frequency = frequency

        self.initial_y = 0
        self.start_time = os_time.time()


@system
def bop_up_and_down(ecs: ECSManager) -> None:
    entity_ids = ecs.find_entity_with_components(BopUpandDown)

    for bop in entity_ids:
        bop_comp = cast(
            BopUpandDown,
            ecs.fetch_components_from_entity(bop, BopUpandDown)[BopUpandDown],
        )
        transform = cast(
            Transform2D, ecs.fetch_components_from_entity(bop, Transform2D)[Transform2D]
        )

        t = os_time.time() - bop_comp.start_time
        y = bop_comp.initial_y + bop_comp.amplitude * math.sin(
            2 * math.pi * bop_comp.frequency * t
        )

        new_pos = transform.local_position
        new_pos.y = y
        transform.set_local_position(new_pos)


class Game(Engine):
    def setup(self) -> Generator[Entity, None, None]:
        self._ecs_manager.register_system(bop_up_and_down)

        yield Entity(
            builtin_components.Transform2D(),
            builtin_components.Camera(),
        )

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
            BopUpandDown(),
        )
