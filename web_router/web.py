from uuid import UUID

import stripe
from fastapi import (APIRouter, BackgroundTasks, Depends, Form, HTTPException,
                     Path, Query, status)
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import dao
from background_tasks.confirm_registration import confirm_registration
from config import STRIPE_KEY
from dao import get_all_products, get_product_by_id
from database import Order, OrderProduct, session
from utils.jwt_auth import get_user_web, set_cookies_web
from utils.utils_hashlib import verify_password

templates = Jinja2Templates(directory='templates')

stripe.api_key = STRIPE_KEY

web_router = APIRouter(
    prefix='',
)


@web_router.post('/payment')
def payment(request: Request, user=Depends(get_user_web)):
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    cart = dao.fetch_order_products(order.id)
    total = round(sum([order_product.cost for order_product in cart]), 2)
    line_items: list[dict] = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': order_product.product.name,
                    'description': order_product.product.description,
                    'images': [order_product.product.cover_url]
                },
                'unit_amount': int(order_product.price * 100)
            },
            'quantity': order_product.quantity
        } for order_product in cart
    ]

    session_stripe: dict = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=request.url_for('success_payment'),
        cancel_url=request.url_for('cancel_payment'),
        customer_email=user.email,
        # locale='uk',
        metadata={'user_uuid': user.user_uuid, 'total': total, 'order_id': order.id},
    )

    # n = {"id": "cs_test_a1ls58kJbCd9MRwTViv9qATiQy4MMVFXdLI7lY9Ey7Q1LZuYZ35PP7r2Op", "object": "checkout.session",
    #      "after_expiration": null, "allow_promotion_codes": null, "amount_subtotal": 580800, "amount_total": 580800,
    #      "automatic_tax": {"enabled": false, "liability": null, "status": null}, "billing_address_collection": null,
    #      "cancel_url": "https://96ea-176-119-83-0.ngrok-free.app/cancel_payment", "client_reference_id": null,
    #      "client_secret": null, "consent": null, "consent_collection": null, "created": 1721754145, "currency": "usd",
    #      "currency_conversion": null, "custom_fields": [],
    #      "custom_text": {"after_submit": null, "shipping_address": null, "submit": null,
    #                      "terms_of_service_acceptance": null}, "customer": null, "customer_creation": "if_required",
    #      "customer_details": {"address": null, "email": "12345@ukr.net", "name": null, "phone": null,
    #                           "tax_exempt": "none", "tax_ids": null}, "customer_email": "12345@ukr.net",
    #      "expires_at": 1721840545, "invoice": null, "invoice_creation": {"enabled": false,
    #                                                                      "invoice_data": {"account_tax_ids": null,
    #                                                                                       "custom_fields": null,
    #                                                                                       "description": null,
    #                                                                                       "footer": null,
    #                                                                                       "issuer": null,
    #                                                                                       "metadata": {},
    #                                                                                       "rendering_options": null}},
    #      "livemode": false, "locale": null, "metadata": {"our_metadata": "78787877"}, "mode": "payment",
    #      "payment_intent": null, "payment_link": null, "payment_method_collection": "if_required",
    #      "payment_method_configuration_details": null,
    #      "payment_method_options": {"card": {"request_three_d_secure": "automatic"}}, "payment_method_types": ["card"],
    #      "payment_status": "unpaid", "phone_number_collection": {"enabled": false}, "recovered_from": null,
    #      "saved_payment_method_options": null, "setup_intent": null, "shipping_address_collection": null,
    #      "shipping_cost": null, "shipping_details": null, "shipping_options": [], "status": "open", "submit_type": null,
    #      "subscription": null, "success_url": "https://96ea-176-119-83-0.ngrok-free.app/success_payment",
    #      "total_details": {"amount_discount": 0, "amount_shipping": 0, "amount_tax": 0}, "ui_mode": "hosted",
    #      "url": "https://checkout.stripe.com/c/pay/cs_test_a1ls58kJbCd9MRwTViv9qATiQy4MMVFXdLI7lY9Ey7Q1LZuYZ35PP7r2Op#fidkdWxOYHwnPyd1blpxYHZxWjA0VWBLbklXc09uRjBrXGxwaXFIYWFBQ3A2Ykh9NmtdVE9DdmhEdzJKbEpLTkh1PWhpNDQ2YUh9YWtiQTN3ZjFPZkFQSDYxZ2QxQm5DQEB9Vk5qcFVjUGJGNTVsfFFwQkgzSCcpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"}

    return RedirectResponse(session_stripe['url'], status_code=status.HTTP_303_SEE_OTHER)


