from enum import Enum, auto


class Stages(Enum):
    SETUP = auto()
    UPDATE = auto()
    RENDER = auto()
    DRAW = auto()
