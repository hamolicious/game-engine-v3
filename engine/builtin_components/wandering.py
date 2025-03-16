import pygame

from engine import builtin_components

from ..component import Component


class Wandering(Component):
    def __init__(
        self,
        *,
        origin: pygame.Vector2 | builtin_components.Transform2D,
        current_target: pygame.Vector2 | None = None,
        max_radius: int = 100,
        min_radius: int = 0,
        target_reached: bool = False,
        next_target_at: float | None = None,
        min_wait_time_sec: int = 3,
        max_wait_time_sec: int = 10,
        arrival_margin: float = 1,
    ) -> None:

        self.origin = (
            origin if isinstance(origin, pygame.Vector2) else origin.world_position
        )
        self.min_radius = min_radius
        self.max_radius = max_radius

        self.current_target: pygame.Vector2 = current_target or pygame.Vector2()
        self.target_reached = target_reached
        self.next_target_at = next_target_at

        self.min_wait_time_sec: int = min_wait_time_sec
        self.max_wait_time_sec: int = max_wait_time_sec

        self.arrival_margin: float = arrival_margin
