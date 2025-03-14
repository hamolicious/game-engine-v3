from .util import generate_unique_id


class Entity:
    def __init__(self) -> None:
        self._id = generate_unique_id()

    @property
    def id(self) -> str:
        return self._id
