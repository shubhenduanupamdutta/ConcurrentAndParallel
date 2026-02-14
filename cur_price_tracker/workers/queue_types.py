from datetime import datetime
from multiprocessing.queues import Queue as QueueType
from typing import Literal

type PostgresQueueItem = tuple[str, float | None, datetime] | Literal["DONE"]
type PostgresQueue = QueueType[PostgresQueueItem]
type SymbolQueue = QueueType[str]
