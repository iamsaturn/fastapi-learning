import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from mynewapi.routers import auth, to_do, users
from mynewapi.schemas import Message

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(to_do.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.get('/htmlhello', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def hello_world():
    return '<h1>Olá Mundo</h1>'
