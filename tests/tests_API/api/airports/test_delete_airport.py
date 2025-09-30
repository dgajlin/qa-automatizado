import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRPORTS

faker = Faker()

@pytest.mark.airport
def test_delete_valid_airport(temporary_airport, auth_headers, api_request):
    iata_code = temporary_airport["iata_code"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"


@pytest.mark.parametrize("iata_code, expected", [
    (faker.unique.bothify(text="???", letters=string.ascii_uppercase), 204),     # aeropuerto invalido
    ("", 405),                                                                   # aeropuerto no ingresado
])
@pytest.mark.airport
def test_delete_invalid_airport(iata_code, expected, auth_headers, api_request):
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"