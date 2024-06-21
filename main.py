from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

import config
import dao
from database import create_tables
from schemas import NewProduct, CreatedProduct

templates = Jinja2Templates(directory='templates')


def lifespan(app: FastAPI):
    create_tables()
    yield



app = FastAPI(
    debug=config.DEBUG,
    lifespan=lifespan,
)




@app.post('/api/products/create/', status_code=status.HTTP_201_CREATED)
def create_product(new_product: NewProduct) -> CreatedProduct:
    created_product = dao.create_product(**new_product.dict())
    return created_product













@app.get('/api/')
def index() -> dict:
    # dao.create_product(nmae='name1', 'desvc', 10.56, 7)
    return {'status': 'OK'}




@app.get('/')
def index_web(request: Request):

    return templates.TemplateResponse('index.html', {'request': request, 'books': books, 'title': 'Main page'})
