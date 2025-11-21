from __future__ import annotations
from uuid import UUID
from typing import List
from pydantic import BaseModel, Field

class CheckoutItem(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]

class OperationStatus(BaseModel):
    operation_id: str
    status: str
