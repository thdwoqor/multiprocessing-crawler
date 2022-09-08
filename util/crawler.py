from abc import abstractmethod
from multiprocessing import Queue


class Crawler:
    def set(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        options.add_argument("user-agent=" + user_agent)
        options.add_argument("headless")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        self.driver.implicitly_wait(10)

    @abstractmethod
    def get_url(self, keyword: str, max: int, url: Queue):
        pass

    @abstractmethod
    def get_data(self, sum: int, max: int, queue, lock, uuid: str):
        pass
