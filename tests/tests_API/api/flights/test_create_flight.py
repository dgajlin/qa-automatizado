import pytest
from datetime import datetime, timedelta
import string
from faker import Faker
from utils.settings import WEB_BASE_URL_API, FLIGHTS

faker = Faker()

@pytest.mark.flight
def test_create_flight(delete_flight, auth_headers, api_request, temporary_airport, temporary_aircraft):
    origin = temporary_airport["iata_code"]
    destination = faker.unique.bothify(text="???", letters=string.ascii_uppercase)
    # Crear aeropuerto destino aparte
    payload_dest = {"iata_code": destination, "city": faker.city(), "country": faker.country()}
    r_dest = api_request("POST", f"{WEB_BASE_URL_API}/airports", headers=auth_headers, json=payload_dest)
    assert r_dest.status_code == 201

    departure_time = datetime.now().isoformat() + "Z"
    arrival_time = (datetime.now() + timedelta(hours=2)).isoformat() + "Z"
    payload = {
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "base_price": 100,
        "aircraft_id": temporary_aircraft["id"],
    }
    r = api_request(
        "POST",
        f"{WEB_BASE_URL_API}{FLIGHTS}",
        headers=auth_headers,
        json=payload
    )
    flight_id = r.json().get('id')
    assert r.status_code == 201, f"Se esperaba '201' pero se obtuvo '{r.status_code}'"
    delete_flight(flight_id)