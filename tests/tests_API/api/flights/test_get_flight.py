import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, FLIGHTS

faker = Faker()

@pytest.mark.flight
def test_get_valid_flight(temporary_flight, auth_headers, api_request):
    flight_id = temporary_flight["id"]
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"get: {r.status_code} - {r.text}"


@pytest.mark.parametrize("flight_id, expected", [
    (faker.unique.bothify(text="fl-######", letters=string.ascii_uppercase), 404),     # vuelo inválido
    ("", 200),                                                                         # vuelo no ingresado
])
@pytest.mark.flight
def test_get_invalid_flight(flight_id, expected, auth_headers, api_request):
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"get: {r.status_code} - {r.text}"