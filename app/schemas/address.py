from pydantic import BaseModel


class Address(BaseModel):
    name: str
    phone_number: str
    province: str
    city: str
    district: str
    subdistrict: str
    street_address: str
    detail: str
    postcode: str

    def to_dict(self):
        return self.model_dump()
