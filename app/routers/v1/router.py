from fastapi import APIRouter

from app.routers.v1.product import router as products_router
from app.routers.v1.order import router as orders_router


router = APIRouter(
    prefix='/v1'
)


router_list = [
    products_router,
    orders_router
]


for r in router_list:
    router.include_router(r)
