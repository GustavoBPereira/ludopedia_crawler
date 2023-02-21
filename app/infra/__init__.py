from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker(autoflush=False))


def includeme(config):
    engine = create_engine(url='sqlite:///app/infra/db/leiloes.db')
    DBSession.configure(bind=engine)
