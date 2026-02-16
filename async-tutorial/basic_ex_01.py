import asyncio


async def async_sleep() -> None:
    print("Before sleeping...")
    await asyncio.sleep(5)
    print("After sleeping...")


async def print_hello() -> None:
    print("Hello world!")


# How to run the above function


async def main() -> None:
    await async_sleep()
    await print_hello()


if __name__ == "__main__":
    asyncio.run(main())


# In this case all the process is still happening sequentially.
# We are waiting for the sleep to finish before we print hello world.
# This happens because inside the main function, we are awaiting the sleep to
# finish before we move to the next line of code.
# In the next examples, we will see how to run these concurrently.
