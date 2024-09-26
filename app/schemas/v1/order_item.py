from pydantic import BaseModel

from app.schemas.base import IdFieldMixin, PaginationBase
from app.schemas.v1.product import S_ProductFull


class S_OrderItemOrderIdMixin(BaseModel):
    order_id: int


class S_OrderItemProductMixin(BaseModel):
    product: S_ProductFull


class S_OrderItemProductIdMixin(BaseModel):
    product_id: int


class S_OrderItemQuantityMixin(BaseModel):
    quantity: int


class S_OrderItem(
    S_OrderItemQuantityMixin,
    S_OrderItemProductMixin
):
    pass


class S_OrderItemInput(
    S_OrderItemQuantityMixin,
    S_OrderItemProductIdMixin
):
    pass


class S_OrderItemFull(S_OrderItem, IdFieldMixin):
    pass


class S_OrderItemFull(S_OrderItem, S_OrderItemOrderIdMixin, IdFieldMixin):
    pass


class S_OrderItemPagination(PaginationBase[S_OrderItemFull]):
    pass
