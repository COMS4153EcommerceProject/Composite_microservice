from __future__ import annotations
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of an asynchronous task"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatusRead(BaseModel):
    """Model for reading task status"""
    task_id: UUID = Field(
        ...,
        description="Unique task ID",
        json_schema_extra={"example": "750e8400-e29b-41d4-a716-446655440000"}
    )
    status: TaskStatus = Field(
        ...,
        description="Current status of the task",
        json_schema_extra={"example": "processing"}
    )
    created_at: datetime = Field(
        ...,
        description="When the task was created",
        json_schema_extra={"example": "2025-01-16T10:20:30Z"}
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
        json_schema_extra={"example": "2025-01-16T10:21:00Z"}
    )
    result: Optional[Dict[str, Any]] = Field(
        None,
        description="Result of the task when completed (e.g., order_id)",
        json_schema_extra={"example": {"order_id": "550e8400-e29b-41d4-a716-446655440000"}}
    )
    error: Optional[str] = Field(
        None,
        description="Error message if task failed",
        json_schema_extra={"example": "Order processing failed"}
    )
    links: Dict[str, str] = Field(
        default_factory=dict,
        description="Relative path links to related resources",
        json_schema_extra={
            "example": {
                "self": "/tasks/750e8400-e29b-41d4-a716-446655440000",
                "status": "/tasks/750e8400-e29b-41d4-a716-446655440000/status"
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "750e8400-e29b-41d4-a716-446655440000",
                    "status": "processing",
                    "created_at": "2025-01-16T10:20:30Z",
                    "updated_at": "2025-01-16T10:21:00Z",
                    "result": None,
                    "error": None,
                    "links": {
                        "self": "/tasks/750e8400-e29b-41d4-a716-446655440000",
                        "status": "/tasks/750e8400-e29b-41d4-a716-446655440000/status"
                    }
                }
            ]
        }
    }


class TaskAcceptedResponse(BaseModel):
    """Response model for 202 Accepted"""
    task_id: UUID = Field(
        ...,
        description="Unique task ID for tracking the async operation",
        json_schema_extra={"example": "750e8400-e29b-41d4-a716-446655440000"}
    )
    status_url: str = Field(
        ...,
        description="URL to poll for task status",
        json_schema_extra={"example": "/tasks/750e8400-e29b-41d4-a716-446655440000/status"}
    )
    message: str = Field(
        ...,
        description="Message describing the async operation",
        json_schema_extra={"example": "Order processing started. Poll the status URL for updates."}
    )
    links: Dict[str, str] = Field(
        default_factory=dict,
        description="Relative path links to related resources",
        json_schema_extra={
            "example": {
                "status": "/tasks/750e8400-e29b-41d4-a716-446655440000/status",
                "self": "/tasks/750e8400-e29b-41d4-a716-446655440000"
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "750e8400-e29b-41d4-a716-446655440000",
                    "status_url": "/tasks/750e8400-e29b-41d4-a716-446655440000/status",
                    "message": "Order processing started. Poll the status URL for updates.",
                    "links": {
                        "status": "/tasks/750e8400-e29b-41d4-a716-446655440000/status",
                        "self": "/tasks/750e8400-e29b-41d4-a716-446655440000"
                    }
                }
            ]
        }
    }

