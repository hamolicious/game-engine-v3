from ..common.component import Component


class Time(Component):
    def __init__(
        self,
        *,
        delta_time: float,
        fps: float,
    ) -> None:
        super().__init__()

        self.delta_time = delta_time
        self.fps = fps
