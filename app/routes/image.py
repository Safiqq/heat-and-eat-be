from fastapi import APIRouter, Depends
from auth.jwt import get_current_user
from service import db
from schemas.image import Image

image_router = APIRouter(tags=["Images"])


@image_router.post("/images/")
async def create_image(image: Image, user: dict = Depends(get_current_user)):
    _, doc = db.collection("images").add({"user_id": user["id"], **image.to_dict()})
    return {"message": f"Image created successfully with ID {doc.id}"}


@image_router.get("/images/{image_id}", response_model=dict)
async def read_image_by_id(image_id):
    image = db.collection("images").document(image_id).get()
    return {"id": image.id, **image.to_dict()}


@image_router.patch("/images/{image_id}")
async def update_image_by_id(
    image_id: str, image: dict, _: dict = Depends(get_current_user)
):
    db.collection("images").document(image_id).update(image)
    return {"message": f"Image with ID {image_id} updated successfully"}


@image_router.delete("/images/{image_id}")
async def delete_image_by_id(image_id: str, _: dict = Depends(get_current_user)):
    db.collection("images").document(image_id).delete()
    return {"message": f"Image with ID {image_id} deleted successfully"}
