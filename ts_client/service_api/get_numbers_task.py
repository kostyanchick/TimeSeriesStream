from datetime import datetime
import json
import asyncio


from aiohttp import ClientSession, WSMsgType
from aiohttp.client_exceptions import ClientConnectionError

from .constants import CONST_MU, CONST_SIGMA, CONST_COEFF
from .app import buffer_numbers
from .config import GENERATOR_URL, DATA_FILE_PATH, TICK_NUMBER_TIME, CONNECTION_RETRY_PERIOD, CLIENT_ID


async def get_numbers_from_server(client_id=CLIENT_ID):
    """This function ran asynchronously with the web application in the same loop
    It continuously getting data from server
    storing numbers in file and pushing it to shared buffer.
    If connection with server lost,
    function will retry during period set in config

    client_id could be used to manage several clients by server
    with a specific time series data for every client
    """

    while True:
        try:
            # continuously receive data until connection lost or client stopped
            async with ClientSession() as session:
                ws = await session.ws_connect(GENERATOR_URL)
                print('Successfully connected to server')

                await receive_data(ws, client_id)

                print('Connection closed')
                return ws

        except ClientConnectionError:
            print(f'Error when tried connect to server. '
                  f'Trying to reconnect in {CONNECTION_RETRY_PERIOD}s')
            await asyncio.sleep(CONNECTION_RETRY_PERIOD)
            continue


async def receive_data(ws, client_id):
    # send client id to the server
    await ws.send_str(client_id)

    # receive and save numbers to log file
    with open(DATA_FILE_PATH, 'a', encoding='utf-8') as ts_log:
        async for msg in ws:
            if msg.type in (WSMsgType.CLOSED, WSMsgType.ERROR):
                break

            tst = datetime.utcnow()

            print(f'[{tst}] Message received from server: {msg}',)
            data_ = json.loads(msg.data)
            data_.update({'timestamp': str(tst)})
            # filter numbers
            if abs(data_['number'] - CONST_MU) >= CONST_COEFF * CONST_SIGMA:
                buffer_numbers.append(data_)
                ts_log.write(f'{json.dumps(data_)} \n')

            # frequency of generator is 1 number per second
            # we leave this time for our application
            await asyncio.sleep(TICK_NUMBER_TIME)

