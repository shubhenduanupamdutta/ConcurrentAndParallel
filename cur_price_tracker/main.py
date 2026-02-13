import time
from multiprocessing import Queue
from typing import TYPE_CHECKING

from workers.nyse_finance_worker import NYSEFinancePriceScheduler
from workers.wiki_worker import WikiWorker

if TYPE_CHECKING:
    import threading


def main() -> None:
    symbol_queue: Queue = Queue()
    scraper_start_time = time.perf_counter()

    wiki_scraper = WikiWorker()
    scheduler_threads: list[threading.Thread] = []

    number_of_workers = 10

    for _ in range(number_of_workers):
        nyse_finance_scheduler = NYSEFinancePriceScheduler(symbol_queue)
        scheduler_threads.append(nyse_finance_scheduler)

    for symbol in wiki_scraper.get_sp_500_companies():
        symbol_queue.put(symbol)

    for _ in range(len(scheduler_threads)):
        symbol_queue.put("DONE")

    for thread in scheduler_threads:
        thread.join()

    scraper_end_time = time.perf_counter()
    print(f"Total time taken to scrape: {scraper_end_time - scraper_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
