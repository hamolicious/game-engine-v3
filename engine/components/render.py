from typing import Self

import pygame


class Renderer:
    def __init__(self) -> None:
        self._size = pygame.Vector2()

    def set_size(self, new_value: pygame.Vector2) -> Self:
        self._size = new_value.copy()
        return self

    def render(self, screen: pygame.Surface) -> None:
        raise NotImplementedError()


class RectRenderer(Renderer):
    def render(self, screen: pygame.Surface) -> None:
        pass
