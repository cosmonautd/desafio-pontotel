from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## URI da instância PostgreSQL
POSTGRES_DB_URL = 'postgresql+psycopg2://postgres:PLACEHOLDER_PASSWORD@bovespa-empresas-database:5432/postgres'

## Conexão ao BD
engine = create_engine(POSTGRES_DB_URL)

# Configura uma sessão
SessionLocal = sessionmaker(engine)

## Configura modo declarativo usando classes para as definições das tabelas no BD
Base = declarative_base()

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
