from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Define modo declarativo usando classes para as definições das tabelas no BD
Base = declarative_base()

# Definição do usuário
class User(Base):
	__tablename__ = 'users'

	username = Column(String, primary_key=True, index=True)
	hashed_password = Column(String)

# Definição do patrimônio
class Equity(Base):
	__tablename__ = 'equities'

	symbol = Column(String, primary_key=True, index=True)
	name = Column(String)
	region = Column(String)
	market_open = Column(String)
	market_close = Column(String)
	currency = Column(String)
	type = Column(String)

	quotes = relationship('Quote')

# Definição da cotação
class Quote(Base):
	__tablename__ = 'quotes'

	id = Column(Integer, primary_key=True)
	open = Column(Float)
	high = Column(Float)
	low = Column(Float)
	price = Column(Float)
	volume = Column(Integer)
	latest_trading_day = Column(String)
	previous_close = Column(Float)
	change = Column(Float)
	change_percent = Column(Float)
	created_at = Column(DateTime(timezone=True))

	equity_symbol = Column(String, ForeignKey('equities.symbol'), index=True)