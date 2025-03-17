from enum import Enum, auto

from engine.builtin_components import BaseBrain, state, Wandering


class State(Enum):
    IDLE = auto()
    RESTING = auto()


class SkeletonBrain(BaseBrain):
    @state(State.IDLE)
    def idle(self) -> Enum | None:
        return State.IDLE

    @state(State.RESTING)
    def resting(self) -> Enum | None:
        return State.RESTING

      
