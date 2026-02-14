import os
import sys
import time

from dotenv import load_dotenv
from yaml_reader import YamlPipelineExecutor

load_dotenv()


def main() -> None:
    pipeline_location = os.getenv("PIPELINE_LOCATION")
    if not pipeline_location:
        print(
            "Pipeline location not set in environment variables. "
            "Please set PIPELINE_LOCATION and try again.",
        )
        sys.exit(1)

    scraper_start_time = time.perf_counter()

    yaml_pipeline_executor = YamlPipelineExecutor(pipeline_location)
    yaml_pipeline_executor.start()
    yaml_pipeline_executor.join()

    scraper_end_time = time.perf_counter()
    print(f"Total execution time: {scraper_end_time - scraper_start_time:.2f} seconds")


if __name__ == "__main__":
    main()
