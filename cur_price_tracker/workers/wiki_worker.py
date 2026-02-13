from collections.abc import Generator
from typing import cast

import requests
from bs4 import BeautifulSoup


class WikiWorker:
    def __init__(self) -> None:
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def get_sp_500_companies(self) -> Generator[str]:
        response = requests.get(self._url, timeout=120)
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
