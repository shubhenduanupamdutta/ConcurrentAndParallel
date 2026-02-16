import asyncio
import time
from collections.abc import AsyncGenerator


async def async_sleep(process_index: int) -> AsyncGenerator[int]:
    print(f"Before sleeping... {process_index}")
    n = max(2, process_index)
    for i in range(1, n):
        yield i
        await asyncio.sleep(i)
    print(f"After sleeping... {process_index}")


async def print_hello() -> None:
    print("Hello world!")


# How to run the above function


async def main() -> None:
    start = time.perf_counter()
    async for k in async_sleep(5):
        print(f"Got value: {k}")
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())

