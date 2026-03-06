import uuid

from datetime import datetime
from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

