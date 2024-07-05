from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, Sequence, String, Text, Float, DateTime, create_engine, UUID, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

import config

Base = declarative_base()


class BaseInfoMixin:
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Product(BaseInfoMixin, Base):
    __tablename__ = 'products'

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    cover_url = Column(Text, nullable=False)
    price = Column(Float, nullable=False, default=10.0)
    quantity = Column(Integer, nullable=False)

    def __str__(self):
        return f'<Product: {self.id=}; {self.name=}; {self.quantity=}; {self.price=}>'

    __repr__ = __str__


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


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
