from pydantic import BaseModel, ValidationError
from requests import Response
from typing import Type
import pytest


def validate_response(
    response: Response,
    model: Type[BaseModel],
    expected_status: int = 200,
    validate_expected_data: bool = True,
    expected_data: dict | None = None
) -> BaseModel:
    """
    Универсальный валидатор ответа API:
    - Проверка status_code
    - Валидация схемы через Pydantic
    - Сравнение с ожидаемыми данными (опционально)

    :return: объект модели
    """
    if response.status_code != expected_status:
        pytest.fail(f"Expected status {expected_status}, got {response.status_code}: {response.text}")

    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка парсинга JSON: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data)
    except ValidationError as e:
        pytest.fail(f"Pydantic валидация не прошла:\n{e}")

    if expected_data:
        if validate_expected_data == True:
        # Обернём данные в такую же модель для сравнения
            expected_model = model(**expected_data)
            expected_model.model_dump(exclude_unset=True)

        if parsed.model_dump(exclude_unset=True) != expected_data:
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_data}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed
