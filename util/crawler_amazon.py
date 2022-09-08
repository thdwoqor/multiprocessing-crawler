import time
from multiprocessing import Queue

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.crawler import Crawler


class Crawler_Amazon(Crawler):
    def get_url(self, keyword: str, max: int, url: Queue):
        self.set()

        self.driver.get(f"https://www.amazon.com/")

        search = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
        search.send_keys(keyword)
        self.driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()

        sum = 0
        for _ in range(1, 21):
            try:
                try:
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]/div/div/div/span/div/div/div/div/span/a')))
                    elements = self.driver.find_elements(By.XPATH, '//*[@id="search"]/div/div/div/span/div/div/div/div/div/div/div/div/div/div/div/h2/a')

                    for element in elements:
                        url.put(element.get_attribute("href"))
                        sum += 1
                        if sum >= max:
                            raise Exception("max")
                except Exception as e1:
                    print(e1)
                    break
                finally:
                    next = self.driver.find_elements(By.XPATH, '//*[@id="search"]/div/div/div/span/div/div/div/div/span/a')
                    next[-1].click()
            except Exception as e2:
                print(e2)
                break
        print(f"url 수집 개수 : {sum}")
        self.driver.quit()

    def get_data(self, sum: int, max: int, queue, lock, uuid: str):
        from database.conn import db
        from database.crud import create_product

        self.set()
        time.sleep(10)
        while not queue.empty():
            seller = title = price = company = "Unknown"

            lock.acquire()
            url = queue.get()
            lock.release()
            self.driver.get(url)

            try:
                element_text = None
                for _ in range(1000):
                    try:
                        element_text = self.driver.find_element(By.ID, "productTitle").text
                        if element_text is not None:
                            break
                    except Exception as e1:
                        print(e1)
                title = element_text
            except Exception:
                print("No such title")

            try:
                price = self.driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[2]/span[2]').text
            except Exception:
                print("No such price")

            create_product(db.session, url, seller, company, title, price, uuid)
            lock.acquire()
            sum.value += 1
            print(sum.value)
            lock.release()

        self.driver.quit()
