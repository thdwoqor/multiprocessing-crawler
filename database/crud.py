import uuid

from database.schema import Product, Store, Work


def create_store(db_session, name):
    store = Store(name=name)
    db_session.add(store)
    db_session.commit()
    db_session.close()


def create_work(db_session, name):
    pk = str(uuid.uuid4())
    work = Work(uuid=pk, name=name)
    db_session.add(work)
    db_session.commit()
    db_session.close()
    return pk


def create_product(db_session, url, seller, company, title, price, product_uuid):
    store = Product(url=url, seller=seller, brand=company, name=title, price=price, uuid=product_uuid)
    db_session.add(store)
    db_session.commit()
    db_session.close()
