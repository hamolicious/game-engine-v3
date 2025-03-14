import pygame

from engine.app import App as BaseApp


class Game(BaseApp):
    def setup(self) -> None:
        pass

    def loop(self) -> None:
        if self.key_press[pygame.K_ESCAPE]:
            pygame.quit()
            quit(0)

    def render(self) -> None:
        self.screen.fill("black")
