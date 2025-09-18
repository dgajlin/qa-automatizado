import pytest
import json
from utils.settings import WEB_BASE_URL_API, BOOKINGS

@pytest.mark.booking
def test_list_booking(auth_headers, api_request, fetch_all_elements):
    bookings, meta = fetch_all_elements(
        f"{WEB_BASE_URL_API}{BOOKINGS}",
        headers=auth_headers,
        limit=100,
    )

    # Troubleshooting
    #print(f"Cantidad de reservas: {len(bookings)}")
    #print(json.dumps(bookings, indent=2, ensure_ascii=False))

    # Assert explícito de 200 en TODAS las páginas
    assert meta["pages"] >= 1 or len(bookings) == 0, "No se obtuvo ninguna página"
    assert all(code == 200 for code in meta["status_codes"]), (
        f"Se encontraron errores en la API: {meta}"
    )