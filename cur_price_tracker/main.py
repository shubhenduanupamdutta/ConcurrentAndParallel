from pathlib import Path

from yaml_reader import YamlPipelineExecutor


def main() -> None:
    current_file_location = Path(__file__).parent
    pipeline_location = current_file_location / "pipelines" / "wiki_nyse_scraper_pipeline.yaml"

    yaml_pipeline_executor = YamlPipelineExecutor(pipeline_location)
    yaml_pipeline_executor.start()


if __name__ == "__main__":
    main()
