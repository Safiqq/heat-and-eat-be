from typing import List
from fastapi import APIRouter, Depends
from auth.jwt import get_current_user
from service import db
from schemas.order import Order
from google.cloud.firestore_v1.base_query import FieldFilter

order_router = APIRouter(tags=["Orders"])


@order_router.post("/orders/")
async def create_order(order: Order, user: dict = Depends(get_current_user)):
    _, doc = db.collection("orders").add({"user_id": user["id"], **order.to_dict()})
    return {"message": f"Order created successfully with ID {doc.id}"}


@order_router.get("/orders/{order_id}", response_model=dict)
async def read_order_by_id(order_id, _: dict = Depends(get_current_user)):
    order = db.collection("orders").document(order_id).get()
    return {"id": order.id, **order.to_dict()}


@order_router.get("/orders/", response_model=List[dict])
async def read_orders(user: dict = Depends(get_current_user)):
    orders = (
        db.collection("orders")
        .where(filter=FieldFilter("user_id", "==", user["id"]))
        .get()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in orders]


@order_router.patch("/orders/{order_id}")
async def update_order_by_id(
    order_id: str, order: dict, _: dict = Depends(get_current_user)
):
    db.collection("orders").document(order_id).update(order)
    return {"message": f"Order with ID {order_id} updated successfully"}


@order_router.delete("/orders/{order_id}")
async def delete_order_by_id(order_id: str, _: dict = Depends(get_current_user)):
    db.collection("orders").document(order_id).delete()
    return {"message": f"Order with ID {order_id} deleted successfully"}
