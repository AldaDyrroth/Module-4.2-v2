import pytest

from src.scenarios.negative_scenarios import NegativeScenarios
from src.scenarios.test_scenarios import Scenarios
from src.api.booking_client import BookingApiClient
from src.data_models.models import Generators

@pytest.fixture
def booking_engine(auth_session):
    client = BookingApiClient(auth_session)
    return Scenarios(client)

@pytest.fixture
def negative_booking_engine(auth_session):
    client = BookingApiClient(auth_session)
    return NegativeScenarios(client)


class TestBookings:

    def test_positive_booking_creation(self, booking_engine):
        booking_engine.create_booking_and_immediately_delete(Generators.booking_data())

    def test_positive_get_bookings(self, booking_engine):
        booking_engine.get_and_verify_bookings_exist()

    def test_positive_update_random_booking(self, booking_engine):
        booking_engine.update_booking_and_verify_changes(Generators.update_booking_data())

    def test_positive_delete_random_booking(self, booking_engine):
        booking_engine.delete_existing_booking_and_verify()

    def test_negative_fail_creation_booking(self, negative_booking_engine):
        negative_booking_engine.create_booking_with_invalid_payload(Generators.booking_data())

    def test_negative_get_removed_booking(self, negative_booking_engine):
        negative_booking_engine.get_removed_booking()

    def test_negative_without_token_update_booking(self, negative_booking_engine):
        negative_booking_engine.update_without_token(Generators.update_booking_data())