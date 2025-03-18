from typing import Generator, TypeAlias

from engine.entity import Entity

SceneSetup: TypeAlias = Generator[Entity, None, None]


class Scene:
    def __init__(self) -> None:
        pass

    def setup(self) -> SceneSetup:
        raise NotImplementedError()
