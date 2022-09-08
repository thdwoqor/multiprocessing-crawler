from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import mysql

from database.conn import Base, engine


class Store(Base):
    __tablename__ = "store"
    name = Column(mysql.VARCHAR(20), primary_key=True)


class Work(Base):
    __tablename__ = "work"
    uuid = Column(mysql.VARCHAR(200), primary_key=True)
    name = Column(mysql.VARCHAR(200), ForeignKey("store.name"))


class Product(Base):
    __tablename__ = "product"
    url = Column(mysql.VARCHAR(200))
    seller = Column(mysql.VARCHAR(20))
    brand = Column(mysql.VARCHAR(20))
    name = Column(mysql.VARCHAR(20))
    price = Column(mysql.INTEGER)
    uuid = Column(mysql.VARCHAR(200), ForeignKey("work.uuid"))

    __mapper_args__ = {"primary_key": [url, uuid]}


if __name__ == "__main__":
    Base.metadata.create_all(engine)
