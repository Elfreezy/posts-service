from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Annotated

from app.services.post_service import PostService
from app.schemas.post_models import CreatePost, ShowPost, UpdatePost
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

@post_router.get("/{post_id}/")
async def get_post_by_id(
    post_id: UUID,
    service: Annotated[PostService, Depends(get_post_service)]
):
    return await service.get_post_by_id(post_id)

@post_router.put("/update/{post_id}/")
async def update_post(
    post_id: UUID,
    post: UpdatePost,
    service: Annotated[PostService, Depends(get_post_service)]
):
    return await service.update_post(post_id, post)

@post_router.delete("/delete/{post_id}/")
async def delete_post(
    post_id: UUID,
    service: Annotated[PostService, Depends(get_post_service)]
):
    return await service.delete_post(post_id)