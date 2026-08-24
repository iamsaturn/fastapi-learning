from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from mynewapi.models import ToDoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    token_type: str
    access_token: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3, max_length=20)
    description: str | None = None
    state: ToDoState | None = None


class ToDoSchema(BaseModel):
    title: str
    description: str
    state: ToDoState = Field(default=ToDoState.todo)


class ToDoPublic(ToDoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ToDoList(BaseModel):
    todos: list[ToDoPublic]
