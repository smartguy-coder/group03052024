from database import Product, session


def create_product(name: str, description: str, price: float, quantity: int) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )
    session.add(product)
    session.commit()
    return product
