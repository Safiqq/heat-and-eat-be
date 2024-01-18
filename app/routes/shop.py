from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from auth.jwt import get_current_user
from service import db
from schemas.shop import Shop

shop_router = APIRouter(tags=["Shops"])


@shop_router.post("/shops/")
async def create_shop(shop: Shop, _: dict = Depends(get_current_user)):
    _, doc = db.collection("shops").add(shop.to_dict())
    return {"message": f"Shop created successfully with ID {doc.id}"}


@shop_router.get("/shops/{shop_id}", response_model=dict)
async def read_shop_by_id(shop_id, _: dict = Depends(get_current_user)):
    shop = db.collection("shops").document(shop_id).get()
    if not shop.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shop with ID {shop_id} not found",
        )
    return {"id": shop.id, **shop.to_dict()}


@shop_router.get("/shops/", response_model=List[dict])
async def read_shops(_: dict = Depends(get_current_user)):
    shops = db.collection("shops").get()
    return [{"id": doc.id, **doc.to_dict()} for doc in shops]


@shop_router.patch("/shops/{shop_id}")
async def update_shop_by_id(
    shop_id: str, payload_shop: dict, _: dict = Depends(get_current_user)
):
    shop = db.collection("shops").document(shop_id).get()
    if not shop.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shop with ID {shop_id} not found",
        )
    db.collection("shops").document(shop_id).update(payload_shop)
    return {"message": f"Shop with ID {shop_id} updated successfully"}


@shop_router.delete("/shops/{shop_id}")
async def delete_shop_by_id(shop_id: str, _: dict = Depends(get_current_user)):
    shop = db.collection("shops").document(shop_id).get()
    if not shop.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shop with ID {shop_id} not found",
        )
    db.collection("shops").document(shop_id).delete()
    return {"message": f"Shop with ID {shop_id} deleted successfully"}
