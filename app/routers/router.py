from fastapi import APIRouter

from app.routers.v1.router import router as v1_router

router = APIRouter(
    prefix='/api'
)

router_list = [
    v1_router,
    # v2_router,
]


for r in router_list:
    router.include_router(r)
