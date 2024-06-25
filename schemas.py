from datetime import datetime

from pydantic import BaseModel, Field


class NewProduct(BaseModel):
    name: str = Field(max_length=100, min_length=2, examples=['iPhoneX'])
    description: str = Field(default='', examples=['Old phone'])
    price: float = Field(ge=0.01, examples=[100.78])
    quantity: int = Field(default=11, gt=0, examples=[100])


class ProductId(BaseModel):
    id: int = Field(description='ID of created item')


class CreatedProduct(NewProduct, ProductId):
    created_at: datetime
    updated_at: datetime


class DeletedProduct(ProductId):
    status: bool = True
