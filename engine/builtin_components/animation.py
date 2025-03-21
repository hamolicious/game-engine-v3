from time import time

from .. import Component


class Animation(Component):
    def __init__(
        self,
        current_animation: str,
        animations: dict[str, tuple[tuple[int, int], ...]],
        fps: int = 8,
    ) -> None:
        super().__init__()

        self.current_animation = current_animation
        self.animations = animations
        self.fps = fps

        self.next_switch = time()
        self.current_frame = self.animations[self.current_animation][0]
