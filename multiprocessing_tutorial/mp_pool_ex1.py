import time
from multiprocessing import Pool, cpu_count


def square(x: float) -> int | float:
    return x**2


num_processes = 4
comparison_list = [1, 2, 3]

num_cpu_to_use = max(1, cpu_count() - 1)
print(f"Number of CPU cores available: {cpu_count()}")
print(f"Using {num_cpu_to_use} cores for multiprocessing.\n")

start_time = time.perf_counter()

with Pool(num_cpu_to_use) as mp_pool:
    result = mp_pool.map(square, comparison_list)

print(result)

end_time = time.perf_counter()
print(f"Time taken: {end_time - start_time} seconds")
