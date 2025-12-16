from __future__ import annotations
import os
from datetime import datetime
from uuid import UUID
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid

import requests
from fastapi import FastAPI, HTTPException, status, Response

from models.address import AddressRead, AddressCreate, AddressUpdate
from models.preference import PreferenceRead, PreferenceCreate, PreferenceUpdate
from models.product import ProductRead, ProductCreate
from models.user import UserRead, UserUpdate, UserCreate
from models.user_address import UserAddressRead
from models.composite import CheckoutRequest
# -------------------------------------------------------------------
# automic microservice urls
# -------------------------------------------------------------------
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "https://user-service-1056727803439.europe-west1.run.app")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://136.116.101.124:8080")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "https://product-service-1056727803439.us-central1.run.app")
port = int(os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="Composite Microservice",
    description="Composite service that orchestrates User, Order, and Product services.",
    version="0.1.0",
    servers=[
        {
            "url": "https://composite-microservice-1056727803439.us-east4.run.app",
            "description": "Cloud Run"
        }
    ],
)

executor = ThreadPoolExecutor(max_workers=10)

operations_store: Dict[str, Dict[str, Any]] = {}



# -------------------------------------------------------------------
# Helper
# -------------------------------------------------------------------
def _check(resp: requests.Response, name: str):
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    if not resp.ok:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream error from {name} ({resp.status_code})"
        )
    return resp.json()
# -------------------------------------------------------------------
# A) Proxy endpoints (re-expose atomic microservice APIs)
# -------------------------------------------------------------------
'''
Proxy for user
'''
@app.post("/composite/users", response_model=UserRead)
def proxy_create_user(user: UserCreate):
    """Proxy: create a user via the User Service."""
    resp = requests.post(
        f"{USER_SERVICE_URL}/users",
        json=user.model_dump(mode="json")
    )
    return _check(resp, "User")


@app.get("/composite/users", response_model=list[UserRead])
def proxy_list_users(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
):
    """Proxy: list users via the User Service."""
    params = {
        k: v for k, v in {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }.items() if v is not None
    }

    resp = requests.get(
        f"{USER_SERVICE_URL}/users",
        params=params
    )
    return _check(resp, "User list")


@app.get("/composite/users/{user_id}", response_model=UserRead)
def proxy_get_user(user_id: UUID):
    """Proxy: get a single user via the User Service."""
    resp = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    return _check(resp, "User")


@app.patch("/composite/users/{user_id}", response_model=UserRead)
def proxy_update_user(user_id: UUID, update: UserUpdate):
    """Proxy: update a user via the User Service."""
    resp = requests.patch(
        f"{USER_SERVICE_URL}/users/{user_id}",
        json=update.model_dump(mode="json", exclude_none=True)
    )
    return _check(resp, "User")


@app.delete("/composite/users/{user_id}", status_code=204)
def proxy_delete_user(user_id: UUID):
    """Proxy: delete a user via the User Service."""
    resp = requests.delete(f"{USER_SERVICE_URL}/users/{user_id}")

    if resp.status_code == 204:
        return Response(status_code=204)

    return _check(resp, "User")

'''
proxy for address
'''
@app.post("/composite/addresses", response_model=AddressRead, status_code=201)
def proxy_create_address(address: AddressCreate):
    """Proxy: create an address via the User Service."""
    resp = requests.post(
        f"{USER_SERVICE_URL}/addresses",
        json=address.model_dump(mode="json")
    )
    return _check(resp, "Address")

@app.get("/composite/addresses", response_model=List[AddressRead])
def proxy_list_addresses(
    street: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
):
    """Proxy: list addresses via the User Service."""
    params = {
        k: v for k, v in {
            "street": street,
            "city": city,
            "state": state,
            "postal_code": postal_code,
        }.items() if v is not None
    }

    resp = requests.get(
        f"{USER_SERVICE_URL}/addresses",
        params=params
    )
    return _check(resp, "Address list")

@app.get("/composite/addresses/{address_id}", response_model=AddressRead)
def proxy_get_address(address_id: UUID):
    """Proxy: get a single address via the User Service."""
    resp = requests.get(
        f"{USER_SERVICE_URL}/addresses/{address_id}"
    )
    return _check(resp, "Address")

@app.patch("/composite/addresses/{address_id}", response_model=AddressRead)
def proxy_update_address(address_id: UUID, update: AddressUpdate):
    """Proxy: update an address via the User Service."""
    resp = requests.patch(
        f"{USER_SERVICE_URL}/addresses/{address_id}",
        json=update.model_dump(mode="json", exclude_none=True)
    )
    return _check(resp, "Address")

@app.delete("/composite/addresses/{address_id}", status_code=204)
def proxy_delete_address(address_id: UUID):
    """Proxy: delete an address via the User Service."""
    resp = requests.delete(
        f"{USER_SERVICE_URL}/addresses/{address_id}"
    )

    if resp.status_code == 204:
        return Response(status_code=204)

    return _check(resp, "Address")

