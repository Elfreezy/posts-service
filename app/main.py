from fastapi import FastAPI

from app.routes.post_routes import post_router
from app.utils.errors_handlers import register_errors_handlers


app = FastAPI()
app.include_router(post_router, prefix="/posts", tags=["posts"])

register_errors_handlers(app)