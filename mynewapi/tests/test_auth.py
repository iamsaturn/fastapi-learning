from http import HTTPStatus


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
