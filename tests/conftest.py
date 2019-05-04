from asyncio import get_event_loop

import pytest
from pytest import fixture
from pytest_sanic.utils import TestClient
from utils.db import RedisDb

from server import create_app


@fixture(scope='module')
def loop():
    # Reference from pytest_sanic.plugin#loop to give a new scope.
    yield get_event_loop()


@pytest.yield_fixture(scope='module')
def app():
    app = create_app('127.0.0.1', 1337, '127.0.0.1', 6379)
    yield app


@pytest.yield_fixture(scope='module')
def db():
    db = RedisDb('127.0.0.1', 6379)
    yield db


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
def test_cli(loop, app, sanic_cli):
    # app.blueprint(session_bp)
    # app.exception(page_not_found)
    return loop.run_until_complete(sanic_cli(app))
