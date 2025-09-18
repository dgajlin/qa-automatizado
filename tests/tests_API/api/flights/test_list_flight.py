import pytest
import json
from utils.settings import WEB_BASE_URL_API, FLIGHTS

@pytest.mark.flight
def test_list_flight(auth_headers, api_request, fetch_all_elements):
    flights, meta = fetch_all_elements(
        f"{WEB_BASE_URL_API}{FLIGHTS}",
        headers=auth_headers,
        limit=100,
    )

    print(f"Cantidad de vuelos: {len(flights)}")
    print(json.dumps(flights, indent=2, ensure_ascii=False))

    # Assert explícito de 200 en TODAS las páginas
    assert meta["pages"] >= 1 or len(flights) == 0, "No se obtuvo ninguna página"
    assert all(code == 200 for code in meta["status_codes"]), (
        f"Se encontraron errores en la API: {meta}"
    )

