from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    goal: str
    gender: str
    birthdate: datetime
    height: int
    current_weight: float
    goal_weight: float

    def to_dict(self):
        return self.model_dump()
