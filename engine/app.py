from typing import cast

import pygame

from engine import builtin_components
from engine.internal_components import Keyboard, Time
from engine.internal_components.display import Display
from engine.types import Stages

from .ecs import ECSManager


class App:
    def __init__(self) -> None:
        self.display_size = (1000, 700)
        self.fps = 0

        self.clock = pygame.time.Clock()
        self.delta_time = 0.0

        self.screen: pygame.Surface
        self.mouse_pos: tuple[int, int]
        self.mouse_rel: tuple[int, int]
        self.mouse_press: tuple[bool, bool, bool]

        self.ecs_manager: ECSManager

    def _init_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        self.screen.fill([255, 255, 255])
        pygame.display.set_icon(self.screen)

        display = self.ecs_manager.fetch_only_one(Display)
        display.surface = self.screen
        display.width, display.height = self.screen.get_size()

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def _update_io(self) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_rel = pygame.mouse.get_rel()
        self.mouse_press = pygame.mouse.get_pressed()
        self.key_press = pygame.key.get_pressed()

        keyboard = self.ecs_manager.fetch_only_one(Keyboard)
        keyboard._keys = self.key_press

    def _update_display(self) -> None:
        pygame.display.update()
        self.delta_time = self.clock.tick(self.fps) / 1000
        self.actual_fps = self.clock.get_fps()
        pygame.display.set_caption(f"Framerate: {int(self.actual_fps)}")

        time = self.ecs_manager.fetch_only_one(Time)
        time.delta_time = self.delta_time
        time.fps = self.actual_fps

    def run(self, ecs_manager: ECSManager):
        self.ecs_manager = ecs_manager

        self._init_pygame()
        self.setup()

        while True:
            self._check_events()
            self._update_io()
            self.loop()
            self._render()
            self._update_display()

    def setup(self) -> None:
        self.ecs_manager.run_systems(Stages.SETUP)

    def loop(self) -> None:
        self.ecs_manager.run_systems(Stages.UPDATE)

    def _render(self) -> None:
        self.ecs_manager.run_systems(Stages.RENDER)
