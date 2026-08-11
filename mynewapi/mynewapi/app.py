from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from mynewapi.schemas import Message, HelloWorldHTML

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.get('/htmlhello', status_code=HTTPStatus.OK,
         response_class=HTMLResponse,
         response_model= HelloWorldHTML)
def hello_world():
    return '<h1>Olá Mundo</h1>'
