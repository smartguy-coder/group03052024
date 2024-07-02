from database import Product, session
from fastapi import HTTPException


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
