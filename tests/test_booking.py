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

