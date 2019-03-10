from asyncio import get_event_loop
from pytest_sanic.utils import TestClient
from pytest_sanic.plugin import sanic_client
from pytest import fixture, yield_fixture
from types import SimpleNamespace

from server import create_app


@fixture(scope='module')
def loop():
    # Reference from pytest_sanic.plugin#loop to give a new scope.
    yield get_event_loop()


#
#
# @fixture(scope='module')
# def sanic_cli(loop):
#     # Reference from pytest_sanic.plugin#sanic_client to give a new scope.
#     clients = []
#
#     async def create_client(app, **kwargs):
#         client = TestClient(app, loop=loop, **kwargs)
#         await client.start_server()
#         clients.append(client)
#         return client
#
#     yield create_client
#
#     # Clean up
#     if clients:
#         for client in clients:
#             loop.run_until_complete(client.close())
#
#
# @fixture(scope='module')
# def test_cli(loop, sanic_cli):
#     app.blueprint(session_bp)
#     app.exception(page_not_found)
#     return loop.run_until_complete(sanic_cli(app))

def pytest_addoption(parser):
    parser.addoption("--host", type=str, required=True, dest="HOST")
    parser.addoption("--port", type=int, required=True, dest="PORT")
    parser.addoption("--worker", type=int, default=2, dest="WORKER")
    parser.addoption("--db-host", type=str, default="127.0.0.1",
                     dest="DB_HOST",
                     help="Redis server ip")
    parser.addoption("--db-port", type=int, default=6379,
                     dest="DB_PORT",
                     help="Redis server port")


@yield_fixture(scope='module')
def app(request):
    args = SimpleNamespace(HOST=request.config.getoption("--host"),
                           PORT=request.config.getoption("--port"),
                           WORKER=request.config.getoption("--worker"),
                           DB_HOST=request.config.getoption("--db-host"),
                           DB_PORT=request.config.getoption("--db-port"))
    app = create_app(args)
    yield app


@fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
