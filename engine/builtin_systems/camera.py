from typing import cast

import pygame

from engine import internal_components

from .. import ECSManager, builtin_components, system
from ..internal_components import Display


@system
def setup_cameras(ecs: ECSManager) -> None:
    display = ecs.get_single_component(internal_components.Display)
    cameras_ids = tuple(
        ecs.find_entities_with_all_components(builtin_components.Camera)
    )

    for camid in cameras_ids:
        camera = cast(
            builtin_components.Camera,
            ecs.fetch_components_from_entity(camid, builtin_components.Camera)[
                builtin_components.Camera
            ],
        )

        if camera.width == -1 or camera.height == -1:
            camera.surf = pygame.Surface(display.surface.get_size())
            camera.width, camera.height = camera.surf.get_size()

    if len(cameras_ids) == 1:
        ecs.add_component_to_entity(cameras_ids[0], builtin_components.Camera.Current())


@system
def camera(ecs: ECSManager) -> None:
    display = ecs.get_single_component(Display)
    current_camera_id = tuple(
        ecs.find_entities_with_all_components(
            builtin_components.Camera, builtin_components.Camera.Current
        )
    )

    if len(current_camera_id) == 0:
        raise ValueError("No Current Camera")

    if len(current_camera_id) > 1:
        raise ValueError("Multiple camera arent supported, _yet_")

    camera = ecs.fetch_single_component_from_entity(
        current_camera_id[0], builtin_components.Camera
    )
    display.surface.blit(camera.surf, camera.ui_offset.xy)
