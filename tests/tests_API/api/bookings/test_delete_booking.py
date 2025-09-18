import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, BOOKINGS

faker = Faker()

@pytest.mark.booking
def test_delete_valid_booking(temporary_booking, auth_headers, api_request):
    booking_id = temporary_booking["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{BOOKINGS}/{booking_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("booking_id, expected", [
    (faker.unique.bothify(text="BKG####", letters=string.ascii_uppercase), 404),    # reserva inválida
    ("", 405),                                                                      # reserva no ingresada
])
@pytest.mark.booking
def test_delete_invalid_booking(booking_id, expected, auth_headers, api_request):
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{BOOKINGS}/{booking_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"
