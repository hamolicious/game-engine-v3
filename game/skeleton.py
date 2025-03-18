from enum import Enum, auto
from time import time

from engine.builtin_components import Wandering, Detection, FollowPlayer
from engine.fsm import FiniteStateMachine, state


class State(Enum):
    IDLE = auto()
    CHASING = auto()


class SkeletonFSM(FiniteStateMachine):
    CHASE_TIME = 5

    @state(handles=State.IDLE, disables=(FollowPlayer,))
    def idle(self, detect: Detection) -> State:
        if len(detect.in_range) > 0:
            return State.CHASING

        return State.IDLE

    @state(handles=State.CHASING, disables=(Wandering,))
    def chasing(self, fp: FollowPlayer) -> State:
        if fp.mounted_time_sec > self.CHASE_TIME:
            return State.IDLE

        return State.CHASING

