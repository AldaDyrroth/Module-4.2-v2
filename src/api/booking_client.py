from src.api.constant import BASE_URL
from src.data_models.models import BookingResponse, BookingData
from src.utils.validator import validate_response
from tenacity import retry, stop_after_delay


class BookingApiClient:

    def __init__(self, auth_session):
        self.auth_session = auth_session
        self.base_url = BASE_URL  # Можно также передавать в конструктор, если он может меняться

    def create_booking(self, booking_data):
        create = self.auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        validate_response(create, model=BookingResponse, validate_expected_data=False, expected_data={"bookingid": create.json()["bookingid"], "booking": booking_data})
        return create.json()

    def full_create_booking(self, booking_data):
        create = self.auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        validate_response(create, model=BookingResponse, expected_data={"bookingid": create.json()["bookingid"], "booking": booking_data})
        return create.json()

    def get_bookings(self):
        response = self.auth_session.get(f"{BASE_URL}/booking")
        # validate_response(response, model=BookingResponse, expected_data=booking_data, is_list=True)
        return response.json()

    def get_booking_id(self, booking_id, booking_data):
        response = self.auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        validate_response(response, model=BookingData, expected_data=booking_data)
        return response.json()

    def get_booking_id_unval(self, booking_id):
        response = self.auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        return response.status_code()

    def update_booking(self, booking_id, upd_booking_data):
        response = self.auth_session.post(f"{BASE_URL}/booking/{booking_id}", json=upd_booking_data)
        validate_response(response, model=BookingData, expected_data=upd_booking_data)
        return response.json()

    def change_booking(self, booking_id, chng_booking_data):
        update = self.auth_session.post(f"{BASE_URL}/booking/{booking_id}", json=chng_booking_data)
        validate_response(update, model=BookingData, expected_data=chng_booking_data)
        return update.json()

    # @retry(stop=stop_after_delay(3))
    def delete_booking(self, booking_id):
        delete = self.auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        if delete.status_code not in (200, 204):
            delete.raise_for_status()
        return delete.status_code

        