from contextlib import contextmanager
from time import gmtime
from typing import Any, Generator

from time import time
from typing import Generator


def _safe_pop[T](arr: list[T]) -> T | None:
    if len(arr) == 0:
        return None

    return arr.pop(0)

def dump_metrics_in_csv() -> None:
    metrics = tuple(Metrics.get_all_metrics())
    headers = tuple([m.name for m in metrics])

    csv: list[Any] = [headers]
    while True:
        values = tuple([_safe_pop(m.running_value) for m in metrics])
        if not any(values):
            break

        csv.append(values)

    t = gmtime()
    stamp = f'{t.tm_year}-{t.tm_mon}-{t.tm_mday}-{t.tm_hour}-{t.tm_min}-{t.tm_sec}'
    str_lines = map(lambda l: ','.join(map(str, l)) + '\n', csv)
    with open(f'engine-metrics.dump-{stamp}.csv', 'w') as f:
        f.writelines(str_lines)

@contextmanager
def dump_metrics_in_csv_on_exit():
    try:
        yield
    finally:
        dump_metrics_in_csv()



class Metric:
    def __init__(self, name: str | None = None, max_size: int = 1_000_000) -> None:
        self.name = name or 'No Name'

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
    TOTAL_SETUP_TIME = Metric("total_setup_time")
    TOTAL_RENDER_TIME = Metric("total_render_time")
    TOTAL_UPDATE_TIME = Metric("total_update_time")
    TOTAL_SYSTEM_TIMES: dict[str, Metric] = {}
    TOTAL_DRAW_TIME = Metric("total_draw_time")

    @classmethod
    def get_all_metrics(cls) -> Generator[Metric, None, None]:
        for prop_name, prop in cls.__dict__.items():
            of_these_dickheads = [
                prop_name.startswith('_'),
                prop_name.upper() != prop_name,
            ]

            if any(of_these_dickheads) is True:
                continue

            if isinstance(prop, dict):
                yield from prop.values()
                continue

            if isinstance(prop, Metric):
                yield prop
