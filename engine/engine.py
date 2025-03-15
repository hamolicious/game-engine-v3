from typing import Generator, cast

import pygame

from engine import builtin_systems
from engine.internal_components import Keyboard, Time

from .app import App
from .ecs import ECSManager
from .entity import Entity


class Engine:
    def __init__(self) -> None:
        self._ecs_manager = ECSManager()
        self._register_setup_entities()

        # TODO: control screen size and whatnot with a special component? 🤔😲
        self._app = App()

    def _register_setup_entities(self) -> None:
        for entity in self.setup():
            self._ecs_manager.create_entity(Entity(*entity._components))

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

        self._ecs_manager.register_system(builtin_systems.exit_on_esc)
        self._ecs_manager.register_system(builtin_systems.follow_player)
        self._ecs_manager.register_system(builtin_systems.simple_wasd)

    def run(self) -> None:
        self._app.run(self._ecs_manager)

    def setup(self) -> Generator[Entity, None, None]:
        raise NotImplementedError("Override setup")
