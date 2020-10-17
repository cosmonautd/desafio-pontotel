from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Company
from database.models import Price
from database.models import Ibovespa

## URI da instância PostgreSQL
POSTGRES_DB_URL = 'postgresql+psycopg2://postgres:PLACEHOLDER_PASSWORD@bovespa-empresas-database:5432/postgres'

## Conexão ao BD
engine = create_engine(POSTGRES_DB_URL)

# Configura uma sessão
SessionLocal = sessionmaker(engine)

@contextmanager
def transaction():
    """Provide a transactional scope around a series of operations."""

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def serialize(db_object):
	"""
	"""

	obj_dict = dict(db_object.__dict__)
	obj_dict.pop('_sa_instance_state', None)
	return obj_dict


def list_companies(session):
	"""
	"""
	
	query = session.query(Company)
	companies = [serialize(q) for q in query.all()]

	return companies


def create_price(session, price):
	"""
	"""

	new_price = Price(
		open=float(price['open']),
		high=float(price['high']),
		low=float(price['low']),
		price=float(price['price']),
		volume=int(price['volume']),
		latest_trading_day=str(price['latest trading day']),
		previous_close=float(price['previous close']),
		change=float(price['change']),
		change_percent=float(price['change percent'][:-1]),
		company_symbol=str(price['symbol'])
	)

	session.add(new_price)

	return new_price

def create_ibovespa(session, ibovespa):
	"""
	"""

	new_ibovespa = Ibovespa(
		open=float(ibovespa['open']),
		high=float(ibovespa['high']),
		low=float(ibovespa['low']),
		price=float(ibovespa['price']),
		volume=int(ibovespa['volume']),
		latest_trading_day=str(ibovespa['latest trading day']),
		previous_close=float(ibovespa['previous close']),
		change=float(ibovespa['change']),
		change_percent=float(ibovespa['change percent'][:-1])
	)

	session.add(new_ibovespa)

	return new_ibovespa