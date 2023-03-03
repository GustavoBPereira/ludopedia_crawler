from sqlalchemy import Column, Integer, String, DateTime, Float, Sequence, func, select
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
    stmt = select(
        Product.leilao_id, Product.name, func.count()
    ).group_by(
        Product.name
    ).filter(
        Product.name.ilike('%' + name + '%')
    ).order_by(
        Product.name.asc()
    )
    return [{'id': product[0], 'name': product[1], 'quantity': product[2]} for product in session.execute(stmt)]


def filter_product_name_equals(name, not_sold):
    session = DBSession()
    stmt = select(
        Product._id,
        Product.leilao_id,
        Product.title,
        Product.finish_at,
        Product.name,
        Product.price,
        Product.state
    ).filter(
        Product.name.ilike(name)
    ).order_by(
            Product.price.asc()
    )
    if not not_sold:
        stmt = stmt.filter(Product.price > 0)
    return products_to_json(session.execute(stmt))
