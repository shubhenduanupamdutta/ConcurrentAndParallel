import threading
import time


def calculate_sum_squares(n: int) -> None:
    sum_squares = sum(i**2 for i in range(n))
    print(sum_squares)


def sleep_a_little(seconds: float) -> None:
    time.sleep(seconds)


def main() -> None:
    calc_start_time = time.perf_counter()
    cur_threads: list[threading.Thread] = []
    for seconds in range(5):
        max_value = (seconds + 1) * 1_000_000
        t = threading.Thread(target=calculate_sum_squares, args=(max_value,))
        t.start()
        cur_threads.append(t)

    for thread in cur_threads:
        thread.join()

    print(f"Calculating sum of square took: {time.perf_counter() - calc_start_time:.2f} seconds")

    sleep_start_time = time.perf_counter()
    cur_threads = []
    for seconds in range(1, 6):
        t = threading.Thread(target=sleep_a_little, args=(seconds,))
        t.start()
        # t.join() # t.join() here will block the execution and there will be no concurrency
        cur_threads.append(t)

    for thread in cur_threads:
        thread.join()
    print(f"Sleeping took: {time.perf_counter() - sleep_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
