from tests.conftest import booking_data
from src.scenarios.test_scenarios import TestScenarios
from src.api.booking_client import BookingApiClient

class TestBookings:

    def test_working(self):
        assert 1 + 1 == 2

    def test_booking_creation(self, auth_session, booking_data):
        client = BookingApiClient(auth_session)
        booking = TestScenarios(client)

        booking.create_booking_and_immediately_delete(booking_data)

        # Assert-проверки
        # assert isinstance(booking, BookingResponse)
        print(booking)
        # assert booking != 1
        assert booking.bookingdates.checkout > booking.bookingdates.checkin

        # def test_get_booking_id(self, auth_session, booking_id):

        # def test_get_booking(self, ):

    def test_booking_delete(self, auth_session, rndm_booking_id):
        client = BookingApiClient(auth_session)
        booking = TestScenarios(client)

        booking.delete_existing_booking_and_verify(rndm_booking_id)
