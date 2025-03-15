from typing import Generator

from .app import App
from .ecs import ECSManager
from .entity import Entity


class Engine:
    def __init__(self) -> None:
        self._ecs_manager = ECSManager()
        # TODO: control screen size and whatnot with a special component? 🤔😲
        self._app = App()

    def _register_setup_entities(self) -> None:
        for entity in self.setup():
            self._ecs_manager.create_entity(Entity(*entity._components))

    def run(self) -> None:
        self._app.run(self._ecs_manager)

    def setup(self) -> Generator[Entity, None, None]:
        raise NotImplementedError("Override setup")
