import pygame

from ..common.component import Component


class Display(Component):
    def __init__(self, surface: pygame.Surface, width: int, height: int) -> None:
        super().__init__()

        self.surface = surface
        self.width = width
        self.height = height
