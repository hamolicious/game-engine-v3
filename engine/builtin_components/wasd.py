from typing import Literal, TypeAlias

from ..common.component import Component

WASDKeys: TypeAlias = Literal["W", "A", "S", "D", ""]
AnimationName: TypeAlias = str


class WASD(Component):
    def __init__(
        self, key_to_animation_map: dict[WASDKeys, AnimationName] | None = None
    ) -> None:
        super().__init__()

        self.key_to_animation_map = key_to_animation_map
