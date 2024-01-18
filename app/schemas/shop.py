from pydantic import BaseModel


class Shop(BaseModel):
    name: str
    city: str

    def to_dict(self):
        return self.model_dump()
