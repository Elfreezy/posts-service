from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Annotated, List

from app.services.post_service import PostService
from app.models.post_model import PostModel
from app.schemas.post_models import CreatePost, ShowPost, DeletePost, UpdatePost
from app.dependencies import get_post_service

post_router = APIRouter()


@post_router.post("/create/")
async def create_post(
    post: CreatePost,
    service: Annotated[PostService, Depends(get_post_service)]
) -> ShowPost:
    return await service.create_post(post)

@post_router.get("/all/")
async def get_post_all(
    service: Annotated[PostService, Depends(get_post_service)]
):
    return await service.get_post_all()

@post_router.post("/update/")
async def delete_post(
    post_id: UUID,
    post: UpdatePost,
    service: Annotated[PostService, Depends(get_post_service)]
):
    return await service.update_post(post_id, post)

@post_router.delete("/delete/")
async def delete_post(
    post: DeletePost,
    service: Annotated[PostService, Depends(get_post_service)]
):
    return await service.delete_post(post)