from http import HTTPStatus

from fastapi.testclient import TestClient

from mynewapi.app import app


def test_root_should_return_hello_world():

    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_html_hello_should_return_html_hello_world():

    client = TestClient(app)
    response = client.get('/htmlhello')
    assert response.text == '<h1>Olá Mundo</h1>'
