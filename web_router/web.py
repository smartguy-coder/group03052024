from fastapi.requests import Request
from fastapi import Query, Path, HTTPException, APIRouter
from fastapi.templating import Jinja2Templates

from dao import get_all_products

templates = Jinja2Templates(directory='templates')

web_router = APIRouter(
    prefix='',
)


@web_router.get('/', include_in_schema=True)
def index(request: Request) -> dict:
    context = {
        'request': request,
        'products': get_all_products(50, 0, ''),
        'title': 'Main page'
    }
    return templates.TemplateResponse('index.html', context=context)
