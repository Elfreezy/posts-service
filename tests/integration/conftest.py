import pytest_asyncio

from contextlib import asynccontextmanager
from redis.asyncio import Redis
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.models.base_model import Base
from app.repositories.post_repository import PostRepository
from app.dependencies import get_post_reposiroty, get_redis_client

from tests.settings import test_settings


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(test_settings.TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine):
    sessionmaker_local = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with sessionmaker_local() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def test_client(test_session) -> AsyncGenerator[AsyncClient, None]:

    async def override_get_repository():
        yield PostRepository(test_session)

    async def override_redis_client():
        redis_client = Redis(
            host=test_settings.TEST_REDIS_HOST, port=test_settings.TEST_REDIS_PORT
        )
        yield redis_client
        await redis_client.aclose()

    app.dependency_overrides[get_post_reposiroty] = override_get_repository
    app.dependency_overrides[get_redis_client] = override_redis_client

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url=test_settings.TEST_CLIENT_BASE_URL
    ) as async_client:
        yield async_client

    app.dependency_overrides = {}


@asynccontextmanager
async def get_redis_instance():
    redis_client = Redis(
        host=test_settings.TEST_REDIS_HOST, port=test_settings.TEST_REDIS_PORT
    )
    yield redis_client
    await redis_client.aclose()
