from http import HTTPStatus

from jwt import decode

from mynewapi.security import create_access_token


def test_jwt(settings):
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    assert decoded['test'] == data['test']


def test_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer false-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_with_invalid_email(client, user):
    generated_wrong_token = create_access_token({'banana': 'hello'})
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {generated_wrong_token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client, user):
    token = create_access_token({'sub': 'wrong@test'})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
