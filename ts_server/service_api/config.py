import os

APP_HOST = os.getenv('HOST', '0.0.0.0')
APP_PORT = int(os.getenv('PORT', 8081))
ACCESS_LOG_FORMAT = " :: %r %s %T %t"


# time for producing one number by server
TICK_NUMBER_TIME = 1

# time of attempt to receive message from client
MSG_TIMEOUT = 0.1
