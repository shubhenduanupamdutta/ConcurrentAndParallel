import os
from datetime import datetime
from queue import Empty
from threading import Thread
from typing import Any, override

from sqlalchemy import create_engine, text

from .queue_types import PostgresQueue


class PostgresMasterScheduler(Thread):
    def __init__(self, input_queue: PostgresQueue, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    @override
    def run(self) -> None:
        while True:
            try:
                val = self._input_queue.get(timeout=120)
            except Empty:
                print("Timeout while waiting for data. Exiting PostgresMasterScheduler.")
                break

            if val == "DONE":
                print("Received DONE signal. Exiting PostgresMasterScheduler.")
                break
            symbol, price, extracted_time = val
            postgres_worker = PostgresWorker(symbol, price, extracted_time)
            postgres_worker.insert_into_db()


class PostgresWorker:
    def __init__(self, symbol: str, price: float | None, extracted_time: datetime) -> None:
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        self.pg_user = os.getenv("PG_USER")
        self.pg_password = os.getenv("PG_PASSWORD")
        self.pg_host = os.getenv("PG_HOST", "localhost")
        self.pg_port = os.getenv("PG_PORT", "5432")
        self.pg_db = os.getenv("PG_DB")
        self.engine = create_engine(
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}",
        )

    def _create_insert_query(self) -> str:
        return """
        INSERT INTO stock_prices (symbol, price, extracted_time)
        VALUES (:symbol, :price, :extracted_time);
        """

    def insert_into_db(self) -> None:
        insert_query = self._create_insert_query()
        with self.engine.connect() as connection:
            connection.execute(
                text(insert_query),
                {
                    "symbol": self._symbol,
                    "price": self._price,
                    "extracted_time": self._extracted_time,
                },
            )
            connection.commit()
