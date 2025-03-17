from enum import Enum, auto

from engine.builtin_components import FiniteStateMachine, state
from engine.builtin_components.transform import Transform2D


class State(Enum):
    IDLE = auto()
    RESTING = auto()


class SkeletonFSM(FiniteStateMachine):
    @state(State.IDLE)
    def idle(self, transform: Transform2D) -> Enum | None:
        return State.IDLE

    @state(State.RESTING)
    def resting(self) -> Enum | None:
        return State.RESTING
