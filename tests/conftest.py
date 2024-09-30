import pytest

from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient


from app.main import app
from app.database.repos.setup import create_engine
from app.configuration import config
from app.database.models.base import Base


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    engine_test = create_engine(config)
    # Создание всех таблиц в БД
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # ПАередача управления на выполнение тестов
    yield
    # Удаление всех таблиц в БД
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
