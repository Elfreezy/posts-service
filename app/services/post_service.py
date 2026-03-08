import json
from uuid import UUID
from typing import Union
from redis.asyncio import Redis

from app.models.post_model import PostModel
from app.schemas.post_models import CreatePost, ShowPost, UpdatePost
from app.repositories.post_repository import PostRepository
from app.utils.custom_errors import ItemNotFoundError
from app.settings import settings


class PostService:
    def __init__(self, repository: PostRepository, redis_client: Redis):
        self.repository = repository
        self.redis_client = redis_client

    async def create_post(
        self,
        post: CreatePost,
    ) -> Union[ShowPost, None]:
        post_model = PostModel(
            title=post.title,
            body=post.body,
        )

        response = await self.repository.create_post(post_model)
        return ShowPost.model_validate(response)

    async def update_post(
        self,
        post_id: UUID,
        post: UpdatePost,
    ) -> Union[ShowPost, None]:
        params = post.model_dump(exclude_none=True)
        response = await self.repository.update_post(post_id, **params)

        if not response:
            raise ItemNotFoundError(name=post_id)

        await self.delete_post_from_cache(post_id)
        return ShowPost.model_validate(response)

    async def get_post_all(
        self,
    ) -> list[PostModel]:
        return await self.repository.get_post_all()

    async def get_post_by_id(
        self,
        post_id: UUID,
    ) -> Union[ShowPost, None]:
        cached_post = await self.get_post_from_cache(post_id)

        if cached_post:
            post = ShowPost(**cached_post)
            return post

        db_post = await self.repository.find_post_by_id(post_id)

        if not db_post:
            raise ItemNotFoundError(name=post_id)

        await self.save_post_to_cache(db_post)
        return ShowPost.model_validate(db_post)

    async def delete_post(
        self,
        post_id: UUID,
    ) -> None:
        await self.repository.delete_post(post_id)
        await self.delete_post_from_cache(post_id)

    async def get_post_from_cache(
        self,
        post_id: UUID,
    ):
        cache_key = f"post:{post_id}"
        cached = await self.redis_client.get(cache_key)

        if cached:
            return json.loads(cached)
        return None

    async def delete_post_from_cache(
        self,
        post_id: UUID,
    ):
        cache_key = f"post:{post_id}"
        await self.redis_client.delete(cache_key)

    async def save_post_to_cache(
        self,
        post: PostModel,
    ):
        cache_key = f"post:{post.id}"
        post_dict = ShowPost.model_validate(post).model_dump(mode="json")
        await self.redis_client.setex(
            cache_key, settings.CACHE_TTL, json.dumps(post_dict)
        )
