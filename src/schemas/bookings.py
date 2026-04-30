from datetime import date
from pydantic import BaseModel, Field


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int

class Booking(BookingAdd):
    id: int



# class BookingPatch(BaseModel):
#     room_id: int | None = Field(None)
#     user_id: int | None = Field(None)
#     date_from: date | None = Field(None)
#     date_to: date | None = Field(None)
#     price: int | None = Field(None)