from ..component import Component


class FollowPlayer(Component):
    def __init__(self) -> None:
        super().__init__()

        self.distance = 10**2
        self.speed = 1

        self.active = True
