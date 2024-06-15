# src/features/offers/routes.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from src.core.entities.offer import Offer
from src.features.offers.offer_service import create_offer, get_offer_by_id, update_offer, delete_offer, \
    update_offer_status

offers_router = APIRouter()


class OfferCreateRequest(BaseModel):
    product_id: UUID
    from_user_id: UUID
    to_user_id: UUID
    offered_product_id: UUID


class OfferUpdateRequest(BaseModel):
    id: UUID
    product_id: UUID
    from_user_id: UUID
    to_user_id: UUID
    offered_product_id: UUID
    status: Optional[str]


@offers_router.post("/", response_model=Offer)
def create_offer_endpoint(offer_request: OfferCreateRequest):
    """
    Endpoint to create a new offer.

    Args:
        offer_request (OfferCreateRequest): Request body containing offer details.

    Returns:
        Offer: The created offer.
    """
    offer = Offer(**offer_request.dict())
    return create_offer(offer)


@offers_router.get("/{offer_id}", response_model=Offer)
def get_offer_endpoint(offer_id: UUID):
    """
    Endpoint to get an offer by its ID.

    Args:
        offer_id (UUID): The ID of the offer.

    Returns:
        Offer: The retrieved offer.
    """
    offer = get_offer_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    return offer


@offers_router.put("/", response_model=Offer)
def update_offer_endpoint(offer_request: OfferUpdateRequest):
    """
    Endpoint to update an existing offer.

    Args:
        offer_request (OfferUpdateRequest): Request body containing updated offer details.

    Returns:
        Offer: The updated offer.
    """
    offer = Offer(**offer_request.dict())
    return update_offer(offer)


@offers_router.delete("/{offer_id}")
def delete_offer_endpoint(offer_id: UUID):
    """
    Endpoint to delete an offer by its ID.

    Args:
        offer_id (UUID): The ID of the offer.

    Returns:
        dict: Message indicating the result of the operation.
    """
    delete_offer(offer_id)
    return {"message": "Offer deleted successfully"}


@offers_router.patch("/{offer_id}/accept", response_model=Offer)
def accept_offer_endpoint(offer_id: UUID):
    """
    Endpoint to accept an offer by its ID.

    Args:
        offer_id (UUID): The ID of the offer.

    Returns:
        Offer: The updated offer with accepted status.
    """
    offer = update_offer_status(offer_id, "accepted")
    return offer


@offers_router.patch("/{offer_id}/reject", response_model=Offer)
def reject_offer_endpoint(offer_id: UUID):
    """
    Endpoint to reject an offer by its ID.

    Args:
        offer_id (UUID): The ID of the offer.

    Returns:
        Offer: The updated offer with rejected status.
    """
    offer = update_offer_status(offer_id, "rejected")
    return offer
