from typing import Optional, Tuple

from sqlalchemy import func, select

from app.database.repos.base_repo import BaseRepo
from app.database.models import Order, OrderStatus


class OrdersRepo(BaseRepo):
    def statuses(self) -> list[str]:
        return list(OrderStatus)

    async def create(self) -> Order:
        new_order = Order(
            status=OrderStatus.CREATED
        )
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def read(
        self,
        id: int
    ) -> Optional[Order]:
        return await self.session.get(Order, id)

    async def update(
        self,
        id: int,
        status: Optional[OrderStatus] = None
    ) -> Order:
        order = await self.read(id)
        if order is None:
            raise ValueError("Order not found")

        if (
            status is not None
            and status != order.status
        ):
            order.status = status
            await self.session.commit()
            await self.session.refresh(order)

        return order

    async def items(
        self,
        page: int,
        items_on_page: int,
        status: Optional[OrderStatus] = None
    ) -> Tuple[list[Order], int, int]:
        total_count = await self.session.execute(
            select(func.count()).select_from(Order).where(
                (Order.status == status) if status is not None else True
            )
        )
        total_count = total_count.scalar()
        total_pages = (total_count + items_on_page - 1) // items_on_page

        # Принудительное изменение номера страницы
        if page > total_pages:
            page = total_pages

        if total_count == 0:
            return [], 1, 1, 0

        offset = (page - 1) * items_on_page
        Ts = await self.session.execute(
            select(Order).where(
                (Order.status == status) if status is not None else True
            ).offset(offset).limit(items_on_page)
        )

        return Ts.unique().scalars().all(), page, total_pages, total_count
