import pytest
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AIRCRAFT

faker = Faker()

@pytest.mark.parametrize("tail_number, model, capacity, expected",
    [
        # tail_number, model y capacity validos
        ("LV-FKN", "Airbus 370", 96, 201),
    ],
)
@pytest.mark.aircraft
def test_create_aircraft(delete_aircraft, auth_headers, api_request, tail_number, model, capacity, expected):
    payload = {"tail_number": tail_number, "model": model, "capacity": capacity}
    r = api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AIRCRAFT}",
        headers=auth_headers,
        json=payload
    )
    assert r.status_code == expected, f"Se esperaba '{expected}' pero se obtuvo '{r.status_code}'"
    delete_aircraft(tail_number)