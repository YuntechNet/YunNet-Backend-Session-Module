from pytest import fixture
from pytest_sanic.plugin import sanic_client

from main import app


@fixture
def test_cli(loop, sanic_client):
    return loop.run_until_complete(sanic_client(app))
