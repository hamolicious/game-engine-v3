from ..common.component import Component


class Name(Component):
    def __init__(self, name: str = "") -> None:
        self.name = name
