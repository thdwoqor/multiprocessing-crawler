import datetime

from dotenv import load_dotenv

from database.conn import db
from database.crud import create_work
from util.crawler_coupang import Crawler_Coupang
from util.mult import Mult

# load .env
load_dotenv()

keyword = "CPU"
max = 400
process = 1

if __name__ == "__main__":
    start = datetime.datetime.now()
    uuid = create_work(db.session, "coupang")
    print(uuid)
    crawler = Mult(keyword, max, uuid)
    crawler.create_process(Crawler_Coupang, process)
    end = datetime.datetime.now()
    print(end - start)
