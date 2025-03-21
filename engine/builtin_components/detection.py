from .. import Component, EntityId


class Detection(Component):
    def __init__(
        self, range: int = 100, detect_only: tuple[type[Component], ...] | None = None
    ) -> None:
        super().__init__()

        self.range = range
        self.detect_only = detect_only
        self.in_range: list[EntityId] = []
