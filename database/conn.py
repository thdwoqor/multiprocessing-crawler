import os
from urllib.parse import quote

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

pymysql.install_as_MySQLdb()

engine = create_engine(f"mysql+mysqldb://{os.environ.get('ID')}:%s@{os.environ.get('IP')}:{os.environ.get('PORT')}/{os.environ.get('DB')}" % quote(os.environ.get("PASSWORD")), convert_unicode=False)


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

# https://stackoverflow.com/questions/1423804/writing-a-connection-string-when-password-contains-special-characters
# https://stackoverflow.com/questions/47670078/java-cant-connect-to-mysql-if-password-contain-symbol
# https://blog.gilbok.com/how-to-use-dot-env-in-python/
