import pytest
from faker import Faker
from utils.settings import WEB_BASE_URL_API, USERS

faker = Faker()

@pytest.mark.login
def test_delete_valid_user(temporary_user, auth_headers, api_request):
    user_id = temporary_user["id"]
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers
    )
    assert r.status_code == 204, f"delete: {r.status_code} - {r.text}"

@pytest.mark.parametrize("user_id, expected", [
    ("usr-00000000", 204),      # usuario invalido
    ("", 204),                  # usuario no ingresado
])
@pytest.mark.user
def test_delete_invalid_user(user_id, expected, auth_headers, api_request):
    user_id = "usr-00000000"
    r = api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers
    )
    assert r.status_code == expected, f"delete: {r.status_code} - {r.text}"