import math
import time as os_time
from typing import Generator, cast

from pygame import Vector2

from engine import (
    Engine,
    builtin_components,
    builtin_renderers,
)
from engine.component import Component
from engine.ecs import ECSManager
from engine.entity import Entity
from engine.system import system

from .skeleton import SkeletonFSM
from .skeleton import State as SkeletonBrainState


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
    entity_ids = ecs.find_entities_with_all_components(BopUpandDown)

    for bop in entity_ids:
        bop_comp = cast(
            BopUpandDown,
            ecs.fetch_components_from_entity(bop, BopUpandDown)[BopUpandDown],
        )
        transform = cast(
            builtin_components.Transform2D,
            ecs.fetch_components_from_entity(bop, builtin_components.Transform2D)[
                builtin_components.Transform2D
            ],
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
        lpc_walkcycle = {
            "idle": ((0, 2),),
            "walk-down": (
                (0, 2),
                (1, 2),
                (2, 2),
                (3, 2),
                (4, 2),
                (5, 2),
                (6, 2),
                (7, 2),
                (8, 2),
            ),
            "walk-up": (
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (8, 0),
            ),
            "walk-left": (
                (0, 1),
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 1),
                (5, 1),
                (6, 1),
                (7, 1),
                (8, 1),
            ),
            "walk-right": (
                (0, 3),
                (1, 3),
                (2, 3),
                (3, 3),
                (4, 3),
                (5, 3),
                (6, 3),
                (7, 3),
                (8, 3),
            ),
        }

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
            builtin_renderers.SpriteRenderer(),
        )

        yield Entity(
            builtin_components.Player(),
            builtin_components.Transform2D(world_pos=Vector2(200, 200), z=1),
            builtin_components.PhysicsMotion(
                accel_dir_to_anim_name ={
                    "": "idle",
                    "N": "walk-up",
                    "W": "walk-left",
                    "S": "walk-down",
                    "E": "walk-right",
                }
            ),
            builtin_components.SpriteSheet(
                src="./assets/BODY_male.png",
                x_count=9,
                y_count=4,
            ),
            builtin_components.Animation(
                current_animation="idle",
                animations=lpc_walkcycle,
            ),
            builtin_renderers.AnimationRenderer(),
            builtin_components.Collision(),
            builtin_components.Health(),
            builtin_components.WASD(
            ),
        )

        yield Entity(
            builtin_components.Name("Log"),
            builtin_components.Transform2D(world_pos=Vector2(300, 500), z=-0.5),
            builtin_components.Sprite(
                src="./assets/wood log sprite sheet.png",
                width=50,
                height=50,
            ),
            builtin_renderers.SpriteRenderer(),
            builtin_components.Collision(),
        )

        yield Entity(
            builtin_components.Name("Idle Enemy"),
            builtin_components.Transform2D(),
            builtin_components.PhysicsMotion(
                speed=2,
                friction=2,
                accel_dir_to_anim_name ={
                    "": "idle",
                    "N": "walk-up",
                    "W": "walk-left",
                    "S": "walk-down",
                    "E": "walk-right",
                }
            ),
            builtin_components.Brain(
                SkeletonFSM(SkeletonBrainState.IDLE),
            ),
            builtin_components.Detection(
                range=200,
                detect_only=(builtin_components.Player,),
            ),
            builtin_components.Wandering(
                origin=Vector2(300, 500),
                min_radius=100,
                max_radius=200,
            ),
            builtin_components.FollowPlayer(),
            builtin_components.SpriteSheet(
                src="./assets/BODY_skeleton.png",
                x_count=9,
                y_count=4,
            ),
            builtin_components.Animation(
                current_animation="idle",
                animations=lpc_walkcycle,
            ),
            builtin_renderers.AnimationRenderer(),
        )

        yield Entity(
            builtin_components.Name("Orb"),
            builtin_components.Transform2D(world_pos=Vector2(150, 150)),
            builtin_components.PhysicsMotion(
                speed=2,
                friction=1,
            ),
            builtin_components.Sprite(
                src="./assets/orb.png",
                width=25,
                height=25,
            ),
            builtin_components.Health(),
            builtin_components.FollowPlayer(),
            BopUpandDown(),
            builtin_renderers.SpriteRenderer(),
        )
