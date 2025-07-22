from src.enums.api_data import BaseRequest

import requests
import pytest

from dotenv import load_dotenv
from pathlib import Path
import os
import sys


root_dir = Path(__file__).parent.parent  # tests/.. → корень проекта
sys.path.append(str(root_dir))


load_dotenv()

@pytest.fixture(scope="session")
def auth_session():
    """
    Создаёт сессию с авторизацией и возвращает объект сессии.
    """
    session = requests.Session()
    session.headers.update(BaseRequest.HEADERS.value)

    auth_response = session.post(f"{BaseRequest.BASE_URL.value}/auth", json={"username": os.getenv('APP_USERNAME'), "password": os.getenv('PASSWORD')})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"

    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session



