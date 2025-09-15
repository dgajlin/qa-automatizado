import pytest
import json
from utils.settings import WEB_BASE_URL_API, USERS

@pytest.mark.user
def test_list_users(auth_headers, fetch_all_elements):
    # Para Troubleshooting
    users, meta = fetch_all_elements(
        f"{WEB_BASE_URL_API}{USERS}",
        headers=auth_headers,
        limit=100,
    )
    print(f"Cantidad de usuarios: {len(users)}")
    print(json.dumps(users, indent=2, ensure_ascii=False))

    # Assert explícito de 200 en TODAS las páginas
    assert meta["pages"] >= 1, "No se obtuvo ninguna página"
    assert all(code == 200 for code in meta["status_codes"]), (
        f"Se encontraron errores en la API: {meta}"
    )
