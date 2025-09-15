import pytest
from utils.settings import WEB_BASE_URL_API, AIRCRAFT

@pytest.mark.parametrize("fields_to_update", [
    ("model",),
    ("capacity"),
    ("model", "capacity"),
])
@pytest.mark.aircraft
def test_update_aircraft(temporary_aircraft, api_request, auth_headers, fields_to_update):
    aircraft = temporary_aircraft
    aircraft_id = aircraft["id"]
    tail_number = aircraft["tail_number"]
    orig_model = aircraft["model"]
    orig_capacity = aircraft["capacity"]

    # Asignacion de nuevos valores
    new_model = f"{orig_model} Updated"
    new_capacity = f"{orig_capacity + 100}"

    model = new_model if "city" in fields_to_update else orig_model
    capacity = new_capacity if "country" in fields_to_update else orig_capacity

    payload = {"tail_number": tail_number, "model": model, "capacity": capacity}
    r = api_request(
        "PUT",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{aircraft_id}",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 200, f"update: {r.status_code} - {r.text}"

    api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{AIRCRAFT}/{tail_number}",
        headers=auth_headers
    )
