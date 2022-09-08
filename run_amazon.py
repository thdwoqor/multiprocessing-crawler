from dotenv import load_dotenv

from database.conn import db_session
from database.crud import create_work
from util.crawler_amazon import Crawler_Amazon
from util.mult import Mult

# load .env
load_dotenv()

keyword = "CPU"
max = 300
process = 1

if __name__ == "__main__":
    crawler = Mult(keyword, max, create_work(db_session, "11st"))
    crawler.create_process(Crawler_Amazon, process)
