import pygame

from ..common.component import Component


class Camera(Component):
    class Current(Component): ...

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.width = -1
        self.height = -1
        self.surf: pygame.Surface = pygame.Surface(
            (0, 0)
            if (self.width == -1 or self.height == -1)
            else (self.width, self.height)
        )

        self.ui_offset = pygame.Vector2()
