import asyncio


async def async_sleep(process_index: int) -> None:
    print(f"Before sleeping... {process_index}")
    await asyncio.sleep(5)
    print(f"After sleeping... {process_index}")

async def print_hello() -> None:
    print("Hello world!")


# How to run the above function


async def main() -> None:
    task = asyncio.create_task(async_sleep(1))
    await async_sleep(2)
    await task
    await print_hello()


if __name__ == "__main__":
    asyncio.run(main())
