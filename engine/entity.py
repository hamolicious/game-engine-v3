from .components.render import Renderer
from .components.transform import Transform
from .util import generate_unique_id


class Entity:
    def __init__(self) -> None:
        self._parent: Entity | None = None
        self._children: list[Entity] = []

        self._id = generate_unique_id()

        self._transform: Transform | None = None
        self._renderer: Renderer | None = None

    @property
    def id(self) -> str:
        return self._id
