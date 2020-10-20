# Imports da biblioteca padrão
import enum
import asyncio
import signal

# Imports relacionados ao fastapi e seu correto funcionamento
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Union
from uvicorn.main import Server
import websockets

# Import do ZeroMQ
import zmq

# Imports dos módulos próprios do app
from modules import config
from modules import alphavantage
from database import db


# Configuração do app
app = FastAPI(
	title='Bovespa/Empresas',
    description='API do backend Bovespa/Empresas.',
    version='0.0.1',
)

# Configuração do banco de dados
database = db.PostgreSQLDatabase(config.get('postgresql_database_uri'))

# Definição das ações de inicialização e término do app
@app.on_event("startup")
def startup():
    database.connect()

@app.on_event("shutdown")
def shutdown():
    database.disconnect()

# Configuração das origens permitidas
origins = [
    '*'
]

# Aplicação do CORS ao app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

# Definição do objeto alpha, que contém as funções relacionadas ao Alpha Vantage
alpha = alphavantage.AlphaMultiKeys(
	api_keys=config.get('alphavantage_api_keys'),
	tor=True
)

# Configuração de objeto para manter o estado do app
# Utilizado para interromper o loop dos websockets quando o app é finalizado
original_handler = Server.handle_exit

# Define classe AppStatus
class AppStatus:
    should_exit = False

    @staticmethod
    def handle_exit(*args, **kwargs):
        AppStatus.should_exit = True
        original_handler(*args, **kwargs)

# Substitui o handler de saída do uvicorn com função que atualiza a flag should_exit.
Server.handle_exit = AppStatus.handle_exit


# Definição do modelo de resposta de erro
class ErrorResponse(BaseModel):
	success = False
	message: str

# Definição da rota base / e seu modelo de resposta
class OnlineResponse(BaseModel):
	online: bool

@app.get('/', response_model=OnlineResponse)
async def online():
	"""Retorna verdadeiro se o backend está online.
	"""
	return {'online': True}


# Definição da rota /companies e seu modelo de resposta
class Company(BaseModel):
	symbol: str
	region: str
	market_close: str
	type: str
	market_open: str
	name: str
	currency: str

class CompaniesResponse(BaseModel):
	success: bool
	companies: List[Company]

@app.get('/companies', response_model=CompaniesResponse)
def list_companies():
	"""
	Obtém a lista de empresas cadastradas.
	"""

	with database.transaction() as session:
		companies = database.list_companies(session)

	return {'success': True, 'companies': companies}


# Definição da rota /company/{symbol} e seu modelo de resposta
class CompanyResponse(BaseModel):
	success: bool
	company: Company

@app.get('/company/{symbol}',
response_model=Union[CompanyResponse, ErrorResponse],
responses={200: {'model': CompanyResponse}, 404: {'model': ErrorResponse}})
def get_company(
	symbol: str = Path(..., title='Símbolo do patrimônio da empresa')):
	"""Obtém informações acerca da empresa requisitada, identificada pelo seu símbolo.

	- **symbol**: Símbolo do patrimônio da empresa
	"""

	with database.transaction() as session:
		company = database.get_company(session, symbol)

	if company is None:
		return JSONResponse(
			status_code=404,
			content={'success': False, 'message': 'Empresa não encontrada'}
		)
	else:
		return JSONResponse(
			status_code=200,
			content={'success': True, 'company': company}
		)


# Definição da rota /search/{keyword} e seu modelo de resposta
class SearchItemResponse(BaseModel):
	symbol: str
	name: str
	type: str
	region: str
	market_open: str
	market_close: str
	timezone: str
	currency: str
	match_score: str

class SearchResponse(BaseModel):
	success: bool
	result: List[SearchItemResponse]

@app.get('/search/{keyword}', response_model=SearchResponse)
def search(
	keyword: str = Path(..., title='Chave de busca para a pesquisa')):
	"""Realiza busca pelos capitais próprios registrados na API do Alpha Vantage.

	- **keyword**: Chave de busca para a pesquisa
	"""

	result = alpha.search(keywords=keyword)

	return {'success': True, 'result': result}


# Definição da rota /equity/{symbol}, seus modelos de input e output
class Period(str, enum.Enum):
	daily = 'daily'
	weekly = 'weekly'
	monthly = 'monthly'

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

