# view for web page rendering our time series
from aiohttp import web, WSMsgType
import aiohttp_jinja2
import asyncio

from .app import buffer_numbers
from .config import RECORD_TEMPLATE


class TSPageView(web.View):
    """This view is for rendering our web page"""

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {'hello': 'world'}


class TSWebsocketView(web.View):
    """Websocket view giving access to the real-time time series
    data received from server"""

    @staticmethod
    def waiting_generator(lst):
        cur_idx = 0
        # this approach let us to wait until new elements are appended to the list
        while True:
            try:
                yield lst[cur_idx]
                cur_idx += 1
            except IndexError:
                yield None

    async def get(self):
        """Method uses custom generator to get data from buffer as it received
        and send it to the web-page client"""

        gen_for_ws = self.waiting_generator(buffer_numbers)

        print('Websocket connection starting')
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        print('Websocket connection ready')

        while True:
            record = next(gen_for_ws)
            if record:
                msg_str = RECORD_TEMPLATE.format(
                    index=record['index'],
                    number=record['number'],
                    timestamp=record['timestamp']
                )
                await ws.send_str(msg_str)
            else:
                await asyncio.sleep(1)

        print('Websocket connection closed')
        return ws
