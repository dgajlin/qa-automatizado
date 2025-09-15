import pytest
import json
from utils.settings import WEB_BASE_URL_API, AIRCRAFT

@pytest.mark.aircraft
def test_list_aircraft(auth_headers, fetch_all_elements):
    # Para Troubleshooting
    aircraft, meta = fetch_all_elements(
        f"{WEB_BASE_URL_API}{AIRCRAFT}",
        headers=auth_headers,
        limit=100,
    )
    print(f"Cantidad de aeronaves: {len(aircraft)}")
    print(json.dumps(aircraft, indent=2, ensure_ascii=False))

    # Assert explícito de 200 en TODAS las páginas
    assert meta["pages"] >= 1 or len(aircraft) == 0, "No se obtuvo ninguna página"
    assert all(code == 200 for code in meta["status_codes"]), (
        f"Se encontraron errores en la API: {meta}"
    )
