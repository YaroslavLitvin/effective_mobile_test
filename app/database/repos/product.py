from typing import Optional, Tuple, Union

from sqlalchemy import func, select

from app.database.repos.base_repo import BaseRepo
from app.database.models import Product


class ProductsRepo(BaseRepo):
    async def create(
        self,
        name: str,
        description: Optional[str],
        price: int,
        quantity: int
    ) -> Product:
        new_entry = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            is_deleted=False
        )
        self.session.add(new_entry)
        await self.session.commit()
        await self.session.refresh(new_entry)
        return new_entry

    async def read(
        self,
        id: int
    ) -> Optional[Product]:
        return await self.session.get(Product, id)

    async def update(
        self,
        id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[int] = None,
        quantity: Optional[int] = None,
        quantity_inc: Optional[int] = None,
        is_deleted: Optional[bool] = None
    ) -> Product:
        entry = await self.read(id)

        if entry is None:
            raise ValueError("Product not found")

        if name is not None:
            entry.name = name
        if description is not None:
            entry.description = description
        if price is not None:
            entry.price = price
        if quantity is not None:
            entry.quantity = quantity
        if quantity_inc is not None:
            entry.quantity += quantity_inc
        if is_deleted is not None:
            entry.is_deleted = is_deleted

        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def items(
        self,
        page: int,
        items_on_page: int,
        is_deleted: Optional[bool]
    ) -> Tuple[list[Product], int, int]:
        total_count = await self.session.execute(
            select(func.count()).select_from(Product).where(
                (
                    (Product.is_deleted == is_deleted)
                    if is_deleted is not None else True
                )
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
            select(Product).where(
                (
                    (Product.is_deleted == is_deleted)
                    if is_deleted is not None else True
                )
            ).offset(offset).limit(items_on_page)
        )

        return Ts.unique().scalars().all(), page, total_pages, total_count

    async def is_in_stock(
        self,
        product_id: int,
        quantity: int = 0
    ) -> Optional[Union[bool, Product]]:
        product = await self.read(id=product_id)
        if product is None or product.is_deleted:
            return None
        return product if product.quantity >= quantity else False
