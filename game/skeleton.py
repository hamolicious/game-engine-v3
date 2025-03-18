from enum import Enum, auto

from engine.builtin_components import Wandering, Detection, FollowPlayer
from engine.fsm import FiniteStateMachine, state


class State(Enum):
    IDLE = auto()
    RESTING = auto()
    CHASING = auto()


class SkeletonFSM(FiniteStateMachine):
    @state(handles=State.IDLE, disables=(FollowPlayer,))
    def idle(self, detect: Detection) -> State:
        if len(detect.in_range) > 0:
            return State.CHASING

        return State.IDLE

    @state(handles=State.CHASING, disables=(Wandering,))
    def chasing(self) -> State:
        return State.CHASING

    @state(handles=State.RESTING)
    def resting(self) -> State:
        return State.RESTING
