from datetime import datetime
import json
import asyncio


from aiohttp import ClientSession, WSMsgType

from .constants import CONST_MU, CONST_SIGMA
from .app import buffer_numbers
from .config import GENERATOR_URL, DATA_FILE_PATH


async def get_numbers_from_server(client_id='12345'):
    """This function ran asynchronously with the web application in the same loop
    It continuously getting data from server
    storing numbers in file and pushing it to shared buffer

    client_id could be used to manage several clients by server
    with a specific time series data for every client
    """

    async with ClientSession() as session:
        try:
            ws = await session.ws_connect(GENERATOR_URL)
            print('Successfully connected to server')

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
                    if abs(data_['number'] - CONST_MU) >= 2 * CONST_SIGMA:
                        buffer_numbers.append(data_)
                        ts_log.write(f'{json.dumps(data_)} \n')

                    # frequency of generator is 1 number per second
                    # we leave this time for our application
                    await asyncio.sleep(1)

            print('Connection closed')
            return ws

        # catch the case when connection was closed improperly
        except Exception as ex:
            print(f'During websocket connection occurred an exception '
                  f'{type(ex).__name__}')
