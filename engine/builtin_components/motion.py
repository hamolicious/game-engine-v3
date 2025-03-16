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

    def apply(self, transform: Transform2D, dt: float) -> None:
        raise NotImplementedError()

    def move_in_direction(self, direction: pygame.Vector2) -> None:
        raise NotImplementedError()

    def move_to_target(
        self,
        source_transform: Transform2D | pygame.Vector2,
        target_transform: Transform2D | pygame.Vector2,
    ) -> None:
        p1 = (
            source_transform.world_position
            if isinstance(source_transform, Transform2D)
            else source_transform
        )
        p2 = (
            target_transform.world_position
            if isinstance(target_transform, Transform2D)
            else target_transform
        )

        self.move_in_direction((p2 - p1).normalize())


class DirectMotion(BaseMotion):
    def __init__(
        self,
        *,
        speed: float = 100,
    ) -> None:
        super().__init__()

        self.speed = speed

    def apply(self, transform: Transform2D, dt: float) -> None:
        transform.set_world_position(transform.world_position + self.velocity * dt)
        self.velocity = pygame.Vector2()

    def move_in_direction(self, direction: pygame.Vector2) -> None:
        self.velocity += direction.normalize() * self.speed


class PhysicsMotion(BaseMotion):
    def __init__(self, *, speed: float = 5, friction: float = 2) -> None:
        super().__init__()

        self.accel = pygame.Vector2()
        self.velocity = pygame.Vector2()

        self.speed = speed
        self.friction_multiplier = 1 - friction / 100

    def apply(self, transform: Transform2D, dt: float) -> None:
        self.velocity += self.accel
        self.accel = pygame.Vector2()

        transform.set_world_position(transform.world_position + self.velocity * dt)

        self.velocity *= self.friction_multiplier

    def move_in_direction(self, direction: pygame.Vector2) -> None:
        self.accel += direction.normalize() * self.speed
