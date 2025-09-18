import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, BOOKINGS

faker = Faker()

@pytest.mark.booking
def test_create_booking(delete_booking, auth_headers, api_request, temporary_flight):
    flight_id = temporary_flight["id"]
    passenger = {
        "full_name": faker.name(),
        "passport": faker.bothify(text="??######", letters=string.ascii_uppercase),
        "seat": faker.bothify(text="##?", letters="ABCDEF"),
    }
    payload = {
        "flight_id": flight_id,
        "passengers": [passenger]
    }
    r = api_request(
        "POST",
        f"{WEB_BASE_URL_API}{BOOKINGS}",
        headers=auth_headers,
        json=payload
    )
    booking_id = r.json().get("id")
    assert r.status_code == 201, f"Se esperaba '201' pero se obtuvo '{r.status_code}'"
    booking = r.json()
    assert booking["flight_id"] == flight_id
    assert booking["passengers"][0]["full_name"] == passenger["full_name"]
    delete_booking(booking_id)
