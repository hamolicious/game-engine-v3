from contextlib import contextmanager
from time import gmtime
from typing import Any, Generator, Sequence, cast

import pygame

from engine import builtin_systems
from engine.internal_components import Display, Keyboard, Time
from engine.metrics import dump_metrics_in_csv_on_exit

from .app import App
from .common.entity import Entity
from .common.types import Stages
from .ecs_manager.ecs import ECSManager


class Engine:
    def __init__(self) -> None:
        self._ecs_manager = ECSManager()
        self._register_setup_entities()
        self._app = App()

    def _spawn_builtin_resources(self) -> None:
        self._ecs_manager.create_entity(
            Entity(
                Keyboard(
                    keys=cast(pygame.key.ScancodeWrapper, {}),
                )
            )
        )
        self._ecs_manager.create_entity(
            Entity(
                Time(
                    delta_time=0,
                    fps=0,
                )
            )
        )
        self._ecs_manager.create_entity(
            Entity(
                Display(surface=pygame.Surface((0, 0)), width=0, height=0),
            )
        )

    def _register_setup_entities(self) -> None:
        self._spawn_builtin_resources()

        for entity in self.setup():
            self._ecs_manager.create_entity(Entity(*entity._components))

        self._ecs_manager.register_system(builtin_systems.setup_cameras, Stages.SETUP)

        self._ecs_manager.register_system(builtin_systems.animation, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.wandering, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.motion, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.exit_on_esc, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.follow_player, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.simple_wasd, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.brain, Stages.UPDATE)
        self._ecs_manager.register_system(builtin_systems.detection, Stages.UPDATE)

        self._ecs_manager.register_system(builtin_systems.camera, Stages.DRAW)

    def run(self) -> None:
        with dump_metrics_in_csv_on_exit():
            self._app.run(self._ecs_manager)

    def setup(self) -> Generator[Entity, None, None]:
        raise NotImplementedError("Override setup")
