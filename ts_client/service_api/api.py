import aiohttp_jinja2
import jinja2

from .ts_page_view import TSPageView, TSWebsocketView


def load_api(app):
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('service_api/templates'))
    app.router.add_view('/', TSPageView)
    app.router.add_view('/index', TSPageView)
    app.router.add_view('/ws/ts_numbers', TSWebsocketView)
