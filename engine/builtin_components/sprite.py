import pygame

from ..component import Component


class Sprite(Component):
    def __init__(self, *, src: str) -> None:
        self.scr = src

        self.surf = pygame.image.load(self.scr)
