from fastapi import FastAPI, Request, Query, Path, HTTPException, status

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

import config
import dao
from database import create_tables
from schemas import NewProduct, CreatedProduct, DeletedProduct

templates = Jinja2Templates(directory='templates')


def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    debug=config.DEBUG,
    lifespan=lifespan,
)


@app.post('/api/products/create/', status_code=status.HTTP_201_CREATED, tags=['API', 'Products'])
def create_product(new_product: NewProduct) -> CreatedProduct:
    created_product = dao.create_product(**new_product.dict())
    return created_product


@app.get('/api/products/', tags=['API', 'Products'])
def get_products(
        limit: int = Query(default=5, gt=0, le=50, description='Number of products'),
        skip: int = Query(default=0, ge=0, description='How many to skip'),
        name: str = Query(default='', description='Part of the product name'),
) -> list[CreatedProduct]:
    products = dao.get_all_products(limit=limit, skip=skip, name=name)
    return products


@app.get('/api/products/{product_id}', tags=['API', 'Products'])
def get_product(
        product_id: int = Path(gt=0, description='ID of the product'),
) -> CreatedProduct:
    product = dao.get_product_by_id(product_id=product_id)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')


@app.put('/api/products/{product_id}', tags=['API', 'Products'])
def update_product(
        updated_product: NewProduct,
        product_id: int = Path(gt=0, description='ID of the product'),
) -> CreatedProduct:
    product = dao.get_product_by_id(product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    product = dao.update_product(product_id, updated_product.dict())
    return product


@app.delete('/api/products/{product_id}', tags=['API', 'Products'])
def delete_product(
        product_id: int = Path(gt=0, description='ID of the product'),
) -> DeletedProduct:
    product = dao.get_product_by_id(product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    dao.delete_product(product_id=product_id)
    return DeletedProduct(id=product_id)



@app.get('/', include_in_schema=False)
def index_web(request: Request):

    return templates.TemplateResponse('index.html', {'request': request, 'books': {}, 'title': 'Main page'})
