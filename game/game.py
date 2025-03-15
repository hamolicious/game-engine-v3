from typing import Generator

from engine import Engine, builtin_components
from engine.entity import Entity
from engine.system import system


class Game(Engine):
    def setup(self) -> Generator[Entity, None, None]:
        yield Entity(
            builtin_components.Name("Player"),
            builtin_components.Transform2D(),
            builtin_components.Motion(),
            builtin_components.Sprite(),
            builtin_components.Collision(),
            builtin_components.Health(),
            builtin_components.WASD(),
        )

        yield Entity(
            builtin_components.Name("Log"),
            builtin_components.Transform2D(),
            builtin_components.Sprite(),
            builtin_components.Collision(),
        )

        yield Entity(
            builtin_components.Name("Orb"),
            builtin_components.Transform2D(),
            builtin_components.Motion(),
            builtin_components.Sprite(),
            builtin_components.Health(),
            # builtin_components.Follow(),
        )
