from typing import Generator

from engine import builtin_systems

from .app import App
from .ecs import ECSManager
from .entity import Entity


class Engine:
    def __init__(self) -> None:
        self._ecs_manager = ECSManager()
        # TODO: control screen size and whatnot with a special component? 🤔😲
        self._app = App()

        self._register_setup_entities()

    def _register_setup_entities(self) -> None:
        for entity in self.setup():
            self._ecs_manager.create_entity(Entity(*entity._components))

        self._ecs_manager.register_system(builtin_systems.follow_player)

    def run(self) -> None:
        self._app.run(self._ecs_manager)

    def setup(self) -> Generator[Entity, None, None]:
        raise NotImplementedError("Override setup")
