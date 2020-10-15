import requests
import json

from modules import config

ALPHAVANTAGE_URI = 'https://www.alphavantage.co/query'

class AlphaVantage:

	def __init__(self, api_key):
		"""
		"""
		self.api_key = api_key
	

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


	def get_time_series_daily(self, symbol):
		"""
		"""

		params = {
			'function': 'TIME_SERIES_DAILY',
			'symbol': symbol,
			'outputsize': 'compact',
			'datatype': 'json',
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Time Series (Daily)']
		metadata = response.json()['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata
	

	def get_time_series_daily_adjusted(self, symbol):
		"""
		"""

		params = {
			'function': 'TIME_SERIES_DAILY_ADJUSTED',
			'symbol': symbol,
			'outputsize': 'compact',
			'datatype': 'json',
			'apikey': self.api_key
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Time Series (Daily)']
		metadata = response.json()['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata
	

	def get_time_series_weekly(self, symbol):
		"""
		"""

		params = {
			'function': 'TIME_SERIES_WEEKLY',
			'symbol': symbol,
			'datatype': 'json',
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Weekly Time Series']
		metadata = response.json()['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata
	

	def get_time_series_weekly_adjusted(self, symbol):
		"""
		"""

		params = {
			'function': 'TIME_SERIES_WEEKLY_ADJUSTED',
			'symbol': symbol,
			'datatype': 'json',
			'apikey': self.api_key
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Weekly Adjusted Time Series']
		metadata = response.json()['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata
	

	def get_time_series_monthly(self, symbol):
		"""
		"""

		params = {
			'function': 'TIME_SERIES_MONTHLY',
			'symbol': symbol,
			'datatype': 'json',
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Monthly Time Series']
		metadata = response.json()['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata
	

	def get_time_series_monthly_adjusted(self, symbol):
		"""
		"""

		params = {
			'function': 'TIME_SERIES_MONTHLY_ADJUSTED',
			'symbol': symbol,
			'datatype': 'json',
			'apikey': self.api_key
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Monthly Adjusted Time Series']
		metadata = response.json()['Meta Data']

		data = self.__remove_prefix_timeseries__(data)
		data = self.__transform_number__(data)

		return data, metadata


	def get_time_series_intraday(self, symbol, interval='5min'):
		"""
		"""

		# Estranhamente, TIME_SERIES_INTRADAY não funciona com a Bovespa. Para
		# outros valores de symbol, como IBM, tudo funciona normalmente.

		params = {
			'function': 'TIME_SERIES_INTRADAY',
			'symbol': symbol,
			'interval': interval,
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Time Series (%s)' % (interval)]
		metadata = response.json()['Meta Data']

		return data, metadata
	
	def search(self, keywords):
		"""
		"""

		params = {
			'function': 'SYMBOL_SEARCH',
			'keywords': keywords,
			'datatype': 'json',
			'apikey': self.api_key,
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['bestMatches']

		data = self.__remove_prefix_search__(data)

		return data
