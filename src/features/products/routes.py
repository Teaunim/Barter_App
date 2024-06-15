# src/features/products/routes.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from src.core.entities.product import Product
from src.features.products.product_service import create_product, get_product_by_id, update_product, delete_product, \
    get_products_by_owner_id

products_router = APIRouter()


class ProductCreateRequest(BaseModel):
    owner_id: UUID
    title: str
    description: str
    image_url: Optional[str] = None
    interests: Optional[List[str]] = []


class ProductUpdateRequest(BaseModel):
    id: UUID
    owner_id: UUID
    title: str
    description: str
    image_url: Optional[str] = None
    interests: Optional[List[str]] = []


@products_router.post("/", response_model=Product)
def create_product_endpoint(product_request: ProductCreateRequest):
    """
    Endpoint to create a new product.

    Args:
        product_request (ProductCreateRequest): Request body containing product details.

    Returns:
        Product: The created product.
    """
    product = Product(**product_request.dict())
    return create_product(product)


@products_router.get("/{product_id}", response_model=Product)
def get_product_endpoint(product_id: UUID):
    """
    Endpoint to get a product by its ID.

    Args:
        product_id (UUID): The ID of the product.

    Returns:
        Product: The retrieved product.
    """
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@products_router.put("/", response_model=Product)
def update_product_endpoint(product_request: ProductUpdateRequest):
    """
    Endpoint to update an existing product.

    Args:
        product_request (ProductUpdateRequest): Request body containing updated product details.

    Returns:
        Product: The updated product.
    """
    product = Product(**product_request.dict())
    return update_product(product)


@products_router.delete("/{product_id}")
def delete_product_endpoint(product_id: UUID):
    """
    Endpoint to delete a product by its ID.

    Args:
        product_id (UUID): The ID of the product.

    Returns:
        dict: Message indicating the result of the operation.
    """
    delete_product(product_id)
    return {"message": "Product deleted successfully"}


@products_router.get("/owner/{owner_id}", response_model=List[Product])
def get_products_by_owner_id_endpoint(owner_id: UUID):
    """
    Endpoint to get all products by the owner's ID.

    Args:
        owner_id (UUID): The ID of the owner.

    Returns:
        list[Product]: List of products owned by the user.
    """
    products = get_products_by_owner_id(owner_id)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found for this user")
    return products
