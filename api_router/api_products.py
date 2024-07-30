from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status

import dao
from api_router.schemas_products import (CreatedProduct, DeletedProduct,
                                         NewProduct)

api_router_products = APIRouter(prefix="/api/products", tags=["API", "Products"])


@api_router_products.post("/create/", status_code=status.HTTP_201_CREATED)
def create_product(new_product: NewProduct) -> CreatedProduct:
    created_product = dao.create_product(**new_product.dict())
    return created_product


@api_router_products.get("/")
def get_products(
    limit: int = Query(default=5, gt=0, le=50, description="Number of products"),
    skip: int = Query(default=0, ge=0, description="How many to skip"),
    name: str = Query(default="", description="Part of the product name"),
) -> list[CreatedProduct]:
    products = dao.get_all_products(limit=limit, skip=skip, name=name)
    return products


@api_router_products.get("/{product_id}")
def get_product(
    product_id: int = Path(gt=0, description="ID of the product"),
) -> CreatedProduct:
    product = dao.get_product_by_id(product_id=product_id)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@api_router_products.put("/{product_id}")
def update_product(
    updated_product: NewProduct,
    product_id: int = Path(gt=0, description="ID of the product"),
) -> CreatedProduct:
    product = dao.get_product_by_id(product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    product = dao.update_product(product_id, updated_product.dict())
    return product


@api_router_products.delete("/{product_id}")
def delete_product(
    product_id: int = Path(gt=0, description="ID of the product"),
) -> DeletedProduct:
    product = dao.get_product_by_id(product_id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    dao.delete_product(product_id=product_id)
    return DeletedProduct(id=product_id)
