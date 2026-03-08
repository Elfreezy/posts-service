from fastapi import FastAPI
from contextlib import asynccontextmanager
from alembic import command
from alembic.config import Config

from app.routes.post_routes import post_router
from app.utils.errors_handlers import register_errors_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_cfg = Config("app/alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(post_router, prefix="/posts", tags=["posts"])

register_errors_handlers(app)
