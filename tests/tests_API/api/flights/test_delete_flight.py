import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, FLIGHTS

faker = Faker()

@pytest.mark.flight
def test_delete_valid_flight(temporary_flight, auth_headers, api_request):
    flight_id = temporary_flight["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"


@pytest.mark.parametrize("flight_id, expected", [
    (faker.unique.bothify(text="FL####", letters=string.ascii_uppercase), 204),     # vuelo inválido
    ("", 405),                                                                      # vuelo no ingresado
])
@pytest.mark.flight
def test_delete_invalid_flight(flight_id, expected, auth_headers, api_request):
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"
