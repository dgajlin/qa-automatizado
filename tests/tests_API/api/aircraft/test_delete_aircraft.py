import pytest
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRCRAFT

faker = Faker()

@pytest.mark.aircraft
def test_delete_valid_aircraft(temporary_aircraft, auth_headers, api_request, fetch_all_elements):
    # Borrar aeronave creada temporalmente
    aircraft_id = temporary_aircraft["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{aircraft_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("tail_number, expected", [
    (faker.unique.bothify(text="????", letters=string.ascii_uppercase), 204),    # aeronave invalida
    ("", 204),                                                                   # aeronave no ingresada
])
@pytest.mark.aircraft
def test_delete_invalid_aircraft(tail_number, expected, auth_headers, api_request):
    aircraft_id = "000"
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{AIRCRAFT}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"list_aircraft devolvió {r.status_code}: {r.text}"
    aircraft = r.json()
    # Buscar si la aeronave existe en la lista
    found = next((u for u in aircraft if u.get("aircraft_id", "") == aircraft_id), None)
    if found:
        tail_number = found.get("aircraft_id")
    # Intentar borrar la aeronave (inexistente o encontrado)
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{aircraft_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"