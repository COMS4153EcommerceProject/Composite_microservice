from __future__ import annotations
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field


class PreferenceBase(BaseModel):
    language: Optional[str] = Field(
        None,
        description="Preferred language code (ISO 639-1).",
        json_schema_extra={"example": "en"},
    )
    currency: Optional[str] = Field(
        None,
        description="Preferred currency code (ISO 4217).",
        json_schema_extra={"example": "USD"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"language": "en", "currency": "USD"},
                {"language": "zh", "currency": "CNY"},
            ]
        }
    }


class PreferenceCreate(PreferenceBase):
    """Creation payload for user preferences."""
    user_id: UUID = Field(
        ...,
        description="Associated user's unique identifier (foreign key).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "language": "en",
                    "currency": "USD",
                }
            ]
        }
    }


class PreferenceUpdate(BaseModel):
    """Update payload for user preferences; all fields optional."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"language": "es"},
                {"currency": "EUR"}
            ]
        }
    }


class PreferenceRead(PreferenceBase):
    user_id: UUID = Field(
        ...,
        description="Associated user's unique identifier (foreign key).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000", 
                    "language": "en", 
                    "currency": "USD",
                }
            ]
        }
    }