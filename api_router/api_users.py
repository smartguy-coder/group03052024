import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import dao
from api_router.schemas_users import BaseUserInfo, RegisterUserRequest
from background_tasks.confirm_registration import confirm_registration
from utils.jwt_auth import create_jwt
from utils.utils_hashlib import verify_password

api_router_users = APIRouter(prefix="/api/users", tags=["API", "Users"])


@api_router_users.post("/token/")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.password, form_data.username)
    maybe_user = dao.get_user_by_email(form_data.username)
    if not maybe_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect data111")

    if verify_password(form_data.password, maybe_user.hashed_password):
        return {"access_token": create_jwt(user=maybe_user)}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password 22222")


@api_router_users.post("/create/", status_code=status.HTTP_201_CREATED)
def create_user(
    request: Request,
    new_user: RegisterUserRequest,
    background_tasks: BackgroundTasks,
) -> BaseUserInfo:
    maybe_user = dao.get_user_by_email(new_user.email)
    if maybe_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User with email {new_user.email} already exists"
        )

    created_user = dao.create_user(**new_user.dict())
    background_tasks.add_task(confirm_registration, created_user, request.base_url)
    return created_user


@api_router_users.get("/verify/{user_uuid}")
def verify_user_account(user_uuid: uuid.UUID):
    maybe_user = dao.get_user_by_uuid(user_uuid)
    if not maybe_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong data")
    dao.activate_user_account(maybe_user)
    return {"verified": True, "user_email": maybe_user.email}
