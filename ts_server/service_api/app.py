import asyncio
import logging

from aiohttp import web

from ts_server.service_api.websocket_view import TSGeneratorView


class TSGeneratorApp(web.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # here we store generators for saving their state for every client
        self.client_session_generators = {}


loop = asyncio.get_event_loop()

logging.basicConfig(level=logging.DEBUG)

app = TSGeneratorApp(loop=loop)
app.router.add_view('/ws/numbers', TSGeneratorView)

