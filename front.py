from pydantic import BaseModel


class PrivateModel(BaseModel):
    name: str
    car_brand: str
    image: str
    hire_fee: int
    date_hire: str


class PublicModel(BaseModel):
    name: str
    location_from: str
    location_to: str
    passengers: int
    price: int


class TicketModel(BaseModel):
    location_from: str
    location_to: str
    bus_id: int
    