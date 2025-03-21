from .. import Component


class Health(Component):
    def __init__(self, *, starting: float = 0, max_health: float = 0) -> None:
        super().__init__()

        self.starting = starting
        self.max_health = max_health
