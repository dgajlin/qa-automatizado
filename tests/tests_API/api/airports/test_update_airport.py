import pytest
from utils.settings import WEB_BASE_URL_API, AIRPORTS

@pytest.mark.parametrize("fields_to_update", [
    ("city",),
    ("country",),
    ("city", "country"),
])
@pytest.mark.airport
def test_update_airport(temporary_airport, api_request, auth_headers, fields_to_update):
    airport = temporary_airport
    iata_code = airport["iata_code"]
    orig_city = airport["city"]
    orig_country = airport["country"]

    # Asignacion de nuevos valores
    new_city = f"{orig_city} Updated"
    new_country = f"{orig_country} Updated"

    city = new_city if "city" in fields_to_update else orig_city
    country = new_country if "country" in fields_to_update else orig_country

    payload = {"iata_code": iata_code, "city": city, "country": country}
    r = api_request(
        "PUT",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 200, f"update: {r.status_code} - {r.text}"

    api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
