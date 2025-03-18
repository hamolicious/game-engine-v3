from enum import Enum, auto
from time import time

from engine.builtin_components import Wandering, Detection, FollowPlayer
from engine.fsm import FiniteStateMachine, state


class State(Enum):
    IDLE = auto()
    CHASING = auto()


class SkeletonFSM(FiniteStateMachine):
    def __init__(self, start_state: Enum) -> None:
        super().__init__(start_state)

        self.chase_started: float = 0
        self.chase_time: float = 5

    @state(handles=State.IDLE, disables=(FollowPlayer,))
    def idle(self, detect: Detection) -> State:
        if len(detect.in_range) > 0:
            self.chase_started = time()
            return State.CHASING

        return State.IDLE

    @state(handles=State.CHASING, disables=(Wandering,))
    def chasing(self) -> State:
        if time() > self.chase_started + self.chase_time:
            return State.IDLE

        return State.CHASING

