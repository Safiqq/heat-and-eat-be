from typing import List
from pydantic import BaseModel


class Review(BaseModel):
    item_id: str
    shop_id: str
    review: str
    rating: int
    images_id: List[str]

    def to_dict(self):
        return self.model_dump()
