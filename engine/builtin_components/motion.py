import math
from typing import Literal, TypeAlias

import pygame

from .. import ComponentTemplate
from .transform import Transform2D

CardinalDirection: TypeAlias = Literal["N", "E", "S", "W"]
CardinalDirectionWithNoDir: TypeAlias = CardinalDirection | Literal[""]


class BaseMotion(ComponentTemplate):
    def __init__(
        self,
        *,
        speed: float = 100,
        accel_dir_to_anim_name: dict[CardinalDirectionWithNoDir, str] | None = None,
    ) -> None:
        self.accel = pygame.Vector2()
        self.speed = speed
        self.velocity = pygame.Vector2()

        self.accel_direction_to_animation_name_map: (
            dict[CardinalDirectionWithNoDir, str] | None
        ) = accel_dir_to_anim_name

    def accel_to_cardinal_direction(self) -> CardinalDirectionWithNoDir:
        if self.accel.length_squared() < 0.1:
            return ""

        angle = math.atan2(-self.accel.y, self.accel.x)
        angle_deg = math.degrees(angle) % 360

        # Map to direction:
        if 45 <= angle_deg < 135:
            return "N"
        elif 135 <= angle_deg < 225:
            return "W"
        elif 225 <= angle_deg < 315:
            return "S"
        else:
            return "E"

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


class PhysicsMotion(BaseMotion):
    def __init__(
        self,
        *,
        speed: float = 5,
        friction: float = 2,
        accel_dir_to_anim_name: dict[CardinalDirectionWithNoDir, str] | None = None,
    ) -> None:
        super().__init__(accel_dir_to_anim_name=accel_dir_to_anim_name)

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
