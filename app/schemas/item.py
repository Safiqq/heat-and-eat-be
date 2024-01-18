from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    image_id: str
    name: str
    description: str
    price: int
    calorie: int
    shop_id: str
    reviews_id: List[str]

    def to_dict(self):
        return self.model_dump()
