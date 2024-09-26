from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship


from app.schemas.v1.order import OrderStatus, S_OrderFull
from .base import (
    Base,
    TableNameMixin,
    TimestampMixin,
    ToSchemaMixin
)


class Order(Base, TableNameMixin, TimestampMixin, ToSchemaMixin):
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatus))

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        lazy='joined'
    )

    def to_schema(self) -> S_OrderFull:
        result = S_OrderFull(
            id=self.id,
            status=self.status,
            items=[item.to_schema() for item in self.order_items],
            created_at=self.created_at
        )
        return result
