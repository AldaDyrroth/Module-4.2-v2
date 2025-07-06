import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent  # tests/.. → корень проекта
sys.path.append(str(root_dir))

import requests
import pytest
import random
from datetime import timedelta
from src.api.constant import Par
from src.data_models.models import BookingResponse, PatchBookingData
from typing import Dict, Any
from faker import Faker
from dotenv import load_dotenv
import os


load_dotenv()
faker = Faker()



@pytest.fixture(scope="session")
def auth_session():
    """
    Создаёт сессию с авторизацией и возвращает объект сессии.
    """
    session = requests.Session()
    session.headers.update(Par.HEADERS.value)

    auth_response = session.post(f"{Par.BASE_URL.value}/auth", json={"username": os.getenv('APP_USERNAME'), "password": os.getenv('PASSWORD')})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"

    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def rndm_booking_id():
    session = requests.Session()
    response = session.get(f"{Par.BASE_URL.value}/booking")
    assert response.status_code == 200, "Ошибка авторизации, статус код не 200"

    get_booking = response.json()
    id = random.choice(get_booking)["bookingid"]
    return id

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