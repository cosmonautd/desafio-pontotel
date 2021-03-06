import sys
import time
import json
import traceback
import datetime

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
	api_keys=config.get('alphavantage_api_keys'),
	tor=True
)

database = db.PostgreSQLDatabase(config.get('postgresql_database_uri'))
database.connect()

equities = None
while equities is None:
	try:
		with database.transaction() as session:
			equities = database.list_equities(session)
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

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (z.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            return super().default(z)

while True:

	try:
		
		symbol = symbols[loopindex]

		data = alpha.get_quote(symbol=symbol)

		with database.transaction() as session:
			new_quote = database.create_quote(session, data)

		topic = 'QUOTE_%s' % (symbol)
		message = json.dumps(new_quote, cls=DateTimeEncoder)
		print('%s: %s' % (topic, message))

		socket.send_string('%s %s' % (topic, message))
	
	except:
		
		traceback.print_exc() 
		pass

	finally:

		__increment_loopindex__()
		time.sleep(16.4)
		database.disconnect()