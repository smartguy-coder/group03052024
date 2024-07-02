from fastapi.requests import Request
from fastapi import Query, Path, HTTPException, APIRouter, Form
from fastapi.templating import Jinja2Templates

from dao import get_all_products, get_product_by_id

templates = Jinja2Templates(directory='templates')

web_router = APIRouter(
    prefix='',
)


@web_router.get('/', include_in_schema=True)
@web_router.post('/', include_in_schema=True)
def index(request: Request, query: str = Form(None)):
    context = {
        'request': request,
        'products': get_all_products(50, 0, query),
        'title': 'Main page'
    }
    return templates.TemplateResponse('index.html', context=context)


@web_router.get('/{product_id}', include_in_schema=True)
def get_product_by_id_web(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    context = {
        'request': request,
        'product': product,
        'title': f'Дані по продукту {product.name} з ціною {product.price}'
    }
    return templates.TemplateResponse('details.html', context=context)
