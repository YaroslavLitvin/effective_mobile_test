import logging
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query

from app.dependencies.v1.database import D_DbRepo
from app.dependencies.v1.pagination import D_PaginationParams
from app.schemas.v1.product import (
    S_Product,
    S_ProductFull,
    S_ProductOptional,
    S_ProductPagination
)


router = APIRouter(
    prefix='/products',
    tags=['V1/Products']
)
log = logging.getLogger(__name__)


@router.get("",
            response_model=S_ProductPagination,
            )
async def product_list(
    db_repo: D_DbRepo,
    pagination: D_PaginationParams = Query(...),
    is_deleted: Optional[bool] = None,
):
    (
        product_list, current_page,
        total_pages, total_count
    ) = await db_repo.products.items(
        page=pagination.page,
        items_on_page=pagination.items_on_page,
        is_deleted=is_deleted
    )
    return S_ProductPagination(
        items=[item.to_schema() for item in product_list],
        current_page=current_page,
        last_page=total_pages,
        total=total_count
    )


@router.post("",
             response_model=S_ProductFull
             )
async def create_product(
    new_product: S_Product,
    db_repo: D_DbRepo
):
    result = await db_repo.products.create(
        name=new_product.name,
        description=new_product.description,
        price=new_product.price,
        quantity=new_product.quantity,
    )
    return result.to_schema()


@router.get("/{id}",
            response_model=S_ProductFull
            )
async def product_info_by_id(
    id: int,
    db_repo: D_DbRepo
):
    product = await db_repo.products.read(id)
    if product is None:
        raise HTTPException(
            404,
            f"Entry with id={id} not found."
        )
    return product.to_schema()


@router.put("/{id}",
            response_model=S_ProductFull
            )
async def update_product_info(
    id: int,
    db_repo: D_DbRepo,
    new_product_info: S_ProductOptional = Body(...),
):
    try:
        result = await db_repo.products.update(
            id=id,
            **(new_product_info.model_dump())
        )
    except ValueError:
        raise HTTPException(
            404,
            f"Entry with id={id} not exist."
        )
    except Exception:
        raise

    return result.to_schema()


@router.delete("/{id}")
async def delete_product_by_id(
    id: int,
    db_repo: D_DbRepo
):
    try:
        await db_repo.products.update(id=id, is_deleted=True)
    except ValueError:
        raise HTTPException(
            404,
            f"Entry with id={id} not exist."
        )
