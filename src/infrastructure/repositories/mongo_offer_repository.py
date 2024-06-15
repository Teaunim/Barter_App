# src/infrastructure/repositories/mongo_offer_repository.py

from pymongo.collection import Collection
from src.core.entities.offer import Offer
from uuid import UUID, uuid4
from bson import Binary, UuidRepresentation


class MongoOfferRepository:
    """Repository for managing offers in MongoDB."""

    def __init__(self, collection: Collection):
        """
        Initializes the MongoOfferRepository instance.

        Args:
            collection (Collection): MongoDB collection.
        """
        self.collection = collection

    def create_offer(self, offer: Offer) -> Offer:
        """
        Creates a new offer.

        Args:
            offer (Offer): The offer to be created.

        Returns:
            Offer: The created offer.
        """
        if offer.id is None:
            offer.id = uuid4()
        offer_dict = offer.dict()
        offer_dict['id'] = Binary.from_uuid(offer.id, uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['product_id'] = Binary.from_uuid(offer.product_id, uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['from_user_id'] = Binary.from_uuid(offer.from_user_id,
                                                      uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['to_user_id'] = Binary.from_uuid(offer.to_user_id, uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['offered_product_id'] = Binary.from_uuid(offer.offered_product_id,
                                                            uuid_representation=UuidRepresentation.STANDARD)
        self.collection.insert_one(offer_dict)
        return offer

    def get_offer_by_id(self, offer_id: UUID) -> Offer:
        """
        Retrieves an offer by its ID.

        Args:
            offer_id (UUID): The ID of the offer.

        Returns:
            Offer: The retrieved offer.
        """
        offer_dict = self.collection.find_one(
            {"id": Binary.from_uuid(offer_id, uuid_representation=UuidRepresentation.STANDARD)})
        if offer_dict:
            offer_dict['id'] = UUID(bytes=offer_dict['id'])
            offer_dict['product_id'] = UUID(bytes=offer_dict['product_id'])
            offer_dict['from_user_id'] = UUID(bytes=offer_dict['from_user_id'])
            offer_dict['to_user_id'] = UUID(bytes=offer_dict['to_user_id'])
            offer_dict['offered_product_id'] = UUID(bytes=offer_dict['offered_product_id'])
            return Offer(**offer_dict)
        return None

    def update_offer(self, offer: Offer) -> Offer:
        """
        Updates an existing offer.

        Args:
            offer (Offer): The offer to be updated.

        Returns:
            Offer: The updated offer.
        """
        offer_dict = offer.dict()
        offer_dict['id'] = Binary.from_uuid(offer.id, uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['product_id'] = Binary.from_uuid(offer.product_id, uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['from_user_id'] = Binary.from_uuid(offer.from_user_id,
                                                      uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['to_user_id'] = Binary.from_uuid(offer.to_user_id, uuid_representation=UuidRepresentation.STANDARD)
        offer_dict['offered_product_id'] = Binary.from_uuid(offer.offered_product_id,
                                                            uuid_representation=UuidRepresentation.STANDARD)
        result = self.collection.update_one({"id": offer_dict['id']}, {"$set": offer_dict})
        if result.modified_count == 0:
            raise ValueError("Offer update failed")
        return offer

    def delete_offer(self, offer_id: UUID):
        """
        Deletes an offer by its ID.

        Args:
            offer_id (UUID): The ID of the offer.

        Raises:
            ValueError: If the offer deletion fails.
        """
        result = self.collection.delete_one(
            {"id": Binary.from_uuid(offer_id, uuid_representation=UuidRepresentation.STANDARD)})
        if result.deleted_count == 0:
            raise ValueError("Offer deletion failed")

    def update_offer_status(self, offer_id: UUID, status: str) -> Offer:
        """
        Updates the status of an offer.

        Args:
            offer_id (UUID): The ID of the offer.
            status (str): The new status of the offer.

        Returns:
            Offer: The updated offer.
        """
        result = self.collection.update_one(
            {"id": Binary.from_uuid(offer_id, uuid_representation=UuidRepresentation.STANDARD)},
            {"$set": {"status": status}}
        )
        if result.modified_count == 0:
            raise ValueError("Offer status update failed")
        return self.get_offer_by_id(offer_id)
