import re
import time
from multiprocessing import Queue

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.crawler import Crawler


class Crawler_Ebay(Crawler):
    def get_url(self, keyword: str, max: int, url: Queue):
        self.set()
        sum = 0

        for page in range(1, 15):
            try:
                self.driver.get(f"https://www.ebay.com/sch/i.html?_nkw={keyword}&_pgn={page}")
                time.sleep(1)
                links = self.driver.find_elements(By.CLASS_NAME, "s-item__link")

                for element in links[1:]:
                    url.put(element.get_attribute("href"))
                    sum += 1
                    if sum >= max:
                        raise Exception("max")
            except Exception as e1:
                print(e1)
                break
        print(f"url 수집 개수 : {sum}")
        self.driver.quit()

    def get_data(self, sum: int, max: int, queue, lock, uuid: str):
        from database.conn import db
        from database.crud import create_product

        self.set()
        time.sleep(15)
        while not queue.empty():
            seller = title = price = company = "Unknown"

            lock.acquire()
            url = queue.get()
            lock.release()
            self.driver.get(url)

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "vi-lkhdr-itmTitl")))
                title = self.driver.find_element(By.ID, "vi-lkhdr-itmTitl").get_attribute("textContent")
            except Exception:
                print("No such title")
                print(url)
            try:
                price = self.driver.find_element(By.CLASS_NAME, "notranslate").text
                price = re.sub(r"^\s+|\s+$", "", price)
            except Exception:
                print("No such price")
                print(url)
            try:
                company = self.driver.find_element(By.XPATH, "//span[@itemprop = 'brand']").text
            except Exception:
                print("No such company")
                print(url)

            try:
                create_product(db.session, url, seller, company, title, price, uuid)
            except Exception as e1:
                print(e1)
                print(url)

            lock.acquire()
            sum.value += 1
            print(sum.value)
            lock.release()

        self.driver.quit()
