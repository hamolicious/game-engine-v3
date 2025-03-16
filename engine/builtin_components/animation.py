from pygame import Vector2

from ..component import Component


class Animation(Component):
    def __init__(
        self,
        current_animation: str,
        animations: dict[str, tuple[tuple[int, int], ...]],
    ) -> None:
        super().__init__()

        self.current_animation = current_animation
        self.animations = animations

        self.current_frame = self.animations[self.current_animation][0]
