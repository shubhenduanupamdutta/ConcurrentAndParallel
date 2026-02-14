import time
from multiprocessing import Process
from threading import Thread


def check_value_in_list(x: list[int]) -> None:
    for i in range(10**8):
        i in x  # pyright: ignore[reportUnusedExpression] # noqa: B015


num_threads = num_processes = 4
comparison_list = [1, 2, 3]


# Using Threads
print("Starting thread-based comparison...")
start_time = time.perf_counter()
threads: list[Thread] = []
for _ in range(num_threads):
    t = Thread(target=check_value_in_list, args=(comparison_list,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.perf_counter()
print(f"Time taken with threads: {end_time - start_time:.2f} seconds")

print("Ending thread-based comparison...\n")

# Time taken with threads: 19.62 seconds


# Using Processes
print("Starting process-based comparison...")
start_time = time.perf_counter()
processes: list[Process] = []
for _ in range(num_processes):
    p = Process(target=check_value_in_list, args=(comparison_list,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

end_time = time.perf_counter()
print(f"Time taken with processes: {end_time - start_time:.2f} seconds")
print("Ending process-based comparison...")

# Time taken with processes: 7.52 seconds
