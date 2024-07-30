from gettext import translation

import sentry_sdk
from fastapi import FastAPI, Request

import config
from api_router.api_products import api_router_products
from api_router.api_users import api_router_users
from database import create_tables
from web_router.web import web_router


def lifespan(app: FastAPI):
    create_tables()
    yield


sentry_sdk.init(
    dsn=config.SENTRY_KEY,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(
    debug=config.DEBUG,
    lifespan=lifespan,
)


@app.middleware("http")
async def set_language_middleware(request: Request, call_next):
    lang = request.cookies.get("lang", "uk")
    translator = translation("this_project", localedir="locale", languages=[lang], fallback=True)
    _ = translator.gettext
    request.state.gettext = _

    response = await call_next(request)
    return response


app.include_router(api_router_products)
app.include_router(api_router_users)
app.include_router(web_router)
