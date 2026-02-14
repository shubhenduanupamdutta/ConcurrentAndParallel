import importlib
from multiprocessing import Queue
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    from threading import Thread

    from cur_price_tracker.workers.queue_types import QueueType


class YamlPipelineExecutor:
    def __init__(self, pipeline_location: str | Path) -> None:
        self._pipeline_location = Path(pipeline_location)
        self._yaml_data: dict[str, Any] = {}
        self._queues: dict[str, QueueType[Any]] = {}
        self._workers: dict[str, list[Thread]] = {}

    def _load_pipeline(self) -> None:
        with self._pipeline_location.open(mode="r", encoding="utf-8") as f:
            self._yaml_data = yaml.safe_load(f)

    def _initialize_queues(self) -> None:
        for queue in self._yaml_data.get("queues", []):
            queue_name = queue["name"]
            self._queues[queue_name] = Queue()

    def _initialize_workers(self) -> None:
        for worker in self._yaml_data.get("workers", []):
            worker_class: type[Thread] = getattr(
                importlib.import_module(worker["location"]),
                worker["class"],
            )
            input_queue = worker.get("input_queue")
            output_queues = worker.get("output_queues", [])
            worker_name = worker["name"]
            num_instance = worker.get("instances", 1)

            init_params: dict[str, Any] = {
                "input_queue": self._queues[input_queue] if input_queue else None,
            }
            if output_queues:
                init_params["output_queues"] = [self._queues[oq] for oq in output_queues]

            input_values = worker.get("input_values", [])
            if input_values:
                init_params["input_values"] = input_values

            self._workers[worker_name] = [worker_class(**init_params) for i in range(num_instance)]  # type: ignore[arg-type]

    def _join_workers(self) -> None:
        for workers in self._workers.values():
            for worker_thread in workers:
                worker_thread.join()

    def process_pipeline(self) -> None:
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()
        # self._join_workers()
