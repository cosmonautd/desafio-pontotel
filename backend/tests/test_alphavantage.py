import pytest

from modules import alphavantage
from modules import config


def test_alpha_constructor():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)
	assert alpha.api_key == config.get('alphavantage_api_keys')[0]
	assert alpha.tor == True

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[-1],
		tor=False
	)
	assert alpha.api_key == config.get('alphavantage_api_keys')[-1]
	assert alpha.tor == False


def test_alphamultikeys_constructor():

	alpha = alphavantage.AlphaMultiKeys(
		api_keys=config.get('alphavantage_api_keys'),
		tor=True
	)
	assert len(alpha.api_keys) == len(config.get('alphavantage_api_keys'))
	assert len(alpha.alpha_workers) == len(config.get('alphavantage_api_keys'))
	assert alpha.number_of_workers == len(config.get('alphavantage_api_keys'))
	assert alpha.alpha_workers[0].tor == True

	alpha = alphavantage.AlphaMultiKeys(
		api_keys=config.get('alphavantage_api_keys'),
		tor=False
	)
	assert len(alpha.api_keys) == len(config.get('alphavantage_api_keys'))
	assert len(alpha.alpha_workers) == len(config.get('alphavantage_api_keys'))
	assert alpha.number_of_workers == len(config.get('alphavantage_api_keys'))
	assert alpha.alpha_workers[0].tor == False


def test_remove_prefix_timeseries():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	data = {'2020-10-19': {
		'1. open': 5, '2. high': 4, '3. low': 3, '4. close': 2, '5. volume': 1}
	}
	exp_data = {'2020-10-19': {
		'open': 5, 'high': 4, 'low': 3, 'close': 2, 'volume': 1}
	}
	
	data = alpha.__remove_prefix_timeseries__(data)

	assert data == exp_data


def test_transform_number():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	data = {'2020-10-19': {
		'open': '5', 'high': '4', 'low': '3', 'close': '2', 'volume': '1'}
	}
	exp_data = {'2020-10-19': {
		'open': 5, 'high': 4, 'low': 3, 'close': 2, 'volume': 1}
	}

	data = alpha.__transform_number__(data)

	assert data == exp_data


def test_add_price_timeseries():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	data = {'2020-10-19': {
		'open': 5, 'high': 4, 'low': 3, 'close': 2, 'volume': 1}
	}
	exp_data = {'2020-10-19': {
		'open': 5, 'high': 4, 'low': 3, 'close': 2, 'volume': 1, 'price': 2}
	}

	data = alpha.__add_price_timeseries__(data)

	assert data == exp_data


def test_fix_metadata_keys():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	metadata = {
		'1. Information': '',
		'2. Symbol': '',
		'3. Last Refreshed': '',
		'4. Output Size': '',
		'5. Time Zone': ''
	}
	exp_metadata = {
		'information': '',
		'symbol': '',
		'last_refreshed': '',
		'output_size': '',
		'timezone': ''
	}

	metadata = alpha.__fix_metadata_keys__(metadata)

	assert metadata == exp_metadata


def test_remove_prefix_search():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	array = [{
		'1. symbol': '5', '2. name': '4', '3. type': '3', '4. region': '2',
		'5. marketOpen': '1', '6. marketClose': '0', '7. timezone': '0',
		'8. currency': '0', '9. matchScore': '0'
	}]
	exp_array = [{
		'symbol': '5', 'name': '4', 'type': '3', 'region': '2', 'market_open': '1',
		'market_close': '0', 'timezone': '0', 'currency': '0', 'match_score': '0'
	}]
	
	array = alpha.__remove_prefix_search__(array)

	assert array == exp_array


def test_remove_prefix_quote():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	data = {
		'01. symbol': '5', '02. open': '4', '03. high': '3', '04. low': '2',
		'05. price': '1', '06. volume': '0', '07. latest trading day': '0',
		'08. previous close': '0', '09. change': '0', '10. change percent': ''
	}
	exp_data = {
		'symbol': '5', 'open': '4', 'high': '3', 'low': '2',
		'price': '1', 'volume': '0', 'latest_trading_day': '0',
		'previous_close': '0', 'change': '0', 'change_percent': ''
	}
	
	data = alpha.__remove_prefix_quote__(data)

	assert data == exp_data


def test_cache():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	key, value = '123', {'key': 'value'}

	alpha.__save_to_cache__(key, value)

	value2 = alpha.__get_from_cache__(key, 10)

	assert value == value2



dataitem_fields = ['open', 'high', 'low', 'close', 'open', 'price']
metadata_fields = ['information', 'symbol', 'last_refreshed', 'output_size', 'timezone']

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def get_time_series_template(function, symbol, datafield, refresh, interval='1min'):

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	data, metadata = alpha.__get_time_series_generic__(
		function, symbol, datafield, refresh, interval
	)

	assert all(item in metadata for item in metadata_fields)
	for dataitem in data:
		assert all(item in data[dataitem] for item in dataitem_fields)

def test_get_time_series_daily():
	get_time_series_template(
		'TIME_SERIES_DAILY', 'BRDT3.SAO', 'Time Series (Daily)', 3600
	)

def test_get_time_series_weekly():
	get_time_series_template(
		'TIME_SERIES_WEEKLY', 'BRDT3.SAO', 'Weekly Time Series', 12*3600
	)

def test_get_time_series_monthly():
	get_time_series_template(
		'TIME_SERIES_MONTHLY', 'BRDT3.SAO', 'Monthly Time Series', 2*24*3600
	)

def test_get_time_series_daily_adjusted():
	get_time_series_template(
		'TIME_SERIES_DAILY_ADJUSTED', 'BRDT3.SAO', 'Time Series (Daily)', 3600
	)

def test_get_time_series_weekly_adjusted():
	get_time_series_template(
		'TIME_SERIES_WEEKLY_ADJUSTED', 'BRDT3.SAO',
		'Weekly Adjusted Time Series', 12*3600
	)

def test_get_time_series_monthly_adjusted():
	get_time_series_template(
		'TIME_SERIES_MONTHLY_ADJUSTED', 'BRDT3.SAO',
		'Monthly Adjusted Time Series', 2*24*3600
	)

def test_get_time_series_intraday():
	interval = '1min'
	get_time_series_template(
		'TIME_SERIES_INTRADAY', 'IBM',
		'Time Series (%s)' % (interval), 2*24*3600, interval
	)


search_fiels = ['symbol', 'name', 'type', 'region', 'market_open', 'market_close',
	'timezone', 'currency', 'match_score']

def test_search():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	result = alpha.search('IBM')

	assert result[0]['symbol'] == 'IBM'
	assert result[0]['type'] == 'Equity'
	assert result[0]['currency'] == 'USD'

	for r in result:
		assert all(item in r for item in search_fiels)


quote_fields = ['symbol', 'open', 'high', 'low', 'price', 'volume',
	'latest_trading_day', 'previous_close', 'change', 'change_percent'
]

def test_quote():

	alpha = alphavantage.Alpha(
		api_key=config.get('alphavantage_api_keys')[0],
		tor=True
	)

	quote = alpha.get_quote('IBM')

	assert all(item in quote for item in quote_fields)
	