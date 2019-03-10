from asyncio import get_event_loop
from pytest import fixture
from pytest_sanic.utils import TestClient
from pytest_sanic.plugin import sanic_client

from main import app, session_bp, page_not_found


@fixture(scope='module')
def loop():
    # Reference from pytest_sanic.plugin#loop to give a new scope.
    yield get_event_loop()


@fixture(scope='module')
def sanic_cli(loop):
    # Reference from pytest_sanic.plugin#sanic_client to give a new scope.
    clients = []

    async def create_client(app, **kwargs):
        client = TestClient(app, loop=loop, **kwargs)
        await client.start_server()
        clients.append(client)
        return client

    yield create_client

    # Clean up
    if clients:
        for client in clients:
            loop.run_until_complete(client.close())


@fixture(scope='module')
def test_cli(loop, sanic_cli):
    app.blueprint(session_bp)
    app.exception(page_not_found)
    return loop.run_until_complete(sanic_cli(app))
