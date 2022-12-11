import re
import time
from multiprocessing import Queue

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.crawler import Crawler


class Crawler_Gmarket(Crawler):
    def get_url(self, keyword: str, max: int, url: Queue):
        self.set()
        sum = 0

        for page in range(1, 15):
            try:
                self.driver.get(f"https://browse.gmarket.co.kr/search?keyword={keyword}&s=8&k=0&p={page}")
                time.sleep(1)
                links = self.driver.find_elements(By.XPATH, '//*[@id="section__inner-content-body-container"]/div/div/div/div/a')

                for element in links:
                    url.put(element.get_attribute("href"))
                    sum += 1
                    if sum >= max * 1.1:
                        raise Exception("max")
            except Exception as e1:
                break
        print(f"url 수집 개수 : {sum}")
        return

    def get_data(self, sum: int, max: int, queue, lock, uuid: str):
        from database.conn import db
        from database.crud import create_product

        self.set()
        while not queue.empty():
            try:
                seller = title = price = company = "Unknown"

                lock.acquire()
                sum.value += 1
                url = queue.get()
                print(sum.value)
                lock.release()
                if sum.value > max:
                    self.driver.quit()
                    break

                self.driver.get(url)

                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "itemtit")))
                    title = self.driver.find_element(By.CLASS_NAME, "itemtit").text
                except Exception:
                    print("No such title")
                    print(url)
                try:
                    price = self.driver.find_element(By.CLASS_NAME, "price_real").text
                except Exception:
                    print("No such price")
                    print(url)
                try:
                    self.driver.find_element(
                        By.CSS_SELECTOR, "#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content > " "div.box__product-notice-more > button"
                    ).send_keys(Keys.ENTER)
                    brand_search = getattr(
                        self.driver.find_element(
                            By.CSS_SELECTOR,
                            "#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content.on > "
                            "div.box__product-notice-list > table:nth-child(1) > tbody > tr:nth-child(7) > th",
                        ),
                        "text",
                        None,
                    )

                    if brand_search == "브랜드":
                        brand = getattr(
                            self.driver.find_element(
                                By.CSS_SELECTOR,
                                "#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice."
                                "js-toggle-content.on > div.box__product-notice-list > table:nth-child(1) > tbody > "
                                "tr:nth-child(7) > td",
                            ),
                            "text",
                            None,
                        )
                    else:
                        brand = "정보 없음"

                    if brand == "상세설명 참조":
                        brand = "정보 없음"
                    brand = re.sub(r"^\s+|\s+$", "", brand)
                except Exception:
                    print("No such brand")
                    print(url)

                try:
                    create_product(db.session, url, seller, company, title, price, uuid)
                except Exception as e1:
                    print(e1)
            except:
                break
