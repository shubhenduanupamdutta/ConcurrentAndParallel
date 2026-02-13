import time
from typing import TYPE_CHECKING

from workers.wiki_worker import WikiWorker
from workers.yahoo_finance_worker import YahooFinanceWorker

if TYPE_CHECKING:
    import threading


def main() -> None:
    scraper_start_time = time.perf_counter()

    wiki_scraper = WikiWorker()
    current_workers: list[threading.Thread] = []
    for symbol in wiki_scraper.get_sp_500_companies():
        yahoo_finance_price_worker = YahooFinanceWorker(symbol)
        current_workers.append(yahoo_finance_price_worker)

    for worker in current_workers:
        worker.join()

    scraper_end_time = time.perf_counter()
    print(f"Total time taken to scrape: {scraper_end_time - scraper_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