'''
proxy for preferences
'''
@app.post("/composite/preferences", response_model=PreferenceRead, status_code=201)
def proxy_create_preference(pref: PreferenceCreate):
    """Proxy: create a preference via the User Service."""
    resp = requests.post(
        f"{USER_SERVICE_URL}/preferences",
        json=pref.model_dump(mode="json")
    )
    return _check(resp, "Preference")

@app.get("/composite/preferences", response_model=List[PreferenceRead])
def proxy_list_preferences(
    language: Optional[str] = None,
    currency: Optional[str] = None,
):
    """Proxy: list preferences via the User Service."""
    params = {
        k: v for k, v in {
            "language": language,
            "currency": currency,
        }.items() if v is not None
    }

    resp = requests.get(
        f"{USER_SERVICE_URL}/preferences",
        params=params
    )
    return _check(resp, "Preference list")

@app.get("/composite/preferences/{user_id}", response_model=PreferenceRead)
def proxy_get_preference(user_id: UUID):
    """Proxy: get a preference via the User Service."""
    resp = requests.get(
        f"{USER_SERVICE_URL}/preferences/{user_id}"
    )
    return _check(resp, "Preference")

@app.patch("/composite/preferences/{user_id}", response_model=PreferenceRead)
def proxy_update_preference(user_id: UUID, update: PreferenceUpdate):
    """Proxy: update a preference via the User Service."""
    resp = requests.patch(
        f"{USER_SERVICE_URL}/preferences/{user_id}",
        json=update.model_dump(mode="json", exclude_none=True)
    )
    return _check(resp, "Preference")

@app.delete("/composite/preferences/{user_id}", status_code=204)
def proxy_delete_preference(user_id: UUID):
    """Proxy: delete a preference via the User Service."""
    resp = requests.delete(
        f"{USER_SERVICE_URL}/preferences/{user_id}"
    )

    if resp.status_code == 204:
        return Response(status_code=204)

    return _check(resp, "Preference")

'''
proxy for user_address
'''
@app.get(
    "/composite/user_addresses/{user_id}/{addr_id}",
    response_model=UserAddressRead,
)
def proxy_get_user_address(user_id: UUID, addr_id: UUID):
    """Proxy: get a user-address mapping via the User Service."""
    resp = requests.get(
        f"{USER_SERVICE_URL}/user_addresses/{user_id}/{addr_id}"
    )
    return _check(resp, "UserAddress")


@app.delete(
    "/composite/user_addresses/{user_id}/{addr_id}",
    status_code=204,
)
def proxy_delete_user_address(user_id: UUID, addr_id: UUID):
    """Proxy: delete a user-address mapping via the User Service."""
    resp = requests.delete(
        f"{USER_SERVICE_URL}/user_addresses/{user_id}/{addr_id}"
    )

    if resp.status_code == 204:
        return Response(status_code=204)

    return _check(resp, "UserAddress")

'''
proxy for product
'''
@app.post(
    "/composite/products",
    response_model=ProductRead,
    status_code=201,
    tags=["Composite Product"],
)
def proxy_create_product(product: ProductCreate):
    """Proxy: create a product via the Product Service."""
    resp = requests.post(
        f"{PRODUCT_SERVICE_URL}/products",
        json=product.model_dump(mode="json")
    )
    return _check(resp, "Product")
@app.get(
    "/composite/products",
    response_model=List[ProductRead],
    tags=["Composite Product"],
)
def proxy_list_products(
    category_id: Optional[UUID] = None,
    inventory_id: Optional[UUID] = None,
):
    """Proxy: list products via the Product Service."""
    params = {
        k: v for k, v in {
            "category_id": category_id,
            "inventory_id": inventory_id,
        }.items() if v is not None
    }

    resp = requests.get(
        f"{PRODUCT_SERVICE_URL}/products",
        params=params
    )
    return _check(resp, "Product list")


@app.get("/composite/products/{product_id}")
def proxy_get_product(product_id: UUID):
    """Proxy: get a single product via the Product Service."""
    resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    return _check(resp, "Product")


@app.get("/composite/orders/{order_id}")
def proxy_get_order(order_id: UUID):
    """Proxy: get a single order via the Order Service."""
    resp = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
    return _check(resp, "Order")


@app.get("/composite/products/{product_id}/inventory")
def proxy_get_inventory(product_id: UUID):
    """
    Proxy: get inventory for a product via the Product Service.
    Uses the /products/{product_id}/inventory endpoint of the Product service.
    """
    resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}/inventory")
    return _check(resp, "Inventory")

