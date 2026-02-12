import threading
import time
from typing import override


class SleepyWorker(threading.Thread):
    def __init__(self, seconds: int, **kwargs: str) -> None:
        self._seconds = seconds
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.start()

    def _sleep_a_little(self) -> None:
        time.sleep(self._seconds)

    @override
    def run(self) -> None:
        self._sleep_a_little()
