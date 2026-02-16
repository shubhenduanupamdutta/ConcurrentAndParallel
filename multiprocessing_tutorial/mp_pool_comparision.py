from multiprocessing import Pool, cpu_count


def check_number_value_in_range(comparison_list: list[float], lower: int, upper: int) -> int:
    number_of_hits = 0
    for i in range(lower, upper):
        if i in comparison_list:
            number_of_hits += 1
    return number_of_hits


cpu_cores_to_use = max(1, cpu_count() - 1)
print(f"Number of CPU cores available: {cpu_count()}")
print(f"Using {cpu_cores_to_use} cores for multiprocessing.\n")

# Using Processes
print("Starting process-based comparison...")

lower_ranges = (i * 10**6 for i in [0, 25, 50, 75])
upper_ranges = ((i + 25) * 10**6 for i in [0, 25, 50, 75])
comparison_list = [[1, 2, 3] for i in range(4)]

with Pool(cpu_cores_to_use) as mp_pool:
    results = mp_pool.starmap(
        check_number_value_in_range,
        zip(comparison_list, lower_ranges, upper_ranges, strict=True),
    )

print(f"Results: {results}")
print("Ending process-based comparison...")
