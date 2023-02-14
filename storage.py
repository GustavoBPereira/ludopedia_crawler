
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Sequence, func

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    leilao_id = Column(Integer)
    title = Column(String)
    finish_at = Column(DateTime)
    name = Column(String)
    price = Column(Float)
    state = Column(String)


engine = create_engine('sqlite:///leiloes.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_product(leilao_id, title, finish_at, name, price, state):
    leilao = Product(leilao_id=leilao_id, title=title, finish_at=finish_at, name=name, price=price, state=state)
    session.add(leilao)
    session.commit()


def get_last_id():
    return session.query(func.max(Product.leilao_id+0)).first()[0]
