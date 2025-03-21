from .. import Component
from ..fsm import FiniteStateMachine


class Brain(Component):
    def __init__(self, fsm: FiniteStateMachine) -> None:
        self.fsm = fsm
        self.memory: list[Component] = []

        self.fsm._build_state_machine()

    def remember(self, *components: Component) -> None:
        self.memory.extend(components)

    def forget(self) -> list[Component]:
        ret = self.memory
        self.memory = []
        return ret
