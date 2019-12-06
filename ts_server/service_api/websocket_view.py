import asyncio

from aiohttp import web, WSMsgType

from .generator import gen_normal_dist_number
from .config import MSG_TIMEOUT, TICK_NUMBER_TIME


class TSGeneratorView(web.View):
    """WebSocket view continuously producing and sending numbers
    to the client"""

    async def receive_client_id(self, ws):
        client_id = None
        while not client_id:
            try:
                client_id = await ws.receive_str()
                if not client_id:
                    await ws.send_str('Please provide valid client id')
            except asyncio.TimeoutError:
                pass
        return client_id

    async def send_single_record(self, ws, idx, number):
        number_obj = {'index': idx, 'number': number}
        print(f'Sending {number_obj}')
        return await ws.send_json(number_obj)

    async def send_numbers(self, ws, client_id):
        # here we are looking for an existing generator by client id
        # in case if found - it will continue work from it's present state
        generator = self.request.app.client_session_generators.get(client_id)
        # if client is connected at first time -
        # create new generator with given client id
        if not generator:
            generator = self.request.app.client_session_generators[client_id] = gen_normal_dist_number()
        while True:
            await asyncio.sleep(TICK_NUMBER_TIME)
            try:
                message = await ws.receive_str(timeout=MSG_TIMEOUT)
                if message == WSMsgType.CLOSE:
                    print('Websocket connection closed')
                    await ws.close()
                    return ws
                elif message == WSMsgType.ERROR:
                    print(f'Websocket connection closed with exception {ws.exception()}')

            # this means we didn't receive any message
            # so server should continue sending numbers
            except asyncio.TimeoutError:
                idx, number = next(generator)
                await self.send_single_record(ws, idx, number)

    async def get(self):
        """Method produces and sends data client.
        Depending on client_id
        it takes existing generator to supplement time series
        or creates a new one if it the first connection of this client"""

        print('Websocket connection starting')
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        print('Websocket connection ready')

        try:
            # get first message with client id
            client_id = await self.receive_client_id(ws)
            print(f'Connected with a client: {client_id}')

            # send numbers to the client till connection is not closed by the client
            await self.send_numbers(ws, client_id)

        # catch the case when connection was closed improperly
        except Exception as ex:
            print(f'Websocket connection closed improperly with exception '
                  f'{type(ex).__name__}')
        finally:
            await ws.close()

        return ws
