# src/infrastructure/repositories/mongo_product_repository.py

from pymongo.collection import Collection
from src.core.entities.product import Product
from uuid import UUID, uuid4
from bson import Binary, UuidRepresentation


class MongoProductRepository:
    """Repository for managing products in MongoDB."""

    def __init__(self, collection: Collection):
        """
        Initializes the MongoProductRepository instance.

        Args:
            collection (Collection): MongoDB collection.
        """
        self.collection = collection

    def create_product(self, product: Product) -> Product:
        """
        Creates a new product.

        Args:
            product (Product): The product to be created.

        Returns:
            Product: The created product.
        """
        if product.id is None:
            product.id = uuid4()
        product_dict = product.dict()
        product_dict['id'] = Binary.from_uuid(product.id, uuid_representation=UuidRepresentation.STANDARD)
        product_dict['owner_id'] = Binary.from_uuid(product.owner_id, uuid_representation=UuidRepresentation.STANDARD)
        self.collection.insert_one(product_dict)
        return product

    def get_product_by_id(self, product_id: UUID) -> Product:
        """
        Retrieves a product by its ID.

        Args:
            product_id (UUID): The ID of the product.

        Returns:
            Product: The retrieved product.
        """
        product_dict = self.collection.find_one(
            {"id": Binary.from_uuid(product_id, uuid_representation=UuidRepresentation.STANDARD)})
        if product_dict:
            product_dict['id'] = UUID(bytes=product_dict['id'])
            product_dict['owner_id'] = UUID(bytes=product_dict['owner_id'])
            return Product(**product_dict)
        return None

    def update_product(self, product: Product) -> Product:
        """
        Updates an existing product.

        Args:
            product (Product): The product to be updated.

        Returns:
            Product: The updated product.
        """
        product_dict = product.dict()
        product_dict['id'] = Binary.from_uuid(product.id, uuid_representation=UuidRepresentation.STANDARD)
        product_dict['owner_id'] = Binary.from_uuid(product.owner_id, uuid_representation=UuidRepresentation.STANDARD)
        result = self.collection.update_one({"id": product_dict['id']}, {"$set": product_dict})
        if result.modified_count == 0:
            raise ValueError("Product update failed")
        return product

    def delete_product(self, product_id: UUID):
        """
        Deletes a product by its ID.

        Args:
            product_id (UUID): The ID of the product.

        Raises:
            ValueError: If the product deletion fails.
        """
        result = self.collection.delete_one(
            {"id": Binary.from_uuid(product_id, uuid_representation=UuidRepresentation.STANDARD)})
        if result.deleted_count == 0:
            raise ValueError("Product deletion failed")

    def get_products_by_owner_id(self, owner_id: UUID) -> list[Product]:
        """
        Retrieves all products by the owner's ID.

        Args:
            owner_id (UUID): The ID of the owner.

        Returns:
            list[Product]: List of products owned by the user.
        """
        cursor = self.collection.find(
            {"owner_id": Binary.from_uuid(owner_id, uuid_representation=UuidRepresentation.STANDARD)})
        products = []
        for product_dict in cursor:
            product_dict['id'] = UUID(bytes=product_dict['id'])
            product_dict['owner_id'] = UUID(bytes=product_dict['owner_id'])
            products.append(Product(**product_dict))
        return products
