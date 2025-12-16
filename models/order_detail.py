from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class OrderDetailBase(BaseModel):
    order_id: UUID = Field(
        ...,
        description="Order ID (Primary Key and Foreign Key to Order).",
        json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"},
    )
    prod_id: UUID = Field(
        ...,
        description="Product ID (Primary Key and Foreign Key to Product service).",
        json_schema_extra={"example": "770e8400-e29b-41d4-a716-446655440002"},
    )
    quantity: int = Field(
        ...,
        ge=1,
        description="Quantity of the product in this order detail.",
        example=2
    )
    subtotal: float = Field(
        ...,
        ge=0,
        description="Subtotal for this line item (quantity * unit price).",
        example=199.98
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "660e8400-e29b-41d4-a716-446655440001",
                    "prod_id": "770e8400-e29b-41d4-a716-446655440002",
                    "quantity": 2,
                    "subtotal": 199.98,
                }
            ]
        }
    }

class OrderDetailCreate(BaseModel):
    order_id: UUID = Field(
        ...,
        description="Order ID (Foreign Key to Order).",
        json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"},
    )
    prod_id: UUID = Field(
        ...,
        description="Product ID (Foreign Key to Product service).",
        json_schema_extra={"example": "770e8400-e29b-41d4-a716-446655440002"},
    )
    quantity: int = Field(
        ...,
        ge=1,
        description="Quantity of the product in this order detail.",
        example=2
    )
    subtotal: float = Field(
        ...,
        ge=0,
        description="Subtotal for this line item (quantity * unit price).",
        example=199.98
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "660e8400-e29b-41d4-a716-446655440001",
                    "prod_id": "770e8400-e29b-41d4-a716-446655440002",
                    "quantity": 2,
                    "subtotal": 199.98,
                }
            ]
        }
    }

class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1, json_schema_extra={"example": 3})
    subtotal: Optional[float] = Field(None, ge=0, json_schema_extra={"example": 299.97})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"quantity": 3},
                {"subtotal": 299.97},
                {
                    "quantity": 5,
                    "subtotal": 499.95,
                }
            ]
        }
    }

class OrderDetailRead(OrderDetailBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )
    links: Dict[str, str] = Field(
        default_factory=dict,
        description="Relative path links to related resources.",
        json_schema_extra={
            "example": {
                "self": "/order-details/660e8400-e29b-41d4-a716-446655440001/770e8400-e29b-41d4-a716-446655440002",
                "order": "/orders/660e8400-e29b-41d4-a716-446655440001"
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "660e8400-e29b-41d4-a716-446655440001",
                    "prod_id": "770e8400-e29b-41d4-a716-446655440002",
                    "quantity": 2,
                    "subtotal": 199.98,
                    "created_at": "2025-01-16T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                    "links": {
                        "self": "/order-details/660e8400-e29b-41d4-a716-446655440001/770e8400-e29b-41d4-a716-446655440002",
                        "order": "/orders/660e8400-e29b-41d4-a716-446655440001"
                    }
                }
            ]
        }
    }