from ..component import Component


class FollowPlayer(Component):
    def __init__(self) -> None:
        super().__init__()

        self.distance = 100**2
        self.speed = 90

        self.active = True
