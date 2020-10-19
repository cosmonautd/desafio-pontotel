import datetime

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Equity
from database.models import Quote

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


def list_equities(session):
	"""
	"""
	
	query = session.query(Equity)
	equities = [serialize(q) for q in query.all()]

	return equities


def list_companies(session):
	"""
	"""
	
	query = session.query(Equity).filter_by(type='company')
	companies = [serialize(q) for q in query.all()]

	return companies


def get_company(session, symbol):
	"""
	"""
	
	query = session.query(Equity).filter_by(type='company', symbol=symbol).first()

	if query is None: return None
	else: return serialize(query)


def create_quote(session, quote):
	"""
	"""

	new_quote = Quote(
		open=float(quote['open']),
		high=float(quote['high']),
		low=float(quote['low']),
		price=float(quote['price']),
		volume=int(quote['volume']),
		latest_trading_day=str(quote['latest trading day']),
		previous_close=float(quote['previous close']),
		change=float(quote['change']),
		change_percent=float(quote['change percent'][:-1]),
		created_at=datetime.datetime.now(datetime.timezone.utc),
		equity_symbol=str(quote['symbol'])
	)

	session.add(new_quote)

	return serialize(new_quote)


def list_quotes(session, symbol):
	"""
	"""

	query = session.query(Quote).filter_by(equity_symbol=symbol)
	quotes = [serialize(q) for q in query.all()]

	return quotes