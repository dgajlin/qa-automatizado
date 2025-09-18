import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRPORTS

faker = Faker()

@pytest.mark.airport
def test_get_valid_airport(temporary_airport, auth_headers, api_request):
    airport_id = temporary_airport["iata_code"]
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{airport_id}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"get: {r.status_code} - {r.text}"

@pytest.mark.parametrize("iata_code, expected", [
    (faker.unique.bothify(text="###", letters=string.ascii_uppercase), 404),     # aeropuerto inválido
    ("", 200),                                                                   # aeropuerto no ingresado
])
@pytest.mark.airport
def test_get_invalid_airport(iata_code, expected, auth_headers, api_request):
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"get: {r.status_code} - {r.text}"