class Metric:
    def __init__(self, max_size: int = 5000) -> None:
        self.curr_value = 0.0
        self.last_value = 0.0

        self.max_size = max_size
        self.running_value: list[float] = []

    def _ensure_size(self) -> None:
        if len(self.running_value) <= self.max_size:
            return

        overrun = len(self.running_value) - self.max_size
        self.running_value = self.running_value[overrun::]

    def set_value(self, new_value: float) -> None:
        self.last_value = self.curr_value
        self.curr_value = new_value
        self.running_value.append(new_value)


class Metrics:
    TOTAL_SETUP_TIME = Metric()
    TOTAL_RENDER_TIME = Metric()
    TOTAL_UPDATE_TIME = Metric()
    TOTAL_DRAW_TIME = Metric()
