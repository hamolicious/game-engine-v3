from typing import Type, cast

from .. import builtin_components
from ..common.component import Component
from .renderer import Renderer, RenderJob


class AnimationRenderer(Renderer):
    DEPENDENCIES = {
        builtin_components.Animation,
        builtin_components.SpriteSheet,
    }

    def _render(
        self, render: RenderJob, components: dict[Type[Component], Component]
    ) -> None:
        animation = cast(
            builtin_components.Animation, components[builtin_components.Animation]
        )
        spritesheet = cast(
            builtin_components.SpriteSheet, components[builtin_components.SpriteSheet]
        )
        transform = cast(
            builtin_components.Transform2D, components[builtin_components.Transform2D]
        )

        final_pos = (
            transform.world_position + transform.local_position
        ) - render.camera_transform.world_position

        x, y = animation.current_frame
        frame = spritesheet.sheet[y][x]

        render.camera.surf.blit(frame, final_pos)
