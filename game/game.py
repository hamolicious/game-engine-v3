import pygame

from engine.app import App as BaseApp
from engine.entity import Entity
from engine.scene import Scene


class Game(BaseApp):
    def setup(self) -> None:
        self.main_scene = Scene()

    def loop(self) -> None:
        if self.key_press[pygame.K_ESCAPE]:
            pygame.quit()
            quit(0)

    def render(self) -> None:
        self.screen.fill("black")
