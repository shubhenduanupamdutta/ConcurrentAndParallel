from datetime import UTC, datetime
import time
from multiprocessing import Queue
from typing import TYPE_CHECKING

from workers.nyse_finance_worker import NYSEFinancePriceScheduler
from workers.postgres_worker import PostgresMasterScheduler, PostgresQueueItem
from workers.wiki_worker import WikiWorker

if TYPE_CHECKING:
    import threading


def main() -> None:
    symbol_queue: Queue = Queue()
    postgres_queue: Queue[PostgresQueueItem] = Queue()
    scraper_start_time = time.perf_counter()

    wiki_scraper = WikiWorker()
    nyse_finance_scheduler_threads: list[threading.Thread] = []

    number_of_nyse_finance_workers = 10

    for _ in range(number_of_nyse_finance_workers):
        nyse_finance_scheduler = NYSEFinancePriceScheduler(symbol_queue, postgres_queue)
        nyse_finance_scheduler_threads.append(nyse_finance_scheduler)

    postgres_scheduler_threads: list[threading.Thread] = []
    number_of_postgres_workers = 2
    for _ in range(number_of_postgres_workers):
        postgres_scheduler = PostgresMasterScheduler(postgres_queue)
        postgres_scheduler_threads.append(postgres_scheduler)

    for i, symbol in enumerate(wiki_scraper.get_sp_500_companies()):
        symbol_queue.put(symbol)
        if i > 10:  # noqa: PLR2004
            break

    for _ in range(len(nyse_finance_scheduler_threads)):
        symbol_queue.put("DONE")

    for thread in nyse_finance_scheduler_threads:
        thread.join()

    for _ in range(len(postgres_scheduler_threads)):
        postgres_queue.put(("DONE", None, datetime.now(UTC)))
    for thread in postgres_scheduler_threads:
        thread.join()

    scraper_end_time = time.perf_counter()
    print(f"Total time taken to scrape: {scraper_end_time - scraper_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
