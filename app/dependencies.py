from fastapi import Depends
from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.database import sessionmaker_local
from app.repositories.post_repository import PostRepository
from app.services.post_service import PostService
from app.settings import settings


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker_local() as session:
        yield session


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    yield redis_client
    await redis_client.aclose()


async def get_post_reposiroty(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PostRepository:
    return PostRepository(session)


async def get_post_service(
    repository: Annotated[PostRepository, Depends(get_post_reposiroty)],
    redis_client: Annotated[Redis, Depends(get_redis_client)],
) -> PostService:
    return PostService(repository, redis_client)
