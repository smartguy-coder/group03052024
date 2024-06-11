from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

app = FastAPI()


books = [
    {
        "title": "Майстер і Маргарита",
        "author": "Михайло Булгаков",
        "year": 1967,
        "genre": "Роман"
    },
    {
        "title": "Тарас Бульба",
        "author": "Микола Гоголь",
        "year": 1835,
        "genre": "Історичний роман"
    },
    {
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "year": 1840,
        "genre": "Збірка віршів"
    },
    {
        "title": "Захар Беркут",
        "author": "Іван Франко",
        "year": 1883,
        "genre": "Історичний роман"
    },
    {
        "title": "Собор Паризької Богоматері",
        "author": "Віктор Гюго",
        "year": 1831,
        "genre": "Роман"
    }
]



@app.get('/api/')
def index() -> dict:
    return {'status': 'OK'}


@app.get('/')
def index_web(request: Request):

    return templates.TemplateResponse('index.html', {'request': request, 'books': books, 'title': 'Main page'})
