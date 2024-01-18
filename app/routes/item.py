from typing import List
from fastapi import APIRouter, Depends
from auth.jwt import get_current_user
from service import db
from schemas.item import Item
from google.cloud.firestore_v1.base_query import FieldFilter

item_router = APIRouter(tags=["Items"])


@item_router.post("/items/")
async def create_item(item: Item, user: dict = Depends(get_current_user)):
    _, doc = db.collection("items").add({"user_id": user["id"], **item.to_dict()})
    return {"message": f"Item created successfully with ID {doc.id}"}


@item_router.get("/items/{item_id}", response_model=dict)
async def read_item_by_id(item_id, _: dict = Depends(get_current_user)):
    item = db.collection("items").document(item_id).get()
    return {"id": item.id, **item.to_dict()}


@item_router.get("/items/", response_model=List[dict])
async def read_items(user: dict = Depends(get_current_user)):
    items = (
        db.collection("items")
        .where(filter=FieldFilter("user_id", "==", user["id"]))
        .get()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in items]


@item_router.patch("/items/{item_id}")
async def update_item_by_id(
    item_id: str, item: dict, _: dict = Depends(get_current_user)
):
    db.collection("items").document(item_id).update(item)
    return {"message": f"Item with ID {item_id} updated successfully"}


@item_router.delete("/items/{item_id}")
async def delete_item_by_id(item_id: str, _: dict = Depends(get_current_user)):
    db.collection("items").document(item_id).delete()
    return {"message": f"Item with ID {item_id} deleted successfully"}
