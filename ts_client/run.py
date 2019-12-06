from aiohttp import web

from service_api.get_numbers_task import get_numbers_from_server
from service_api.app import app, loop
from service_api.api import load_api
from service_api.config import APP_HOST, APP_PORT, ACCESS_LOG_FORMAT


if __name__ == '__main__':
    # Creating task for receiving data from sever
    loop.create_task(get_numbers_from_server())

    # Running our web application in the same loop
    load_api(app)
    web.run_app(app,
                host=APP_HOST,
                port=APP_PORT,
                access_log_format=ACCESS_LOG_FORMAT)
