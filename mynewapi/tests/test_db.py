from dataclasses import asdict

from mynewapi.models import User


def test_create_user(session, mock_db_time):

    new_user = User(
        username='bunny', email='bunny@example.com', password='secret'
    )
    with mock_db_time(User) as fake_time:
        session.add(new_user)
        session.commit()

        assert asdict(new_user) == {
            'id': 1,
            'username': 'bunny',
            'email': 'bunny@example.com',
            'password': 'secret',
            'created_at': fake_time,
            'updated_at': fake_time,
        }
