from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    product_id: UUID = Field(
        default_factory=uuid4,
        description="Unique Product ID (server-generated).",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    name: str = Field(
        ...,
        description="Name of the product.",
        example="Wireless Mouse",
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed product description.",
        example="Ergonomic wireless mouse with 2.4GHz connectivity.",
    )
    price: float = Field(
        ...,
        ge=0,
        description="Product price in USD.",
        example=29.99,
    )
    rating: Optional[float] = Field(
        default=None,
        ge=0,
        le=5,
        description="Average user rating (0-5 scale).",
        example=4.5,
    )
    category_id: Optional[UUID] = Field(
        default=None,
        description="Foreign key reference to the product category.",
        json_schema_extra={"example": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11"},
    )
    inventory_id: Optional[UUID] = Field(
        default=None,
        description="Foreign key reference to the product inventory.",
        json_schema_extra={"example": "b6f63b25-15d8-4e12-8c6e-8a87a1254e22"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Logitech MX Master 3 Mouse",
                    "description": "Advanced wireless mouse with ergonomic design.",
                    "price": 99.99,
                    "rating": 4.8,
                    "category_id": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11",
                    "inventory_id": "b6f63b25-15d8-4e12-8c6e-8a87a1254e22",
                }
            ]
        }
    }


class ProductCreate(BaseModel):
    name: str = Field(..., example="Wireless Mouse")
    description: Optional[str] = Field(None, example="Ergonomic wireless mouse")
    price: float = Field(..., ge=0, example=29.99)
    rating: Optional[float] = Field(None, ge=0, le=5, example=4.5)
    category_id: Optional[UUID] = Field(None, example="9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11")
    inventory_id: Optional[UUID] = Field(None, example="b6f63b25-15d8-4e12-8c6e-8a87a1254e22")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Mechanical Keyboard")
    description: Optional[str] = Field(None, example="RGB backlit, blue switches.")
    price: Optional[float] = Field(None, example=79.99)
    rating: Optional[float] = Field(None, example=4.7)
    category_id: Optional[UUID] = Field(
        None, example="9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11"
    )
    inventory_id: Optional[UUID] = Field(
        None, example="b6f63b25-15d8-4e12-8c6e-8a87a1254e22"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"price": 89.99, "rating": 4.9},
                {"name": "Gaming Mouse", "category_id": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11"},
            ]
        }
    }


class ProductRead(ProductBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "product_id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Logitech MX Master 3 Mouse",
                    "description": "Advanced wireless mouse with ergonomic design.",
                    "price": 99.99,
                    "rating": 4.8,
                    "category_id": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11",
                    "inventory_id": "b6f63b25-15d8-4e12-8c6e-8a87a1254e22",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


class ProductDelete(BaseModel):
    """Placeholder for Product deletion request model."""
    pass
