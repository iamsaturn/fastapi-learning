from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    response_data = response.json()
    assert 'access_token' in response_data
    assert response_data['token_type'] == 'Bearer'
    assert response.status_code == HTTPStatus.OK


def test_post_token_with_wrong_email(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'wrong@email.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_post_token_with_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'wrongpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_expiration(client, user):
    with freeze_time('2001-07-28 07:00:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time('2001-07-28 07:31:00'):
        response = client.put(
            '/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'Mariana',
                'email': 'Mari@veve.com',
                'password': 'marisecret',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_inexistent_user_token(client):
    resp = client.post(
        '/auth/token',
        data={
            'username': 'inexistent',
            'password': 'alsoinexistent',
        },
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    assert resp.json() == {'detail': 'Incorrect email or password'}


def test_wrong_password(client, user):
    resp = client.post(
        'auth/token', data={'username': {user.email}, 'password': 'wrongpass'}
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    assert resp.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2001-07-14 06:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time('2001-07-14 06:31:00'):
        response = client.post(
            'auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
