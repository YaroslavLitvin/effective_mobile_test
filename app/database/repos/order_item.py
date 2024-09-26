from typing import Optional

from .base_repo import BaseRepo
from app.database.models import OrderItem


class OrderItemsRepo(BaseRepo):
    async def create(
        self,
        order_id: int,
        product_id: int,
        quantity: int
    ) -> OrderItem:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity
        )
        self.session.add(order_item)
        await self.session.commit()
        await self.session.refresh(order_item)
        return order_item

    async def read(self, id: int) -> Optional[OrderItem]:
        return await self.session.get(OrderItem, id)

    async def update(
        self,
        order_id: Optional[int] = None,
        product_id: Optional[int] = None,
        quantity: Optional[int] = None,
    ) -> OrderItem:
        entry = await self.read(id)

        if entry is None:
            raise ValueError("Order item not found")

        if order_id is not None:
            entry.order_id = order_id

        if product_id is not None:
            entry.product_id = product_id

        if quantity is not None:
            entry.quantity = quantity

        await self.session.commit()
        await self.session.refresh(entry)
        return entry
