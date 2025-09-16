import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, FLIGHTS

faker = Faker()

@pytest.mark.flight
def test_delete_valid_flight(temporary_flight, auth_headers, api_request, fetch_all_elements):
    # Borrar vuelo creado temporalmente
    flight_id = temporary_flight["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("flight_number, expected", [
    (faker.unique.bothify(text="FL####", letters=string.ascii_uppercase), 204),  # vuelo inválido
    ("", 204),                                                                   # vuelo no ingresado
])
@pytest.mark.flight
def test_delete_invalid_flight(flight_number, expected, auth_headers, api_request):
    flight_id = "000"
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{FLIGHTS}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"list_flights devolvió {r.status_code}: {r.text}"
    flights = r.json()
    if isinstance(flights, dict) and "flights" in flights:
        flights = flights["flights"]
    # Buscar si el vuelo existe en la lista
    found = next((u for u in flights if u.get("id", "") == flight_id), None)
    if found:
        flight_id = found.get("id")
    # Intentar borrar el vuelo (inexistente o encontrado)
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"
