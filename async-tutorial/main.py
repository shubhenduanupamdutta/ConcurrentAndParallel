# Schedule 10 tasks and whenever one completes deal with it
import asyncio


async def async_sleep(duration: int) -> int:
    await asyncio.sleep(duration)
    return duration


async def main() -> None:
    pending = set()
    for i in range(1, 11):
        pending.add(asyncio.create_task(async_sleep(i)))

    # Default behavior of asyncio.wait is to wait until all tasks are done
    # done, pending = await asyncio.wait(pending)
    # print(done)
    # print(pending)

    # We can also specify to return with timeout, this means we will get a response after every
    # timeout seconds with the tasks that are done and the tasks that are still pending
    # while pending:
    #     done, pending = await asyncio.wait(pending, timeout=1)
    #     print(done)
    #     print(pending)
    #     print("----")

    # We can also loop over the done tasks and get the result of the task that is done,
    # this way we can deal with the tasks that are done as per the timeout
    # while pending:
    #     done, pending = await asyncio.wait(pending, timeout=2)
    #     for done_task in done:
    #         print(f"Task with duration {await done_task} is done")
    #     print(done)
    #     print(pending)
    #     print("----")

    # There is another parameter which can be used `return_when` which can be used to specify
    # when to return the done and pending tasks,
    # while pending:
    #     done, pending = await asyncio.wait(pending, return_when=asyncio.ALL_COMPLETED)
    #     for done_task in done:
    #         print(f"Task with duration {await done_task} is done")

    # asyncio.FIRST_COMPLETED will return as soon as any task is completed, this way we can deal
    # with the tasks that are done as soon as they are done
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for done_task in done:
            print(f"Task with duration {await done_task} is done")


if __name__ == "__main__":
    asyncio.run(main())
