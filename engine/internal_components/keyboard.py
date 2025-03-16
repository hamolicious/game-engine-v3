import pygame

from ..component import Component


class Keyboard(Component):
    def __init__(self, *, keys: pygame.key.ScancodeWrapper) -> None:
        super().__init__()

        self.keys: pygame.key.ScancodeWrapper = keys
