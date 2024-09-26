from typing import Annotated
from fastapi import Depends
from app.configuration import config
from app.database.repos.requests import RequestsRepo
from app.database.repos.setup import (
    create_engine,
    create_session_pool
)


async_engine = create_engine(config)
async_session_pool = create_session_pool(async_engine)


async def get_async_repo():
    async with async_session_pool() as session:
        yield RequestsRepo(session)


D_DbRepo = Annotated[RequestsRepo, Depends(get_async_repo)]
