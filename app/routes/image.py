import base64
import io
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from auth.jwt import get_current_user
from service import db
from schemas.image import Image

image_router = APIRouter(tags=["Images"])


@image_router.post("/images/")
async def create_image(image: Image, _: dict = Depends(get_current_user)):
    _, doc = db.collection("images").add(image.to_dict())
    return {"message": f"Image created successfully with ID {doc.id}"}


@image_router.get("/images/{image_id}", response_model=dict)
async def read_image_by_id(image_id):
    image = db.collection("images").document(image_id).get()
    if not image.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found",
        )
    image_content = base64.b64decode(image.get("blob"))
    return StreamingResponse(io.BytesIO(image_content), media_type="image/jpeg", headers={"Content-Disposition": f"inline; filename={image_id}.jpeg"})


@image_router.patch("/images/{image_id}")
async def update_image_by_id(
    image_id: str, payload_image: dict, _: dict = Depends(get_current_user)
):
    image = db.collection("images").document(image_id).get()
    if not image.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found",
        )
    db.collection("images").document(image_id).update(payload_image)
    return {"message": f"Image with ID {image_id} updated successfully"}


@image_router.delete("/images/{image_id}")
async def delete_image_by_id(image_id: str, _: dict = Depends(get_current_user)):
    image = db.collection("images").document(image_id).get()
    if not image.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found",
        )
    db.collection("images").document(image_id).delete()
    return {"message": f"Image with ID {image_id} deleted successfully"}
