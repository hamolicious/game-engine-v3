import pygame

from ..component import ComponentTemplate
from .transform import Transform2D


class BaseMotion(ComponentTemplate):
    def __init__(
        self,
        *,
        speed: float = 100,
    ) -> None:
        self.speed = speed
        self.velocity = pygame.Vector2()

    def apply(self, transform: Transform2D) -> None:
        raise NotImplementedError()


class DirectMotion(BaseMotion):
    def __init__(
        self,
        *,
        speed: float = 100,
    ) -> None:
        super().__init__()

        self.speed = speed

    def apply(self, transform: Transform2D) -> None:
        transform.set_world_position(transform.world_position + self.velocity)
        self.velocity = pygame.Vector2()
