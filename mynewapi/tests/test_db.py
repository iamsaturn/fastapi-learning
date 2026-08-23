from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mynewapi.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):

    new_user = User(
        username='bunny', email='bunny@example.com', password='secret'
    )
    with mock_db_time(User) as fake_time:
        session.add(new_user)
        await session.commit()

    new_user = await session.scalar(
        select(User).where(User.username == 'bunny')
    )

    assert asdict(new_user) == {
        'id': 1,
        'username': 'bunny',
        'email': 'bunny@example.com',
        'password': 'secret',
        'created_at': fake_time,
        'updated_at': fake_time,
        'todos': [],
    }
