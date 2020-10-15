import requests
import json
import time
import datetime

import redis

from modules import config

ALPHAVANTAGE_URI = 'https://www.alphavantage.co/query'

class AlphaVantage:

	def __init__(self, api_key):
		"""
		"""
		self.api_key = api_key
		self.cache = redis.Redis('bovespa-empresas-redis')
	

	def __remove_prefix_timeseries__(self, data):
		"""
		"""

		for date in data:
			data[date]['open'] = data[date].pop('1. open', 0)
			data[date]['high'] = data[date].pop('2. high', 0)
			data[date]['low'] = data[date].pop('3. low', 0)
			data[date]['close'] = data[date].pop('4. close', 0)
			data[date]['volume'] = data[date].pop('5. volume', 0)

		return data


	def __transform_number__(self, data):
		"""
		"""

		for date in data:
			for variable in data[date]:
				if 'volume' in variable:
					data[date][variable] = int(data[date][variable])
				else:
					data[date][variable] = float(data[date][variable])

		return data
	

	def __remove_prefix_search__(self, array):
		"""
		"""

		for data in array:
			data['symbol'] = data.pop('1. symbol', 0)
			data['name'] = data.pop('2. name', 0)
			data['type'] = data.pop('3. type', 0)
			data['region'] = data.pop('4. region', 0)
			data['marketOpen'] = data.pop('5. marketOpen', 0)
			data['marketClose'] = data.pop('6. marketClose', 0)
			data['timezone'] = data.pop('7. timezone', 0)
			data['currency'] = data.pop('8. currency', 0)
			data['matchScore'] = data.pop('9. matchScore', 0)

		return array
	

	def __remove_prefix_quote__(self, data):
		"""
		"""

		data['symbol'] = data.pop('01. symbol', 0)
		data['open'] = data.pop('02. open', 0)
		data['high'] = data.pop('03. high', 0)
		data['low'] = data.pop('04. low', 0)
		data['price'] = data.pop('05. price', 0)
		data['volume'] = data.pop('06. volume', 0)
		data['latest trading day'] = data.pop('07. latest trading day', 0)
		data['previous close'] = data.pop('08. previous close', 0)
		data['change'] = data.pop('09. change', 0)
		data['change percent'] = data.pop('10. change percent', 0)

		return data
	

	def __get_from_cache__(self, key, refresh):
		"""
		"""

		entry = self.cache.get(key)

		if entry == None:
			return None
		else:
			entry = json.loads(entry)
			timestamp = entry['timestamp']
			if time.time() - timestamp > refresh:
				return None
			else:
				return entry['value']
	

	def __save_to_cache__(self, key, value):
		"""
		"""

		entry = json.dumps({'value': value, 'timestamp': time.time()})

		self.cache.set(key, entry)
	

	def __get_time_series_generic__(self, function, symbol, datafield, refresh,
		interval='1min'):
		"""
		"""

		params = {
			'function': function,
			'symbol': symbol,
			'apikey': self.api_key,
		}

		if function == 'TIME_SERIES_INTRADAY':
			params['interval'] = interval
			q = '%s-%s-%s' % (symbol, function, interval)
		else:
			q = '%s-%s' % (symbol, function)

		response_json = self.__get_from_cache__(q, refresh)

		if response_json == None:

			response = requests.get(ALPHAVANTAGE_URI, params=params)
			response_json = response.json()

			try:
				data = response_json[datafield]
				metadata = response_json['Meta Data']
			except:
				return None, None

			self.__save_to_cache__(q, response_json)
		
		else:

			data = response_json[datafield]
			metadata = response_json['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata


	def get_time_series_daily(self, symbol):
		"""
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_DAILY',
			symbol=symbol,
			datafield='Time Series (Daily)',
			refresh=3600
		)


	def get_time_series_daily_adjusted(self, symbol):
		"""
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_DAILY_ADJUSTED',
			symbol=symbol,
			datafield='Time Series (Daily)',
			refresh=3600
		)
	

	def get_time_series_weekly(self, symbol):
		"""
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_WEEKLY',
			symbol=symbol,
			datafield='Weekly Time Series',
			refresh=12*3600
		)
	

	def get_time_series_weekly_adjusted(self, symbol):
		"""
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_WEEKLY_ADJUSTED',
			symbol=symbol,
			datafield='Weekly Adjusted Time Series',
			refresh=12*3600
		)
	

	def get_time_series_monthly(self, symbol):
		"""
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_MONTHLY',
			symbol=symbol,
			datafield='Monthly Time Series',
			refresh=2*24*3600
		)
	

	def get_time_series_monthly_adjusted(self, symbol):
		"""
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_MONTHLY_ADJUSTED',
			symbol=symbol,
			datafield='Monthly Adjusted Time Series',
			refresh=2*24*3600
		)


	def get_time_series_intraday(self, symbol, interval='1min'):
		"""
		"""

		# Estranhamente, TIME_SERIES_INTRADAY não funciona com a Bovespa. Para
		# outros valores de symbol, como IBM, tudo funciona normalmente.

		return self.__get_time_series_generic__(
			function='TIME_SERIES_INTRADAY',
			symbol=symbol,
			datafield='Time Series (%s)' % (interval),
			refresh=60,
			interval=interval
		)

	
	def search(self, keywords):
		"""
		"""

		params = {
			'function': 'SYMBOL_SEARCH',
			'keywords': keywords,
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['bestMatches']

		data = self.__remove_prefix_search__(data)

		return data
	

	def get_quote(self, symbol):
		"""
		"""

		params = {
			'function': 'GLOBAL_QUOTE',
			'symbol': symbol,
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Global Quote']

		data = self.__remove_prefix_quote__(data)

		return data
