import uuid

from database import Product, session, User
from fastapi import HTTPException

from utils.utils_hashlib import get_password_hash


def create_product(name: str, description: str, price: float, quantity: int, cover_url) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        cover_url=str(cover_url),
    )
    session.add(product)
    session.commit()
    return product


def get_all_products(limit: int, skip: int, name: str | None) -> list[Product]:
    if name:
        products = session.query(Product).filter(Product.name.icontains(name)).limit(limit).offset(skip).all()
    else:
        products = session.query(Product).limit(limit).offset(skip).all()
    return products


def get_product_by_id(product_id) -> Product | None:
    product = session.query(Product).filter(Product.id == product_id).first()
    return product


def update_product(product_id: int, product_data: dict) -> Product:
    session.query(Product).filter(Product.id==product_id).update(product_data)
    session.commit()
    product = session.query(Product).filter(Product.id==product_id).first()
    return product


def delete_product(product_id) -> None:
    session.query(Product).filter(Product.id==product_id).delete()
    session.commit()


def create_user(name: str, email: str, password: str) -> User:
    try:
        user = User(
            name=name,
            email=email,
            hashed_password=get_password_hash(password),
        )
        session.add(user)
        session.commit()
        return user
    except Exception:
        session.rollback()


def get_user_by_email(email: str) -> User | None:
    user = session.query(User).filter(User.email == email).first()
    return user


def get_user_by_uuid(user_uuid: uuid.UUID) -> User | None:
    user = session.query(User).filter(User.user_uuid == user_uuid).first()
    return user


def activate_user_account(user: User) -> User:
    if user.is_verified:
        # raise HTTPException(status_code=400, detail='Already was verified')
        return user

    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
