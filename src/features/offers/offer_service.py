# src/features/offers/offer_service.py

from src.infrastructure.repositories.mongo_offer_repository import MongoOfferRepository
from src.core.entities.offer import Offer
from src.infrastructure.database import offers_collection
from uuid import UUID

offer_repository = MongoOfferRepository(offers_collection)


def create_offer(offer: Offer) -> Offer:
    """
    Creates a new offer.

    Args:
        offer (Offer): The offer to be created.

    Returns:
        Offer: The created offer.
    """
    return offer_repository.create_offer(offer)


def get_offer_by_id(offer_id: UUID) -> Offer:
    """
    Retrieves an offer by its ID.

    Args:
        offer_id (UUID): The ID of the offer.

    Returns:
        Offer: The retrieved offer.
    """
    return offer_repository.get_offer_by_id(offer_id)


def update_offer(offer: Offer) -> Offer:
    """
    Updates an existing offer.

    Args:
        offer (Offer): The offer to be updated.

    Returns:
        Offer: The updated offer.
    """
    return offer_repository.update_offer(offer)


def delete_offer(offer_id: UUID):
    """
    Deletes an offer by its ID.

    Args:
        offer_id (UUID): The ID of the offer.
    """
    return offer_repository.delete_offer(offer_id)


def update_offer_status(offer_id: UUID, status: str) -> Offer:
    """
    Updates the status of an offer.

    Args:
        offer_id (UUID): The ID of the offer.
        status (str): The new status of the offer.

    Returns:
        Offer: The updated offer.
    """
    return offer_repository.update_offer_status(offer_id, status)
