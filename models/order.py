from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class OrderBase(BaseModel):
    order_id: UUID = Field(
        default_factory=uuid4,
        description="Unique Order ID (Primary Key).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    user_id: UUID = Field(
        ...,
        description="User ID (Foreign Key to User service).",
        json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"},
    )
    order_date: datetime = Field(
        default_factory=datetime.utcnow,
        description="Date when the order was placed.",
        json_schema_extra={"example": "2025-01-16T10:20:30Z"},
    )
    total_price: float = Field(
        ...,
        ge=0,
        description="Total price of the order in USD.",
        example=1999.98
    )
    status: Optional[str] = Field(
        default="pending",
        description="Order status (pending/shipped/delivered/cancelled).",
        example="pending",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "660e8400-e29b-41d4-a716-446655440001",
                    "order_date": "2025-01-16T10:20:30Z",
                    "total_price": 1999.98,
                    "status": "pending",
                }
            ]
        }
    }


class OrderCreate(BaseModel):
    user_id: UUID = Field(
        ...,
        description="User ID (Foreign Key to User service).",
        json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"},
    )
    total_price: float = Field(
        ...,
        ge=0,
        description="Total price of the order in USD.",
        example=1999.98
    )
    status: Optional[str] = Field(
        default="pending",
        description="Order status (pending/shipped/delivered/cancelled).",
        example="pending",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "660e8400-e29b-41d4-a716-446655440001",
                    "total_price": 1999.98,
                    "status": "pending",
                }
            ]
        }
    }


class OrderUpdate(BaseModel):
    user_id: Optional[UUID] = Field(None, json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"})
    order_date: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-01-16T10:20:30Z"})
    total_price: Optional[float] = Field(None, ge=0, json_schema_extra={"example": 2499.99})
    status: Optional[str] = Field(None, json_schema_extra={"example": "shipped"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "shipped"},
                {"total_price": 2499.99, "status": "delivered"},
            ]
        }
    }

class OrderRead(OrderBase):
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
    links: Dict[str, str] = Field(
        default_factory=dict,
        description="Relative path links to related resources.",
        json_schema_extra={
            "example": {
                "self": "/orders/550e8400-e29b-41d4-a716-446655440000",
                "payments": "/payments?order_id=550e8400-e29b-41d4-a716-446655440000",
                "order_details": "/order-details?order_id=550e8400-e29b-41d4-a716-446655440000"
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "550e8400-e29b-41d4-a716-446655440000",
                    "user_id": "660e8400-e29b-41d4-a716-446655440001",
                    "order_date": "2025-01-16T10:20:30Z",
                    "total_price": 1999.98,
                    "status": "pending",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                    "links": {
                        "self": "/orders/550e8400-e29b-41d4-a716-446655440000",
                        "payments": "/payments?order_id=550e8400-e29b-41d4-a716-446655440000",
                        "order_details": "/order-details?order_id=550e8400-e29b-41d4-a716-446655440000"
                    }
                }
            ]
        }
    }