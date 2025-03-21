from typing import Self

from pygame import Vector2

from ..common.component import Component


class Transform2D(Component):
    def __init__(
        self,
        *,
        world_pos: Vector2 | None = None,
        local_pos: Vector2 | None = None,
        size: Vector2 | None = None,
        rot: float = 0,
        z: float = 0,
    ) -> None:
        self._world_pos: Vector2 = world_pos or Vector2()
        self._local_pos: Vector2 = local_pos or Vector2()
        self._size: Vector2 = size or Vector2()
        self._rot: float = rot
        self._z: float = z

    def set_z(self, new_z: float) -> Self:
        self._z = new_z
        return self

    def set_world_position(self, new_pos: Vector2) -> Self:
        self._world_pos = new_pos.copy()
        return self

    def set_local_position(self, new_pos: Vector2) -> Self:
        self._local_pos = new_pos.copy()
        return self

    @property
    def local_position(self) -> Vector2:
        return self._local_pos.copy()

    @property
    def world_position(self) -> Vector2:
        return self._world_pos.copy()

    @property
    def size(self) -> Vector2:
        return self._size.copy()

    @property
    def z(self) -> float:
        return self._z
