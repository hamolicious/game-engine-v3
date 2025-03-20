from typing import Callable


class Node:
    def __init__(self, system: Callable) -> None:
        self.system = system
        self.dependencies: tuple[Node, ...] = tuple()
        self.produces: tuple[Node, ...] = tuple()