@app.get('/equity/{symbol}/{period}',
response_model=Union[EquityResponse, ErrorResponse],
responses={200: {'model': EquityResponse}, 404: {'model': ErrorResponse}})
def equity(
	symbol: str = Path(..., title='Símbolo do patrimônio'),
	period: Period = Path(..., title='Regime temporal a ser adotado')):
	"""Retorna informações de cotação de um patrimônio com base em seu símbolo em
	um determinado regime temporal, que pode ser diário, semanal ou mensal.

	- **symbol**: Símbolo do patrimônio
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

		if data is None or metadata is None:
			return JSONResponse(
				status_code=404,
				content={'success': False, 'message': 'Símbolo não encontrado'}
			)

		return {
			'success': True,
			'period': 'daily',
			'data': data, 
			'metadata': metadata
		}

	elif period == Period. weekly:

		data, metadata = alpha.get_time_series_weekly(symbol=symbol)

		if data is None or metadata is None:
			return JSONResponse(
				status_code=404,
				content={'success': False, 'message': 'Símbolo não encontrado'}
			)

		return {
			'success': True,
			'period': 'weekly',
			'data': data,
			'metadata': metadata
		}

	elif period == Period.monthly:

		data, metadata = alpha.get_time_series_monthly(symbol=symbol)

		if data is None or metadata is None:
			return JSONResponse(
				status_code=404,
				content={'success': False, 'message': 'Símbolo não encontrado'}
			)

		return {
			'success': True,
			'period': 'monthly',
			'data': data,
			'metadata': metadata
		}


# Definição da rota /equity-realtime/{symbol} e seu modelo de resposta
class EquityRealTimeResponse(BaseModel):
	success: bool
	period: str
	data: dict
	metadata: dict

@app.get('/equity-realtime/{symbol}',
response_model=Union[EquityRealTimeResponse, ErrorResponse],
responses={200: {'model': EquityRealTimeResponse}, 404: {'model': ErrorResponse}})
def equity_realtime(
	symbol: str = Path(..., title='Símbolo do patrimônio')):
	"""Retorna as últimas informações de cotação de um patrimônio registradas no
	banco de dados com base em seu símbolo. Atualmente, a variável metadata contém um 
	objeto vazio.

	- **symbol**: Símbolo do patrimônio

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

	with database.transaction() as session:
		data = database.list_quotes(session, symbol)
		if len(data) == 0:
			return JSONResponse(
				status_code=404,
				content={'success': False, 'message': 'Símbolo não encontrado'}
			)
		data = data[-40:]
		data = {d['created_at'].strftime('%Y-%m-%d %H:%M:%S') : d for d in data}

	return {
		'success': True,
		'period': 'realtime',
		'data': data,
		'metadata': {}
	}


# Gerenciador de conexões via websocket
# https://fastapi.tiangolo.com/advanced/websockets/

class ConnectionManager:
	"""Gerenciador de conexões via websocket, com funções para conexão, desconexão,
	envio de mensagens a um único cliente ou broadcast.
	"""
	def __init__(self):
		"""Construtor do gerenciador de conexões"""
		self.active_connections: List[WebSocket] = []

	async def connect(self, websocket: WebSocket):
		"""Realiza a conexão de um novo cliente

		Keyword arguments:
		websocket -- objeto websocket relacionado ao novo cliente
		"""
		await websocket.accept()
		self.active_connections.append(websocket)

	def disconnect(self, websocket: WebSocket):
		"""Realiza a desconexão de um cliente

		Keyword arguments:
		websocket -- objeto websocket relacionado a um cliente conectado
		"""
		self.active_connections.remove(websocket)

	async def send_personal_message(self, message: str, websocket: WebSocket):
		"""Envia mensagem a um cliente específico

		Keyword arguments:
		message -- mensagem a ser enviada ao cliente
		websocket -- objeto websocket relacionado a um cliente conectado
		"""
		try:
			await websocket.send_text(message)
		except:
			pass

	async def broadcast(self, message: str):
		"""Envia mensagem a todos os clientes conectados

		Keyword arguments:
		message -- mensagem a ser enviada aos clientes
		"""
		for connection in self.active_connections:
			await connection.send_text(message)

# Define uma instância do gerenciador de conexões
manager = ConnectionManager()

@app.websocket('/quote/realtime/{symbol}/ws')
async def websocket_endpoint(websocket: WebSocket, symbol: str):
	"""Loop de processamento para atualização de cotações dos capitais próprios com
	base em seu símbolo.
	"""

	# Realiza a conexão do cliente
	await manager.connect(websocket)

	# Define o host e a porta em que o publisher ZMQ está publicando as cotações
	host = config.get('quote_publisher_host')
	port = config.get('quote_publisher_port')

	# Cria uma instância subscriber de socket ZMQ
	context = zmq.Context()
	socket = context.socket(zmq.SUB)

	# Conecta ao publisher
	socket.connect("tcp://{}:{}".format(host, port))

	# Subscreve ao tópico relacionado a um patrimônio específico, com base no símbolo
	socket.subscribe('QUOTE_%s' % (symbol))

	# Loop de operação
	# O loop é interrompido quando o app é finalizado
	while AppStatus.should_exit is False:

		try:

			# Espera assíncrona para execução de outras tarefas
			await asyncio.sleep(config.get('quote_realtime_update_period'))

			# Verificação da fila de mensagens em modo sem bloqueio
			message = socket.recv(flags=zmq.NOBLOCK)

			# Caso haja uma mensagem na fila, decodifica para o formato utf-8...
			message = message.decode('utf-8')
			# Remove a informação do tópico e mantém apenas a mensagem
			message = message[message.index(' ')+1:]
			
			# Submete a mensagem ao cliente conectado
			await manager.send_personal_message(message, websocket)

		# Caso não haja mensagens na fila, não faz nada, vai para a próxima iteração
		except zmq.Again as e:
			pass

		# Caso haja desconexão do cliente, atualiza o estado do gerenciador
		except WebSocketDisconnect:
			manager.disconnect(websocket)
