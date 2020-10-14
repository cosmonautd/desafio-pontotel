import enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from modules import config
from modules import alphavantage

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

	if period == Period.daily:

		alpha = alphavantage.AlphaVantage(api_key=config.get()['alphavantage_api_key'])
		data, metadata = alpha.get_time_series_daily(symbol=config.get()['bovespa'])

		return {'success': True, 'period': 'daily', 'data': data, 'metadata': metadata}

	elif period == Period. weekly:

		return {'success': True, 'period': 'weekly'}

	elif period == Period.monthly:

		return {'success': True, 'period': 'monthly'}
	
	else:

		return {'success': False}