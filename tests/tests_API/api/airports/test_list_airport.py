import pytest
import json
from utils.settings import WEB_BASE_URL_API, AIRPORTS

@pytest.mark.airport
def test_list_airports(auth_headers, fetch_all_elements):
    airports, meta = fetch_all_elements(
        f"{WEB_BASE_URL_API}{AIRPORTS}",
        headers=auth_headers,
        limit=100,
    )

    # Troubleshooting
    #print(f"Cantidad de aeropuertos: {len(airports)}")
    #print(json.dumps(airports, indent=2, ensure_ascii=False))

    # Assert explícito de 200 en TODAS las páginas
    assert meta["pages"] >= 1 or len(airports) == 0, "No se obtuvo ninguna página"
    assert all(code == 200 for code in meta["status_codes"]), (
        f"Se encontraron errores en la API: {meta}"
    )
