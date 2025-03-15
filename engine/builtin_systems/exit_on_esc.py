import pygame

from ..ecs import ECSManager
from ..internal_components import Keyboard
from ..system import system


@system
def exit_on_esc(ecs: ECSManager) -> None:
    keyboard = ecs.fetch_only_one(Keyboard)

    if keyboard._keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit(0)
