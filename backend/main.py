import enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules import config
from modules import alphavantage

from database import db
from database import models

app = FastAPI()

origins = [
    'http://localhost:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

@app.get('/')
async def root():
	"""
	"""
	return {'online': True}

class Period(str, enum.Enum):
	daily = 'daily'
	weekly = 'weekly'
	monthly = 'monthly'

@app.get('/bovespa/{period}')
async def bovespa(period: Period):
	"""
	"""

	alpha = alphavantage.AlphaVantage(api_key=config.get()['alphavantage_api_key'])

	if period == Period.daily:

		data, metadata = alpha.get_time_series_daily(symbol=config.get()['bovespa'])

		return {
			'success': True,
			'period': 'daily',
			'data': data, 
			'metadata': metadata
		}

	elif period == Period. weekly:

		data, metadata = alpha.get_time_series_weekly(symbol=config.get()['bovespa'])

		return {
			'success': True,
			'period': 'weekly',
			'data': data,
			'metadata': metadata
		}

	elif period == Period.monthly:

		data, metadata = alpha.get_time_series_monthly(symbol=config.get()['bovespa'])

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


@app.get('/companies')
async def list_companies():
	"""
	"""

	with db.transaction() as session:
		query = session.query(models.Company)
		companies = [db.serialize(q) for q in query.all()]

	return {'success': True, 'companies': companies}


@app.get('/search/{keywords}')
async def search(keywords: str):
	"""
	"""

	alpha = alphavantage.AlphaVantage(api_key=config.get()['alphavantage_api_key'])
	result = alpha.search(keywords=keywords)

	return {'success': True, 'result': result}


@app.get('/company/{symbol}/{period}')
async def company(symbol: str, period: Period):
	"""
	"""

	alpha = alphavantage.AlphaVantage(api_key=config.get()['alphavantage_api_key'])

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