# src/core/entities/product.py

from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class Product(BaseModel):
    id: Optional[UUID] = None
    owner_id: UUID
    title: str
    description: str
    image_url: Optional[str] = None
    interests: Optional[list[str]] = []

    class Config:
        json_encoders = {
            UUID: lambda v: str(v)
        }
