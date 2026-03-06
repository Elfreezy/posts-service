from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TunnelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CreatePost(TunnelModel):
    title: str
    body: str

class ShowPost(TunnelModel):
    id: UUID
    title: str
    body: str
    created_at: datetime
    updated_at: datetime

class DeletePost(TunnelModel):
    id: UUID

class UpdatePost(TunnelModel):
    title: Optional[str] = None
    body: Optional[str] = None