# -------------------------------------------------------------------
# 1) Checkout
# -------------------------------------------------------------------
@app.post("/composite/users/{user_id}/checkout", status_code=201)
def checkout(user_id: UUID, body: CheckoutRequest):
    user_resp = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    user_json = _check(user_resp, "User")

    items_info: List[Dict[str, Any]] = []

    for item in body.items:
        product_id = item.product_id

        p_resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        product = _check(p_resp, "Product")


        inv_resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}/inventory")
        inventory = _check(inv_resp, "Inventory")

        if inventory["stock_quantity"] < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product_id}"
            )

        line_total = product["price"] * item.quantity

        items_info.append({
            "product_id": product["product_id"],
            "product": product,
            "inventory": inventory,
            "quantity": item.quantity,
            "line_total": line_total,
        })

    # Create the order
    total_price = sum(i["line_total"] for i in items_info)
    order_payload = {
        "user_id": str(user_id),
        "order_date": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "total_price": total_price,
        "status": "PENDING",
    }
    order_resp = requests.post(f"{ORDER_SERVICE_URL}/orders", json=order_payload)
    order_json = _check(order_resp, "Order")
    order_id = order_json["order_id"]

    # Create corresponding OrderDetail for each order
    details_out = []
    for item in items_info:
        detail_payload = {
            "order_id": order_id,
            "prod_id": item["product_id"],
            "quantity": item["quantity"],
            "subtotal": item["line_total"],
        }

        d_resp = requests.post(
            f"{ORDER_SERVICE_URL}/order-details",
            json=detail_payload
        )
        detail_json = _check(d_resp, "OrderDetail")
        details_out.append(detail_json)

        # Decrease the inventory
        new_qty = item["inventory"]["stock_quantity"] - item["quantity"]
        inv_update_payload = {"stock_quantity": new_qty}

        inv_up_resp = requests.put(
            f"{PRODUCT_SERVICE_URL}/inventories/{item['product_id']}",
            json=inv_update_payload,
        )
        _check(inv_up_resp, "InventoryUpdate")

    # Create payment (default method: credit card?)
    pay_payload = {
        "order_id": order_id,
        "payment_method": "CREDIT_CARD",
        "payment_date": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "amount": total_price,
    }
    pay_resp = requests.post(f"{ORDER_SERVICE_URL}/payments", json=pay_payload)
    payment_json = _check(pay_resp, "Payment")

    return {
        "user": user_json,
        "order": order_json,
        "order_details": details_out,
        "payment": payment_json,
    }


@app.get("/composite/users/{user_id}/order-summary")
def order_summary(user_id: UUID):

    def f_user():
        resp = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
        return _check(resp, "User")

    def f_pref():
        resp = requests.get(f"{USER_SERVICE_URL}/preferences/{user_id}")
        if resp.status_code == 404:
            return None
        return _check(resp, "Preference")

    def f_addresses():
        resp = requests.get(
            f"{USER_SERVICE_URL}/user_addresses",
            params={"user_id": str(user_id)}
        )
        mappings = _check(resp, "UserAddress")

        out = []
        for m in mappings:
            addr_id = m["addr_id"]
            ar = requests.get(f"{USER_SERVICE_URL}/addresses/{addr_id}")

            if ar.status_code == 404:
                continue

            addr_json = _check(ar, "Address")
            out.append(addr_json)

        return out

    def f_orders():
        resp = requests.get(
            f"{ORDER_SERVICE_URL}/orders",
            params={"user_id": str(user_id)}
        )
        if not resp.ok:
            return []
        return resp.json()

    futures = {
        executor.submit(f_user): "user",
        executor.submit(f_pref): "pref",
        executor.submit(f_addresses): "addr",
        executor.submit(f_orders): "orders",
    }

    data: Dict[str, Any] = {}
    for f in as_completed(futures):
        key = futures[f]
        data[key] = f.result()

    enriched_orders = []

    def enrich(order):
        oid = order["order_id"]

        pay_r = requests.get(f"{ORDER_SERVICE_URL}/payments", params={"order_id": oid})
        payments = pay_r.json() if pay_r.ok else []

        det_r = requests.get(f"{ORDER_SERVICE_URL}/order-details", params={"order_id": oid})
        details = det_r.json() if det_r.ok else []

        for d in details:
            pid = d["prod_id"]
            p_r = requests.get(f"{PRODUCT_SERVICE_URL}/products/{pid}")
            if p_r.ok:
                d["product"] = p_r.json()
            i_r = requests.get(f"{PRODUCT_SERVICE_URL}/inventories/{pid}")
            if i_r.ok:
                d["inventory"] = i_r.json()

        return {
            "order": order,
            "payments": payments,
            "details": details,
        }

    futures2 = {executor.submit(enrich, o): o["order_id"] for o in data["orders"]}
    for fs in as_completed(futures2):
        enriched_orders.append(fs.result())

    return {
        "user": data["user"],
        "preference": data.get("pref"),
        "addresses": data["addr"],
        "orders": enriched_orders,
    }



@app.post("/composite/reports/user-orders", status_code=202)
def generate_report(user_id: UUID):
    op_id = str(uuid.uuid4())
    operations_store[op_id] = {"status": "PENDING", "result": None}

    def job():
        try:
            r = order_summary(user_id)
            operations_store[op_id] = {"status": "COMPLETED", "result": r}
        except Exception as e:
            operations_store[op_id] = {"status": "FAILED", "error": str(e)}

    executor.submit(job)
    return {"operation_id": op_id, "status": "PENDING"}


@app.get("/composite/reports/user-orders/{operation_id}")
def get_report(operation_id: str):
    if operation_id not in operations_store:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operations_store[operation_id]
# double check

@app.get("/favicon.ico")
def favicon():
    return {}, 204


# -------------------------------------------------------------------
# Root
# -------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Composite service ready. Orchestrating User/Order/Product."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)