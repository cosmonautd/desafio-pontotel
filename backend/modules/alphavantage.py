import requests
import json

from modules import config

ALPHAVANTAGE_URI = 'https://www.alphavantage.co/query'

class AlphaVantage:

	def __init__(self, api_key):
		"""
		"""
		self.api_key = api_key
	

	def __remove_prefix__(self, data):
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

		data = self.__remove_prefix__(data)
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

		data = self.__remove_prefix__(data)
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

		data = self.__remove_prefix__(data)
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

		data = self.__remove_prefix__(data)
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

		data = self.__remove_prefix__(data)
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

		data = self.__remove_prefix__(data)
		data = self.__transform_number__(data)

		return data, metadata


	def get_time_series_intraday(self, symbol, interval='5min'):
		"""
		"""

		# Estranhamente, TIME_SERIES_INTRADAY não funciona com a Bovespa. Para
		# outros valores de symbol, como IBM, tudo funciona normalmente.

		params = {
			'apikey': self.api_key,
			'function': 'TIME_SERIES_INTRADAY',
			'symbol': symbol,
			'interval': interval
		}

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		data = response.json()['Time Series (%s)' % (interval)]
		metadata = response.json()['Meta Data']

		return data, metadata


if __name__ == '__main__':

	alpha = AlphaVantage(api_key=config.get()['alphavantage_api_key'])

	ibm = config.get()['ibm']
	bovespa = config.get()['bovespa']

	data_daily_adjusted, _ = alpha.get_time_series_daily_adjusted(bovespa)

	print(data_daily_adjusted)