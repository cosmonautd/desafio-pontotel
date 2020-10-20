import datetime

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Equity
from database.models import Quote

def serialize(db_object):
	"""
	"""

	obj_dict = dict(db_object.__dict__)
	obj_dict.pop('_sa_instance_state', None)
	return obj_dict

class PostgreSQLDatabase:

	def __init__(self, uri):
		self.uri = uri
		self.engine = None
		self.session_local = None

	def connect(self):
		"""
		"""

		## Conexão ao BD
		self.engine = create_engine(self.uri)

		# Configura uma sessão
		self.session_local = sessionmaker(self.engine)
	
	def disconnect(self):
		"""
		"""
		self.engine.dispose()

	@contextmanager
	def transaction(self):
		"""Provide a transactional scope around a series of operations."""

		session = self.session_local()
		try:
			yield session
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()

	def list_equities(self, session):
		"""
		"""
		
		query = session.query(Equity)
		equities = [serialize(q) for q in query.all()]

		return equities


	def list_companies(self, session):
		"""
		"""
		
		query = session.query(Equity).filter_by(type='company')
		companies = [serialize(q) for q in query.all()]

		return companies


	def get_company(self, session, symbol):
		"""
		"""
		
		query = session.query(Equity).filter_by(type='company', symbol=symbol).first()

		if query is None: return None
		else: return serialize(query)


	def create_quote(self, session, quote):
		"""
		"""

		new_quote = Quote(
			open=float(quote['open']),
			high=float(quote['high']),
			low=float(quote['low']),
			price=float(quote['price']),
			volume=int(quote['volume']),
			latest_trading_day=str(quote['latest_trading_day']),
			previous_close=float(quote['previous_close']),
			change=float(quote['change']),
			change_percent=float(quote['change_percent'][:-1]),
			created_at=datetime.datetime.now(datetime.timezone.utc),
			equity_symbol=str(quote['symbol'])
		)

		session.add(new_quote)

		return serialize(new_quote)


	def list_quotes(self, session, symbol):
		"""
		"""

		query = session.query(Quote).filter_by(equity_symbol=symbol)
		quotes = [serialize(q) for q in query.all()]

		return quotes