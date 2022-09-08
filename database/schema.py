from sqlalchemy import INTEGER, VARCHAR, Column, ForeignKey

from database.conn import Base, db


class Store(Base):
    __tablename__ = "store"
    name = Column(VARCHAR(20), primary_key=True)


class Work(Base):
    __tablename__ = "work"
    uuid = Column(VARCHAR(200), primary_key=True)
    name = Column(VARCHAR(200), ForeignKey("store.name"))


class Product(Base):
    __tablename__ = "product"
    url = Column(VARCHAR(200))
    seller = Column(VARCHAR(20))
    brand = Column(VARCHAR(20))
    name = Column(VARCHAR(20))
    price = Column(INTEGER)
    uuid = Column(VARCHAR(200), ForeignKey("work.uuid"))

    __mapper_args__ = {"primary_key": [url, uuid]}


if __name__ == "__main__":
    Base.metadata.create_all(db.engine)
