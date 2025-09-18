import pytest
from utils.settings import WEB_BASE_URL_API, FLIGHTS
from faker import Faker
import string

faker = Faker()

@pytest.mark.parametrize("fields_to_update", [
    ("orig",),
    ("destination"),
])
@pytest.mark.flight
def test_update_flight(temporary_flight, api_request, auth_headers, fields_to_update):
    flight = temporary_flight
    flight_id = flight["id"]
    orig_origin = flight["origin"]
    orig_destination = flight["destination"]
    orig_departure_time = flight["departure_time"]
    orig_arrival_time = flight["arrival_time"]
    orig_base_price = flight["base_price"]
    orig_aircraft_id = flight["aircraft_id"]

    # Asignar nuevos valores
    new_origin = faker.unique.bothify(text="???", letters=string.ascii_uppercase)
    new_destination = faker.unique.bothify(text="???", letters=string.ascii_uppercase)
    departure_time = orig_departure_time
    arrival_time = orig_arrival_time
    base_price = orig_base_price
    aircraft_id = orig_aircraft_id

    origin = new_origin if "origin" in fields_to_update else orig_origin
    destination = new_destination if "destination" in fields_to_update else orig_destination

    payload = {
        "origin": origin,
        "destination": destination,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "base_price": base_price,
        "aircraft_id": aircraft_id,
    }
    r = api_request(
        "PUT",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 200, f"update: {r.status_code} - {r.text}"

    api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{FLIGHTS}/{flight_id}",
        headers=auth_headers
    )
