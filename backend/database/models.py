from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from sqlalchemy.orm import relationship

from database.db import Base

## Definição do Usuário
class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, primary_key=True)
	hashed_password = Column(String)

## Definição da Empresa
class Company(Base):
	__tablename__ = 'companies'

	id = Column(Integer, primary_key=True, index=True)
	symbol = Column(String, unique=True, index=True)
	name = Column(String)
	region = Column(String)
	marketOpen = Column(String)
	marketClose = Column(String)
	currency = Column(String)

	prices = relationship("Price")

## Definição da Cotação
class Price(Base):
	__tablename__ = 'prices'

	id = Column(Integer, primary_key=True, index=True)
	open = Column(Float)
	high = Column(Float)
	low = Column(Float)
	price = Column(Float)
	volume = Column(Integer)
	latest_trading_day = Column(String)
	previous_close = Column(Float)
	change = Column(Float)
	change_percent = Column(Float)

	company_id = Column(Integer, ForeignKey('companies.id'))