from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class PaymentBase(BaseModel):
    payment_id: UUID = Field(
        default_factory=uuid4,
        description="Unique payment transaction ID (Primary Key).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    order_id: UUID = Field(
        ...,
        description="Order ID (Primary Key and Foreign Key to Order).",
        json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"},
    )
    payment_method: str = Field(
        ...,
        description="Payment method used (e.g., credit_card, paypal, bank_transfer).",
        example="credit_card"
    )
    payment_date: datetime = Field(
        ...,
        description="Date and time when payment was made.",
        example="2025-01-16T10:30:00Z"
    )
    amount: float = Field(
        ...,
        ge=0,
        description="Payment amount.",
        example=199.99
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "660e8400-e29b-41d4-a716-446655440001",
                    "payment_method": "credit_card",
                    "payment_date": "2025-01-16T10:30:00Z",
                    "amount": 199.99,
                }
            ]
        }
    }

class PaymentCreate(BaseModel):
    order_id: UUID = Field(
        ...,
        description="Order ID (Foreign Key to Order).",
        json_schema_extra={"example": "660e8400-e29b-41d4-a716-446655440001"},
    )
    payment_method: str = Field(
        ...,
        description="Payment method used (e.g., credit_card, paypal, bank_transfer).",
        example="credit_card"
    )
    payment_date: datetime = Field(
        ...,
        description="Date and time when payment was made.",
        example="2025-01-16T10:30:00Z"
    )
    amount: float = Field(
        ...,
        ge=0,
        description="Payment amount.",
        example=199.99
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "order_id": "660e8400-e29b-41d4-a716-446655440001",
                    "payment_method": "credit_card",
                    "payment_date": "2025-01-16T10:30:00Z",
                    "amount": 199.99,
                }
            ]
        }
    }

class PaymentUpdate(BaseModel):
    payment_method: Optional[str] = Field(None, json_schema_extra={"example": "paypal"})
    payment_date: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-01-16T11:00:00Z"})
    amount: Optional[float] = Field(None, ge=0, json_schema_extra={"example": 249.99})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"payment_method": "paypal"},
                {"amount": 249.99},
                {
                    "payment_method": "bank_transfer",
                    "payment_date": "2025-01-16T11:00:00Z",
                    "amount": 249.99,
                }
            ]
        }
    }

class PaymentRead(PaymentBase):
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
                "self": "/payments/550e8400-e29b-41d4-a716-446655440000",
                "order": "/orders/660e8400-e29b-41d4-a716-446655440001"
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "payment_id": "550e8400-e29b-41d4-a716-446655440000",
                    "order_id": "660e8400-e29b-41d4-a716-446655440001",
                    "payment_method": "credit_card",
                    "payment_date": "2025-01-16T10:30:00Z",
                    "amount": 199.99,
                    "created_at": "2025-01-16T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                    "links": {
                        "self": "/payments/550e8400-e29b-41d4-a716-446655440000",
                        "order": "/orders/660e8400-e29b-41d4-a716-446655440001"
                    }
                }
            ]
        }
    }