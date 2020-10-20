import datetime

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Equity
from database.models import Quote


def get_dict(db_object):
	"""Converte um objeto do SQLAlchemy em um dicionário Python.

		Parâmetros:
			db_object (objeto SQLAlchemy): objeto a ser convertido

		Retorno:
			obj_dict (dict): objeto convertido em dicionário
	"""
	obj_dict = dict(db_object.__dict__)
	obj_dict.pop('_sa_instance_state', None)
	return obj_dict


class PostgreSQLDatabase:

	def __init__(self, uri):
		"""Inicializa o objeto PostgreSQLDatabase.

			Parâmetros:
				uri (str): URI de um banco de dados PostgreSQL
		"""
		self.uri = uri
		self.engine = None
		self.session_local = None


	def connect(self):
		"""Conecta o objeto ao banco de dados com base na URI definida."""
		self.engine = create_engine(self.uri)
		self.session_local = sessionmaker(self.engine)
	

	def disconnect(self):
		"""Desconecta o objeto do banco de dados."""
		self.engine.dispose()


	@contextmanager
	def transaction(self):
		"""Provê um escopo para realização de uma série de operações em uma transação."""
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
		"""Lista todos os patrimônios cadastrados.

			Parâmetros:
				session (SessionLocal): sessão do SQLAlchemy

			Retorno:
				equities (list): lista de patrimônios cadastrados
		"""
		query = session.query(Equity)
		equities = [get_dict(q) for q in query.all()]

		return equities


	def list_companies(self, session):
		"""Lista todos os patrimônios cadastrados que são do tipo empresa.

			Parâmetros:
				session (SessionLocal): sessão do SQLAlchemy

			Retorno:
				companies (list): lista de empresas cadastradas
		"""
		query = session.query(Equity).filter_by(type='company')
		companies = [get_dict(q) for q in query.all()]

		return companies


	def get_company(self, session, symbol):
		"""Obtém uma empresa a partir do símbolo de seu patrimônio.

			Parâmetros:
				session (SessionLocal): sessão do SQLAlchemy
				symbol (str): o símbolo do patrimônio da empresa

			Retorno:
				company (dict): dicionário com informações da empresa ou None, caso
					a empresa não tenha sido encontrada
		"""
		query = session.query(Equity).filter_by(type='company', symbol=symbol).first()

		if query is None: return None
		else: return get_dict(query)


	def create_quote(self, session, quote):
		"""Cria uma cotação.

			Parâmetros:
				session (SessionLocal): sessão do SQLAlchemy
				quote (dict): dicionário contendo as informações da cotação

			Retorno:
				new_quote (dict): reflexo da cotação cadastrada no banco de dados
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

		return get_dict(new_quote)


	def list_quotes(self, session, symbol):
		"""Lista todas as cotações de um patrimônio.

			Parâmetros:
				session (SessionLocal): sessão do SQLAlchemy
				symbol (str): o símbolo do patrimônio

			Retorno:
				quotes (list): lista de cotações cadastradas
		"""
		query = session.query(Quote).filter_by(equity_symbol=symbol)
		quotes = [get_dict(q) for q in query.all()]

		return quotes