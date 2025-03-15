from ..component import Component


class Motion(Component):
    def __init__(
        self,
        *,
        speed: float = 100,
    ) -> None:
        super().__init__()

        self.speed = speed
