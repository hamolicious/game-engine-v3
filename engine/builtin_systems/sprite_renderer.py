from typing import cast

import pygame

from .. import builtin_components
from ..ecs import ECSManager
from ..internal_components.display import Display
from ..system import system


@system
def sprite_renderer(ecs: ECSManager) -> None:
    display = ecs.get_single_component(Display)
    cameras_ids = tuple(ecs.find_entity_with_components(builtin_components.Camera))

    if len(cameras_ids) == 0:
        print("No cameras, nothing to render")
        return

    entities = list(
        ecs.find_entity_with_components(
            builtin_components.Sprite, builtin_components.Transform2D
        )
    )

    for camera_id in cameras_ids:
        camera = cast(
            builtin_components.Camera,
            ecs.fetch_components_from_entity(camera_id, builtin_components.Camera)[
                builtin_components.Camera
            ],
        )
        camera_transform = cast(
            builtin_components.Transform2D,
            ecs.fetch_components_from_entity(camera_id, builtin_components.Transform2D)[
                builtin_components.Transform2D
            ],
        )

        camera_world_rect = pygame.Rect(
            camera_transform.world_position.xy, (display.width, display.height)
        )

        renderables = []
        for entity_id in entities:
            comps = ecs.fetch_components_from_entity(
                entity_id, builtin_components.Sprite, builtin_components.Transform2D
            )

            sprite = cast(builtin_components.Sprite, comps[builtin_components.Sprite])
            transform = cast(
                builtin_components.Transform2D, comps[builtin_components.Transform2D]
            )

            if not camera_world_rect.collidepoint(transform.world_position):
                continue

            renderables.append((transform, sprite))

        renderables.sort(key=lambda e: e[0].z)
        for render in renderables:
            final_pos = render[0].world_position + render[0].local_position
            camera.surf.blit(render[1].surf, final_pos.xy)
