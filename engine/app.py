import pygame

from engine import builtin_components

from .ecs import ECSManager


class App:
    def __init__(self) -> None:
        self.display_size = (1000, 700)
        self.fps = 0

        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.screen: pygame.Surface
        self.mouse_pos: tuple[int, int]
        self.mouse_rel: tuple[int, int]
        self.mouse_press: tuple[bool, bool, bool]
        self.key_press: pygame.key.ScancodeWrapper

        self.ecs_manager: ECSManager

    def _init_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_size)
        self.screen.fill([255, 255, 255])
        pygame.display.set_icon(self.screen)

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

    def _update_display(self) -> None:
        pygame.display.update()
        self.delta_time = self.clock.tick(self.fps)
        pygame.display.set_caption(f"Framerate: {int(self.clock.get_fps())}")

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
        pass

    def loop(self) -> None:
        if self.key_press[pygame.K_ESCAPE]:
            pygame.quit()
            quit(0)

    def _render(self) -> None:
        for entity_id in self.ecs_manager.query_all_exist(
            builtin_components.Sprite, builtin_components.Transform2D
        ):
            comps = self.ecs_manager.fetch_components(
                entity_id, builtin_components.Sprite, builtin_components.Transform2D
            )

            sprite = comps[builtin_components.Sprite]
            transform = comps[builtin_components.Transform2D]
