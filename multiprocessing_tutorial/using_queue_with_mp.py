import time
from multiprocessing import Process, Queue
from multiprocessing.queues import Queue as QueueType
from typing import Literal

type MPQueue = QueueType[tuple[int, int, int] | Literal["DONE"]]


def check_value_in_list(
    x: list[int],
    process_index: int,
    num_of_processes: int,
    queue: MPQueue,
) -> None:
    max_number_to_check_to = 10**8
    lower = process_index * (max_number_to_check_to // num_of_processes)
    upper = (process_index + 1) * (max_number_to_check_to // num_of_processes)

    number_of_hits = 0
    for i in range(lower, upper):
        if i in x:
            number_of_hits += 1

    queue.put((lower, upper, number_of_hits))


num_processes = 4
comparison_list = [1, 2, 3]
queue: MPQueue = Queue()


# Using Processes
print("Starting process-based comparison...")
start_time = time.perf_counter()
processes: list[Process] = []
for i in range(num_processes):
    p = Process(target=check_value_in_list, args=(comparison_list, i, num_processes, queue))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

queue.put("DONE")

while True:
    value = queue.get()
    if value == "DONE":
        break
    lower, upper, number_of_hits = value
    print(f"Between {lower} and {upper}, found {number_of_hits} hits.")


end_time = time.perf_counter()
print(f"Time taken with processes: {end_time - start_time:.2f} seconds")
print("Ending process-based comparison...")

# Time taken with processes: 7.52 seconds
