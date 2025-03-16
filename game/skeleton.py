from enum import Enum, auto

from engine.builtin_components import BaseBrain, state


class State(Enum):
    IDLE = auto()


class SkeletonBrain[State](BaseBrain):
    @state(State.IDLE)
    def idle(self) -> State | None:
        pass
