import sys
import time
import json
import traceback

import zmq

sys.path.append('.')
from modules import alphavantage
from modules import config
from database import db

PORT = 5556

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:%s' % (PORT))

alpha = alphavantage.AlphaMultiKeys(
	api_keys=config.get()['alphavantage_api_keys'],
	tor=True
)

equities = None
while equities is None:
	try:
		with db.transaction() as session:
			equities = db.list_equities(session)
	except:
		pass
	finally:
		time.sleep(10)

symbols = [equity['symbol'] for equity in equities]
loopindex = 0

def __increment_loopindex__():
	"""
	"""
	global loopindex
	loopindex = (loopindex + 1) % len(symbols)

while True:

	try:
		
		symbol = symbols[loopindex]

		data = alpha.get_quote(symbol=symbol)

		with db.transaction() as session:
			new_quote = db.create_quote(session, data)

		topic = 'QUOTE_%s' % (symbol)
		message = json.dumps(data)
		print('%s: %s' % (topic, message))

		socket.send_string('%s %s' % (topic, message))
	
	except:
		
		traceback.print_exc() 
		pass

	finally:

		__increment_loopindex__()
		time.sleep(16.4)