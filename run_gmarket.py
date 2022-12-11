import datetime

from dotenv import load_dotenv

from database.conn import db
from database.crud import create_work
from util.crawler_gmarket import Crawler_Gmarket
from util.mult import Mult

# load .env
load_dotenv()

keyword = "CPU"
max = 400
process = 7

if __name__ == "__main__":
    start = datetime.datetime.now()
    uuid = create_work(db.session, "gmarket")
    print(uuid)
    crawler = Mult(keyword, max, uuid)
    crawler.create_process(Crawler_Gmarket, process)
    end = datetime.datetime.now()
    print(end - start)
