import pygame

from ..ecs import ECSManager
from ..internal_components import Keyboard
from ..system import system


@system
def exit_on_esc(ecs: ECSManager) -> None:
    keyboard = ecs.get_single_component(Keyboard)

    if keyboard.keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit(0)
