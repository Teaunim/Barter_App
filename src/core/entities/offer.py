# src/core/entities/offer.py

from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class Offer(BaseModel):
    id: Optional[UUID] = None
    product_id: UUID
    from_user_id: UUID
    to_user_id: UUID
    offered_product_id: UUID  # Product being offered in the trade
    status: Optional[str] = "pending"  # Possible statuses: pending, accepted, rejected

    class Config:
        json_encoders = {
            UUID: lambda v: str(v)
        }
