import pytest
from time import time
from faker import Faker
from utils.settings import WEB_BASE_URL_API, AUTH_SIGNUP

faker = Faker()

@pytest.mark.parametrize("username, password, fullname, expected",
    [
        # usuario, password y full_name validos
        (f"{faker.user_name()}{str(int(time()*100))[-6:]}@example.org", faker.password(length=10, special_chars=False), faker.name(), 201),
    ],
)
@pytest.mark.user
def test_signup(delete_user, api_request, username, password, fullname, expected):
    payload = {"email": username, "password": password, "full_name": fullname}
    r = api_request(
        "POST",
        f"{WEB_BASE_URL_API}{AUTH_SIGNUP}",
        json=payload
    )
    assert r.status_code == expected, f"Se esperaba '{expected}' pero se obtuvo '{r.status_code}'"
    user_id = r.json().get('id')
    delete_user(user_id)