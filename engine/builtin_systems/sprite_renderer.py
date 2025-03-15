from typing import cast

from .. import builtin_components
from ..ecs import ECSManager
from ..internal_components.display import Display
from ..system import system


@system
def sprite_renderer(ecs: ECSManager) -> None:
    display = ecs.fetch_only_one(Display)
    entities = list(
        ecs.query_all_exist(builtin_components.Sprite, builtin_components.Transform2D)
    )

    renderables = []
    for entity_id in entities:
        comps = ecs.fetch_components(
            entity_id, builtin_components.Sprite, builtin_components.Transform2D
        )

        sprite = cast(builtin_components.Sprite, comps[builtin_components.Sprite])
        transform = cast(
            builtin_components.Transform2D, comps[builtin_components.Transform2D]
        )

        renderables.append((transform, sprite))

    renderables.sort(key=lambda e: e[0].z)
    for render in renderables:
        final_pos = render[0].world_position + render[0].local_position
        display.surface.blit(render[1].surf, final_pos.xy)
