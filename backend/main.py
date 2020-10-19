import enum
import asyncio
import signal

import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

import zmq

from modules import config
from modules import alphavantage

from database import db

from uvicorn.main import Server

original_handler = Server.handle_exit

class AppStatus:
    should_exit = False

    @staticmethod
    def handle_exit(*args, **kwargs):
        AppStatus.should_exit = True
        original_handler(*args, **kwargs)

Server.handle_exit = AppStatus.handle_exit


app = FastAPI(
	title='Bovespa/Empresas',
    description='API do backend Bovespa/Empresas.',
    version='0.0.1',
)

origins = [
    'http://localhost:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

alpha = alphavantage.AlphaMultiKeys(
	api_keys=config.get()['alphavantage_api_keys'],
	tor=True
)


class Period(str, enum.Enum):
	daily = 'daily'
	weekly = 'weekly'
	monthly = 'monthly'


class Company(BaseModel):
	symbol: str
	region: str
	market_close: str
	type: str
	market_open: str
	name: str
	currency: str

class OnlineResponse(BaseModel):
	online: bool

@app.get('/', response_model=OnlineResponse)
async def online():
	"""
	Retorna verdadeiro se o backend está online.
	"""
	return {'online': True}


class CompaniesResponse(BaseModel):
	success: bool
	companies: List[Company]

@app.get('/companies', response_model=CompaniesResponse)
async def list_companies():
	"""
	Obtém a lista de empresas cadastradas.
	"""

	with db.transaction() as session:
		companies = db.list_companies(session)

	return {'success': True, 'companies': companies}


class CompanyResponse(BaseModel):
	success: bool
	company: Company

@app.get('/company/{symbol}', response_model=CompanyResponse)
async def get_company(
	symbol: str = Path(..., title='Símbolo do capital próprio da empresa')):
	"""
	Obtém informações acerca da empresa requisitada, identificada pelo seu símbolo.

	- **symbol**: Símbolo do capital próprio da empresa
	"""

	with db.transaction() as session:
		company = db.get_company(session, symbol)

	if company is None: return {'success': False}
	return {'success': True, 'company': company}


class SearchItemResponse(BaseModel):
	symbol: str
	name: str
	type: str
	region: str
	marketOpen: str
	marketClose: str
	timezone: str
	currency: str
	matchScore: str

class SearchResponse(BaseModel):
	success: bool
	result: List[SearchItemResponse]

@app.get('/search/{keyword}', response_model=SearchResponse)
async def search(
	keyword: str = Path(..., title='Chave de busca para a pesquisa')):
	"""
	Realiza busca pelos capitais próprios registrados na API do Alpha Vantage.

	- **keyword**: Chave de busca para a pesquisa
	"""

	result = alpha.search(keywords=keyword)

	return {'success': True, 'result': result}


class QuoteItem(BaseModel):
	open: float
	high: float
	low: float
	close: float
	volume: int
	price: float

class EquityQuoteDate(BaseModel):
	DATE_VALUE: QuoteItem

class MetadataResponse(BaseModel):
	information: str
	symbol: str
	last_refreshed: str
	output_size: str
	timezone: str

class EquityResponse(BaseModel):
	success: bool
	period: str
	data: dict
	metadata: MetadataResponse

@app.get('/equity/{symbol}/{period}', response_model=EquityResponse)
async def equity(
	symbol: str = Path(..., title='Símbolo do capital próprio'),
	period: Period = Path(..., title='Regime temporal a ser adotado')):
	"""
	Retorna informações de cotação de um capital próprio com base em seu símbolo em
	um determinado regime temporal, que pode ser diário, semanal ou mensal.

	- **symbol**: Símbolo do capital próprio
	- **period**: Regime temporal a ser adotado (daily, weekly ou monthly)

	Um exemplo da variável data é:

	```
	"data": {
		"2020-10-16": {
			"open": 20.26,
			"high": 20.6,
			"low": 20.05,
			"close": 20.44,
			"volume": 4907100,
			"price": 20.44
		},
		"2020-10-15": {
			"open": 20.28,
			"high": 20.45,
			"low": 20.15,
			"close": 20.27,
			"volume": 5262700,
			"price": 20.27
		},
		"2020-10-14": {
			"open": 20.4,
			"high": 20.84,
			"low": 20.38,
			"close": 20.6,
			"volume": 4670800,
			"price": 20.6
		}
	}
	```
	"""

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


class EquityRealTimeResponse(BaseModel):
	success: bool
	period: str
	data: dict
	metadata: dict

@app.get('/equity-realtime/{symbol}', response_model=EquityRealTimeResponse)
async def equity_realtime(
	symbol: str = Path(..., title='Símbolo do capital próprio')):
	"""
	Retorna as últimas informações de cotação de um capital próprio registradas no
	banco de dados com base em seu símbolo. Atualmente, a variável metadata contém um 
	objeto vazio.

	- **symbol**: Símbolo do capital próprio

	Um exemplo da variável data é:

	```
	"data": {
		"2020-10-19 12:16:56": {
			"price": 20.44,
			"id": 6961,
			"high": 20.6,
			"latest_trading_day": "2020-10-16",
			"previous_close": 20.27,
			"change_percent": 0.8387,
			"equity_symbol": "BRDT3.SAO",
			"low": 20.05,
			"open": 20.26,
			"volume": 4907100,
			"change": 0.17,
			"created_at": "2020-10-19T12:16:56.473724+00:00"
		},
		"2020-10-19 12:20:17": {
			"price": 20.44,
			"id": 6972,
			"high": 20.6,
			"latest_trading_day": "2020-10-16",
			"previous_close": 20.27,
			"change_percent": 0.8387,
			"equity_symbol": "BRDT3.SAO",
			"low": 20.05,
			"open": 20.26,
			"volume": 4907100,
			"change": 0.17,
			"created_at": "2020-10-19T12:20:17.465768+00:00"
		},
		"2020-10-19 12:20:50": {
			"price": 20.44,
			"id": 6974,
			"high": 20.6,
			"latest_trading_day": "2020-10-16",
			"previous_close": 20.27,
			"change_percent": 0.8387,
			"equity_symbol": "BRDT3.SAO",
			"low": 20.05,
			"open": 20.26,
			"volume": 4907100,
			"change": 0.17,
			"created_at": "2020-10-19T12:20:50.158947+00:00"
		}
	```
	"""

	with db.transaction() as session:
		data = db.list_quotes(session, symbol)
		data = data[-40:]
		data = {d['created_at'].strftime('%Y-%m-%d %H:%M:%S') : d for d in data}

	return {
		'success': True,
		'period': 'realtime',
		'data': data,
		'metadata': {}
	}


class ConnectionManager:
	def __init__(self):
		self.active_connections: List[WebSocket] = []

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connections.append(websocket)

	def disconnect(self, websocket: WebSocket):
		self.active_connections.remove(websocket)

	async def send_personal_message(self, message: str, websocket: WebSocket):
		try:
			await websocket.send_text(message)
		except:
			pass

	async def broadcast(self, message: str):
		for connection in self.active_connections:
			await connection.send_text(message)

manager = ConnectionManager()

@app.websocket('/quote/realtime/{symbol}/ws')
async def websocket_endpoint(websocket: WebSocket, symbol: str):
	"""
	"""

	await manager.connect(websocket)

	host = 'bovespa-empresas-publisher'
	port = '5556'

	# Creates a socket instance
	context = zmq.Context()
	socket = context.socket(zmq.SUB)

	# Connects to a bound socket
	socket.connect("tcp://{}:{}".format(host, port))

	# Subscribes to all topics
	socket.subscribe('QUOTE_%s' % (symbol))

	# Receives a string format message
	while AppStatus.should_exit is False:

		try:
			await asyncio.sleep(5)
			message = socket.recv(flags=zmq.NOBLOCK)
			message = message.decode('utf-8')
			message = message[message.index(' ')+1:]
			await manager.send_personal_message(message, websocket)
		except zmq.Again as e:
			pass
		except WebSocketDisconnect:
			manager.disconnect(websocket)
