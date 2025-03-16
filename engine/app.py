from time import time
from typing import cast

import pygame

from . import builtin_components, builtin_renderers
from .ecs import ECSManager
from .internal_components import Keyboard, Time
from .internal_components.display import Display
from .metrics import Metrics
from .types import Stages


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
        self.render_jobs: list[builtin_renderers.RenderJob] = []

    def _init_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        self.screen.fill([255, 255, 255])
        pygame.display.set_icon(self.screen)

        display = self.ecs_manager.get_single_component(Display)
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

        keyboard = self.ecs_manager.get_single_component(Keyboard)
        keyboard._keys = self.key_press

    def _update_display(self) -> None:
        pygame.display.update()
        self.delta_time = self.clock.tick(self.fps) / 1000
        self.actual_fps = self.clock.get_fps()
        pygame.display.set_caption(f"Framerate: {int(self.actual_fps)}")

        time = self.ecs_manager.get_single_component(Time)
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
            self._draw()
            self._update_display()

    def setup(self) -> None:
        start = time()
        self.ecs_manager.run_systems(Stages.SETUP)
        Metrics.TOTAL_SETUP_TIME.set_value((time() - start) * 1000)

    def loop(self) -> None:
        start = time()
        self.ecs_manager.run_systems(Stages.UPDATE)
        Metrics.TOTAL_UPDATE_TIME.set_value((time() - start) * 1000)

    def _render(self) -> None:
        start = time()

        camera_ids = tuple(
            self.ecs_manager.find_entity_with_components(
                builtin_components.Camera, builtin_components.Transform2D
            )
        )

        renderers = tuple(builtin_renderers.Renderer.__subclasses__())
        self.render_jobs = []

        for camera_id in camera_ids:
            for renderer in renderers:
                entity_ids = tuple(
                    self.ecs_manager.find_entity_with_components(*renderer.DEPENDENCIES)
                )

                camera = self.ecs_manager.fetch_single_component_from_entity(
                    camera_id, builtin_components.Camera
                )
                camera_transform = self.ecs_manager.fetch_single_component_from_entity(
                    camera_id, builtin_components.Transform2D
                )
                camera_world_rect = pygame.Rect(
                    camera_transform.world_position.xy, (camera.width, camera.height)
                )

                for entity_id in entity_ids:
                    entity_transform = (
                        self.ecs_manager.fetch_single_component_from_entity(
                            entity_id, builtin_components.Transform2D
                        )
                    )
                    entity_world_rect = pygame.Rect(
                        entity_transform.world_position.xy, entity_transform.size.xy
                    )

                    self.render_jobs.append(
                        builtin_renderers.RenderJob(
                            camera,
                            camera_transform,
                            entity_id,
                            entity_transform.z,
                            renderer,
                        )
                    )
        self.render_jobs = sorted(self.render_jobs, key=lambda r: r.z)
        for rj in self.render_jobs:
            entity_renderer = self.ecs_manager.fetch_single_component_from_entity(
                rj.entity_id, rj.renderer
            )

            print(rj.entity_id)
            entity_renderer._render(
                rj,
                self.ecs_manager.fetch_components_from_entity(
                    rj.entity_id,
                    *rj.renderer.DEPENDENCIES,
                    builtin_components.Transform2D,
                ),
            )
        self.render_jobs = []

        Metrics.TOTAL_RENDER_TIME.set_value((time() - start) * 1000)

    def _draw(self) -> None:
        start = time()
        self.ecs_manager.run_systems(Stages.DRAW)
        Metrics.TOTAL_DRAW_TIME.set_value((time() - start) * 1000)
