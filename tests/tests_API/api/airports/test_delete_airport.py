import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRPORTS

faker = Faker()

@pytest.mark.airport
def test_delete_valid_airport(temporary_airport, auth_headers, api_request, fetch_all_elements):
    # Borrar aeropuerto creado temporalmente
    iata_code = temporary_airport["iata_code"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("iata_code, expected", [
    (faker.unique.bothify(text="???", letters=string.ascii_uppercase), 204),    # aeropuerto invalido
])
@pytest.mark.airport
def test_delete_invalid_airport(iata_code, expected, auth_headers, api_request):
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{AIRPORTS}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"list_airports devolvió {r.status_code}: {r.text}"
    airports = r.json()
    # Buscar si el aeropuerto existe en la lista
    found = next((u for u in airports if u.get("iata_code", "") == iata_code), None)
    if found:
        iata_code = found.get("iata_code")
    # Intentar borrar al aeropuerto (inexistente o encontrado)
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRPORTS}/{iata_code}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"