import datetime

from dotenv import load_dotenv

from database.conn import db
from database.crud import create_work
from util.crawler_11st import Crawler_11st
from util.mult import Mult

# load .env
load_dotenv()

keyword = "CPU"
max = 100
process = 7

if __name__ == "__main__":
    start = datetime.datetime.now()
    uuid = create_work(db.session, "11st")
    print(uuid)
    crawler = Mult(keyword, max, uuid)
    crawler.create_process(Crawler_11st, process)
    end = datetime.datetime.now()
    print(end - start)
