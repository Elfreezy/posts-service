from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import sessionmaker_local
from app.repositories.post_repository import PostRepository
from app.services.post_service import PostService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker_local() as session:
        yield session

async def get_post_reposiroty(session: AsyncSession = Depends(get_session)) -> PostRepository:
    return PostRepository(session)

async def get_post_service(repository: PostRepository = Depends(get_post_reposiroty)) -> PostService:
    return PostService(repository)
