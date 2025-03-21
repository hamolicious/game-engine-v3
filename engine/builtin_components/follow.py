from .. import Component


class FollowPlayer(Component):
    def __init__(self, desired_proximity: float = 0) -> None:
        super().__init__()

        self.distance = desired_proximity**2

        self.active = True
