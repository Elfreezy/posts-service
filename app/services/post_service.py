from uuid import UUID
from typing import Union

from app.models.post_model import PostModel
from app.schemas.post_models import CreatePost, ShowPost, DeletePost, UpdatePost
from app.repositories.post_repository import PostRepository

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository
    
    async def create_post(
        self,
        post: CreatePost,
    ) -> Union[ShowPost, None]:
        post_model = PostModel(
            title = post.title,
            body = post.body,
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
        return ShowPost.model_validate(response)

    async def get_post_all(
        self,
    ) -> list[PostModel]:
        return await self.repository.get_post_all()
    
    async def delete_post(
        self,
        post: DeletePost,
    ) -> None:
        await self.repository.delete_post(post.id)