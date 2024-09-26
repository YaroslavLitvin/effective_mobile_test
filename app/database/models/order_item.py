from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import relationship

from .base import Base, TableNameMixin, ToSchemaMixin
from app.schemas.v1.order_item import S_OrderItemFull


class OrderItem(Base, TableNameMixin, ToSchemaMixin):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer,
        ForeignKey('orders.id'),
        nullable=False,
        unique=False
    )
    product_id = Column(
        Integer,
        ForeignKey('products.id'),
        nullable=False,
        unique=False
    )
    quantity = Column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_non_negative'),
    )

    order = relationship(
        "Order",
        back_populates="order_items",
        lazy='joined'
    )
    product = relationship(
        "Product",
        back_populates="order_items",
        lazy='joined'
    )

    def to_schema(self) -> S_OrderItemFull:
        return S_OrderItemFull(
            id=self.id,
            order_id=self.order_id,
            product=self.product.to_schema(),
            quantity=self.quantity,
        )
