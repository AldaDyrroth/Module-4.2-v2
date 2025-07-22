from pydantic import BaseModel
from typing import Optional
from typing import List
from faker import Faker
import random
from datetime import timedelta
from typing import Dict, Any


faker = Faker()


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


class Generators:

    @staticmethod
    def booking_data():
        # Сначала генерируем checkin, затем вычисляем checkout
        checkin = faker.date_between(start_date='today', end_date='+1y')
        checkout = checkin + timedelta(days=random.randint(1, 30))

        # Базовый набор данных (обязательные поля)
        data: Dict[str, Any] = {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "totalprice": faker.random_int(min=100, max=10000),
            "depositpaid": True,
            "bookingdates": {
                "checkin": checkin.strftime("%Y-%m-%d"),  # Преобразуем в строку
                "checkout": checkout.strftime("%Y-%m-%d")  # Преобразуем в строку
            }
        }

        # С вероятностью 50% добавляем additionalneeds
        if random.choice([True, False]):
            data["additionalneeds"] = faker.word().capitalize()

        return BookingData(**data).model_dump()

    @staticmethod
    def invalid_booking_data(booking_data):
        list_of_keys = booking_data()
        params = list_of_keys.keys()
        el = faker.random_element(params)
        list_of_keys.pop(el) # убираем случайное поле из тела запроса
        return [list_of_keys, el]

    @staticmethod
    def update_booking_data():
        # Сначала генерируем checkin, затем вычисляем checkout
        checkin = faker.date_between(start_date='today', end_date='+1y')
        checkout = checkin + timedelta(days=random.randint(1, 30))

        # Базовый набор данных (обязательные поля)
        data: Dict[str, Any] = {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "totalprice": faker.random_int(min=100, max=10000),
            "depositpaid": True,
            "bookingdates": {
                "checkin": checkin.strftime("%Y-%m-%d"),  # Преобразуем в строку
                "checkout": checkout.strftime("%Y-%m-%d")  # Преобразуем в строку
            }
        }

        # С вероятностью 50% добавляем additionalneeds
        if random.choice([True, False]):
            data["additionalneeds"] = faker.word().capitalize()

        return BookingData(**data).model_dump()