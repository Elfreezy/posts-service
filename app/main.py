from fastapi import FastAPI

from app.routes.post_routes import post_router


app = FastAPI()
app.include_router(post_router, prefix="/posts", tags=["posts"])