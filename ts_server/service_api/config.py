import os

APP_HOST = os.getenv('HOST', '0.0.0.0')
APP_PORT = int(os.getenv('PORT', 8081))
ACCESS_LOG_FORMAT = " :: %r %s %T %t"


