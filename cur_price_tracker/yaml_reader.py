import importlib
import time
from multiprocessing import Queue
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING, Any, override

import yaml

if TYPE_CHECKING:
    from cur_price_tracker.workers.queue_types import QueueType


class YamlPipelineExecutor(Thread):
    def __init__(self, pipeline_location: str | Path) -> None:
        super().__init__()
        self._pipeline_location = Path(pipeline_location)
        self._yaml_data: dict[str, Any] = {}
        self._queues: dict[str, QueueType[Any]] = {}
        self._workers: dict[str, list[Thread]] = {}
        self._queue_consumers: dict[str, int] = {}
        self._downstream_queues: dict[str, list[str]] = {}

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

            self._downstream_queues[worker_name] = output_queues
            if input_queue:
                self._queue_consumers[input_queue] = num_instance

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

    @override
    def run(self) -> None:  # noqa: C901
        self.process_pipeline()
        while True:
            total_workers_alive = 0
            # Monitoring
            worker_stats = []
            to_del = []
            for worker_name, workers in self._workers.items():
                total_worker_threads_alive = 0
                for worker_thread in workers:
                    if worker_thread.is_alive():
                        total_worker_threads_alive += 1
                total_workers_alive += total_worker_threads_alive
                # When all threads of a worker have finished their execution, we can send "DONE"
                # signal to downstream queues and remove the worker from the active workers list.
                if total_worker_threads_alive == 0:
                    downstream_queues = self._downstream_queues.get(worker_name, [])
                    for output_queue in downstream_queues:
                        number_of_consumers = self._queue_consumers.get(output_queue, 0)
                        for _ in range(number_of_consumers):
                            self._queues[output_queue].put("DONE")

                    to_del.append(worker_name)

                worker_stats.append((worker_name, total_workers_alive))
            print(worker_stats)

            if total_workers_alive == 0:
                print("All workers have finished execution. Exiting YamlPipelineExecutor.")
                break

            for worker_name in to_del:
                del self._workers[worker_name]

            queue_stats = []
            for queue_name, queue in self._queues.items():
                queue_stats.append((queue_name, queue.qsize()))
            print(queue_stats)

            time.sleep(5)
