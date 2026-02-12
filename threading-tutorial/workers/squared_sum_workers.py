import threading
from typing import override


class SquaredSumWorker(threading.Thread):
    def __init__(self, n: int, **kwargs: str) -> None:
        self._n = n
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.start()

    def _calculate_sum_squares(self, n: int) -> None:
        sum_squares = sum(i**2 for i in range(n))
        print(sum_squares)

    @override
    def run(self) -> None:
        self._calculate_sum_squares(self._n)
