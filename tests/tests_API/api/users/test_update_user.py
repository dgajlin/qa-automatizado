import pytest
from utils.settings import WEB_BASE_URL_API, USERS

@pytest.mark.parametrize("fields_to_update", [
    ("password",),
    ("full_name",),
    ("password", "full_name"),
])
@pytest.mark.user
def test_update_users(temporary_user, api_request, auth_headers, fields_to_update):
    user = temporary_user
    user_id = user["id"]
    email = user["email"]
    orig_password = user["password"]
    orig_fullname = user["full_name"]

    # Asignar nuevos valores
    new_password = "NewPass123"
    new_fullname = f"{orig_fullname} Updated"

    password = new_password if "password" in fields_to_update else orig_password
    fullname = new_fullname if "full_name" in fields_to_update else orig_fullname

    payload = {"user_id": user_id, "email": email, "password": password, "full_name": fullname}
    r = api_request(
        "PUT",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers,
        json=payload,
    )
    assert r.status_code == 200, f"update: {r.status_code} - {r.text}"

    api_request(
        "DELETE",
        f"{WEB_BASE_URL_API}{USERS}/{user_id}",
        headers=auth_headers
    )
