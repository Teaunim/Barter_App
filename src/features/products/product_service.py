# src/features/products/product_service.py

from src.infrastructure.repositories.mongo_product_repository import MongoProductRepository
from src.core.entities.product import Product
from src.infrastructure.database import products_collection
from uuid import UUID

product_repository = MongoProductRepository(products_collection)


def create_product(product: Product) -> Product:
    """
    Creates a new product.

    Args:
        product (Product): The product to be created.

    Returns:
        Product: The created product.
    """
    return product_repository.create_product(product)


def get_product_by_id(product_id: UUID) -> Product:
    """
    Retrieves a product by its ID.

    Args:
        product_id (UUID): The ID of the product.

    Returns:
        Product: The retrieved product.
    """
    return product_repository.get_product_by_id(product_id)


def update_product(product: Product) -> Product:
    """
    Updates an existing product.

    Args:
        product (Product): The product to be updated.

    Returns:
        Product: The updated product.
    """
    return product_repository.update_product(product)


def delete_product(product_id: UUID):
    """
    Deletes a product by its ID.

    Args:
        product_id (UUID): The ID of the product.
    """
    return product_repository.delete_product(product_id)


def get_products_by_owner_id(owner_id: UUID) -> list[Product]:
    """
    Retrieves all products by the owner's ID.

    Args:
        owner_id (UUID): The ID of the owner.

    Returns:
        list[Product]: List of products owned by the user.
    """
    return product_repository.get_products_by_owner_id(owner_id)
