import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRCRAFT

faker = Faker()

@pytest.mark.aircraft
def test_delete_valid_aircraft(temporary_aircraft, auth_headers, api_request):
    aircraft_id = temporary_aircraft["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{aircraft_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("aircraft_id, expected", [
    (faker.unique.bothify(text="????", letters=string.ascii_uppercase), 204),     # aeronave invalida
    ("", 405),                                                                    # aeronave no ingresada
])
@pytest.mark.aircraft
def test_delete_invalid_aircraft(aircraft_id, expected, auth_headers, api_request):
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{aircraft_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"