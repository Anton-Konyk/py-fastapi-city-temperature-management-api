from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    author_id: int


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
