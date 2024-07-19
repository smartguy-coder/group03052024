from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, Sequence, String, Text, Float, DateTime, create_engine, UUID, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import config

Base = declarative_base()


class BaseInfoMixin:
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)





class User(BaseInfoMixin, Base):
    __tablename__ = 'users'

    name = Column(String, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    user_uuid = Column(UUID, default=uuid.uuid4)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    def __str__(self):
        return f'<User: {self.id=}; {self.name=}>'

    __repr__ = __str__


class Order(BaseInfoMixin, Base):
    __tablename__ = 'orders'

    user_id = Column(ForeignKey('users.id'), nullable=False)
    is_closed = Column(Boolean, default=False)

    def __str__(self):
        return f'<Order: {self.id=}; {self.user_id=}; {self.is_closed=}>'

    __repr__ = __str__



class OrderProduct(BaseInfoMixin, Base):
    __tablename__ = 'order_products'

    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    price = Column(Float, nullable=False, default=10.0)
    quantity = Column(Integer, nullable=False, default=0)

    product = relationship('Product', back_populates='products')

    @property
    def cost(self):
        return self.quantity * self.price

    def __str__(self):
        return f'<OrderProduct: {self.id=}; {self.order_id=}; {self.quantity=}; {self.price=}, cost={self.cost}>'

    __repr__ = __str__


class Product(BaseInfoMixin, Base):
    __tablename__ = 'products'

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    cover_url = Column(Text, nullable=False)
    price = Column(Float, nullable=False, default=10.0)
    quantity = Column(Integer, nullable=False)

    products = relationship('OrderProduct', back_populates='product')

    def __str__(self):
        return f'<Product: {self.id=}; {self.name=}; {self.quantity=}; {self.price=}>'

    __repr__ = __str__

engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
