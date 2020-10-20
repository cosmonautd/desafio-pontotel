import json

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)



def test_online():
	response = client.get('/')
	assert response.status_code == 200
	assert response.json() == {'online': True}



company_fields = [
	'symbol', 'region', 'market_close', 'market_open', 'type', 'name', 'currency'
]

def test_list_companies():
	response = client.get('/companies')
	rbody = response.json()
	assert response.status_code == 200
	assert rbody['success'] == True
	for company in rbody['companies']:
		assert all(item in company.keys() for item in company_fields)



def test_get_company_success():
	response = client.get('/company/BRDT3.SAO')
	rbody = response.json()
	assert response.status_code == 200
	assert rbody['success'] == True
	assert all(item in rbody['company'].keys() for item in company_fields)

def test_get_company_failure():
	response = client.get('/company/AAAAAA')
	rbody = response.json()
	assert response.status_code == 404
	assert rbody['success'] == False
	assert 'message' in rbody
	assert 'company' not in rbody



def test_search_success():
	response = client.get('/search/B3')
	rbody = response.json()
	first_result = rbody['result'][0]
	assert response.status_code == 200
	assert rbody['success'] == True
	assert first_result['symbol'] == 'B3SA3.SAO'
	assert first_result['currency'] == 'BRL'

def test_search_empty():
	response = client.get('/search/B4')
	rbody = response.json()
	assert response.status_code == 200
	assert rbody['success'] == True
	assert len(rbody['result']) == 0



dataitem_fields = ['open', 'high', 'low', 'close', 'open', 'price']
metadata_fields = ['information', 'symbol', 'last_refreshed', 'output_size', 'timezone']

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_template_success(symbol, period):
	response = client.get('/equity/%s/%s' % (symbol, period))
	rbody = response.json()
	assert response.status_code == 200
	assert rbody['success'] == True
	assert rbody['period'] == period
	assert all(item in rbody.keys() for item in ['data', 'metadata'])
	assert all(item in rbody['metadata'] for item in metadata_fields)
	for dataitem in rbody['data']:
		assert all(item in rbody['data'][dataitem] for item in dataitem_fields)

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_template_notfound(symbol, period):
	response = client.get('/equity/%s/%s' % (symbol, period))
	rbody = response.json()
	assert response.status_code == 404
	assert rbody['success'] == False
	assert 'message' in rbody
	assert 'data' not in rbody
	assert 'metadata' not in rbody

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_template_invalid_period(symbol, period):
	response = client.get('/equity/%s/%s' % (symbol, period))
	rbody = response.json()
	assert response.status_code == 422
	assert 'data' not in rbody
	assert 'metadata' not in rbody
	assert 'detail' in rbody
	assert rbody['detail'][0]['loc'][0] == 'path'
	assert rbody['detail'][0]['loc'][1] == 'period'

def test_equity_daily():
	equity_template_success('BRDT3.SAO', 'daily')

def test_equity_weekly():
	equity_template_success('BRDT3.SAO', 'weekly')
	
def test_equity_monthly():
	equity_template_success('BRDT3.SAO', 'monthly')

def test_equity_notfound():
	equity_template_notfound('BRDT3', 'daily')

def test_equity_invalid_period():
	equity_template_invalid_period('BRDT3.SAO', 'abcde')



realtime_dataitem_fields = ['price', 'high', 'latest_trading_day', 'previous_close',
	'change_percent', 'equity_symbol', 'low', 'open', 'volume', 'change', 'created_at']

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_realtime_template_success(symbol):
	response = client.get('/equity-realtime/%s' % (symbol))
	rbody = response.json()
	assert response.status_code == 200
	assert rbody['success'] == True
	assert all(item in rbody.keys() for item in ['data', 'metadata'])
	for dataitem in rbody['data']:
		assert all(item in rbody['data'][dataitem] for item in realtime_dataitem_fields)

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_realtime_template_notfound(symbol):
	response = client.get('/equity-realtime/%s' % (symbol))
	rbody = response.json()
	assert response.status_code == 404
	assert rbody['success'] == False
	assert 'message' in rbody
	assert 'data' not in rbody
	assert 'metadata' not in rbody

def test_equity_realtime_success():
	equity_realtime_template_success('BRDT3.SAO')

def test_equity_realtime_not_found():
	equity_realtime_template_notfound('BRDT3.')


# Teste para websocket não está funcionando ainda...
# @pytest.mark.skip(reason="Essa é uma função auxiliar")
# def quote_realtime_websocket_template(symbol):
# 	with client.websocket_connect('/quote/realtime/%s/ws' % (symbol)) as websocket:
# 		message = websocket.receive_json()
# 		assert message['equity_symbol'] == symbol
# 		websocket.close(code=1000)

# def test_quote_realtime_websocket():
# 	quote_realtime_websocket_template('BOVB11.SAO')