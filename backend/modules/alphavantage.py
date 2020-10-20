import requests
import json
import time
import datetime

import redis
from torrequest import TorRequest

ALPHAVANTAGE_URI = 'https://www.alphavantage.co/query'

def get(params, tor=True):
	"""Realiza chamadas à API do Alpha Vantage através do TOR

		Parâmetros:
			params (dict): parâmetros a serem enviados à API do Alpha Vantage
			tor (bool): flag indicando se o TOR deve ser usado

		Retorno:
			response_json (dict): corpo da resposta do Alpha Vantage
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
	"""Uma classe para intermediar as operações com a API do Alpha Vantage.

	Atributos
	----------
	api_key : str
		chave de API do Alpha Vantage
	tor : bool
		flag indicando se o TOR deve ser usado nas interações com Alpha Vantage
	cache : Redis
		objeto Redis para fazer caching de respostas do Alpha Vantage

	Métodos
	-------
	get_time_series_daily(symbol):
		Obtém série temporal diária de cotações de um patrimônio.
	get_time_series_daily_adjusted(symbol):
		Obtém série temporal diária ajustada de cotações de um patrimônio.
	get_time_series_weekly(symbol):
		Obtém série temporal semanal de cotações de um patrimônio.
	get_time_series_weekly_adjusted(symbol):
		Obtém série temporal semanal ajustada de cotações de um patrimônio.
	get_time_series_monthly(symbol):
		Obtém série temporal mensal de cotações de um patrimônio.
	get_time_series_monthly_adjusted(symbol):
		Obtém série temporal mensal ajustada de cotações de um patrimônio.
	get_time_series_intraday(symbol, interval='1min'):
		Obtém série temporal intraday de cotações de um patrimônio.
	search(keywords):
		Realiza busca entre os patrimônios cadastrados no Alpha Vantage.
	get_quote(symbol):
		Obtém a cotação mais atualizada de um patrimônio no Alpha Vantage.
	"""

	def __init__(self, api_key, tor=False):
		"""Construtor da classe Alpha.

			Parâmetros:
				api_key (str): chave de API do Alpha Vantage
				tor (bool): flag indicando se o TOR deve ser usado
		"""
		self.api_key = api_key
		self.tor = tor
		self.cache = redis.Redis('bovespa-empresas-redis')
	

	def __remove_prefix_timeseries__(self, data):
		"""Remove os prefixos numéricos dos dados do Alpha Vantage.

			Parâmetros:
				data (dict): dados retornados pelo Alpha Vantage

			Retorno:
				data (dict): dados com prefixos numéricos removidos
		"""
		for date in data:
			data[date]['open'] = data[date].pop('1. open', 0)
			data[date]['high'] = data[date].pop('2. high', 0)
			data[date]['low'] = data[date].pop('3. low', 0)
			data[date]['close'] = data[date].pop('4. close', 0)
			data[date]['volume'] = data[date].pop('5. volume', 0)

		return data


	def __transform_number__(self, data):
		"""Converte dados do Alpha Vantage de strings numéricas para números.

		Deve ser usado apenas depois da passagem por self.__remove_prefix_timeseries__()

			Parâmetros:
				data (dict): dados retornados pelo Alpha Vantage após remoção de prefixos

			Retorno:
				data (dict): dados com valores numéricos
		"""
		for date in data:
			for variable in data[date]:
				if 'volume' in variable:
					data[date][variable] = int(data[date][variable])
				else:
					data[date][variable] = float(data[date][variable])

		return data
	

	def __add_price_timeseries__(self, data):
		"""Adiciona informação de preço às cotações das séries temporais.

		Deve ser usado apenas depois da passagem por self.__remove_prefix_timeseries__()

			Parâmetros:
				data (dict): dados retornados pelo Alpha Vantage após remoção de prefixos

			Retorno:
				data (dict): dados com adição do campo de preço
		"""
		for date in data:
			data[date]['price'] = data[date]['close']

		return data
	

	def __fix_metadata_keys__(self, metadata):
		"""Conserta os campos dos metadados retornados pelo Alpha Vantage.

			Parâmetros:
				metadata (dict): metadados retornados pelo Alpha Vantage

			Retorno:
				metadata (dict): metadados com nomes dos campos normalizados
		"""
		metadata['information'] = metadata.pop('1. Information', 0)
		metadata['symbol'] = metadata.pop('2. Symbol', 0)
		metadata['last_refreshed'] = metadata.pop('3. Last Refreshed', 0)
		metadata['output_size'] = metadata.pop('4. Output Size', 0)
		metadata['timezone'] = metadata.pop('5. Time Zone', 0)

		return metadata


	def __remove_prefix_search__(self, array):
		"""Remove os prefixos numéricos dos dados da busca do Alpha Vantage.

			Parâmetros:
				array (list): lista de resultados retornada pelo Alpha Vantage

			Retorno:
				array (list): lista de resultados com campos normalizados
		"""
		for data in array:
			data['symbol'] = data.pop('1. symbol', 0)
			data['name'] = data.pop('2. name', 0)
			data['type'] = data.pop('3. type', 0)
			data['region'] = data.pop('4. region', 0)
			data['market_open'] = data.pop('5. marketOpen', 0)
			data['market_close'] = data.pop('6. marketClose', 0)
			data['timezone'] = data.pop('7. timezone', 0)
			data['currency'] = data.pop('8. currency', 0)
			data['match_score'] = data.pop('9. matchScore', 0)

		return array
	

	def __remove_prefix_quote__(self, data):
		"""Remove os prefixos numéricos dos dados de cotação do Alpha Vantage.

			Parâmetros:
				data (dict): informação de cotação retornada pelo Alpha Vantage

			Retorno:
				data (dict): informação de cotação com campos normalizados
		"""
		data['symbol'] = data.pop('01. symbol', 0)
		data['open'] = data.pop('02. open', 0)
		data['high'] = data.pop('03. high', 0)
		data['low'] = data.pop('04. low', 0)
		data['price'] = data.pop('05. price', 0)
		data['volume'] = data.pop('06. volume', 0)
		data['latest_trading_day'] = data.pop('07. latest trading day', 0)
		data['previous_close'] = data.pop('08. previous close', 0)
		data['change'] = data.pop('09. change', 0)
		data['change_percent'] = data.pop('10. change percent', 0)

		return data
	

	def __save_to_cache__(self, key, value):
		"""Armazena um valor no cache redis.

		O valor é armazenado junto a um timestamp para posterior verificação de sua idade.

			Parâmetros:
				key (str): chave do valor
				value (?): valor a ser armazenado
		"""
		entry = json.dumps({'value': value, 'timestamp': time.time()})
		self.cache.set(key, entry)
	

	def __get_from_cache__(self, key, refresh):
		"""Obtém valor armazenado no cache redis.

			Parâmetros:
				key (str): chave do valor
				refresh (int): idade máxima do valor em segundos; caso o valor seja mais
					antigo que refresh, o retorno é None

			Retorno:
				value (?): valor armazenado no cache sob a chave informada ou None, caso
					a chave não tenha sido encontrada ou o valor armazenado é mais antigo
					que o definido pelo parâmetro refresh
		"""
		entry = self.cache.get(key)

		if entry == None: return None
		else:
			entry = json.loads(entry)
			timestamp = entry['timestamp']
			if time.time() - timestamp > refresh:
				return None
			else:
				return entry['value']
	

	def __get_time_series_generic__(self, function, symbol, datafield, refresh, interval='1min'):
		"""Método auxiliar para requisições de séries temporais à API do Alpha Vantage.

			Parâmetros:
				function (str): nome da operação a ser executada no Alpha Vantage
				symbol (str): símbolo do patrimônio a ser buscado
				datafield (str): nome do campo em que os dados retornados são armazenados
					pela API do Alpha Vantage
				refresh (int): idade máxima, em segundos, do valor da resposta em cache;
					caso o valor seja mais antigo que refresh, uma nova requisição à
					API do Alpha Vantage é realizada
				interval (str): intervalo usado na operação TIME_SERIES_INTRADAY

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
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
		data = self.__add_price_timeseries__(data)

		metadata = self.__fix_metadata_keys__(metadata)

		return data, metadata


	def get_time_series_daily(self, symbol):
		"""Obtém série temporal diária de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_DAILY',
			symbol=symbol,
			datafield='Time Series (Daily)',
			refresh=3600
		)


	def get_time_series_daily_adjusted(self, symbol):
		"""Obtém série temporal diária ajustada de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_DAILY_ADJUSTED',
			symbol=symbol,
			datafield='Time Series (Daily)',
			refresh=3600
		)
	

	def get_time_series_weekly(self, symbol):
		"""Obtém série temporal semanal de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_WEEKLY',
			symbol=symbol,
			datafield='Weekly Time Series',
			refresh=12*3600
		)
	

	def get_time_series_weekly_adjusted(self, symbol):
		"""Obtém série temporal semanal ajustada de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_WEEKLY_ADJUSTED',
			symbol=symbol,
			datafield='Weekly Adjusted Time Series',
			refresh=12*3600
		)
	

	def get_time_series_monthly(self, symbol):
		"""Obtém série temporal mensal de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_MONTHLY',
			symbol=symbol,
			datafield='Monthly Time Series',
			refresh=2*24*3600
		)
	

	def get_time_series_monthly_adjusted(self, symbol):
		"""Obtém série temporal mensal ajustada de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
		"""

		return self.__get_time_series_generic__(
			function='TIME_SERIES_MONTHLY_ADJUSTED',
			symbol=symbol,
			datafield='Monthly Adjusted Time Series',
			refresh=2*24*3600
		)


	def get_time_series_intraday(self, symbol, interval='1min'):
		"""Obtém série temporal intraday de cotações de um patrimônio.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado
				interval (str): intervalo usado na operação

			Retorno:
				data (dict): dados da série temporal retornada pelo Alpha Vantage
				metadata (dict): metadados da série temporal
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
		"""Realiza busca entre os patrimônios cadastrados no Alpha Vantage.

			Parâmetros:
				keywords (str): chave de busca a ser utilizada

			Retorno:
				data (list): resultados da busca armazenados em uma lista
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
		"""Obtém a cotação mais atualizada de um patrimônio no Alpha Vantage.

			Parâmetros:
				symbol (str): símbolo do patrimônio a ser buscado

			Retorno:
				data (dict): as informações da cotação armazenadas em um dicionário
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
	"""Uma classe para interagir com a API do Alpha Vantage usando múltiplas chaves.

	Atributos
	----------
	api_keys : list
		lista de chaves de API do Alpha Vantage
	tor : bool
		flag indicando se o TOR deve ser usado nas interações com Alpha Vantage
	alpha_workers: list
		lista contendo os múltiplos objetos Alpha que serão iterados
	number_of_alpha_workers: int
		quantidade de objetos Alpha utilizados nas interações
	index: int
		índice do próximo objeto Alpha a ser utilizado para requisição

	Métodos
	-------
	get_time_series_daily(symbol):
		Obtém série temporal diária de cotações de um patrimônio.
	get_time_series_daily_adjusted(symbol):
		Obtém série temporal diária ajustada de cotações de um patrimônio.
	get_time_series_weekly(symbol):
		Obtém série temporal semanal de cotações de um patrimônio.
	get_time_series_weekly_adjusted(symbol):
		Obtém série temporal semanal ajustada de cotações de um patrimônio.
	get_time_series_monthly(symbol):
		Obtém série temporal mensal de cotações de um patrimônio.
	get_time_series_monthly_adjusted(symbol):
		Obtém série temporal mensal ajustada de cotações de um patrimônio.
	get_time_series_intraday(symbol, interval='1min'):
		Obtém série temporal intraday de cotações de um patrimônio.
	search(keywords):
		Realiza busca entre os patrimônios cadastrados no Alpha Vantage.
	get_quote(symbol):
		Obtém a cotação mais atualizada de um patrimônio no Alpha Vantage.
	"""

	def __init__(self, api_keys, tor):
		"""Construtor da classe AlphaMultiKeys.

			Parâmetros:
				api_keys (list): lista de chaves de API do Alpha Vantage
				tor (bool): flag indicando se o TOR deve ser usado
		"""
		self.api_keys = api_keys
		self.tor = tor
		self.alpha_workers = [Alpha(api_key=k, tor=self.tor) for k in self.api_keys]
		self.number_of_workers = len(self.alpha_workers)
		self.index = -1


	def __increment_index__(self):
		"""Incrementa o índice, selecionando o próximo objeto Alpha a ser usado."""
		self.index = (self.index + 1) % self.number_of_workers

	def get_time_series_daily(self, symbol):
		"""Executa o método get_time_series_daily() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_daily(symbol)


	def get_time_series_daily_adjusted(self, symbol):
		"""Executa o método get_time_series_daily_adjusted() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_daily_adjusted(symbol)
	

	def get_time_series_weekly(self, symbol):
		"""Executa o método get_time_series_weekly() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_weekly(symbol)
	

	def get_time_series_weekly_adjusted(self, symbol):
		"""Executa o método get_time_series_weekly_adjusted() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_weekly_adjusted(symbol)
	

	def get_time_series_monthly(self, symbol):
		"""Executa o método get_time_series_monthly() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_monthly(symbol)
	

	def get_time_series_monthly_adjusted(self, symbol):
		"""Executa o método get_time_series_monthly_adjusted() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_monthly_adjusted(symbol)


	def get_time_series_intraday(self, symbol, interval='1min'):
		"""Executa o método get_time_series_intraday() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_time_series_intraday(symbol, interval)

	
	def search(self, keywords):
		"""Executa o método search() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].search(keywords)
	

	def get_quote(self, symbol):
		"""Executa o método get_quote() do objeto Alpha.

		Os parâmetros e retornos são os mesmos documentados na classe Alpha.
		"""
		self.__increment_index__()
		return self.alpha_workers[self.index].get_quote(symbol)
