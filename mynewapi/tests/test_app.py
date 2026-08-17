from http import HTTPStatus


def test_root_should_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_html_hello_should_return_html_hello_world(client):
    response = client.get('/htmlhello')
    assert response.text == '<h1>Olá Mundo</h1>'
