import time
from multiprocessing import Queue

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.crawler import Crawler


class Crawler_Coupang(Crawler):
    def get_url(self, keyword: str, max: int, url: Queue):
        self.set()
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            },
        )

        sum = 0

        for page in range(1, 30):
            try:
                self.driver.get(f"https://www.coupang.com/np/search?q={keyword}&channel=user&sorter=scoreDesc&listSize=36&isPriceRange=false&rating=0&page={page}&rocketAll=false")
                time.sleep(1)
                links = self.driver.find_elements(By.XPATH, "/html/body/div/section/form/div/div/ul/li/a")

                for element in links:
                    url.put(element.get_attribute("href"))
                    sum += 1
                    if sum >= max * 2:
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

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            },
        )

        time.sleep(15)
        while True:
            try:
                seller = title = price = company = "Unknown"

                if sum.value > max:
                    self.driver.quit()
                    break

                lock.acquire()
                url = queue.get()
                lock.release()
                time.sleep(5)
                self.driver.delete_all_cookies()
                self.driver.get(url)

                try:
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "prod-buy-header__title")))
                    title = self.driver.find_element(By.CLASS_NAME, "prod-buy-header__title").text
                except Exception:
                    continue
                try:
                    price = self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div/span[1]/strong').text
                except Exception:
                    print("No such price")
                try:
                    company = self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[3]/a').text
                except Exception:
                    print("No such company")

                print(sum.value)

                try:
                    create_product(db.session, url, seller, company, title, price, uuid)
                    sum.value += 1
                except Exception as e1:
                    print(e1)
            except:
                print("error")
                self.get_data(sum, max, queue, lock, uuid)
                break

        self.driver.quit()
