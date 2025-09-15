import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRPORTS

faker = Faker()

@pytest.mark.parametrize("iata_code, city, country, expected",
    [
        # iata_code, city y country validos
        (faker.unique.bothify(text="???", letters=string.ascii_uppercase), faker.city(), faker.country(), 201),
    ],
)
@pytest.mark.airport
def test_create_airport(delete_airport, auth_headers, api_request, iata_code, city, country, expected):
    payload = {"iata_code": iata_code, "city": city, "country": country}
    r = api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AIRPORTS}",
        headers=auth_headers,
        json=payload
    )
    assert r.status_code == expected, f"Se esperaba '{expected}' pero se obtuvo '{r.status_code}'"
    delete_airport(iata_code)