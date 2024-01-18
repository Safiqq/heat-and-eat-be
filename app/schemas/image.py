from pydantic import BaseModel


class Image(BaseModel):
    blob: str

    def to_dict(self):
        return self.model_dump()
