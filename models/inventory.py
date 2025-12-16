from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class InventoryBase(BaseModel):
    inventory_id: UUID = Field(
        default_factory=uuid4,
        description="Unique Inventory ID (server-generated).",
        json_schema_extra={"example": "b6f63b25-15d8-4e12-8c6e-8a87a1254e22"},
    )
    product_id: UUID = Field(
        ...,
        description="Foreign key reference to the associated product.",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    stock_quantity: int = Field(
        ...,
        ge=0,
        description="Number of product units available in stock.",
        example=320,
    )
    warehouse_location: Optional[str] = Field(
        default=None,
        description="Physical location or warehouse where product is stored.",
        example="Warehouse A - Section B3",
    )
    update_time: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of the last inventory update (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "inventory_id": "b6f63b25-15d8-4e12-8c6e-8a87a1254e22",
                    "product_id": "123e4567-e89b-12d3-a456-426614174000",
                    "stock_quantity": 320,
                    "warehouse_location": "Warehouse A - Section B3",
                    "update_time": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    stock_quantity: Optional[int] = Field(None, ge=0, example=250)
    warehouse_location: Optional[str] = Field(None, example="Warehouse B - Shelf 4")
    update_time: Optional[datetime] = Field(
        None,
        description="Update timestamp for inventory change.",
        json_schema_extra={"example": "2025-02-01T09:30:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"stock_quantity": 250, "warehouse_location": "Warehouse B - Shelf 4"},
                {"stock_quantity": 180},
            ]
        }
    }


class InventoryRead(InventoryBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp of inventory record (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "inventory_id": "b6f63b25-15d8-4e12-8c6e-8a87a1254e22",
                    "product_id": "123e4567-e89b-12d3-a456-426614174000",
                    "stock_quantity": 320,
                    "warehouse_location": "Warehouse A - Section B3",
                    "update_time": "2025-01-16T12:00:00Z",
                    "created_at": "2025-01-15T10:20:30Z",
                }
            ]
        }
    }


class InventoryDelete(BaseModel):
    """Placeholder for Inventory deletion request model."""
    pass
