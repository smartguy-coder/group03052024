import datetime as dt

import jwt
from fastapi import Depends, HTTPException, Request, status
from starlette.responses import RedirectResponse

import dao
from config import JWT_KEY
from database import User
from security.security import oauth2_scheme


def encode_jwt(payload_data: dict) -> str:
    encode_jwt_ = jwt.encode(payload=payload_data, key=JWT_KEY, algorithm="HS256")
    return encode_jwt_


def decode_jwt(encoded_jwt: str) -> dict:
    try:
        decoded_data = jwt.decode(
            jwt=encoded_jwt,
            key=JWT_KEY,
            algorithms=["HS256"],
        )
        return decoded_data
    except jwt.exceptions.ExpiredSignatureError:
        return {}
    except jwt.exceptions.InvalidSignatureError:
        return {}


def create_jwt(user) -> str:
    payload = {
        "sub": user.email,
        "exp": dt.datetime.utcnow() + dt.timedelta(seconds=3000),
        "iat": dt.datetime.utcnow(),
    }
    jwt_token = encode_jwt(payload)
    return jwt_token


def set_cookies_web(user, response: RedirectResponse) -> RedirectResponse:
    if not user:
        return response

    jwt_token = create_jwt(user)
    response.set_cookie("token_user_hillel", jwt_token)
    return response


def get_user_web(request: Request) -> User | None:
    token = request.cookies.get("token_user_hillel")

    if not token:
        return

    user_data = decode_jwt(token)
    if not user_data:
        return
    user = dao.get_user_by_email(user_data["sub"])
    return user


def get_user_api(token: str = Depends(oauth2_scheme)) -> User | None:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_data = decode_jwt(token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = dao.get_user_by_email(user_data["sub"])
    return user


def get_user_api_only_admin(user: User = Depends(get_user_api)) -> User | None:
    if user.is_admin:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
