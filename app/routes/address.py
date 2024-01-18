from typing import List
from fastapi import APIRouter, Depends
from auth.jwt import get_current_user
from service import db
from schemas.address import Address
from google.cloud.firestore_v1.base_query import FieldFilter

address_router = APIRouter(tags=["Addresses"])


@address_router.post("/addresses/")
async def create_address(address: Address, user: dict = Depends(get_current_user)):
    _, doc = db.collection("addresses").add(
        {"user_id": user["id"], **address.to_dict()}
    )
    return {"message": f"Address created successfully with ID {doc.id}"}


@address_router.get("/addresses/{address_id}", response_model=dict)
async def read_address_by_id(address_id, _: dict = Depends(get_current_user)):
    address = db.collection("addresses").document(address_id).get()
    return {"id": address.id, **address.to_dict()}


@address_router.get("/addresses/", response_model=List[dict])
async def read_addresses(user: dict = Depends(get_current_user)):
    addresses = (
        db.collection("addresses")
        .where(filter=FieldFilter("user_id", "==", user["id"]))
        .get()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in addresses]


@address_router.patch("/addresses/{address_id}")
async def update_address_by_id(
    address_id: str, address: dict, _: dict = Depends(get_current_user)
):
    db.collection("addresses").document(address_id).update(address)
    return {"message": f"Address with ID {address_id} updated successfully"}


@address_router.delete("/addresses/{address_id}")
async def delete_address_by_id(address_id: str, _: dict = Depends(get_current_user)):
    db.collection("addresses").document(address_id).delete()
    return {"message": f"Address with ID {address_id} deleted successfully"}
