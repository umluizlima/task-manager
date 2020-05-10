from pytest import fixture
from starlette.testclient import TestClient

from app import app


@fixture
def client():
    client = TestClient(app)
    return client