@web_router.get('/success_payment')
def success_payment(request: Request, user=Depends(get_user_web)):
    context = {
        'request': request,
        'title': 'success payment',
        'user': user
    }
    response = templates.TemplateResponse('success_payment.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get('/cancel_payment')
def cancel_payment():
    pass


@web_router.post('/web_hook_payment')
def web_hook_payment(data: dict):
    n = {'id': 'evt_1PfmSbRvJkC5nYiuZcj7BJaL', 'object': 'event', 'api_version': '2024-06-20', 'created': 1721755512,
         'data': {'object': {'id': 'cs_test_a1hEyG1x8EtCPlm5rVW3jrN8HLVqEIBPAzM6aENJIlC0ifMv1Dy2esougo',
                             'object': 'checkout.session', 'after_expiration': None, 'allow_promotion_codes': None,
                             'amount_subtotal': 580800, 'amount_total': 580800,
                             'automatic_tax': {'enabled': False, 'liability': None, 'status': None},
                             'billing_address_collection': None,
                             'cancel_url': 'https://96ea-176-119-83-0.ngrok-free.app/cancel_payment',
                             'client_reference_id': None, 'client_secret': None, 'consent': None,
                             'consent_collection': None, 'created': 1721755489, 'currency': 'usd',
                             'currency_conversion': None, 'custom_fields': [],
                             'custom_text': {'after_submit': None, 'shipping_address': None, 'submit': None,
                                             'terms_of_service_acceptance': None}, 'customer': None,
                             'customer_creation': 'if_required', 'customer_details': {
                 'address': {'city': None, 'country': 'UA', 'line1': None, 'line2': None, 'postal_code': None,
                             'state': None}, 'email': '12345@ukr.net', 'name': 'kjfhjgfhj', 'phone': None,
                 'tax_exempt': 'none', 'tax_ids': []}, 'customer_email': '12345@ukr.net', 'expires_at': 1721841889,
                             'invoice': None, 'invoice_creation': {'enabled': False,
                                                                   'invoice_data': {'account_tax_ids': None,
                                                                                    'custom_fields': None,
                                                                                    'description': None, 'footer': None,
                                                                                    'issuer': None, 'metadata': {},
                                                                                    'rendering_options': None}},
                             'livemode': False, 'locale': None, 'metadata': {'our_metadata': '78787877'},
                             'mode': 'payment', 'payment_intent': 'pi_3PfmSYRvJkC5nYiu1W4lMDqC', 'payment_link': None,
                             'payment_method_collection': 'if_required', 'payment_method_configuration_details': None,
                             'payment_method_options': {'card': {'request_three_d_secure': 'automatic'}},
                             'payment_method_types': ['card'], 'payment_status': 'paid',
                             'phone_number_collection': {'enabled': False}, 'recovered_from': None,
                             'saved_payment_method_options': None, 'setup_intent': None,
                             'shipping_address_collection': None, 'shipping_cost': None, 'shipping_details': None,
                             'shipping_options': [], 'status': 'complete', 'submit_type': None, 'subscription': None,
                             'success_url': 'https://96ea-176-119-83-0.ngrok-free.app/success_payment',
                             'total_details': {'amount_discount': 0, 'amount_shipping': 0, 'amount_tax': 0},
                             'ui_mode': 'hosted', 'url': None}}, 'livemode': False, 'pending_webhooks': 3,
         'request': {'id': None, 'idempotency_key': None}, 'type': 'checkout.session.completed'}
    try:
        event = stripe.Event.construct_from(data, STRIPE_KEY)
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(detail='NOT STRIPE DATA', status_code=status.HTTP_400_BAD_REQUEST)
    print(event)
    if event['type'] == 'checkout.session.completed':
        print(999999999999)
        user_uuid = event['data']['object']['metadata']['user_uuid']
        user = dao.get_user_by_uuid(UUID(user_uuid))
        order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
        # todo check sums
        order.is_closed = True
        session.add(order)
        session.commit()

@web_router.get('/', include_in_schema=True)
@web_router.post('/', include_in_schema=True)
def index(request: Request, user=Depends(get_user_web), query: str = Form(None)):
    _ = request.state.gettext
    context = {
        'request': request,
        'products': get_all_products(50, 0, query),
        'title': 'Main page',
        'user': user,

        'details': _('details'),
        'buy_product': _('buy product'),
    }
    response = templates.TemplateResponse('index.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies


@web_router.get('/set-lang/{lang}', include_in_schema=True)
def set_lang(request: Request, lang: str):
    redirect_url = request.url_for('index')
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    if lang in {'uk', 'ru', 'en'}:
        response.set_cookie('lang', lang)
    return response


@web_router.get('/cart', include_in_schema=True)
def cart(request: Request, user=Depends(get_user_web)):
    if not user:
        context = {
            'request': request,
            'products': get_all_products(50, 0, ''),
            'title': 'Main page',
        }
        return templates.TemplateResponse('index.html', context=context)

    order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    cart = dao.fetch_order_products(order.id)

    total = round(sum([order_product.cost for order_product in cart]), 2)

    context = {
        'request': request,
        'cart': cart,
        'title': 'Кошик',
        'user': user,
        'total': total,
    }
    response = templates.TemplateResponse('cart.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies

@web_router.get('/set-lang', include_in_schema=True)
def set_lang(request: Request, user=Depends(get_user_web)):
    context = {
        'request': request,
        'products': get_all_products(50, 0, ''),
        'title': 'Main page',
        'user': user,
    }
    response = templates.TemplateResponse('index.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    response_with_cookies.set_cookie('language', 'uk')
    return response_with_cookies

@web_router.get('/set-lang-ru', include_in_schema=True)
def set_lang_ru(request: Request, user=Depends(get_user_web)):
    context = {
        'request': request,
        'products': get_all_products(50, 0, ''),
        'title': 'Main page',
        'user': user,
    }
    response = templates.TemplateResponse('index.html', context=context)
    response_with_cookies = set_cookies_web(user, response)
    response_with_cookies.set_cookie('language', 'ru')
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
        response_with_cookies = set_cookies_web(maybe_user, response)
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


@web_router.post('/add-product-to-cart/')
def add_product_to_cart(request: Request, product_id: int = Form(), user=Depends(get_user_web)):
    product = dao.get_product_by_id(product_id)
    if not all([user, product]):
        context = {
            'request': request,
            'products': get_all_products(50, 0, ''),
            'title': 'Main page',
        }
        return templates.TemplateResponse('index.html', context=context)
    order: Order = dao.get_or_create(Order, user_id=user.id, is_closed=False)
    order_product: OrderProduct = dao.get_or_create(OrderProduct, order_id=order.id, product_id=product_id)
    order_product.quantity += 1
    order_product.price = product.price
    session.add(order_product)
    session.commit()
    session.refresh(order_product)

    redirect_url = request.url_for('index')
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response_with_cookies = set_cookies_web(user, response)
    return response_with_cookies
