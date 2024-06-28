from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, String, Text, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import config

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    cover_url = Column(Text, nullable=False)
    price = Column(Float, nullable=False, default=10.0)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'<Product: {self.id=}; {self.name=}; {self.quantity=}; {self.price=}>'

    __repr__ = __str__


engine = create_engine(config.DB_PATH, echo=config.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
