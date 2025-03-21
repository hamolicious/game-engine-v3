from __future__ import annotations

from typing import Type

from engine import builtin_components

from ..common.component import Component
from ..common.entity import EntityId


class RenderJob:
    def __init__(
        self,
        camera: builtin_components.Camera,
        camera_transform: builtin_components.Transform2D,
        entity_id: EntityId,
        z: float,
        renderer: Type[Renderer],
    ) -> None:
        self.camera = camera
        self.camera_transform = camera_transform
        self.entity_id = entity_id
        self.renderer = renderer
        self.z = z


class Renderer(Component):
    DEPENDENCIES: set[Type[Component]] = set()

    def __init__(self) -> None:
        super().__init__()

        self.enabled = True

    def _render(
        self, render: RenderJob, components: dict[Type[Component], Component]
    ) -> None:
        raise NotImplementedError("Override this")
