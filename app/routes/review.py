from typing import List
from fastapi import APIRouter, Depends
from auth.jwt import get_current_user
from service import db
from schemas.review import Review
from google.cloud.firestore_v1.base_query import FieldFilter

review_router = APIRouter(tags=["Reviews"])


@review_router.post("/reviews/")
async def create_review(review: Review, user: dict = Depends(get_current_user)):
    _, doc = db.collection("reviews").add({"user_id": user["id"], **review.to_dict()})
    return {"message": f"Review created successfully with ID {doc.id}"}


@review_router.get("/reviews/{review_id}", response_model=dict)
async def read_review_by_id(review_id, _: dict = Depends(get_current_user)):
    review = db.collection("reviews").document(review_id).get()
    return {"id": review.id, **review.to_dict()}


@review_router.get("/reviews/", response_model=List[dict])
async def read_reviews(user: dict = Depends(get_current_user)):
    reviews = (
        db.collection("reviews")
        .where(filter=FieldFilter("user_id", "==", user["id"]))
        .get()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in reviews]


@review_router.patch("/reviews/{review_id}")
async def update_review_by_id(
    review_id: str, review: dict, _: dict = Depends(get_current_user)
):
    db.collection("reviews").document(review_id).update(review)
    return {"message": f"Review with ID {review_id} updated successfully"}


@review_router.delete("/reviews/{review_id}")
async def delete_review_by_id(review_id: str, _: dict = Depends(get_current_user)):
    db.collection("reviews").document(review_id).delete()
    return {"message": f"Review with ID {review_id} deleted successfully"}
