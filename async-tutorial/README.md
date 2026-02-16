# Notes on Asynchronous Programming in Python

---

Basically when async process starts, we start an **event loop** (a programming construct that waits for and dispatches events or messages in a program). The event loop runs in a single thread and manages the execution of asynchronous tasks, which are also called **coroutines**. When an asynchronous task is waiting for an I/O operation to complete, it yields control back to the event loop, allowing other tasks to run in the meantime. This allows for efficient handling of I/O-bound tasks without blocking the main thread.

In an asynchronous program, coroutines are defined using the `async def` syntax. To run coroutines concurrently, you use `asyncio.create_task()` to schedule them as Tasks, or `asyncio.gather()` to run multiple coroutines together. The `await` keyword is used to wait for a coroutine to complete and retrieve its result - it doesn't schedule concurrent execution, but rather pauses until the awaited operation finishes. When a coroutine awaits an I/O operation, it yields control back to the event loop, which can then run other tasks. The event loop manages the execution of these tasks and ensures they run efficiently without blocking each other.

Futures and Tasks are used to represent the result of an asynchronous operation that may not have completed yet. In Python's `asyncio`, a `Task` is a subclass of `Future` that wraps a coroutine for execution. In practice, you typically work with Tasks rather than raw Futures. A Future can be in one of these states: `PENDING` (not yet completed), `CANCELLED` (explicitly cancelled), or `FINISHED` (completed with a result or exception). While executing, a Future remains in the PENDING state until it completes. Tasks allow for managing the state of asynchronous operations and enable synchronization between concurrent tasks.

- `asyncio.run()` is a high-level function that runs the event loop until the given coroutine completes. It is used to execute an asynchronous program by starting the event loop and running the specified coroutine. When you call `asyncio.run()`, it creates a new event loop, runs the provided coroutine, and then closes the event loop once the coroutine has finished executing.

- By default, we can only have one event loop per thread. We are only going to be running this on one core and one thread.

---

## Running tasks concurrently

---

```python
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
```

In the above code, two `async_sleep` function are running concurrently because task is created using `asyncio.create_task()`. When the first `async_sleep(2)` is called, it starts executing and when it hits the `await asyncio.sleep(5)`, it yields control back to the event loop. At this point, the event loop can run other tasks, such as the `async_sleep(1)` task that was created earlier. This allows both sleep operations to run concurrently without blocking each other.

But we do need to await the task at some point after `async_sleep(2)` to ensure that it starts executing and when it waits only then the task is run. If we await the task before `async_sleep(2)`, then it will run sequentially and we won't get the benefits of concurrency.

`asyncio.create_task()` is used to schedule the execution of a coroutine as a Task. It allows you to run multiple coroutines concurrently by creating separate Tasks for each coroutine. When you create a Task using `asyncio.create_task()`, it is scheduled to run in the event loop, and you can await it later to retrieve its result or ensure it has completed.

```python
async def main() -> None:
    await asyncio.gather(async_sleep(1), async_sleep(2), print_hello())
```

- `asyncio.gather()` is a function that allows you to run multiple coroutines concurrently and wait for all of them to complete. It takes multiple coroutines as arguments and returns a single coroutine that completes when all the input coroutines have completed. This is useful for running several tasks at the same time and waiting for all of them to finish before proceeding.
- `asyncio.gather()` is a convenient way to run multiple coroutines concurrently without having to create separate Tasks for each one. It simplifies the code and allows you to easily manage multiple asynchronous operations.

- `async for` is used to iterate over asynchronous iterators, which are objects that implement the asynchronous iteration protocol. This allows you to process items from an asynchronous source, such as a stream of data or a sequence of events, without blocking the main thread. When you use `async for`, it automatically handles the asynchronous nature of the iteration and allows you to write code that is more readable and easier to manage. It works sequentially, but it allows you to yield control back to the event loop while waiting for the next item in the iteration, enabling other tasks to run concurrently.
