import pytest
from time import time
from faker import Faker
from utils.settings import WEB_BASE_URL_API, USERS

faker = Faker()

@pytest.mark.login
def test_delete_valid_user(temporary_user, auth_headers, api_request, fetch_all_elements):
    # Borrar usuario creado temporalmente
    user_id = temporary_user["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("username, expected", [
    (f"{faker.user_name()}{str(int(time()*100))[-6:]}@example.org", 204),    # usuario invalido
    ("", 204),                                                               # usuario no ingresado
])
@pytest.mark.user
def test_delete_invalid_users(username, expected, auth_headers, api_request):
    user_id = "usr-00000000"
    r = api_request(
        "GET",
        f"{WEB_BASE_URL_API}{USERS}",
        headers=auth_headers
    )
    assert r.status_code == 200, f"list_users devolvió {r.status_code}: {r.text}"
    users = r.json()
    # Buscar si el email existe en la lista
    found = next((u for u in users if u.get("email", "").lower() == username.lower()), None)
    if found:
        user_id = found.get("id")
    # Intentar borrar al usuario (inexistente o encontrado)
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"