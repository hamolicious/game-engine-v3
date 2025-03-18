from typing import Type, cast

from engine import builtin_components
from engine.builtin_renderers import renderer

from .renderer import Component, Renderer, RenderJob


class SpriteRenderer(Renderer):
    DEPENDENCIES = {
        builtin_components.Sprite,
    }

    def _render(
        self, render: RenderJob, components: dict[Type[Component], Component]
    ) -> None:
        sprite = cast(builtin_components.Sprite, components[builtin_components.Sprite])
        transform = cast(
            builtin_components.Transform2D, components[builtin_components.Transform2D]
        )

        final_pos = (
            transform.world_position + transform.local_position
        ) - render.camera_transform.world_position

        render.camera.surf.blit(sprite.surf.convert_alpha(), final_pos)
