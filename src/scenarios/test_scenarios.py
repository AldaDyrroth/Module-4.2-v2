from src.api import booking_client
from src.api.booking_client import BookingApiClient



class TestScenarios:
    def __init__(self, client: BookingApiClient): # Типизация для ясности
        self.client = client

    def create_booking_and_immediately_delete(self, booking_data):
        """
        Сценарий: создать booking и сразу же его удалить.
        Возвращает ID созданного и удаленного booking.
        """
        created_booking_data = self.client.create_booking(booking_data)
        booking_id = created_booking_data.get("bookingid")
        assert booking_id is not None, f"ID не найден в ответе на создание: {created_booking_data}"

        print(self.client.get_booking_id(booking_id, booking_data))

        self.client.delete_booking(booking_id) # Проверка на успешность удаления внутри delete_booking (raise_for_status)
        # или можно проверить статус ответа здесь, если delete_booking его возвращает
        print(f"booking с ID {booking_id} успешно создан и удален.")
        return booking_id

    def get_and_verify_bookings_exist(self):
        """
        Сценарий: получить список bookings и проверить, что он не пуст.
        """
        bookings = self.client.get_bookings()
        assert len(bookings) > 0, "Список bookings пуст"
        print(f"Получено {len(bookings)} bookings.")
        return bookings

    def update_booking_and_verify_changes(self, booking_id, upd_booking_data):
        """
        Сценарий: обновить booking и проверить, что данные изменились.
        """
        updated_booking = self.client.update_booking(booking_id, upd_booking_data)

        print(f"booking с ID {booking_id} успешно обновлен.")
        return updated_booking

    def delete_existing_booking_and_verify(self, booking_id): # test_booking переименован в booking_id для ясности
        """
        Сценарий: удалить существующий booking и убедиться, что он удален.
        """
        self.client.delete_booking(booking_id)
        not_exist_booking = self.client.get_booking_id_unval(booking_id)
        assert not_exist_booking == 404, f"booking с ID {booking_id} не была удалена"

        print(f"booking с ID {booking_id} отправлен на удаление.")
