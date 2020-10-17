import requests
import json
import time
import datetime

import redis
from torrequest import TorRequest

ALPHAVANTAGE_URI = 'https://www.alphavantage.co/query'

def get(params, tor=False):
	"""
	"""

	if not tor:

		response = requests.get(ALPHAVANTAGE_URI, params=params)
		return response.json()

	else:

		proxies = {
			'http': 'socks5://bovespa-empresas-tor:9050',
			'https': 'socks5://bovespa-empresas-tor:9050'
		}

		# myip = requests.get('http://ipv4.plain-text-ip.com', proxies=proxies)
		# print(myip.text)

		response = requests.get(ALPHAVANTAGE_URI, params=params, proxies=proxies)
		return response.json()


class Alpha:

	def __init__(self, api_key, tor=False):
		"""
		"""
		self.api_key = api_key
		self.cache = redis.Redis('bovespa-empresas-redis')
		self.tor = tor
	

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

			response_json = get(params, tor=self.tor)

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

		response_json = get(params, tor=self.tor)
		data = response_json['bestMatches']

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

		response_json = get(params, tor=self.tor)
		data = response_json['Global Quote']

		data = self.__remove_prefix_quote__(data)

		return data


class AlphaMultiKeys:

	def __init__(self, api_keys, tor):
		"""
		"""
		self.api_keys = api_keys
		self.alpha_workers = [Alpha(api_key=k, tor=tor) for k in self.api_keys]
		self.number_of_workers = len(self.alpha_workers)
		self.index = -1


	def __increment_index__(self):
		"""
		"""
		self.index = (self.index + 1) % self.number_of_workers

	def get_time_series_daily(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_daily(symbol)


	def get_time_series_daily_adjusted(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_daily_adjusted(symbol)
	

	def get_time_series_weekly(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_weekly(symbol)
	

	def get_time_series_weekly_adjusted(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_weekly_adjusted(symbol)
	

	def get_time_series_monthly(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_monthly(symbol)
	

	def get_time_series_monthly_adjusted(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_monthly_adjusted(symbol)


	def get_time_series_intraday(self, symbol, interval='1min'):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_intraday(symbol, interval)

	
	def search(self, keywords):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].search(keywords)
	

	def get_quote(self, symbol):
		"""
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_quote(symbol)
