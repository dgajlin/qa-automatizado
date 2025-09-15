import pytest
import json
from utils.settings import WEB_BASE_URL_API, FLIGHTS

@pytest.mark.flight
def test_list_flight(auth_headers, api_request):
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{FLIGHTS}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"list_flights devolvió {r.status_code}: {r.text}"
    flights = r.json()

    print(f"Cantidad de vuelos: {len(flights)}")
    print(json.dumps(flights, indent=2, ensure_ascii=False))

    # Asegurar que sea lista
    assert isinstance(flights, list), "La API no devolvió una lista de vuelos"

