import time
from pathlib import Path

from workers.wiki_worker import WikiWorker
from yaml_reader import YamlPipelineExecutor


def main() -> None:
    current_file_location = Path(__file__).parent
    pipeline_location = current_file_location / "pipelines" / "wiki_nyse_scraper_pipeline.yaml"
    yaml_pipeline_executor = YamlPipelineExecutor(pipeline_location)
    yaml_pipeline_executor.process_pipeline()
    # symbol_queue: SymbolQueue = Queue()
    # postgres_queue: PostgresQueue = Queue()
    scraper_start_time = time.perf_counter()

    wiki_scraper = WikiWorker()
    # nyse_finance_scheduler_threads: list[threading.Thread] = []

    # number_of_nyse_finance_workers = 10

    # for _ in range(number_of_nyse_finance_workers):
    #     nyse_finance_scheduler = NYSEFinancePriceScheduler(symbol_queue, [postgres_queue])
    #     nyse_finance_scheduler_threads.append(nyse_finance_scheduler)

    # postgres_scheduler_threads: list[threading.Thread] = []
    # number_of_postgres_workers = 2
    # for _ in range(number_of_postgres_workers):
    #     postgres_scheduler = PostgresMasterScheduler(postgres_queue)
    #     postgres_scheduler_threads.append(postgres_scheduler)

    for i, symbol in enumerate(wiki_scraper.get_sp_500_companies()):
        yaml_pipeline_executor._queues["SymbolQueue"].put(symbol)  # noqa: SLF001
        if i > 10:  # noqa: PLR2004
            break

    for _ in range(20):
        yaml_pipeline_executor._queues["SymbolQueue"].put("DONE")  # noqa: SLF001

    nyse_finance_workers = yaml_pipeline_executor._workers.get("NYSEFinanceWorker", [])  # noqa: SLF001
    for thread in nyse_finance_workers:
        thread.join()

    for _ in range(20):
        yaml_pipeline_executor._queues["PostgresQueue"].put("DONE")  # noqa: SLF001

    postgres_scheduler_threads = yaml_pipeline_executor._workers.get("PostgresWorker", [])  # noqa: SLF001
    for thread in postgres_scheduler_threads:
        thread.join()

    scraper_end_time = time.perf_counter()
    print(f"Total time taken to scrape: {scraper_end_time - scraper_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
