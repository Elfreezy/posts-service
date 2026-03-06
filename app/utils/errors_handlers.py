from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError
from loguru import logger

from app.utils.custom_errors import ItemNotFoundError

def register_errors_handlers(app: FastAPI):

    @app.exception_handler(ItemNotFoundError)
    async def item_not_found_exception_handler(
        request: Request, 
        exc: ItemNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": f"Object \"{exc.name}\" not found",
            },
        )
    
    @app.exception_handler(DatabaseError)
    async def database_exceprion_handler(
        request: Request, 
        exc: DatabaseError
    ) -> JSONResponse:
        logger.error(f"Unexpected DB error: {exc}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Database error",
            },
        )