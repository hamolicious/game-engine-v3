from typing import Generic, Self, TypeVar, cast

from pygame import Vector2, Vector3

from ..component import Component

T = TypeVar(
    "T",
    bound=Vector2 | Vector3,
)


class Transform(Generic[T]):
    def __init__(self) -> None:
        self._world_pos: T
        self._local_pos: T
        self._size: T
        self._rot: float

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


class Transform2D(Transform[Vector2], Component):
    pass


class Transform3D(Transform[Vector3], Component):
    pass
