from src.enums.api_data import BaseRequest
from src.data_models.models import BookingResponse, BookingData
from src.utils.validator import validate_response
from faker import Faker

fake = Faker()


class BookingApiClient:

    def __init__(self, auth_session):
        self.auth_session = auth_session
        self.BASE_URL = BaseRequest.BASE_URL.value  # Можно также передавать в конструктор, если он может меняться

    def create_booking(self, booking_data):
        create = self.auth_session.post(f"{BaseRequest.BASE_URL.value}/booking", json=booking_data)
        validate_response(create, model=BookingResponse, validate_expected_data=False, expected_data={"bookingid": create.json()["bookingid"], "booking": booking_data})
        return create.json()

    def create_booking_noval(self, expected_status, booking_data):
        create = self.auth_session.post(f"{BaseRequest.BASE_URL.value}/booking", json=booking_data)
        assert create.status_code == expected_status, f"Expected status {expected_status}, got {create.status_code}: {create.text}"
        return create



    def get_bookings(self):
        response = self.auth_session.get(f"{BaseRequest.BASE_URL.value}/booking")
        # validate_response(response, model=BookingResponse, expected_data=booking_data, is_list=True)
        return response.json()

    def get_booking_id(self, booking_id, booking_data):
        response = self.auth_session.get(f"{BaseRequest.BASE_URL.value}/booking/{booking_id}")
        validate_response(response, model=BookingData, expected_data=booking_data)
        return response.json()

    def get_random_booking_id(self):
        list_bookings = self.auth_session.get(f"{BaseRequest.BASE_URL.value}/booking").json()
        booking_id = fake.random_element(list_bookings)["bookingid"]
        return booking_id

    def get_booking_id_noval(self, expected_status, booking_id):
        response = self.auth_session.get(f"{BaseRequest.BASE_URL.value}/booking/{booking_id}")
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}: {response.text}"
        return response



    def update_booking(self, booking_id, upd_booking_data):
        response = self.auth_session.put(f"{BaseRequest.BASE_URL.value}/booking/{booking_id}", json=upd_booking_data)
        validate_response(response, model=BookingData, expected_data=upd_booking_data)
        return response

    def update_booking_noval(self, expected_status, booking_id, upd_booking_data, headers: dict = {}):
        self.auth_session.headers.update(headers)
        response = self.auth_session.put(f"{BaseRequest.BASE_URL.value}/booking/{booking_id}", json=upd_booking_data)
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}: {response.text}"
        return response



    def change_booking(self, booking_id, chng_booking_data):
        update = self.auth_session.patch(f"{BaseRequest.BASE_URL.value}/booking/{booking_id}", json=chng_booking_data)
        validate_response(update, model=BookingData, expected_data=chng_booking_data)
        return update.json()



    def delete_booking(self, booking_id):
        delete = self.auth_session.delete(f"{BaseRequest.BASE_URL.value}/booking/{booking_id}")
        if delete.status_code != 201:
            delete.raise_for_status()
        return delete

        