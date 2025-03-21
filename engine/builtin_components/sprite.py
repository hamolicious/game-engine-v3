import pygame

from ..common.component import Component


class Sprite(Component):
    def __init__(
        self,
        *,
        src: str,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        self.scr = src

        self.surf = pygame.image.load(self.scr)

        w, h = self.surf.get_size()
        if (width is not None and height is not None) and (w != width or h != height):
            self.surf = pygame.transform.scale(self.surf, (width, height))
