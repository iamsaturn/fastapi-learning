from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mynewapi.database import get_session
from mynewapi.models import Todo, User
from mynewapi.schemas import (
    FilterTodo,
    Message,
    ToDoList,
    ToDoPublic,
    ToDoSchema,
)
from mynewapi.security import get_current_user

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=ToDoPublic)
async def create_to_do(todo: ToDoSchema, session: Session, user: CurrentUser):

    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=ToDoList)
async def list_todos(
    session: Session,
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))
    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )
    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.limit(todo_filter.limit).offset(todo_filter.offset)
    )
    return {'todos': todos.all()}


@router.delete('/{todo_id}', response_model=Message)
async def delete_todo(session: Session, user: CurrentUser, todo_id: int):
    todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    session.delete(todo)
    await session.commit()
    return {'message': 'Task has been deleted'}
