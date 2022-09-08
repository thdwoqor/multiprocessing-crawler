import time
from multiprocessing import Queue

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.crawler import Crawler


class Crawler_11st(Crawler):
    def get_url(self, keyword: str, max: int, url: Queue):
        self.set()
        sum = 0
        for page in range(1, 15):
            try:
                self.driver.get(f"https://search.11st.co.kr/Search.tmall?kwd={keyword}&fromACK=recent#sortCd%%I%%%EB%A7%8E%EC%9D%80%20%EB%A6%AC%EB%B7%B0%EC%88%9C%%1$$pageNum%%{page}%%")
                self.driver.refresh()
                time.sleep(1)
                elements = self.driver.find_elements(By.XPATH, '//*[@id="layBodyWrap"]/div/div/div/div/section/ul/li/div/div/a')

                for element in elements[:80]:
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
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layBodyWrap"]/div/div/div/div/div/div/h1/a')))
                seller = self.driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div/div/div/div/div/h1/a').text
            except Exception:
                print("No such seller")
            try:
                title = self.driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div/div/div/div/div/div/div/h1').text
            except Exception:
                print("No such title")
            try:
                price = self.driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div/div/div/div/div/div/div/div/div/ul/li/dl/dd/strong/span').text
            except Exception:
                print("No such price")
            try:
                tables = self.driver.find_elements(By.XPATH, '//*[@id="tabpanelDetail1"]/table/tbody/tr')
            except Exception:
                print("No such tables")

            for table in tables:
                if "브랜드" in table.text:
                    company = table.text.split()[1]
            try:
                create_product(db.session, url, seller, company, title, price, uuid)
            except Exception as e1:
                print(e1)
            lock.acquire()
            sum.value += 1
            print(sum.value)
            lock.release()

        self.driver.quit()
