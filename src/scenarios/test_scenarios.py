import pytest
import random

from src.enums.api_data import BaseRequest
from src.api.booking_client import BookingApiClient


@pytest.fixture()
def rndm_booking_id(auth_session):
    response = auth_session.get(f"{BaseRequest.BASE_URL.value}/booking")
    assert response.status_code == 200, "Ошибка авторизации, статус код не 200"

    get_booking = response.json()
    id = random.choice(get_booking)["bookingid"]
    return id


class Scenarios:
    def __init__(self, client: BookingApiClient): # Типизация для ясности
        self.client = client

    def create_booking_and_immediately_delete(self, booking_data):
        """
        Сценарий: создать booking, проверить доступность по API и сразу же его удалить.
        Возвращает ID созданного и удаленного booking.
        """
        created_booking_data = self.client.create_booking(booking_data)
        booking_id = created_booking_data.get("bookingid")
        assert booking_id is not None, f"ID не найден в ответе на создание: {created_booking_data}"

        new_booking = self.client.get_booking_id(booking_id, booking_data)
        assert new_booking is not None, f"Booking недоступен по API"
        print(f"Booking с ID {booking_id} получен через API.", end=" ")

        self.client.delete_booking(booking_id) # Проверка на успешность удаления внутри delete_booking (raise_for_status)
        # или можно проверить статус ответа здесь, если delete_booking его возвращает
        print(f"Booking с ID {booking_id} успешно создан и удален.")
        return booking_id

    def get_and_verify_bookings_exist(self):
        """
        Сценарий: получить список bookings и проверить, что он не пуст.
        """
        bookings = self.client.get_bookings()
        assert len(bookings) > 0, "Список bookings пуст"
        print(f"Получено {len(bookings)} bookings.")

        return bookings

    def update_booking_and_verify_changes(self, upd_booking_data):
        """
        Сценарий: обновить booking и проверить, что данные изменились.
        """
        booking_id = self.client.get_random_booking_id()

        updated_booking = self.client.update_booking(booking_id, upd_booking_data)
        print(f"Booking с ID {booking_id} успешно обновлен.")

        return updated_booking

    def delete_existing_booking_and_verify(self): # test_booking переименован в booking_id для ясности
        """
        Сценарий: удалить существующий booking и убедиться, что он удален.
        """

        booking_id = self.client.get_random_booking_id()

        remove_booking = self.client.delete_booking(booking_id)
        assert remove_booking.status_code == 201, f"booking с ID {booking_id} не была удалена."

        self.client.get_booking_id_noval(404, booking_id)

        print(f"Booking с ID {booking_id} успешно удален.")

class NegativeScenarios:
    def __init__(self, client: BookingApiClient): # Типизация для ясности
        self.client = client

    def create_booking_with_invalid_payload(self, data):
        """
        Сценарий: создать booking, проверить доступность по API и сразу же его удалить.
        Возвращает ID созданного и удаленного booking.
        """

        self.client.create_booking_noval(500, data)
        print(f"Booking не создан из-за отсутствия поля {data[1]}.", end=" ")

    def get_removed_booking(self):
        """
        Сценарий: Попытаться получить данные удаленного booking.
        """
        booking_id = self.client.get_random_booking_id()

        self.client.delete_booking(booking_id) # удаляем booking

        booking = self.client.get_booking_id_noval(404, booking_id)
        print(f"Booking с ID {booking_id} удален и недоступен по API.")

        return booking

    def update_non_existent_booking(self, upd_booking_data):
        """
        Сценарий: Попытаться обновить данные удаленного booking
        """
        booking_id = self.client.get_random_booking_id()

        self.client.delete_booking(booking_id)  # удаляем booking

        updated_booking = self.client.update_booking_noval(405, booking_id, upd_booking_data)
        print(f"Booking с ID {booking_id} удален и недоступен для обновления по API.")

        return updated_booking

    def update_without_token(self, upd_booking_data): # test_booking переименован в booking_id для ясности
        """
        Сценарий: Обновить booking без токена c предварительной проверкой данных.
        """

        booking_id = self.client.get_random_booking_id()

        chosen_booking = self.client.get_booking_id_noval(200, booking_id)
        expected_booking = chosen_booking.json()

        self.client.update_booking_noval(403, booking_id, upd_booking_data, {"Cookie": f"token=111"})

        self.client.get_booking_id(booking_id, expected_booking)

        print(f"Booking с ID {booking_id} не получилось обновить без токена.")
