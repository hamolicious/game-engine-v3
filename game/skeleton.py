from enum import Enum, auto

from engine.builtin_components import Transform2D, Wandering
from engine.fsm import FiniteStateMachine, state


class State(Enum):
    IDLE = auto()
    RESTING = auto()


class SkeletonFSM(FiniteStateMachine):
    @state(handles=State.IDLE)
    def idle(self) -> State:
        return State.IDLE

    @state(handles=State.RESTING)
    def resting(self) -> State:
        return State.RESTING
