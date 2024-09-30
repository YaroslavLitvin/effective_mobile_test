import asyncio
import pytest
from httpx import AsyncClient

from app.schemas.v1.order import (
    S_OrderFull,
    S_OrderInput,
    S_OrderPagination
)
from app.schemas.v1.order_item import S_OrderItemInput


@pytest.mark.asyncio(loop_scope="session")
async def test_order_list(ac: AsyncClient):
    response = await ac.get("/api/v1/orders")
    assert response.status_code == 200
    r = S_OrderPagination(**response.json())
    assert r.items == []
    assert r.total == 0
    assert r.current_page == 1
    assert r.last_page == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_create_order(ac: AsyncClient):
    from tests.test_routers.test_v1.test_01_products import test_create_product

    await test_create_product(ac, expected_id=2)
    order_data = S_OrderInput(
        items=[
            S_OrderItemInput(
                product_id=2,
                quantity=2
            ),
        ]
    )
    jsn = order_data.model_dump()
    print(f'{jsn=}')

    response = await ac.post("/api/v1/orders", json=jsn)
    assert response.status_code == 201
    r = S_OrderFull(**response.json())
    assert len(r.items) == len(order_data.items)
    assert r.items[0].product.quantity == 8


@pytest.mark.asyncio(loop_scope="session")
async def test_order_statuses(ac: AsyncClient):
    response = await ac.get("/api/v1/orders/statuses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio(loop_scope="session")
async def test_order_info_by_id(ac: AsyncClient):
    response = await ac.get("/api/v1/orders/1")
    assert response.status_code == 200
    r = S_OrderFull(**response.json())
    assert r.id == 1
    assert len(r.items) == 1
    assert r.items[0].product.id == 2
    assert r.items[0].product.quantity == 8
    assert r.items[0].quantity == 2


@pytest.mark.asyncio(loop_scope="session")
async def test_update_order_status(ac: AsyncClient):
    from app.schemas.v1.order import OrderStatus

    response = await ac.patch(
        "/api/v1/orders/1/status?status=SHIPPING"
    )
    assert response.status_code == 200
    r = S_OrderFull(**response.json())
    assert r.id == 1
    assert r.status == OrderStatus.SHIPPING


@pytest.mark.asyncio(loop_scope="session")
async def test_create_order_no_items(ac: AsyncClient):
    order_data = {
        "items": []
    }
    response = await ac.post("/api/v1/orders", json=order_data)
    assert response.status_code == 400
