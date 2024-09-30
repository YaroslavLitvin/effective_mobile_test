import pytest
from httpx import AsyncClient

from app.schemas.v1.product import (
    S_Product,
    S_ProductFull,
    S_ProductPagination
)

TEST_PRODUCT = S_Product(
    name="Test Product",
    description="Test Description",
    price=100,
    quantity=10
)


@pytest.mark.asyncio(loop_scope="session")
async def test_product_list_empty(ac: AsyncClient):
    response = await ac.get("/api/v1/products")
    assert response.status_code == 200
    r = S_ProductPagination(**response.json())
    assert r.items == []
    assert r.total == 0
    assert r.current_page == 1
    assert r.last_page == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(ac: AsyncClient, expected_id: int = 1):
    print(f'test_create_product {ac=}')

    response = await ac.post(
        "/api/v1/products",
        json=TEST_PRODUCT.model_dump()
    )
    assert response.status_code == 201
    product_result = response.json()
    assert product_result['id'] == expected_id
    del product_result['id']
    assert product_result == TEST_PRODUCT.model_dump()


@pytest.mark.asyncio(loop_scope="session")
async def test_product_list_one_item(ac: AsyncClient):
    response = await ac.get("/api/v1/products")
    assert response.status_code == 200
    r = S_ProductPagination(**response.json())
    assert len(r.items) == 1
    assert r.total == 1
    assert r.items[0].id == 1
    assert r.current_page == 1
    assert r.last_page == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_product_info_by_id(ac: AsyncClient):
    response = await ac.get("/api/v1/products/1")
    assert response.status_code == 200
    product_result = response.json()
    assert product_result['id'] == 1
    del product_result['id']
    assert product_result == TEST_PRODUCT.model_dump()


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_info(ac: AsyncClient):
    product_data = {
        "name": "Updated Product",
        "price": 150
    }
    response = await ac.put("/api/v1/products/1", json=product_data)
    assert response.status_code == 200
    product_result = response.json()
    assert product_result['id'] == 1
    assert product_result['name'] == "Updated Product"
    assert product_result['price'] == 150


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_by_id(ac: AsyncClient):
    response = await ac.delete("/api/v1/products/1")
    assert response.status_code == 204


@pytest.mark.asyncio(loop_scope="session")
async def test_product_info_marked_as_deleted(ac: AsyncClient):
    response = await ac.get("/api/v1/orders/1")
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_product_info_not_found(ac: AsyncClient):
    response = await ac.get("/api/v1/products/999")
    assert response.status_code == 404
