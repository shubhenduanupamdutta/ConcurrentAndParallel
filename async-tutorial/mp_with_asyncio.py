import asyncio
from multiprocessing import Process


class MultiprocessingWithAsyncio(Process):
    def __init__(self, durations: list[int]) -> None:
        super().__init__()
        self._durations = durations

    @staticmethod
    async def async_sleep(duration: float) -> float:
        await asyncio.sleep(duration)
        return duration

    async def consecutive_sleeps(self) -> None:
        pending: set[asyncio.Task[float]] = set()
        for duration in self._durations:
            pending.add(asyncio.create_task(self.async_sleep(duration)))

        while pending:
            done, pending = await asyncio.wait(pending, timeout=1)
            for done_task in done:
                print(f"Task with duration {await done_task} is done")

    def run(self) -> None:
        asyncio.run(self.consecutive_sleeps())


# Using this we can start multiple event loops
if __name__ == "__main__":
    durations = list(range(1, 11))
    processes = [MultiprocessingWithAsyncio(durations[i * 5 : (i + 1) * 5]) for i in range(2)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
