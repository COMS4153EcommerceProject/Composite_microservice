from __future__ import annotations
import os
from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query, Header, Request, Depends
from fastapi.responses import JSONResponse
from starlette.responses import Response

from models.order import OrderCreate, OrderRead, OrderUpdate
from models.payment import PaymentCreate, PaymentRead, PaymentUpdate
from models.order_detail import OrderDetailCreate, OrderDetailRead, OrderDetailUpdate

from resources.order_resource import OrderResource
from resources.payment_resource import PaymentResource
from resources.order_detail_resource import OrderDetailResource
from utils.etag import generate_etag, etag_match
from services.order_processing_service import OrderProcessingService

import jwt
from jwt import PyJWKClient
import time
import requests

from google.cloud import pubsub_v1
import json
import os

port = int(os.environ.get("FASTAPIPORT", 8002))
# --------------------------------------------------------------------------
# JWT validation
# --------------------------------------------------------------------------
JWKS_URL = "https://auth-service-1056727803439.us-east4.run.app/.well-known/jwks.json"
jwks_client = PyJWKClient(JWKS_URL)
ISSUER = "https://auth-service-1056727803439.us-east4.run.app"
ALGORITHM = "RS256"
AUDIENCE = "local-api"
#
#
# def get_public_key(kid: str):
#     global JWKS_CACHE, JWKS_CACHE_TIMESTAMP
#
#     # 缓存过期或者缓存未命中
#     if time.time() - JWKS_CACHE_TIMESTAMP > JWKS_CACHE_TTL or kid not in JWKS_CACHE:
#         try:
#             jwks = requests.get(JWKS_URL).json()
#             JWKS_CACHE = {}
#             for key_dict in jwks.get("keys", []):
#                 jwk_obj = PyJWK.from_dict(key_dict)
#                 JWKS_CACHE[key_dict["kid"]] = jwk_obj.key
#             JWKS_CACHE_TIMESTAMP = time.time()
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to fetch JWKS: {str(e)}")
#
#     public_key = JWKS_CACHE.get(kid)
#     if public_key is None:
#         raise HTTPException(status_code=401, detail=f"Public key not found for kid: {kid}")
#
#     return public_key


