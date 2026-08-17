from http import HTTPStatus

from mynewapi.schemas import UserPublic
from mynewapi.security import create_access_token


def test_root_should_return_hello_world(client):
    response = client.get('/')

    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_html_hello_should_return_html_hello_world(client):
    response = client.get('/htmlhello')
    assert response.text == '<h1>Olá Mundo</h1>'


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@iamalice.com',
            'password': 'alice123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@iamalice.com',
        'username': 'alice',
    }


def test_create_user_email_already_exists(client, user, token):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'anotherusername',
            'password': user.clean_password,
            'email': user.email,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_username_already_exists(client, user, token):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'password': user.clean_password,
            'email': 'another@email.com',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_read_users(client, user, token):

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bunny',
            'email': 'bunny@iambunny.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bunny',
        'email': 'bunny@iambunny.com',
        'id': 1,
    }


def test_update_user_error(client, user, token):
    response = client.put(
        '/users/666',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bunny',
            'email': 'bunny@iambunny.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_without_token(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bunny',
            'email': 'bunny@iambunny.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user_should_return_ok(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_user_should_return_not_found(client, token):
    response = client.get(
        '/users/666', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Id not found'}


def test_get_user(client, user, token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    user_schema = UserPublic.model_validate(user)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema.model_dump()


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    response_data = response.json()
    assert 'access_token' in response_data
    assert response_data['token_type'] == 'Bearer'
    assert response.status_code == HTTPStatus.OK


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'lua',
            'email': 'lua@gmail.com',
            'password': 'secret',
        },
    )

    response_update = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'lua',
            'email': 'lua@outlook.com',
            'password': 'secretnew',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


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


def test_delete_user_different_than_logged_in(client, token, user):
    response = client.delete(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_post_token_with_wrong_email(client, user):
    response = client.post(
        '/token',
        data={
            'username': 'wrong@email.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_post_token_with_wrong_password(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': 'wrongpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
