import sys
import time
import json
import traceback

import zmq

sys.path.append('.')
from modules import alphavantage
from modules import config
from database import db

alpha = alphavantage.AlphaMultiKeys(
	api_keys=config.get()['alphavantage_api_keys'],
	tor=True
)

with db.transaction() as session:
	companies = db.list_companies(session)

symbols = [config.get()['bovespa']] + [company['symbol'] for company in companies]
loopindex = 0

def __increment_loopindex__():
	global loopindex
	loopindex = (loopindex + 1) % len(symbols)

PORT = 5556

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:%s' % (PORT))

while True:

	try:
		
		symbol = symbols[loopindex]

		data = alpha.get_quote(symbol=symbol)

		if symbol == config.get()['bovespa']:
			with db.transaction() as session:
				new_ibovespa = db.create_ibovespa(session, data)
		else:
			with db.transaction() as session:
				new_price = db.create_price(session, data)

		topic = 'QUOTE_%s' % (symbol)
		message = json.dumps(data)
		print('%s: %s' % (topic, message))

		socket.send_string('%s %s' % (topic, message))
	
	except:
		
		traceback.print_exc() 
		pass

	finally:

		__increment_loopindex__()
		time.sleep(18)