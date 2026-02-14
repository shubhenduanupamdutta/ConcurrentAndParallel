from collections.abc import Generator
from threading import Thread
from typing import Any, cast, override

import requests
from bs4 import BeautifulSoup

from .queue_types import SymbolQueue


class WikiWorkerMasterScheduler(Thread):
    def __init__(self, output_queues: list[SymbolQueue] | SymbolQueue, **kwargs: Any) -> None:  # noqa: ANN401
        if "input_queue" in kwargs:
            kwargs.pop("input_queue")

        self._input_values = kwargs.pop("input_values", [])
        super().__init__(**kwargs)
        self._output_queues = output_queues if isinstance(output_queues, list) else [output_queues]
        self.start()

    @override
    def run(self) -> None:
        for entry in self._input_values:
            wiki_worker = WikiWorker(entry)

            for i, symbol in enumerate(wiki_worker.get_sp_500_companies()):
                for output_queue in self._output_queues:
                    output_queue.put(symbol)
                if i >= 10:  # noqa: PLR2004
                    break


class WikiWorker:
    def __init__(self, url: str) -> None:
        self._url = url

    def get_sp_500_companies(self) -> Generator[str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # noqa: E501
        }
        response = requests.get(self._url, headers=headers, timeout=120)
        response.raise_for_status()

        yield from self._extract_companies_from_wiki_page(response.text)

    @staticmethod
    def _extract_companies_from_wiki_page(html_content: str) -> Generator[str]:
        soup = BeautifulSoup(html_content, "lxml")
        table = soup.find(id="constituents")
        assert table is not None, "Failed to find the constituents table on the Wikipedia page."
        table_rows = table.find_all("tr")[1:]  # skip header row
        for table_row in table_rows:
            symbol_col = table_row.find("td")
            assert symbol_col is not None, "Failed to find symbol column in table row."
            symbol = cast("str", symbol_col.text).strip(" \n")
            yield symbol
