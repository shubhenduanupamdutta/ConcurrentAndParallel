import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from threading import Thread

from workers.sleepy_workers import SleepyWorker
from workers.squared_sum_workers import SquaredSumWorker


def main() -> None:
    calc_start_time = time.perf_counter()
    cur_workers: list[Thread] = []
    for i in range(5):
        max_value = (i + 1) * 1_000_000
        t: Thread = SquaredSumWorker(n=max_value)
        cur_workers.append(t)

    for worker in cur_workers:
        worker.join()

    print(f"Calculating sum of square took: {time.perf_counter() - calc_start_time:.2f} seconds")

    sleep_start_time = time.perf_counter()
    cur_workers = []
    for seconds in range(1, 6):
        t = SleepyWorker(seconds=seconds)
        cur_workers.append(t)

    for worker in cur_workers:
        worker.join()
    print(f"Sleeping took: {time.perf_counter() - sleep_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
