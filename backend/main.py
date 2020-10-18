import enum
import asyncio

import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

import zmq

from modules import config
from modules import alphavantage

from database import db

app = FastAPI()

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
	realtime = 'realtime'
	daily = 'daily'
	weekly = 'weekly'
	monthly = 'monthly'

@app.get('/')
async def root():
	"""
	"""
	return {'online': True}


@app.get('/companies')
async def list_companies():
	"""
	"""

	with db.transaction() as session:
		companies = db.list_companies(session)

	return {'success': True, 'companies': companies}


@app.get('/search/{keywords}')
async def search(keywords: str):
	"""
	"""

	result = alpha.search(keywords=keywords)

	return {'success': True, 'result': result}


@app.get('/equity/{symbol}/{period}')
async def equity(symbol: str, period: Period):
	"""
	"""

	if period == Period.realtime:

		with db.transaction() as session:
			data = db.list_quotes(session, symbol)
			data = {d['created_at'].strftime('%Y-%m-%d %H:%M:%S') : d for d in data}

		return {
			'success': True,
			'period': 'realtime',
			'data': data,
			'metadata': {}
		}

	elif period == Period.daily:

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


@app.get('/quote/{symbol}')
async def search(symbol: str):
	"""
	"""

	data = alpha.get_quote(symbol=symbol)

	return {'success': True, 'data': data}


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
		except websockets.exceptions.ConnectionClosedError as e:
			pass

	async def broadcast(self, message: str):
		for connection in self.active_connections:
			await connection.send_text(message)

manager = ConnectionManager()

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
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
	socket.subscribe("")

	# Receives a string format message
	while True:

		try:
			await asyncio.sleep(5)
			message = socket.recv(flags=zmq.NOBLOCK)
			message = message.decode('utf-8')
			await manager.send_personal_message(message, websocket)
		except zmq.Again as e:
			pass
		except WebSocketDisconnect:
			manager.disconnect(websocket)
