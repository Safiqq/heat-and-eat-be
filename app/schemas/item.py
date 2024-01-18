from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: int
    calory: int
    shop_id: str
    reviews_id: List[str]

    def to_dict(self):
        return self.model_dump()
