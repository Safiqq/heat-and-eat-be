from fastapi import APIRouter, Depends
from schemas.cart import Cart
from auth.jwt import get_current_user
from service import db

cart_router = APIRouter(tags=["Carts"])


@cart_router.get("/cart/", response_model=dict)
async def read_cart(user: dict = Depends(get_current_user)):
    cart = db.collection("carts").document(user["id"]).get()
    if not cart.exists:
        db.collection("carts").document(user["id"]).set({"items_id": []})
    return {"id": cart.id, **cart.to_dict()}


@cart_router.patch("/cart/")
async def update_cart(cart: Cart, user: dict = Depends(get_current_user)):
    db.collection("carts").document(user["id"]).set(cart.to_dict())
    return {"message": f"Cart for user {user['id']} updated successfully"}
