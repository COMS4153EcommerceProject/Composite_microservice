from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    category_id: UUID = Field(
        default_factory=uuid4,
        description="Unique Category ID (server-generated).",
        json_schema_extra={"example": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11"},
    )
    name: str = Field(
        ...,
        description="Name of the category.",
        example="Computer Accessories",
    )
    description: Optional[str] = Field(
        default=None,
        description="Description of the category.",
        example="All peripheral devices and accessories for computers.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category_id": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11",
                    "name": "Computer Accessories",
                    "description": "All peripheral devices and accessories for computers.",
                }
            ]
        }
    }


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Keyboards & Mice")
    description: Optional[str] = Field(None, example="Input devices for computers.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Monitors", "description": "Display devices for PCs."},
            ]
        }
    }


class CategoryRead(CategoryBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Category creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last category update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category_id": "9c37a7e4-6f6d-49f5-b2ea-34a3b29d9a11",
                    "name": "Computer Accessories",
                    "description": "All peripheral devices and accessories for computers.",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


class CategoryDelete(BaseModel):
    """Placeholder for Category deletion request model."""
    pass
