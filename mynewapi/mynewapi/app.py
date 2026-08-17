from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from mynewapi.routers import auth, users
from mynewapi.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.get('/htmlhello', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def hello_world():
    return '<h1>Olá Mundo</h1>'
