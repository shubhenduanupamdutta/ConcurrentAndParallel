import random
from datetime import UTC, datetime
from multiprocessing.queues import Queue as QueueType
from threading import Thread
from typing import Any, override

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .queue_types import PostgresQueueItem


class NYSEFinancePriceScheduler(Thread):
    def __init__(
        self,
        input_queue: QueueType[str],
        output_queue: QueueType[PostgresQueueItem],
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._output_queue = output_queue
        self.start()

    @override
    def run(self) -> None:
        while True:
            symbol = self._input_queue.get()
            if symbol == "DONE":
                print("Received DONE signal. Exiting NYSEFinancePriceScheduler.")
                break
            finance_worker = NYSEFinanceWorker(symbol)
            price = finance_worker.get_price()
            self._output_queue.put((symbol, price, datetime.now(UTC)))
            print(f"{symbol}: {price}")


class NYSEFinanceWorker:
    def __init__(self, symbol: str) -> None:
        self._symbol = symbol
        base_url = "https://www.nyse.com/quote/XNYS:"
        self._url = f"{base_url}{self._symbol}"
        self.xpath = """//*[@id="integration-id-04b1814"]/section[1]/div/div[2]/div/div[1]/div[2]/div[1]/div[1]/p"""  # noqa: E501

    def create_headless_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def get_price(self) -> float | None:
        driver = self.create_headless_driver()
        driver.get(self._url)

        # try:
        #     wait = WebDriverWait(driver, timeout=120, poll_frequency=20)
        #     wait.until(lambda d: d.find_element(By.XPATH, self.xpath).text.strip() != "")
        # except TimeoutException:
        #     print(f"Timeout while waiting for price to load for {self._symbol}")
        #     driver.quit()
        #     return

        driver.implicitly_wait(random.randint(20, 40))
        try:
            price = driver.find_element(By.XPATH, self.xpath).text.strip()
            float_price = float(price.replace(",", ""))
        except NoSuchElementException:
            print(f"Price element not found for symbol {self._symbol}")
            float_price = None
        except ValueError:
            print(f"Failed to convert price to float for symbol {self._symbol}")
            float_price = None
        finally:
            driver.quit()

        return float_price
