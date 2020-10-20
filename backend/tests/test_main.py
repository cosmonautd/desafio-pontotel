import json

import pytest
from fastapi.testclient import TestClient

from main import app


def test_online():
	with TestClient(app) as client:
		response = client.get('/')
		assert response.status_code == 200 # status correto?
		assert response.json() == {'online': True} # resposta correta?


company_fields = [
	'symbol', 'region', 'market_close', 'market_open', 'type', 'name', 'currency'
]

def test_list_companies():
	with TestClient(app) as client:
		response = client.get('/companies')
		rbody = response.json()
		assert response.status_code == 200 # status correto?
		assert rbody['success'] == True # sucesso?
		for company in rbody['companies']: # todas as empresas contém os campos esperados?
			assert all(item in company.keys() for item in company_fields)

def test_get_company_success():
	with TestClient(app) as client:
		response = client.get('/company/BRDT3.SAO')
		rbody = response.json()
		assert response.status_code == 200 # status correto?
		assert rbody['success'] == True # sucesso?
		assert all(item in rbody['company'].keys() for item in company_fields) # campos esperados?

def test_get_company_failure():
	with TestClient(app) as client:
		response = client.get('/company/AAAAAA')
		rbody = response.json()
		assert response.status_code == 404 # status correto?
		assert rbody['success'] == False # falha?
		assert 'message' in rbody # contém mensagem?
		assert 'company' not in rbody # exclui empresa?


def test_search_success():
	with TestClient(app) as client:
		response = client.get('/search/B3')
		rbody = response.json()
		first_result = rbody['result'][0]
		assert response.status_code == 200 # status correto?
		assert rbody['success'] == True # sucesso?
		assert first_result['symbol'] == 'B3SA3.SAO' # símbolo correto?
		assert first_result['currency'] == 'BRL' # moeda correta?

def test_search_empty():
	with TestClient(app) as client:
		response = client.get('/search/B4')
		rbody = response.json()
		assert response.status_code == 200 # status correto?
		assert rbody['success'] == True # sucesso?
		assert len(rbody['result']) == 0 # nenhum valor como esperado?


dataitem_fields = ['open', 'high', 'low', 'close', 'open', 'price']
metadata_fields = ['information', 'symbol', 'last_refreshed', 'output_size', 'timezone']

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_template_success(symbol, period):
	with TestClient(app) as client:
		response = client.get('/equity/%s/%s' % (symbol, period))
		rbody = response.json()
		assert response.status_code == 200 # status correto?
		assert rbody['success'] == True # sucesso?
		assert rbody['period'] == period # período correto?
		assert all(item in rbody.keys() for item in ['data', 'metadata']) # campos corretos?
		assert all(item in rbody['metadata'] for item in metadata_fields) # metadados corretos?
		for dataitem in rbody['data']: # dados corretos?
			assert all(item in rbody['data'][dataitem] for item in dataitem_fields)

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_template_notfound(symbol, period):
	with TestClient(app) as client:
		response = client.get('/equity/%s/%s' % (symbol, period))
		rbody = response.json()
		assert response.status_code == 404 # status correto?
		assert rbody['success'] == False # falha?
		assert 'message' in rbody # contém mensagem?
		assert 'data' not in rbody # exclui dados?
		assert 'metadata' not in rbody # exclui metadados?

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_template_invalid_period(symbol, period):
	with TestClient(app) as client:
		response = client.get('/equity/%s/%s' % (symbol, period))
		rbody = response.json()
		assert response.status_code == 422 # status correto?
		assert 'data' not in rbody # exclui dados?
		assert 'metadata' not in rbody # exclui metadados?
		assert 'detail' in rbody # contém detalhes?
		assert rbody['detail'][0]['loc'][0] == 'path' # detalhe aponta local do erro?
		assert rbody['detail'][0]['loc'][1] == 'period' # detalhe aponta variável errada?

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
	with TestClient(app) as client:
		response = client.get('/equity-realtime/%s' % (symbol))
		rbody = response.json()
		assert response.status_code == 200 # status correto?
		assert rbody['success'] == True # sucesso?
		assert all(item in rbody.keys() for item in ['data', 'metadata']) # contém dados e metadados?
		for dataitem in rbody['data']: # todos os dados possuem os campos esperados?
			assert all(item in rbody['data'][dataitem] for item in realtime_dataitem_fields)

@pytest.mark.skip(reason="Essa é uma função auxiliar")
def equity_realtime_template_notfound(symbol):
	with TestClient(app) as client:
		response = client.get('/equity-realtime/%s' % (symbol))
		rbody = response.json()
		assert response.status_code == 404 # status correto?
		assert rbody['success'] == False # falha?
		assert 'message' in rbody # contém mensagem?
		assert 'data' not in rbody # exclui dados?
		assert 'metadata' not in rbody # exclui metadados?

def test_equity_realtime_success():
	equity_realtime_template_success('BRDT3.SAO')

def test_equity_realtime_not_found():
	equity_realtime_template_notfound('BRDT3.')


# Teste para websocket não está funcionando ainda...
@pytest.mark.skip(reason="Essa é uma função auxiliar")
def quote_realtime_websocket_template(symbol):
	with client.websocket_connect('/quote/realtime/%s/ws' % (symbol)) as websocket:
		message = websocket.receive_json()
		assert message['equity_symbol'] == symbol
		websocket.close(code=1000)

@pytest.mark.skip(reason="Não está funcionando ainda...")
def test_quote_realtime_websocket():
	quote_realtime_websocket_template('BOVB11.SAO')