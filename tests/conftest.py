import requests
import pytest
import random
from datetime import timedelta
from src.api.constant import HEADERS, BASE_URL
from src.data_models.models import BookingResponse, PatchBookingData
from typing import Dict, Any
from faker import Faker
faker = Faker()



@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"

    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def rndm_booking_id():
    session = requests.Session()
    response = session.get(f"{BASE_URL}/booking")
    assert response.status_code == 200, "Ошибка авторизации, статус код не 200"

    get_booking = response.json()
    id = random.choice(get_booking)["bookingid"]
    return id

@pytest.fixture(scope="session")
def booking_data():
    # # Сначала генерируем checkin, затем вычисляем checkout
    # checkin = faker.date_between(start_date='today', end_date='+1y')
    # checkout = checkin + timedelta(days=random.randint(1, 30))
    #
    # # Базовый набор данных (обязательные поля)
    # data: Dict[str, Any] = {
    #     "firstname": faker.first_name(),
    #     "lastname": faker.last_name(),
    #     "totalprice": faker.random_int(min=100, max=10000),
    #     "depositpaid": True,
    #     "bookingdates": {
    #         "checkin": checkin.strftime("%Y-%m-%d"),  # Преобразуем в строку
    #         "checkout": checkout.strftime("%Y-%m-%d")  # Преобразуем в строку
    #     }
    # }
    #
    # # С вероятностью 50% добавляем additionalneeds
    # if random.choice([True, False]):
    #     data["additionalneeds"] = faker.word().capitalize()
    #
    # return data
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }



@pytest.fixture(scope="session")
def upd_booking_data() -> BookingResponse:
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

    return BookingResponse(**data)

@pytest.fixture(scope="session")
def chng_booking_data() -> PatchBookingData:
    return PatchBookingData(
        firstname=faker.first_name(),
        lastname=faker.last_name(),
        totalprice=faker.random_int(min=100, max=10000)
    )