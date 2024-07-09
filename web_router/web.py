from fastapi.requests import Request
from fastapi import Query, Path, HTTPException, APIRouter, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates

import dao
from background_tasks.confirm_registration import confirm_registration
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


@web_router.get('/product/{product_id}', include_in_schema=True)
def get_product_by_id_web(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    context = {
        'request': request,
        'product': product,
        'title': f'Дані по продукту {product.name} з ціною {product.price}'
    }
    return templates.TemplateResponse('details.html', context=context)


@web_router.get('/register/', include_in_schema=True)
@web_router.post('/register/', include_in_schema=True)
def web_register(
        request: Request,
        background_tasks: BackgroundTasks,
        name: str = Form(None),
        email: str = Form(None),
        password: str = Form(None),
):
    if request.method == 'GET':
        context = {
            'request': request,
            'title': 'Register'
        }
        return templates.TemplateResponse('registration.html', context=context)

    # maybe_user = dao.get_user_by_email(new_user.email)
    # if maybe_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f'User with email {new_user.email} already exists'
    #     )

    created_user = dao.create_user(name, email, password)
    background_tasks.add_task(confirm_registration, created_user, request.base_url)
    context = {
        'request': request,
        'title': 'Register',
        'products': get_all_products(limit=100, skip=0, name=''),
        'user': created_user
    }
    return templates.TemplateResponse('index.html', context=context)



