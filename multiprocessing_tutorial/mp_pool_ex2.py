from functools import partial
from multiprocessing import Pool, cpu_count


def multiply(x: float, y: float) -> int | float:
    return x * y


x_values = [1, 3, 5, 7, 8, 10]
y_values = [2, 4, 6, 8, 9, 11]

num_cpu_to_use = max(1, cpu_count() - 1)
print(f"Number of CPU cores available: {cpu_count()}")
print(f"Using {num_cpu_to_use} cores for multiprocessing.\n")

with Pool(num_cpu_to_use) as mp_pool:
    result = mp_pool.starmap(multiply, zip(x_values, y_values, strict=True))

print(result)


# With fixed other arguments
# In following case, suppose y and z are fixed for the operation you want

print("\nUsing partial function to fix other arguments...\n")


def multiply_1(x: float, y: float, z: float) -> int | float:
    return (x + y) * z


partial_multiply = partial(multiply_1, y=10, z=5)
x_values = [1, 3, 5, 7, 8, 10]

with Pool(num_cpu_to_use) as mp_pool:
    result = mp_pool.map(partial_multiply, x_values)

print(result)
