# Current Price Tracker

---

This project is a simple app to demonstrate practical use of `threading` in Python. It gets S&P 500 stock names from Wikipedia and tracks their current prices from yahoo finance.

---

## Scheduler-Worker Pattern

---

This pattern allows us to decouple the task of generating work items from the task of processing them. In this project, we have a `NYSEFinancePriceScheduler` that generates stock symbols and multiple `NYSEFinanceWorker` threads that consume these symbols to fetch their current prices.
This allows us to explicitly maintain number of workers which are working on the queue.

---

## Why multiple output queues?

---

In `NYSEFinancePriceScheduler`

```python
class NYSEFinancePriceScheduler(Thread):
    def __init__(
        self,
        input_queue: SymbolQueue,
        output_queues: list[PostgresQueue] | PostgresQueue,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._output_queues = output_queues if isinstance(output_queues, list) else [output_queues]
        self.start()

    @override
    def run(self) -> None:
        while True:
            try:
                symbol = self._input_queue.get(timeout=120)
            except Empty:
                print("Timeout while waiting for data. Exiting NYSEFinancePriceScheduler.")
                break

            if symbol == "DONE":
                print("Received DONE signal. Exiting NYSEFinancePriceScheduler.")
                break
            finance_worker = NYSEFinanceWorker(symbol)
            price = finance_worker.get_price()
            for output_queue in self._output_queues:
                output_queue.put((symbol, price, datetime.now(tz=UTC)))
            print(f"{symbol}: {price}")
```

We are going with multiple output queues, because this way we can support multiple database workers consuming the same data.
This will allow us to write on multiple databases, like redis, postgres, etc. without changing the scheduler code. We can just add more database workers and pass their queues to the scheduler.
