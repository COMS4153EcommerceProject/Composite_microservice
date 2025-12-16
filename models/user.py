from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example": "Veronica"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example": "Chen"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example": "ada@example.com"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number (optional).",
        json_schema_extra={"example": "+1-212-555-0199"},
    )
    password: str = Field(
        ...,
        description="Encrypted or hashed password string.",
        json_schema_extra={"example": "securePassword123!"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Veronica",
                    "last_name": "Chen",
                    "email": "vc@example.com",
                    "phone": "+1-212-555-0199",
                    "password": "securePassword123!"
                }
            ]
        }
    }


class UserCreate(UserBase):
    """Creation payload; all fields required except phone."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Veronica",
                    "last_name": "Chen",
                    "email": "vc@example.com",
                    "phone": "+1-646-555-9012",
                    "password": "mypassword2025!"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """Partial update; all fields optional."""
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Augusta"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "King"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "ada@newmail.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-646-000-0000"})
    password: Optional[str] = Field(None, json_schema_extra={"example": "newPassword2025!"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Ada", "last_name": "Byron"},
                {"email": "ada@newmail.com"},
                {"password": "newPassword2025!"},
            ]
        }
    }


class UserRead(UserBase):
    user_id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Person ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
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
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "first_name": "Veronica",
                    "last_name": "Chen",
                    "email": "vc@example.com",
                    "phone": "+1-212-555-0199",
                    "password": "securePassword123!",
                    "created_at": "2025-02-01T10:00:00Z",
                    "updated_at": "2025-02-05T12:30:00Z",
                }
            ]
        }
    }