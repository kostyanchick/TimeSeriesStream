import os

APP_HOST = os.getenv('HOST', '0.0.0.0')
APP_PORT = int(os.getenv('PORT', 8082))

GENERATOR_HOST = os.getenv('GENERATOR_HOST', '0.0.0.0')
GENERATOR_PORT = int(os.getenv('GENERATOR_PORT', 8081))
GENERATOR_URL = f'http://{GENERATOR_HOST}:{GENERATOR_PORT}/ws/numbers'
CONNECTION_RETRY_PERIOD = 3

# will be used by server to identify client
CLIENT_ID = "12345"

ACCESS_LOG_FORMAT = " :: %r %s %T %t"

DATA_FILE_PATH = 'service_api/data/numbers.txt'

RECORD_TEMPLATE = '''index: {index:<6} | number: {number:7} | timestamp: {timestamp}'''

# time for producing one number by server
TICK_NUMBER_TIME = 1
