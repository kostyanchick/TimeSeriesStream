from aiohttp import web

from ts_server.service_api.app import app
from ts_server.service_api.config import APP_HOST, APP_PORT, ACCESS_LOG_FORMAT


if __name__ == '__main__':
    web.run_app(app,
                host=APP_HOST,
                port=APP_PORT,
                access_log_format=ACCESS_LOG_FORMAT)
