import random
import threading
import time
from typing import Any, override

import requests
from lxml import html


class YahooFinanceWorker(threading.Thread):
    def __init__(self, symbol: str, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(**kwargs)
        self._symbol = symbol
        base_url = "https://finance.yahoo.com/quote/"
        self._url = f"{base_url}{self._symbol}"
        self.start()

    @override
    def run(self) -> None:
        time.sleep(20 * random.random())
        response = requests.get(self._url, timeout=120)
        response.raise_for_status()
        page_contents = html.fromstring(response.text)
        price = float(
            page_contents.xpath(
                '//*[@id="main-content-wrapper"]/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/span[1]'  # noqa: COM812
            )[0].text,  # type: ignore[index, union-attr, arg-type]
        )
        print(price)
