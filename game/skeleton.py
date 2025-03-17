from enum import Enum, auto

from engine.builtin_components.transform import Transform2D
from engine.fsm import FiniteStateMachine, state


class State(Enum):
    IDLE = auto()
    RESTING = auto()


class SkeletonFSM(FiniteStateMachine):
    @state(State.IDLE)
    def idle(self, transform: Transform2D) -> State:
        return State.IDLE

    @state(State.RESTING)
    def resting(self) -> State:
        return State.RESTING
