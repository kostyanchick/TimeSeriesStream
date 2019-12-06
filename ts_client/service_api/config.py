import os
from string import Template


APP_HOST = os.getenv('HOST', '0.0.0.0')
APP_PORT = int(os.getenv('PORT', 8082))

GENERATOR_HOST = os.getenv('HOST', '0.0.0.0')
GENERATOR_PORT = int(os.getenv('PORT', 8081))
GENERATOR_URL = f'http://{GENERATOR_HOST}:{GENERATOR_PORT}/ws/numbers'

ACCESS_LOG_FORMAT = " :: %r %s %T %t"

DATA_FILE_PATH = 'ts_data.log'

RECORD_TEMPLATE = 'index: {index:>10} number: {number:>10} timestamp: {timestamp}'
