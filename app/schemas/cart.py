from typing import List
from pydantic import BaseModel


class Cart(BaseModel):
    items_id: List[str]

    def to_dict(self):
        return self.model_dump()
