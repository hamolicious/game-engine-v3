import pygame

from ..common.component import Component


class SpriteSheet(Component):
    def __init__(
        self,
        *,
        src: str,
        x_count: int | None = None,
        y_count: int | None = None,
        each_width: int | None = None,
        each_height: int | None = None,
    ) -> None:
        self.scr = src

        self.surf = pygame.image.load(self.scr)
        sheet: list[list[pygame.Surface]] = []

        if (
            x_count is None
            and y_count is None
            and each_width is not None
            and each_height is not None
        ):
            x_count = self.surf.get_width() // each_width
            y_count = self.surf.get_height() // each_height
        elif (
            each_width is None
            and each_height is None
            and x_count is not None
            and y_count is not None
        ):
            each_width = self.surf.get_width() // x_count
            each_height = self.surf.get_height() // y_count
        else:
            ValueError("")

        self.x_count: int = x_count or 0
        self.y_count: int = y_count or 0
        self.each_width: int = each_width or 0
        self.each_height: int = each_height or 0

        for row in range(self.y_count):
            row_arr = []
            for col in range(self.x_count):
                row_arr.append(
                    pygame.Surface((self.each_width, self.each_height), pygame.SRCALPHA)
                )

                row_arr[-1].blit(
                    self.surf,
                    (
                        -col * self.each_width,
                        -row * self.each_height,
                        self.each_width,
                        self.each_height,
                    ),
                )

            sheet.append(row_arr)

        self.sheet = sheet
