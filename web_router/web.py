from fastapi.requests import Request
from fastapi import Query, Path, HTTPException, APIRouter, Form, BackgroundTasks, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import dao
from background_tasks.confirm_registration import confirm_registration
from dao import get_all_products, get_product_by_id
from utils.jwt_auth import set_cookies_web, get_user_web
from utils.utils_hashlib import verify_password

templates = Jinja2Templates(directory='templates')

web_router = APIRouter(
    prefix='',
)


@web_router.get('/', include_in_schema=True)
@web_router.post('/', include_in_schema=True)
def index(request: Request, user=Depends(get_user_web), query: str = Form(None)):
    context = {
        'request': request,
        'products': get_all_products(50, 0, query),
        'title': 'Main page',
        'user': user
    }
    response = templates.TemplateResponse('index.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get('/product/{product_id}', include_in_schema=True)
def get_product_by_id_web(request: Request, product_id: int, user=Depends(get_user_web)):
    product = get_product_by_id(product_id)
    context = {
        'request': request,
        'product': product,
        'title': f'Дані по продукту {product.name} з ціною {product.price}',
        'user': user,

    }
    response = templates.TemplateResponse('details.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.post('/add-product-to-cart/')
def add_product_to_cart(product_id: int):
    print(9999999999, product_id)
    pass


@web_router.get('/register/', include_in_schema=True)
@web_router.post('/register/', include_in_schema=True)
def web_register(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    user=Depends(get_user_web)
):
    if user:
        redirect_url = request.url_for('index')
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies

    if request.method == 'GET':
        context = {
            'request': request,
            'title': 'Register'
        }
        return templates.TemplateResponse('registration.html', context=context)

    maybe_user = dao.get_user_by_email(email)
    context = {
        'request': request,
        'title': 'Register',
        'products': get_all_products(limit=100, skip=0, name=''),
        'user': maybe_user
    }
    if not maybe_user:
        created_user = dao.create_user(name, email, password)
        background_tasks.add_task(confirm_registration, created_user, request.base_url)
        context['user'] = created_user

    # response = templates.TemplateResponse('index.html', context=context)
    redirect_url = request.url_for('index')
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response_with_cookies = set_cookies_web(context['user'], response)
    return response_with_cookies


@web_router.get('/login/', include_in_schema=True)
@web_router.post('/login/', include_in_schema=True)
def web_login(
        request: Request,
        email: str = Form(None),
        password: str = Form(None),
        user=Depends(get_user_web)
):
    if user:
        redirect_url = request.url_for('index')
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies

    context = {'request': request}

    if request.method == 'GET':
        context['title'] = 'Login'
        return templates.TemplateResponse('login.html', context=context)

    maybe_user = dao.get_user_by_email(email)
    if not maybe_user:
        context['title'] = 'Login'
        context['error'] = True
        context['email_value'] = email

        return templates.TemplateResponse('login.html', context=context)

    if verify_password(password, maybe_user.hashed_password):
        context = {
            'title': 'Login',
            'products': get_all_products(limit=100, skip=0, name=''),
            'user': maybe_user,
            **context,
        }
        response = templates.TemplateResponse('index.html', context=context)
        response_with_cookies = set_cookies_web(user, response)
        return response_with_cookies

    context['title'] = 'Login'
    context['error'] = True
    context['email_value'] = email
    return templates.TemplateResponse('login.html', context=context)


@web_router.get('/logout/', include_in_schema=True)
def web_logout(request: Request):
    context = {
        'request': request,
        'products': get_all_products(50, 0, ''),
        'title': 'Main page',
        'user': None
    }
    response = templates.TemplateResponse('index.html', context=context)
    response.delete_cookie(key='token_user_hillel')
    return response
