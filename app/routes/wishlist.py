from fastapi import APIRouter, Depends
from schemas.wishlist import Wishlist
from auth.jwt import get_current_user
from service import db

wishlist_router = APIRouter(tags=["Wishlists"])


@wishlist_router.get("/wishlist/", response_model=dict)
async def read_wishlist(user: dict = Depends(get_current_user)):
    wishlist = db.collection("wishlists").document(user["id"]).get()
    if not wishlist.exists:
        db.collection("wishlists").document(user["id"]).set({"items_id": []})
    return {"id": wishlist.id, **wishlist.to_dict()}


@wishlist_router.patch("/wishlist/")
async def update_wishlist(wishlist: Wishlist, user: dict = Depends(get_current_user)):
    db.collection("wishlists").document(user["id"]).set(wishlist.to_dict())
    return {"message": f"Wishlist for user {user['id']} updated successfully"}
