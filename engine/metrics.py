from time import time


class Metric:
    def __init__(self, max_size: int = 5000) -> None:
        self.curr_value = 0.0
        self.last_value = 0.0

        self.max_size = max_size
        self.running_value: list[float] = []

        self.__start: float | None = None

    def running_average(self) -> float:
        if len(self.running_value) == 0:
            return 0

        return sum(self.running_value) / len(self.running_value)

    def _ensure_size(self) -> None:
        if len(self.running_value) <= self.max_size:
            return

        overrun = len(self.running_value) - self.max_size
        self.running_value = self.running_value[overrun::]

    def set_value(self, new_value: float) -> None:
        self.last_value = self.curr_value
        self.curr_value = new_value
        self.running_value.append(new_value)

    def start_timer(self) -> None:
        self.__start = time()

    def end_timer(self) -> float:
        """ Records a time, also saves it """
        if self.__start is None:
            raise RuntimeError('ended timer without starting it')

        elapsed = time() - self.__start
        self.__start = None

        self.set_value(elapsed)
        return elapsed


class Metrics:
    TOTAL_SETUP_TIME = Metric()
    TOTAL_RENDER_TIME = Metric()
    TOTAL_UPDATE_TIME = Metric()
    TOTAL_DRAW_TIME = Metric()
