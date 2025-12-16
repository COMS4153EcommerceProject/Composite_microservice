from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, Field


class UserAddressBase(BaseModel):
    user_id: UUID = Field(
        ...,
        description="Associated user's unique identifier (foreign key).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    addr_id: UUID = Field(
        ...,
        description="Associated address's unique identifier (foreign key).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "addr_id": "660e8400-e29b-41d4-a716-446655440000",
                }
            ]
        }
    }


class UserAddressCreate(UserAddressBase):
    """Creation payload for associating a user with an address."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "addr_id": "660e8400-e29b-41d4-a716-446655440000",
                }
            ]
        }
    }


class UserAddressRead(UserAddressBase):
    """Read model for user-address association."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "addr_id": "660e8400-e29b-41d4-a716-446655440000",
                }
            ]
        }
    }
