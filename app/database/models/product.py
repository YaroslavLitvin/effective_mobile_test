from sqlalchemy import Boolean, Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship

from .base import (
    Base,
    TableNameMixin,
    TimestampMixin,
    ToSchemaMixin,
)
from app.schemas.v1.product import S_ProductFull


class Product(
    Base,
    TableNameMixin,
    TimestampMixin,
    ToSchemaMixin[S_ProductFull]
):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product",
        lazy='joined'
    )

    def to_schema(self) -> S_ProductFull:
        return S_ProductFull(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
        )
