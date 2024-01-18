from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from auth.jwt import get_current_user
from service import db
from schemas.item import Item

item_router = APIRouter(tags=["Items"])


@item_router.post("/items/")
async def create_item(item: Item, _: dict = Depends(get_current_user)):
    _, doc = db.collection("items").add(item.to_dict())
    return {"message": f"Item created successfully with ID {doc.id}"}


@item_router.get("/items/{item_id}", response_model=dict)
async def read_item_by_id(item_id, _: dict = Depends(get_current_user)):
    item = db.collection("items").document(item_id).get()
    if not item.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return {"id": item.id, **item.to_dict()}


@item_router.get("/items/", response_model=List[dict])
async def read_items(_: dict = Depends(get_current_user)):
    items = db.collection("items").get()
    return [{"id": doc.id, **doc.to_dict()} for doc in items]


@item_router.patch("/items/{item_id}")
async def update_item_by_id(
    item_id: str, payload_item: dict, _: dict = Depends(get_current_user)
):
    item = db.collection("items").document(item_id).get()
    if not item.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    db.collection("items").document(item_id).update(payload_item)
    return {"message": f"Item with ID {item_id} updated successfully"}


@item_router.delete("/items/{item_id}")
async def delete_item_by_id(item_id: str, _: dict = Depends(get_current_user)):
    item = db.collection("items").document(item_id).get()
    if not item.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    db.collection("items").document(item_id).delete()
    return {"message": f"Item with ID {item_id} deleted successfully"}
