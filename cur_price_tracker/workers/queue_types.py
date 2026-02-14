from datetime import datetime

type PostgresQueueItem = tuple[str, float | None, datetime]
