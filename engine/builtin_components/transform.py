from typing import Generic, Self, TypeVar, cast

from pygame import Vector2, Vector3
from pygame.image import load

from ..component import Component

T = TypeVar(
    "T",
    bound=Vector2 | Vector3,
)


class Transform(Generic[T]):
    def __init__(
        self,
        *,
        world_pos: T,
        local_pos: T,
        size: T,
        rot: float,
        z: float,
    ) -> None:
        self._world_pos: T = world_pos
        self._local_pos: T = local_pos
        self._size: T = size
        self._rot: float = rot
        self._z: float = z

    def set_z(self, new_z: float) -> Self:
        self._z = new_z
        return self

    def set_world_position(self, new_pos: T) -> Self:
        self._world_pos = cast(T, new_pos.copy())
        return self

    def set_local_position(self, new_pos: T) -> Self:
        self._local_pos = cast(T, new_pos.copy())
        return self

    @property
    def local_position(self) -> T:
        return cast(T, self._local_pos.copy())

    @property
    def world_position(self) -> T:
        return cast(T, self._world_pos.copy())

    @property
    def size(self) -> T:
        return cast(T, self._size.copy())

    @property
    def z(self) -> float:
        return self._z


class Transform2D(Transform[Vector2], Component):
    def __init__(
        self,
        *,
        world_pos: Vector2 = Vector2(0, 0),
        local_pos: Vector2 = Vector2(0, 0),
        size: Vector2 = Vector2(1, 1),
        rot: float = 0,
        z: float = 0,
    ) -> None:
        super().__init__(
            world_pos=world_pos,
            local_pos=local_pos,
            size=size,
            rot=rot,
            z=z,
        )
