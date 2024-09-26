from typing import Optional
from enum import Enum as PyEnum

from pydantic import (
    BaseModel,
    model_validator
)

from app.schemas.base import (
    PaginationBase,
    IdFieldMixin,
    TimestampFieldMixin
)
from app.schemas.v1.order_item import S_OrderItemFull, S_OrderItemInput


# Статусы заказа
class OrderStatus(PyEnum):
    CREATED = "CREATED"
    FORMED = "FORMED"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class StatusFieldMixin(BaseModel):
    status: OrderStatus


class S_OrderInput(BaseModel):
    items: list[S_OrderItemInput]


class S_Order(BaseModel):
    items: list[S_OrderItemFull]


class S_OrderOptional(BaseModel):
    status: Optional[OrderStatus] = None

    @model_validator(mode='after')
    def validate(self):
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("All fields are null")
        return self


class S_OrderFull(
    S_Order, TimestampFieldMixin,
    StatusFieldMixin, IdFieldMixin
):
    pass


class S_OrderPagination(PaginationBase[S_OrderFull]):
    pass
