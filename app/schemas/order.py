from datetime import datetime
from typing import List
from pydantic import BaseModel
from pydantic.v1 import root_validator


class Order(BaseModel):
    items_id: List[str]
    address_id: str
    price: int
    delivery: int
    food_subtotal_discount: int
    payment_total: int
    points_earned: int
    payment_method: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(_, values):
        values["updated_at"] = datetime.now()
        return values

    def to_dict(self):
        return self.model_dump()
