from uuid import UUID
from typing import Union, Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post_model import PostModel
from app.utils.custom_errors import ItemNotFoundError

class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(
        self,
        post: PostModel,
    ) -> PostModel:
        self.session.add(post)
        await self.session.commit()
        return post
    
    async def find_post_by_id(
        self,
        post_id: UUID,
    ) -> Union[PostModel, None]:
        statement = (
            select(PostModel)
            .filter(PostModel.id == post_id)
        )

        db_response = await self.session.scalars(statement)
        post = db_response.one_or_none()
        return post
    
    async def get_post_all(
        self,
    ) -> Union[Sequence[PostModel], None]:
        statement = select(PostModel)
        db_result = await self.session.scalars(statement)
        posts = db_result.all()
        return posts
    
    
    async def update_post(
        self,
        post_id: UUID,
        **kwargs,
    ) -> Union[PostModel, None]:
        statement = (
            update(PostModel)
            .filter(PostModel.id == post_id)
            .values(kwargs)
            .returning(PostModel)
        )

        db_result = await self.session.scalars(statement)
        post = db_result.one_or_none()
        await self.session.commit()
        return post

    async def delete_post(
        self,
        post_id: UUID,
    ) -> None:
        post = await self.find_post_by_id(post_id)

        if not post:
            raise ItemNotFoundError(name=post_id)
        
        await self.session.delete(post)
        await self.session.commit()