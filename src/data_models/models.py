from pydantic import BaseModel
from typing import Optional
from typing import List


class BookingDates(BaseModel):
    checkin: str
    checkout: str

class BookingData(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

class BookingResponse(BaseModel):
    bookingid: int
    booking: BookingData

class BookingItem(BaseModel):
    bookingid: int

class PatchBookingData(BaseModel):
    firstname: str
    lastname: str
    totalprice: int