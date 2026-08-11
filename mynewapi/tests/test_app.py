from fastapi.testclient import TestClient
from http import HTTPStatus

from mynewapi.app import app

client = TestClient(app)


def test_root_should_return_hello_world():

    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK

