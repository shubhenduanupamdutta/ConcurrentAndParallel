from pathlib import Path

from yaml_reader import YamlPipelineExecutor


def main() -> None:
    current_file_location = Path(__file__).parent
    pipeline_location = current_file_location / "pipelines" / "wiki_nyse_scraper_pipeline.yaml"

    yaml_pipeline_executor = YamlPipelineExecutor(pipeline_location)
    yaml_pipeline_executor.process_pipeline()

    nyse_finance_workers = yaml_pipeline_executor._workers.get("NYSEFinanceWorker", [])  # noqa: SLF001
    for thread in nyse_finance_workers:
        thread.join()

    for _ in range(20):
        yaml_pipeline_executor._queues["PostgresQueue"].put("DONE")  # noqa: SLF001

    postgres_scheduler_threads = yaml_pipeline_executor._workers.get("PostgresWorker", [])  # noqa: SLF001
    for thread in postgres_scheduler_threads:
        thread.join()


if __name__ == "__main__":
    main()
