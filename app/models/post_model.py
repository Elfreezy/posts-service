from sqlalchemy import String, Index
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base_model import BaseModel


class PostModel(BaseModel):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(
        String(120),
    )

    body: Mapped[str] = mapped_column(
        String(500),
    )

    __table_args__ = (
        Index("idx_title", "title"),
    )
