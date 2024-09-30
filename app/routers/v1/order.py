import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.dependencies.v1.database import D_DbRepo
from app.dependencies.v1.pagination import D_PaginationParams
from app.schemas.v1.order import (
    OrderStatus,
    S_Order,
    S_OrderFull,
    S_OrderInput,
    S_OrderOptional,
    S_OrderPagination
)


router = APIRouter(
    prefix='/orders',
    tags=['V1/Orders']
)
log = logging.getLogger(__name__)


@router.get("",
            response_model=S_OrderPagination
            )
async def order_list(
    db_repo: D_DbRepo,
    pagination: D_PaginationParams = Query(...),
    status: Optional[OrderStatus] = Query(None)
):
    (
        item_list, current_page,
        total_pages, total_count
    ) = await db_repo.orders.items(
        page=pagination.page,
        items_on_page=pagination.items_on_page,
        status=status
    )
    return S_OrderPagination(
        items=[item.to_schema() for item in item_list],
        current_page=current_page,
        last_page=total_pages,
        total=total_count
    )


@router.get("/statuses",
            response_model=List[str]
            )
async def order_statuses(
    db_repo: D_DbRepo
):
    return db_repo.orders.statuses()


@router.post("",
             response_model=S_OrderFull,
             status_code=201
             )
async def create_order(
    new_order: S_OrderInput,
    db_repo: D_DbRepo
):
    if len(new_order.items) == 0:
        raise HTTPException(400, 'No items in the order.')

    order_products = [
        (await db_repo.products.is_in_stock(i.product_id, i.quantity))
        for i in new_order.items
    ]

    not_in_stock_id = ''
    out_of_stock_id = ''
    for i, product in enumerate(order_products):
        # Собираем идентификаторы товаров, которых нет в БД.
        if product is None:
            not_in_stock_id += f'{new_order.items[i].product_id}, '

        # Собираем идентификаторы товаров, которых нет в наличии (кол-тво).
        if isinstance(product, bool) and product is False:
            out_of_stock_id += f'{new_order.items[i].product_id}, '

    # Удаляем лишние символы
    if len(not_in_stock_id) > 0:
        not_in_stock_id = not_in_stock_id[:-2]

    # Удаляем лишние символы
    if len(out_of_stock_id) > 0:
        out_of_stock_id = out_of_stock_id[:-2]

    # Генерируем исключение если есть id товаров, не прошедших валидацию.
    if len(not_in_stock_id) > 0 or len(out_of_stock_id) > 0:
        raise HTTPException(
            404,
            "Follow products' ids are: "
            f'NOT IN STOCK ({not_in_stock_id}), '
            f'OUT OF STOCK ({out_of_stock_id}).'
        )

    # Уменьшаем количество товаров в БД
    for i in new_order.items:
        await db_repo.products.update(id=i.product_id, quantity_inc=-i.quantity)

    # Создаем новый заказ
    order = await db_repo.orders.create()

    # Формируем список записей в БД
    order_products = [
        (await db_repo.order_items.create(
            order_id=order.id,
            product_id=product.id,
            quantity=new_order.items[i].quantity,
        ))
        for i, product in enumerate(order_products)
    ]

    # Преобразование в pydantic схемы
    order_products = [product.to_schema() for product in order_products]

    result = order.to_schema()
    result.items = order_products

    return result


@router.get("/{id}",
            response_model=S_OrderFull
            )
async def order_info_by_id(
    id: int,
    db_repo: D_DbRepo
):
    entry = await db_repo.orders.read(id)
    if entry is None:
        raise HTTPException(
            404,
            f"Entry with id={id} not found."
        )
    return entry.to_schema()


@router.patch("/{id}/status",
              response_model=S_OrderFull
              )
async def update_order_status(
    id: int,
    status: OrderStatus,
    db_repo: D_DbRepo
):
    try:
        entry = await db_repo.orders.update(id=id, status=status)
    except ValueError:
        raise HTTPException(
            404,
            f"Entry with id={id} not found."
        )

    return entry.to_schema()