def verify_jwt(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split()[1]

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        payload = jwt.decode(
            token,
            signing_key,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
        return payload

    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JWT verification error: {str(e)}")



PROJECT_ID = "aurora-coms4153-project"
TOPIC_ID = "order-events"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def publish_order_event(order):
    data_str = json.dumps({
        "order_id": str(order.order_id),
        "user_id": str(order.user_id),
        "total_price": order.total_price,
        "status": order.status
    })
    data_bytes = data_str.encode("utf-8")
    future = publisher.publish(topic_path, data=data_bytes)
    print(f"Published message ID: {future.result()}")


app = FastAPI(
    title="Order Management API",
    description="Microservice for managing user orders, payments, and order details",
    version="0.1.0"
    # dependencies=[Depends(verify_jwt)]
)


# --------------------------------------------------------------------------
# Order endpoints
# --------------------------------------------------------------------------
@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order: OrderCreate, user=Depends(verify_jwt)):
    """Create a new order"""
    new_order = OrderResource.create_order(order)
    etag = generate_etag(new_order)
    location = new_order.links.get("self", f"/orders/{new_order.order_id}")

    try:
        publish_order_event(new_order)
    except Exception as e:
        print(f"Failed to publish order event: {str(e)}")

    return JSONResponse(
        content=new_order.model_dump(mode='json'),
        status_code=201,
        headers={
            "Location": location,
            "ETag": etag
        }
    )


@app.get("/orders", response_model=List[OrderRead])
def list_orders(
        user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
        status: Optional[str] = Query(None, description="Filter by order status"),
        order_date_from: Optional[datetime] = Query(None, description="Filter orders from this date (inclusive)"),
        order_date_to: Optional[datetime] = Query(None, description="Filter orders up to this date (inclusive)"),
        min_total_price: Optional[float] = Query(None, ge=0,
                                                 description="Filter orders with total price >= this value"),
        max_total_price: Optional[float] = Query(None, ge=0,
                                                 description="Filter orders with total price <= this value"),
        sort_by: Optional[str] = Query(None,
                                       description="Sort by field: order_id, user_id, order_date, total_price, status, created_at, updated_at"),
        order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
        limit: Optional[int] = Query(None, ge=1, description="Maximum number of results to return"),
        offset: Optional[int] = Query(None, ge=0, description="Number of results to skip"),
):
    """Get all orders with optional filtering, sorting, and pagination"""
    return OrderResource.get_orders(
        user_id=user_id,
        status=status,
        order_date_from=order_date_from,
        order_date_to=order_date_to,
        min_total_price=min_total_price,
        max_total_price=max_total_price,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(
        order_id: UUID,
        if_none_match: Optional[str] = Header(None, alias="If-None-Match")
):
    """
    Get a specific order by ID with eTag support.

    - Returns 304 Not Modified if If-None-Match header matches current eTag
    - Returns order with ETag header for caching
    """
    order = OrderResource.get_order(order_id)
    current_etag = generate_etag(order)

    # Check If-None-Match header for conditional GET
    if if_none_match and etag_match(if_none_match, current_etag):
        return Response(status_code=304, headers={"ETag": current_etag})

    # Return order with ETag header
    return JSONResponse(
        content=order.model_dump(mode='json'),
        headers={"ETag": current_etag}
    )


@app.put("/orders/{order_id}", response_model=OrderRead)
def update_order(
        order_id: UUID,
        update: OrderUpdate,
        if_match: Optional[str] = Header(None, alias="If-Match")
):
    """
    Update an existing order with eTag support.

    - Requires If-Match header with current eTag
    - Returns 412 Precondition Failed if eTag doesn't match
    - Returns updated order with new ETag header
    """
    # Get current order to check eTag
    try:
        current_order = OrderResource.get_order(order_id)
    except HTTPException:
        raise

    current_etag = generate_etag(current_order)

    # Check If-Match header
    if if_match is None:
        raise HTTPException(
            status_code=428,
            detail="If-Match header required for updates"
        )

    if not etag_match(if_match, current_etag):
        raise HTTPException(
            status_code=412,
            detail="Precondition Failed: Resource has been modified. Please refresh and try again.",
            headers={"ETag": current_etag}
        )

    # Update the order
    updated_order = OrderResource.update_order(order_id, update)
    new_etag = generate_etag(updated_order)

    # Return updated order with new ETag header
    return JSONResponse(
        content=updated_order.model_dump(mode='json'),
        headers={"ETag": new_etag}
    )


@app.delete("/orders/{order_id}", response_model=OrderRead)
def delete_order(order_id: UUID):
    """Delete an order"""
    return OrderResource.delete_order(order_id)


# --------------------------------------------------------------------------
# Async Order Processing endpoints (202 Accepted example)
# --------------------------------------------------------------------------
@app.post("/orders/process", status_code=202)
def process_order_async(order: OrderCreate):
    """
    Process an order asynchronously.

    Returns 202 Accepted with a task ID and status URL for polling.
    The order will be processed in the background.
    Use the status URL to poll for completion status.
    """
    task_info = OrderProcessingService.start_order_processing(order)

    return JSONResponse(
        content={
            "task_id": task_info["task_id"],
            "status_url": task_info["status_url"],
            "message": "Order processing started. Poll the status URL for updates."
        },
        status_code=202,
        headers={
            "Location": task_info["status_url"]
        }
    )


@app.get("/tasks/{task_id}/status")
def get_task_status(task_id: UUID):
    """
    Poll the status of an asynchronous task.

    Returns the current status of the task:
    - pending: Task is queued but not yet started
    - processing: Task is currently being processed
    - completed: Task completed successfully (check result field for order_id)
    - failed: Task failed (check error field for details)
    """
    return OrderProcessingService.get_task_status(task_id)


# --------------------------------------------------------------------------
# Payment endpoints
# --------------------------------------------------------------------------
@app.post("/payments", response_model=PaymentRead, status_code=201)
def create_payment(payment: PaymentCreate):
    """Create a new payment"""
    new_payment = PaymentResource.create_payment(payment)
    etag = generate_etag(new_payment)
    location = new_payment.links.get("self", f"/payments/{new_payment.payment_id}")

    return JSONResponse(
        content=new_payment.model_dump(mode='json'),
        status_code=201,
        headers={
            "Location": location,
            "ETag": etag
        }
    )


@app.get("/payments", response_model=List[PaymentRead])
def list_payments(
        order_id: Optional[UUID] = Query(None, description="Filter by order ID"),
        payment_method: Optional[str] = Query(None, description="Filter by payment method"),
        payment_date_from: Optional[datetime] = Query(None, description="Filter payments from this date (inclusive)"),
        payment_date_to: Optional[datetime] = Query(None, description="Filter payments up to this date (inclusive)"),
        min_amount: Optional[float] = Query(None, ge=0, description="Filter payments with amount >= this value"),
        max_amount: Optional[float] = Query(None, ge=0, description="Filter payments with amount <= this value"),
        sort_by: Optional[str] = Query(None,
                                       description="Sort by field: payment_id, order_id, payment_method, payment_date, amount, created_at, updated_at"),
        order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
        limit: Optional[int] = Query(None, ge=1, description="Maximum number of results to return"),
        offset: Optional[int] = Query(None, ge=0, description="Number of results to skip"),
):
    """Get all payments with optional filtering, sorting, and pagination"""
    return PaymentResource.get_payments(
        order_id=order_id,
        payment_method=payment_method,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to,
        min_amount=min_amount,
        max_amount=max_amount,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


@app.get("/payments/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: UUID):
    """Get a specific payment by ID"""
    return PaymentResource.get_payment(payment_id)


@app.put("/payments/{payment_id}", response_model=PaymentRead)
def update_payment(payment_id: UUID, update: PaymentUpdate):
    """Update an existing payment"""
    return PaymentResource.update_payment(payment_id, update)


@app.delete("/payments/{payment_id}", response_model=PaymentRead)
def delete_payment(payment_id: UUID):
    """Delete a payment"""
    return PaymentResource.delete_payment(payment_id)


# --------------------------------------------------------------------------
# Order Detail endpoints
# --------------------------------------------------------------------------
@app.post("/order-details", response_model=OrderDetailRead, status_code=201)
def create_order_detail(order_detail: OrderDetailCreate):
    """Create a new order detail"""
    new_order_detail = OrderDetailResource.create_order_detail(order_detail)
    etag = generate_etag(new_order_detail)
    location = new_order_detail.links.get("self",
                                          f"/order-details/{new_order_detail.order_id}/{new_order_detail.prod_id}")

    return JSONResponse(
        content=new_order_detail.model_dump(mode='json'),
        status_code=201,
        headers={
            "Location": location,
            "ETag": etag
        }
    )


@app.get("/order-details", response_model=List[OrderDetailRead])
def list_order_details(
        order_id: Optional[UUID] = Query(None, description="Filter by order ID"),
        prod_id: Optional[UUID] = Query(None, description="Filter by product ID"),
        min_quantity: Optional[int] = Query(None, ge=1, description="Filter order details with quantity >= this value"),
        max_quantity: Optional[int] = Query(None, ge=1, description="Filter order details with quantity <= this value"),
        min_subtotal: Optional[float] = Query(None, ge=0,
                                              description="Filter order details with subtotal >= this value"),
        max_subtotal: Optional[float] = Query(None, ge=0,
                                              description="Filter order details with subtotal <= this value"),
        sort_by: Optional[str] = Query(None,
                                       description="Sort by field: order_id, prod_id, quantity, subtotal, created_at, updated_at"),
        order: Optional[str] = Query("asc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
        limit: Optional[int] = Query(None, ge=1, description="Maximum number of results to return"),
        offset: Optional[int] = Query(None, ge=0, description="Number of results to skip"),
):
    """Get all order details with optional filtering, sorting, and pagination"""
    return OrderDetailResource.get_order_details(
        order_id=order_id,
        prod_id=prod_id,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        min_subtotal=min_subtotal,
        max_subtotal=max_subtotal,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )


@app.get("/order-details/{order_id}/{prod_id}", response_model=OrderDetailRead)
def get_order_detail(order_id: UUID, prod_id: UUID):
    """Get a specific order detail by composite key (order_id, prod_id)"""
    return OrderDetailResource.get_order_detail(order_id, prod_id)


@app.put("/order-details/{order_id}/{prod_id}", response_model=OrderDetailRead)
def update_order_detail(order_id: UUID, prod_id: UUID, update: OrderDetailUpdate):
    """Update an existing order detail"""
    return OrderDetailResource.update_order_detail(order_id, prod_id, update)


@app.delete("/order-details/{order_id}/{prod_id}", response_model=OrderDetailRead)
def delete_order_detail(order_id: UUID, prod_id: UUID):
    """Delete an order detail"""
    return OrderDetailResource.delete_order_detail(order_id, prod_id)


# --------------------------------------------------------------------------
# Root
# --------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the Order Management API. See /docs for OpenAPI UI.",
        "version": "0.1.0",
        "entities": ["orders", "payments", "order-details"]
    }


# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)