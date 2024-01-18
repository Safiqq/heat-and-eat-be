from pydantic import BaseModel


class Shop(BaseModel):
    name: str

    def to_dict(self):
        return self.model_dump()
