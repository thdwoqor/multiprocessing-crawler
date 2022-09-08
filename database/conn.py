from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# pymysql.install_as_MySQLdb()

# engine = create_engine(f"mysql+mysqldb://{os.environ.get('ID')}:%s@{os.environ.get('IP')}:{os.environ.get('PORT')}/{os.environ.get('DB')}" % quote(os.environ.get("PASSWORD")), convert_unicode=False)


# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Base = declarative_base()

# https://stackoverflow.com/questions/1423804/writing-a-connection-string-when-password-contains-special-characters
# https://stackoverflow.com/questions/47670078/java-cant-connect-to-mysql-if-password-contain-symbol
# https://blog.gilbok.com/how-to-use-dot-env-in-python/


DATABASE = "sqlite:///sqlite.db"


class SQLite:
    def __init__(self):
        self._engine = None
        self._session = None
        database_url = DATABASE

        self._engine = create_engine(database_url, connect_args={"check_same_thread": False})
        # https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @property
    def session(self):
        return scoped_session(self._session)

    @property
    def engine(self):
        return self._engine


db = SQLite()
Base = declarative_base()
