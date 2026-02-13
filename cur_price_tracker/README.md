# Current Price Tracker

---

This project is a simple app to demonstrate practical use of `threading` in Python. It gets S&P 500 stock names from Wikipedia and tracks their current prices from yahoo finance.

---

## Scheduler-Worker Pattern

---

This pattern allows us to decouple the task of generating work items from the task of processing them. In this project, we have a `NYSEFinancePriceScheduler` that generates stock symbols and multiple `NYSEFinanceWorker` threads that consume these symbols to fetch their current prices.
This allows us to explicitly maintain number of workers which are working on the queue.
