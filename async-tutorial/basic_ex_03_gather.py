import asyncio


async def async_sleep(process_index: int) -> None:
    print(f"Before sleeping... {process_index}")
    await asyncio.sleep(5)
    print(f"After sleeping... {process_index}")


async def print_hello() -> None:
    print("Hello world!")


# How to run the above function


async def main() -> None:
    try:
        await asyncio.gather(
            asyncio.wait_for(async_sleep(1), timeout=5),
            async_sleep(2),
            print_hello(),
        )
    except TimeoutError:
        print("A task timed out")


if __name__ == "__main__":
    asyncio.run(main())
