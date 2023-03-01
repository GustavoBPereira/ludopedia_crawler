from sqlalchemy import Column, Integer, String, DateTime, Float, Sequence, func
from sqlalchemy.orm import declarative_base

from app.infra import DBSession

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    _id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    leilao_id = Column(Integer)
    title = Column(String)
    finish_at = Column(DateTime)
    name = Column(String)
    price = Column(Float)
    state = Column(String)


def products_to_json(products):
    return [
        {
            'id': p._id,
            'leilao_id': p.leilao_id,
            'title': p.title,
            'finish_at': p.finish_at.isoformat(),
            'name': p.name,
            'price': p.price,
            'state': p.state
        } for p in products
    ]

def add_product(leilao_id, title, finish_at, name, price, state):
    session = DBSession()
    leilao = Product(leilao_id=leilao_id, title=title, finish_at=finish_at, name=name, price=price, state=state)
    session.add(leilao)
    session.commit()


def get_last_id():
    session = DBSession()
    return session.query(func.max(Product.leilao_id + 0)).first()[0] or 0


def filter_product_name_contains(name):
    session = DBSession()
    products = products_to_json(
        session.query(Product).group_by(Product.name).filter(Product.name.ilike('%' + name + '%')).order_by(Product.name.asc()).all())
    for product in products:
        del product['id']
        del product['leilao_id']
        del product['finish_at']
        del product['title']
        del product['price']
        del product['state']
        product['count_sold'] = session.query(Product).filter(Product.name.is_(product['name']),
                                                              Product.price > 0).count()
        product['count_not_sold'] = session.query(Product).filter(Product.name.is_(product['name']),
                                                                  Product.price.is_(0.0)).count()
    return products


def filter_product_name_equals(name, not_sold):
    session = DBSession()
    query = session.query(Product).filter(Product.name.ilike(name))
    if not not_sold:
        query = query.filter(Product.price > 0)
    return products_to_json(query.order_by(Product.price.asc()).all())
