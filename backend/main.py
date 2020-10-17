import enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules import config
from modules import alphavantage

from database import db

app = FastAPI()

origins = [
    'http://localhost:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

alpha = alphavantage.AlphaMultiKeys(
	api_keys=config.get()['alphavantage_api_keys'],
	tor=True
)

class Period(str, enum.Enum):
	intraday = 'intraday'
	daily = 'daily'
	weekly = 'weekly'
	monthly = 'monthly'

@app.get('/')
async def root():
	"""
	"""
	return {'online': True}


@app.get('/companies')
async def list_companies():
	"""
	"""

	with db.transaction() as session:
		companies = db.list_companies(session)

	return {'success': True, 'companies': companies}


@app.get('/search/{keywords}')
async def search(keywords: str):
	"""
	"""

	result = alpha.search(keywords=keywords)

	return {'success': True, 'result': result}


@app.get('/equity/{symbol}/{period}')
async def equity(symbol: str, period: Period):
	"""
	"""

	if period == Period.daily:

		data, metadata = alpha.get_time_series_daily(symbol=symbol)

		return {
			'success': True,
			'period': 'daily',
			'data': data, 
			'metadata': metadata
		}

	elif period == Period. weekly:

		data, metadata = alpha.get_time_series_weekly(symbol=symbol)

		return {
			'success': True,
			'period': 'weekly',
			'data': data,
			'metadata': metadata
		}

	elif period == Period.monthly:

		data, metadata = alpha.get_time_series_monthly(symbol=symbol)

		return {
			'success': True,
			'period': 'monthly',
			'data': data,
			'metadata': metadata
		}
	
	else:

		return {
			'success': False
		}


@app.get('/quote/{symbol}')
async def search(symbol: str):
	"""
	"""

	data = alpha.get_quote(symbol=symbol)

	return {'success': True, 'data': data}