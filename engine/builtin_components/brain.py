from ..component import Component
from ..fsm import FiniteStateMachine


class Brain(Component):
    def __init__(self, fsm: FiniteStateMachine) -> None:
        self.fsm = fsm

        self.fsm._build_state_machine()
